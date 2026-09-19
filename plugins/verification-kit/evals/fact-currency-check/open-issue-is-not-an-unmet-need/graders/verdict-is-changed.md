---
type: regex
pattern: "\\bCHANGED\\b"
match: contains
---

Tests SKILL.md lines 44 to 47: "An open issue is not evidence of an unmet need...
check whether the thing was done, not whether the ticket was tidied." The fixture
release record shows the ask shipped in v3.2.0, so the claim that the feature is
missing is stale-open, and the verdict from the vocabulary at SKILL.md line 67 is
CHANGED, carrying the new value and what it invalidates (the two-week budget). A run
that reads the open ticket as confirmation, or that stops at UNVERIFIABLE without
consulting the record in front of it, does not produce this label. The word boundary
keeps UNCHANGED from matching.
