# Decisions: handoff-vs-handoff-skill

contract: v1
classes: rubric v2 mapped to v1 (see make-ledger.py)
source: src1 at 8990d64805fe340c9e79f59db5a93da273559dc6
reviewed: 2026-09-18
verdict: HARVEST

## Rows

| # | Slot | Item | Source path | Class (v1, per judge) | Class (v2, per judge) | Ruling |
|---|---|---|---|---|---|---|
| 1 | handoff | item-5fc81ea9 | /private/tmp/tr-runs/spot-1/candidates/src1/commands/pickup.md | REDUNDANT / REDUNDANT | REDUNDANT item-57dd6a97; REDUNDANT item-57dd6a97 | out |
| 2 | handoff | item-c238a6db | /private/tmp/tr-runs/spot-1/candidates/src1/skills/session-handoff | INGESTIBLE FRAGMENT / INGESTIBLE FRAGMENT | FRAGMENT -> item-57dd6a97; FRAGMENT -> item-57dd6a97 | ratified |
| 3 | handoff | item-e0eb292d | /private/tmp/tr-runs/spot-1/candidates/src1/commands/handoff.md | REDUNDANT / REDUNDANT | REDUNDANT item-57dd6a97; REDUNDANT item-57dd6a97 | out |

## Rulings log

- 2026-09-18, Graham: "apply the fragment, merge and push it". Row 2 ratified and applied (handoff 0.5.0); rows 1 and 3 out (redundant with the installed skill's triggers). No override, no side effect reassigned.
