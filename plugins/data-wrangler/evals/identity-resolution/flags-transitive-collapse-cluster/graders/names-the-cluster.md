---
type: regex
pattern: "cluster"
match: contains
flags: i
---

Tests SKILL.md line 91 ("Cluster explicitly and inspect any cluster above two
members before accepting it") together with the Verify section's requirement,
line 24, that "every cluster is listed." V1-V2 (0.93) and V2-V3 (0.91) both clear
the accept threshold but V1-V3 (0.71) does not: chaining them into one entity by
transitivity, without naming the three-record group a cluster, is exactly the
"Transitive collapse" trap the skill names at lines 90-92. The word "cluster" is
the skill's own required vocabulary for this group, not an invented label a model
might or might not reach for on its own.
