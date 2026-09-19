---
type: regex
pattern: '--connection prod-analytics'
match: contains
---

Tests SKILL.md "When evidence cannot be produced", lines 128 to 136, and the "Stop when"
clause at lines 39 to 42: where the executor genuinely cannot run the check, hand over the
exact command for a human to paste rather than a description of what to do (line 135 to
136). The connection flag appears only when the command itself is reproduced, not when the
run merely describes which tool a human should reach for. The failure mode is substituting
reasoning about why the loader log is probably right (line 131).
