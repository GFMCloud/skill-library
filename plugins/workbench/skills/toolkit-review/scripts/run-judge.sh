#!/bin/bash
# toolkit-review: run one judge on the extraction reports of one slot.
# Usage: run-judge.sh <slot> <order>
#   order: XY | YX   comparison, the two reports read in that order (models.judge)
#          ESC       comparison on models.escalation, random order (used when a pair disagrees)
#          S1 | S2   self-review: one report R.md, judged against the bar; two runs for agreement
# cwd is $TR_RUN/extracts/<slot>/, which must hold only the report files.
RUN="${TR_RUN:?run-judge.sh: set TR_RUN to the run directory}"
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REF="$(dirname "$S")/references"
slot="$1"; order="$2"
dir="$RUN/extracts/$slot"
if [ -z "$slot" ] || [ ! -d "$dir" ]; then echo "run-judge.sh: no extracts for slot: $slot" >&2; exit 2; fi
JUDGE_MODEL=$(jq -r '.models.judge // "sonnet"' "$RUN/run.json" 2>/dev/null); JUDGE_MODEL="${JUDGE_MODEL:-sonnet}"
ESC_MODEL=$(jq -r '.models.escalation // "opus"' "$RUN/run.json" 2>/dev/null); ESC_MODEL="${ESC_MODEL:-opus}"
purpose="$(cat "$RUN/slots/$slot/purpose.txt" 2>/dev/null)"
if [ -z "$purpose" ]; then echo "run-judge.sh: missing $RUN/slots/$slot/purpose.txt" >&2; exit 2; fi
model="$JUDGE_MODEL"
case "$order" in
  S1|S2)
    if [ ! -s "$dir/R.md" ]; then echo "run-judge.sh: $dir must hold a non-empty R.md for a self-review" >&2; exit 2; fi
    extra=$(find "$dir" -type f -not -name R.md | wc -l | tr -d ' ')
    if [ "$extra" != "0" ]; then echo "run-judge.sh: $dir holds files other than R.md" >&2; exit 2; fi
    tpl="$(cat "$REF/self-review-prompt.md")"
    label="judge:$slot:$order:R" ;;
  XY|YX|ESC)
    if [ ! -s "$dir/X.md" ] || [ ! -s "$dir/Y.md" ]; then echo "run-judge.sh: $dir must hold non-empty X.md and Y.md" >&2; exit 2; fi
    extra=$(find "$dir" -type f -not -name X.md -not -name Y.md | wc -l | tr -d ' ')
    if [ "$extra" != "0" ]; then echo "run-judge.sh: $dir holds files other than X.md and Y.md" >&2; exit 2; fi
    case "$order" in
      XY) first=X; second=Y ;;
      YX) first=Y; second=X ;;
      ESC) model="$ESC_MODEL"; if [ $((RANDOM % 2)) -eq 0 ]; then first=X; second=Y; else first=Y; second=X; fi ;;
    esac
    tpl="$(cat "$REF/judge-prompt.md")"
    case "$slot" in
      challenge-*) note="$(cat "$REF/judge-challenge-note.md")"; tpl="${tpl/\#\# What to write, in this order/$note

## What to write, in this order}" ;;
    esac
    tpl="${tpl//\[first\]/$first}"
    tpl="${tpl//\[second\]/$second}"
    label="judge:$slot:$order:$first$second" ;;
  *) echo "usage: run-judge.sh <slot> XY|YX|ESC|S1|S2" >&2; exit 2 ;;
esac
tpl="${tpl//\[slot name\]/$slot}"
tpl="${tpl//\[one line\]/$purpose}"
mkdir -p "$RUN/prompts-built"
pf="$RUN/prompts-built/judge-$slot-$order.txt"
printf '%s\n' "$tpl" > "$pf"
exec bash "$S/headless.sh" clean "$dir" "$model" "$pf" "$RUN/judgments/$slot/judge-$order.md" "$label"
