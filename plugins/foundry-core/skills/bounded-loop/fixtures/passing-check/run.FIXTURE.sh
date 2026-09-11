#!/usr/bin/env bash
# FIXTURE: passing-check. Proves two things:
#   1. A check that exits 0 releases the hook (exit 0, no block).
#   2. Repeating the exact same workspace state (same diff hash) does not
#      consume a new attempt, the hook is idempotent on a repeated hash.
# Note: attempt 2 below repeats the workspace with a now-passing check
# rather than a repeated failing check. Two consecutive identical hashes on
# a still-failing check escalate as no_progress (see fixtures/no-progress),
# so repeating a failing check here would escalate instead of demonstrating
# idempotency on the passing path.
#
# Usage: bash run.FIXTURE.sh [workdir]
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$HERE/../../scripts/stop-hook-verify.sh"
WORK="${1:-$(mktemp -d)}"

mkdir -p "$WORK/src"
echo "FIXTURE: passing-check workspace" > "$WORK/README.txt"
echo "def add(a, b): return a + b" > "$WORK/src/app.py"

run_once () {
  local label="$1" check="$2"
  echo "=== $label: stop-hook-verify.sh --check '$check' --budget 3 ==="
  echo '{"cwd": "'"$WORK"'"}' | bash "$HOOK" \
    --check "$check" --budget 3 \
    --state "$WORK/.bounded-loop/state.json" \
    --escalation-out "$WORK/.bounded-loop/escalation.yaml"
  echo "exit code: $?"
}

# First attempt: fails, so an "attempt" exists to prove idempotency against.
echo "=== attempt 1 (setup): check exits 1 so there is a recorded attempt ==="
echo '{"cwd": "'"$WORK"'"}' | bash "$HOOK" \
  --check "exit 1" --budget 3 \
  --state "$WORK/.bounded-loop/state.json" \
  --escalation-out "$WORK/.bounded-loop/escalation.yaml"
echo "exit code: $?"
echo "attempts recorded after attempt 1:"
python3 -c "import json; print(len(json.load(open('$WORK/.bounded-loop/state.json'))['attempts']))"
echo

echo "=== attempt 2 (repeat): same workspace, no file changed, check now passes ==="
run_once "attempt 2 (repeat, no file change, now passes)" "exit 0"
echo "attempts recorded after repeated hash (must be unchanged: still 1):"
python3 -c "import json; print(len(json.load(open('$WORK/.bounded-loop/state.json'))['attempts']))"
echo

echo "=== attempt 3: already passed, further Stop events find nothing to gate ==="
run_once "attempt 3 (already passed)" "exit 0"
echo

echo "=== final state.json ==="
cat "$WORK/.bounded-loop/state.json"
echo
echo "=== workdir: $WORK ==="
