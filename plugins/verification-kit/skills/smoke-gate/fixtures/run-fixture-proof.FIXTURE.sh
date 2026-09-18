#!/usr/bin/env bash
# FIXTURE. smoke-gate's own deliberate-failure proof, run entirely offline against
# fixture_server.py in this directory. Runnable from any directory:
#   bash /Users/gfm/skill-library/plugins/verification-kit/skills/smoke-gate/fixtures/run-fixture-proof.FIXTURE.sh
#
# Sequence:
#   1. Start the fixture server on a free localhost port.
#   2. Generate a smoke script from manifest.FIXTURE.yaml.
#   3. Run the poison-coverage check against manifest.FIXTURE.yaml (expect PROVEN x5,
#      exit 0) and against manifest-missing-poison.FIXTURE.yaml (expect one UNPROVEN
#      line, exit 3) - proving an unproven category is reported as unproven, never as
#      passed. Also run the generator itself against manifest-missing-poison.FIXTURE.yaml
#      (expect it to refuse with "UNPROVEN console: no poison entry", exit 1, and write
#      no script) - proving the generated script itself can never default to PASS for a
#      category that was never proven.
#   4. Run the generated script once per assertion category with that category's
#      poison override active and the rest at their passing defaults: expect exit 1
#      each time, five times (identity, freshness, connections, routes, console).
#   5. Run the generated script with no overrides: expect exit 0 (the live pass).
#   6. Stop the fixture server.
#
# Screenshot: not available in fixture mode. A real live pass captures one via the
# Browser tool or Playwright (see references/webapp-testing-intake.md); this fixture
# server has no browser in front of it to screenshot.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$HERE/.." && pwd)"
WORKDIR="$(mktemp -d)"
trap 'kill "${SERVER_PID:-0}" 2>/dev/null; rm -rf "$WORKDIR"' EXIT

echo "== 1. start fixture server =="
python3 "$HERE/fixture_server.py" --port 0 > "$WORKDIR/server.log" 2>&1 &
SERVER_PID=$!
for _ in $(seq 1 50); do
  if grep -q '^LISTENING ' "$WORKDIR/server.log" 2>/dev/null; then break; fi
  sleep 0.1
done
PORT="$(grep '^LISTENING ' "$WORKDIR/server.log" | awk '{print $2}')"
if [ -z "$PORT" ]; then
  echo "FIXTURE PROOF FAIL: fixture server never printed LISTENING"; cat "$WORKDIR/server.log"; exit 1
fi
echo "fixture server pid=$SERVER_PID port=$PORT"
export SMOKE_TARGET="http://127.0.0.1:$PORT/"

echo
echo "== 2. generate smoke script from manifest.FIXTURE.yaml =="
python3 "$SKILL_DIR/scripts/generate-smoke-script.py" "$HERE/manifest.FIXTURE.yaml" "$WORKDIR/smoke.FIXTURE.sh"
cat "$WORKDIR/smoke.FIXTURE.sh" > "$WORKDIR/smoke.printed.sh"

echo
echo "== 3a. poison coverage: manifest.FIXTURE.yaml (expect exit 0, five PROVEN lines) =="
python3 "$SKILL_DIR/scripts/check-poison-coverage.py" "$HERE/manifest.FIXTURE.yaml"
COVERAGE_FULL_EXIT=$?
echo "exit: $COVERAGE_FULL_EXIT"

echo
echo "== 3b. poison coverage: manifest-missing-poison.FIXTURE.yaml (expect exit 3, one UNPROVEN line) =="
python3 "$SKILL_DIR/scripts/check-poison-coverage.py" "$HERE/manifest-missing-poison.FIXTURE.yaml"
COVERAGE_MISSING_EXIT=$?
echo "exit: $COVERAGE_MISSING_EXIT"

