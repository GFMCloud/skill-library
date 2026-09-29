#!/usr/bin/env bash
# Acceptance for turn-reduction. Every check is run against a known-bad input and a
# known-good input and must distinguish them. A check that has not been shown to go red
# has not been shown to be a check — so each red case also asserts the reason it went red,
# not merely that it did.
#
# Usage:  bash plugins/turn-reduction/tests/run-tests.sh
# Exit:   0 all assertions held, 1 otherwise.

set -u

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FIXTURES="$PLUGIN_ROOT/tests/fixtures"
PREFLIGHT="$PLUGIN_ROOT/skills/capability-preflight/preflight.py"
LINT="$PLUGIN_ROOT/skills/output-lint/output_lint.py"
AUTHZ="$PLUGIN_ROOT/skills/standing-authorization/authz.py"
EXAMPLE_AUTHZ="$PLUGIN_ROOT/skills/standing-authorization/authorization.example.json"

PASS=0
FAIL=0
OUT=""

scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
mkdir -p "$scratch/repo"
printf 'seed\n' > "$scratch/seed.txt"
git -C "$scratch/repo" init -q
export PREFLIGHT_TEST_DIR="$scratch"

# run <expected-exit> <label> -- <command...>
run() {
  local expected="$1" label="$2"
  shift 3
  OUT="$("$@" 2>&1)"
  local actual=$?
  if [ "$actual" -eq "$expected" ]; then
    printf '  ok    %s (exit %d)\n' "$label" "$actual"
    PASS=$((PASS + 1))
  else
    printf '  FAIL  %s (expected exit %d, got %d)\n' "$label" "$expected" "$actual"
    printf '%s\n' "$OUT" | sed 's/^/          /'
    FAIL=$((FAIL + 1))
  fi
}

# because <substring> — asserts the last run's output explains itself
because() {
  if printf '%s' "$OUT" | grep -qF -- "$1"; then
    PASS=$((PASS + 1))
  else
    printf '  FAIL  reason not found in output: %s\n' "$1"
    FAIL=$((FAIL + 1))
  fi
}

echo "capability-preflight"
run 0 "green manifest passes" -- python3 "$PREFLIGHT" "$FIXTURES/preflight/green.manifest.json"
because "PRE-FLIGHT PASSED"
because "UNREACHABLE (verified)"

run 1 "red manifest blocks" -- python3 "$PREFLIGHT" "$FIXTURES/preflight/red-runtime.manifest.json"
because "BLOCKERS — 4"
because "INCONCLUSIVE"                 # exit 0 that examined nothing
because "NOT DISCRIMINATING"           # negative control that could not fail
because "FALSE-ARCHITECTURAL-CLAIM"    # unreachable claim the system refuted

run 2 "malformed manifest rejected before anything runs" -- \
  python3 "$PREFLIGHT" "$FIXTURES/preflight/red-manifest.manifest.json"
because "MANIFEST REJECTED — nothing was run."
because "command contains ||"
because "missing 'negative_control'"
because "'excludes' must be a non-empty string"
because "needs a 'probe'"

echo
echo "output-lint"
run 0 "green message passes" -- python3 "$LINT" "$FIXTURES/output-lint/green.md"
because "PASS — 0 errors, 0 warning(s)"
because "NOT CHECKED"

run 1 "red message fails" -- python3 "$LINT" "$FIXTURES/output-lint/red.md"
because "[placeholder]"
because "[interpreter]"
because "[cwd]"
because "[glob]"
because "[announced-write]"
because "[uncited-count]"

echo
echo "standing-authorization"
run 0 "shipped example validates" -- python3 "$AUTHZ" validate "$EXAMPLE_AUTHZ"
because "VALID — 0 errors, 0 warning(s)"

run 1 "defective file fails" -- \
  python3 "$AUTHZ" validate "$FIXTURES/standing-authorization/red-authorization.json"
because "which is not defined in 'ceilings'"
because "has no 'value'"
because "names a ceiling in prose but binds none"
because "'log_to' must name where the action is logged"
because "appears in both granted"

run 1 "ceiling defined twice is caught at parse time" -- \
  python3 "$AUTHZ" validate "$FIXTURES/standing-authorization/red-duplicate-ceiling.json"
because "duplicate key 'commits_before_review'"

run 1 "asking for a granted action is a defect" -- \
  python3 "$AUTHZ" check "$EXAMPLE_AUTHZ" --ask "These are ready — should I commit them to the feature branch?"
because "ALREADY-GRANTED"

run 0 "asking about a stop-listed action is correct" -- \
  python3 "$AUTHZ" check "$EXAMPLE_AUTHZ" --ask "Do you want me to force push the rebased branch?"
because "STOP-LISTED"

run 0 "asking about something uncovered is correct" -- \
  python3 "$AUTHZ" check "$EXAMPLE_AUTHZ" --ask "Which league season should the backfill start from?"
because "NOT-COVERED"

echo
echo "work-board"
WB="$PLUGIN_ROOT/skills/work-board/scripts/work_board.py"
P="$scratch/wb-project"
mkdir -p "$P"
URL="https://claude.ai/artifact/FixtureBoard123"
run 0 "first render from flags, before a URL exists" -- \
  python3 "$WB" render --name wb-project --lane now:"This week" --out "$P/.claude/work-board.html"
because "rendered"
run 0 "init writes board.json and the starter authorization.json" -- \
  python3 "$WB" init --project-dir "$P" --url "$URL" --name wb-project --lane now:"This week"
