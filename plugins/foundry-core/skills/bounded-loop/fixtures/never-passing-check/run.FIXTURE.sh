#!/usr/bin/env bash
# FIXTURE: never-passing-check. Proves that stop-hook-verify.sh escalates on
# budget exhaustion with cause_class unreachable_condition, because the
# check's failing output never changes across three genuinely distinct
# attempts (each attempt edits src/app.py so the diff hash differs).
#
# Usage: bash run.sh [workdir]   (workdir defaults to a fresh mktemp -d)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$HERE/../../scripts/stop-hook-verify.sh"
WORK="${1:-$(mktemp -d)}"

mkdir -p "$WORK/src"
echo "FIXTURE: never-passing-check workspace" > "$WORK/README.txt"

run_attempt () {
  local n="$1"
  echo "print('attempt $n')" > "$WORK/src/app.py"
  echo "=== attempt $n: stop-hook-verify.sh --check 'exit 1' --budget 3 ==="
  echo '{"cwd": "'"$WORK"'"}' | bash "$HOOK" \
    --check "exit 1" --budget 3 \
    --state "$WORK/.bounded-loop/state.json" \
    --escalation-out "$WORK/.bounded-loop/escalation.yaml"
  echo "exit code: $?"
  echo
}

for n in 1 2 3; do
  run_attempt "$n"
done

echo "=== escalation.yaml ==="
cat "$WORK/.bounded-loop/escalation.yaml"
echo "=== workdir: $WORK ==="
