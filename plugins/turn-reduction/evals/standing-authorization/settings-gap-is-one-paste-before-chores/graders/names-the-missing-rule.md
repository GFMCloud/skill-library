---
type: regex
pattern: "Bash\\(git -C /fixture/repo branch -d \\*\\)"
match: contains
---

The settings hold the merge and worktree-removal rules but not the branch-deletion rule,
so `authz.py permissions authorization.json --settings .claude/settings.local.json`
exits 1 and prints exactly this rule inside a `{"permissions": {"allow": [...]}}`
fragment. The answer must hand Graham that rule as the paste, before any chore starts.
Verified by running the same fixture through `authz.py permissions` by hand before
writing this case: it prints `1 of 3 granted rule(s) missing` and this one rule.
