#!/usr/bin/env bash
# FIXTURE runner: proves check-claims.py against the five FIXTURE handoff files.
# Usage: bash run-fixtures.sh [path/to/check-claims.py]   (default ../scripts/check-claims.py)
# Rebuilds the throwaway repo under /tmp (see setup-fixture-repo.sh), then asserts:
#   match     exit 0, and no STALE notice (the repo's files predate written_at)
#   mismatch  exit 1
#   stale     b.txt touched after written_at: exit 0, a STALE notice naming b.txt, and the
#             notice printed before the discrepancy table
#   refused   a write-shaped check (rm) is listed, marked refused, exit 1, and its target
#             file still exists afterwards (the command never ran)
#   nongit    --project is a folder with no .git: staleness comes from an mtime walk and
#             names the touched file; a read-only `git merge-base` check runs, not refused
#   offset    written_at's UTC offset has no colon (-0500): staleness is still judged from
#             written_at, never from the handoff file's mtime
# Exits 0 only when every assertion holds. Pass an older check-claims.py as the argument
# to see the stale case fail without the staleness check, or the offset case fail before
# 0.6.5.
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

# nongit: --project is a plain folder (no .git). Staleness must still be checked by an
# mtime walk, naming the file touched after written_at and not the older one, exit 0;
# and the read-only `git merge-base --is-ancestor` row must run and match, not be refused.
NONGIT="/tmp/handoff-fixture-nongit"
rm -rf "$NONGIT"; mkdir -p "$NONGIT/sub" "$NONGIT/.git-not-a-repo"
echo "old" > "$NONGIT/before.txt"; echo "new" > "$NONGIT/sub/after.txt"
touch -t 202609010000 "$NONGIT/before.txt"
out="$(python3 "$CHECK" "$HERE/FIXTURE-nongit-handoff.md" --project "$NONGIT" 2>&1)"; code=$?
[ "$code" -eq 0 ]; assert "nongit: exit 0 (got $code)" $?
grep -q "^STALE.*1 file.*not a git repo, mtime walk" <<<"$out"; assert "nongit: STALE notice counts 1 file and says mtime walk" $?
grep -q "sub/after\.txt" <<<"$out"; assert "nongit: notice names sub/after.txt" $?
! grep -q "before\.txt" <<<"$out"; assert "nongit: the older before.txt is not listed" $?
! grep -q "^not checked" <<<"$out"; assert "nongit: no 'not checked' line (the 0.6.2 behavior)" $?
! grep -q "^status:  refused" <<<"$out"; assert "nongit: the merge-base row was not refused" $?
[ "$(grep -c "^status:  match" <<<"$out")" -eq 2 ]; assert "nongit: both rows ran and matched" $?

# offset: written_at carries its UTC offset without a colon (-0500, what `date +%z`
# prints). YAML leaves that a string and Python 3.9's fromisoformat rejects it, so until
# 0.6.5 the checker silently fell back to the handoff file's mtime. The staleness label
# must name the parsed written_at; the repo's files are backdated by the setup script, so
# the verdict is "fresh", as in the match case.
bash "$HERE/setup-fixture-repo.sh" >/dev/null
out="$(python3 "$CHECK" "$HERE/FIXTURE-offset-handoff.md" --project "$REPO" 2>&1)"; code=$?
[ "$code" -eq 0 ]; assert "offset: exit 0 (got $code)" $?
grep -q "after written_at 2026-09-11T00:00:00-05:00" <<<"$out"; assert "offset: staleness is judged from the parsed written_at" $?
! grep -q "no usable written_at" <<<"$out"; assert "offset: no fallback to the handoff file's mtime" $?
grep -q "^fresh: no file" <<<"$out"; assert "offset: verdict is fresh, as in the match case" $?

echo
if [ "$fails" -eq 0 ]; then echo "RESULT: all fixture assertions pass."; else echo "RESULT: $fails assertion(s) failed."; fi
[ "$fails" -eq 0 ]
