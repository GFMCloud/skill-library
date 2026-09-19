---
type: regex
pattern: "cubic-bezier\\(\\s*0\\.16\\s*,\\s*1\\s*,\\s*0\\.3\\s*,\\s*1\\s*\\)"
match: contains
target: { source: file, path: reveal.js }
---

`SKILL.md:80` fixes the easing curve by value, and the prompt asks for the
transition declaration to be pasted into the reply. Whitespace after the commas
is tolerated; any other curve, or a bare `ease-out`, fails.
