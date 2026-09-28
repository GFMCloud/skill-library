# Comparing `placebo` (candidate) against the installed toolkit

## 0. Ancestry

**No shared history.** The candidate is a standalone GitHub project (`Tuleeeee/placebo`, pinned `da03cc2a5f3015eb9eb38d41b39bafa9945c6987`), a shallow clone with a single commit, `"Initial release: placebo 0.1.0"` (`candidate/CHANGELOG.md:3`: `## 0.1.0 (unreleased)`). It shares no file names, no directory structure, and no prose with `inc-eval-harness/`, `inc-toolkit-review/`, or `inc-skill-discovery/` — I diffed the file listings and found zero overlapping paths, and grepped the candidate for the incumbents' names, plugin ids, and section headers (`rubric v2`, `toolkit-review`, `eval-harness`, `skill-discovery`) with no hits. There is no merge note, no CHANGELOG entry naming the other side, no matching section structure.

The one real point of contact is **citation, not code**: the candidate's own README independently cites the same paper the queue watch-list already tracks —

> "The more skills you install, the worse agents get at picking the right one. Selection precision fell from 29.6% with 5 skills to 3.3% with 100 ([arXiv 2608.14036](https://arxiv.org/abs/2608.14036))." (`candidate/README.md:24`)

— matching the queue's "arXiv 2608.14036 (retrieval precision 29.6% at 5 skills to 3.3% at 100)... already on the watch list." That's convergent problem-framing between two independent authors, not shared lineage. This reframes the comparison as ordinary "is it better," not "what did the fork learn" — there is no fork.

---

## 1. Classification

### 1.1 Same-length inert sham arm as a control for context effects
`candidate/src/placebo_cli/engine/arms.py:1-8` (verified: `build_sham_skill`, `arms.py:76-88`, keeps frontmatter, replaces body with `inert_text()`).

> "The sham keeps the skill's name and description... but its body is replaced with inert, instruction-free prose of equal length... If `treatment` beats `baseline` but not `sham`, the gain comes from the ritual, not the instructions." (`candidate/METHODOLOGY.md:16-25`)

**COMPLEMENT.** Nothing in the installed set controls for the placebo effect of *adding any text at all*. `eval-harness`'s closest mechanism is a held-out case (`inc-eval-harness/SKILL.md:91-93`: "Hold back at least one case that the change was never run against"), which guards against overfitting the *known* cases, not against the ritual effect of the change's mere presence. Consumer on this machine: `eval-harness`'s "Graders, in order of preference" section (`inc-eval-harness/SKILL.md:59-73`) has no slot for this; it would need a new clause.

### 1.2 "No effect" as a positive finding, via TOST
`candidate/src/placebo_cli/stats.py:193-238` (verified: `verdict()` implements the exact rule order stated in `METHODOLOGY.md:81-92`, including the `PLACEBO` branch at `stats.py:229-234`).

**SUPERIOR SUBSTITUTE** for `eval-harness`'s noise-handling, which is the same underlying problem (is an observed pass-rate delta real or noise) treated far more loosely:

> "Read a before/after difference against noise. It counts only when it exceeds the baseline's own run-to-run spread, measured by running the unchanged baseline more than once. At k=3 one flipped trial moves a case's pass fraction by a third." (`inc-eval-harness/SKILL.md:85-88`)

vs.

> "PLACEBO needs the 90% CI to fall inside ±delta (a TOST equivalence test at alpha = 0.05), so 'no effect' is a positive finding rather than a failure to find one." (`candidate/src/placebo_cli/stats.py:9-11`)

`eval-harness` names no formula at all — "read... against noise" is a judgment call a model makes by eyeballing three trials. `stats.py` computes a two-level bootstrap (`stats.py:121-190`, 4,000 resamples) and a formal equivalence test. **What would have to change before it could replace the incumbent's clause:** `eval-harness` is a *prose skill executed by a stateless model turn by turn* — it has no Python runtime of its own. A session cannot manually run a 4,000-resample bootstrap; adopting this idea means either (a) shipping the `stats.py` module (or a trimmed version) as a script the skill invokes, or (b) writing a much simpler closed-form CI the model can compute by hand (e.g., a Wilson interval), which is weaker than what `placebo` does. Prose transplant alone would not work — this is a **correction needed at ingest**, not a copy-paste fragment.

