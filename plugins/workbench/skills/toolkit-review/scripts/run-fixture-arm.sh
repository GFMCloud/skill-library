#!/bin/bash
# toolkit-review: run the review task on a fresh copy of the FIXTURE repo (full size only).
# Usage: run-fixture-arm.sh <arm> <run-number>     arm: bare | current | current-plus-candidate
# Results are fixture-derived and must be labelled so wherever they are reported.
# current-plus-candidate adds a markdown-only plugin directory at
# $TR_RUN/fixtures/review/arm-plugin (refused if it holds anything but markdown and a manifest).
# All arms get --tools "Read,Glob,Grep,Skill,Agent": without Skill a run sees no skills and
# without Agent it cannot invoke an agent (proven in the ECC run, 2026-09-17). Still no
# shell and no write tool. Model: models.fixture in run.json.
RUN="${TR_RUN:?run-fixture-arm.sh: set TR_RUN to the run directory}"
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
arm="$1"; n="$2"
repo="$RUN/fixtures/review/repo"
if [ -z "$n" ] || [ ! -d "$repo" ]; then echo "usage: run-fixture-arm.sh <arm> <n>  (needs $repo)" >&2; exit 2; fi
MODEL=$(jq -r '.models.fixture // "sonnet"' "$RUN/run.json" 2>/dev/null); MODEL="${MODEL:-sonnet}"
extra=(--tools "Read,Glob,Grep,Skill,Agent")
case "$arm" in
  bare) profile=bare ;;
  current) profile=current ;;
  current-plus-candidate)
    profile=current
    plug="$RUN/fixtures/review/arm-plugin"
    if [ ! -d "$plug" ]; then echo "run-fixture-arm.sh: missing $plug" >&2; exit 2; fi
    nonmd=$(find "$plug" -type f -not -name '*.md' -not -name plugin.json | wc -l | tr -d ' ')
    if [ "$nonmd" != "0" ]; then echo "run-fixture-arm.sh: REFUSED, $plug holds non-markdown files" >&2; exit 2; fi
    extra+=(--plugin-dir "$plug") ;;
  *) echo "run-fixture-arm.sh: unknown arm: $arm" >&2; exit 2 ;;
esac
work="$RUN/fixtures/review/work/$arm-$n"
rm -rf "$work"
mkdir -p "$(dirname "$work")" "$RUN/prompts-built"
cp -R "$repo" "$work"
pf="$RUN/prompts-built/fixture-task.txt"
printf '%s\n' "Review this repo for issues. Report each finding with the file, the line, and the evidence for it. Say what you checked and what you did not check." > "$pf"
exec bash "$S/headless.sh" "$profile" "$work" "$MODEL" "$pf" "$RUN/fixtures/review/runs/$arm-$n.md" "fixture:$arm:$n" "${extra[@]}"
