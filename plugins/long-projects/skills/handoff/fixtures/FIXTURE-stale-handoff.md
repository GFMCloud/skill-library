FIXTURE: this handoff file is the staleness case for the handoff skill's resume-mode
gate. Every claim holds against the scratch repo built by `setup-fixture-repo.sh`, but
`run-fixtures.sh` touches `b.txt` after `written_at`, so `check-claims.py --project
/tmp/handoff-fixture-repo` must print a STALE notice naming `b.txt` before the
discrepancy table, and still exit 0. Never run this checker against the real
skill-library repo.

# Claude Handoff - FIXTURE stale case
2026-09-11

---

Session Type: technical
Date: 2026-09-11

WHAT HAPPENED
- FIXTURE only: this is not a real session summary.

FIRST MOVE
FIXTURE - no real next step. This file exists only to prove check-claims.py reports
project files that changed after the handoff was written.

## Typed Claims

```yaml
claims: v1
written_at: 2026-09-11T00:00:00-05:00
checkable:
  - type: branch
    claim: work is on the feature-typed-claims branch of the fixture repo
    check: git -C /tmp/handoff-fixture-repo branch --show-current
    expected: feature-typed-claims
  - type: count
    claim: the fixture repo tracks 2 files
    check: git -C /tmp/handoff-fixture-repo ls-files | wc -l | tr -d ' '
    expected: "2"
not_checkable:
  - kind: decision
    text: FIXTURE - this row is unverified by design and must appear in the output as such.
```
