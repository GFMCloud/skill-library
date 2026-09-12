---
type: regex
pattern: "VERDICT:[^\\n]*(rules out|empty|#53948)"
match: contains
---

A verdict that does not say what failure mode it eliminates is decoration. Here the claim rules out the empty-cache-dir failure.