echo
echo "== 3c. generator refusal: manifest-missing-poison.FIXTURE.yaml (expect exit 1, UNPROVEN console, no script written) =="
rm -f "$WORKDIR/should-not-exist.sh"
python3 "$SKILL_DIR/scripts/generate-smoke-script.py" "$HERE/manifest-missing-poison.FIXTURE.yaml" "$WORKDIR/should-not-exist.sh"
GENERATOR_REFUSAL_EXIT=$?
echo "exit: $GENERATOR_REFUSAL_EXIT"
if [ "$GENERATOR_REFUSAL_EXIT" -eq 0 ] || [ -e "$WORKDIR/should-not-exist.sh" ]; then
  echo "FIXTURE PROOF FAIL: generator did not refuse the missing-poison manifest"; FAIL_GENERATOR_REFUSAL=1
else
  FAIL_GENERATOR_REFUSAL=0
fi

FAIL=0

check_exit_1() {
  local label="$1"; shift
  echo
  echo "== poison: $label (expect exit 1) =="
  "$@"
  local code=$?
  echo "exit: $code"
  if [ "$code" -ne 1 ]; then
    echo "FIXTURE PROOF FAIL: $label did not exit 1"; FAIL=1
  fi
}

check_exit_1 "identity" env SMOKE_IDENTITY_EXPECT="Guest" \
  SMOKE_CONN_HOST_FIXTURE_SERVER="127.0.0.1" SMOKE_CONN_PORT_FIXTURE_SERVER="$PORT" \
  bash "$WORKDIR/smoke.FIXTURE.sh"

check_exit_1 "freshness" env SMOKE_FRESHNESS_STALE="2099-01-01" \
  SMOKE_CONN_HOST_FIXTURE_SERVER="127.0.0.1" SMOKE_CONN_PORT_FIXTURE_SERVER="$PORT" \
  bash "$WORKDIR/smoke.FIXTURE.sh"

check_exit_1 "connections" env \
  SMOKE_CONN_HOST_FIXTURE_SERVER="127.0.0.1" SMOKE_CONN_PORT_FIXTURE_SERVER="1" \
  bash "$WORKDIR/smoke.FIXTURE.sh"

check_exit_1 "routes" env SMOKE_ROUTE_PATH_STATUS="/does-not-exist" \
  SMOKE_CONN_HOST_FIXTURE_SERVER="127.0.0.1" SMOKE_CONN_PORT_FIXTURE_SERVER="$PORT" \
  bash "$WORKDIR/smoke.FIXTURE.sh"

curl -sS "http://127.0.0.1:$PORT/console-error" > "$WORKDIR/console-error.FIXTURE.html"
check_exit_1 "console" env SMOKE_CONSOLE_SOURCE="$WORKDIR/console-error.FIXTURE.html" \
  SMOKE_CONN_HOST_FIXTURE_SERVER="127.0.0.1" SMOKE_CONN_PORT_FIXTURE_SERVER="$PORT" \
  bash "$WORKDIR/smoke.FIXTURE.sh"

echo
echo "== live pass: no overrides beyond the connection address (expect exit 0) =="
env SMOKE_CONN_HOST_FIXTURE_SERVER="127.0.0.1" SMOKE_CONN_PORT_FIXTURE_SERVER="$PORT" \
  bash "$WORKDIR/smoke.FIXTURE.sh"
LIVE_EXIT=$?
echo "exit: $LIVE_EXIT"
if [ "$LIVE_EXIT" -ne 0 ]; then
  echo "FIXTURE PROOF FAIL: live pass did not exit 0"; FAIL=1
fi
echo "screenshot: not available in fixture mode"

echo
echo "== 6. Stop hook, red: poisoned identity through scripts/smoke-stop-hook.sh (expect exit 2, SMOKE FAIL on stderr) =="
HOOK="$SKILL_DIR/scripts/smoke-stop-hook.sh"
printf '{"hook_event_name":"Stop","stop_hook_active":false}' | env SMOKE_IDENTITY_EXPECT="Guest" \
  SMOKE_CONN_HOST_FIXTURE_SERVER="127.0.0.1" SMOKE_CONN_PORT_FIXTURE_SERVER="$PORT" \
  bash "$HOOK" "$WORKDIR/smoke.FIXTURE.sh" > "$WORKDIR/hook-red.out" 2> "$WORKDIR/hook-red.err"