### 1.3 Turning commit history into validated tasks
`candidate/src/placebo_cli/tasks/git_miner.py:1-8, 128-156` (verified: `validate()` runs the check pre- and post-golden-commit and rejects tasks that don't flip; `list_candidates` requires both a test-file and a source-file diff).

> "With validation on (default), we check that the tests fail before the change and pass after it, so every task is solvable and non-trivial." (`candidate/src/placebo_cli/tasks/git_miner.py:6-7`)

**COMPLEMENT, with a scope caveat.** `eval-harness` leaves case-authoring entirely to the human ("The workflow, prompt, skill or hook under test, and the change proposed to it" — `inc-eval-harness/SKILL.md:27-28`); nothing in the incumbent set auto-mines validated cases. But `eval-harness` also explicitly disclaims this exact use: "**not a test framework for product code**" (`inc-eval-harness/SKILL.md:9-10`) — and `git_miner.py` mines *product-code* commits (source+test diffs), not skill/prompt behavior. So the gap this fills sits just outside `eval-harness`'s stated boundary; it's a generally useful technique with no current consumer on this machine, not a drop-in fix for `eval-harness` itself.

### 1.4 Interleaving arms against drift
`candidate/src/placebo_cli/engine/runner.py:61-76` (verified: `plan()` shuffles `(task, arm)` pairs per round with a seeded RNG).

> "Interleaving arms over time protects against drift (API load, silent model updates) that would bias an 'all baselines first' schedule." (`candidate/src/placebo_cli/engine/runner.py:64-65`)

**COMPLEMENT**, narrow. `toolkit-review` interleaves *judge order* (`references/judge-prompt.md`: read `[first]` then `[second]`, with an `XY`/`YX` swap — `SKILL.md:79-81`) to cancel primacy bias, which is a different axis (reader bias, not time drift), and `toolkit-review` has no multi-arm, time-separated comparison at all. `eval-harness` runs `k` trials of one target with no arms to interleave. Nothing on this machine currently protects a comparison from model-version drift across a run that takes hours.

### 1.5 NOT_ACTIVATED — not scoring what never ran
`candidate/src/placebo_cli/stats.py:204-209` (verified: first verdict-rule check, activation rate `< min_activation` short-circuits to `NOT_ACTIVATED`); activation is detected in `candidate/src/placebo_cli/adapters/claude_code.py:106-108` (`tool_use` events matched against `watch`) and requested via `arms.py:99,104` (`watch=[name]`).

**COMPLEMENT — fills a gap the incumbents have documented but not solved.** `toolkit-review`'s own limits file names this exact blind spot and stops there:

> "**Skill calls are invisible in `--output-format json`.** 'Did the current setup trigger a review skill' cannot be answered from a fixture run's JSON result." (`inc-toolkit-review/references/limits.md:17-18`)

`placebo` answers precisely that question, working: it parses the `stream-json` event stream for `tool_use` calls naming the skill (`claude_code.py:104-108`) and gates the whole verdict on a 30% activation floor before anything else is computed (`stats.py:205-209`). This is also the "trigger" and "restraint" half of the queue's Q-2026-09-14-1 plan — see §3.

### 1.6 Separating infrastructure failures from performance failures (circuit breaker)
`candidate/src/placebo_cli/engine/runner.py:153-158, 261-264` (verified: an `agent_error` classification when the run produced no tool calls and no changed files; a breaker trips if the first two completed runs are both `agent_error`).

**REDUNDANT** against `eval-harness`, which already states the identical principle, more conservatively:

> "The same trial fails identically twice for an environmental reason (missing tool, auth): report it as `not runnable`, not as a failed eval." (`inc-eval-harness/SKILL.md:114-115`)

`eval-harness`'s trigger is narrower and safer (the *same* case must fail *identically twice* for an *environmental* reason) than `placebo`'s heuristic (any run with zero tool calls and zero changed files, which can also catch a skill that makes the agent fail immediately on legitimate task difficulty — this is exactly cleanroom review finding 4a-3, which I spot-checked and confirmed at `runner.py:97` excluding `agent_error` from `records_to_trials`). `placebo`'s version is not measurably better; if anything it is more exploitable. Nothing to take here beyond what `eval-harness` already says.

### 1.7 Norms for publishing results about someone else's skill
`candidate/METHODOLOGY.md:109-113`.

> "If you publish results about a named public skill, please: share the full report and traces, state agent and model versions and the number of tasks and trials, report nulls as well as wins, and give the author a chance to respond before publication."

**COMPLEMENT.** None of `eval-harness`, `toolkit-review`, or `skill-discovery` addresses disclosure ethics for publishing a verdict about someone else's published work. `toolkit-review` runs in `many-repos` mode against named external sources and produces a `LEDGER.md`/`decisions.md` that could plausibly get shared outside this machine (`inc-toolkit-review/SKILL.md:42-45`) — if that ever happens, this is the one clause worth grafting in, as a fragment (see §1.9).

### 1.8 `placebo trigger` — activation and false-activation rate testing
`candidate/src/placebo_cli/engine/trigger.py:91-149` (verified: generates or loads "should trigger" / "should NOT trigger" probes, runs each in a scratch dir, computes `recall` and `false_trigger_rate`).

**COMPLEMENT — the single highest-value item.** This is not on the cleanroom review's curated "ideas" list, but it is the most consequential thing in the repo relative to the queue, so I classify it separately. See §3 for detail; briefly: nothing installed generates near-miss probes and measures a false-activation rate as a standing, repeatable check. `skill-discovery` and `toolkit-review` both reason about triggering *in prose*, never by running probes and counting.

### 1.9 `placebo scan` — collision detector, context-tax accounting, security flags
`candidate/src/placebo_cli/static/collisions.py:79-113` (TF-IDF cosine similarity over `name + name + description`, threshold 0.35), `candidate/src/placebo_cli/static/tokens.py:21-34` (byte-based always-loaded/body/resource token estimates), `candidate/src/placebo_cli/static/security.py:140-166` (Unicode-tag decoding, pipe-to-shell, instruction-override, exfil-endpoint patterns).

**COMPLEMENT, strong applicability.** `toolkit-review`'s rubric asks a judge to score "Context cost" using "the counted facts in the report, do not estimate" (`references/judge-prompt.md:44`) — which requires a ~100k-token headless extraction pass per side (`SKILL.md` frontmatter: "about 100k tokens per extraction side" — `inc-toolkit-review/SKILL.md:13`) to get a number `placebo scan` computes for the whole 76-skill library in one free, instant, offline pass (`README.md:33-36`: "Free, instant, no API calls"). `skill-discovery`'s Step 1 dedup check is a single LLM's prose judgment ("If an extracted workflow maps cleanly to an existing skill, exclude it" — `inc-skill-discovery/SKILL.md:155-157`), with no similarity score and no standing, repeatable check across the whole library. Neither incumbent has anything that scans the *entire* installed set for accidental description overlap the way `find_collisions` does — which is exactly the mechanism behind the arXiv 2608.14036 finding both the candidate and the queue already cite. This machine's own inventory (`../inventory.md`, 76 skills) sits well inside that paper's danger zone.

### 1.10 Verdict grammar, HTML report, adapter framework, examples/skills fixtures, "How it compares" table, roadmap branding
**DISCARD.** The comparison table (`README.md:126-136`), badges, "SkillBench" branding, and the `examples/skills/*` fixtures are demo/marketing scaffolding for the standalone tool and carry no transferable idea; nothing here is worth harvesting into a skill file.

---

## 2. Routing collisions

The candidate ships **no `SKILL.md` of its own** — it is a `pip`-installed CLI, so there is no live description string competing for the router today, and therefore no case of "identical names, different bodies" (the worst case) to report.

The real risk is *if someone wraps `placebo` in a skill*. `eval-harness`'s trigger vocabulary —

> "Use when the user says 'write evals for this', 'eval-driven', 'pass@k', 'is this skill reliable', 'did the prompt change regress anything'..." (`inc-eval-harness/SKILL.md:6-8`)

— overlaps heavily with the natural description of a `placebo`-wrapping skill (it literally reports `pass@k`-shaped verdicts and answers "is this skill reliable"). A prompt like **"did that prompt change regress anything?"** would today route cleanly to `eval-harness`; if a `placebo` wrapper skill were installed describing itself with similar words, the router would have two candidates that give *materially different* answers — `eval-harness`'s hand-written pass@k/pass^k vs. `placebo`'s git-mined, sham-controlled, bootstrap-CI verdict — and nothing in either description currently distinguishes "graded by a rubric you write" from "measured against a sham-controlled baseline on real git history." Whichever skill's description scores higher against the prompt's exact wording would win, and that's not predictable from the current text. **Recommendation if a wrapper is ever built:** its description should explicitly name what makes it different ("actually executes the agent against git-mined tasks with a sham control," not "evals") to keep the two from colliding on "reliable"/"regression"/"pass@k."

Separately, **not a routing collision but a naming trap**: the candidate's own module is `placebo_cli/skills/discovery.py` (`discover_installed`, `discover_path` — finds `SKILL.md` files across agent directories on disk). This is a different job entirely from the installed `skill-discovery` skill (which mines Claude *session transcripts* for undocumented workflows — `inc-skill-discovery/SKILL.md:16-21`). Nothing routes on this today since it's a Python module name, not a skill name — but if a maintainer names a future wrapper skill "skill-discovery" or "discovery," it would collide directly with the installed skill under a shared name but a completely different body (the worst case the task asks me to watch for). Flagging pre-emptively.

---

## 3. Philosophy conflicts

**Judgment-primary vs. execution-primary grading — a real contradiction, not just emphasis.**

`eval-harness` ranks graders explicitly and subordinates model judgment below execution:

> "1. **Code grader.** A command with an exit code... Use it whenever the criterion can be stated mechanically. 2. **Model grader.** A separate run scores the output against a written rubric... its known weakness is stated beside the score: **it is a second opinion, not a measurement.**" (`inc-eval-harness/SKILL.md:61-67`)

`toolkit-review`'s entire method is the opposite: the load-bearing verdict for "should this replace what's installed" is *computed from two LLM judges' prose rows*, with no execution step at all except a narrow, explicitly unreliable fixture arm:

> "the judges see neutral reports and never the files... the slot verdict is computed from their per-item rows." (`inc-toolkit-review/SKILL.md:23-24`)
> "**Fixture results are fixture-derived** and say nothing about real repositories." (`inc-toolkit-review/references/limits.md:24-25`)

So for `toolkit-review`, a "second opinion, not a measurement" *is* the measurement — for everything except the one slot type (`full`, hook/fixture) where behavior can actually be run, and even that layer is labeled unreliable. `placebo`'s entire premise agrees with `eval-harness`, not `toolkit-review`: pass rate from executed agent runs is the real signal, and the sham arm exists specifically to catch the case where an LLM (or a human) *thinks* something helped when the actual behavior didn't change (`METHODOLOGY.md:22-25`, quoted in §1.1). This is a genuine, quotable disagreement between two installed skills — worth a note in `toolkit-review`'s `history.md` next to the existing "what it cost" section, not just something to resolve silently by picking a side.

**Alignment worth naming explicitly (not a conflict):** the queue's Q-2026-09-21-2 — "skills are measured rather than deleted" — is exactly `placebo`'s stated thesis (`METHODOLOGY.md:1-9` frames the whole tool as answering "does adding this skill... change how often the agent completes real tasks," not whether to keep or cut it). No tension there.

---

## 4. Corrections needed at ingest

- **A code comment is factually wrong — verified by direct read.** `arms.py:84`: `# count referenced resources too, so the sham has comparable bulk`, immediately followed by `arms.py:85`: `body = "# Notes\n\n" + inert_text(max(body_len - 10, 200))`, where `body_len = len(skill.body)` (`arms.py:83`) — only the `SKILL.md` body length, never anything in `skill.root`'s other files. `build_sham_skill` writes only `SKILL.md` (`arms.py:76-88`) and never touches `references/`, `scripts/`, or `templates/`. I confirmed this by reading the function in full: this matches cleanroom review finding 4a-2 exactly. Any fragment pulled from `arms.py` needs that comment deleted before it goes anywhere — it currently documents behavior the code doesn't have. (The limitation itself *is* disclosed correctly in `METHODOLOGY.md:17`: "Supporting files are omitted" — only the code comment is wrong.)
- **A rule a stateless model cannot honor as prose.** The TOST/bootstrap idea (§1.2) cannot be adopted by writing it into `eval-harness`'s markdown alone — a session executing that skill turn-by-turn cannot reliably hand-compute a 4,000-resample bootstrap. Ingesting it requires shipping runnable code (a trimmed `stats.py`) alongside the skill, not just prose describing the method.
- **Factual claims not independently verifiable here, and already flagged once.** The README's headline statistics ("39 of 49 skills," "307 skill-induced failures," SWE-Skills-Bench) were marked "claimed only, not verified" by the cleanroom reviewer (`cleanroom-review.md:51-59`); I had no network access either and could not check them. Before quoting these numbers anywhere in the library, run `verification-kit:fact-currency-check` — this is the exact case that skill exists for, and `toolkit-review`'s own `limits.md` models the right habit: "re-measure the CLI ones with `verification-kit:fact-currency-check` on a new CLI version" (`inc-toolkit-review/references/limits.md:3-4`).
- **Style violations against the library's register.** The candidate's README uses badges, an emoji in the title ("placebo 💊"), a competitor comparison table framed as marketing (`README.md:126-136`), and roadmap branding ("SkillBench"). None of that belongs in a `SKILL.md` — the installed skills are uniformly terse, imperative, and non-promotional (compare `inc-eval-harness/SKILL.md`'s plain "Use when the user says..." register). Any lifted fragment needs that tone stripped before it goes in.
- **Operational risk, not a text problem, but worth stating at ingest time regardless:** `trigger` and `ab` run a real agent with `--permission-mode acceptEdits` and `Bash` allowed (`claude_code.py:73`), inside a worktree that is not a sandbox — the cleanroom review's own safety framing (rubric item 4, 3/5) applies unchanged to any use of this code, not just to reading it.

---

## 5. Net assessment

If only three things could be taken:

1. **`placebo trigger` + `placebo ab`'s baseline/treatment arms, as a whole capability, not a fragment.** This is the strongest finding of the whole review: the queue's Q-2026-09-14-1 plans "a first `claude plugin eval` suite (three cases: trigger, behavior, restraint) with a with/without ablation arm." `placebo trigger`'s `recall` metric is the trigger case, its `false_trigger_rate` is the restraint case (`trigger.py:135-149`), and `placebo ab`'s baseline-vs-treatment comparison (`arms.py:97-99`, `stats.py:215-222`) *is* the with/without ablation arm. Three of the four things Q-2026-09-14-1 set out to build already exist here, working, with tests. **Form:** not a skill port — it's a Python dependency with real operating cost (paid agent runs, `Bash`-enabled worktrees) — so land it as a referenced external tool, not lifted prose. **Target:** a line in `inc-eval-harness/SKILL.md`'s "Graders" section pointing at it as an option for the code-grader tier, and a note on Q-2026-09-14-1 itself naming this repo as a reference implementation to evaluate before building from scratch.

2. **The sham-arm / equivalence-testing idea, as a fragment, into `eval-harness`'s Metrics section.** Replace the vague "Read a before/after difference against noise" clause (`inc-eval-harness/SKILL.md:85-88`) with an explicit equivalence concept modeled on `METHODOLOGY.md:81-92`'s verdict-rule ordering — even without porting the bootstrap code, naming "no effect is a provable finding, not silence" tightens a currently hand-wavy instruction. **Target file:** `inc-eval-harness/SKILL.md`, Metrics section.

3. **`placebo scan`'s collision detector, as a fragment/tool, referenced from `toolkit-review`.** Nothing installed scans the *whole* library for accidental description overlap the way `find_collisions` does (`collisions.py:79-113`) — and this machine's 76-skill inventory is exactly the size the queue's own watched paper (arXiv 2608.14036) says starts degrading routing precision. **Target:** a pre-flight step referenced from `inc-toolkit-review/SKILL.md`'s pipeline (before Step 4, "Slot map and items") or a standalone note pointing maintainers at running this scan against `~/skill-library` periodically — cheap, free, and currently unaddressed by anything installed.

Everything else — the runner/workspace/git-worktree machinery, the HTML reporter, the adapter framework, the circuit breaker, and the README's own marketing apparatus — is either infrastructure with no idea left to extract once the above three are taken, or (circuit breaker, §1.6) already matched, more safely, by prose already in `eval-harness`.
