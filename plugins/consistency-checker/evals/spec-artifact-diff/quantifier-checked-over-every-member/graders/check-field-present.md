---
type: regex
pattern: "CHECK:"
match: contains
---

Step 5, `SKILL.md:142-151`, requires four literal fields per defect, one of which is the
`CHECK:` line carrying the command the finding rests on. `SKILL.md:26` says the command
used is recorded and goes in the report. The label is fixed text, so its absence means
the required format was not followed.
