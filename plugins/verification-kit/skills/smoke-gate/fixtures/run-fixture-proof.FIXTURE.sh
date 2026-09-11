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
#      passed.
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
if [ "$COVERAGE_FULL_EXIT" -ne 0 ] || [ "$COVERAGE_MISSING_EXIT" -ne 3 ]; then
  echo "FIXTURE PROOF FAIL: poison-coverage check did not behave as expected"
  FAIL=1
fi

if [ "$FAIL" -ne 0 ]; then
  echo "FIXTURE PROOF: FAIL"
  exit 1
fi
echo "FIXTURE PROOF: PASS (five poisoned categories exit 1, live pass exits 0, unproven category correctly reported)"
