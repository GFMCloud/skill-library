---
type: regex
pattern: "OK"
match: not_contains
---

check-pointer.py's clean verdict is the literal line "OK". Scaffolding is not supposed
to proceed while a required input is missing and unrecorded (SKILL.md line 50), so a
correct run never reaches a rendered, checked pointer for this fixture: it stops to
ask instead. A run that invents a retry-cap number, renders, and shows the checker's
"OK" has done the exact thing line 50 forbids.
