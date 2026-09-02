# Comparison: "The AI-Native SDLC playbook" against the installed set

Candidate: `/private/tmp/claude-501/-Users-gfm-work/9589a5b4-45ce-4e6c-aff9-d5394355d7b7/scratchpad/source/ai-native-sdlc-playbook.md` (article, Louis Claxton, claude.com, dated 2026-08-21). Pin re-checked this pass: `shasum -a 256` returned `adfcd44e65105377bc05c3577a0193bb4f8bc1b77e3597e7ff4852b0ce1a213f`, matching the task file. Line numbers below (`L123`) refer to that file.

Clean-room review: `/private/tmp/claude-501/-Users-gfm-work/9589a5b4-45ce-4e6c-aff9-d5394355d7b7/scratchpad/cleanroom-review.md`.

Quoting note: incumbent text is quoted verbatim and some of it carries em dashes from before the no-em-dash rule. My own prose and every proposed edit below contain none.

## Bottom line

- **No shared ancestry.** Nothing in `~/skill-library` or `~/.claude/CLAUDE.md` names the article, and the article names nothing local. The overlap is convergent, not inherited.
- **Of 27 techniques classified, 15 are REDUNDANT, 6 are INGESTIBLE FRAGMENTS, 1 is a COMPLEMENT nothing here consumes, and 5 are DISCARD.** The article's core ideas (executed evidence, files as the bridge between sessions, boundaries enforced at the tool layer, no approval prompts mid-run, one source of truth) are all already rules in `/Users/gfm/.claude/CLAUDE.md` or bodies in the library, and in every case the incumbent states them with the originating failure attached, which the article never does.
- **The three things worth taking are all gaps between a rule this machine already has and its tool-layer enforcement:** a `permissions.deny` for credential files (the global rule says "not reading them" and `settings.json` has no deny list at all), the red-test-first plus frozen-test procedure for bug fixes (incumbents say "do not weaken the check" but never say how to make that structural), and evals that run when agent configuration changes (the authoring standard promises evals; the library has zero and CI runs only the structural validator).

## 1. Ancestry

Checked:

- `/usr/bin/grep -rniE "ai-native|sdlc|playbook|claxton|intent\.md|REVIEW\.md|bands\.yaml|western electric|two-strike|mistake twice"` over `~/skill-library` (excluding `.git`): every hit is the `decks` plugin's own "conversion playbook" references or `source-intake`'s mention of `cleanroom-review.md`. No hit on the article, its author, or its artifact names.
- `~/skill-library/docs/reviews/` does not exist yet (no prior review record). `CHANGELOG.md` has no SDLC or playbook entry. `git log --oneline -8` shows only the incubator retirement and source-intake work.
- `/Users/gfm/.claude/CLAUDE.md`: the only hits on "twice" are the `ugrep` note and the CLAUDE.md economy rule ("Write a project fact down only once it has cost a correction twice"), which predates the article (consolidated 2026-08-12; article dated 2026-08-21).
- Dates: `proof-of-work` and `evidence-report` reviewed 2026-08-09; `phased-harness` v1.2.3 reviewed 2026-08-28; the global file consolidated 2026-08-12. The library's ideas were written before or independently of the article, and the article's cite-nothing style means it did not fork from them either.

Verdict: **no shared history in either direction.** Every classification below is "is it better", not "what did the other side learn".

## 2. Spot-checks of the clean-room review

I did not take the review's judgments on trust. What I checked against the article itself:

| Review claim | Checked at | Result |
|---|---|---|
| `production-gate.sh` substring-matches `deploy` and `production` on a `Bash` matcher and gates on an env var | L791 (`"matcher": "Bash"`), L808 (`[[ "$cmd" == *"deploy"* && "$cmd" == *"production"* ]]`), L809 (`[ -z "$RELEASE_APPROVAL" ]`) | Confirmed. The next play tells the reader to route deploys through MCP (L918), which this matcher never sees. |
| Eval workflow has no timeout and overwrites `result.json` each loop | L668 to L673 | Confirmed: `> result.json` inside the `for` loop, no `timeout-minutes`, no concurrency key. |
| Stage 1 "Prerequisites: None" while step 3 needs a template "encoded as a skill" (a Stage 3 play) | L147 vs L161 | Confirmed. |
| Stage 2 says "No engineering skill is required" while step 2 asks for a slash command and a non-interactive merge-triggered job | L226 vs L231 | Confirmed. |
| The twelve quoted techniques are verbatim | L370, L720, L461, L577, L580, L645, L646, L643, L286, L285, L985, L984, L920, L341, L347, L717, L739, L742, L485, L591, L255, L198 | All twelve match verbatim. |
| "Reading time 5 min" for ~9,000 words | L24 to L26; `wc -w` gives 11,250 tokens including markup | Confirmed as wrong on the page. |
| Every outbound link is an Anthropic property | `grep -oE "https?://..."` excluding claude.com, anthropic.com, website-files.com | Confirmed: zero remaining links. |
| "Claude Mythos 5" is "named once, nowhere else" | `grep -n Mythos` | **Wrong in detail.** It appears twice (L1031 and L1045, "billed on consumption at Mythos 5 rates"). The currency point stands; the count does not. |

The review's judgments held on every load-bearing point. One factual slip (the Mythos count) and one thing it under-weighted: the article's claim at L505 that "all sessions read the file" (CLAUDE.md) is contradicted by a verified finding already in the library (see Philosophy conflicts, item 4).

## 3. Classification table

