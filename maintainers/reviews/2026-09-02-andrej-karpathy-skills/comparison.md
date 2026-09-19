# Comparison: `andrej-karpathy-skills` vs. the installed set

Candidate: `/private/tmp/claude-501/-Users-gfm-work/062312e6-0d60-4e62-a69d-6ebd96427e9c/scratchpad/src`, pinned at `2c606141936f1eeef17fa3043a72095b4765b9c2` (confirmed via `git rev-parse HEAD` in that checkout; the clone is shallow with one commit, `2c60614 Sync Chinese README with English version`).

Files read in full for this comparison: `skills/karpathy-guidelines/SKILL.md`, `CLAUDE.md`, `.cursor/rules/karpathy-guidelines.mdc`, `CURSOR.md`, `README.md`, `EXAMPLES.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, the clean-room review, `/Users/gfm/.claude/CLAUDE.md`, `foundry-core/skills/proof-of-work/SKILL.md`, `foundry-core/skills/evidence-report/SKILL.md`, `~/skill-library/docs/authoring-standard.md`, `~/skill-library/docs/inventory.md`. `README.zh.md` was not read line by line; the clean-room review's claim that it is a translation of `README.md` was spot-checked by diffing structure, not content.

## Ancestry: none found

Checked for shared history between the candidate and the installed library:

- `find`-driven `grep -ril "karpathy"` over `/Users/gfm/skill-library` and `/Users/gfm/.claude` (excluding this session's own working files) returns zero hits outside this task's own scratchpad output.
- `git log --oneline --all` in `~/skill-library` (33 commits shown) contains no merge note, PR title, or CHANGELOG line naming Karpathy, `forrestchang`, or `andrej-karpathy-skills`.
- No file in the installed set is byte-identical or near-identical to any candidate file; nothing in the library addresses "think before coding / simplicity first / surgical changes / goal-driven execution" as a named unit.

Independent origin. This is a straightforward "is it worth taking" comparison, not a post-fork reconciliation.

## Spot-checks of the clean-room review

The review's judgments were checked against the actual files rather than accepted on faith:

1. **3-way byte-identical duplication.** Confirmed by reading all three files directly: the body text of `SKILL.md`, `CLAUDE.md`, and `.cursor/rules/karpathy-guidelines.mdc` is identical section-for-section (numbered headings 1-4, same bullets, same bold thesis lines, same code-fenced plan template). The only deltas are the H1, the intro sentence, and the trailing "These guidelines are working if" block, exactly as the review states, and `SKILL.md` is indeed missing that trailing block.
2. **`EXAMPLES.md` is orphaned.** Confirmed: `.claude-plugin/plugin.json` lists `"skills": ["./skills/karpathy-guidelines"]` only, and none of `SKILL.md`, `README.md`, or `CURSOR.md` link to `EXAMPLES.md` by path.
3. **The stable-sort example is broken, and worse than the review says.** The review notes Python's `sorted` is stable and that the test's assertions hold under any tie order. Reading the actual code block turns up a sharper problem the review did not name: the "bug" function and the "fix" function in `EXAMPLES.md` lines 462-491 are the *same implementation* (`sorted(scores, key=lambda x: (-x['score'], x['name']))` in both), differing only by a docstring. The worked example does not show a fix being applied at all, on top of not reproducing a real bug.
4. **The `@lru_cache` on `async def` claim.** Confirmed at `EXAMPLES.md` lines 66-68: `@lru_cache(maxsize=1000)` decorates `async def search(...)`. This does cache the coroutine object rather than its result, and a second `await` on the cached object raises `RuntimeError`. The file marks this block wrong for the reason given (unrequested optimization) and never flags the correctness bug it also contains.
5. **Em dash usage differs across the three duplicate copies, unstated by the review.** `grep -n "—"` over the four prose files turns up zero em dashes in `SKILL.md`, `CLAUDE.md`, or `.cursor/rules/karpathy-guidelines.mdc` (they use plain hyphens: `"...present them - don't pick silently."`), but ten in `README.md` (e.g. `README.md:68`: `"...mention it — don't delete it"`). This matters directly for ingest, below.

Everything else in the review (frontmatter well-formedness, the §3/§4 test contradiction, the four-signal validation section, the flagged install/promotion content) was cross-read against the source files and matches.

## Classification

Per the task instructions, classified separately: the four principles, `EXAMPLES.md`, and the trailing success-signal line. `CLAUDE.md`, `CURSOR.md`, and the `.mdc` rule are not classified again as separate items since spot-check #1 confirms they carry the same four principles verbatim; they are addressed under Routing collisions and Corrections instead.

### Principle 1: Think Before Coding — REDUNDANT, and the redundant part is worse than the incumbent

> `SKILL.md:17-21`: "Before implementing: State your assumptions explicitly. If uncertain, ask. If multiple interpretations exist, present them - don't pick silently. If a simpler approach exists, say so. Push back when warranted. If something is unclear, stop. Name what's confusing. Ask."

Incumbent C (the harness system prompt) already governs this territory, and more permissively:

> "Interpret ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work. [...] Reserve blocking questions [...] for cases where proceeding under any assumption would be unsafe or would make the work useless if wrong."

`/Users/gfm/.claude/CLAUDE.md` ("Working with Graham" > "Intent before execution") covers the same ground for this machine specifically:

> "For any ad-hoc request [...] restate in one line what Graham is trying to accomplish and why before choosing an approach. If the why is unclear and would change the approach, ask one question first."

The candidate's "present multiple interpretations, don't pick silently" and "if something is unclear, stop [...] ask" apply to *any* ambiguity, not just ambiguity that changes the approach or is unsafe to guess at. Against C and against CLAUDE.md, this is not an equal restatement, it is a broader trigger for the same behavior, which C and CLAUDE.md deliberately narrowed after being burned by the opposite failure (see CLAUDE.md's "Standing defaults": "Build, verify, inspect, and search steps with no destructive side effect proceed without asking. Report what was run, do not request permission to run it."). One bullet, "If a simpler approach exists, say so. Push back when warranted," is a clean match for CLAUDE.md's "push back when a step looks wrong for his setup" and adds nothing beyond it.

**Does the candidate add any checkable directive beyond C?** No. Every bullet either restates C in a second voice ("state your assumptions" = C's "deliver the complete work under explicitly stated assumptions") or widens C's trigger condition without adding a new check.

**Since C cannot be edited: should anything on disk carry this principle?** No. Adopting it, even as a fragment, would put a standing instruction on disk that argues with an unrevisable system prompt every session. CLAUDE.md's narrower version already threads this needle (ask only when it changes approach or only Graham can supply the fact); duplicating the broader version anywhere would reintroduce the exact ask-loop failure mode the clean-room review documents (`alwaysApply: true` plus this description matches "essentially all coding work").

### Principle 2: Simplicity First — split verdict

> `SKILL.md:25-31`: "No features beyond what was asked. No abstractions for single-use code. No 'flexibility' or 'configurability' that wasn't requested. No error handling for impossible scenarios. If you write 200 lines and it could be 50, rewrite it."

The opening bullet is **REDUNDANT** against Incumbent C:

> "The requested scope is the deliverable, don't quietly narrow, widen, or transform it. [...] Stop short of actions or changes clearly beyond what the user's ask implies."

"No features beyond what was asked" restates this exactly; nothing on disk needs to carry it separately.

The remaining three bullets ("no abstractions for single-use code," "no unrequested flexibility/configurability," "no error handling for impossible scenarios") are **COMPLEMENT**. C governs the *scope of the task*; these bullets govern the *shape of code written within scope*, a genuinely different failure mode (code that never exceeds the ask but is still over-engineered inside it). No file read for this comparison, global CLAUDE.md included, states a general rule against speculative abstraction or unrequested configurability in code. **Gap:** no on-disk rule constrains code-level scope creep distinct from task-level scope creep. **Would anything consume it:** nothing currently would; there is no coding-hygiene skill in the inventory (`foundry-core` holds only verification skills: `proof-of-work`, `evidence-report`, `full-output-enforcement`). Per CLAUDE.md's own "CLAUDE.md economy" rule ("Write a project fact down only once it has cost a correction twice"), this should be banked rather than written into the global file preemptively, absent an actual recorded incident of over-abstraction.

The closing line, `Ask yourself: "Would a senior engineer say this is overcomplicated?"`, is weak on its own terms (the clean-room review's specificity score of 2/5 is fair: it outsources the criterion to an imagined third party) and is not a useful addition regardless of incumbent coverage.

### Principle 3: Surgical Changes — COMPLEMENT (the strongest item in the candidate)

> `SKILL.md:39-47`: "When editing existing code: Don't 'improve' adjacent code, comments, or formatting. Don't refactor things that aren't broken. Match existing style, even if you'd do it differently. If you notice unrelated dead code, mention it - don't delete it. When your changes create orphans: Remove imports/variables/functions that YOUR changes made unused. Don't remove pre-existing dead code unless asked."

The opening two bullets ("don't improve adjacent code," "don't refactor things that aren't broken") are redundant against Incumbent C's scope discipline, same reasoning as Principle 2's opening bullet. But the orphan-cleanup rule is **not** covered anywhere in the incumbent set:

> Candidate: "Remove imports/variables/functions that YOUR changes made unused. Don't remove pre-existing dead code unless asked."

This is checkable against a diff (did *this edit* orphan the symbol, or was it already dead before the edit), resolves a real tension between "leave the campsite cleaner" and "keep the diff reviewable," and appears in none of `/Users/gfm/.claude/CLAUDE.md`, `proof-of-work/SKILL.md`, or `evidence-report/SKILL.md`. "Match existing style, even if you'd do it differently" is likewise new: it is an explicit override of the model's own aesthetic prior, which none of the read incumbents state.

**Gap:** no on-disk rule distinguishes edit-caused dead code from pre-existing dead code, and no rule tells the model to defer to existing style against its own preference. **Would anything on this machine consume it:** nothing currently does; this is a genuine, low-cost, checkable addition with no home yet.

### Principle 4: Goal-Driven Execution — REDUNDANT, and inferior to the incumbent it duplicates

> `SKILL.md:55-57`: `"Fix the bug" → "Write a test that reproduces it, then make it pass"`; `"Add validation" → "Write tests for invalid inputs, then make them pass"`

`foundry-core/skills/proof-of-work/SKILL.md` covers this ground more rigorously:

> "Run the thing. Grep, lint, type-check, and self-review do not count as verification where the failure mode can hide from them. [...] Verify at the level the failure lives. A check that structurally cannot see the defect is not a check, however green it comes back."

and, critically, states the escape hatch the candidate lacks entirely:

> "When evidence cannot be produced [...] Say so, in those words, and put it in the not-verified list. Do not substitute reasoning about why it probably works."

The clean-room review already flags this exact gap ("§4 mandates tests with no escape hatch for repos with no test harness, or for UI/infra/one-off script work"), and it is independently confirmed: nothing in `SKILL.md`, `CLAUDE.md`, or the `.mdc` rule addresses what to do when a test harness does not exist. `proof-of-work` also covers non-code artifact classes (documents, deployments, data, config) that the candidate's test-only framing never reaches. `evidence-report/SKILL.md`'s CLAIM/CHECK/OUTPUT/VERDICT format is likewise a stricter reporting contract than anything in the candidate.

One narrow piece is not simply redundant: the pre-execution "state a brief plan" template,

> `SKILL.md:60-64`: "1. [Step] → verify: [check] / 2. [Step] → verify: [check] / 3. [Step] → verify: [check]"

is a forward-declared plan-with-verification-points, distinct from `evidence-report`'s backward-looking report format. It is thin (no falsifiable-assumption structure, no blocking-question cap) compared to `anthropic-skills:plan-gate` (Incumbent D), but plan-gate explicitly scopes itself to "real blast radius" work and "skip[s] it for typos, renames, and throwaway scripts," leaving ordinary coding tasks without a lightweight version of the same discipline. This narrow slice is a minor complement; the rest of Principle 4 is redundant and worse.

### `EXAMPLES.md` — COMPLEMENT, with defects serious enough to require rework before use

No incumbent read for this comparison provides worked before/after code examples illustrating over-abstraction, drive-by refactoring, style drift, or incremental verified delivery. That is genuinely uncovered territory: `proof-of-work` and `evidence-report` state the standard and the report format but carry no example gallery, and none of the `frontend-design` or `workbench` skills address code-level editing hygiene at all.

**Gap:** no incumbent has a worked-example reference for coding-hygiene anti-patterns. **Would anything consume it:** nothing does today; it would only become useful if Principle 2/3's complement content above is ever built into a real skill, at which point selected examples (the discount-calculation over-abstraction example, the drive-by-refactor diff, the style-drift diff, the incremental rate-limiting plan) could serve as its `references/` material.

This is not a clean take, though. The file is unreferenced by its own repo (spot-check #2), and its single most on-topic example (Test-First Verification, meant to demonstrate "reproduce the bug before fixing it") is factually broken in a way that actively teaches the wrong lesson: the "bug" it claims to reproduce cannot occur under Python's stable sort, and the "before" and "after" code are identical (spot-check #3). Any ingestion of this file must delete or rewrite that example first; it is not safe to carry forward as-is.

### The "These guidelines are working if" success-signal line — REDUNDANT, superseded by a stronger incumbent mechanism

> `CLAUDE.md:65` / `.mdc:70`: "These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes." (`README.md:144-147` expands this to four bullets, identically unmeasured.)

`~/skill-library/docs/authoring-standard.md` already specifies a stronger, checkable mechanism for the same question (is a behavioral change actually working):

> "Behavior testing: for stable skills keep 2-3 eval cases and run them on change (the official `skill-creator` plugin provides evals and version comparison). Reviewing prompt diffs alone tells you almost nothing about behavior."

The candidate's line is four subjective impressions with no baseline, no measurement method, and no test case, exactly the "reviewing prompt diffs" approach the authoring standard names as insufficient. The incumbent mechanism is superior on its own terms (a concrete artifact, re-runnable, versioned) rather than merely different in emphasis. Nothing on disk needs this line; where the library wants to know if a change is working, it already has a better answer.

## Routing collisions

No literal name collision exists: no skill in `~/skill-library/docs/inventory.md` is named `karpathy-guidelines`, so the worst case (identical name, different body) does not occur here.

A real collision would occur on **description overlap** if the candidate were installed via its own recommended path (`/plugin install andrej-karpathy-skills@karpathy-skills`, per `README.md:104-111`). Its description:

> `.claude-plugin/plugin.json`: "Behavioral guidelines to reduce common LLM coding mistakes, derived from Andrej Karpathy's observations on LLM coding pitfalls" / `SKILL.md`: "Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria."

matches essentially all coding work, with no negative scope and no stated cost, which `authoring-standard.md` names directly as the failure mode to avoid:

> "Say what the skill is not for and what it costs [...] alongside what it does; a description with no negative scope routes neighbouring requests to it."

Under this description, a routine "fix this bug" request would compete for `karpathy-guidelines` (fires on "refactoring code") and for `proof-of-work` (fires on "before declaring any artifact complete"). Neither wins outright since the router matches on relevance, not priority, so the practical effect is duplicate, mildly inconsistent verification guidance loaded for the same task: the candidate's thinner "write a test, make it pass" against `proof-of-work`'s fuller standard with its escape hatch. No precedence between them is declared anywhere the way `/Users/gfm/.claude/CLAUDE.md` declares `dataviz` vs. `visualize` precedence, so which one the model leans on for a given phrasing is unpredictable.

A second, worse collision would occur at the file level rather than the router level: if Graham followed `README.md`'s Option B verbatim,

> `README.md:122-126`: `echo "" >> CLAUDE.md` / `curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md`

against `/Users/gfm/.claude/CLAUDE.md`, the appended "If something is unclear, stop [...] Ask" text would sit in the same file as, and textually contradict, the existing "Intent before execution" section a few hundred lines above it. That is not a routing ambiguity, it is a self-contradicting instruction file, and the append command is itself unguarded (run twice, it duplicates the block).

## Philosophy conflicts

One genuine contradiction, not merely a difference of emphasis, between the candidate's Principle 1 and both Incumbent C and the installed CLAUDE.md:

> Candidate, `SKILL.md:18-21`: "If multiple interpretations exist, present them - don't pick silently. [...] If something is unclear, stop. Name what's confusing. Ask."

> Incumbent C: "Interpret ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work. [...] Reserve blocking questions [...] for cases where proceeding under any assumption would be unsafe or would make the work useless if wrong."

> `/Users/gfm/.claude/CLAUDE.md` ("Standing defaults"): "Build, verify, inspect, and search steps with no destructive side effect proceed without asking. Report what was run, do not request permission to run it."

The candidate's default is stop-and-ask on any unclarity or any multiple interpretation; the incumbents' default is proceed-and-flag, escalating only when the choice is materially consequential or unsafe. These cannot both be followed as written on the same task: a model given "make it work" style requests will either silently pick (satisfying C and CLAUDE.md, violating the candidate) or ask (satisfying the candidate, violating C and CLAUDE.md's explicit anti-permission-loop stance). The candidate's single mitigating clause, `SKILL.md:11`: "For trivial tasks, use judgment," does not resolve this, since "trivial" is undefined and the harness's threshold ("materially different work") is a different and better-specified test.

No other candidate/incumbent pair produces a direct contradiction; the rest of the overlap is coverage difference (candidate thinner or narrower) rather than opposite advice.

## Corrections needed at ingest

- **Factual error, must-fix before any use:** `EXAMPLES.md`'s Test-First Verification example (lines 456-494) claims a non-existent non-determinism bug in Python's stable sort, and its "before" and "after" implementations are identical code. Delete or rewrite before this file is cited from anywhere.
- **Rules a stateless/headless model cannot honor:** `SKILL.md:21`, "If something is unclear, stop. Name what's confusing. Ask," and `:19`, "If multiple interpretations exist, present them - don't pick silently," both presuppose an interactive human on the other end. They cannot be honored by a subagent, a background task, or a `claude -p` headless run, exactly the run modes `/Users/gfm/.claude/CLAUDE.md`'s "Concurrency and multi-agent runs" section is written around. If any fragment of Principle 1 were ever ingested despite the net assessment below, this would need an explicit "if nobody can answer, state the assumption and proceed" clause first.
- **Style violation against the library's own no-em-dash rule:** confirmed by direct grep, `README.md` uses ten em dashes (e.g. `README.md:68`: "mention it — don't delete it") where the byte-identical content in `SKILL.md`/`CLAUDE.md`/`.mdc` uses plain hyphens for the same sentence. Any text pulled from `README.md` specifically (rather than the other three files) needs em dashes stripped per `/Users/gfm/.claude/CLAUDE.md` ("Style": "No em dashes in any written content you produce or edit").
- **Frontmatter shape against `authoring-standard.md`:** the candidate's `SKILL.md` frontmatter has only `name`, `description`, `license`, no `metadata:` block. The library's standard frontmatter always carries `metadata: {maturity, version, reviewed}`; anything ingested as a library skill would need that block added (at minimum `maturity: incubator`), and the description rewritten to state negative scope and cost per the router-quality rule quoted above.
- **Unverifiable, single-source citation:** the sole authority for all four principles is one X/Twitter post (`https://x.com/karpathy/status/2015883857489522876`), cited identically in three files, not independently fetchable (confirmed: the clean-room reviewer could not retrieve it either, and this task did not attempt to since the URL is untrusted external content encountered inside candidate files). If any fragment is ingested, attribute it as an informal, unverified practitioner observation, not a settled reference.
- **Not an ingest correction but worth surfacing to Graham, per the clean-room review's own flags section:** `README.md:122-126`'s CLAUDE.md-append command is unguarded against being run twice, and the repo requests plugin-marketplace installation and contains third-party self-promotion (`README.md:3-5`). None of this was acted on; it is quoted above only where it bears on the append-collision risk.

