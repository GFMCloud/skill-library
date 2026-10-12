---
type: tool_used
tool: Skill
---

Tests the widened trigger in `SKILL.md:3`: "asked to brainstorm or audit, then propose a
design, architecture, pipeline or plan for approval: load it before the first proposal".
The prompt is the first user message of the 2026-10-10 session (transcript
`c0558760-bc8d-4f18-a30f-b193335137e5`, line 5), quoted verbatim with one framing
paragraph added so the run writes a page. It never names plan-gate and never says "plan".
In that session the skill loaded only at the later plan stage. Known trap
(CONTRIBUTING.md, Evaluation cases): a `tool_used` grader on `Skill` passes even when the
skill was not found, so this grader alone does not prove plan-gate loaded; the
`plan-has-assumptions` grader checks for the skill's output shape.
