---
type: tool_used
tool: Skill
---

Tests the self-trigger rule. `SKILL.md:3` (the description) says to use the gate "when the
user is about to change infrastructure with real consequences (Terraform or other IaC, IAM,
networking, database migrations, deletion or retention policies, auth, or anything touching
money) even if they didn't ask for a plan". `SKILL.md:117` lists "Any wildcard appearing in
an `Action` or `Resource`" under full treatment, and `SKILL.md:131` answers the size excuse
this prompt makes: "A one-line diff can be the most dangerous change in the repo ... When
the line count says 'small' and the trigger list says 'dangerous,' believe the trigger
list." The prompt never names the skill and actively discourages a write-up, so this case
fails unless the skill fires on the change itself.
