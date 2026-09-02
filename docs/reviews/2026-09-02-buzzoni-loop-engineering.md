---
contract: v1
source: https://x.com/polydao/article/2083061585858158636 ("Claude Loop Engineering: How to Build an Agent That Works While You Sleep", Mr. Buzzoni, 2026-07-31)
type: article
pin: fetched 2026-09-02; sha256 12d990e57c9738a9759a58a51d5172fab1930033089cf4c63ef313b24ee8c5ed
reviewed: 2026-09-02
verdict: SKIP
recheck: n/a
applied: none
evidence: docs/reviews/2026-09-02-buzzoni-loop-engineering/ (cleanroom-review.md, comparison.md, decisions.md, currency-check.md)
---

# buzzoni-loop-engineering

**Verdict:** SKIP. Fourteen techniques; ten are already rules in the global CLAUDE.md or a
harness skill with a named incident behind them, and the three fragments the comparison
proposed (a UI-verification table row, a "does this step need a model at all" rubric
question, an acceptance-rate metric) were ruled not worth the maintenance surface. About 7%
of the article's claims are evidenced; no number was imported.

**Ancestry:** none. Convergent practice; no reference to the article or author anywhere in
the library, the weekly maintainer, or git history.

## Method

One clean-room review at the CLI default model (`claude -p --setting-sources ""`, read-only
tools, article rubric), one Sonnet comparison agent against 13 incumbents plus the authoring
standard, the global CLAUDE.md and the live `claude-improvements-weekly` loop. Product
claims a row could name were checked against the docs and the installed Claude Code 2.1.258
binary: /goal, /loop, cloud routines, desktop tasks, `CLAUDE_CODE_DISABLE_CRON`,
`isolation: worktree`, all confirmed as of 2026-09-02.

## What landed

Nothing.

## What was declined, and why

- Rows 2 to 11 and 13 (REDUNDANT): program-checkable conditions, goal caps (the
  information-based stop rule in deploy-verify-fix is stronger than a flat count), build
  order, named-skill-from-schedule, STATE.md shape, STATE plus VISION (end-state.md is
  mandatory), worktree isolation and asymmetric models, the go/no-go filter, evaluator acts,
  security in the gate, runtime physics. Each already in the global CLAUDE.md or a harness
  skill.
- Row 1 (INGESTIBLE FRAGMENT, UI verification): the global rule already says load the page
  and click the flow; the row added console and screenshot steps to a table. Cosmetic.
- Row 12 (COMPLEMENT, cost per accepted change): the weekly maintainer already reports
  applied and reverted counts side by side; naming the ratio changes no decision.
- Row 14 (COMPLEMENT, no model at all): the one row that would have changed routing
  behavior. Ruled out with the rest; the strongest candidate if this source is ever
  revisited.
- Ruled by Graham 2026-09-02: "skip it all", on the ground that a narrow harvest is not
  worth the maintenance surface and the pipeline had returned HARVEST on every prior run.

## Flags

Nothing addressed to a reviewing agent; skill and command examples are tutorial content.
The closing third is promotional (consulting rates, a Telegram funnel). Scrape chrome
excluded. Side finding while testing row 5, not from the article: the weekly maintainer's
scheduled-task prompt at `~/.claude/scheduled-tasks/claude-improvements-weekly/SKILL.md`
lacks the same-day rule ruled 2026-08-28 (`publish` and `ratify` are correctly absent);
raised as a chip for Graham, not acted on.

## Re-review trigger

The library gaining a routing step where "no model at all" would have been the right call
and was missed (row 14); or a sweep whose done check is a judgment rather than an exit
code. Not the pin moving: the article's durable content is its architecture, which is
already here.
