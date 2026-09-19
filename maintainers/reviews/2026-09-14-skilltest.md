---
contract: v1
source: https://github.com/archplg/skilltest
type: code-repo
pin: 6191446a56d93bfe299512f73da6f1b394758def
reviewed: 2026-09-14
verdict: HARVEST
recheck: n/a
applied: rows 2 and 5 as cross-references in the config-drift-checker decisions file (same commit as this record); rows 1, 3, 4 proposed to /phase ratify in claude-scout-weekly (Q-2026-09-14-8)
evidence: docs/reviews/2026-09-14-skilltest/
---

# skilltest

**Verdict:** HARVEST. The static content guard (nothing installed reads a skill for
malice) and the decoy-catalog trigger test (the executed form of the routing check) are
worth taking; the cases, judge, and baseline are redundant to `claude plugin eval`, and
installing a global npm binary with an OpenRouter-only spend cap rules out ADOPT.

**Ancestry:** none.

## What landed

- Rows 2 and 5: rider lines under config-drift-checker decisions row 3 (this commit).
- Rows 1, 3, 4: proposed (guard script, M; W8 description-no-when, S; token estimate on F7, S).

## What was declined, and why

- Cases engine, judge, provider layer, spend cap: `claude plugin eval` provides them
  first-party, and row 3 of the config-drift-checker review already ruled against a bespoke
  provider layer.
- OBSOLETE status: `claude plugin eval --ablation` is the same measurement.
- Cyrillic word boundaries, repeat-lint scoring, format-neutral grading, kebab-case check:
  nothing here consumes them.

## Flags

Deliberate injection fixtures in `test/fixtures/malicious-skill/` and one example input;
quoted in the decisions file, not acted on.

## Re-review trigger

The pin moving with the missing `web/` hub and field reports present, or the guard's
calibration numbers becoming checkable; or config-drift-checker row 3 being unshelved.
