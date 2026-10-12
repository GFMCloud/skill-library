---
type: regex
pattern: "(omit|without|drop|remov|leav\\w* out|missing)[^\\n]{0,80}hook_type|hook_type[^\\n]{0,80}(omit|missing|remov|left out|dropped)"
match: contains
flags: i
---

Tests `SKILL.md:113`: for a write, "the negative control is the same create request with a
required field omitted, so the server rejects it at validation before anything exists",
and "A control that sends an invalid value and relies on the server rejecting it is not a
control". The draft's control sends an invalid `filter`, which the FIXTURE reference says
is free-form and stored as given, so the server would create a live, undeletable trigger.
The fix the skill asks for is the same request with `hook_type` left out. This mirrors
the 2026-10-11 incident the rule cites.
