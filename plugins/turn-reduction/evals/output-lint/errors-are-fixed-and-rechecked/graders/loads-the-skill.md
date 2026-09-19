---
type: tool_used
tool: Skill
---

This case tests `SKILL.md` "Stop when", lines 37 to 38: "Exit 1: errors are present; fix
the draft and re-run, never send with an error standing." The failure mode is handing the
draft back with the errors reported but still standing, or fixing it and calling it clean
without a second run. The fixture draft carries two error rules the sibling cases do not
touch (announced-write and interpreter). The skill has to fire for any of that to be the
skill's doing.
