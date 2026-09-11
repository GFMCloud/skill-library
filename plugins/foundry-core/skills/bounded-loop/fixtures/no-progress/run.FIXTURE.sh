#!/usr/bin/env bash
# FIXTURE: no-progress. Proves that stop-hook-verify.sh escalates with
# cause_class no_progress on the second of two consecutive attempts whose
# workspace snapshot (diff hash) is identical, without waiting for budget
# exhaustion: a failing check, workspace unchanged between two consecutive
# invocations.
#
# Usage: bash run.FIXTURE.sh [workdir]
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$HERE/../../scripts/stop-hook-verify.sh"
WORK="${1:-$(mktemp -d)}"
CHECK='echo "FAIL: FIXTURE assertion" >&2; exit 1'

mkdir -p "$WORK/src"
echo "FIXTURE: no-progress workspace" > "$WORK/README.txt"
echo "print('unchanged')" > "$WORK/src/app.py"

run_once () {
  local label="$1"
  echo "=== $label: stop-hook-verify.sh --check '$CHECK' --budget 3 ==="
  echo '{"cwd": "'"$WORK"'"}' | bash "$HOOK" \
    --check "$CHECK" --budget 3 \
    --state "$WORK/.bounded-loop/state.json" \
    --escalation-out "$WORK/.bounded-loop/escalation.yaml"
  echo "exit code: $?"
}

echo "=== attempt 1: check fails, establishes the first diff hash ==="
run_once "attempt 1"
echo

echo "=== attempt 2: same workspace, same failing check, nothing changed, must escalate no_progress ==="
run_once "attempt 2 (identical hash)"
echo

echo "=== escalation.yaml ==="
cat "$WORK/.bounded-loop/escalation.yaml"
echo "=== workdir: $WORK ==="
