---
type: regex
pattern: "Geist Mono|SF Mono|JetBrains Mono"
match: contains
target: { source: file, path: type.css }
---

`SKILL.md:37` gives the monospace target literally. The generic default for a
keyboard-shortcut style is `monospace` or `ui-monospace` alone, which matches
none of these names.
