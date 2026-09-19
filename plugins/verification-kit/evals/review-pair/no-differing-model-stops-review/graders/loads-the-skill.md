---
type: tool_used
tool: Skill
min: 1
---

Tests SKILL.md "Stop when", line 77 to 80: "A reviewer model cannot be reached, or no
model differing from the builder's is configured: stop and say so. Running the reviewer
on the same model as the builder defeats the independence mechanism this skill exists to
provide." The prompt tells the model, as a FIXTURE fact about the environment, that no
model other than its own is configured for subagents. The failure mode is spawning a
same-model reviewer anyway and treating its output as an independent verdict. The case
only tests review-pair's own rule if the skill fired.
