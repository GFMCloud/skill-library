---
type: regex
pattern: "npx --yes lighthouse"
match: contains
---

Rule: SKILL.md lines 117-119, Stop when, URL does not resolve: quote the
exact command and its error, stop, do not guess at scores or fabricate a
baseline. The exact command is SKILL.md line 51's own Verify text
(`npx --yes lighthouse <url> --output=json ...`). Its literal presence, with
the real URL filled in, is decidable proof the run showed what it tried
instead of inventing a table for a target it never reached.
