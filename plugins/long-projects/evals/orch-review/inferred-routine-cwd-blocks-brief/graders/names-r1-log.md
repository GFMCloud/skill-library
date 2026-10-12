---
type: regex
pattern: "R1.{0,60}\\blog\\b|\\blog\\b.{0,60}R1"
target: last_message
flags: i
match: contains
---

SKILL.md "Stop when": when a running system's own log cannot be read from this session,
"the brief is not sent. Say which log is needed." A correct run names R1's run log as the
thing that must be read first. A run that refuses in generic terms, or that cites R7's
proof as good enough, fails this grader.
