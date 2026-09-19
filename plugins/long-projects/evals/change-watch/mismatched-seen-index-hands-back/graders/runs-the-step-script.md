---
type: tool_used
tool: Bash
---

Shows the run actually copied the fixture and invoked the skill's step script
rather than answering from description alone. Both sibling cases in this
suite (transition-reports-once, unclassified-action-refused) grade skill
firing the same way, through the Bash call that runs the script, rather than
tool_used on Skill, since the prompt points at SKILL.md by path rather than
naming the Skill tool.
