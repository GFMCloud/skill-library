---
type: regex
pattern: "#EAEAEA"
match: contains
flags: i
target: { source: file, path: palette.css }
---

`SKILL.md:44` and `SKILL.md:54` name one literal value for every card border and
divider, and `SKILL.md:91` repeats it as an execution step. The prompt asks for
the border written out in full and for every hex value to be listed in the reply,
so the required string is decidable from the reply text. Any other gray, or a
Tailwind `border-gray-200`, fails.