## Net assessment

If only three things could be taken:

1. **The orphan-cleanup asymmetry and "match existing style," as a two-bullet fragment, not the whole principle.** `SKILL.md:45-47` plus `:42` ("Remove imports/variables/functions that YOUR changes made unused. Don't remove pre-existing dead code unless asked." / "Match existing style, even if you'd do it differently.") This is the single most novel, cheapest, most checkable rule in the repo, confirmed to have no incumbent equivalent anywhere read for this comparison. Target: `/Users/gfm/.claude/CLAUDE.md`, as a new short bullet in the "Working agreements" section, the same shape as the existing "Edit the generator, never the output" rule. Per the file's own "CLAUDE.md economy" rule, this should be added once, or held as a noted candidate until an actual correction incident justifies the line, rather than added purely on this review's say-so.

2. **The concrete anti-overengineering bullets from Simplicity First, minus the circular "senior engineer" framing.** `SKILL.md:27-30` ("No abstractions for single-use code. No 'flexibility' or 'configurability' that wasn't requested. No error handling for impossible scenarios.") This is genuine complement territory with no current owner. Target: a new incubator skill in `foundry-core` (alongside `proof-of-work` and `evidence-report`, which already own the verification pillar) rather than the global CLAUDE.md, since it is coding-task-specific and would otherwise load every session regardless of task type; write its description with explicit negative scope from the start, per `authoring-standard.md`.

3. **The step-to-verify plan template, as a cross-reference, not a new file.** `SKILL.md:60-64`'s numbered "`[Step] → verify: [check]`" format is the one part of Goal-Driven Execution not already redundant against `proof-of-work`/`evidence-report`, since it is a pre-execution plan format where those two are post-execution report formats. Target: add a short "before you start" pointer to it in `proof-of-work/SKILL.md`'s "Pairs with" section, as a stable-skill change (version bump, CHANGELOG line, per `authoring-standard.md`'s change-hygiene rules), rather than installing the candidate's own file.

Explicitly not among the three: Principle 1 (net negative once C is accounted for; nothing on disk should carry it, per the reasoning above), the trailing success-signal line (superseded by the library's eval-case discipline), and `EXAMPLES.md` as a whole (real value trapped behind an orphan status and a factual error that must be fixed first; worth returning to only once principle 2/3's complement content actually has a skill to illustrate).
