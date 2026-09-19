# Source

Vendored from `cloudflare/security-audit-skill`, path `skills/security-audit/`, at commit
`c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`, on 2026-09-18. MIT, Copyright (c) 2025-2026
Cloudflare, Inc.; the licence text is `LICENSE` in this directory.

Every file is byte-identical to that commit except `SKILL.md`, where only the frontmatter
changed: the description gained its negative scope, its costs and this pointer, and a
`metadata.maturity: incubator` block was added. The body is untouched. `LICENSE` and this
file are the only additions.

This is a deliberate exception to the library's practice of rewriting adopted material in
its own voice. The value here is two dependency-free validators
(`validate-findings.cjs`, `validate-coverage-ledger.cjs`) and their tests, which are only
worth having as written. Ruled by Graham at Gate B of the 2026-09-18 pack review ("B5 -
Adopt as a sep skill as well", then "approve with defaults" on the plan-gate); record in
`maintainers/reviews/2026-09-18-pack-review.md`.

To update: re-vendor from a newer commit, re-run both test files, and change the commit
above. Do not edit the vendored files in place; an edit here is drift from upstream.

Consequences of vendoring unmodified, known and accepted: the body does not carry the
library's four contract sections (the validator warns, W4, and passes for incubator), and
the reference files sit at the skill root and not under `references/`.
