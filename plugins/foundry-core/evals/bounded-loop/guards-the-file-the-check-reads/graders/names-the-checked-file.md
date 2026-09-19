---
type: regex
pattern: "tests/test_login\\.py"
match: contains
---

The `--guard` flag alone is not enough: SKILL.md line 45 says to "name every file the
check itself reads to decide pass/fail." A setup that adds `--guard` pointing at some
other path, or with no path at all, would pass the sibling grader but still leave the
real file the check reads unguarded. The prompt names the one file the check reads
(`tests/test_login.py`) explicitly, so that literal path appearing in the setup command
is decidable and distinguishes "guarded something" from "guarded the right thing."
