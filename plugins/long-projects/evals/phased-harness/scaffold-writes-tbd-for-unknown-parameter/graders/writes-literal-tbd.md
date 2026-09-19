---
type: regex
pattern: "TBD"
match: contains
---

Tests SKILL.md line 117-118: "Parameters the user did not supply stay literally
`TBD` in CONFIG.md, and the generated CLAUDE.md + dispatch skill both stop on
`TBD`. Never invent a value." The prompt marks the archive repo path
FIXTURE-UNKNOWN and tells the model not to guess. The skill's own text requires
the literal string `TBD` in that case, and the prompt asks the model to cat
CONFIG.md into its output, so the transcript must contain it if the rule was
followed. A run that invents a plausible path (for example writing a made-up
`/repos/archive` value) instead of `TBD` fails this grader.
