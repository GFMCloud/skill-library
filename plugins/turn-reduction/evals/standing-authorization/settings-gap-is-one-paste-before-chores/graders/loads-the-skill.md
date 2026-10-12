---
type: tool_used
tool: Skill
---

The rule under test lives in SKILL.md, "Settings that match the grants: `permissions`":
run `permissions` at adoption and before any chore a grant covers, and hand Graham its
output as one paste. Known weakness, from CONTRIBUTING.md: a `tool_used` grader on
`Skill` passes even when the skill was not found, so this grader alone never proves the
pack loaded. The other two graders carry the behaviour.