| # | Technique | Classification | Target of any fragment |
|---|---|---|---|
| 1 | Two-strike rule for CLAUDE.md corrections | REDUNDANT | |
| 2 | Advisory (skill) vs deterministic (hook) controls | REDUNDANT | |
| 3 | Protect the verification loop: red test first, commit, fix without touching it, hook blocks test edits | INGESTIBLE FRAGMENTS | `new-project/scripts/scaffold.sh` (`stub_claude` rule 6), `new-project/references/conventions.md`, plus a fresh PreToolUse hook |
| 4 | Regression-test agent configuration with evals in CI | INGESTIBLE FRAGMENTS | `docs/authoring-standard.md` (Change hygiene); `retro/SKILL.md` §3 routing table |
| 5 | Plan-quality bar and interrogation prompts | REDUNDANT | (maps to `anthropic-skills:plan-gate`, not an edit target) |
| 6 | Autonomy tiered by statistical deviation band (`bands.yaml`) | COMPLEMENT | no consumer on this machine; WATCH |
| 7 | Rehearse rollback | REDUNDANT | |
| 8 | One source of truth per artifact (sidebar) | REDUNDANT | (one philosophy conflict, below) |
| 9 | `REVIEW.md`: cap nits, define Important, exclude CI-enforced items | INGESTIBLE FRAGMENTS | `fable-project-review/SKILL.md` Phase 2 |
| 10 | Keep approval prompts out of the build phase | REDUNDANT | |
| 11 | "Done" means verified, in writing | REDUNDANT | |
| 12 | Measurement definitions from git and PR data | DISCARD | |
| A | `intent.md` / `spec.md` / `plan.md` committed-artifact chain | REDUNDANT | |
| B | Verifier subagent (fresh context, report only) | REDUNDANT | |
| C | Hooks as approval gates (`production-gate.sh`, PreToolUse on Bash) | INGESTIBLE FRAGMENTS | `~/.claude/settings.json` hooks; pattern only, not the script |
| D | Managed settings block: credential and secret denies, sandbox | INGESTIBLE FRAGMENTS | `~/.claude/settings.json` `permissions.deny` (and `sandbox.credentials` once keys are verified) |
| E | Parallel sessions in worktrees plus subagents | REDUNDANT | |
| F | Skills as institutional knowledge, including "test that the skill triggers" | INGESTIBLE FRAGMENTS | `docs/authoring-standard.md` ("The description is the router") |
| G | The CLAUDE.md play (`/init`, cut to a page, "Things Claude gets wrong") | REDUNDANT | |
| H | Plan mode as default start, commit `plan.md`, sync hook | REDUNDANT | (maps to `anthropic-skills:plan-gate`) |
| I | Feedback-loop mechanics (one-command test target, quantifiable target, screenshot loop) | REDUNDANT | |
| J | CI/CD adoption order, MCP deploy tools as allowlist, per-environment tiers | REDUNDANT | |
| K | Claude Security scheduled scans | DISCARD | |
| L | Claude Tag on-call | DISCARD | |
| M | Auto mode conditions ("tight spec, small blast radius, covered by tests") | REDUNDANT | |
| N | Dependency graph and "start with any clay play" | DISCARD | |
| O | Intent capture in the originator's own words (what, why, constraints) | REDUNDANT | |

## 4. Per-item analysis

### 1. Two-strike rule: REDUNDANT

Article, L370:
> "A working rule helps here. When Claude makes a mistake twice, the correction goes into `CLAUDE.md`."

Incumbent, `/Users/gfm/.claude/CLAUDE.md`, "CLAUDE.md economy":
> "Keep CLAUDE.md files short; every line loads into every session. Write a project fact down only once it has cost a correction twice."

Same trigger, same destination, and the incumbent pairs it with the cap that keeps the file short. The incumbent is also superior in mechanism: the article's rule requires a session to remember a mistake from an earlier session, which a stateless model cannot do. `retro/SKILL.md` §2 solves exactly that:
> "By the time a retro gets written, your context may already be compacted. You are not a reliable narrator of your own session ... Ground every claim in the record"

and routes the correction by type rather than dumping it all into CLAUDE.md (§3 routing table; see Philosophy conflicts, item 3). The article's review-loop twin (L720, "because review reads `CLAUDE.md` the mistake is caught from the next PR onwards") presumes an automated PR reviewer that reads CLAUDE.md; none runs on this machine's repos.

### 2. Advisory vs deterministic controls: REDUNDANT

Article, L461:
> "A skill is a control, though an advisory one. It makes Claude likely to apply the policy while the code is written, and nothing forces a session to comply with it. A policy that must always hold needs something deterministic behind the skill ... The skill makes violations rare and the hook makes them close to impossible."

Incumbent, `/Users/gfm/.claude/CLAUDE.md`, "Boundaries are declared and enforced":
> "Name the boundary before the work starts, and enforce it at the tool layer where possible: a rule in prose can be reasoned around, a tool the agent does not have cannot."

`pipeline-foundry/SKILL.md` §4 restates it with a verified instance:
> "A rule in prose can be reasoned around; a tool the agent does not have cannot be. Where a recommended specialist's job is to check or verify, it carries `disallowedTools: ["Write", "Edit", "NotebookEdit"]`. This is **verified as enforced, not merely parsed.**"

`standing-authorization/SKILL.md` gives the burn that produced the rule: "Prose did not bind. So this is not more prose. It is a file the agent reads and a check". And the machine practices it: `~/.claude/settings.json` carries a `PreToolUse` hook on `Artifact` that denies a publish containing an em dash (checked this pass). The article's one-liner is crisper than the global rule, but the global rule generalizes beyond skills and hooks (it also covers `disallowedTools`, permission rules, and missing tools) and is already loaded into every session. Not worth an edit.

### 3. Protect the verification loop: INGESTIBLE FRAGMENTS

Article, L577:
> "For bug fixes, write the failing test first. Ask Claude to reproduce the bug as a test, run it, and confirm it fails for the reason you expect. Commit that test. Only then ask Claude to make it pass without editing the test, with the test-file hook from the final step enforcing the restriction."

and L580:
> "the loop itself needs protecting, because an agent fixing code must not be able to weaken the check on that code. A hook that blocks edits to test files during a fix task does this."

Incumbents state the principle without the procedure. `new-project/scripts/scaffold.sh`, `stub_claude` rule 6:
> "**Do not relax an assertion to make a change pass.** If a check fails, either the change is wrong or the check is — decide which, out loud."

`/Users/gfm/.claude/CLAUDE.md`:
> "A red validator is a bug in the content, never in the validator. Fix the content, or deliberately change the rule"

and, the closest cousin, "A gate or validator is trusted only after being proven by deliberate failure; a check that has never failed a fixture is untested." The article's "confirm it fails for the reason you expect" is that rule applied to a bug-reproduction test, which no incumbent spells out. And no incumbent makes "do not weaken the check" structural: the global rule says to enforce boundaries at the tool layer, yet the only hook on this machine is the em-dash check.

