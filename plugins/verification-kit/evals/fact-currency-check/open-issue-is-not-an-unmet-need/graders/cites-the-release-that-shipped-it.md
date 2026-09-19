---
type: regex
pattern: "3\\.2\\.0"
match: contains
---

SKILL.md line 34 makes the primary source for a status claim the system of record,
checked today. Here that record is the fixture changelog, which says the feature shipped
in v3.2.0. A run that reasons from the ticket's open state never names that release. (A
`tool_used: Read` grader was tried first and was wrong: the run writes the fixture itself,
so it has no need to read it back.)
