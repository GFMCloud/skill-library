#!/bin/bash
# toolkit-review: static safety read of one chunk of candidate hook code (full size only).
# Usage: run-reader.sh <chunk-number>
# cwd is $TR_RUN/readthrough/input/chunk-<n>/, clean profile, nothing executed.
# Model: models.reader in run.json.
RUN="${TR_RUN:?run-reader.sh: set TR_RUN to the run directory}"
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REF="$(dirname "$S")/references"
n="$1"
dir="$RUN/readthrough/input/chunk-$n"
if [ -z "$n" ] || [ ! -d "$dir" ]; then echo "run-reader.sh: no such chunk: $dir" >&2; exit 2; fi
MODEL=$(jq -r '.models.reader // "sonnet"' "$RUN/run.json" 2>/dev/null); MODEL="${MODEL:-sonnet}"
exec bash "$S/headless.sh" clean "$dir" "$MODEL" "$REF/reader-checklist.md" "$RUN/readthrough/report-$n.md" "reader:chunk-$n"
