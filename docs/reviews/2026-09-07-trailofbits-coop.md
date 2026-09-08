---
contract: v1
source: https://github.com/trailofbits/coop
type: code-repo
pin: cbfe0273ac68585f381bcd9edf22384cac2cefce
reviewed: 2026-09-07
verdict: HARVEST
recheck: n/a
applied: row 2 as a STATE.md annotation in claude-scout-weekly (2026-09-07); other rows proposed to /phase ratify (Q-2026-09-07-7)
evidence: docs/reviews/2026-09-07-trailofbits-coop/
---

# trailofbits-coop

**Verdict:** HARVEST. The tool is the first concrete candidate for the OS-sandbox alternative
that Q-2026-09-03-4 left open, and installing it is Graham's call (Tier 3); the transferable
rows are two runbook sentences, one authoring-standard bullet, a pointer, and a trust-model
pattern for security-sensitive projects.

**Ancestry:** none.

## What landed

- Row 2 (tiered enforcement that reports which tier held): pin attached to the
  Q-2026-09-03-4 row in claude-scout-weekly STATE.md as the worked example for the sandbox
  decision.

## What was declined, and why

- Test-that-the-self-test-can-fail: already the global deliberate-failure rule and
  prove-hooks.sh.
- Self-restrict after startup; permit attached to the response body: sound, no consumer here.

## Flags

disclosed agent-directed content only (AGENTS.md, CLAUDE.md, repo-authored hooks in
.claude/settings.json that run on any agent opening the clone as a working directory); see
decisions file.

## Re-review trigger

Graham naming a week for the OS-sandbox decision (row 1 becomes a phased-harness), or the
VM integration suite moving into CI.
