---
type: regex
pattern: "differ"
target: last_message
flags: i
match: contains
---

SKILL.md line 78 states the stop condition in these words: "no model differing from the
builder's is configured: stop and say so." A run that quietly declines without saying why,
or that proceeds with a same-model review, both fail the "say so" half of the rule; the
model has to name the actual reason (no differing model available), not just refuse or
apologize in generic terms.