HOOK_RED_EXIT=$?
echo "exit: $HOOK_RED_EXIT"; sed 's/^/stderr: /' "$WORKDIR/hook-red.err"
if [ "$HOOK_RED_EXIT" -ne 2 ] || ! grep -q 'SMOKE FAIL' "$WORKDIR/hook-red.err"; then
  echo "FIXTURE PROOF FAIL: stop hook did not block a red smoke run with its own output"; FAIL=1
fi

echo
echo "== 7. Stop hook, red again with stop_hook_active true (expect exit 0, released, still reported) =="
printf '{"hook_event_name":"Stop","stop_hook_active":true}' | env SMOKE_IDENTITY_EXPECT="Guest" \
  SMOKE_CONN_HOST_FIXTURE_SERVER="127.0.0.1" SMOKE_CONN_PORT_FIXTURE_SERVER="$PORT" \
  bash "$HOOK" "$WORKDIR/smoke.FIXTURE.sh" > "$WORKDIR/hook-loop.out" 2> "$WORKDIR/hook-loop.err"
HOOK_LOOP_EXIT=$?
echo "exit: $HOOK_LOOP_EXIT"
if [ "$HOOK_LOOP_EXIT" -ne 0 ] || ! grep -q 'still red' "$WORKDIR/hook-loop.err"; then
  echo "FIXTURE PROOF FAIL: stop hook did not release a second stop while red"; FAIL=1
fi

echo
echo "== 8. Stop hook, green: no overrides (expect exit 0, empty stderr) =="
printf '{"hook_event_name":"Stop","stop_hook_active":false}' | env \
  SMOKE_CONN_HOST_FIXTURE_SERVER="127.0.0.1" SMOKE_CONN_PORT_FIXTURE_SERVER="$PORT" \
  bash "$HOOK" "$WORKDIR/smoke.FIXTURE.sh" > "$WORKDIR/hook-green.out" 2> "$WORKDIR/hook-green.err"
HOOK_GREEN_EXIT=$?
echo "exit: $HOOK_GREEN_EXIT"
if [ "$HOOK_GREEN_EXIT" -ne 0 ] || [ -s "$WORKDIR/hook-green.err" ]; then
  echo "FIXTURE PROOF FAIL: stop hook did not release a green smoke run silently"; FAIL=1
fi

echo
echo "== 9. Stop hook, missing script (expect exit 0 and a stderr line naming the path: fails open, never silent) =="
printf '{}' | bash "$HOOK" "$WORKDIR/no-such-smoke.sh" > /dev/null 2> "$WORKDIR/hook-missing.err"
HOOK_MISSING_EXIT=$?
echo "exit: $HOOK_MISSING_EXIT"; sed 's/^/stderr: /' "$WORKDIR/hook-missing.err"
if [ "$HOOK_MISSING_EXIT" -ne 0 ] || ! grep -q 'no-such-smoke.sh' "$WORKDIR/hook-missing.err"; then
  echo "FIXTURE PROOF FAIL: stop hook with a missing script did not name it on stderr"; FAIL=1
fi

echo
if [ "$COVERAGE_FULL_EXIT" -ne 0 ] || [ "$COVERAGE_MISSING_EXIT" -ne 3 ]; then
  echo "FIXTURE PROOF FAIL: poison-coverage check did not behave as expected"
  FAIL=1
fi

if [ "$FAIL_GENERATOR_REFUSAL" -ne 0 ]; then
  FAIL=1
fi

if [ "$FAIL" -ne 0 ]; then
  echo "FIXTURE PROOF: FAIL"
  exit 1
fi
echo "FIXTURE PROOF: PASS (five poisoned categories exit 1, live pass exits 0, unproven category correctly reported, stop hook blocks red once and releases green)"
