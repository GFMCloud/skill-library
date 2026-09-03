I've read the repository. Here is the review in full.

---

# Standalone review: `config-drift-checker`

## 1. Executive summary

A regression-testing harness for coding-agent *configuration* (CLAUDE.md, skills, hooks), packaged as a Claude Code plugin plus a composite GitHub Action. The core idea is sound and unusually well-specified: turn config expectations into eval cases, run the real agent on a pinned baseline and a canary track, diff score *and* efficiency (turns/cost/duration), and gate spend with a ledger. The code backs the pitch — I verified zero npm dependencies, real self-hosted run data with real cost figures and Actions run URLs, and genuinely careful shell-injection hardening in the Action.

Two things temper it. First, the repository is **one commit, one author, ~7 days of observable history** — every maturity signal a git log would give is absent by construction. Second, and concretely: **42 unit tests exist and are good, but no CI workflow runs them**, while `bump.yml` auto-versions, tags, releases and optionally npm-publishes on every functional push. Tests are claimed, not verified; releases ship through no test gate.

Adoption means a long-lived credential in CI, an unbounded-growth orphan results branch, and an unpinned `npm install -g @anthropic-ai/claude-code@latest` on the canary path.

## 2. Maturity signals

| Signal | Command | Output | Reading |
|---|---|---|---|
| Last commit | `git log --format='%ci %an' \| head -50` | `2026-09-02 20:49:31 +0200 James Komo` | 1 day before review date — active, but see below |
| Commit cadence | `git log --oneline \| wc -l` | `1` | **Single commit.** No cadence is measurable. Squashed export or fresh init; either way the log carries zero history signal |
| Distinct authors, 12mo | same log | `James Komo` (1) | Bus factor 1. Sole author, sole email `james.komoh@gmail.com` (`plugin.json`) |
| Dependency count | `grep -n dependencies config-drift-checker/package.json` | `(none)` | No `dependencies`/`devDependencies` key at all |
| Dependency freshness | `grep -rn "^import .* from '" tools/*.mjs \| grep -v node:` | 5 hits, all relative (`./cdc-config.mjs`, `./eval-report.mjs`) | **Zero-dependency claim verified.** Only `node:` builtins + local modules. CI actions are major-tag pinned (`actions/checkout@v7`, `codeql-action@v4`), not SHA-pinned; Dependabot watches them (`.github/dependabot.yml`, 3 ecosystems) |
| License file | `head -20 LICENSE`, `grep -c '' LICENSE` | `Functional Source License, Version 1.1, ALv2 Future License` / 105 lines | Real 105-line license file, not a badge. **Source-available, not open source** — no competing commercial service; converts to Apache-2.0 two years post-publication |
| Tests exist | `grep -c "test(" test/*.test.mjs` | **42 across 7 files** — exactly the README's number | Verified, and they're behavioral: they drive the shim through a fake `claude` binary and assert on the argv it emits |
| **CI runs them** | `grep -rn "npm test\|node --test" .` | 3 hits: `README.md:103`, `docs/runbook.md:103`, `package.json:13` — **zero in `.github/workflows/`** | **Not verified.** No workflow invokes the suite. CodeQL runs static analysis only; `config-drift-checker.yml` runs the *eval* suite, not the unit tests |
| Release gating | `cat .github/workflows/bump.yml` | Bumps version, tags, `gh release create`, `npm publish` if `NPM_TOKEN` — on every push touching `tools/`, `skills/`, `action/` | Auto-release with **no test step preceding it** |
| Open issues / templates | `find .github -type f` | Only `workflows/` (5) + `dependabot.yml` | No issue templates, no CONTRIBUTING, no CODE_OF_CONDUCT, no CHANGELOG. No volume signal available |
| Real-world run evidence | `cat docs/drift/spend.json`, `ls docs/drift/history` | 3 runs, `$1.3971` spent in 2026-09, live `actions/runs/33658217347` URLs; 10 history reports spanning `20260827T185151Z-cc2.1.247` → `20260902T184000Z-cc2.1.258` | **The system demonstrably runs on itself** across 4 Claude Code versions — over a 7-day window |

**Files I read for the interesting work** (found via entry points in `package.json` `bin` and `action/action.yml`, not the README): `config-drift-checker/tools/eval-shim.mjs` (346 lines, the runner), `tools/eval-diff.mjs` (130, the drift logic), `tools/cdc-gate.mjs` (63, the budget ledger), `tools/cdc-config.mjs` (203, the YAML subset), `tools/safety-net.mjs` (31, the PreToolUse hook), `tools/release-watch.mjs` (72), `action/action.yml` (403, the real deployment surface), `test/eval-shim.test.mjs` + `test/fixtures/fake-claude.mjs`, and all five workflows.

## 3. Claimed vs verified

**Claimed and verified**

