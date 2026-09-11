#!/usr/bin/env bash
# FIXTURE: test-file-guard. Proves that stop-hook-verify.sh treats a change to
# a guarded path (tests/) as an automatic fail, cause_class test_file_modified,
# even when the check exits 0 on the attempt that changed it.
#
# Usage: bash run.FIXTURE.sh [workdir]
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$HERE/../../scripts/stop-hook-verify.sh"
WORK="${1:-$(mktemp -d)}"

mkdir -p "$WORK/src" "$WORK/tests"
echo "FIXTURE: test-file-guard workspace" > "$WORK/README.txt"
echo "def add(a, b): return a + b" > "$WORK/src/app.py"
echo "assert True  # placeholder test" > "$WORK/tests/test_app.py"

echo "=== attempt 1: check exits 1 (fails, budget remains), tests/ untouched (establishes baseline guard hash) ==="
echo '{"cwd": "'"$WORK"'"}' | bash "$HOOK" \
  --check "exit 1" --budget 3 \
  --state "$WORK/.bounded-loop/state.json" \
  --escalation-out "$WORK/.bounded-loop/escalation.yaml" \
  --guard tests
code1=$?
echo "exit code: $code1"
echo

echo "=== attempt 2: check now exits 0, but tests/test_app.py was edited in between, must still fail ==="
echo "assert True  # weakened to always pass" > "$WORK/tests/test_app.py"
echo '{"cwd": "'"$WORK"'"}' | bash "$HOOK" \
  --check "exit 0" --budget 3 \
  --state "$WORK/.bounded-loop/state.json" \
  --escalation-out "$WORK/.bounded-loop/escalation.yaml" \
  --guard tests
code2=$?
echo "exit code: $code2"
echo

echo "=== escalation.yaml ==="
cat "$WORK/.bounded-loop/escalation.yaml"
echo "=== workdir: $WORK ==="
