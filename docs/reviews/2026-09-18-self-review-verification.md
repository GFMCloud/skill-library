---
contract: v1
source: installed verification slot, five items (proof-of-work, evidence-report, smoke-gate, review-pair, pre-delivery-verifier), this library at af9faf7 plus the toolkit-review worktree
type: skill-collection
pin: af9faf7 (library main, 2026-09-18)
reviewed: 2026-09-18
verdict: HARVEST
recheck: none
applied: branch tighten-verification, the commit titled "foundry-core 0.5.0, verification-kit 0.3.0: the five TIGHTEN rows", ruled by Graham 2026-09-18 ("apply the five TIGHTEN rows")
evidence: 2026-09-18-self-review-verification/ (extraction report, both judgments, ledger, usage)
---

# Self-review: the verification slot (toolkit-review, mode `self`, size `spot`)

**Verdict:** every one of the five items earns its place and every one is `TIGHTEN`, both
judges agreeing on the item and the section; the recurring gap is that four of the five
state what evidence is in prose and ship no script that checks it was produced.

**Ancestry:** none; this is the installed set judged against its own bar, no candidate.

**Method:** the first real `toolkit-review` run. One headless Sonnet extraction of the five
items under the clean profile (read-only tools, no settings), passed `check-extract.sh`
on attempt 1 (two plugin names allowed because the sources cite them). Two headless Sonnet
judges read the one report against the bar with `references/self-review-prompt.md`; both
passed `check-judgment.sh` on attempt 1. Ledger by `make-ledger.py`. Spend 388,599 tokens
(extraction 321,361; judges 32,380 and 34,858). The judges saw the run path
`/private/tmp/tr-runs/self-1` and the owner's email block (standing limit).

## What landed

All five rows, each as the mechanism the judges described, each proven red and green:

| Item | Landed as | Proof |
|---|---|---|
| proof-of-work 1.3.0 | `scripts/run-checks.sh` records each phase's command, exit code and output; `ran` only with a captured exit code | `fixtures/run-fixture-proof.sh`: green 0, failing tests 1 with later phases skipped, absent tool 3 |
| evidence-report 1.2.0 | `scripts/check-report.py` validates the four fields, the verdict token, a non-empty OUTPUT on VERIFIED and FAILED, an identifier, the NOT VERIFIED section | `fixtures/report-good.md` passes; `report-bad.md` fails on four counts |
| smoke-gate | Stop hook required and shipped as `scripts/smoke-stop-hook.sh`; settings entry stays a paste | fixture proof steps 6 to 9: red exits 2 with `SMOKE FAIL`, red again released, green silent, missing script named |
| review-pair | `verdict-check.sh` rejects evidence that is a bare quote; spec section 3 tightened | `verdict-fail-bare-quote.FIXTURE.yaml` rejected; the four older fixtures unchanged in outcome |
| pre-delivery-verifier | plugin hook `hooks/readonly-agent-guard.py` denies write-shaped Bash when `agent_type` is a read-only agent | `hooks/prove-guard.sh` 16 cases; live: a real verifier subagent's redirect denied, `guard-live-proof.md` |

## Rows (both judges, same class on all five)

| Item | Class | Criterion | What a tighter version would do (judge S1 / S2, paraphrased) |
|---|---|---|---|
| `foundry-core/skills/proof-of-work` | `TIGHTEN Enforcement` | Enforcement mechanism | Ship a script that confirms the fallback check sequence (build, type, lint, test, secret scan) actually ran and captured exit codes, instead of describing the order in prose. |
| `foundry-core/skills/evidence-report` | `TIGHTEN Enforcement` | Enforcement mechanism | Validate the report shape mechanically: four fields per claim, a verbatim OUTPUT, an identifier, a non-empty NOT VERIFIED list; flag a CHECK/OUTPUT pair with no traceable run. |
| `verification-kit/skills/smoke-gate` | `TIGHTEN Stop-hook` | Enforcement mechanism | The Stop-hook that makes a red result unavoidable is "optional... and not proven by a fixture"; make it mandatory and cover it with the item's own fixture-proof script. |
| `verification-kit/skills/review-pair` | `TIGHTEN Verdict evidence field` | Fit with the bar | Per-issue `evidence` may be "a quote under 15 words" rather than run output, which is why the validator "cannot check that the reviewer actually looked at the change"; require a reference to an executed check. |
| `verification-kit/agents/pre-delivery-verifier` | `TIGHTEN Enforcement` | Enforcement mechanism | The non-modification guarantee is a `disallowedTools` list the item itself calls "a narrowed surface, not a boundary", with a cited heredoc bypass; a hook or sandbox that inspects Bash for write patterns would be the boundary. |

Both steelmans credited the same thing: the set is layered, not duplicative, three of the
five ship fail-closed scripts, and the weak points are self-disclosed in the text. The
`TIGHTEN` on `pre-delivery-verifier` is the same gap the ECC retro's lesson 7 named from
the other direction (read-only agents keep Bash, so redirects write).

## What was declined, and why

Nothing declined; no `RETIRE` or `SPLIT` row.

## Flags

None. No agent-directed text in the five items beyond their own instructions.

## Re-review trigger

After any of the five rows is applied, or when `toolkit-review` reaches `set` size and
this slot is judged beside a candidate.
