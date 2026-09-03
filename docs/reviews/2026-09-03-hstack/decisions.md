# Decisions: hstack

contract: v1
source: https://github.com/howardchan2008/hstack
type: code-repo
pin: b1abe1ae2659920d9e2452309e97074628eacfd3 (cloned 2026-09-03T05:55:59Z)
reviewed: 2026-09-03
verdict: HARVEST
recheck: n/a
evidence: docs/reviews/2026-09-03-hstack/cleanroom-review.md, docs/reviews/2026-09-03-hstack/comparison.md

## Verdict reasoning

Installing is out: the installer copies 903 lines of standing rules into
~/.claude/rules (loaded into every session, not removed by uninstall), six hooks are
registered to a `python` that does not exist on macOS with the doctor script masking it,
26 of 37 hooks have no test, and the LICENSE is a truncated MIT text with no grant. The
test methodology and three specific mechanisms are worth taking. What would change the
verdict: a complete license and a test per hook.

## Ancestry

none. One coincidental parallel: both sides wrote Fable 5.1 routing notes the same week.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour | `M` an afternoon, one PR | `L` multi-session.

| # | Item | Class | Proposal | Source | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Negative-control methodology: feed a guard the payload it exists to refuse and a payload it must allow, assert both verdicts | INGESTIBLE FRAGMENT (turns "a check that has never failed a fixture is untested" into a procedure) | Executed this cycle against the one installed hook (see run log); make it standing: a `scripts/prove-hooks.sh` in skill-library that runs both controls for every hook in settings.json, invoked by the Thursday maintainer's Phase 0 beside the validator proof | `tests/negative-control.py`, `docs/TESTING.md:48` | new `~/skill-library/scripts/prove-hooks.sh` plus one line in `claude-improvements-weekly/prompts/phase-0-survey.md` step 5 | S | a script to keep in step with settings.json; a red result when a hook silently dies (the point) | ratified 2026-09-03 (script: next scout Phase 2 in skill-library; the phase-0-survey line is Graham's hand edit) | Graham |
| 2 | dash-gate fragments: codepoint matching instead of a literal (so the hook file cannot self-block), en dash and horizontal bar alongside em dash, an exemption list for `.superseded` and scratch paths | INGESTIBLE FRAGMENT | Rewrite the installed hook's grep into a small script with those three improvements; keep the trigger scoped to Artifact publish unless Graham widens it deliberately | `hooks/dash-gate.sh` | `~/.claude/settings.json` PreToolUse entry plus `~/.claude/hooks/dash-gate.sh` | S | one script; widening scope to Write/Edit is a separate behavior decision | ratified 2026-09-03 (one-session runbook: hooks and permissions; scope stays Artifact publish) | Graham |
| 3 | Mutation-test regexes with a self-tested sweep; detector vs exemption need different test arms | INGESTIBLE FRAGMENT | When row 1's script exists, add a corrupted-regex arm for each hook pattern; record the "dead detector under-blocks, dead exemption over-blocks" distinction in the script header | `tests/dead-branch-sweep.py:1,21,133` | row 1's script | M | none beyond row 1 | ratified with row 1 (second step) | Graham |
| 4 | A checker must not be able to match its own documentation (parse, do not grep prose) | INGESTIBLE FRAGMENT | One paragraph in the validator's header comment and the authoring standard: structural checks parse frontmatter with the YAML loader, never grep for the key name | `tests/parity.py:192-230` | `~/skill-library/scripts/validate-skills.sh` header; `docs/authoring-standard.md` | S | none | ratified 2026-09-03 (next scout Phase 2) | Graham |
| 5 | Config keys that silently drop the whole hooks block (`fallbackModel`, `workflowSizeGuideline` per the author); verify hooks by side effect, not by config state | INGESTIBLE FRAGMENT | Row 1's script is the side-effect check; add the author's key list as a "re-verify against your version" note | `doctor.sh:73` | row 1's script header | S | none | ratified with row 1 | Graham |
| 6 | State a heuristic's ceiling in the file that implements it (backtest table, "sees about a third of what he asks for") | INGESTIBLE FRAGMENT | One sentence in the authoring standard: a skill or check that is a heuristic states its measured ceiling where it is implemented | `hooks/item-coverage.py:213` | `~/skill-library/docs/authoring-standard.md` | S | none | ratified 2026-09-03 (next scout Phase 2) | Graham |
| 7 | Stop hooks for close-out shape, item coverage, and handoff appropriateness | COMPLEMENT | Real gap: prose rules exist (adhd skill, ask-intent memory, "Never ask") with no mechanical enforcement. Needs re-tuning against Graham's own close-out format and turn corpus; phased-harness, not a port | `hooks/item-coverage.py`, `hooks/handoff-gate.py` | new phased-harness project | L | ongoing tuning; false positives block turns until tuned | tabled 2026-09-03 until the close-out format is stable | Graham |
| 8 | 15 rules files installed into ~/.claude/rules, six UserPromptSubmit injectors, burn-context model steering | DISCARD | Contradicts the CLAUDE.md economy rule and the one-editable-home rule | `install.sh:226`, `hooks/burn-context.sh:197` | none | n/a | n/a | out | Graham |

## Conflicts for the user to rule on

- Fail-open guards: hstack guards no-op silently when a helper is missing (documented in
  `ARCHITECTURE.md`); the global rule is "a red validator is a bug in the content". Row 1's
  proof is the answer: a guard that cannot fire is red, never silent. No further ruling.
- "State the goal and the constraints, not the steps" (candidate CLAUDE.md) vs the library's
  runbook style. Different objects (a personal prompt style vs resumable runbooks); no change.

## Corrections at ingest

- Stale counts in README, CHANGELOG, SECURITY.md, ARCHITECTURE.md (word-form numerals miss
  the parity check); do not quote its numbers.
- LICENSE is not a valid MIT grant; nothing is copied verbatim, only techniques, until fixed.
- Style: em dashes throughout; restyle any ingested sentence.

## Flags

Disclosed, not injection: its CLAUDE.md addresses the reading agent (ordinary project
config); `install.sh:226` writes 903 lines of rules into `~/.claude/rules/` and uninstall
leaves them; `burn-context.sh:197` injects model-selection steering each turn. None acted on.

## Rulings log

2026-09-03: proposed by the scout cycle; nothing ratified. Row 1's proof was executed as
verification evidence, not as an applied change.
2026-09-03 ratify: rows 1, 2, 4, 6 ratified as one S-effort session (rows 3 and 5 ride on row 1); row 7 tabled until Graham's close-out format is stable; row 8 out. Recorded in claude-scout-weekly STATE.md as Q-2026-09-03-16.
