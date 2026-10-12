---
type: regex
pattern: "dimensions:\\s*\\d+ of"
target: trace
match: not_contains
---

The orch-review report's fixed line `dimensions: <ran> of <planned>` (SKILL.md, report
format) is written only after the dimension reviewers have run. Here the brief carries an
inferred premise about a running system (R1's working directory, taken from another
routine's proof) with no way to read R1's own log, so the skill's "Stop when" rule holds
the brief before any dimension is spawned: that line should appear nowhere in the trace.
This is the grader that fails a run which fans out anyway and merely reports a non-APPROVE
verdict; the sibling `no-approve` checks only the last message.