- *"Zero npm dependencies"* — verified by import scan and absent manifest keys.
- *"42 tests run against a fake `claude`, so the suite needs no API key"* — 42 is exact. `test/fixtures/fake-claude.mjs` is a real stand-in driven by `FAKE_CLAUDE_COST/FAIL/ERROR/VERSION` env vars; tests assert on the recorded `calls.jsonl`.
- *"a budget you set… your key cannot be drained"* — `cdc-gate.mjs:19-31` implements both gates; `eval-shim.mjs:295-298` aborts mid-suite before starting a run past the cap; `test/eval-shim.test.mjs:97-106` proves the third run never starts.
- *"Pinned baseline, canary on the latest"* — `resolveTrack` + `--track` are real and tested (`eval-shim.test.mjs:61-89`).
- *"not just a number… turns, cost and time per case are diffed too"* — `eval-diff.mjs:58-67`, median-based, with separate thresholds and `fail_on`.
- *"nothing is sent anywhere"* — the only outbound calls in the tools are `npm view` (`release-watch.mjs:63`) and `GET /v1/models` (`:44`). The optional Slack POST goes to a webhook the user supplies.
- Action shell-injection hardening (`action/action.yml:6-7`: *"never through `${{ … }}` inside the script"*) — I grepped every command line in every `run:` body for `${{` and found **no matches**. The claim holds.
- *"Never auto-merged"* — bump/pin/repair all stop at `gh pr create`; the branch-name guard at `action.yml:317` restricts force-pushes to `cdc/*`.

**Claimed, not verified**

- *"CI for your agent setup"* applied to itself: the eval suite runs in CI, but **the unit tests never do**. `docs/runbook.md:103` presents `npm test` as a manual step. Nothing enforces it.
- *"42 tests"* is a count in prose that will silently drift; nothing asserts it.

**Unverifiable from the repo**

- Everything the git log would normally answer — cadence, contributor growth, review practice, issue responsiveness. One commit.
- The linked demo, hosted site, and Marketplace mirror repo (`config-drift-checker-action`) are external; I did not fetch them.

**Inconsistency worth noting:** `LICENSE` self-identifies as `FSL-1.1-ALv2`; `README.md:115` and `plugin.json` say `FSL-1.1-Apache-2.0`. Same license (ALv2 *is* Apache-2.0), two names — harmless but it will confuse license scanners.

## 4. Rubric

**1. Does what it says — 4/5.** Every substantive mechanism in the README exists in the code at roughly the described sophistication, and the published drift data proves it runs end to end. Held back one point because the project's own headline discipline — CI enforcement — is not applied to its own test suite.

**2. Quality of the interesting part — 4/5.** `eval-shim.mjs` is the real work and it is not glue. Mid-suite budget abortion that keeps and scores what already ran (`:295-298`), sequential expansion that buys more runs only on deviation (`:315-318`), `--regrade` that re-scores saved runs with zero agent calls (`:300-303`), provenance stamping so you can tell whether the thing under test moved or the thing testing it did (`eval-diff.mjs:91-94`), and a careful `truncated` vs `isError` distinction (`:262-264`) so max-turns exits aren't miscounted as failures. Deductions: it's a 346-line module of top-level statements with no exports, testable only by subprocess; there are **two separate hand-rolled YAML parsers** with different subsets (`eval-shim.mjs:73-101` for frontmatter, `cdc-config.mjs:30-59` for `.cdc.yml`), which is a divergence waiting to happen.