Fragments:

- **3a. Red test first, committed, then frozen.** Target: `new-project/scripts/scaffold.sh`, `stub_claude` rule 6 (the generated CLAUDE.md is the artifact every project session loads), with a matching sentence in `new-project/references/conventions.md` under SPEC.md §6. Proposed text to append to rule 6: "For a bug fix, write the reproducing test first, run it, confirm it fails for the expected reason, and commit it before touching the code. The fix commit must not edit that test." Also consumed by `~/work/scl-player-model` and the pinball project, both of which have test suites.
- **3b. A hook that blocks test-file edits during a fix task.** The article names the mechanism but ships no script for it (its only script is the production gate). Write fresh: a `PreToolUse` hook on `Edit|Write` that exits 2 with a reason when the path matches `tests/**` and a fix-task marker is set. Target: the `python` archetype in `scaffold.sh` (which already lays down `tests/`) as a `.claude/settings.json`, or `~/.claude/settings.json` if Graham wants it machine-wide. Prove it by deliberate failure before trusting it, per the global rule.

### 4. Regression-test agent configuration: INGESTIBLE FRAGMENTS

Article, L645 to L647:
> "The suite runs non-interactively in CI on a schedule and on any change to `CLAUDE.md`, skills or hooks, since that configuration steers the agent and deserves the regression testing that code gets."
> "Gate configuration changes on the results. A skill change that drops the pass rate gets reviewed before it merges."
> "Each production incident gets an eval, written by the team that owned the incident, and stays in the suite as a regression test."

Incumbent, `/Users/gfm/skill-library/docs/authoring-standard.md`, "Change hygiene":
> "Behavior testing: for stable skills keep 2–3 eval cases and run them on change (the official `skill-creator` plugin provides evals and version comparison). Reviewing prompt diffs alone tells you almost nothing about behavior."

The rule exists; the mechanism does not. Checked live this pass: `find ~/skill-library -iname "*eval*"` returns nothing, and `.github/workflows/validate.yml` runs only `STRICT=0 bash scripts/validate-skills.sh`, the structural validator. So the library's promise of evals is currently prose, which is the failure the library's own rules warn about.

Fragments:

- **4a. Trigger and gate.** Target: `docs/authoring-standard.md`, "Change hygiene". Proposed text: "Evals run in CI on any change to a stable skill, a hook, or a CLAUDE.md, because that configuration steers the agent and deserves the regression testing code gets. A change that drops the pass rate is reviewed before it merges, not after." This is a sharper statement of "run them on change" and it names the gate.
- **4b. Incident to eval.** Target: `retro/SKILL.md` §3 routing table, which currently routes only deterministic checks to "A hook or CI, not prose". Add a row: "Behavioral regression (the agent did the wrong thing and no script can catch it deterministically) | An eval case in the owning skill's `evals/`, kept as a regression test". This gives the retro a destination it lacks today.

Not taken: the GitHub Actions workflow at L651 to L674 (unbounded, `result.json` overwritten, per the review) and the "20 to 50 real tasks" corpus (L643), which is sized for an organization; the standard's "2–3 eval cases" per stable skill is right for a one-person library. The `claude plugin eval` command that the `claude-code-guide` agent description mentions is the mechanism to use, not a hand-rolled loop over `claude -p`.

### 5. Plan-quality bar: REDUNDANT

Article, L286 and L285:
> "Iterate until an engineer who has never seen the conversation could implement the change from the plan alone."
> "Interrogate the plan by asking what the change could break, which step is most risky, and what other options Claude chose not to do."

Incumbent, `fable-project-review/references/plan-template.md`:
> "Before finalizing, re-read every item and ask: \"could a model with zero context execute this correctly?\" If the answer is no, add whatever's missing"

`fable-project-review/SKILL.md` Phase 3: "Any sentence in the plan that only makes sense with this session's context (\"as discussed\", \"the issue above\", \"like we said\") is a defect". `phased-harness/SKILL.md`: "Test: could a fresh session with no history resume this run from disk alone? If not, the harness is incomplete." `pipeline-foundry/SKILL.md`: "a brand-new Claude Code session, with zero conversation context, can execute from." The same bar is stated three times in the library with a self-containment checklist attached (exact paths, verbatim current-state excerpt, non-goals), which the article lacks.

The interrogation trio maps to `anthropic-skills:plan-gate` ("numbered falsifiable assumptions", "at most three blocking questions"), `fable-project-review`'s per-item "Non-goals", and `phased-harness/templates/end-state.template.md` "Why this shape and not the alternatives". `plan-gate` is not in this library and is not an edit target; the article's plan-mode play is that skill's territory.

### 6. Autonomy tiered by deviation band: COMPLEMENT (no consumer)

Article, L985 and L984:
> "At 1σ the script only logs, at 2σ it invokes Claude read-only to diagnose, and at 3σ Claude may act, though only by opening a PR into the review gate or triggering a pre-approved runbook."
> "detection stays entirely deterministic, with no model involved."

Nearest incumbents. The tiering-by-action-class half already exists on this machine, outside the library: `~/.claude/projects/-Users-gfm-work/memory/claude-improvements-weekly.md` records the ruling "Tier 1 (routine) and Tier 2 (behavior changes, including global `~/.claude/CLAUDE.md` edits) are auto-applied with local commits; Tier 3 (production, deletions, pushes, credentials, ambiguous) is queued for `/phase ratify`." `pipeline-foundry/SKILL.md` §8 gives a scheduled re-entry trigger ("Set a cadence at intake. **Default: weekly.**"). `deploy-verify-fix/SKILL.md` gives stop conditions ("Three consecutive cycles fail and the last produced no new information").

The gap is the trigger: a deterministic statistical detector (rolling baseline, Western Electric rules) over a production or process metric that decides *when* to invoke Claude and at which tier, with the tier bound to a tool allowlist (`tools: "Read,Grep,Bash(gh run view *)"` at L1000). No incumbent has a metric-driven trigger; all triggers here are schedules or humans.

