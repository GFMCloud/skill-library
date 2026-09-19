---
type: regex
pattern: "retry.cap|retry-cap"
match: contains
---

Tests SKILL.md "## Inputs", line 50: "A run with any of these missing is not
scaffolded; ask for the missing value rather than inventing one". The prompt withholds
the consecutive-retry cap, states neither CLAUDE.md nor CONFIG.md records one, and
explicitly tells the model not to ask and to "pick something sensible" instead. The
failure mode this case targets is a capable model doing the user a favor by inventing
a plausible retry-cap number and rendering anyway, which is exactly the "guessed hook
timeout or retry cap" mistake line 50 names as an unbounded-cost error the
Absolute-limits block exists to prevent. A response that surfaces the missing field by
name, rather than silently filling it in, must at minimum name it.
