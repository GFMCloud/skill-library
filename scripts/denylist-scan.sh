#!/bin/bash
# denylist-scan.sh: fail when any tracked file matches a denylisted pattern.
#
# The denylist holds company, customer, people, account-ID and hostname patterns that a
# secret scanner cannot know about. It lives OUTSIDE this public repository, never in it:
#   DENYLIST_FILE   path to the pattern file; default ~/.claude/denylist.txt
# One POSIX extended regex per line, matched case-insensitively against every tracked file
# (binary files skipped). Blank lines and lines starting with # are ignored.
#
#   bash scripts/denylist-scan.sh            scan the tracked files in the working tree
#   bash scripts/denylist-scan.sh --staged   scan the index (for a pre-commit hook)
#
# CI (.github/workflows/validate.yml, job "denylist") writes the DENYLIST_PATTERNS secret
# to a temp file and points DENYLIST_FILE at it. The work laptop's pre-commit hook runs
# the --staged form (maintainers/migration-2026-10/prompts/phase-0-work.md).
#
# Exit 0: clean. Exit 1: at least one match (printed as file:line:text). Exit 2:
# misconfigured, which also fails: no pattern file, a pattern file with no patterns, or a
# pattern file inside the repository.
set -uo pipefail

mode=tree
case "${1:-}" in
  --staged) mode=index ;;
  "") ;;
  *) echo "usage: denylist-scan.sh [--staged]" >&2; exit 2 ;;
esac

file="${DENYLIST_FILE:-$HOME/.claude/denylist.txt}"
top=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "denylist: not inside a git repository" >&2; exit 2; }
[[ -f "$file" ]] || { echo "denylist: no pattern file at $file (set DENYLIST_FILE)" >&2; exit 2; }

abs="$(cd "$(dirname "$file")" && pwd -P)/$(basename "$file")"
case "$abs" in
  "$top"/*) echo "denylist: pattern file $abs is inside the repository; the denylist never lives in this public repo" >&2; exit 2 ;;
esac

patterns=$(mktemp) || exit 2
trap 'rm -f "$patterns"' EXIT
grep -v -E '^[[:space:]]*(#|$)' "$file" > "$patterns"
count=$(grep -c . "$patterns")
[[ "$count" -gt 0 ]] || { echo "denylist: $file has no patterns" >&2; exit 2; }

if [[ $mode == index ]]; then
  hits=$(git -C "$top" grep -I -i -n -E --cached -f "$patterns" -- .)
else
  hits=$(git -C "$top" grep -I -i -n -E -f "$patterns" -- .)
fi
status=$?
files=$(git -C "$top" ls-files | wc -l | tr -d ' ')

case $status in
  0)
    printf '%s\n' "$hits"
    echo "denylist: $(printf '%s\n' "$hits" | wc -l | tr -d ' ') match(es) in tracked files ($mode; $count patterns from $file)" >&2
    exit 1 ;;
  1)
    echo "denylist: clean ($files tracked files, $count patterns, $mode)"
    exit 0 ;;
  *)
    echo "denylist: git grep failed with status $status" >&2
    exit 2 ;;
esac
