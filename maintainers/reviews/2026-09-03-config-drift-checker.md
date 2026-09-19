---
contract: v1
source: https://github.com/jameskomo/config-drift-checker
type: code-repo
pin: df6969cc8ed1fab35aea12ebfa6866a74af8ca63
reviewed: 2026-09-03
verdict: HARVEST
recheck: n/a
applied: none yet; rows ruled 2026-09-03 by /phase ratify in claude-scout-weekly (see decisions.md Rulings log); ratified S rows land in the next scout Phase 2
evidence: docs/reviews/2026-09-03-config-drift-checker/
---

# config-drift-checker

**Verdict:** HARVEST. The ideas (pinned/canary behavioral regression for agent config,
ablation as the measure of a config element's worth, a destructive-command hook, a spend
ledger) are worth taking; the artifact is one author, one week old, source-available, and
auto-releases without a test gate.

**Ancestry:** none.

## What landed

nothing yet. Rows 1 to 5 in the decisions file are proposed.

## What was declined, and why

- Installing the plugin or Action as-is: long-lived credential in CI, unpinned canary
  install, bus factor one, FSL license.
- Porting `eval-shim.mjs`: Anthropic's native `claude plugin eval` covers the runner.

## Flags

none addressed to the reviewer; see decisions file for disclosed credential handling.

## Re-review trigger

A second maintainer, a CI test gate, or a license change; or the pin moving after row 3
is scaffolded.
