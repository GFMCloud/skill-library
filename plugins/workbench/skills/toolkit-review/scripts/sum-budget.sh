#!/bin/bash
# toolkit-review: total tokens from the run's budget file against its ceiling.
# Usage: sum-budget.sh [extra-tokens]
# Prints runs, input (incl. cache reads), output, total, ceiling, percent and a count per
# status. <extra-tokens> adds spend metered outside the budget file (the orchestrator's own
# session, subagents) so the one ceiling covers the whole run, not only the headless calls.
# Exits 8 at or past budget_stop_percent (run.json, default 80).
RUN="${TR_RUN:?sum-budget.sh: set TR_RUN to the run directory}"
B="$RUN/budget/usage.tsv"
ceiling=$(jq -r '.budget_ceiling_tokens // 0' "$RUN/run.json" 2>/dev/null)
stop=$(jq -r '.budget_stop_percent // 80' "$RUN/run.json" 2>/dev/null)
extra="${1:-0}"
if [ ! -s "$B" ]; then echo "no usage recorded yet; ceiling $ceiling"; exit 0; fi
awk -F'\t' -v c="$ceiling" -v s="$stop" -v x="$extra" '{ i += $5; o += $6; n++; st[$7]++ } END {
  t = i + o + x; printf "runs: %d\ninput tokens (incl. cache): %d\noutput tokens: %d\nextra (unmetered, given): %d\ntotal: %d\nceiling: %d\npercent: %.1f\nstop at: %d percent\n", n, i, o, x, t, c, (c > 0 ? 100 * t / c : 0), s;
  for (k in st) printf "status %s: %d\n", k, st[k];
  if (c > 0 && t >= s / 100 * c) exit 8 }' "$B"
