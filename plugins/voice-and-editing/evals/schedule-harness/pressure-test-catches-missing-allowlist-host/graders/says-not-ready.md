---
type: regex
pattern: "not ready|item 1 fails|fails item|failing item|blocks? the (first )?(unattended )?run|blocked|(is|put|stays) on hold|holds? the run"
target: last_message
flags: i
match: contains
---

The checklist's own rule: "One failing item blocks the first unattended run." A reply
that names the host but still clears R2 for tonight's run has not applied the checklist.
The pattern names the failing item or the blocked run, not a bare "fail" or "hold", so
"no item fails" or "nothing on hold" does not satisfy it.
