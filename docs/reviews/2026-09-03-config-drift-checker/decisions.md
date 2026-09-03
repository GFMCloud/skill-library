# Decisions: config-drift-checker

contract: v1
source: https://github.com/jameskomo/config-drift-checker
type: code-repo
pin: df6969cc8ed1fab35aea12ebfa6866a74af8ca63 (cloned 2026-09-03T05:55:54Z)
reviewed: 2026-09-03
verdict: HARVEST
recheck: n/a
evidence: docs/reviews/2026-09-03-config-drift-checker/cleanroom-review.md, docs/reviews/2026-09-03-config-drift-checker/comparison.md

## Verdict reasoning

The artifact is one week old, one author, Functional Source License (not open source),
auto-publishes releases with no test gate, and adoption puts a long-lived credential
into CI with an unpinned canary install. The ideas are the deliverable: nothing on this
machine proves a skill or rule still produces the intended behavior after a Claude
Code or model change; the library only proves structure. What would change the
verdict to ADOPT: a second maintainer, a CI test gate, and an Apache or MIT license.

## Ancestry

none. Independent invention of adjacent territory; no shared strings, no merge notes.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour | `M` an afternoon, one PR | `L` multi-session (phased-harness).
Adoption cost is mandatory and never "none".

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Stub-aware destructive-command PreToolUse hook | SUPERIOR SUBSTITUTE (vs the prose rule "enforce it at the tool layer") | Port the blocklist as a global PreToolUse Bash hook; drop the `.eval-bin` escape hatch; re-derive the pattern set from commands actually run here (AWS, Route 53, git history rewrites); prove it by deliberate failure before trusting it | `tools/safety-net.mjs:25-26` | `~/.claude/settings.json` hooks entry plus a hook script; pointer sentence in global CLAUDE.md "Boundaries" | S | one more process before every Bash call; a wrong pattern blocks legitimate work until edited; removal is deleting the hook entry | ratified 2026-09-03 (one-session runbook: hooks and permissions; deliberate-failure proof before trust) | Graham |
| 2 | Budget and interval gate ledger for subagent fan-outs | COMPLEMENT | Add a per-cycle USD cap and a spend ledger to both weekly maintainers: check before spend, append after spend, force only on manual invocation. The cap value is a fact only Graham can supply | `tools/cdc-gate.mjs:19-31`, `tools/eval-shim.mjs:295-298` | `claude-improvements-weekly/CONFIG.md` and `claude-scout-weekly/CONFIG.md` (harness edits, Graham's) | M | a ledger file per project; a cycle that hits the cap stops early and must say so as a non-green state, never exit 0 (the candidate's own default is the wrong one) | ratified 2026-09-03 (cap USD 25 per cycle per maintainer; one-session runbook; CONFIG edits are Graham's) | Graham |
| 3 | Pinned/canary behavioral regression harness for skills and rules, with ablation, efficiency drift, provenance tags, and regrade riding on it | COMPLEMENT | New incubator capability in foundry-core consuming `claude plugin eval` cases rather than porting the bespoke 346-line shim; reports through evidence-report conventions; "budget exhausted" renders as a distinct non-green state | `README.md:25-45`, `tools/eval-diff.mjs:58,91-94`, `tools/config-coverage.mjs`, `tools/eval-shim.mjs:300-318` | new `plugins/foundry-core/skills/skill-eval-harness/` (name TBD at scaffold) | L | API spend per run; a baseline store; case-writing for the first skills; ongoing maintenance of graders | tabled 2026-09-03 (phased-harness when a week is available; not scaffolded yet) | Graham |
| 4 | Ablation as the measure of a config element's worth | INGESTIBLE FRAGMENT (rides on row 3) | One paragraph in the skill authoring standard: a skill earns its place by a measured delta, not by existing | `README.md:42-45` | `~/skill-library/docs/authoring-standard.md` | S | none beyond row 3 existing to measure it; until then it is a stated intent | tabled with row 3 | Graham |
| 5 | Coverage over prose rules (map rule headings to eval cases) | INGESTIBLE FRAGMENT (rides on row 3) | Part of row 3's case format: each case names the rule heading it covers, so uncovered rules are enumerable | `tools/config-coverage.mjs`, `docs/drift/coverage.json` | row 3 | S | none beyond row 3 | tabled with row 3 | Graham |

## Conflicts for the user to rule on

- Budget-skipped runs: the candidate exits 0 and marks cases "unknown, not regressions" when the
  monthly cap is hit (`action.yml:401`, `docs/security.md:36-39`). The installed
  pre-delivery-verifier doctrine is that UNVERIFIED never renders as passing. Proposal: any
  port renders cap-hit as a distinct non-green state. Alternative: none recommended.

## Corrections at ingest

- No CI step runs the candidate's 42 unit tests; any port must add one before trusting them.
- Two hand-rolled YAML parsers with different subsets; do not port either, use a real parser.
- The Action writes a marketing footer into every consumer's step summary; strip on port.
- Style: candidate prose uses em dashes; restyle on ingest.

## Flags

None addressed to the reviewing agent. Credentials are requested by name for the user's own
CI (`ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, optional `NPM_TOKEN`, `MIRROR_TOKEN`,
`SLACK_WEBHOOK_URL`); no exfiltration path found by the clean-room reviewer. `scaffold_script`
runs arbitrary bash as the runner user, default on.

## Rulings log

2026-09-03: proposed by the scout cycle; nothing ratified. Tier 2 is off; every row is
Tier 3 by class anyway (settings.json, harness config, effort L).
2026-09-03 ratify: rows 1 and 2 ratified (row 2 cap set at USD 25 per cycle per maintainer, ledger required, cap-hit is non-green). Row 3 tabled, with rows 4 and 5, until there is a week for a phased-harness. Recorded in claude-scout-weekly STATE.md as Q-2026-09-03-15.
