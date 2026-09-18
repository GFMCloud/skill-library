#!/bin/bash
# toolkit-review: structure and name-leak check for one extraction report.
# Usage: check-extract.sh <extract.md> [source-dir]
# Exit 0 only if the four sections and the seven per-item fields are present and no
# forbidden name appears. Two name lists in the run directory:
#   name-list.txt      always forbidden: the owner, account, organization and repository
#                      names and the words installed and incumbent
#   context-names.txt  plugin and tool names, forbidden unless <source-dir> is given and
#                      the source files themselves contain the name (a report may quote a
#                      name its source cites; the ECC run lost a slot to this, 2026-09-17)
# Known weakness: it checks that sections exist, not that they are any good, and a name
# list only catches names someone thought to put on it.
RUN="${TR_RUN:?check-extract.sh: set TR_RUN to the run directory}"
f="$1"; src="$2"
if [ ! -s "$f" ]; then echo "check-extract: missing or empty: $f"; exit 1; fi
# When the report sits at extracts/<slot>/<letter>.md and no source dir was given, find
# the side through private/map.json here, so the orchestrator never reads the map.
letter="$(basename "$f" .md)"; slot="$(basename "$(dirname "$f")")"
if [ -z "$src" ] && [ "$(dirname "$(dirname "$f")")" = "$RUN/extracts" ]; then
  side=""
  if [ -s "$RUN/private/map.json" ]; then side=$(jq -r --arg s "$slot" --arg l "$letter" '.[$s][$l] // empty' "$RUN/private/map.json"); fi
  if [ -z "$side" ] && [ "$letter" = R ]; then side=$(find "$RUN/slots/$slot" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | head -1); fi
  [ -n "$side" ] && src="$RUN/slots/$slot/$side"
fi
fail=0
for h in '### Items' '### For each item' '### Agent-directed text' '### Could not determine'; do
  if ! /usr/bin/grep -q -F "$h" "$f"; then echo "check-extract: missing section: $h"; fail=1; fi
done
other=$(/usr/bin/grep -E '^### ' "$f" | /usr/bin/grep -v -E '^### (Items|For each item|Agent-directed text|Could not determine)\s*$' | head -3)
if [ -n "$other" ]; then echo "check-extract: unexpected level-3 heading(s):"; echo "$other"; fail=1; fi
for k in 'Trigger' 'What it makes the agent do' 'Enforcement' 'Dependencies' 'State it writes' 'Fit with the bar' 'What it does not cover'; do
  if ! /usr/bin/grep -q -F "**$k" "$f"; then echo "check-extract: no per-item field: $k"; fail=1; fi
done
if [ -s "$RUN/name-list.txt" ]; then
  hits=$(/usr/bin/grep -n -i -w -F -f "$RUN/name-list.txt" "$f")
  if [ -n "$hits" ]; then echo "check-extract: name-list hits:"; echo "$hits"; fail=1; fi
fi
if [ -s "$RUN/context-names.txt" ]; then
  while read -r name; do
    [ -z "$name" ] && continue
    if /usr/bin/grep -q -i -w -F "$name" "$f"; then
      if [ -n "$src" ] && [ -d "$src" ] && /usr/bin/grep -r -q -i -w -F "$name" "$src"; then
        echo "check-extract: context name '$name' allowed, the source cites it"
      else
        echo "check-extract: context-name hit (source does not cite it): $name"; fail=1
      fi
    fi
  done < "$RUN/context-names.txt"
fi
if [ "$fail" -eq 0 ]; then echo "check-extract: ok: $f"; exit 0; fi
# A rejected report under extracts/ is archived as extracts-raw/<slot>/<letter>.attempt-<n>.md
# and a rejection note is written for the re-dispatch. The report is never repaired here.
if [ "$(dirname "$(dirname "$f")")" = "$RUN/extracts" ]; then
  raw="$RUN/extracts-raw/$slot"; mkdir -p "$raw"
  n=$(( $(find "$raw" -name "$letter.attempt-*.md" | wc -l | tr -d ' ') + 1 ))
  mv "$f" "$raw/$letter.attempt-$n.md"
  {
    echo "Attempt $n was rejected. The exact failures, from the mechanical check:"
    echo
    bash "$0" "$raw/$letter.attempt-$n.md" "$src" 2>&1 | /usr/bin/grep -v -E '^check-extract: (ok|context name .* allowed)' | sed 's/^/    /'
    echo
    echo "Write the whole report again. Use exactly the four level-three headings and the seven bold fields in the order given. Do not write any of the forbidden words or names, even inside a quotation: paraphrase the quoted line and replace the name with 'the repository' or 'the owner'. Before replying, search your draft for every forbidden word."
  } > "$raw/$letter.rejection.txt"
  echo "check-extract: archived as $raw/$letter.attempt-$n.md; rejection note written; re-dispatch with: run-extractor.sh $slot $letter"
fi
exit 1
