---
type: regex
pattern: "SF Pro Display|Geist Sans|Switzer"
match: contains
target: { source: file, path: type.css }
---

`SKILL.md:35` gives the sans stack as a literal target: `'SF Pro Display',
'Geist Sans', 'Helvetica Neue', 'Switzer', sans-serif`. A run that defaults to
Inter, Roboto or Open Sans emits none of these three names. Helvetica Neue is
deliberately left out of the pattern because a generic system stack can reach it
by accident.
