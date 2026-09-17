# Gate B rulings

Ruled by Graham on 2026-09-17 on `gate-b/package.md` and the row-by-row walk-through that followed it:
"yes to all as recommended, plus B20, continue". Before that, in the same exchange: the landing label stays
`maturity: incubator` ("I'm good with the initially proposed state since it's just a label and not a path").
No push, PR or merge was authorized; the branch stays local and unpushed.

| Row | Ruling | Side effect and owner |
|---|---|---|
| B1 `skills/tdd-workflow/` | Land as FRAGMENT EDITS only (untrusted-plan checklist, "do not invent PASS results" language) into the installed loop skill the judges pair it with; not a new skill | Phase 6 |
| B2 `skills/eval-harness/` | Land as a new incubator skill in `foundry-core` | Phase 6 |
| B3 `skills/delivery-gate/` | NOT landed as a skill (its directory holds `quality-gate.py`, ECC runtime code). Moved to the hook-gate lane as H3: plan-gate output only | Phase 6 writes `hook-gate/H3-delivery-gate.md`; patch stays in the workspace as reference-only |
| B4 `agents/tdd-guide.md` | Left out | Patch row stays in the workspace as reference-only; owner Graham, no action |
| B5 `agents/silent-failure-hunter.md` | Land as a new agent in `verification-kit` | Phase 6 |
| B6 `skills/security-review/` | Land as a new incubator skill in `verification-kit`, CONDITION: every action-phrased row (rotate secrets, enable MFA and the like) sits behind an explicit stop-and-confirm gate | Phase 6 |
| B7 `agents/loop-operator.md`, B8 `agents/harness-optimizer.md` | Land as new agents in `workbench`; references to scripts that are absent are stated or dropped | Phase 6 |
| B9 `skills/orch-pipeline/` | Land as a new incubator skill in `workbench` | Phase 6 |
| B10 to B14 the five `orch-*` wrapper skills | Left out | Reference-only in the workspace; owner Graham; revisit only if B9 earns its place |
| B15 `commands/orch-review.md`, B16 `skills/council/`, B17 `skills/santa-method/` | Land as new incubator skills in `workbench` | Phase 6 |
| B18 `agents/planner.md` | FRAGMENT EDIT into `plan-gate` (`turn-reduction`): red-flags plan self-check and a worked example; the agent itself is not landed | Phase 6 |
| B19 `skills/verification-loop/` | FRAGMENT EDIT into `proof-of-work` (`foundry-core`): the concrete command checklist for the code artifact class; the "continuous mode" cadence fragment is EXCLUDED | Phase 6 |
| B20 `agents/code-reviewer.md` (added at the gate) | FRAGMENT EDIT into `review-pair` (`verification-kit`): the four-question pre-report gate and the Node/React false-positive list; the agent itself is not landed | Phase 6 |
| H1 `memory`, H2 `hooks-runtime` | Approved: plan-gate output only, nothing installed | Phase 6 writes `hook-gate/H1-memory.md`, `hook-gate/H2-hooks-runtime.md` |
| `gates-pre-work` | No verdict accepted; later pass after the name rule and the rubric's SUPERIOR SUBSTITUTE wording are fixed | Owner Graham, `STATE.md` Open items |
