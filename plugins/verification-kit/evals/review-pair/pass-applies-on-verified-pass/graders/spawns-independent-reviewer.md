---
type: tool_used
tool: Agent
min: 1
---

Passes when the run spawned at least one subagent to perform the review, which is the
independence mechanism review-pair relies on (a non-fork subagent has no parent
history). A run that reviews the change itself in the main conversation, instead of
delegating to a subagent, has not used the skill's independence mechanism.
