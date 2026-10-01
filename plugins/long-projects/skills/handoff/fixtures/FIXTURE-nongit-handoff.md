FIXTURE: this handoff file is the non-git project case for the handoff skill's resume-mode
gate. Its `--project` is a plain folder with no `.git`, built by `run-fixtures.sh` under
`/tmp/handoff-fixture-nongit` with one file older than `written_at` and one touched after,
so `check-claims.py` must still print a STALE notice (labelled "not a git repo, mtime
walk") naming `after.txt` and not `before.txt`, and exit 0. Its second claim is a read-only
`git merge-base --is-ancestor` check against the scratch repo, which the write-shape guard
must let run (it was refused as `merge` before 0.6.3). Never run this checker against the
real skill-library repo.

# Claude Handoff - FIXTURE non-git project case
2026-09-11

---

Session Type: technical
Date: 2026-09-11

WHAT HAPPENED
- FIXTURE only: this is not a real session summary.

FIRST MOVE
FIXTURE - no real next step. This file exists only to prove check-claims.py reports
staleness for a project folder that is not a git repo, and runs a read-only merge-base check.

## Typed Claims

```yaml
claims: v1
written_at: 2026-09-11T00:00:00-05:00
checkable:
  - type: branch
    claim: work is on the feature-typed-claims branch of the fixture repo
    check: git -C /tmp/handoff-fixture-repo branch --show-current
    expected: feature-typed-claims
  - type: status
    claim: HEAD of the fixture repo is its own ancestor (a read-only merge-base check)
    check: git -C /tmp/handoff-fixture-repo merge-base --is-ancestor HEAD HEAD && echo ancestor
    expected: ancestor
not_checkable:
  - kind: decision
    text: FIXTURE - this row is unverified by design and must appear in the output as such.
```
