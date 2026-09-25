FIXTURE: this handoff file is a deliberately poisoned fixture for the handoff skill's
resume-mode gate. One of its checks is write-shaped (an `rm` of a file in the scratch
repo built by `setup-fixture-repo.sh`). Run `check-claims.py` against this file after
running the setup script - it must exit 1 with that row marked `refused`, and
`/tmp/handoff-fixture-repo/b.txt` must still exist afterwards, which proves the command
was never run. Never run this checker against the real skill-library repo.

# Claude Handoff - FIXTURE refused case
2026-09-24

---

Session Type: technical
Date: 2026-09-24

WHAT HAPPENED
- FIXTURE only: this is not a real session summary.

FIRST MOVE
FIXTURE - no real next step. This file exists only to prove check-claims.py refuses a
write-shaped check instead of running it.

## Typed Claims

```yaml
claims: v1
written_at: 2026-09-11T00:00:00-05:00
checkable:
  - type: branch
    claim: work is on the feature-typed-claims branch of the fixture repo
    check: git -C /tmp/handoff-fixture-repo branch --show-current
    expected: feature-typed-claims
  - type: file
    claim: FIXTURE - a write-shaped check that must be refused, never run
    check: rm -f /tmp/handoff-fixture-repo/b.txt; echo gone
    expected: gone
not_checkable:
  - kind: decision
    text: FIXTURE - this row is unverified by design and must appear in the output as such.
```
