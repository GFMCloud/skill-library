---
type: regex
pattern: "VERDICT:[^\\n]*0 errors"
match: contains
---

Tests SKILL.md "Rules", the "Count errors, not adjectives" bullet, lines 91-94:
"Tools emit reassuring words alongside failures... The number that matters is
the error count." The FIXTURE output here pairs a large warning count (47)
with a reassuring adjective ("passed") and the real number that decides the
verdict (0 errors). A report that follows the rule states the error count on
the VERDICT line instead of just repeating "passed". A report that ignores
the rule can drop the count entirely and lean on the adjective, or get
spooked by the 47 warnings and hedge, either of which fails this grader.
