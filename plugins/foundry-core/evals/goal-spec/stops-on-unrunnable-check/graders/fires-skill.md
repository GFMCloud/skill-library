---
type: tool_used
tool: Skill
---
Tests the Stop-when rule in SKILL.md lines 104-107, "The check cannot
actually be run": when the named check fails for reasons unrelated to the
goal (here, the FIXTURE log file does not exist), the skill must say so,
name the exact command that failed and its output, and stop rather than
record a fabricated baseline. This grader confirms the skill actually fired
for the ask, so a pass on the other graders is credited to the skill and not
to a model that happened to behave well on its own.
