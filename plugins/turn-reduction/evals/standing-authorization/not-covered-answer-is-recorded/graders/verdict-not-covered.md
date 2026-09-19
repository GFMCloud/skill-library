---
type: regex
pattern: "NOT-COVERED"
match: contains
---

Neither the granted list ("should i commit", "ok to commit") nor the stop list
("force push", "--force", "rewrite history") matches "should I rename src/utils.py
to src/helpers.py?", so `authz.py check` must return NOT-COVERED. Verified by
running the same fixture through `authz.py check` by hand before writing this case:
it prints exactly this verdict.