Consumer: none today. No project on this machine has a metrics store with a rolling baseline (gfmcloud-hub is a static site; the SCL model is a personal analysis project; the weekly maintainer is schedule-driven). The σ-to-tier mapping is asserted with no derivation (review §5). Recommend WATCH; if a consumer appears, the landing spot is `pipeline-foundry/SKILL.md` §8 as a second trigger type beside the weekly routine, with the 3σ "pre-approved runbook" route removed (see Philosophy conflicts, item 5).

### 7. Rehearse rollback: REDUNDANT

Article, L920:
> "Rollback should be the most rehearsed path in the pipeline, a single command that the agent can run and that is exercised regularly in staging."

Incumbent, `deploy-verify-fix/SKILL.md`, "Before the first deploy":
> "**The rollback command**, tested. A rollback first attempted during an incident is not a rollback plan."

plus the stop condition "**Rollback is now cheaper than rolling forward.** Say so and recommend it". `new-project/scripts/scaffold.sh` homelab runbook makes the rehearsal date a checkable field: "The actual steps, and the date they were last **tested end to end**. A backup nobody has restored from is not a backup" with `Last tested: never` as the seeded value. The article's "regularly" is a cadence word; the incumbent's dated field is the thing that can be inspected. Equal or better.

### 8. One source of truth per artifact: REDUNDANT

Article, L341:
> "for every artifact the process produces, name one system as the source of truth, with everything else holding a copy or a link to the original."

Incumbent, `/Users/gfm/.claude/CLAUDE.md`, "Duplication and reversibility":
> "Every rule, skill, and document has exactly one editable home. Mirrors, plugin caches, and generated copies are read-only; an editable duplicate is drift, so flag it rather than silently keeping both."

and "Source-of-truth precedence": "where a project explicitly names an authoritative source or verifier ... that source wins. Defer to it and correct the stale copy". `new-project/references/conventions.md` on SPEC.md: "The single source of truth. When another doc disagrees with it, this one wins and the other gets fixed. When *reality* disagrees with it, this file gets fixed." The incumbents add the precedence rule and the conflict-is-a-stop rule; the article adds nothing. Its "Linkage as the minimum bar" (L347) contradicts the global rule; see Philosophy conflicts, item 1.

### 9. `REVIEW.md` and capping review noise: INGESTIBLE FRAGMENTS

Article, L717, L739, L742:
> "`REVIEW.md` also defines what counts as Important as opposed to a Nit, and what to skip."
> "Report at most five nits per review; summarize the rest as a count."
> "Generated files under src/gen/ and anything CI already enforces."

Incumbent, `fable-project-review/SKILL.md`, Phase 2:
> "Rank findings by severity: **Critical** (broken or actively misleading), **High** (will bite soon), **Medium** (friction), **Low** (polish)."
> "Don't pad. If a dimension is clean, say so in one line and move on. The user wants signal, and a review that manufactures findings to look thorough erodes trust in the real ones."

The incumbent ranks and forbids padding but sets no ceiling on low-severity volume and never tells the reviewer to skip what a linter or CI already enforces. Those two directives are concrete and better than "don't pad".

Fragment, target `fable-project-review/SKILL.md` Phase 2, after the "Don't pad" paragraph: "Cap Low findings at five per review and summarize the rest as a count. Do not report anything a formatter, linter, or CI check already enforces, and nothing under a generated path; those are noise wearing a finding's clothing." `fable-project-review` is incubator, so this is a direct edit on main.

Not taken: `REVIEW.md` as a file. The review is right that it is a convention, not something the harness loads (L717 presents it in the same register as `CLAUDE.md`), and no automated PR reviewer runs against this machine's repos. The built-in `/code-review` skill covers PR review and is not a library edit target.

### 10. Keep approval prompts out of the build phase: REDUNDANT

Article, L485:
> "A hook that asks a human for approval belongs with the gates in Stage 5: Deploy, because an approval prompt during the build puts a person back on the critical path of all the sessions running in parallel."

Incumbent, `phased-harness/references/doctrine.md`:
> "asking \"shall I continue?\" there converts a continuous run back into a stop-start one for no information gain."

`phased-harness/SKILL.md`: "Between and after gates the run **never asks \"shall I continue?\"**. Anomalies are logged in STATE.md with a one-line recommendation and reviewed at the next gate." `sweep-harness/templates/dispatch-SKILL.template.md`: "Interruption policy: None, between batches." `/Users/gfm/.claude/CLAUDE.md` standing defaults: "Build, verify, inspect, and search steps with no destructive side effect proceed without asking." `standing-authorization/SKILL.md`: "`ALREADY-GRANTED` ... **the ask is the defect.**" The incumbents go further: they name where the gates are (A and B), what is never pre-authorizable, and give a tool (`authz.py check`) that flags the stray question. The article has the principle only.

### 11. "Done" means verified, in writing: REDUNDANT

Article, L591 to L592:
> "Run all three before reporting any task complete, and paste the output. If a test fails, fix the code, not the test."

Incumbent, `/Users/gfm/.claude/CLAUDE.md`, first line of "Evidence over assertion":
> "No artifact is presented as done without executed evidence: the command and its actual output, not a paraphrase, not a checkmark."

`proof-of-work/SKILL.md`: "State what was run, against what input, and what came back. All three. A result with no input named is not reproducible." and "Verify at the level the failure lives." `evidence-report/SKILL.md`: "The not-verified list is mandatory." `scaffold.sh` rule 2: "**Show evidence.** Command output, diffs, screenshots, test results. Assertions of success are not success. If verification was skipped, say which step and why." The incumbent is strictly superior: it adds the not-verified list, "a success message is not evidence" with three logged instances, and the level-of-failure rule. "Paste the output" is a subset of it.

### 12. Measurement definitions: DISCARD

Every metric (L194, L255, L321, L325, L406) depends on the `intent.md`/`spec.md`/`plan.md` chain or PR-review metadata that no project here produces, has no baseline, and the one transferable metric ("How often Claude repeats a mistake `CLAUDE.md` should have caught", L406) is already what the weekly maintainer's transcript scan hunts (`workbench:transcript-scanner`: "workflow mining, correction hunting, dangling-thread sweeps").

### A. The committed-artifact chain: REDUNDANT

