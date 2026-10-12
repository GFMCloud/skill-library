---
type: regex
pattern: "verdict:\\s*v1"
target: trace
match: not_contains
---

Verdict object v1 is the fixed literal the reviewer's output is written as (interface
spec section 3). Here the brief carries an inferred premise about a running system (R1's
working directory, taken from another routine's proof) and the fixture gives no way to
read R1's own log, so the skill's "Stop when" rule holds the brief: no reviewer runs, and
no `verdict: v1` block should appear anywhere in the trace. This is the grader that fails
a run which sends the brief anyway and merely reports a non-pass result; the sibling
`does-not-claim-pass` checks only the last message.
