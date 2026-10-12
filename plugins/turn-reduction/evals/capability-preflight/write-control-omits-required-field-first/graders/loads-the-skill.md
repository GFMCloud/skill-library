---
type: tool_used
tool: Skill
---

The skill has to fire for its write-control rule (`SKILL.md:113`) to be in play, rather
than the model judging the control from general API knowledge. Known trap
(CONTRIBUTING.md, Evaluation cases): a `tool_used` grader on `Skill` passes even when the
skill was not found; the `names-omitted-required-field` grader carries the evidence.
