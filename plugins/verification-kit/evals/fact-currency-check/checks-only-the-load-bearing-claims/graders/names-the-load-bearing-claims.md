---
type: regex
pattern: "load-bearing|Load-bearing"
match: contains
---

Tests SKILL.md step 1, lines 21 to 23: "Mark which claims are load-bearing. A claim
is load-bearing if a decision changes when it flips. Check those. Do not check the
rest." The brief mixes two claims that move the version decision with three that
cannot. A run that checks all five, or that never separates them, has skipped the
step the skill opens with. The term is the skill's own label for the selection, so
the output has to carry it.
