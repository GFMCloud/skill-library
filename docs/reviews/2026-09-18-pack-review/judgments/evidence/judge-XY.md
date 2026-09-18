## Steelman X

X offers two complementary skills that together cover the full lifecycle of evidence: item-7aed43c3 forces actual execution of checks (build/types/lint/tests/secrets/diff) via a script that captures real exit codes per phase and refuses to let a phase be marked "passed" without a captured exit code — even catching a tampered summary line. item-92c76be2 then forces the write-up into a fixed, machine-checkable shape (CLAIM/CHECK/OUTPUT/VERDICT plus a mandatory NOT VERIFIED section) with a validator script that fails closed on missing fields. Both ship fixture-proofs of their own scripts' correctness, and both are candid about their own limits (heuristic identifier check, can't detect a fabricated OUTPUT paired with a check that never ran). This is a rare case of a toolkit that separates "run it" from "report it" and hardens each half with an actual script rather than prose.

## Steelman Y

Y's single skill targets a specific, high-value failure mode: inferring a training/run result from memory, status, or scattered/truncated log output instead of the actual persisted log. It gives concrete, actionable CLI instructions (`orx logs --tail/--head/--bytes/--range`) and a checklist of what must be present before a claim is accepted (variant/config, final metrics, summary, recoverable trajectory, non-truncated window). Its two hard rules — "Never infer a result from run status or memory" and "Truncated output is not evidence of absence" — are exactly the kind of concrete stop conditions the bar wants, and it also shapes the run command itself (print config, print periodic metrics) so evidence exists to read in the first place, not just after the fact.

## Scores

| Criterion | X | Y |
|---|---|---|
| Fit with the bar | 3 — neither item blocks planning; item-7aed43c3 is "strongly supported and central" on executed evidence, and item-92c76be2 makes the not-verified list mandatory, directly reinforcing behavior 3 (report cites "An omitted not-verified list reads as 'everything was checked'"). | 3 — nothing in the item conflicts with planning or stopping; it strongly reinforces behavior 2 ("Never infer a result from run status or memory") and partially behavior 3, per the report. |
| Enforcement mechanism | 3 — both items ship executable scripts (`check-report.py`, `run-checks.sh`) with fixture-proofs; run-checks.sh "marks a phase 'ran' only if an exit code was actually captured" and includes a tamper test, per the report. | 0 — the report states explicitly: "Prose only — no executable checker, hook, or script is included in this file. Nothing blocks, warns, or exits non-zero." |
| Context cost | 1 — two skills, each loaded on demand ("Not always on"), but together they carry two scripts, dependencies (bash, python3, node, npm, gh) and more surface area than a single item. | 2 — a single skill, loaded on demand, with one CLI dependency (`orx`) and a shorter, focused instruction set, but it defers undefined content (the "evidence-and-links contract") that the reader could not assess. |
| Maintenance burden | 2 — dependencies are python3 (item-92c76be2) and bash/python3/node/npm/gh (item-7aed43c3); report flags an unresolved question of where "gh" is actually used, and states these are otherwise runtime-free scripts. | 1 — depends on the external `orx` CLI and an undefined "session playbook," both presented as already present but neither's install/availability is verified in the report; report lists this among things it "could not determine." |
| Specificity | 3 — concrete phase list (build/types/lint/tests/secrets/diff), explicit verdict-token vocabulary, explicit tamper/failure-mode handling ("cannot tell whether a CHECK was run, only that its OUTPUT is empty"). | 3 — concrete checklist (variant/config, final metric, summary, trajectory, byte window) and concrete stop conditions ("Never infer a result from run status or memory," "Truncated output is not evidence of absence"). |

## Per-item rows

| Item | Class | Note |
|---|---|---|
| item-92c76be2 | COMPLEMENT | Fills a gap in Y's set: a checkable, fixed-field report format with a mandatory not-checked section and a validator script enforcing it — Y has no analogous formatting enforcement, only a deferred external "evidence-and-links contract." |
| item-7aed43c3 | SUPERSEDES item-b9504c3e | Both make an agent produce and trust only executed evidence rather than self-reported success or memory, but item-7aed43c3 backs this with an executable script that captures real exit codes, marks phases not-run/skipped correctly, and is itself fixture-proofed, while item-b9504c3e's equivalent guidance ("Never infer a result from run status or memory") is prose only with no enforcement mechanism, per the report. |
| item-b9504c3e | SUPERSEDED BY item-7aed43c3 | Its core evidence-discipline content overlaps with item-7aed43c3's but with weaker enforcement (prose only, no script/hook); its concrete log-reading instructions (`orx logs --tail/--head/--bytes/--range`, printing config/summary in the run command) are a narrower, tool-specific skill not present in X, but this is FRAGMENT-worthy detail rather than a reason to keep the whole item. |

## Deciding criteria

Enforcement mechanism and Specificity settled the rows: X's items back their instructions with executable, fixture-proofed scripts that verify their own claims, while Y's item is prose-only despite comparably concrete checklists.

## What I could not assess from reading alone

Whether either script (`check-report.py`, `run-checks.sh`) or the `orx logs` workflow is actually invoked automatically in practice versus skipped by an agent — a behavioral run would need to show a real agent completing a task and either running these tools unprompted or being blocked from declaring "done" without them. I also could not verify the `orx` CLI's real behavior or the referenced "session playbook" contract, nor whether X's "gh" dependency is genuinely exercised. I don't believe I can identify the origin of either candidate.
