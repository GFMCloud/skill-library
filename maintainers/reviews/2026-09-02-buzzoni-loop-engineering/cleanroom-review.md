# Review: "Claude Loop Engineering: How to Build an Agent That Works While You Sleep"

*Source: `sources/buzzoni-loop-engineering.md` — Mr. Buzzoni (@polydao), X Article, dated Jul 31 2026*

---

## 1. Executive summary

A well-organized conceptual guide to running Claude Code agents on triggers rather than on your typing. Its spine — trigger / work / gate / state / stop, and "the gate is the part that decides whether any of this works" — is sound and usable. The strongest content is structural: the four-layer stack (prompt → context → harness → loop), the local-vs-cloud execution table, and the argument that an author-agent cannot be its own critic. Evidence quality is the weak point: nearly every factual claim is a named-source assertion with no link, and the two flagship results (Karpathy, Shopify) are single anecdotes carrying a lot of narrative weight. A large fraction of the concrete instruction is product-surface detail — `/goal`, `/loop`, `/schedule`, `/workflows`, `/usage`, `CLAUDE_CODE_DISABLE_CRON`, minimum intervals — that is unversioned and must be re-verified against current docs before use. The commercial close ($3k–8k contracts, $95k→$300k title arbitrage, Telegram funnel) is unsupported and should be read as promotion, not analysis. Net: take the architecture, verify the commands, ignore the pricing.

---

## 2. Claims list with evidence status

### Origin story and named results

