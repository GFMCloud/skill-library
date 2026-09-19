---
type: regex
pattern: "uploading a handoff file from a previous Claude session"
match: contains
---

The copy-paste prompt block opens with this fixed line (`SKILL.md:249`). It is a
verbatim string the skill supplies, not wording the prompt suggests, so a run that
hands over only the file, or that replaces the block with its own summary, does not
produce it.
