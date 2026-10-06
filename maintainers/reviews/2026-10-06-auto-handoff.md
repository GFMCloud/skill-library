---
contract: v1
source: https://github.com/obie/auto-handoff
type: code-repo
pin: 19405aa47bcb31ef775a427a7118f9519ea21734
reviewed: 2026-10-06
verdict: HARVEST
recheck: -
applied: none yet (row 3 landed by overlap with Q-2026-09-21-4 row 1 in handoff 0.6.4, this cycle's long-projects commit; rows 1, 2, 4 await ruling, Q-2026-10-06-9)
evidence: maintainers/reviews/2026-10-06-auto-handoff/ (cleanroom-review.md, comparison.md, decisions.md); scout run log claude-scout-weekly/runs/2026-10-06.md
---

# auto-handoff

**Verdict:** HARVEST. A 145-line function-hooks plugin that runs a handoff command after 50
idle minutes, before the one-hour prompt cache expires; the trigger is a real gap (nothing
installed acts on idle), but the plugin itself ships a skill with the bare name `handoff`, no
redaction and no typed claims, on an early-access API, with an untested latch assumption.

**Ancestry:** none; convergent narrative sections only.

## What landed

- Row 3, standing instructions travel with the handoff: covered by the ratified INVARIANTS
  field (Q-2026-09-21-4 row 1) and the "Standing instructions travel" Behavior Note in
  `plugins/long-projects/skills/handoff/SKILL.md` (handoff 0.6.4, long-projects 0.19.5, this
  cycle's commit).
- Rows 1 (the idle trigger as our own mod), 2 (an unattended-runs section for the installed
  handoff skill) and 4 (three cold-cache sentences in `cache-economics.md`, which fits Tier 2
  as written) are proposed, Q-2026-10-06-9.

## What was declined, and why

- Row 5 (sleep detection, origin set, latch, timer test technique): travels with row 1 as
  code, not prose.
- Row 6 (the bundled `handoff` skill, its template, the default command): redundant to a
  stricter incumbent and a bare-name collision; its files are invisible to
  `session-carryover.py`.

## Flags

The bundled skill's "Ask no questions and wait for no confirmation" and its `allowed-tools`
line, both by design and narrow; the README's advice to grant your own `allowed-tools` for a
replacement command widens what runs unattended. Nothing addresses the reviewing agent or asks
for credentials. Not acted on.

## Re-review trigger

A second maintainer or a test for the `$.command.run` origin assumption; the pin moving past
0.1.0; or a decision here to build an idle-triggered mod, at which point `register.ts` is
re-read in full before any vendoring. Context for that decision: alexknowshtml/claude-auto-handoff
(W-58) is the context-threshold form of the same trigger.
