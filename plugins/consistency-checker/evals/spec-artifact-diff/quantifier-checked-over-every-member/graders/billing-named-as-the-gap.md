---
type: regex
pattern: "billing"
match: contains
---

Tests the scope-quantifier rule, `SKILL.md:39` and `SKILL.md:45-47`: "A quantifier is a
claim about every member of a set. Checking one member and generalising is how 'one
placeholder component each' survived a review over a set that was unevenly distributed."
The set has five members and only `modules/billing/` breaks the "every module folder
ships its own README.md" claim. Decidable because the defect cannot be stated without
naming the offending folder in the `TRUTH:` field, and a run that spot-checks `auth` or
`export` and generalises never emits the string.
