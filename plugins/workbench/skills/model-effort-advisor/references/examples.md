# Examples

## Quick Pass Example

**Request:** "Rename these 40 screenshot files to match our naming convention."

**Rubric read:** Reasoning low (mechanical rule application), Creativity low, Risk low (easily reversible, no external exposure), Repetition high (40 near-identical items), Human Oversight low-effective (probably spot-checked, not reviewed file by file).

**Output:**
```
Model: claude-haiku-4-5-20251001
Effort: low
Routing: inline (or a single subagent if it keeps the parent's context cleaner), not worth a full fan-out for a mechanical batch rename
Why: mechanical, well-defined, low-risk, high-repetition, exactly Haiku's lane.
```

## Deep Planning Example

**Request:** "Break down the IAM Identity Center rollout across the partner/marketplace org into a build plan."

**Rubric read:** This is a multi-task project with real architecture decisions (permission sets, group structure, account governance), customer/partner-facing consequences if misconfigured, and a mix of mechanical and judgment-heavy steps.

**Output:**
```
## Task Breakdown

| Task | Model | Effort | Routing | Why |
|---|---|---|---|---|
| Design permission set / group structure | Opus | high | inline | High risk (access control), real architectural tradeoffs |
| Draft IaC (CloudFormation) for the approved structure | Sonnet | medium | inline | Mechanical once the design is approved, moderate risk |
| Write rollout comms to partner/marketplace org | Sonnet | medium | inline, use graham-voice | Drafting task, reviewed before sending |
| Audit existing accounts against new structure (40+ accounts) | Haiku | low | subagent fan-out, ~5 agents | High repetition, mechanical check per account |
| Final review of full rollout plan before execution | Opus | high | inline, build/review pairing recommended | High risk, irreversible once permissions go live |

## Human Review Checkpoints
- Before the permission set / group structure is finalized, this is the one decision everything downstream depends on.
- Before any IaC actually applies changes to a live AWS account.

## Notes
The audit task can run in parallel with the IaC draft since neither blocks the other; both need the structure design finished first.
```
