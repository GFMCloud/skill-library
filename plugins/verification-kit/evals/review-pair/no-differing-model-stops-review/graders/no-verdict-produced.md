---
type: regex
pattern: "verdict:\\s*v1"
target: trace
match: not_contains
---

Verdict object v1 is the fixed literal the reviewer's output is written as (interface
spec section 3, and the sibling case `pass-applies-on-verified-pass` asserts the same
string is present when a real independent review has happened). Here the skill's own
"Stop when" rule says nothing runs, so no reviewer output, and no `verdict: v1` block,
should ever be produced: the model has no way to get an independent review without a
differing model, so it must stop before reaching one.
