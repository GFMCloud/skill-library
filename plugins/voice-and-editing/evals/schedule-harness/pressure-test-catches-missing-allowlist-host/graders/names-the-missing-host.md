---
type: regex
pattern: "feeds\\.example\\.net"
target: last_message
match: contains
---

A correct run names the host that is fetched but not allowlisted. The failure this case
targets is reading the allowlist and the fetch list separately and calling the design
ready, which is how the 2026-10-10 design passed three review rounds with the same gap.
