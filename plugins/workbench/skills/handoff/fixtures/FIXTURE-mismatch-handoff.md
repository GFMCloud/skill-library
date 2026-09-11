FIXTURE: this handoff file is a deliberately poisoned fixture for the handoff skill's
resume-mode gate. It names the wrong branch for the scratch repo built by
`setup-fixture-repo.sh`. Run `check-claims.py` against this file after running the setup
script - it must exit 1. Never run this checker against the real skill-library repo.

# Claude Handoff - FIXTURE mismatch case
2026-09-11

---

Session Type: technical
Date: 2026-09-11

WHAT HAPPENED
- FIXTURE only: this is not a real session summary.

FIRST MOVE
FIXTURE - no real next step. This file exists only to prove check-claims.py fails
correctly on a wrong claim.

## Typed Claims

```yaml
claims: v1
written_at: 2026-09-11T00:00:00-05:00
checkable:
  - type: branch
    claim: work is on the main branch of the fixture repo
    check: git -C /tmp/handoff-fixture-repo branch --show-current
    expected: main
  - type: count
    claim: the fixture repo tracks 2 files
    check: git -C /tmp/handoff-fixture-repo ls-files | wc -l | tr -d ' '
    expected: "2"
not_checkable:
  - kind: decision
    text: FIXTURE - this row is unverified by design and must appear in the output as such.
```
