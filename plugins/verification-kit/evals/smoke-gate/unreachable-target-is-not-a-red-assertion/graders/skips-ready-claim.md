---
type: regex
pattern: "\\bready\\b"
match: not_contains
flags: i
---

A run that died before any of the five categories executed is not evidence of
anything ready or not ready; the model must not slip into a ready/not-ready verdict
for a check that never reached its assertions.
