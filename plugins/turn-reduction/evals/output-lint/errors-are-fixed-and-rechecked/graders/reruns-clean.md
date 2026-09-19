---
type: regex
pattern: "PASS[\\s\\S]*0 errors"
match: contains
---

`output_lint.py` prints exactly one clean verdict line, "PASS", followed by "0 errors,".
Only a second run on the corrected draft produces it: the first run on the fixture ends
"FAIL", with "error(s)" rather than "0 errors,". Showing that line is the evidence that
the draft was re-run after the fix rather than declared clear.
