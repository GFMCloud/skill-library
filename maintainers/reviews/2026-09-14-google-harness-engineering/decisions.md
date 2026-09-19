# Decisions: google-harness-engineering

contract: v1
source: https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/
type: article
pin: fetched 2026-09-14T23:30:18Z, sha256 in pin.txt
reviewed: 2026-09-14
verdict: HARVEST
recheck: n/a
evidence: docs/reviews/2026-09-14-google-harness-engineering/cleanroom-review.md, docs/reviews/2026-09-14-google-harness-engineering/comparison.md

## Verdict reasoning

The article (Google for Developers, 2026-09-09, two named engineers; surfaced by two
independent scanners) carries no data: the clean room scored evidence 1 of 5 and found its
"fast, deterministic, under 5 seconds" framing contradicted by its own live-model example.
Its one durable contribution is two constraints and two seed ideas for the skill
regression harness this library tabled on 2026-09-03 (config-drift-checker row 3), which
`claude plugin eval` (Claude Code 2.1.269) now gives a first-party runner. Nothing here is
worth building on its own; the rows are riders on that tabled item so its eventual design
does not repeat the article's self-tuning-loop mistake. What would change the verdict:
nothing toward ADOPT; a version of the article with a measured before and after would
raise the seed rows from "attach" to "adopt as cases".

## Ancestry

none. Independent arrival on ground the library surveyed and shelved (config-drift-checker
decisions row 3, 2026-09-03).

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour | `M` an afternoon, one PR | `L` multi-session (phased-harness).
Adoption cost is mandatory and never "none".

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Two standing constraints for the tabled skill eval harness: never tune a prompt or skill against the suite that gates it (the article's self-tuning loop violates experiment-harness's frozen-holdout rule and the global bounded-loop rule), and every behavioral case carries a negative control (the article's only example asserts a tool call happened and never shows the check failing) | INGESTIBLE FRAGMENT (constraints, not code) | Two rider lines under config-drift-checker decisions row 3, so the harness design inherits them when row 3 is unshelved | article lines 87 and 114; comparison.md "Philosophy conflicts" and "Corrections needed at ingest" | `docs/reviews/2026-09-03-config-drift-checker/decisions.md` row 3 (a pointer) | S | two more lines to read before scaffolding row 3; nothing to back out | proposed (a review-record cross-reference; applied 2026-09-14 as Tier 1, see rulings log) | scout |
| 2 | Seed the harness's first cases from observed failures ("pick one failure mode ... find a single, obvious action that slipped, and make that your target") and match assertion strictness to how open-ended the task is (strict single-turn milestone for one-solution tasks; outcome checks with an independently validated judge for open-ended ones) | COMPLEMENT (nothing installed turns an observed misbehavior into a persisted, re-runnable case; the consumer is row 3, tabled) | Attach as design input to Q-2026-09-14-1 (first eval suite on `claude plugin eval`): the three seed cases come from the retro or hooks incident lists, not from the article's examples | article lines 87 to 122; comparison.md items 2 and 3 | none today (rides Q-2026-09-14-1 and config-drift-checker row 3) | S | none until row 3 exists; then the judge-validation step is a cost per case | proposed | Graham |
| 3 | Assert on intermediate execution steps rather than final strings | REDUNDANT (proof-of-work "verify at the level the failure lives", SKILL.md 47-48, backed by three dated incidents) | none | article line 87 | none | n/a | n/a | out | scout |
| 4 | Gate on aggregate pass rates over batches, not single runs | REDUNDANT as a principle (experiment-harness run template 33-38 requires paired per-item wins and a stated sample size, a stricter form); the batch mechanism itself is row 3's gap | none | article line 122 | none | n/a | n/a | out | scout |
| 5 | Illustrative seed behaviors and the self-tuning prompt loop | DISCARD (the loop conflicts with two installed rules; the examples are prompts, not a method) | none; row 1 forbids the loop explicitly | article lines 63 to 65, 114 | none | n/a | n/a | out | scout |

## Conflicts for the user to rule on

- Self-tuning loop: the article proposes "a loop where an LLM tweaks its own system prompt,
  iterating until a failing test finally passes"; experiment-harness's CLAUDE template says
  "Do not fit, tune, or adjust anything against the holdout after it is frozen", and the
  global rule says fix loops run under /goal with bounded-loop and an attempt budget.
  Proposal: row 1 records the prohibition on the tabled harness. Alternative: none
  recommended.

## Corrections at ingest

- "Fast, deterministic, under 5 seconds" is false of the article's own example (a live model
  call with web search); no fragment carries that framing.
- "Trending correctly" has no threshold a stateless model could check; any ingested form
  states a sample size and a delta, per experiment-harness's run template.
- An LLM judge counts as evidence only after it is checked against human labels (the clean
  room's "unvalidated judge" risk becomes a requirement in row 2).

## Flags

none. The article is written for human readers; its code samples are examples for a human
to run in their own project, and nothing was run.

## Rulings log

2026-09-14: proposed by the scout cycle (cycle 3). Row 1 applied the same day as Tier 1 (a
cross-reference between two review records, no library behavior changed); row 2 attached to
Q-2026-09-14-1 for Graham's ruling. Recorded in claude-scout-weekly STATE.md as
Q-2026-09-14-9.