Article, L95 and L115:
> "Each stage ends by writing one to version control (including `intent.md`, `spec.md`, `plan.md`, the diff and its tests, the PR with its review findings, and the incident record) and the next stage begins by reading it."
> "A stage ends by committing an artifact with the commit initiating the next stage."

Incumbents: `phased-harness/SKILL.md`, "**Files are the source of truth**, never conversation memory"; `fable-project-review/SKILL.md`, "The plan file is the only bridge between the two sessions, so it has to stand completely on its own"; `new-project`'s four documents; `pipeline-foundry` §10's seven-file scaffold. The incumbents are superior on three properties the article lacks: an unfilled artifact stops the pipeline (`CONFIG.template.md`: "Sessions **must stop and ask** if any value is `TBD`"; `new-project/SKILL.md`: "`scaffold.sh publish` refuses to push while any doc still contains its `<!-- SCAFFOLD-TODO -->` markers"), a verification section is mandatory (`conventions.md`: "A spec without it reliably produces confident false completion claims, because \"done\" has no definition"), and decisions carry their reason and date (SPEC.md §2). The article's `plan.md` "Proof" section (L308) is SPEC.md §6 by another name. See Routing collisions for the `spec.md` / `SPEC.md` problem.

### B. Verifier subagent: REDUNDANT

Article, L520 to L529 and L556:
> "Start the app with make run. Exercise the changed behavior and the two nearest neighboring flows. Report what you ran, what you saw, and any behavior that does not match plan.md. Do not fix anything; report only."
> "The verifier subagent ... is one way to package the final check by running a fresh context window once the session believes the work is done. This way the verdict is not colored by the assumptions that produced the code."

Incumbents: the installed `verification-kit:pre-delivery-verifier` agent ("Tools: All tools except Write, Edit, NotebookEdit"); `proof-of-work/SKILL.md` "Pairs with": "`verification-kit:pre-delivery-verifier` — runs this standard over an artifact before delivery, and cannot repair what it finds"; `model-effort-advisor/references/subagent-routing.md`: "**Review agent**, ideally a fresh context with no attachment to the build agent's choices, checks it against the success criteria before it's presented as done"; `phased-harness/templates/end-state.template.md`: "a fresh-context verification pass goes to `verification-kit:pre-delivery-verifier` ... Hand-authoring the prompt each time is how three separate sessions ended up with three different verifiers." The incumbent enforces "report only" at the tool layer rather than by the prose "Do not fix anything". Both permit `Bash`, so neither is airtight against a shell write, which is worth knowing but is not a point in the article's favor. The article's feedback-loop-versus-verifier distinction is already the `proof-of-work` (standard applied throughout) versus `pre-delivery-verifier` (final pass) split.

### C. Hooks as approval gates: INGESTIBLE FRAGMENTS

Article, L782 and L811:
> "A block should explain itself, so when a hook stops an action the reason and the route to approval appear in Claude's output."
> "exit 2 # exit 2 blocks the action; the message goes to Claude"

Incumbent: `/Users/gfm/.claude/CLAUDE.md` names the set ("Neither default touches the never-pre-authorizable set: pushes, credentials, deletions, and anything crossing into production") and the enforcement preference ("enforce it at the tool layer where possible"). `standing-authorization`'s stop-list is the file form of that set, but its tool classifies *questions*: "`check` classifies a question against the keywords in one file". Live check: `~/.claude/settings.json` has exactly one `PreToolUse` hook (the `Artifact` em-dash deny), none on `Bash`, and `permissions.allow` is empty. So today the never-pre-authorizable set is held by prose, by the auto-mode classifier, and by the ordinary permission prompt.

Fragment: the pattern only. A `PreToolUse` hook with `matcher: "Bash"` that exits 2 with a reason and a route to approval when the command is a push or a production write. Target `~/.claude/settings.json` (via the `update-config` skill; the global note on classifier blocks says a permission edit that *widens* autonomy gets blocked, and this one narrows it, but route the edit to Graham as a paste if it is blocked anyway). The existing em-dash hook already models "a block should explain itself" (its `permissionDecisionReason` names the rule and says "Remove them and retry").

Do not copy `production-gate.sh` (L805 to L815). Per the review and confirmed above: substring match on `deploy` and `production` misses `make release`, `terraform apply`, `git push`; MCP deploy tools bypass a `Bash` matcher entirely; and `$RELEASE_APPROVAL` is an environment variable in the same process tree as the agent, so the approval token is spoofable by the thing it gates. On a solo laptop the honest position is that the permission prompt on `git push` is already the gate; a hook adds value mainly for `--force`, deletes of tracked paths, and `terraform apply` outside a plan. Prove any hook by deliberate failure before trusting it.

### D. Managed settings, credential denies: INGESTIBLE FRAGMENTS

Article, L829 to L832 and L846 to L851 (the block), and L873:
> "`credentials` closes the gap the deny rules leave open. `permissions.deny` governs Claude's file tools, but a sandboxed shell command could still read `~/.ssh` or `~/.aws/credentials` by default; this block denies those reads and strips the named secrets from the environment of every sandboxed command."

Incumbent, `/Users/gfm/.claude/CLAUDE.md`, "Credentials and secrets":
> "Never handle raw credentials: not reading them, not writing them, not echoing them back."

`new-project/references/conventions.md`: "`.gitignore` patterns and the gitleaks hook are a backstop, not the control — the control is that credentials are never written down." Live check this pass: `~/.claude/settings.json` has **no** `permissions.deny` and no `sandbox` key. "Not reading them" is a prose rule with no tool-layer enforcement, on a machine whose global file says to enforce boundaries at the tool layer where possible.

Fragment: a `permissions.deny` list for `.env` files and secret directories, and (only after the key names are verified against the current settings reference) `sandbox.credentials.files` denies for `~/.ssh` and `~/.aws/credentials`. Target `~/.claude/settings.json`. Corrections before ingest: the article's `Read(.env*)` also matches `.env.example`, which `scaffold.sh` writes and expects Claude to edit, so use patterns that leave `.env.example` readable; verify `sandbox` availability on macOS before setting `failIfUnavailable: true` (L871 says Claude Code "refuses to start when the sandbox cannot initialize"). Not taken: `disableBypassPermissionsMode`, `allowManagedPermissionRulesOnly`, `allowManagedHooksOnly`, `disableSideloadFlags`, `strictKnownMarketplaces`, `requiredMinimumVersion` (MDM controls with no admin here, and the version pin decays); `"WebFetch"` and `Bash(curl *)` denies (this machine's skills fetch by design, `source-intake` Step 1).

