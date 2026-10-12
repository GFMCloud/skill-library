---
type: tool_order
before: Skill
after: Write
---

The gate has to load before the proposal page exists, not after it. `SKILL.md:135`: "the
gate starts before the first proposal is written, not when the work later reaches a plan
stage." A run that writes `proposal.md` and then loads the skill reproduces the
2026-10-10 failure and fails here.
