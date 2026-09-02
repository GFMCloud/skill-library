---
contract: v1
source: https://x.com/posthog/article/2094485724171223409 ("Your AGENTS.md is holding you back", PostHog / Jina Yoon, 2026-08-31)
type: article
pin: fetched 2026-09-02; sha256 476068f76c43349c57f768c90f8f9804e1c90e7b9f79dce60e9ecc9c809a971f
reviewed: 2026-09-02
verdict: SKIP
recheck: n/a
applied: none
evidence: docs/reviews/2026-09-02-posthog-agents-md/ (cleanroom-review.md, comparison.md, decisions.md, currency-check.md)
---

# posthog-agents-md

**Verdict:** SKIP. Nine techniques; six are covered as well or better by rulings-harness,
the authoring standard, the weekly maintainer and the consolidation harness. The two
sweep-harness fragments proposed (an optional independent grader, an end-of-run
self-report field) address gaps no sweep here has hit, and were ruled out.

**Ancestry:** none. Zero hits for posthog, wizard-ci, context-mill, commandments.yaml or
pr-evaluator in the library or its history.

## Method

One clean-room review at the CLI default model, one Sonnet comparison agent against 9
incumbents plus the authoring standard, the global CLAUDE.md, `claude-md-consolidation`
and `claude-improvements-weekly`. Currency check: the article's /doctor feature list is
stale against the docs fetched 2026-09-02 (current wording: finds unused skills, MCP
servers and plugins versus context cost; trims checked-in CLAUDE.md; reports first and
asks before changing anything; trim check needs v2.1.206, not v2.1.198). Installed: 2.1.258.

## What landed

Nothing.

## What was declined, and why

- Row 1, "if you can't name the failure it prevents, delete it": rulings-harness keeps
  preferences and burn-derived rules without a nameable incident, and a stateless reviewer
  can never name one. The heuristic inverts the burden of proof.
- Rows 2 and 5, failures.md evals: the authoring standard already requires boundary and
  retention sets. Note for Graham: that rule has never fired, the library has zero eval
  cases as of 2026-09-02.
- Row 3, end-of-run self-report field: no consumer, and retro's rule distrusts self-report.
- Row 4, independent grader for sweeps: real gap only for judgment-based done checks; none
  has occurred.
- Row 6, cluster and verify: the weekly maintainer does it against transcripts.
- Row 7, skills-consulted line in commits: no incident behind it (CLAUDE.md economy rule).
- Row 8, delete CLAUDE.md every six months: contradicts one-editable-home with continuous
  verification.
- Row 9, commandments.yaml: ruling.template.md is a strict superset.
- Ruled by Graham 2026-09-02: "skip it all".

## Flags

Agent-directed content quoted inside the article (a merge-queue AGENTS.md line, three SDK
commandments, the wizard's end-of-run prompt) read as data, not acted on. Vendor post: every
internal link carries newsletter UTM parameters. Implementation claims are openable;
efficacy claims are unmeasured. Scrape chrome excluded. No em dashes in the source.

## Re-review trigger

The library's first eval case landing (row 2 becomes testable in practice); or a sweep with
a judgment-based done check (row 4). Not the pin moving.