**3. Adoption cost — 3/5.** Non-trivial. You add: a long-lived credential (`ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`, tied to one person's subscription) as an Actions secret; `contents: write` + `pull-requests: write`; a global `npm install -g @anthropic-ai/claude-code@latest` on the canary path; an orphan `eval-results` branch that accumulates a JSON *and* an HTML report per run forever (`action.yml:268, 283`) with no pruning; and per-run API spend. Removal is straightforward — delete the workflow, the branch, `.cdc.yml` — but note `action.yml:229` writes a *"hosted beta · ⭐ repo"* marketing footer into every consumer's GitHub step summary on every run.

**4. Failure modes — 3/5.** The disclosed ones are handled honestly; the residual ones are real:

- **Budget exhaustion silently stops testing.** Hit `per_month_usd` and the gate returns `run=false`, `gate-exit` exits 0 (`action.yml:401`), and cases with no runs score `null` → `❔ unknown`, explicitly *"not as regressions"*. A busy month therefore masks live regressions behind a green check. Documented (`docs/security.md:36-39`), but it inverts the tool's purpose exactly when you'd want it most.
- **The LLM judge defaults to `haiku`** (`cdc-config.mjs:21`) for nuanced rubrics, and an unparseable verdict silently becomes `pass: false` (`eval-shim.mjs:248-249`). Judge flakiness lands as baseline churn indistinguishable from real drift.
- **`|| true` and `set +e` at several decision points** (`action.yml:162, 168, 194, 351`) — a runner crash can degrade into a mostly-quiet path.
- **`scaffold_script` runs arbitrary bash as the runner user**, and the Action defaults `scaffold: true` (`action.yml:16`). Fine for suites you wrote; the doc says so plainly (`security.md:22-24`).
- **Unpinned harness install with credentials in env** — inherent to canarying `latest`, but it is third-party code executing next to your key.
- **The `repair` feature gives an agent edit + push rights** (`action.yml:357`, `--permission-mode acceptEdits --max-turns 40`). Correctly defaulted to `false` and budget-capped at $2/incident.

Credit where due: `docs/security.md:29-33` discloses a real incident — *"On 2026-08-27 a without-arm run tore down a real Docker stack from a throwaway workspace"* — and the `safety-net.mjs` hook exists because of it. That is more candour than most projects offer.

**5. Originality — 4/5.** There are transferable ideas here independent of the implementation (below).

## 5. Ideas worth taking independently of the code

- **Treat agent configuration as a tested artifact with a pinned/canary split.** `config-drift-checker/ci/config-drift-checker.yml` / `README.md:25-28`: *"**Pinned**: an exact model id and Claude Code version, the baseline every PR is diffed against. **Canary**: the alias your developers actually get, on the latest Claude Code, run on a schedule only when npm or Anthropic's model list moved."* Renovate-for-models is a genuinely underserved gap.

- **Ablation as the measure of what a config element is worth.** `README.md:42-45`: *"the same cases run with and without your plugin. The delta tells you what each skill or hook is actually worth… a conventions skill turned out to add nothing the codebase and CLAUDE.md didn't already carry."* Reporting a *negative* result about the author's own example plugin is the strongest credibility signal in the repo. Any prompt/skill library could adopt this.

- **Efficiency drift as a first-class regression class.** `tools/eval-diff.mjs:58`: `const EFF = [['turns','numTurns','slower'],['cost','costUsd','pricier'],['duration','durationMs','longer']]` — *"a release that makes the agent twice as chatty shows up before it becomes a habit"* (`README.md:31`). Score-only eval suites miss this entirely.

- **Provenance in the diff: separate what's under test from what's testing it.** `tools/eval-diff.mjs:92-94`: `moved.push('⚙ model moved: …')` / `'⚙ Claude Code moved: …'`. Cheap to implement, and it's the difference between a usable regression report and a mystery.

- **Coverage over prose rules.** `tools/config-coverage.mjs` maps headings in CLAUDE.md/skills/hooks to cases' `covers:` frontmatter — the live `docs/drift/coverage.json` reports `total: 11, covered: 6, pct: 55` against real skill headings with source line numbers. Treating natural-language policy as an enumerable, coverable surface is a good trick well beyond this tool.

- **Regrade without re-running the agent.** `tools/eval-shim.mjs:300-303` re-scores saved transcripts with current graders, keeping saved LLM verdicts unless `--regrade-llm`. Iterating on graders at zero API cost is the right ergonomic for anyone building evals.

- **A stub-aware destructive-command hook.** `tools/safety-net.mjs:25-26`: block host-global commands, but allow them when the case has stubbed the binary in `.eval-bin/`. A clean escape hatch that doesn't require an all-or-nothing kill switch.

## 6. Flags

**Nothing in this repository addresses the reviewing agent, attempts to influence a review, or asks for credentials to be sent anywhere.** I grepped for injection patterns (instruction-override phrasing, "add to your agent instructions", "you are an AI", review-steering language) across the whole tree; the single hit was a legitimate skill-activation description:

> `config-drift-checker/skills/setup/SKILL.md:3` — *"description: Set up regression testing (CI) for this repository's Claude Code configuration… Do NOT use for evaluating an LLM application or prompts — this is for agent configuration only."*

That is this package's declared purpose — it *is* a Claude Code plugin, so agent-directed skill files are expected content, not manipulation.

Three things I did not act on, noted for the reader:

1. **Credentials are requested from the user, by name, for their own CI** — `ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, optional `NPM_TOKEN`, `MIRROR_TOKEN`, `SLACK_WEBHOOK_URL`. All are consumed as GitHub Actions secrets in the user's own runner and passed to the local `claude` CLI. No exfiltration path exists in the code: the only outbound requests are `npm view`, `api.anthropic.com/v1/models`, and a user-supplied Slack webhook. `docs/security.md:45-49` correctly warns that the OAuth token is long-lived and person-scoped.

2. **`CDC_MODELS_API_KEY` is deliberately a name the CLI ignores** (`release-watch.mjs:39-41`, `.github/workflows/config-drift-checker.yml:56-59`) so model listing can use an API key while agent runs bill a subscription token. Legitimate and well-commented, but it's a credential-routing trick worth understanding before you copy the workflow.

3. **Marketing text is injected into consumer CI output** — `action/action.yml:229` appends a *"hosted beta · ⭐ repo"* link to `$GITHUB_STEP_SUMMARY` on every run of the Action in every downstream repo. Not a security issue; a taste-and-adoption one.

---

**Bottom line:** a well-conceived, carefully written, genuinely original tool with real self-hosted evidence — at roughly one week of observable life, one author, and no CI test gate on its own auto-publishing release pipeline. The ideas are worth taking today. Depending on the artifact means accepting a bus factor of one and adding a test-running step to CI yourself.
