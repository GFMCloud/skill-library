#!/bin/bash
# toolkit-review: create a run directory.
# Usage: init-run.sh <run-dir> <size> <mode> [name]
#   size: spot | set | full      mode: self | one-repo | many-repos | subset
# Writes run.json from templates/run.json, the marker, the two name lists, empty
# slot-map.tsv and items.tsv, and the budget file. The run directory must not be a git
# repository (a judge's context can carry branch and commit subjects) and its path must
# not contain the owner's name or the project's name (a judge sees its cwd).
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T="$(dirname "$S")/templates"
run="$1"; size="$2"; mode="$3"; name="${4:-$(basename "$1")}"
case "$size" in spot|set|full) ;; *) echo "usage: init-run.sh <run-dir> spot|set|full self|one-repo|many-repos|subset [name]" >&2; exit 2 ;; esac
case "$mode" in self|one-repo|many-repos|subset) ;; *) echo "usage: init-run.sh <run-dir> spot|set|full self|one-repo|many-repos|subset [name]" >&2; exit 2 ;; esac
if [ -e "$run/run.json" ]; then echo "init-run.sh: $run already holds a run.json" >&2; exit 2; fi
if git -C "$run" rev-parse 2>/dev/null; then echo "init-run.sh: $run is inside a git repository; pick a path that is not" >&2; exit 2; fi
mkdir -p "$run/budget" "$run/slots" "$run/private" "$run/prompts-built" "$run/extracts" "$run/extracts-raw" "$run/judgments" "$run/waves" "$run/candidates"
jq --arg n "$name" --arg s "$size" --arg m "$mode" --arg d "$(date -u +%Y-%m-%d)" \
  '.name = $n | .size = $s | .mode = $m | .created = $d' "$T/run.json" > "$run/run.json"
touch "$run/.marker"
: > "$run/budget/usage.tsv"
printf 'slot\tpurpose\tevidence\n' > "$run/slot-map.tsv"
printf 'id\tside\tsource\tslot\ttype\tpath\n' > "$run/items.tsv"
# Always-forbidden names: the owner (git identity), the library's org and repo, the words
# installed and incumbent. Edit before the first extraction; add account names by hand.
{
  git config user.name 2>/dev/null | tr ' ' '\n'
  git config user.email 2>/dev/null | sed -E 's/@.*//'
  lib="${TOOLKIT_LIBRARY:-$HOME/skill-library}"
  url="$(git -C "$lib" remote get-url origin 2>/dev/null)"
  if [ -n "$url" ]; then
    basename "$url" .git
    basename "$(dirname "$url")" | sed 's/.*://'
  fi
  printf 'installed\nincumbent\n'
} | /usr/bin/grep -v '^$' | sort -u > "$run/name-list.txt"
# Context names: plugin names, forbidden unless the source itself cites them.
lib="${TOOLKIT_LIBRARY:-$HOME/skill-library}"
if [ -d "$lib/plugins" ]; then ls "$lib/plugins" | sort -u > "$run/context-names.txt"; else : > "$run/context-names.txt"; fi
echo "run created: $run ($size, $mode)"
echo "next: fill slot-map.tsv and items.tsv, review name-list.txt and context-names.txt, then bin-slots.py and make-facts.py"
