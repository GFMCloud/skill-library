---
type: regex
pattern: "--guard"
match: contains
---

Tests SKILL.md "Inputs", lines 43 to 46: "Optionally, one or more guarded paths
(`--guard`): the verifier and test files that must not change between attempts. Name
every file the check itself reads to decide pass/fail; an unguarded test file can be
edited to make a failing attempt look like it passed." The failure mode is installing
the Stop hook with `--check` and `--budget` but no `--guard`, which leaves the one file
this check reads free to edit between attempts, so a failing attempt can be made to look
passing without the hook ever noticing. `--guard` is the skill's own literal flag name,
so its presence in the setup command is decidable.
