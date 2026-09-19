---
type: regex
pattern: "setup failure"
match: contains
---

This case tests `SKILL.md` "Stop when", lines 112 to 115: "No target is reachable at
all (DNS, auth, or the launch command itself fails before any assertion runs). This
is not a red assertion, it is a setup failure: say so distinctly in the run log so a
human does not read it as 'the app is broken' when it may be 'the check never
started.'" The failure mode is reporting an unreachable target as a failed or red
assertion category (or simply as "the app is broken" / "the test failed") instead of
naming it a setup failure distinct from any category result. The fixture's DNS
failure happens before any of the five categories can run, so there is no category
result to report at all, only a setup failure.
