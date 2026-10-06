---
contract: v1
source: https://runbook.scosovan.com/claude-code-routine-reported-success-did-nothing/
type: article
pin: fetched 2026-10-06, sha256 8b1cd7956bcdac94ce46ecbd5caa93705520d36b97346ac01de3ab77fc5dd31d
reviewed: 2026-10-06
verdict: HARVEST
recheck: -
applied: none (rows 1 to 4 await ruling, Q-2026-10-06-11 and Q-2026-10-06-6 (e); row 5 is watch row W-64)
evidence: maintainers/reviews/2026-10-06-scosovan-routine-postmortem/ (cleanroom-review.md, comparison.md, decisions.md); scout run log claude-scout-weekly/runs/2026-10-06.md
---

# scosovan routine postmortem

**Verdict:** HARVEST, thin. A vendor post whose one sharp idea, that a green Routine run only
means the session exited cleanly and an unreadable source must never render as empty, the
incumbents already hold at harness level; three fragments sharpen the wording, every platform
claim is asserted with a date and nothing is quoted, and the comparison found a defect in
`schedule-harness` in passing.

**Ancestry:** none; convergent.

## What landed

- Nothing in the library this cycle. Row 1 (verbatim error text and the explicit window in
  the unreachable record) is a scout-harness edit, Q-2026-10-06-6 (e); rows 2 (an OK or
  PARTIAL token on a run's first line), 3 (late-run disclosure and the intended window) and 4
  (the incumbent defect: schedule-harness tells the pointer to carry a time guard that its
  template and the interface spec's section 7 forbid) are proposed, Q-2026-10-06-11.
- Row 5 (the four unverified Routine platform claims) is watch row W-64 until the Routines
  doc is quoted with a fetch date.

## What was declined, and why

- Row 6: a same-session verification step (the spec's independent reviewer is stronger), the
  head-SHA idempotency key (seen-index entry v1 handles re-fire and flapping), the eight-row
  checklist as a whole (each row covered where it overlaps), and matching the exact
  `x-deny-reason` header (brittle, unverified).

## Flags

None addressed to an agent. Commercial funnel to a paid product; author slug `manus_admin`
and four same-day posts suggest agent-written content. The Check 5 prompt block is addressed
to the reader. Nothing acted on.

## Re-review trigger

The Routines doc quoted with a fetch date (closes W-64 one way or the other); a Routine
being registered from this machine (`change-watch`), which would make the connector-pruning
claim load-bearing.
