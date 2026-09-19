---
type: regex
pattern: "#FDEBEC|#E1F3FE|#EDF3EC|#FBF3DB"
match: contains
flags: i
target: { source: file, path: palette.css }
---

`SKILL.md:45-49` permits exactly four accent backgrounds and names each by hex.
Three status badges cannot be built inside the palette without at least one of
them. A run that reaches for saturated status colors emits none of these four
strings.
