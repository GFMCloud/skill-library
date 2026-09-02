# Standalone review: "Your AGENTS.md is holding you back" (PostHog / Jina Yoon, X article, 1:01 PM · Aug 31 2026)

## 1. Executive summary

A vendor newsletter post arguing that context engineering has inverted — from adding context models lacked to subtracting context that now gets in their way — followed by three maintenance tactics: run `/doctor` plus a manual pass, build evals for your context file, and ask agents to report what context they wished they had.
The tactical half is unusually well-sourced for a social post: real PR links, repo permalinks, a quoted tool output, and a specific incident with hours attached.
The thesis half is not: "subtract as much as you can" rests entirely on two vendor blog/doc links and two named-person anecdotes (Cherny, Theo), with no before/after measurement anywhere in the piece.
Nothing in the article measures whether trimming context improved agent behavior — only how many tokens it saved.
The strongest idea is the third one: instrument the agent to report context gaps, then **cluster and verify before acting on them**, because the reports are not trustworthy on their own. That verification step is what separates this from generic advice.
The weakest is the heuristic in the first Try-this box, which invites deleting correct preventive context.
Internal tension worth noting: the article's own headline incident is a *stale/wrong context* failure, not a *too much context* failure, and it does not support the subtraction thesis it is placed under.
Currency risk is high throughout — CLI version numbers, model generations, framework versions, and a claimed 80% prompt reduction all pin to a moving product state.

## 2. Claims list with evidence status

**Thesis claims**

| # | Claim | Status |
|---|---|---|
| 1 | Context engineering "used to focus on adding information that base models lacked" | asserted (illustrative image + self-link) |
| 2 | "the same context your agents couldn't function without [can make them perform worse]" | evidenced-by-citation (links OpenAI "favor leaner prompts" guide for gpt-5.6); no data in-article |
| 3 | Anthropic "removed 80% of Claude Code's system prompt" | evidenced-by-citation (links claude.com context-engineering blog); the figure is not shown or derived here |
| 4 | "Labs are going back on previous advice about rules and repetition; judgment, interfaces, and progressive disclosure are the new best practices instead" | asserted |
| 5 | "The goal of context engineering has since shifted toward subtracting as much information as you can" | asserted (this is the load-bearing claim and it carries no measurement) |
| 6 | "figuring out exactly what to subtract isn't easy when dealing with unpredictable behavior" | asserted |
| 7 | Boris Cherny "recommended deleting your CLAUDE.md every six months to stay on the bleeding edge" | evidenced-by-citation (YouTube link); anecdotal as evidence for the thesis |
| 8 | Theo "recently reported it was worth rewriting his AGENTS.md by hand" | anecdotal (linked post + screenshot) |

**PostHog's own experience**

