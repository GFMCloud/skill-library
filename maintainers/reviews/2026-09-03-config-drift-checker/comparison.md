# Stage 3 comparison: config-drift-checker vs. the installed set

Candidate pinned at `df6969cc8ed1fab35aea12ebfa6866a74af8ca63`, single commit, author James Komo,
remote `https://github.com/jameskomo/config-drift-checker`.

## Ancestry

**No shared history.** Checked for: merge notes naming either side, byte-identical or
near-identical files, matching section structure, CHANGELOG cross-references, shared strings.

- `git log --format='%H %ci %an %s'` on the candidate shows one commit only:
  `df6969c 2026-09-02 20:49:31 +0200 James Komo Auto-merge Dependabot patch/minor updates once
  every check is green [skip ci]`. No prior history to share.
- `grep -rl "skill-library|gfmcloud|Graham|foundry-core|consistency-checker|verification-kit"`
  across the whole candidate tree (md/json/mjs/yml) returns **zero hits**.
- The candidate's own `docs/architecture.md`/README credit only its own prior art (Anthropic's
  `claude plugin eval` format, Renovate for the pinned/canary metaphor) — no reference to this
  machine's skill library, its authors, or its conventions.
- Independent authorship is otherwise corroborated: single author (`james.komoh@gmail.com`),
  distinct license (FSL-1.1), distinct repo (`jameskomo/config-drift-checker`), distinct domain
  (agent-configuration regression testing vs. this machine's skill-authoring/verification stack).

This is two independent inventions of adjacent territory, not a fork in either direction. Every
classification below is "does the incumbent already cover this" — not "what did the fork learn."

## Spot-checks on the clean-room review

The review is unusually careful (it cites line numbers and quotes verbatim); I re-ran or re-read
the load-bearing claims rather than trusting the write-up:

| Claim | My check | Result |
|---|---|---|
| Single commit, one author | `git log --format='%H %ci %an %s'` | Confirmed: one commit, James Komo |
| Zero npm dependencies | Read `config-drift-checker/package.json` in full | Confirmed: no `dependencies`/`devDependencies` key |
| 42 tests, exact count | `grep -c "test(" test/*.test.mjs` summed | Confirmed: 5+4+8+8+5+3+9 = **42** |
| Unit tests never run in CI | `grep -rn "npm test\|node --test" .` across the whole tree | Confirmed: 3 hits (`README.md`, `docs/runbook.md`, `package.json` script def) — **zero** inside `.github/workflows/**` |
| `bump.yml` auto-releases with no test gate | Read `.github/workflows/bump.yml` in full | Confirmed: triggers on push to `tools/`, `skills/`, `.claude-plugin/`, `ci/`, `action/`; bumps version, tags, `gh release create`, conditionally `npm publish` — no step anywhere runs the test suite first |
| Budget-skip exits green (not a documented "unverified") | Read `action/action.yml` `gate-exit` step | Confirmed: `if [ "$SKIPPED" = "true" ]; then echo "skipped ($SKIP_REASON) — not a failure"; exit 0; fi` |
| License name inconsistency (`FSL-1.1-ALv2` vs `FSL-1.1-Apache-2.0`) | Grepped `LICENSE`, `plugin.json`, `README.md` | Confirmed: `LICENSE:5` says `FSL-1.1-ALv2`; `plugin.json:12` and `README.md:115` say `FSL-1.1-Apache-2.0` |
| Shell-injection hardening claim | Read `action/action.yml` in full, grepped every `run:` block for `${{` | Confirmed: the file's own header comment states the rule and every `run:` body reads inputs through `env:` + quoted `"$VAR"`; no `${{ }}` interpolation found inside a script body |

Every claim I checked held. I found one thing the review did not surface in its Section 5 list
(the budget/interval gate, `cdc-gate.mjs`) that is worth classifying on its own — see below.

## Classification of every idea in clean-room Section 5, plus one it missed

### 1. Pinned/canary track split ("Renovate for models")

> `README.md:25-28` — *"**Pinned**: an exact model id and Claude Code version, the baseline every
> PR is diffed against. **Canary**: the alias your developers actually get, on the latest Claude
> Code, run on a schedule only when npm or Anthropic's model list moved."*

**COMPLEMENT.** No incumbent runs the actual agent against a pinned model/harness version and
diffs behavior when a new release ships. `scripts/validate-skills.sh` and
`scripts/generate-inventory.sh` check skill *structure* (frontmatter fields, body length, broken
links, name/dir match, staleness by calendar date) — never agent *behavior*, and never against a
tracked model or Claude Code version. `claude-improvements-weekly` is the closest thing on this
machine to "does our config still work," but its method is git-diff and session-transcript mining
on a weekly cadence, not running eval cases before/after a version change:

> `claude-improvements-weekly/prompts/phase-0-survey.md:33-37` — *"Repo change sweep... Read the
> diffs of any global CLAUDE.md change and any skill body change. Look for: rules restated in more
> than one place, load-bearing claims that changed without a sweep, version fields not bumped
> alongside body edits."*

That is prose-diffing, not behavior-testing. The gap is real and exactly the kind of thing
`claude-improvements-weekly` would consume — it already watches for "did Claude Code ship a new
version" implicitly (session dates), but has no mechanism to *prove* a skill still fires and
behaves the same way after such a release.

### 2. Ablation as the measure of what a config element is worth

> `README.md:42-45` — *"the same cases run with and without your plugin. The delta tells you what
> each skill or hook is actually worth… a conventions skill turned out to add nothing the codebase
> and CLAUDE.md didn't already carry."*

**COMPLEMENT.** Nothing in the incumbent set measures whether a skill changes agent behavior at
all. `validate-skills.sh` cannot: it never invokes an agent, only parses frontmatter and markdown
structure. `proof-of-work` states the doctrine ("run the thing... against representative data")
but has no with/without protocol for isolating one component's contribution. This is a genuinely
underserved gap on this machine, given the skill library currently holds dozens of `incubator`
skills with no behavioral evidence that any given one earns its context-window cost versus base
CLAUDE.md instructions.

### 3. Efficiency drift as a first-class regression class (turns/cost/duration)

> `tools/eval-diff.mjs:58` — `const EFF = [['turns','numTurns','slower'],['cost','costUsd','pricier'],['duration','durationMs','longer']];`

**COMPLEMENT**, tightly coupled to idea 1 — it only exists because idea 1's harness produces
repeated, comparable runs to diff. No incumbent tracks agent chattiness/cost/latency as a
regression signal; `proof-of-work` and `pre-delivery-verifier` both stop at pass/fail correctness.
Not independently adoptable without also adopting (or building) the run-and-compare harness idea 1
describes.

### 4. Provenance in the diff — separate what's under test from what's testing it

> `tools/eval-diff.mjs:92-94` — `moved.push('⚙ model moved: …')` / `'⚙ Claude Code moved: …'`

**COMPLEMENT**, and the most philosophically resonant of the seven with something already on this
machine — but not redundant with it. `consistency-checker:spec-artifact-diff` teaches the adjacent
but distinct lesson that a check's *scope* can exclude the place a defect lives:

> `spec-artifact-diff/SKILL.md:120-121` — *"When writing a check, state what it would fail to
> detect. If that answer is 'the thing I am checking for,' the check is decoration."*

That is about whether a check can *see* a defect. The candidate's provenance idea is about a
different failure: two runs can differ because the artifact under test changed **or** because the
instrument measuring it changed (model alias resolved differently, Claude Code shipped a new
version) — and a diff that doesn't separate those two causes reports "regression" when the truth
is "our ruler moved." Nothing in `spec-artifact-diff`, `proof-of-work`, or the weekly maintainer's
survey addresses this. It is directly applicable: `claude-improvements-weekly`'s session-mining
survey has exactly this exposure today — if Graham's corrections between one Thursday and the next
look different, the maintainer currently has no way to tell "the skill drifted" from "Claude Code
itself changed under me," because it never stamps or diffs the harness version session-to-session.

### 5. Coverage over prose rules

> `tools/config-coverage.mjs` docstring — *"Rules are the bullets in CLAUDE.md and every skill's
> SKILL.md (outside code fences)... A case claims rules with `covers: [id, …]`."* Live output:
> `docs/drift/coverage.json` → `{"total": 11, "covered": 6, "pct": 55}` against real skill headings
> with source line numbers.

**COMPLEMENT.** `validate-skills.sh` checks that a skill file has the right *shape* (F1-F11: name
present, description ≥40 chars, name matches directory, body ≤500 lines, no broken links, valid
maturity, stable skills carry semver + reviewed date, deprecated skills name a supersedes target).
None of that asks whether any individual instruction inside the body has ever been exercised by
anything. `config-coverage.mjs`'s trick — slugging every bullet into a stable id, and requiring a
test to claim it by id — is a mechanism the skill library has no equivalent of at any layer:
neither the validator, nor `proof-of-work`, nor `spec-artifact-diff` (which checks a document
against ground truth, not "has this rule ever been tested at all"). A natural consumer would be an
extension to `validate-skills.sh` or a new incubator skill, once eval cases for skills exist to
count as coverage.

### 6. Regrade without re-running the agent

> `tools/eval-shim.mjs:300-303` — `--regrade` re-scores a saved `aggregate-result.json` against
> current graders with zero agent calls, keeping saved LLM verdicts unless `--regrade-llm`.

**COMPLEMENT**, but a corollary of idea 1 rather than a standalone adoptable piece — it only makes
sense once something is saving replayable agent transcripts to re-score, which nothing on this
machine currently does. Filed here for completeness per the task's instruction to classify every
Section 5 item, but it should not be counted separately in a net-effort estimate; it ships free
with idea 1 if idea 1 is ever built.

### 7. Stub-aware destructive-command hook

> `tools/safety-net.mjs` header — *"Blocks commands with host-global side effects that a throwaway
> workspace cannot contain. A case that must exercise such a command creates a stub binary in
> `<workspace>/.eval-bin/<name>`... when a stub exists for the command's binary, the net allows
> it."*

**SUPERIOR SUBSTITUTE** for a principle the global config states but does not itself implement as
a working artifact:

> `~/.claude/CLAUDE.md`, "Boundaries are declared and enforced" — *"Pre-declared boundaries held;
> undeclared ones drifted. Name the boundary before the work starts, and enforce it at the tool
> layer where possible: a rule in prose can be reasoned around, a tool the agent does not have
> cannot."*

`safety-net.mjs` is exactly this rule made concrete and runnable: a PreToolUse Bash hook with a
7-rule blocklist (`docker compose down -v`, `docker system/volume/container/image prune`,
`git push --force/--delete`, recursive `rm` outside the workspace, destructive SQL, `kubectl
delete`/`terraform destroy|apply`/cloud deletes, `systemctl stop|disable|restart`/`pkill`), plus a
disciplined escape hatch (a stub binary in `.eval-bin/`) so a legitimate test case isn't blocked
outright. None of the incumbents ship a comparable generic tool-layer enforcement artifact for this
exact class of destructive command — the global rule is stated in prose and left to each project to
implement itself.

**What would need editing before it could generalize:** strip the `.eval-bin` stub escape hatch (or
keep it, generalized to a configurable allowlist directory) since it is eval-workspace-specific;
remove the eval-only framing in the header comment; decide install scope (a project's
`.claude/settings.json` PreToolUse hook vs. a global one in `~/.claude/settings.json`); and verify
the regex rules against this machine's actual near-miss set (e.g., add whatever specific
destructive command classes matter here — AWS/Route 53 zone deletion, `npm publish`, git history
rewrites) since the candidate's list is generic to its own use case (Docker/K8s/Terraform/SQL/git).