| # | Claim | Status |
|---|---|---|
| 1 | In March 2026 Andrej Karpathy pushed three files to GitHub, ~630 lines total | **asserted** — no link, no repo name |
| 2 | The three files held (a) the model, (b) a scorer, (c) a file-scope constraint | **asserted** |
| 3 | Within two days that setup ran ~700 experiments and surfaced 20 improvements | **asserted / anecdotal** |
| 4 | One improvement was a missing scalar in the attention path, missed by hand for two decades | **asserted / anecdotal** |
| 5 | "No linter catches that" | **asserted** |
| 6 | The prompt inside the loop was ordinary; the value was in the surrounding scaffolding | **asserted** (interpretation of #1–4) |
| 7 | Shopify's CEO ran an overnight setup on an internal model and got a 19% quality gain on a model half the size | **anecdotal** — no link, no definition of "quality" |
| 8 | June 2026: Peter Steinberger (author of OpenClaw) posted that you should design loops rather than prompt; post cleared 8M views | **asserted** |
| 9 | Boris Cherny, who leads Claude Code at Anthropic, said his job is now writing loops that prompt Claude | **asserted** — paraphrase, no quote or link |
| 10 | On June 7 Addy Osmani (Google Chrome) wrote it up and named it | **asserted** |
| 11 | Three independent people converging in one week indicates a real shift, not a fad | **asserted** (inference) |
| 12 | "Your subscription is probably running at ten percent capacity" | **asserted** — folklore; no basis given |

### Conceptual architecture

| # | Claim | Status |
|---|---|---|
| 13 | Prompt / context / harness / loop engineering stack rather than replace each other | **asserted** (definitional, but a real taxonomy) |
| 14 | Each layer fails on a different clock; loop failures compound longest before detection | **asserted** — plausible, unmeasured |
| 15 | Every working loop has exactly five parts: trigger, work, gate, state, stop | **asserted** |
| 16 | Without a gate, the agent reviews itself every cycle and approves itself | **asserted** — supported downstream by #22–24 |
| 17 | Without a state file, tomorrow's run starts from zero | **asserted** |
| 18 | Without a hard cap, the loop spends until a human notices | **asserted** |
| 19 | A real turn runs: discover → hand off → verify → persist → schedule | **asserted** (a procedure, not a finding) |

### Evaluator / self-review

| # | Claim | Status |
|---|---|---|
| 20 | Anthropic engineer Prithvi Rajasekaran found that agents asked to evaluate their own output praise it confidently even when quality is visibly mediocre | **anecdotal** — named source, no citation |
| 21 | The cause is structural: the writing context is full of arguments for the choices made, so on reread the agent sees its reasoning rather than the artifact | **asserted** — a mechanism story, untested |
| 22 | Pushing the generator to be harsher on itself failed | **anecdotal** |
| 23 | "Tuning a standalone skeptic is far easier than making an author self-critical" | **anecdotal**, generalized to a rule |
| 24 | Evaluator design: own instructions, different model where possible, acts on the artifact rather than reading it, assumes broken by default | **asserted** — prescriptive, no comparison data |
| 25 | Same base model as generator keeps the same blind spots | **asserted** |
| 26 | Rajasekaran wired his evaluator to Playwright MCP | **asserted** |
| 27 | `/goal` ships separation-of-concerns as a product primitive: a fresh model that took no part in production decides completion | **asserted** — checkable against docs |
| 28 | Banks have used maker/checker separation for decades | **asserted** (true as background, decorative here) |

### Product mechanics (Claude Code surface)

| # | Claim | Status |
|---|---|---|
| 29 | The Claude Code team sorts loops by what starts a run and what ends it, into four types | **asserted** |
| 30 | Turn-based loops improve when verification lives in a `SKILL.md` | **asserted** + reproducible template given |
| 31 | `/goal`: a small fast model reads the transcript after every turn, answers yes/no, returns a one-line reason used as next-turn guidance | **asserted** |
| 32 | One goal per session; a new goal replaces the old | **asserted** |
| 33 | `/goal` with no argument shows turns, tokens, and the evaluator's last reason | **asserted** |
| 34 | `/goal clear` ends it | **asserted** |
| 35 | The goal condition can run to 4,000 characters | **asserted** |
| 36 | The evaluator runs nothing itself — it can only judge what Claude surfaced in conversation | **asserted** — load-bearing for #37 |
| 37 | Objective conditions ("tests in test/auth pass, lint clean") survive many turns; subjective ones ("the code looks clean") fail on turn one | **asserted** |
| 38 | `/loop` runs on your machine; `/schedule` moves the same shape to the cloud | **asserted** |
| 39 | `/loop` reruns on a timer; `/goal` runs until a condition holds; confusing them breaks most loops | **asserted** |
| 40 | Cloud routine: no machine on, no session open, 1-hour minimum interval, fresh clone (no local files) | **asserted** |
| 41 | Desktop scheduled task: machine on, session closed, 1-minute minimum, sees local files | **asserted** |
| 42 | `/loop`: machine on, session open, 1-minute minimum, sees local files | **asserted** |
| 43 | Underneath is ordinary cron: five fields, one-minute granularity | **asserted** |
| 44 | `CLAUDE_CODE_DISABLE_CRON=1` turns the whole thing off | **asserted** — single-string, high-confidence-looking, unverified |
| 45 | `isolation: worktree` prevents two parallel agents writing the same file | **asserted** |
| 46 | `/usage` breaks recent spend down by skills, subagents, MCPs | **asserted** |
| 47 | `/workflows` shows per-agent usage and lets you kill any agent mid-run | **asserted** |

### Task selection and build order

| # | Claim | Status |
|---|---|---|
| 48 | Four conditions must all hold: weekly recurrence, automatic rejection, waste-tolerant budget, senior tooling | **asserted** |
| 49 | The loops that pay off first are CI triage, dependency bumps, lint-and-fix, flaky-test repro, issue-to-PR drafts | **asserted** |
| 50 | Architecture rewrites, auth, payments, prod deploys, vague product work should stay manual | **asserted** |
| 51 | If review capacity was already your ceiling, a loop lengthens the queue rather than shortening it | **asserted** — the sharpest unsupported claim in the piece |
| 52 | Build order matters: manual run → skill → state file → gate+cap → schedule → verifier subagent | **asserted** |
| 53 | Instructions pasted inside a cron job never get updated; a named skill does | **asserted** (rhetorical absolute) |
| 54 | Memory ends with the session; a repo file outlives it | **asserted** |
| 55 | Pairing `STATE.md` (position) with `VISION.md` (destination) prevents goal drift "around turn 47" | **asserted** — the number is rhetorical |
| 56 | Run the builder on a fast cheap model, the reviewer on a slower stricter one | **asserted** |

### Case studies

| # | Claim | Status |
|---|---|---|
| 57 | Osmani runs a morning triage loop: triage skill → isolated worktree per finding → drafting sub-agent → attacking sub-agent → connectors open PR / update ticket → ambiguous items to a human inbox → state file carries leftovers | **anecdotal** |
| 58 | Stripe runs an internal system called Minions, described publicly by engineer Steve Kaliski | **asserted** |
| 59 | More than 1,300 PRs merged weekly with nobody typing the code | **asserted / anecdotal** |
| 60 | It's triggered by tagging a bot in Slack or an emoji reaction | **asserted** |
| 61 | A deterministic orchestrator assembles context first (links, Jira, docs, Sourcegraph, MCP) before the model starts | **asserted** |
| 62 | A hard-coded lint pipeline runs after, and the agent cannot bypass it | **asserted** |
| 63 | Reliability came from constraints, not model size — Minions is a fork of open-source Goose | **asserted** |
| 64 | Those 1,300 PRs are still reviewed by engineers; humans moved from writing to reviewing | **asserted** |
| 65 | Anything a rule can decide should never go to a probabilistic model | **asserted** (generalized from #61) |
| 66 | "90% of Claude Code writes itself" and similar headline figures are mostly secondhand | **asserted** — but a commendable self-flag |
| 67 | Anthropic's own 8x merge-rate figure comes with the company calling it almost certainly an overstatement | **asserted** — no link |

### Costs, risks, security

| # | Claim | Status |
|---|---|---|
| 68 | Four unalerted bills: verification debt, comprehension rot, cognitive surrender, token blowout | **asserted** (a framework, not a finding) |
| 69 | The "Ralph Wiggum loop" — agent fires completion on a half-finished job — was named by Geoffrey Huntley | **asserted** |
| 70 | A reviewer with an opinion eventually argues itself into approval; only a zero/non-zero gate holds | **asserted** |
| 71 | Generated code merges faster than anyone reads it, so SAST + dependency audit + secret scanning belong inside the gate | **asserted** — good advice regardless |
| 72 | Auto-installed community skills carry whatever is in their descriptions | **asserted** |
| 73 | One audit of 17,022 skills found 520 leaking credentials | **asserted** — precise number, **no source at all**; treat as unverified |
| 74 | Verbose logging on long runs scatters secrets into unwatched logs | **asserted** |
| 75 | A write permission granted "just this once" is never reviewed again unless calendared | **asserted** |
| 76 | One person plus a stack of loops becomes a room where everyone agrees | **asserted** (rhetorical, but the piece's best warning) |
| 77 | The right metric is cost per accepted change | **asserted** |
| 78 | If fewer than half of a loop's changes survive review, you're doing the review work the loop was meant to remove | **asserted** — the 50% threshold is invented |

### Money

| # | Claim | Status |
|---|---|---|
| 79 | Small teams pay $3k–8k to have someone stand up CI triage, dependency automation, an overnight review loop | **asserted** — no market data |
| 80 | Retainers run $500–1,500/mo | **asserted** |
| 81 | Morning triage that ate 8 hrs/week falls to 2–3 hrs of reading diffs | **asserted / anecdotal** |
| 82 | "$95k developer" and "$300k AI architect" are often the same person eighteen months apart | **asserted** — pure folklore |
| 83 | The first loop runs on a $20 subscription; heavy overnight verification needs a real budget | **asserted** |
| 84 | On a consumer plan running heavy verification, spend arrives weeks before payoff | **asserted** — honest, and cuts against the sales pitch |
| 85 | Generation is now near-free; judgment stays scarce | **asserted** (thesis) |
| 86 | A loop's basis for picking is "looks reasonable," not "is correct" | **asserted** — the article's central and best argument |

**Tally:** ~86 checkable claims. Evidenced by the rubric's definition (data, citation, or reproducible procedure): essentially only the procedural ones — the `SKILL.md` template, the `STATE.md` template, the build order, the four commands, the `/goal` example. Roughly **6–8% evidenced, ~80% asserted, ~12% anecdotal.** Not a single external link supports a factual claim; the only three links in the piece are two product docs pages and claude.ai.

---

## 3. Techniques worth taking, quoted

These are stated concretely enough to act on.

**1. Put verification in a skill file, not in the prompt.**
> ```
> ---
> name: verify-frontend-change
> description: Verify any UI change end-to-end before calling it done.
> ---
>
> 1. start the dev server, open the edited page
> 2. click the new control, confirm the state change, screenshot before/after
> 3. browser console: zero new errors or warnings
> 4. run a performance trace, audit Core Web Vitals
>
> if any step fails, fix it and rerun from step 1
> ```
> "The more measurable those steps are, the less room Claude has to talk itself into finishing early"

**2. Write goal conditions a program could check, not a human could argue.**
> "So *all tests in test/auth pass and the lint step is clean* holds up across twenty turns. *The code looks clean* collapses on the first one."

Paired with the constraint that makes it necessary:
> "it can only judge what Claude surfaced in the conversation, because the evaluator runs nothing itself."

**3. Cap the goal explicitly in the command.**
> `/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries`

**4. Build in this order — the sequence is the technique.**
> "1. Make one manual run reliable... 2. Write that run down as a skill... 3. Add a state file. STATE.md at the repo root... 4. Put a gate and a cap around it. An objective check plus a turn limit. This is the step where the loop gains the ability to fail. 5. Then schedule it. /loop while you are still watching. /schedule once you trust it unattended. 6. Bring in a verifier subagent."

**5. Fire a named skill from the schedule, never pasted instructions.**
> "Have the schedule fire a named skill rather than a wall of pasted instructions, because instructions inside a cron job never get updated by anyone, ever."

**6. A copyable state-file shape.**
> ```
> # Loop state · ci-triage
>
> ## Last run
> 2026-07-28 03:30 UTC · 7 failures classified, 3 fixes drafted, 4 escalated
>
> ## In progress
> - claude/fix-auth-token-refresh - tests pass locally, awaiting CI
>
> ## Escalated to humans
> - src/billing/refund.ts - failing three ways, root cause unclear
>
> ## Lessons learned (write here, not in chat)
> - 2026-07-27: tests/e2e/checkout needs the Stripe webhook secret. skip if missing
> ```

**7. Split position from destination on long runs.**
> "pair the state file with a standing VISION.md. STATE.md holds the position, VISION.md holds the destination"

**8. Isolate parallel agents; asymmetric models.**
> "Give parallel agents `isolation: worktree` so two of them can never write the same file... Let the builder run fast and cheap, and hand the reviewer the slower, stricter model"

**9. A four-part go/no-go filter before automating anything.**
> "The task recurs at least weekly - check your calendar, not your intentions. / Something can reject bad output automatically - name the command that fails: npm test, tsc, the build. / The token budget survives waste... / The agent has senior tools"

**10. Make the evaluator act, not read.**
> "Rajasekaran wired his evaluator to Playwright MCP for exactly that reason. The verdict moves from 'the JSX looks fine' to 'I clicked login, it navigated, here is the screenshot.'"

**11. Put security scanning inside the gate.**
> "put SAST, dependency audit and secret scanning inside the gate."

**12. Measure one thing.**
> "Cost per accepted change... If fewer than half the changes your loop produces survive review, you are doing the review work the loop was meant to remove."

**13. Choose the runtime from the task's physics.**
> "Watching a local dev server every minute is only possible with /loop. Scanning open issues at 3 a.m. and opening PRs belongs in a cloud routine or a scheduled GitHub Action, because laptops get carried out of the house."

---

## 4. Rubric scores

**1. Evidence quality — 2/5**
Roughly 6–8% of claims meet the evidenced bar, and every one of those is a procedure the author wrote rather than a result anyone measured; the load-bearing empirical claims (Karpathy's 700 experiments, Shopify's 19%, Stripe's 1,300 PRs/week, the 17,022-skill audit) are named-source assertions with zero links, and the two most-cited product facts — `/goal`'s 4,000-character limit and the 1-hour cloud minimum — are stated as settled without a doc reference. Credit where due: §8's warning that headline figures like "90% of Claude Code writes itself" are secondhand shows the author knows the difference and chose not to apply the standard to his own numbers.

**2. Novelty — 3/5**
The four-layer stack, the maker/checker framing of `/goal`, "the evaluator sets what your loop refuses to produce," and above all "when review capacity was already your ceiling, a loop lengthens the queue instead of shortening it" are genuine, non-obvious framings that would change how someone scopes a project; against that, the build-in-order list, the four-conditions filter, and the closing "judgment stays scarce" are standard advice delivered with unusually good sentences.

**3. Actionability — 4/5**
A reader could start tomorrow with a real artifact: a `SKILL.md` template to copy, a `STATE.md` template to copy, a six-step order with a named first step ("make one manual run reliable"), four commands with example arguments, and a filter that tells them when *not* to start — held off 5 only because every command is unversioned and the reader must confirm each exists before the plan survives contact.

**4. Currency risk — 2/5** *(5 = durable; 2 = most product specifics need re-checking)*
The conceptual half (gates, state, evaluator separation, the layer stack) will age well, but claims #29–47 and #55 are entirely a snapshot of one tool's command surface at July 2026 — minimum intervals, flag names, what `/goal` with no argument prints, `CLAUDE_CODE_DISABLE_CRON=1`, `isolation: worktree`, whether `/workflows` and "auto mode" exist under those names — and a single renamed command silently breaks a scheduled loop at 3 a.m., which is precisely the failure the article itself warns takes a week to notice.

**5. Failure modes — 3/5** *(scoring how well the article protects a reader who follows it uncritically)*
Unusually self-aware for the genre — §9's four bills, §5's "keep these manual" list, and the security paragraph pre-empt most of what would go wrong — but three gaps remain live: the article never tells you to test that your gate can actually fail (a green-by-construction test suite satisfies every instruction here), it never bounds spend concretely despite naming token blowout as a bill, and the `$3k–8k` / `$95k → $300k` section invites a reader to sell this service to clients before they have run one loop themselves. See the failure list below.

### What breaks for an uncritical reader

- **A gate that cannot fail.** The whole architecture rests on "something with no taste that can reject the output," but nothing instructs the reader to verify their check ever returns non-zero. A test suite with no assertions, a lint config with everything disabled, or a build that succeeds on broken code turns the loop into an unsupervised writer with a rubber stamp — while presenting as correctly built.
- **Scheduling before trusting.** Step 5 says `/loop` while watching, `/schedule` once you trust it. A reader excited by "works while you sleep" will invert this. The article's own §1 says a bad loop "changes code at 3 a.m., feeds the error into the next run, and nobody notices for a week."
- **Unbounded spend.** Token blowout is named as a bill and the guard is "Per-run budget, daily budget, max retries, set before shipping" — but no mechanism, flag, or number is given for any of the three. A reader who follows the article literally has a turn cap and nothing else.
- **Commands that no longer exist as described.** Any of #29–47 being stale produces either an immediate error (recoverable) or, worse, a silently different behavior — e.g. a cloud routine that turns out to see no local files when the reader assumed it did, or a minimum interval that rejects their cron expression.
- **Evaluator theater.** The reader adds a second agent, same model, instructions that amount to "review this," and now believes they have separation of concerns. The article's own table calls this the "decorative evaluator," but the six-step build order lists the verifier subagent *last* and doesn't require the differentiation the table demands.
- **Automating a judgment task anyway.** The four conditions are a filter, but nothing forces the reader to actually apply it; the seductive examples (auth fixes, refunds, billing) appear in the article's own sample state file even while §5 says to keep auth and payments manual.
- **Selling the service too early.** §11 prices consulting work before the reader has evidence their own loop clears the 50% acceptance bar.
- **Copy-paste security surface.** "Auto-installed community skills bring along whatever sits in their descriptions" is a real warning, but the article gives no vetting procedure, and simultaneously teaches skill-driven scheduling.

---

## 5. Currency-risk list — re-verify before acting

**Highest risk (a stale value silently breaks an unattended loop):**

1. `/goal` exists and behaves as described — evaluator runs after every turn, returns a one-line reason fed forward (#31).
2. `/goal` with no argument reports turns, tokens, and last reason; `/goal clear` ends it (#33, #34).
3. One goal per session; a new goal replaces the old (#32).
4. The 4,000-character condition limit (#35).
5. The evaluator executes nothing and only sees what surfaced in conversation (#36) — **this is the single most load-bearing product claim in the article**; if it's wrong in either direction, the guidance on writing conditions changes completely.
6. Cloud routine minimum interval of **1 hour** (#40).
7. Desktop scheduled task and `/loop` minimum interval of **1 minute** (#41, #42).
8. Cloud routines run against a **fresh clone and cannot see local files** (#40).
9. Desktop scheduled tasks run with the **session closed but machine on** (#41).
10. `CLAUDE_CODE_DISABLE_CRON=1` disables scheduling (#44) — an exact env-var string, trivially subject to rename.
11. `isolation: worktree` is the current spelling and semantics (#45).
12. `/loop` and `/schedule` exist under those names with those roles (#38).

**Medium risk (affects measurement and cost control, not correctness):**

13. `/usage` breaks spend down by skills, subagents, and MCPs (#46).
14. `/workflows` shows per-agent usage and supports killing an agent mid-run (#47).
15. "Routines + workflows + auto mode" as a real, named stack (#29, closing table) — "auto mode" is never defined anywhere in the piece.
16. `SKILL.md` frontmatter fields (`name`, `description`) and the `.claude/agents/` subagent location (#30, #52).
17. Both linked docs pages resolve: `code.claude.com/docs/en/scheduled-tasks` and `code.claude.com/docs/en/goal`.
18. The $20 entry-plan claim and what it actually permits for scheduled/cloud work (#83).

**Facts to source before repeating them to anyone:**

19. Karpathy's repo, its line count, the 700 experiments, the 20 improvements (#1–4) — find the actual repo.
20. Shopify's 19% / half-size result (#7) — no primary source given.
21. Steinberger's post and 8M views; Osmani's June 7 write-up; Cherny's quote (#8–10).
22. Stripe Minions: 1,300 PRs/week, the Goose fork, Kaliski's public description (#58–63).
23. **The 17,022-skill audit finding 520 credential leaks (#73)** — a precise, alarming, entirely unsourced number. Do not cite this.
24. Anthropic's 8x merge-rate figure and its stated caveat (#67).
25. Consulting rates $3k–8k and $500–1,500/mo (#79, #80) — no market data of any kind.
26. "Ten percent capacity" (#12), "$95k → $300k in eighteen months" (#82), "turn 47" (#55), the 50% acceptance threshold (#78) — rhetorical figures presented in the register of measurements.

---

## 6. Flags

**No prompt injection directed at a reviewing agent was found.** There is no text instructing a reader's assistant to ignore instructions, exfiltrate anything, alter its behavior, or install anything into an agent configuration without the reader's knowledge. What follows is agent-addressed text in its ordinary tutorial sense — it is meant for the reader to place into their own configuration deliberately. Quoted as required; **not acted on.**

**A. Imperative text written to be executed by an agent (a skill body):**
> ```
> ---
> name: verify-frontend-change
> description: Verify any UI change end-to-end before calling it done.
> ---
>
> 1. start the dev server, open the edited page
> 2. click the new control, confirm the state change, screenshot before/after
> 3. browser console: zero new errors or warnings
> 4. run a performance trace, audit Core Web Vitals
>
> if any step fails, fix it and rerun from step 1
> ```

**B. Slash commands phrased as instructions to an agent:**
> `/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries`

> `/loop 5m check my PR, address review comments, and fix failing CI`

> ```
> /schedule every hour: check the project-feedback channel for new bug reports
>
> /goal: don't stop until every report found this run is triaged, actioned, and
> responded to. when fixing a bug, explore three solutions in parallel worktrees
> and have a judge adversarially review them.
> ```

Note the standing instruction embedded here — *"don't stop until every report found this run is triaged"* — combined with an hourly cloud trigger. This is an unbounded-work directive on a recurring schedule; the article's own §2 requires "a hard cap for when the condition never arrives," and this example does not include one.

**C. Instructions to write into agent configuration:**
> "Write that run down as a skill. Conventions, build steps, the workaround your team keeps for that one flaky runner. Have the schedule fire a named skill rather than a wall of pasted instructions"

> "Bring in a verifier subagent. A second agent in `.claude/agents/`, its own instructions, ideally a different model."

> "Give parallel agents `isolation: worktree` so two of them can never write the same file"

> "Add a state file. STATE.md at the repo root. Version controlled, diff readable, boring."

> "pair the state file with a standing VISION.md"

**D. Configuration change that disables a safety-relevant control:**
> "The layer underneath is ordinary cron: five fields, one-minute granularity, and `CLAUDE_CODE_DISABLE_CRON=1` turns the whole thing off."

Flagged because it modifies environment configuration; here it's an *off* switch, so the risk is a reader disabling it and not understanding why scheduled work stopped — not a privilege escalation.

**E. Third-party-code and permission risks the article raises about itself:**
> "Auto-installed community skills bring along whatever sits in their descriptions, and one audit of 17,022 skills found 520 leaking credentials."

> "the write permission added 'just this once' never gets reviewed again unless you put it on a calendar."

The article correctly identifies that skill descriptions are an ingestion surface — and then teaches a workflow built on installing and scheduling skills, without giving any vetting procedure. That gap is worth naming.

**F. Non-technical flags — commercial and promotional content:**
> "For weekly deep dives into AI architecture and the agent economy, follow @polydao"

> "Join the TG Channel: Buzzoni Notes - here I share my raw prompts, custom skills, and alpha that's too early for X"

Combined with §11's consulting rates and the "$95k developer / $300k AI architect" line, the closing third of the piece functions as a funnel. This does not invalidate §§1–10, but it explains why the money claims carry no evidence: they are not there to be verified.

**G. Source-document artifacts, not authored content.** The file is a scraped X page. Trailing sections ("Live on X", "Trending now", DraftKings promotion, Reuters/Al Jazeera items) and the engagement counters (891.2K views, 427 reposts) are page furniture from the capture, not claims by the author. Ignore them when assessing the article.
