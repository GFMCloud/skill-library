---
type: regex
pattern: "IntersectionObserver"
match: contains
target: { source: file, path: reveal.js }
---

`SKILL.md:80` names the required API as a literal identifier and forbids the
alternative by name. The prompt asks for the opening lines of `reveal.js` and for
the API to be named in the reply, so the string is decidable from the reply text.
A scroll listener implementation never spells `IntersectionObserver`.
