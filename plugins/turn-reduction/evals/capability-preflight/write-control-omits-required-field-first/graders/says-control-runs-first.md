---
type: regex
pattern: "(negative control|control)[^\\n]{0,80}\\bfirst\\b|\\bfirst\\b[^\\n]{0,40}(negative control|control)"
match: contains
flags: i
---

The prompt asks for the run order. `SKILL.md:113`: "`preflight.py` runs every negative
control before its read and write probes, and when the control does not fail it does not
run the write." Known weakness: the pattern accepts any sentence placing "control" near
"first", so it shows the order was stated, not that it was stated correctly.
