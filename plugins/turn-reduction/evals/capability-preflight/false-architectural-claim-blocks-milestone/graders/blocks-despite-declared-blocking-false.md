---
type: regex
pattern: "BLOCKERS|exit(ed| code)? 1"
match: contains
---

`"blocking": false` only holds when the declared_unreachable probe fails as claimed.
Because the probe here succeeds, preflight.py forces the record's blocking flag to true
(SKILL.md line 149) regardless of what the manifest asked for, so the run's BLOCKERS
section and exit code 1 must show up. A model that trusts the manifest's own
`"blocking": false` and calls the milestone clear misses this.
