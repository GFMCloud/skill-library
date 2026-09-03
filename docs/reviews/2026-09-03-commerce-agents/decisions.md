# Decisions: commerce-agents (Anthropic blueprint and companion article)

contract: v1
source: https://github.com/anthropics/commerce-agents and https://claude.com/blog/the-anatomy-of-effective-commerce-agents
type: code-repo (plus article)
pin: fd4d59224ab96b43c6dc6888207c67b3bd5a24cf (cloned 2026-09-03T05:56:06Z); article fetched 2026-09-03T05:56:07Z sha256 2c9b3d7d68b18445...
reviewed: 2026-09-03
verdict: HARVEST
recheck: n/a
evidence: docs/reviews/2026-09-03-commerce-agents/cleanroom-review-repo.md, cleanroom-review-article.md, comparison.md

## Verdict reasoning

Nobody here is building a commerce agent, so ADOPT is off the table. The general
principles are the deliverable: a cost-per-completed-task metric, the scoping of when
subagents pay off, harness-enforced provenance gates, snapshot evals, and a
consistency-checker pattern. Every README count verified; Apache-2.0; but one commit,
one author, and "not maintained": a fork-and-own template. What would change the
verdict: a product-agent build on this machine, which would make rows 5 and 6 live.

## Ancestry

none. Convergent design on both sides (evidence-first verification, gate-not-prompt
enforcement) with no shared history.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour | `M` an afternoon, one PR | `L` multi-session.

| # | Item | Class | Proposal | Source | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Cost per completed task, not per call, as the model-selection metric | INGESTIBLE FRAGMENT | One sentence: "Measure cost per completed task rather than per model call, since a cheaper model that needs more turns, or fails more often, is not cheaper." | article, "Model selection" | `plugins/workbench/skills/model-effort-advisor/references/effort-sizing.md` | S | one line to keep current; no runtime | ratified 2026-09-03 (next scout Phase 2) | Graham |
| 2 | Scope the subagent fan-out rule to session orchestration | COMPLEMENT (resolves a letter-level conflict) | Add to the global Concurrency section: fan-out applies to independent research or mechanical chunks reassembled by an orchestrator; for a live conversational agent every handoff is state-lossy (several times the tokens, seconds of latency) and subagents earn their place only for narrow self-contained tasks | article, "Architecture"; comparison "Philosophy conflicts" | `~/.claude/CLAUDE.md`, Concurrency section (one sentence) | S | one more sentence in the always-loaded file | ratified 2026-09-03 (global CLAUDE.md is Graham's hand edit; exact sentence in the ratify hand-edits note) | Graham |
| 3 | Repo-consistency checker as a CI gate | SUPERIOR SUBSTITUTE (vs the manual load-bearing-claim sweep) | A `scripts/check.py` for skill-library: counts and claims in README, inventory, and CHANGELOG verified against the tree on every push; automates the "rewriting a load-bearing claim triggers a sweep" rule | `scripts/check.py` | new `~/skill-library/scripts/check-claims.py` plus a CI step | M | a script to maintain; a red check when prose drifts (which is the point) | ratified 2026-09-03 as a one-session runbook | Graham |
| 4 | Snapshot evals, real failures as cases, 50 to 100 per flow, gate on pass rate over a few trials plus cost per turn | COMPLEMENT | Rides on the skill-eval harness proposed in the config-drift-checker decisions (row 3 there); record here as the case-design guidance for it | article, "Evals" | folded into `2026-09-03-config-drift-checker/decisions.md` row 3 | S (once that exists) | none beyond that harness | tabled with config-drift-checker row 3 | Graham |
| 5 | Held is not error: a refusal that names the recovery call; provenance as a hard write gate; fence labels as source literals; log a digest of the session id; cache-prefix discipline | INGESTIBLE FRAGMENTS (for a future product-agent build) | Keep as a references note in this proposals directory; ingest into a product-agent skill when one is scaffolded | `gates.py:29,40`, `fencing.py:4`, `turn.py:110`, `prompt_assembly.py:29-33` | none today | L (only when a build exists) | none until consumed | out (no consumer on this machine) | Graham |
| 6 | Memory as typed facts extracted by a separate process that reads only user and assistant text, with a validator at the write path | COMPLEMENT | No consumer: Claude Code's own memory is not this project's to redesign. Note for the Thursday maintainer's memory hygiene: "never tool results" is a good rule for what gets remembered | article, "Memory" | none | M | none until consumed | out | Graham |
| 7 | Placement rule: a third of traffic goes in the system prompt, the rest in skills | COMPLEMENT | Different object than the CLAUDE.md economy rule (a narrow single-purpose agent with a measurable traffic mix vs a general global file). No change | article, "Prompt/skill placement" | none | S | n/a | out (rules govern different objects) | Graham |
| 8 | CI tripwire for dependency confusion on unregistered internal package names | COMPLEMENT | No unpublished internal packages here; note only | `.github/workflows/ci.yml` | none | S | n/a | out | Graham |

## Conflicts for the user to rule on

- Subagent fan-out (row 2): letter-level contradiction between "a single agent with skills
  consistently has outperformed ... the subagent design" and the Concurrency section's
  fan-out pattern. Resolved by scope: the article speaks of routing a live conversation
  mid-turn; the rule speaks of asynchronous orchestration of independent chunks. Proposal
  is the scoping sentence, not a reversal. Alternative: leave the rule as is and record
  the scope in Settled ground.
- Outcome grading vs proof-of-work: the article's "grade the outcome, not the path"
  weights the trade-off opposite to proof-of-work's "verify at the level the failure
  lives". The article partly concedes (gate on pass rate over trials plus cost per turn).
  No change proposed; the eval harness (row 4) should grade outcome AND record path cost.

## Corrections at ingest

- Article prose uses em dashes and product-marketing register; restyle any ingested line.
- The repo's own CLAUDE.md is project configuration for that repo, not guidance for this
  library; not ingested.

## Flags

None addressed to the reviewing agent. Injection strings present in the repo are
adversarial test fixtures, correctly used. No credentials requested.

## Rulings log

2026-09-03: proposed by the scout cycle; nothing ratified.
2026-09-03 ratify: rows 1 and 2 ratified now, row 3 as a one-session runbook; row 4 tabled with the eval harness; rows 5 to 8 out. Q-2026-09-03-9 closed as superseded by this table. Recorded in claude-scout-weekly STATE.md as Q-2026-09-03-17.
