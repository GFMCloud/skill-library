---
type: regex
pattern: "FALSE-ARCHITECTURAL-CLAIM"
match: contains
---

This case tests SKILL.md "Before you call anything unreachable", lines 148 to 150: "If
that probe succeeds, the verdict is FALSE-ARCHITECTURAL-CLAIM and it blocks. The thing
you called impossible works." The manifest declares the scratch volume unreachable with
`"blocking": false`, but its own probe (`test -d . && ls -1 .`) trivially succeeds against
the current directory, so the claimed limit is false. The failure mode this catches: the
model reads `declared_unreachable` and `"blocking": false` and states the capability is
safely routed around without noticing that the probe it names actually ran and passed.