### 8. Missed mechanism: the budget/interval gate ledger

Not listed in clean-room Section 5 (it appears only in the review's "claimed and verified" table),
but worth flagging on its own:

> `tools/cdc-gate.mjs:9-10` header — *"the two things that keep a BYOK key from being drained: a
> monthly budget ledger and a minimum interval between scheduled canaries."* Implementation:
> `decide()` refuses to start a run once `spend.months[month].usd >= track.budget.per_month_usd`,
> and separately throttles scheduled (not manual) runs to `min_interval_hours`; a manual
> `workflow_dispatch --force` is the only bypass, "the person clicking the button is the budget."

**COMPLEMENT.** Nothing in the incumbent set enforces a hard USD ceiling on autonomous or
scheduled agent spend. `claude-improvements-weekly/CONFIG.md` grants `auth_subagents: yes` for
"Sonnet subagent fan-outs on disjoint file subtrees" with no dollar cap anywhere in its authority
table, and the global CLAUDE.md's concurrency section talks about model-choice discipline
(`model-effort-advisor`) but not a spend ledger with a hard stop. Given `claude-improvements-weekly`
is an **unattended, Thursday-scheduled** run that already fans out multiple Sonnet subagents, this
is the most directly relevant of the eight ideas to that specific project: a scheduled, unattended
job with no one watching is exactly the failure mode `cdc-gate.mjs` was built to prevent (a "busy
week" draining a key with nobody noticing until the bill arrives).

## Routing collisions

If `config-drift-checker`'s plugin were installed alongside the skill library:

- **`run`** — the candidate ships a skill literally named `run`
  (`config-drift-checker/skills/run/SKILL.md`, invoked as `/config-drift-checker:run`, triggered by
  natural-language phrases about running the eval suite). This machine already has a **top-level,
  unscoped** skill named `run`: *"Launch and drive this project's app to see a change working. Use
  when asked to run, start, or screenshot the app, or to confirm a change works in the real app."*
  Slash-command form is namespaced (`/config-drift-checker:run` vs `/run`) so there is no literal
  name clash, but natural-language routing is genuinely ambiguous: a user saying "run the tests" or
  "run this and check it" in a repo that has both plugins installed could trigger either skill, and
  the two do materially different things (one launches the app for a visual check, the other spends
  API budget running an agent eval suite).
- **`setup`** — soft collision, not a hard one. `config-drift-checker:setup`'s description ("Set up
  regression testing (CI) for this repository's Claude Code configuration... Use when the user says
  'set up config-drift-checker'... 'wire the eval GitHub Action'") overlaps in surface form with
  `workbench:project-setup-wizard` ("Helps set up new Claude Projects from rough ideas") and
  `anthropic-skills:setup-cowork`. The candidate's description is specific enough (names itself,
  names CI/evals) that a router should disambiguate correctly in practice, but "set up X" is a
  generic enough trigger phrase that it is worth watching if this is ever actually installed.
- **`write-case`** and **`repair`** — no collision found against the current inventory.
- **Plugin/marketplace name** — `config-drift-checker` as a plugin name does not collide with any
  installed plugin (`foundry-core`, `consistency-checker`, `verification-kit`, `workbench`, etc.).

## Philosophy conflicts (contradictory, not just differently emphasized)

**Converting "we didn't check" into a green result.** This is a direct contradiction, not a
difference of emphasis:

- Candidate, `action/action.yml` `gate-exit` step (verified above): when the budget or interval
  gate skips a run, `exit 0` — *"skipped (\$SKIP_REASON) — not a failure."* The eval-diff report
  correspondingly renders unrun cases as `❔ unknown` and the design is explicit that this must
  *not* read as a regression:
  `tools/eval-shim.mjs` log line — *"cases without runs score as unknown, not as regressions."*
  The net effect: a CI check can go green in a month with no budget left, having tested nothing.
- Installed doctrine, `verification-kit:pre-delivery-verifier`, on the three legal verdicts:
  *"**UNVERIFIED** — no check ran, or the check could not reach the failure mode. This is a
  legitimate and expected verdict. 'Looks fine,' 'should work,' and 'no issues found on review' are
  not verdicts and must never appear."* And `foundry-core:proof-of-work`: *"Where evidence cannot be
  produced, say so, in those words, and put it in the not-verified list. Do not substitute
  reasoning about why it probably works."*

The candidate's own `docs/security.md` is honest about this exact failure mode (*"it inverts the
tool's purpose exactly when you'd want it most,"* per the clean-room review) — so the authors know
it's a real cost, but the *shipped default* is still "budget exhausted = green check," which is the
inverse of what this machine's verification doctrine treats as a hard rule: an unverified claim
must render as unverified, never as passing. Anyone adopting the harness idea (1) onto this machine
should flip that default — a budget-skipped run should render as a distinct, non-green CI state
(e.g. `neutral`/`skipped` on GitHub, not the same green tick as "all cases passed") rather than
`exit 0` indistinguishable from success.

No other contradiction rose to this level. Everywhere else the two sides differ in what they cover
(agent-behavior regression vs. document/skill-structure verification), not in what they'd tell you
to do about the same situation.

## Corrections needed at ingest

- **Style: em dashes.** The candidate's prose (README, docs, SKILL.md files, code comments) uses em
  dashes throughout (e.g. `README.md:1` — *"CI for your agent setup. · [site] ·..."*; `tools/*.mjs`
  header comments). The global rule: *"No em dashes in any written content you produce or edit."*
  Any lifted fragment (safety-net.mjs comments, coverage-tool docstring, README quotes used as
  skill documentation) needs a pass to remove them before landing in a skill body.
- **Style: body-length ceiling.** `validate-skills.sh` fails a skill (`F7`) whose body exceeds 500
  lines. None of the candidate's four SKILL.md files are close to that on their own, but if the
  whole `setup`/`repair` procedural detail were folded into one skill body rather than split with a
  `references/` directory, it would need splitting to pass F7.
- **Factual/versioned claims that will drift.** The review already flags *"'42 tests' is a count in
  prose that will silently drift; nothing asserts it"* — the same trap this machine's own rules name
  explicitly (*"Rewriting a load-bearing claim triggers a repo-wide sweep... A claim restated in
  four places goes stale in three of them"*). Any ingested fragment that quotes a specific count
  (42 tests, `total: 11, covered: 6, pct: 55` coverage numbers, `$1.3971` spend) is describing the
  candidate's own repo at one point in time and must not be copied as if it were a fact about this
  machine.
- **A stateless model cannot honor "two attempts, then revert."** `skills/repair/SKILL.md` step 5:
  *"Up to two attempts. If the second is not green, revert your edits... and write a summary."*
  This requires the executing session to remember it already tried once, which holds within a
  single agent run (as here) but would not survive being split across a `phased-harness`-style
  multi-session resume without an explicit attempt-counter written to disk — worth noting if
  `repair`'s procedure is ever lifted into this machine's phased-harness pattern.
- **License mismatch is real but harmless to fix on ingest**: if any candidate text is quoted
  verbatim into a skill-library file, attribute it and do not restate the license claim — the
  candidate itself doesn't agree with itself on `FSL-1.1-ALv2` vs `FSL-1.1-Apache-2.0` (confirmed
  above).
- **No CI test gate on the candidate's own release pipeline** is not something to "correct" on
  ingest (this machine wouldn't be adopting the candidate's CI), but it's a reason to treat this
  specific candidate as low-trust for anything beyond the ideas themselves — don't `npm install` or
  `plugin install` this artifact wholesale; port the specific mechanisms named above as prose/code
  fragments into skill-library's own reviewed, tested surface.

## Net assessment

If only three things could be taken:

1. **`safety-net.mjs`'s destructive-command blocklist, as a fragment** (idea 7, SUPERIOR
   SUBSTITUTE). It is the single most directly portable artifact in the repo: a working, generic
   PreToolUse Bash-hook implementation of a principle the global CLAUDE.md currently only states in
   prose ("Boundaries are declared and enforced"). Target: a new hook file plus a pointer from
   `~/.claude/CLAUDE.md`'s "Boundaries are declared and enforced" section, or a `settings.json`
   hooks entry via the `update-config` skill. Strip the `.eval-bin` escape hatch, keep or replace it
   with a generic allowlist mechanism, and validate the regex set against this machine's actual
   near-misses (AWS, Route 53, git history rewrites) rather than the candidate's Docker/K8s/SQL set.
   **Effort: S** — it is close to drop-in; the main work is deciding install scope and re-testing
   the blocklist against real commands actually run on this machine (per the global rule, "a gate or
   validator is trusted only after being proven by deliberate failure" — this hook has never been
   fired here, so it needs at least one deliberate-failure proof before being trusted).

