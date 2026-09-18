#!/bin/bash
# toolkit-review: run one neutral extraction for one side of one slot.
# Usage: run-extractor.sh <slot> <side>
# cwd for the run is $TR_RUN/slots/<slot>/<side>/, under the clean profile. The report
# lands at extracts/<slot>/<letter>.md, the letter read from private/map.json (X or Y);
# a slot with exactly one side (self-review) gets the letter R and needs no map entry.
# Raw JSON and stderr stay in extracts-raw/, because the judge's cwd may hold only the
# reports. A rejection note left by the checker for this letter is appended to the prompt.
# Model: models.extractor in run.json.
RUN="${TR_RUN:?run-extractor.sh: set TR_RUN to the run directory}"
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REF="${TR_SKILL_DIR:-$(dirname "$S")}/references"
slot="$1"; side="$2"
if [ -z "$slot" ] || [ -z "$side" ]; then echo "usage: run-extractor.sh <slot> <side|X|Y|R>" >&2; exit 2; fi
# A letter instead of a side name (re-dispatch after a rejection) is resolved through the
# map here, so the orchestrator never has to read private/map.json.
case "$side" in
  X|Y) side=$(jq -r --arg s "$slot" --arg l "$side" '.[$s][$l] // empty' "$RUN/private/map.json" 2>/dev/null)
       if [ -z "$side" ]; then echo "run-extractor.sh: no side for letter $2 in slot $slot" >&2; exit 2; fi ;;
  R)   side=$(find "$RUN/slots/$slot" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | head -1) ;;
esac
dir="$RUN/slots/$slot/$side"
if [ ! -d "$dir" ]; then echo "run-extractor.sh: no such slot side: $dir" >&2; exit 2; fi
MODEL=$(jq -r '.models.extractor // "sonnet"' "$RUN/run.json" 2>/dev/null); MODEL="${MODEL:-sonnet}"
letter=""
if [ -s "$RUN/private/map.json" ]; then
  letter=$(jq -r --arg s "$slot" --arg side "$side" '.[$s] // {} | to_entries[] | select(.value == $side) | .key' "$RUN/private/map.json")
fi
if [ -z "$letter" ]; then
  nsides=$(find "$RUN/slots/$slot" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
  if [ "$nsides" = "1" ]; then letter=R; else echo "run-extractor.sh: no X/Y assignment for $slot $side in private/map.json" >&2; exit 2; fi
fi
purpose="$(cat "$RUN/slots/$slot/purpose.txt" 2>/dev/null)"
if [ -z "$purpose" ]; then echo "run-extractor.sh: missing $RUN/slots/$slot/purpose.txt" >&2; exit 2; fi
facts="$(jq -r --arg side "$side" '.items[] | select(.side == $side) | "- \(.id): type \(.type); \(.body_lines) lines; description \(.description_words) words; loads \(.load); runtime deps: \(.runtime_deps | join(", ") | if . == "" then "none named" else . end); enforcement files: \(.enforcement_files | join(", ") | if . == "" then "none" else . end); path: \(.file)"' "$RUN/facts/$slot.json" 2>/dev/null)"
if [ -z "$facts" ]; then echo "run-extractor.sh: no facts rows for $slot $side in $RUN/facts/$slot.json" >&2; exit 2; fi
tpl="$(cat "$REF/extraction-prompt.md")"
tpl="${tpl//\[slot name\]/$slot}"
tpl="${tpl//\[one line purpose\]/$purpose}"
tpl="${tpl//\[facts rows for this side\]/$facts}"
mkdir -p "$RUN/prompts-built" "$RUN/extracts-raw/$slot"
pf="$RUN/prompts-built/extract-$slot-$side.txt"
printf '%s\n' "$tpl" > "$pf"
rej="$RUN/extracts-raw/$slot/$letter.rejection.txt"
if [ -s "$rej" ]; then
  { printf '\n## Your previous report was rejected by a mechanical check\n\n'; cat "$rej"; } >> "$pf"
fi
raw="$RUN/extracts-raw/$slot/$letter.md"
bash "$S/headless.sh" clean "$dir" "$MODEL" "$pf" "$raw" "extract:$slot:$side"
rc=$?
if [ "$rc" -ne 0 ]; then exit "$rc"; fi
mkdir -p "$RUN/extracts/$slot"
mv "$raw" "$RUN/extracts/$slot/$letter.md"