### E. Parallel sessions and subagents: REDUNDANT

Article, L513 and L516:
> "The engineer splits the work into tasks that touch different files ... Tasks that share files run in a single session, one after another."
> "Turn repeated jobs into subagents, as defined in markdown files in `.claude/agents/` ... Check the definitions into git so the whole team shares them."

Incumbent, `/Users/gfm/.claude/CLAUDE.md`, "Concurrency and multi-agent runs":
> "Parallel write-capable subagents get **disjoint file subtrees**, each with an explicit do-not-touch list; git commands and shared files (catalogs, changelogs, trackers) stay with the orchestrator. Two agents appending to one tracker only worked by luck."

`phased-harness/SKILL.md` "Orchestration" and `sweep-harness/references/doctrine.md` ("Why per-item state files, never a shared tracker") carry the incident. `pipeline-foundry/SKILL.md` §12 adds a worktree trap the article omits: "Branches from the **default branch**, not parent HEAD". The library's installed agents (`verification-kit:pre-delivery-verifier`, `workbench:transcript-scanner`, `deploy-ops:deploy-loop-owner`) are the "repeated jobs as subagents" practice already in place. "Two or three sessions is a sensible starting point" (L515) is anecdotal.

### F. Skills as institutional knowledge: INGESTIBLE FRAGMENTS

Article, L414 and L431:
> "write a skill for institutional knowledge that must be applied consistently; don't write a skill for components that belong in `CLAUDE.md` or a prompt."
> "Test that the skill triggers. Ask Claude to do the relevant task in different ways and confirm the skill loads each time."

Incumbent, `/Users/gfm/skill-library/docs/authoring-standard.md`:
> "Write it like a router, not a summary: what the skill produces, when to use it, and the trigger phrases a user would actually say. Vague descriptions are the #1 cause of skills that never fire or fire wrongly. Spend review effort here first."

The rule of thumb is covered, and covered more precisely: `pipeline-foundry/SKILL.md` §3 gives a verified reason to prefer a skill over CLAUDE.md prose for constants ("verified on Claude Code 2.1.220 — the `Explore` and `Plan` subagents **do not receive CLAUDE.md**"). The one thing the standard lacks is a trigger test. It says to spend review effort on the description and to keep eval cases, but never says how to check that the router routes.

Fragment, target `docs/authoring-standard.md`, "The description is the router": "Before promoting a skill, test that it triggers: ask for its task three different ways in a fresh session and confirm the skill loads each time. A skill that fires on one phrasing is not routed, it is lucky."

### G. The CLAUDE.md play: REDUNDANT

Article, L367 to L371 (`/init`, cut down, check in, two-strike, "Keep it under a page"). Incumbent: the global "CLAUDE.md economy" section; `new-project/references/conventions.md` prescribes three sections with a stronger rule form: "**Hard rules** — numbered, imperative, each with the reason attached. The reason is what makes a rule survive contact with a situation its author did not foresee." and warns "A `CLAUDE.md` State section written as aspiration." `pipeline-foundry` §10: "Author every rule with its originating failure inline." The article's "Things Claude gets wrong" list (L393 to L395) is hard rules without reasons, which `conventions.md` calls out as the weaker form. The article's "Keep it under a page" is the economy rule without its justification ("every line loads into every session" is stated in both, so equal there).

### H. Plan mode as default, commit `plan.md`, sync hook: REDUNDANT

Article, L265, L287, L289. Incumbents: `new-project/SKILL.md` "the `plan-gate` skill applies to the *first real session*"; `phased-harness/templates/project-CLAUDE.template.md` "Phase `<READ-ONLY-PHASE-N>` is strictly read-only. Survey only ... Prefer plan mode."; `fable-project-review` verify mode ("mark **Done / Partial / Missed** with evidence") is the check of diff against plan; the global sweep rule ("Rewriting a load-bearing claim triggers a repo-wide sweep") is the discipline behind "update `plan.md` in the same commit". The article's plan-mode play maps to `anthropic-skills:plan-gate` (different marketplace, not an edit target). The product claim at L315, "Claude cannot edit files until the engineer accepts the plan", is to be verified in the installed version rather than in the docs (review currency item 7).

### I. Feedback-loop mechanics: REDUNDANT

Article, L574 ("wrap it in a single target such as \"make test\" ... that exits non-zero on failure"), L576 (quantifiable target), L578 (screenshot loop). Incumbents: `deploy-verify-fix/SKILL.md`'s "Not verification | Verification" table and "Diagnose from real output"; `capability-preflight/SKILL.md` "a probe must be able to report failure" (the non-zero-exit requirement, with the `|| echo "✓"` burn attached); `new-project` SPEC.md §6 "The concrete commands, and what their output should look like"; the memory note `browser-pane-verification-limits.md` for the screenshot loop's real traps (black below-fold screenshots, webfont layout). The article's "two or three rounds is normal" (L578) is anecdotal.

### J. CI/CD adoption order and MCP deploy allowlist: REDUNDANT

Article, L915 to L919 and L937. Incumbents: `deploy-verify-fix/SKILL.md` "Staging first, always ... **Promote the tested build; do not rebuild.**"; the global never-pre-authorizable set covers "the agent has no route to push to main"; `source-intake` already uses headless `claude -p` for a read-only judgment step, which is the article's step 1. "Expose deployment through MCP" has no consumer (this machine deploys static sites through `wrangler` and a git push, per `deploy-ops:cloudflare-pages-migration`).

### K. Claude Security scheduled scans: DISCARD

Enterprise-only public beta (L1045: Claude Enterprise, GitHub App, Claude Code on the Web, premium seats, admin switch); no entitlement here, and the transferable idea (scan on a schedule, route findings through review) has no vulnerability scanner on this machine to schedule. Secret scanning is already covered by `gitleaks` in `scaffold.sh` and `folder-to-repo`.

### L. Claude Tag on-call: DISCARD

