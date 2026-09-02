# Decisions: buzzoni-loop-engineering

contract: v1
source: https://x.com/polydao/article/2083061585858158636 ("Claude Loop Engineering: How to Build an Agent That Works While You Sleep", Mr. Buzzoni, published 2026-07-31)
type: article
pin: fetched 2026-09-02 (saved X page, /Users/gfm/Downloads/page-2026-09-02-22-36-51.md); sha256 12d990e57c9738a9759a58a51d5172fab1930033089cf4c63ef313b24ee8c5ed
reviewed: 2026-09-02
verdict: SKIP
recheck: n/a
evidence: cleanroom-buzzoni.md (CLI default model, --setting-sources "", read-only tools), comparison-buzzoni.md (Sonnet subagent, 13 incumbents plus the authoring standard, the global CLAUDE.md and the live weekly maintainer), currency-check.md

## Verdict reasoning

Fourteen techniques; ten are already rules in the global CLAUDE.md or a harness skill, usually with a stricter evidence bar and a named incident behind them. Three fragments fill real gaps confirmed by grep against the target files: a concrete UI-verification example (deploy-verify-fix has no UI row), a "no model at all" zeroth question (the decision rubric only ever asks which tier), and an acceptance-rate metric (the weekly maintainer already counts applied and reverted and never divides them). Roughly 7% of the article's claims are evidenced; no number is imported. What would change the verdict: nothing upward. If Graham declines all three rows it becomes SKIP.

## Ancestry

none. No mention of the article or author in the library, the weekly maintainer, or the global CLAUDE.md; git log clean in both directions. Convergent practice: the incumbents trace to the 2026-08-09 skill-migration run and a 2026-08-12 near-miss, the article to Karpathy, Osmani, Rajasekaran and Stripe.

## Fact-currency check

