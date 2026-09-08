---
contract: v1
source: https://github.com/Astezelex/oops-i-did-it-again-poc
type: code-repo
pin: 7069bf0d88da6854e3bb0ef3db55ab4178c66001
reviewed: 2026-09-07
verdict: HARVEST
recheck: n/a
applied: none yet; rows proposed to /phase ratify in claude-scout-weekly (Q-2026-09-07-8)
evidence: docs/reviews/2026-09-07-oops-i-did-it-again/
---

# oops-i-did-it-again

**Verdict:** HARVEST. Replay-before-wiring, five evidence-class Bash guards, rule-birth
dating, and the recurrence-escalation rule are worth taking; the installer, the
unconditional hook-writing step, and the every-turn style guard rule out ADOPT.

**Ancestry:** none.

## What landed

nothing yet. Rows 1 to 8 proposed; rows 9 to 12 out.

## What was declined, and why

- install.sh: merges hooks into settings.json by script; this machine wires hooks by a
  ruled runbook with recorded proofs.
- style-guard.py: fires on every Stop event; the em-dash gate is scoped to Artifact publish
  by ruling.
- The skill's Step 3: writes new hook code as an ordinary step with no confirmation gate.
- ShellCheck-on-write as written: passes silently when ShellCheck is absent.

## Flags

disclosed agent-directed content only (AGENTS.md install and read-aloud instructions); see
decisions file.

## Re-review trigger

CI added and the test count reconciled; or the first Stop hook being built here (row 8).