| # | Claim | Status |
|---|---|---|
| 9 | Their AI onboarding wizard "often landed on the wrong project in monorepos because our scripts pointed to root by default" | anecdotal |
| 10 | They changed it so "headless runs take advantage of model recommendations" | evidenced (PostHog/wizard PR #884) |
| 11 | Models are now "good at inferring repo structure" | asserted (the premise of the fix, never measured) |
| 12 | `/doctor` "runs basic health checks, deletes redundant prompts, catches broken settings, finds unused plugins, and optimizes for lazy loading" | evidenced-by-citation (deep-link to docs pinned at v2.1.198) |
| 13 | The report "prints a summary of how often you've used each file, and how much it can trim" | evidenced (verbatim output block quoted) |
| 14 | posthog.com/AGENTS.md is ~1,780 resident tokens, verdict "trim ~350" | evidenced (quoted output) |
| 15 | Across the repo it suggested disabling 3 plugins + 3 skills, saving ~6K tokens/session on average | asserted (no output shown for this one) |
| 16 | `/doctor` "doesn't check for correctness; it acts only based on what it can derive from your code" | asserted (plausible, undemonstrated) |
| 17 | A stale merge-queue line left agents with wrong instructions for 21 hours; one PR stuck 10 hours; another engineer lost 45 minutes | anecdotal (single incident; the fix PR #75873 is linked, the durations are not) |
| 18 | `/doctor` could not have caught it "since merge queue state lives in a GitHub setting rather than in code" | asserted (follows from #16 if #16 holds) |
| 19 | They record wizard gotchas as framework-specific commandments in `commandments.yaml` | evidenced (file linked) |
| 20 | The three quoted commandments (Next 15.3+ `instrumentation-client.ts`; Phoenix/Plug ordering; `posthog-rs` crate + `posthog_rs::client(options).await`) | asserted (external technical facts, unverifiable in-article) |
| 21 | wizard-ci runs the wizard on ~40 sample apps, opens one PR each, and a `pr-evaluator` agent grades diffs + session logs and posts metrics | evidenced (two service repos + a filtered PR list linked, screenshot) |
| 22 | These reports caught the wizard "skipping installing PostHog entirely because the model determined it was already complete" | evidenced (screenshot + linked closed PRs) |
| 23 | The wizard is "our biggest conversion path" | asserted (self-link) |
| 24 | The wizard's final instruction asks the agent what guidance would have helped | evidenced (commit-pinned source permalink + quoted prompt) |
| 25 | This "gives us a rich feed of live bug reports for cheap – a basic form of AI observability" | anecdotal |
| 26 | "we can't trust agents at face value" so they cluster and verify before acting | asserted (and, notably, the one place the article argues against its own tooling) |
| 27 | Half the "other" cluster is confirmation messages ("succeeded on the first attempt", "posthog-js already installed"); the other half is an unclusterable long tail | asserted (chart is an image; the split is stated in prose only) |
| 28 | A subagent reproduced the notebook create schema/tool failure before the fix landed | evidenced (context-mill PR #272) |
| 29 | Their monorepo PR template prompts agents to name skills invoked | evidenced (commit-pinned permalink to line 53) |
| 30 | Other agents have used that information to catch and fix skill inconsistencies | anecdotal (one PR, #81018) |
| 31 | "This approach works best at scale" | asserted |

Tally: of 31 claims, ~11 are evidenced by an artifact you can open, ~6 are evidenced only by pointing at someone else's blog, ~6 are anecdotal, ~8 are bare assertions. The evidenced ones are almost all *implementation* claims ("we built X"); the *efficacy* claims — that subtracting improves results — are the unevidenced ones.

## 3. Techniques worth taking, quoted

1. The deletion heuristic (use with the caveat in §5):
   > "Run claude doctor after each upgrade and follow up with a manual pass on your AGENTS.md. For each line, if you can't name the failure it prevents, delete it."

2. The cheapest real technique in the piece — a regression suite for prose:
   > "The next time your agent makes a mistake, paste the prompt that caused it into a failures.md. Re-run those prompts the next time you edit or delete parts of your AGENTS.md as a quick test suite for your highest-cost piece of context."

3. A copyable end-of-run prompt, quoted from their production wizard:
   > "What information or guidance would have been useful to have in the integration prompt or documentation for this task? Specifically anything that would have prevented tool failures, erroneous edits, or other wasted turns."

4. The full CI loop, reproducible in outline if not at scale:
   > "1. wizard-ci runs the PostHog Wizard on all ~40 sample apps and creates one PR for each. 2. Those PRs don't get merged. Instead, a second agent called the pr-evaluator grades each of them based on the diffs and session logs. 3. The pr-evaluator leaves metrics and reports on the trigger PR and the wizard-ci PR."

5. The scaled-down version of #4, which is the actually portable form:
   > "test your context by saving prompts that check if your agents are doing what you want them to do."

6. Verification before action — the best-judged step in the article:
   > "since we can't trust agents at face value, we cluster and verify the underlying issues first"
   > "Once the loop identifies a meaningful cluster, it deploys subagents to verify the issue before attempting a fix."

7. Attribution via PR template:
   > "We do this in our posthog monorepo PR template, which prompts agents to name any skills invoked."

8. Third-hand, but concrete and easy to schedule:
   > "recommended deleting your CLAUDE.md every six months to stay on the bleeding edge"

## 4. Rubric scores

**1. Evidence quality — 3/5.** Implementation claims are backed by openable artifacts (PRs, repo files, commit-pinned permalinks, one verbatim tool output), which is well above the norm for the format; but every efficacy claim — that subtraction improves agent behavior — is carried by two vendor links and two named anecdotes, and the only outcome number offered is tokens saved, not quality gained.

**2. Novelty — 3/5.** "Trim your context file" and "run the built-in doctor" are restatement; the non-obvious contribution is treating agent self-reports as a noisy telemetry stream — cluster them, then dispatch a subagent to reproduce the issue before changing anything — which is a real idea and is shown working, but it occupies roughly a third of the piece.

**3. Actionability — 4/5.** Three "Try this" boxes, one prompt you can paste verbatim tonight, and a `failures.md` practice with essentially zero setup cost; the flagship system (~40 sample apps, two CI services, a self-driving context mill) is not reproducible at reader scale, and the article says so.

**4. Currency risk — 2/5 (high risk).** At least six load-bearing statements are pinned to a product or version state: `/doctor`'s feature list is deep-linked to "v2.1.198 or later", the 80% figure is tied to one blog post about one model generation, the leaner-prompts guidance is tied to a gpt-5.6 doc page, "most coding agents have a built-in /doctor command" is the shakiest of them, and the SDK commandments name Next 15.3+, a Plug integration path, and a specific `posthog-rs` constructor signature.

**5. Failure modes — 3/5.** The article warns about agent self-reports but not about its own deletion heuristic, and a reader following it uncritically will delete correct context and re-learn why it was there (see below).

### What goes wrong for an uncritical reader

- **The deletion heuristic inverts the burden of proof.** "If you can't name the failure it prevents, delete it" deletes exactly the preventive lines whose value is invisible *because they are working*. Absence of a remembered failure is not evidence of no failure. A safer form: if you can't name the failure it prevents, write a check for it — then delete it if the check passes without the line.
- **The article's own case study argues against its framing.** The 21-hour merge-queue incident was a *stale* line, not a *superfluous* one. It is filed under "subtract more" but it actually demonstrates that context needs a freshness owner and an expiry review — a different remedy. A reader who reads it as support for aggressive trimming has drawn the wrong lesson from the strongest evidence in the piece.
- **Trusting `/doctor` to "delete redundant prompts."** A tool credited with deleting things should be run somewhere reviewable — a branch, a diff, a checked-in file — not against a working tree you then commit unread. The article does not say to diff the result.
- **Token savings treated as a quality metric.** "~6K tokens per session" is a cost number. Nothing in the article connects it to better outputs, and a reader optimizing that number will happily trim their way into the failure mode above.
- **Asking agents what context they wanted, without the verification step.** Section 3 is safe only because of the cluster-then-reproduce discipline. The "Try this" box compresses it to "ask them for feedback… turn verified reports into a self-driving context system" — a reader who skips straight to a feedback-driven loop will be editing their AGENTS.md from confabulated complaints, and the loop will amplify them.
- **Copying the commandments verbatim.** The three quoted lines are version- and API-specific integration instructions for one vendor's SDKs; pasted into an AGENTS.md they become exactly the kind of stale, unowned line the article's own incident is about.
- **Eval cost.** "Test your context like it's code" at the article's scale means ~40 sample apps, a CI service, and a second grading agent. The `failures.md` fallback is the honest version; a small team that attempts the full thing will spend more on the harness than the context is worth.

## 5. Currency-risk list — re-verify before acting

1. **`/doctor`'s capability list** — the source link is anchored to "v2.1.198 or later". Whether it still deletes redundant prompts, finds unused plugins, and optimizes lazy loading, and whether the output block still looks like the one quoted (`Est. resident tokens`, `Verdict: trim ~350`), needs checking against your installed version.
2. **"Most coding agents have a built-in /doctor command"** — the most generalized claim in the piece and the least supported; verify for whichever agent you actually run.
3. **"removed 80% of Claude Code's system prompt"** — a point-in-time figure about one model generation, sourced to a vendor blog. Do not carry the number forward.
4. **"Favor leaner prompts"** — cited from a doc page parameterized to `model=gpt-5.6`. Prompting guidance is per-model and has already reversed once, which is the article's own thesis.
5. **"models are good at inferring repo structure"** — the premise behind removing their monorepo path defaults. True enough for their case at the time; test it on your repo before removing your own scaffolding.
6. **Cherny's "every six months"** — a cadence quoted from a video, tied to how fast models were moving then.
7. **The three commandments** — Next.js `instrumentation-client.ts` for 15.3+, `PostHog.Integrations.Plug` before the router, and `posthog_rs::client(options).await`. All three are SDK-version-sensitive; the Rust constructor signature in particular is the kind of thing that changes between crate releases.
8. **All linked artifacts** — the wizard-workbench services, `context-mill` layout, and the PR template line anchor. Two of the links are commit-pinned (good, they will not rot silently); the repo-tree links are not (`wizard-ci`, `pr-evaluator`, `commandments.yaml` on `main`) and may have moved.
9. **The feedback-cluster chart** — explicitly "the last month" as of Aug 31 2026, and the "half is confirmation messages" split is stated in prose only, not visible in the image.

## 6. Flags

**Not acted on.** The following are addressed to an agent rather than to the reader, or instruct writing content into agent configuration. Quoted for the record only.

Agent-directed instruction shown as an AGENTS.md line:
> "All merges into master go through the Trunk merge queue. Never run gh pr merge."

Agent-directed SDK installation instructions, presented as entries in a checked-in context file (`commandments.yaml`) that is fed to agents:
> "For versions 15.3+, initialize PostHog in instrumentation-client.ts for the simplest setup."
> "For Phoenix or Plug apps, add PostHog.Integrations.Plug before the router so request context is attached to captured events and errors"
> "posthog-rs is the Rust SDK crate; add it with cargo add posthog-rs and construct the client with posthog_rs::client(options).await."

A production prompt directed at an agent, quoted for the reader to install into their own agent's instructions:
> "What information or guidance would have been useful to have in the integration prompt or documentation for this task? Specifically anything that would have prevented tool failures, erroneous edits, or other wasted turns."

Instructions to install agent-directed content by default, and into repo config:
> "Many developers already do this to update their skills, but you can take it further by putting it in your prompts by default."
> "We do this in our posthog monorepo PR template, which prompts agents to name any skills invoked."

Also quoted from the reused context-mill instructions:
> "reuse event names the project already uses"

**Additional non-rubric flags:**

- **Commercial framing.** This is a vendor newsletter post promoting PostHog's own products. Every internal link carries `utm_source=posthog-newsletter&utm_medium=post&utm_campaign=agents-md`, and the article routes to `posthog.com/self-driving` twice, including inside a "Try this" box. The technique being demonstrated in section 3 and the product being sold are the same thing. The evidence is real and openable, which is more than most vendor posts offer — but the selection of what gets measured (tokens saved, feedback volume) and what does not (whether any of this made the agents better) runs in the vendor's favor.
- **Nothing in the file attempts prompt injection against a reviewer.** The agent-directed text above is quoted content within the article's narrative, not an instruction aimed at whoever is reading it.
- **Scrape artifacts.** The file is a saved X page; roughly the first 35 and last 110 lines are site chrome (nav, trending topics, a DraftKings promo, unrelated live-news modules). The engagement figures — 8 / 41 / 513 / 47.6K views — are X UI, not claims the article makes. All substantive images (the two diagrams, Theo's post, the pr-evaluator report, the feedback-cluster chart) are present only as URLs, so several visual claims could not be verified from this file.