All product-surface claims a row could name were checked against docs fetched 2026-09-02 and the installed Claude Code 2.1.258 binary: /goal (evaluator is a Stop hook on the small fast model, calls no tools, judges only what surfaced; 4,000-char limit; cap stated in the condition as "or stop after N turns"), /loop (1-minute minimum, session-scoped, 7-day expiry, loop.md), cloud routines (1-hour minimum, fresh clone), desktop tasks, CLAUDE_CODE_DISABLE_CRON=1, isolation: worktree. All CONFIRMED. Detail in currency-check.md. None of the rows below names a product command, so none is currency-sensitive.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour, one sitting | `M` an afternoon, one PR | `L` multi-session; L always goes through `phased-harness`.

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Concrete UI-change verification (open the page, exercise the control, before/after screenshot, console shows zero new errors) | INGESTIBLE FRAGMENT | Add one "UI change" block to the verification table, in scope/action/exception/verification shape; no Core Web Vitals step (no consumer here) | buzzoni-loop-engineering.md 271-285 | plugins/deploy-ops/skills/deploy-verify-fix/SKILL.md, "Not verification / Verification" table | S | Four lines in an always-loaded incubator skill; deploy-ops version bump; back out by reverting the commit | proposed (ratified by default) | this session |
| 2 | Program-checkable goal conditions | REDUNDANT | phased-harness fit test ("testable by inspection at any moment") and sweep-harness WORKER done check already require it | 297-306 | n/a | | | out | |
| 3 | Cap the goal in the command ("stop after 5 tries") | REDUNDANT | deploy-verify-fix's information-based stop rule (three cycles, last one produced no new information) is stronger than a flat count | 298 | n/a | | | out | |
| 4 | Six-step build order | REDUNDANT | every harness skill opens with fit test, interview, scaffold, gate; the weekly maintainer was built in this order with four cycles of evidence | 422-432 | n/a | | | out | |
| 5 | Fire a named skill from the schedule, never pasted instructions | REDUNDANT | global one-editable-home rule. Testing the claim found a partial live instance: the weekly scheduled task's prompt lacks the same-day rule; see Flags | 424 | n/a (outside library) | | | out; chip raised for Graham | |
| 6 | Copyable STATE.md shape | REDUNDANT | phased-harness STATE.template.md adds decision log, evidence and owned open items | 435-449 | n/a | | | out | |
| 7 | STATE.md plus VISION.md | REDUNDANT | docs/end-state.md is mandatory in phased-harness and is the tiebreaker | 453 | n/a | | | out | |
| 8 | isolation: worktree; cheap builder, strict reviewer | REDUNDANT | sweep-harness disjoint targets; subagent-routing.md build/review pairing (reviewer never sees the builder's rationale) | 455 | n/a | | | out | |
| 9 | Four-condition go/no-go filter | REDUNDANT | every harness fit test, and each routes the declined case somewhere | 401-407 | n/a | | | out | |
| 10 | Evaluator acts, does not read | REDUNDANT | proof-of-work, three dated incidents | 383 | n/a | | | out | |
| 11 | Security scanning inside the gate | REDUNDANT | global secret-scan-before-commit rule; practiced live (S-32). SAST and dependency audit not named anywhere; too far from current CI shape for a row | 603 | n/a | | | out | |
| 12 | Cost per accepted change: acceptance rate = applied / (applied + reverted) | COMPLEMENT | (a) one trigger line in the rubric's "Diagnosing a skill or prompt that underperforms": a falling acceptance rate on a recurring loop is a reason to run the diagnostic; (b) one line per cycle in the weekly maintainer's Phase 3 report and STATE last-run block. The article's 50% threshold is invented and is not imported | 643-645 | (a) plugins/workbench/skills/model-effort-advisor/references/decision-rubric.md; (b) ~/work/claude-improvements-weekly/prompts/phase-3-report.md (outside the library, Tier 3 there, Graham-only) | S | (a) one bullet in a reference file; (b) a new field the report template must carry every cycle; back out by removing the line | proposed; (b) is Question 1 | this session for (a); Graham for (b) |
| 13 | Choose the runtime from the task's physics (local vs cloud) | REDUNDANT | capability-preflight; the durable kernel is "probe before assuming", already stated | 515-517 | n/a | | | out | |
| 14 | Deterministic work stays deterministic: ask whether a step needs a model at all before asking which model | COMPLEMENT | New first check before "The Five Axes": if a rule, lookup, search or fixed transform can decide the step, write it as code or a shell step and route no model to it; the rubric applies to what remains. Verification: the step's output is reproducible byte-for-byte across two runs | 537-543 | plugins/workbench/skills/model-effort-advisor/references/decision-rubric.md | S | Five to eight lines in a reference file loaded on every routing decision; workbench version bump; back out by reverting the commit | proposed (ratified by default) | this session |

## Conflicts for the user to rule on

Question 1 (row 12b): add an acceptance-rate line to the weekly maintainer's Phase 3 report and STATE last-run block? It edits `prompts/phase-3-report.md`, which that project's CLAUDE.md reserves for Graham. Recommendation: yes; the counts already exist every cycle and the division is free. Alternative: library line only (row 12a), which then names a metric nothing computes.

No philosophy conflict found. The gate-proven-by-deliberate-failure rule is an omission in the article, not a disagreement, and the article's own flagship "everything stacked" example carries no cap, which standing-authorization's validate step would reject.

## Corrections at ingest

- No number from the article is imported: 700 experiments, 19%, 8M views, 1,300 PRs/week, the 17,022-skill audit, the 50% survival threshold, all pricing.
- "The evaluator runs nothing itself" is a documented limitation of /goal, not doctrine; the library's verifiers must act (proof-of-work, pre-delivery-verifier). Not imported.
- Every landed fragment is reshaped as scope, action, exception, verification. No mannered prose ("earns its place", "you are the number"). Zero em dashes in the source.

## Flags

- Nothing addressed to a reviewing agent. Skill and command examples are tutorial content for the reader (cleanroom Flags A to E); not acted on.
- Promotional close: consulting rates, a Telegram funnel, a "$95k to $300k" line. Ignored.
- Live finding while testing row 5 (not from the article): `~/.claude/scheduled-tasks/claude-improvements-weekly/SKILL.md` hand-restates the no-argument dispatch and lacks the same-day rule ruled 2026-08-28. `publish` and `ratify` are correctly absent (Graham-only). Raised as chip task_d32231df; the subagent's original chip overstated it and was withdrawn.
- Scrape chrome (trending, DraftKings, live news, engagement counters) excluded.

## Rulings log

- 2026-09-02, proposed by this session. Awaiting the batch ruling on Question 1; rows 1, 12a and 14 ratified by default unless objected to.
- 2026-09-02, Graham, batch ruling: "skip it all". Rows 1, 12a, 12b and 14 out; Question 1 answered no. Source verdict changed from HARVEST to SKIP. Reason given: narrow harvest not worth the maintenance surface; the pipeline had never yet returned SKIP. No side effects to reassign: none of the proposals carried cleanup or retirement steps. The scheduled-task chip (task_d32231df) stands independently of this ruling.