because "wrote $P/.claude/board.json"
run 0 "generated authorization.json validates" -- python3 "$AUTHZ" validate "$P/authorization.json"
because "0 errors, 0 warning(s)"
run 1 "asking to push is already granted" -- python3 "$AUTHZ" check "$P/authorization.json" --ask "should i push"
because "ALREADY-GRANTED"
because "pushes_per_session = 5"
run 0 "asking to deploy to prod is stop-listed" -- python3 "$AUTHZ" check "$P/authorization.json" --ask "deploy to prod"
because "STOP-LISTED"
run 0 "republishing the board page is not stop-listed" -- \
  python3 "$AUTHZ" check "$P/authorization.json" --ask "should I republish the board page to the same url"
because "NOT-COVERED"
run 0 "making the repo public is still stop-listed" -- \
  python3 "$AUTHZ" check "$P/authorization.json" --ask "Should I make it public?"
because "STOP-LISTED"
run 1 "init refuses to overwrite an existing board" -- \
  python3 "$WB" init --project-dir "$P" --url "$URL"
because "refusing to overwrite"
run 0 "validate passes a fresh board and page" -- python3 "$WB" validate "$P/.claude/board.json"
because "VALID: 0 errors"
printf '<!-- hand edit -->\n' >> "$P/.claude/work-board.html"
run 1 "validate catches a hand-edited page" -- python3 "$WB" validate "$P/.claude/board.json"
because "does not match a fresh render"
run 0 "render --board regenerates the page" -- python3 "$WB" render --board "$P/.claude/board.json"
run 0 "and validate passes again" -- python3 "$WB" validate "$P/.claude/board.json"
run 1 "validate rejects a bad url, lane and trigger" -- \
  python3 "$WB" validate "$FIXTURES/work-board/red-board.json"
because "'url' must be the board artifact's claude.ai URL"
because "lanes[1].id 'now' is used twice"
because "triggers[0] does not compile"
A="$scratch/wb-adopt"
mkdir -p "$A"
printf '{"project": "kept"}\n' > "$A/authorization.json"
run 0 "adopt keeps an existing authorization.json and records project triggers" -- \
  python3 "$WB" adopt --project-dir "$A" --url "$URL" --trigger 'seed write=\bseed\.py\b.*--apply\b'
because "kept the existing"
run 0 "adopted board carries its trigger" -- python3 "$WB" validate "$A/.claude/board.json"
because "1 project trigger(s)"
N="$scratch/wb-has-authz"
mkdir -p "$N"
printf '{"project": "kept"}\n' > "$N/authorization.json"
run 1 "init refuses a project that already has authorization.json" -- \
  python3 "$WB" init --project-dir "$N" --url "$URL"
because "use adopt"

echo
echo "board-gate hook"
run 0 "every fixture case gets its expected verdict" -- bash "$PLUGIN_ROOT/tests/prove-board-gate.sh"
because "BOARD-GATE PROOF: PASS"
run 1 "the prover fails a hook that never blocks" -- \
  bash "$PLUGIN_ROOT/tests/prove-board-gate.sh" "$FIXTURES/board-gate/stub-never-blocks.py"
because "BOARD-GATE PROOF: FAIL"
# Replay mode on a synthetic projects dir made read-only: a write would fail the run.
RP="$scratch/replay-projects"
mkdir -p "$RP/-fixture-project" "$scratch/replay-empty"
{
  printf '%s\n' '{"type":"user","message":{"role":"user","content":"ship it"}}'
  printf '%s\n' '{"type":"assistant","message":{"role":"assistant","content":[{"type":"tool_use","name":"Bash","input":{"command":"git -C /repo push origin main"}}]}}'
  printf '%s\n' '{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"Pushed."}]}}'
  printf '%s\n' '{"type":"user","message":{"role":"user","content":"next"}}'
  printf '%s\n' '{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"The branch is green.\n\nShould I merge it to main?"}]}}'
  printf '%s\n' '{"type":"user","message":{"role":"user","content":"find it"}}'
  printf '%s\n' '{"type":"assistant","message":{"role":"assistant","content":[{"type":"tool_use","name":"Bash","input":{"command":"grep -n \"git push\" notes.md"}}]}}'
  printf '%s\n' '{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"Found it."}]}}'
  printf '%s\n' '{"type":"user","message":{"role":"user","content":"status"}}'
  printf '%s\n' '{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"c1 is done.\n\nNext in Ready is c2, and I will start it when you say go.\n\nBoard: https://claude.ai/artifact/TestBoard123"}]}}'
} > "$RP/-fixture-project/fixture-session.jsonl"
chmod -R a-w "$RP"
run 0 "replay mode reports each hit from local transcripts and writes nothing" -- \
  python3 "$PLUGIN_ROOT/tests/replay-board-gate.py" --n 5 --projects-dir "$RP"
because "(a) git push"
because "(b) should-I ask"
because "Should I merge it to main?"
because "(b) offer"
because "I will start it when you say go."
because "REPLAY: 1 transcripts, 2 shell commands, 4 final messages"
because "REPLAY: (a) 1 hits (git push 1); (b) 2 hits"
chmod -R u+w "$RP"
run 2 "replay mode with no transcripts says so" -- \
  python3 "$PLUGIN_ROOT/tests/replay-board-gate.py" --projects-dir "$scratch/replay-empty"
because "REPLAY: no transcripts"

echo
echo "push check"
run 0 "push_check.sh stops on every planted fault in throwaway clones" -- bash "$PLUGIN_ROOT/tests/prove-push-check.sh"
because "PUSH-CHECK PROOF: PASS"

echo
echo "------------------------------------------------------------------------------"
echo "SCOPE: $((PASS + FAIL)) assertions over the components in this plugin, run against"
echo "the fixtures in tests/fixtures and throwaway projects and clones under a temp"
echo "directory only. It says nothing about any other plugin, and nothing about inputs"
echo "these fixtures do not represent."
printf 'RESULT: %d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