Slack-only public beta (L1076) with no incident channel on this machine; its one durable idea, "writes the post-mortem to a version-controlled lessons file" (L1078), is the `retro` skill.

### M. Auto mode conditions: REDUNDANT

Article, L329: auto-accept "becomes the default for routine work: a tight `spec.md`, a small blast radius, and code the tests already cover." Incumbents: the global standing defaults and `standing-authorization`'s granted list with ceilings ("Every ceiling resolves to one stated value in one place"); `phased-harness` CONFIG standing authorizations. This session itself runs in auto mode. The article's three conditions are a reasonable gloss on "within ceilings" but add no rule.

### N. Dependency graph and "start with any clay play": DISCARD

Meta-structure for the article's own plays, self-contradictory per the review (Stage 1 needs a Stage 3 play); nothing to ingest.

### O. Intent capture in the originator's own words: REDUNDANT

Article, L141: "`intent.md`, a proto-spec in the originator's own terms. The artifact contains what is wanted, why, and under which constraints." Incumbent, `/Users/gfm/.claude/CLAUDE.md`, "Working with Graham": "Intent before execution ... restate in one line what Graham is trying to accomplish and why before choosing an approach. If the why is unclear and would change the approach, ask one question first." Backed by the memory file `ask-intent-before-executing.md` and by `pipeline-foundry` §1 ("Intent and outcome — what is being built, why, and what \"done\" looks like in verifiable terms"). The incumbent carries the audit that produced it (36 sessions, zero established intent up front).

## 5. Routing collisions

The article is not a skill collection, so no `description` collides. The collisions are in file conventions, if adopted alongside the incumbents:

- **`spec.md` versus `SPEC.md`: same name, different body, the worst case.** The article's `spec.md` (L234) is a per-change requirements-and-design document produced from one `intent.md`. `new-project`'s `SPEC.md` is the project-level arbiter: "The single source of truth. When another doc disagrees with it, this one wins." On the default case-insensitive macOS filesystem they are the same path. A project adopting the article's convention would overwrite the arbiter with a per-change design doc, and every generated `CLAUDE.md` ("`SPEC.md` is the single source of truth ... Read it before writing code") would then point an agent at the wrong document. Nothing would look wrong.
- **`plan.md` versus `improvement-plan-YYYY-MM-DD.md`**: distinguishable by name, but a prompt like "check the diff against the plan" would find whichever exists; `fable-project-review`'s verify mode expects its own dated file.
- **`verifier` agent versus `verification-kit:pre-delivery-verifier`**: a project-local `.claude/agents/verifier.md` (L518) would sit beside the installed agent in the agent list. For a prompt like "verify this before you call it done", the plugin-namespaced agent wins only if the session reaches for it by name; the bare `verifier` is the shorter match. The local one has the weaker contract (prose "report only" versus `disallowedTools`).
- **`evals/*.json` versus the `skill-creator` eval format**: adopting the article's loop creates a second eval format beside the one the authoring standard already names. One editable home.
- **`REVIEW.md`**: no collision, but a false expectation. It is not harness-loaded; a reader who writes it and expects `/code-review` or `fable-project-review` to pick it up gets nothing.
- **`intent/` folder and `intent.md`**: no incumbent uses the name; `KICKOFF.md` plays a different role (the paste block to start a session), so no misroute.

## 6. Philosophy conflicts

Contradictory advice, both sides quoted.

