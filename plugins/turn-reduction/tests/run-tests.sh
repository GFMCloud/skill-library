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
echo "------------------------------------------------------------------------------"
echo "SCOPE: $((PASS + FAIL)) assertions over the three components in this plugin, run"
echo "against the fixtures in tests/fixtures only. It says nothing about any other"
echo "plugin, and nothing about inputs these fixtures do not represent."
printf 'RESULT: %d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
