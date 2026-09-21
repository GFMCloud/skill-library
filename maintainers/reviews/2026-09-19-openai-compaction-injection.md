---
contract: v1
source: https://alignment.openai.com/misalignment-reports/self-generated-prompt-injections-in-compaction-summaries/
type: article
pin: fetched 2026-09-19, sha256 27983c70ee6c2bd9462111d2edcc120879fdb72b2bbd7a02a8eb644a5f9f859d
reviewed: 2026-09-19
verdict: HARVEST
recheck:
applied: none (three rows proposed, Q-2026-09-19-6 in claude-scout-weekly STATE.md)
evidence: maintainers/reviews/2026-09-19-openai-compaction-injection/ (decisions.md, cleanroom-review.md, comparison.md)
---

# openai-compaction-injection

**Verdict:** HARVEST. The report is not a tool; one rule transfers to `handoff` (a summary cannot confer authority, the user's visible words win), plus a README sentence and one incumbent-side question about the carry-over hook.

**Ancestry:** none.

## What landed

Nothing yet. Rows 1 to 3 are proposed.

## What was declined, and why

- Rows 4 and 5: training-loop techniques with no consumer on this machine.
- Row 6: `handoff` already separates "done" from "verified" with executed output.

## Flags

The source quotes three model-written injection texts as evidence. Treated as data. Nothing addresses a reviewing agent.

## Re-review trigger

A follow-up report with denominators, or a comparable report about Claude Code's own compaction.

Record location note: written to claude-scout-weekly `docs/proposals/` on 2026-09-19 because the Stage C migration was live on skill-library (A-11); moved here with its directory by scout cycle 5 on 2026-09-21, after Stage C closed (PR 27 merged 2026-09-19 20:41 CDT).
