# Gate A: set-1 (2026-09-18)

One batch. Rows not objected to are ratified as proposed.

Vocabulary: **slot** is one capability being compared; **side** is `installed` or a source
id; **static** evidence is reading only. No bench and no fixture in this run.

## A0. Slot map

| Slot | Installed items | Candidate items | Evidence |
|---|---|---|---|
| security-audit | security-checklist | src4 (cloudflare) security-audit | static |
| diagram | html-diagram | src5 (archify) archify | static |
| overengineering-review | orch-review, review-pair | src1 (ponytail) ponytail-review, ponytail-audit | static |
| evidence | evidence-report, proof-of-work | src2 (OpenResearch) orx-evidence | static |
| experiment-loop | experiment-harness | src2 orx-experiment-tree | static |
| delegation | model-effort-advisor | src2 orx-agent-delegation | static |
| orchestration | sweep-harness, loop-operator agent | src3 (orca) orchestration | static |
| figures | chart-discipline | src2 orx-figures | static |

Recommendation: as built. Items given no slot are listed on the morning page, section 4,
from `mapping/src*.tsv`. Most are bound to the pack's own CLI.

## A1. Calibration result and budget

Calibration slot: security-audit. Both extractions and both judges passed their checkers
on the first attempt. Cost, cache reads included: library-side extraction 40k, candidate
extraction 514k (400k of it cache reads), judges 32k each; slot total about 620k. Spent
so far 2.95M (inventory readers 2.3M, calibration 0.62M). Projection: 7 slots about 2.8M
with escalations and re-dispatch, 7 worth-adopting reviews about 7M on large repos, total
about 13M. Recommendation: ceiling 16,000,000, stop at 80 percent.

## A2. Behavioral layers

None. `auth_candidate_hook_bench` stays absent; no candidate code runs.

## A3. Deferred slots

| What | Why | Default |
|---|---|---|
| ponytail core ruleset, debt ledger, hooks | the counterpart is a section of the global CLAUDE.md, not a library item | reviewed whole in the worth-adopting lane |
| orx-lit-review, orx-paper, orca computer-use | no library counterpart | listed on the page, not reviewed |

## A4. Name lists

As generated: GFMCloud, Graham, incumbent, installed, skill-library; context names are the
ten plugin names.

## A5. Anomalies so far

- The skill's scripts are committed mode 100644; run through `bash`. Fix in the library later.
- The default 2M ceiling was passed by the inventory step alone. Ceiling set at this gate.
- Orchestrator learned one side mapping from checker output; logged in `notes/orchestrator-bias.md`.
- A 429 overnight stops the run; nothing relaunches; the page is still built from what exists.

## Ratified by default

sonnet for extraction and judging, opus for escalation, wave size 4, re-dispatch budget 3,
timeout 1200s.
