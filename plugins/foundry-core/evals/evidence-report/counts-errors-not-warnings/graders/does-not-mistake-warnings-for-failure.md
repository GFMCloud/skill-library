---
type: regex
pattern: "VERDICT:\\s*FAILED"
match: not_contains
---

The 47 warnings are not errors; the check returned 0 errors. A report that
treats the warning count as a failure signal writes "VERDICT: FAILED", which
this grader rules out.
