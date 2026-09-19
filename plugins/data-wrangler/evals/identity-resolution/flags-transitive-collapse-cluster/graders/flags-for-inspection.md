---
type: regex
pattern: "inspect"
match: contains
flags: i
---

SKILL.md line 92 requires that any cluster above two members be inspected before
it is accepted as one entity, and the Stop-when section (line 37) treats an
uninspectable cluster above two members as a reason to stop rather than resolve.
V1, V2 and V3 form exactly such a cluster once V1-V2 (0.93) and V2-V3 (0.91) are
each accepted on their own: the response must say the group needs inspection
before being collapsed to a single canonical row, not merge all three silently
because two of the three pairwise scores individually cleared the threshold.