2. **The budget/interval gate pattern (idea 8, COMPLEMENT), as a fragment**, folded into
   `claude-improvements-weekly`'s guardrails. Target: `claude-improvements-weekly/CONFIG.md`'s
   authority-tiers/standing-authorizations tables, adding a spend ledger and a hard per-cycle or
   per-month USD cap for subagent fan-outs, modeled on `cdc-gate.mjs`'s `decide()`/`record()` split
   (check-before-spend, append-after-spend, force-only-on-manual-invocation). **Effort: M** — needs
   a small ledger file convention (`STATE.md` extension or a new `spend.json`), a check step wired
   into Phase 0 or Phase 2, and a decision on what the cap should actually be (a fact only Graham
   can supply, per the "ask for it directly" rule — his monthly budget tolerance isn't inferable
   from anything in this comparison).

3. **The pinned/canary behavioral-regression idea (idea 1, COMPLEMENT), as a whole new capability,
   not a fragment.** This is the biggest genuine gap surfaced by the whole review: nothing on this
   machine proves that a skill or CLAUDE.md rule still produces the intended agent behavior after a
   Claude Code release or model-alias change, only that it still parses correctly
   (`validate-skills.sh`) or that its prose hasn't silently drifted from a document
   (`spec-artifact-diff`). Ideas 2 (ablation), 3 (efficiency drift), 4 (provenance-tagging), and 6
   (regrade) all ride on top of this one and become free or near-free once it exists. Target: a new
   incubator skill/tool in `foundry-core` or a dedicated new plugin (e.g.
   `foundry-core:skill-eval-harness`), consuming Anthropic's own `claude plugin eval` case format
   rather than reinventing the candidate's bespoke shim, and reporting through the existing
   `evidence-report`/`pre-delivery-verifier` conventions rather than the candidate's own HTML
   dashboard. **Effort: L** — multi-session: needs case-writing for a first skill or two, a runner
   (reuse Anthropic's native `claude plugin eval` where available rather than porting
   `eval-shim.mjs`'s 346-line reimplementation), a place to store baselines, and — per the
   philosophy-conflict finding above — a decision to render "budget exhausted" as a distinct
   non-green state rather than copying the candidate's `exit 0` default.