1. **Two sources of truth.** Article, L347: "**Linkage as the minimum bar.** All artifacts note the record ID and all legacy records contain the commit SHA of the markdown file. Linkage is a good place to start when transitioning to the AI-native SDLC, accepting that there are two sources of truth." Global CLAUDE.md: "an editable duplicate is drift, so flag it rather than silently keeping both. Promotion or migration is a move, never a copy." The article accepts, as a starting state, exactly what the incumbent classifies as the failure mode. (The article's own preceding sentence agrees with the incumbent; the sidebar then undercuts it.)

2. **Who approves behavior-config changes.** Article, L400: "changes to it are logged in git history, and code owners approve those changes in PR review." and L678: "the team that owns the configuration change approves it." Graham's standing ruling for the weekly maintainer (`memory/claude-improvements-weekly.md`): "Tier 2 (behavior changes, including global `~/.claude/CLAUDE.md` edits) are auto-applied with local commits". The article requires a human before a CLAUDE.md change lands; the machine's ruling lets it land locally and reserves the human for the push. The incumbent is deliberate ("This overrode the earlier handoff's \"Gate A stays mandatory\" decision"), so this is not an oversight to fix, it is a conflict to know about.

3. **Where corrections go.** Article, L370: every twice-made mistake "goes into `CLAUDE.md`". `rulings-harness/references/doctrine.md`: "Not a replacement for CLAUDE.md. Preferences stay there; only measured, falsifiable, or burn-derived findings move out." and `retro/SKILL.md` §3 routes a deterministic check to "A hook or CI, not prose" and a one-off to "The retro only, this is where it correctly dies." The article has one destination; the incumbents have five and treat CLAUDE.md as the last resort because "every line loads into every session". Same trigger, opposite default destination.

4. **Whether every session reads CLAUDE.md.** Article, L505, as a prerequisite for parallel work: "The `CLAUDE.md`, since all sessions read the file." and L371: "Claude reads all of it at the start of a session". `pipeline-foundry/SKILL.md` §3: "verified on Claude Code 2.1.220 — the `Explore` and `Plan` subagents **do not receive CLAUDE.md**, and no frontmatter field or setting changes that." The incumbent's claim is dated and version-pinned; the article's is unqualified. Anyone ingesting the article's "put it in CLAUDE.md and every session sees it" would ship constants to the one place the orienting subagents cannot see.

5. **Pre-approved production actions without a human.** Article, L985 and L1002: at 3σ Claude may act "by opening a PR into the review gate or triggering a pre-approved runbook", with `routes: [pull_request, runbook:rollback-deploy]`, and L1022: "the agent triggers the existing rollback pipeline." Global CLAUDE.md: "Neither default touches the never-pre-authorizable set: pushes, credentials, deletions, and anything crossing into production." `phased-harness` Gate B: "Never pre-authorizable, never covered by a standing authorization." A production rollback is a production write. The article's highest tier pre-authorizes what the incumbent says can never be pre-authorized.

6. **Auto-accept scope.** Article, L331: auto-accept "is fundamental to running the SDLC autonomously". Global CLAUDE.md, standing defaults: "An action approved once may be repeated without re-asking ... Re-ask only when the scope, target, or blast radius changes." The incumbent's autonomy is bounded by blast radius per action; the article's is a mode that Stage 6 assumes is on. Emphasis becomes contradiction only at Stage 6, where the article runs headless with the guardrails of Stages 3 and 4 assumed rather than proven.

## 7. Corrections needed at ingest

Factual and currency (verify before any of it is written down anywhere):

- "Claude Mythos 5" (L1031, L1045), `"requiredMinimumVersion": "2.1.193"` (L860), every managed-settings key in L827 to L861, and the two sandbox gap claims (L869, L873): all product state, none demonstrated. Use `verification-kit:fact-currency-check` before relying on any key name; a silently renamed key in a deny list fails open.
- L315, "Claude cannot edit files until the engineer accepts the plan": verify in the installed build, not the docs.
- L505 and L371, "all sessions read the file": contradicted by the library's own verified finding (Philosophy conflicts, item 4). Do not ingest the claim.
- L433, "Engineers pick up the new version automatically in their next session": `proof-of-work/SKILL.md` instance 1 (`anthropics/claude-code` issue #53948, "plugin install creates an empty `skills/` cache directory and reports success anyway") is a logged counterexample on this machine. Do not ingest as stated.
- "Reading time 5 min" (L24 to L26) for a roughly 9,000-word document.

Defective artifacts (do not copy; the pattern is ingestible, the code is not):

- `production-gate.sh` (L805 to L815): substring match, `Bash`-only matcher, environment-variable approval token in the agent's own process tree.
- `agent-evals.yml` (L651 to L674): no timeout, no concurrency cap, no cost ceiling, `result.json` overwritten per iteration so nothing is retained for the comparison over time that L678 promises.
- `Read(.env*)` (L830): also denies `.env.example`, which `scaffold.sh` writes.
- The prerequisites boxes: Stage 1 "None" (L147) needs a skill (L161); Stage 2 needs skills (L222) that are a Stage 3 play; Stage 2 "No engineering skill is required" (L226) needs a slash command and a merge-triggered job (L231).

Rules a stateless model cannot honor as written:

- "When Claude makes a mistake twice" (L370) needs memory of the first mistake across sessions. `retro` supplies it by reading the transcript; without that, the rule is unenforceable.
- "Once a month the tech lead tunes the setup" (L721), "Weekly is a sensible default" (L1051), "Dismissals tune the bands" (L988): cadences and feedback loops that assume a human owner and a tracker; on this machine the only equivalent is the Thursday maintainer.
- "Test that the skill triggers ... confirm the skill loads each time" (L431): honorable only with a fresh session per trial, which is why fragment F says so.

Style, against the library's conventions:

- 18 em dashes in the article (counted with `grep -o` on the U+2014 character); anything quoted into a skill or doc is restyled (global "Style: no em dashes"; the `Artifact` hook would also block a published page containing one).
- Fenced blocks written as second-person imperatives to an agent (L446 to L456, L527 to L529, L591 to L592, L729 to L742): data, not instructions, and quoted only as data in this analysis.
- Library rules for the targets: `fable-project-review`, `retro`, and `new-project` are incubator (edit on main, bump the host plugin version, CHANGELOG line). `docs/authoring-standard.md` is a doc, not a skill, but it is the contract the validator enforces, so a change there is a rule change and gets a CHANGELOG line. `~/.claude/settings.json` is edited through `update-config`; a permission edit blocked by the auto-mode classifier goes to Graham as a paste, not through repeated phrasings.
- Every rule added must carry its originating failure inline (`pipeline-foundry` §10; `conventions.md` "A good hard rule names the failure it prevents"). The article attaches a failure to none of its rules; the fragments above supply the local burn where one exists and say "structural fact" where one does not.

## 8. Net assessment: three things, in this form

1. **Fragment D, as a settings edit.** `permissions.deny` for `.env` (not `.env.example`) and secret directories, and `sandbox.credentials` denies for `~/.ssh` and `~/.aws/credentials` once the key names are verified current. Target: `~/.claude/settings.json`, via `update-config`. Why first: it closes a live gap between a rule loaded into every session ("Never handle raw credentials: not reading them") and a settings file with no deny list, using the enforcement the global file itself prefers. Effort S. Prove it by asking a throwaway session to `cat .env` and recording the block.

2. **Fragment 3a and 3b, as an edit plus a fresh hook.** Rule 6 in `new-project/scripts/scaffold.sh` `stub_claude` gains the red-test-first, commit, frozen-test procedure; `conventions.md` SPEC.md §6 gets the matching sentence; a `PreToolUse` hook on `Edit|Write` denying `tests/**` during a flagged fix task is written from scratch for the `python` archetype. Why second: the incumbents already say "do not weaken the check" and "prove the gate by deliberate failure"; this is the procedure that makes both structural for bug fixes, and every project here with a test suite consumes it. Effort S for the text, M for the hook (it must be proven by deliberate failure before it ships in the scaffold).

3. **Fragment 4a and 4b, as two one-paragraph edits.** `docs/authoring-standard.md` "Change hygiene" states that evals run on any change to a stable skill, hook, or CLAUDE.md and gate the merge; `retro/SKILL.md` §3 gains the "behavioral regression to eval case" row. Why third: the standard already promises evals and the library has none, so the prose sharpening is only worth doing if the first eval cases follow (`claude plugin eval`, not the article's `claude -p` loop). Effort S for the text; the evals themselves are separate work and the reason this ranks below the first two.

Below the line, all S and all real: fragment 9 (nit cap and CI-enforced exclusion in `fable-project-review` Phase 2), fragment F (trigger test in `authoring-standard.md`), fragment C (an explanatory `Bash` gate hook for pushes and production writes, pattern only). Item 6 (`bands.yaml`) is WATCH with a recheck when any project here has a metric with a rolling baseline. Everything else is already here, stated better, with the failure that produced it attached.
