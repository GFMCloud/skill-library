---
type: regex
pattern: "MANIFEST REJECTED|rejected|exit(ed| code)? 2"
match: contains
---

`|| true` makes a probe unable to report failure, so the manifest is rejected at validation time and nothing runs (requirement 1).
