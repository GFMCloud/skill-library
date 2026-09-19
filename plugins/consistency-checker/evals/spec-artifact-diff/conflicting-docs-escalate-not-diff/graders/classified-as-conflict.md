---
type: regex
pattern: "[Cc]onflict"
match: contains
---

Tests the third classification in Step 4, `SKILL.md:136-137`: "Conflict: two documents
assert different decisions. Not a diff. Escalate with both locations named." Nothing in
`src/archive.py` implements a retention window, so no command can settle which number is
correct, and the prompt pushes for a winner to be picked. `Conflict` is the literal label
the skill names for this class, so a run that quietly picks 30 or 90 days as the truth
never emits it.
