FIXTURE: this handoff file is the offset case for the handoff skill's resume-mode gate.
Its `written_at` carries the UTC offset without a colon (`-0500`, what `date +%z`
prints), which YAML leaves as a string and which Python 3.9's `fromisoformat` rejects.
`check-claims.py --project /tmp/handoff-fixture-repo` must still judge staleness from
`written_at` (the label names it, parsed as `-05:00`) and never fall back to the
handoff file's mtime, and must exit 0. Never run this checker against the real
skill-library repo.

# Claude Handoff - FIXTURE offset case
2026-09-11

---

Session Type: technical
Date: 2026-09-11

WHAT HAPPENED
- FIXTURE only: this is not a real session summary.

FIRST MOVE
FIXTURE - no real next step. This file exists only to prove check-claims.py reads a
`written_at` whose offset has no colon.

## Typed Claims

```yaml
claims: v1
written_at: 2026-09-11T00:00:00-0500
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
