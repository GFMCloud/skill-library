#!/usr/bin/env bash
# FIXTURE runner: proves check-claims.py against the four FIXTURE handoff files.
# Usage: bash run-fixtures.sh [path/to/check-claims.py]   (default ../scripts/check-claims.py)
# Rebuilds the throwaway repo under /tmp (see setup-fixture-repo.sh), then asserts:
#   match     exit 0, and no STALE notice (the repo's files predate written_at)
#   mismatch  exit 1
#   stale     b.txt touched after written_at: exit 0, a STALE notice naming b.txt, and the
#             notice printed before the discrepancy table
#   refused   a write-shaped check (rm) is listed, marked refused, exit 1, and its target
#             file still exists afterwards (the command never ran)
# Exits 0 only when every assertion holds. Pass an older check-claims.py as the argument
# to see the stale case fail without the staleness check.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK="${1:-$HERE/../scripts/check-claims.py}"
REPO="/tmp/handoff-fixture-repo"
fails=0

assert() {  # assert <label> <condition-exit-code>
    if [ "$2" -eq 0 ]; then echo "PASS  $1"; else echo "FAIL  $1"; fails=$((fails + 1)); fi
}

bash "$HERE/setup-fixture-repo.sh" >/dev/null

out="$(python3 "$CHECK" "$HERE/FIXTURE-match-handoff.md" --project "$REPO" 2>&1)"; code=$?
[ "$code" -eq 0 ]; assert "match: exit 0 (got $code)" $?
! grep -q "^STALE" <<<"$out"; assert "match: no STALE notice when no file is newer than written_at" $?

out="$(python3 "$CHECK" "$HERE/FIXTURE-mismatch-handoff.md" --project "$REPO" 2>&1)"; code=$?
[ "$code" -eq 1 ]; assert "mismatch: exit 1 (got $code)" $?

touch "$REPO/b.txt"
out="$(python3 "$CHECK" "$HERE/FIXTURE-stale-handoff.md" --project "$REPO" 2>&1)"; code=$?
[ "$code" -eq 0 ]; assert "stale: exit 0, staleness warns and never fails the check (got $code)" $?
grep -q "^STALE.*1 file" <<<"$out"; assert "stale: STALE notice counts 1 changed file" $?
grep -q "b\.txt" <<<"$out"; assert "stale: notice names b.txt" $?
stale_line="$(grep -n "^STALE" <<<"$out" | head -1 | cut -d: -f1)"
table_line="$(grep -n "^Discrepancy table" <<<"$out" | head -1 | cut -d: -f1)"
[ -n "$stale_line" ] && [ -n "$table_line" ] && [ "$stale_line" -lt "$table_line" ]
assert "stale: notice comes before the discrepancy table" $?

# refused: a write-shaped check (rm of b.txt) is printed, marked refused, never run.
bash "$HERE/setup-fixture-repo.sh" >/dev/null
out="$(python3 "$CHECK" "$HERE/FIXTURE-refused-handoff.md" --project "$REPO" 2>&1)"; code=$?
[ "$code" -eq 1 ]; assert "refused: exit 1 (got $code)" $?
grep -q "^status:  refused" <<<"$out"; assert "refused: the rm row is marked refused" $?
grep -q "^Checks to run" <<<"$out"; assert "refused: the check list is printed before running" $?
[ -f "$REPO/b.txt" ]; assert "refused: b.txt still exists, so the rm never ran" $?
grep -q "^status:  match" <<<"$out"; assert "refused: the read-only row in the same file still ran and matched" $?

echo
if [ "$fails" -eq 0 ]; then echo "RESULT: all fixture assertions pass."; else echo "RESULT: $fails assertion(s) failed."; fi
[ "$fails" -eq 0 ]
