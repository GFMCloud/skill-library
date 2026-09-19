# Standalone review: *The AI-Native SDLC Playbook*

**Source:** `ai-native-sdlc-playbook.md` — Louis Claxton, dated August 21, 2026, published on claude.com/blog. ~9,000 words.

---

## 1. Executive summary

This is a vendor playbook: a six-stage operating model (Plan → Design → Build → Test → Deploy → Maintain) in which every stage commits a markdown artifact to git and the commit triggers the next stage. Its strongest contribution is not the stage model — that part is conventional — but the control taxonomy underneath it: skills are advisory, hooks are deterministic, evals are the regression test for agent *configuration*, and autonomy is tiered by statistical deviation band. Those distinctions are stated crisply and are hard to find elsewhere in this compressed a form.

Evidence is the weak axis. Nearly every load-bearing claim is asserted from the authors' consulting practice; there are no measured outcomes, no named customers, no before/after data, and the two diagrams are schematics, not plots. The article is unusually honest about one limit (skills don't bind) but silent about others.

Actionability is high — the configuration snippets, prompts, and measurement definitions are directly usable — and that is also the risk: the production gate script, the eval CI job, and the managed-settings block all have defects a reader who copies them will inherit. Treat it as a well-organized checklist of *what to build*, not as code to paste.

---

## 2. Claims list with evidence status

### Framing claims (§ "Code is no longer the bottleneck", § "What is an AI-native SDLC")

| # | Claim | Status |
|---|---|---|
| 1 | Organizations now write code with AI "at a speed unthinkable one year ago" while surrounding process has not changed pace | **asserted** |
| 2 | Approval gates, reviews, handoffs and policies are "stalling productivity gains" from agentic coding | **asserted** |
| 3 | Most organizations run six SDLC stages with role-per-stage ownership | **asserted** (plausible, uncited) |
| 4 | The traditional SDLC was designed for an era when writing code was the most time-consuming and expensive stage | **asserted** |
| 5 | When build accelerates, the bottleneck moves to plan, review/test and deploy | **asserted** — the accompanying figure is a schematic illustration, not measurement |
| 6 | Line-by-line human review "can't keep up once agents write most of the diff" | **asserted** |
| 7 | Governance costs increase because exceptions route through weekly/monthly committees | **asserted** |
| 8 | Security teams sized for human output produce either a review queue or under-reviewed code | **asserted** (well-reasoned, still unevidenced) |
| 9 | "The organizations generating the most value have rebuilt their process around what agentic AI can now do" | **asserted** — no organization named, no measure of "most value" |
| 10 | The practices described are what Anthropic's Applied AI team does daily with customers | **anecdotal** — provenance claim, unverifiable from the text |
| 11 | The chain of commits constitutes an audit trail of who asked for what, what the agent produced, who approved | **asserted** — mechanically plausible; no auditor or regulator acceptance shown |
| 12 | Legacy systems (Jira, requirements tools, change boards) are hard to displace because auditors already accept them | **asserted** |

### Product-behavior claims (checkable, but only against current product state)

| # | Claim | Status |
|---|---|---|
| 13 | Plan mode lets Claude read the codebase without changing anything, and "Claude cannot edit files until the engineer accepts the plan" | **asserted** — stated as product behavior with a doc link, no demonstration |
| 14 | Auto mode applies each change without a per-edit prompt | **asserted** |
| 15 | `/init` generates a starting `CLAUDE.md` from what Claude finds in the repo | **asserted** — reproducible in one command, so close to evidenced |
| 16 | Claude reads all of `CLAUDE.md` at the start of a session | **asserted** — load-bearing for the "keep it under a page" rule |
| 17 | A skill is "an advisory control… nothing forces a session to comply with it" | **asserted** — notable as a limitation the article volunteers |
| 18 | A hook is deterministic and runs on every matching action; `exit 2` blocks the action and the message goes to Claude | **evidenced** (reproducible procedure — working script given) |
| 19 | Hook decisions are written to the OpenTelemetry export with timestamp and allow/block verdict | **asserted** |
| 20 | Session transcripts are forwarded to the org's observability stack via OpenTelemetry | **asserted** |
| 21 | A parallel session is a full Claude Code instance in its own worktree; sessions share nothing but the engineer | **asserted** |
| 22 | Subagents have their own context window and tool limits | **asserted** |
| 23 | `claude --worktree <name>` starts a session in a separate checkout on its own branch | **evidenced** (reproducible command) |
| 24 | Subagents are markdown files in `.claude/agents/` with name, description, tools | **evidenced** (full working example given) |
| 25 | Skills are `.claude/skills/<name>/SKILL.md` with triggering frontmatter and instructional body | **evidenced** (full example given) |
| 26 | Skills can be distributed org-wide via plugin marketplaces | **asserted** |
| 27 | Tagging `@claude` on a review comment makes Claude address it and push a fix (claude-code-action); in the managed service `@claude review` requests a fresh review instead | **asserted** |
| 28 | The managed Code Review service is a research preview an admin enables per repository | **asserted** |
| 29 | The review check run publishes a machine-readable severity tally | **asserted** |
| 30 | `permissions.deny` governs Claude's file tools but a sandboxed shell command could still read `~/.ssh` / `~/.aws/credentials` by default, which the `credentials` block closes | **asserted** — a specific, falsifiable security claim, given no demonstration |
| 31 | A tool-level deny on WebFetch does not stop a shell command reaching the network; the OS-level domain allowlist does | **asserted** — same |
| 32 | `failIfUnavailable` makes Claude Code refuse to start when the sandbox cannot initialize; `allowUnsandboxedCommands: false` prevents retrying a failed sandboxed command outside | **asserted** |
| 33 | `requiredMinimumVersion` refuses to start below the approved floor | **asserted** |
| 34 | Each non-interactive pipeline run acts under the agent's own identity, so logs separate agent from triggering engineer | **asserted** |
| 35 | Claude Security scans run on Claude Mythos 5 in Anthropic infrastructure, validate each finding, attach a confidence rating | **asserted** |
| 36 | Claude Security is public beta for Enterprise orgs, needs the Anthropic GitHub App (github.com cloud-hosted only), Claude Code on the Web, Extra Usage with a spend limit, premium seats, admin enablement at a named settings URL | **asserted** — highly specific, entirely uncited |
| 37 | Claude Tag is public beta, Slack only, and makes Claude a channel member under its own identity | **asserted** |

### Methodological / outcome claims

| # | Claim | Status |
|---|---|---|
| 38 | Time from first conversation to committed `intent.md` will fall "from a multi-week elicitation and refinement cycle to hours" | **asserted** — the single boldest outcome claim in the article, with no data |
| 39 | Requirements and design can be collapsed into one session without loss, and the separation is "slow and lossy" | **asserted** |
| 40 | "With a solid plan, the implementation is often a single pass" | **anecdotal** |
| 41 | PR review findings citing a policy "should fall towards zero once the skill is applying the policy" | **asserted** — presented as a diagnostic, which is its saving grace |
| 42 | Time to first review "should fall to minutes" | **asserted** |
| 43 | A test written before the fix, which the agent could not rewrite, is proof the bug is gone | **asserted** — reasonable, and overstated as "proof" |
| 44 | Two or three visual-check rounds is normal for UI work and results improve each round | **anecdotal** |
| 45 | "Each model generation finds vulnerabilities the previous one missed" | **asserted** |
| 46 | A first Claude Security scan "will likely surface findings in code that was considered clean" | **asserted** |
| 47 | Deterministic detection (mean/stddev, Western Electric rules) catches slow drift as well as spikes | **evidenced** — Western Electric rules are a real, published SPC method; the article names it and gives a config
| 48 | Because runs are stateless and non-interactive, "a loop can begin and end without anyone starting it" | **asserted** (follows from the design given) |
| 49 | Two or three concurrent sessions is a sensible start; the ceiling is how many streams one person can review | **anecdotal** |
| 50 | Context switching between tasks is "tiring enough that few people choose to" | **asserted** |

**Tally:** ~50 checkable claims. Six approach *evidenced* (all of them procedures the reader can run, not outcomes). Five are *anecdotal*. The remaining ~39 are *asserted*. **Zero external citations. Zero measured results. Every hyperlink points to an Anthropic product or docs page.**

---

## 3. Techniques worth taking, quoted

These are the parts stated concretely enough to act on. Quoted verbatim.

**1. The two-strike rule for agent memory** — the cheapest habit in the article.
> "A working rule helps here. When Claude makes a mistake twice, the correction goes into `CLAUDE.md`."

And its review-loop twin:
> "When a review flags a mistake for the second time, the correction goes into `CLAUDE.md` as part of that review, and because review reads `CLAUDE.md` the mistake is caught from the next PR onwards."

**2. Advisory vs. deterministic controls** — the article's single most useful conceptual tool.
> "A skill is a control, though an advisory one. It makes Claude likely to apply the policy while the code is written, and nothing forces a session to comply with it. A policy that must always hold needs something deterministic behind the skill, such as a hook that blocks the action or a review pass that re-checks the policy at the PR. The skill makes violations rare and the hook makes them close to impossible."

**3. Protect the verification loop from the thing being verified.**
> "For bug fixes, write the failing test first. Ask Claude to reproduce the bug as a test, run it, and confirm it fails for the reason you expect. Commit that test. Only then ask Claude to make it pass without editing the test, with the test-file hook from the final step enforcing the restriction."

> "the loop itself needs protecting, because an agent fixing code must not be able to weaken the check on that code. A hook that blocks edits to test files during a fix task does this."

**4. Regression-test the agent's configuration, not just the code.**
> "The suite runs non-interactively in CI on a schedule and on any change to `CLAUDE.md`, skills or hooks, since that configuration steers the agent and deserves the regression testing that code gets."

> "Gate configuration changes on the results. A skill change that drops the pass rate gets reviewed before it merges."

With a concrete corpus size:
> "The platform engineer collects 20 to 50 real tasks from recent work with its expected/accepted outcome."

**5. The plan-quality bar** — an unusually testable definition of "good enough".
> "Iterate until an engineer who has never seen the conversation could implement the change from the plan alone."

And the interrogation prompts:
> "Interrogate the plan by asking what the change could break, which step is most risky, and what other options Claude chose not to do."

**6. Tier autonomy by statistical deviation band.**
> "At 1σ the script only logs, at 2σ it invokes Claude read-only to diagnose, and at 3σ Claude may act, though only by opening a PR into the review gate or triggering a pre-approved runbook."

> "detection stays entirely deterministic, with no model involved."

**7. Rehearse rollback before you need it.**
> "Rollback should be the most rehearsed path in the pipeline, a single command that the agent can run and that is exercised regularly in staging."

**8. Name one source of truth per artifact.**
> "for every artifact the process produces, name one system as the source of truth, with everything else holding a copy or a link to the original."

> "**Linkage as the minimum bar.** All artifacts note the record ID and all legacy records contain the commit SHA of the markdown file."

**9. Cap review noise explicitly** — the `REVIEW.md` pattern.
> "`REVIEW.md` also defines what counts as Important as opposed to a Nit, and what to skip."

> "Report at most five nits per review; summarize the rest as a count."

> "## Do not report / Generated files under src/gen/ and anything CI already enforces."

**10. Keep the approval prompt out of the build phase.**
> "A hook that asks a human for approval belongs with the gates in Stage 5: Deploy, because an approval prompt during the build puts a person back on the critical path of all the sessions running in parallel."

**11. Make "done" mean verified, in writing.**
> "Run all three before reporting any task complete, and paste the output. If a test fails, fix the code, not the test."

**12. Measurement definitions that use data you already have.** Several are genuinely computable tomorrow, e.g.:
> "Count `spec.md` commits dated after the first `plan.md` commit for the same change. Git log will give this directly."

> "the number of changes made to the `intent.md` that are made after the first `spec.md` commit for the same change."

---

## 4. Rubric scores

*Polarity note: on all five axes, 5 is good. For "Currency risk" and "Failure modes," 5 means low risk / robust.*

### 1. Evidence quality — **2 / 5**
Roughly six of ~50 claims are evidenced, and all six are procedures the reader can run rather than outcomes; the load-bearing claims — that build is no longer the bottleneck, that this model works, that elicitation collapses from weeks to hours — are entirely unsupported, and both diagrams are schematics rather than data.

### 2. Novelty — **4 / 5**
The stage model is standard, but the control taxonomy is not: advisory-skill vs. deterministic-hook, evals as regression tests for agent configuration rather than for model quality, the test-file-edit block during fix tasks, σ-banded autonomy tiers, and the artifact-chain-as-audit-trail framing are each non-obvious and are set out more sharply than the topic usually gets.

### 3. Actionability — **4 / 5**
Almost every play ships a runnable artifact — `SKILL.md`, `verifier.md`, `settings.json`, `production-gate.sh`, `bands.yaml`, a GitHub Actions workflow, a review policy, and prompts — plus metrics defined against git and PR data a team already holds; it loses a point because several snippets need repair before use and the org-scale prerequisites (skills authored, policy owners named, MDM in place) are far larger than "getting started" implies.

### 4. Currency risk — **2 / 5**
Four products are explicitly labeled beta/preview (Claude Design, Code Review, Claude Security, Claude Tag), one model name appears exactly once and nowhere else in the piece (Mythos 5), and the managed-settings block pins `"requiredMinimumVersion": "2.1.193"` alongside a dozen setting keys, a named admin URL, and a Slack-only integration — the highest-value section is also the fastest-decaying.

### 5. Failure modes — **2 / 5**
A reader who follows it uncritically inherits a production gate that is trivially bypassable, an unbounded eval job, a dependency graph the text contradicts, and a governance story whose weakest link — the human at the gate — gets more to review, not less; details below.

**What goes wrong, specifically:**

- **The production gate is security theater as written.** `production-gate.sh` substring-matches `*"deploy"*` and `*"production"*` on the Bash command and checks that `$RELEASE_APPROVAL` is non-empty. It misses `./ship.sh prod`, `make release`, `kubectl apply -f prod/`, `terraform apply`, and anything routed through an MCP deploy tool rather than Bash — which the very next play tells you to build ("Expose deployment through MCP. Deploy, status, and rollback become tools"). The `PreToolUse` matcher is `"Bash"`, so MCP deploys skip the gate entirely. And the approval token is an ordinary environment variable: an agent that can run shell commands sits in the same process tree that decides whether it is approved. The article says "The gate condition is enforced every time, for everyone." For this script, it is not.
- **The eval job can run away.** The workflow loops over `evals/*.json` calling `claude -p` with `Bash(make test)` allowed, on every PR touching `.claude/**` and nightly at 02:00 — with no timeout, no concurrency cap, no cost ceiling, and no `continue-on-error`. Fifty evals × a real test suite × an API key with "budget for eval runs" is an unbounded bill and a CI queue blocker. `result.json` is also overwritten each iteration, so nothing is retained for the comparison over time the governance section promises.
- **The dependency graph contradicts itself.** Stage 1 Plan lists prerequisites "None," but its infrastructure needs an intent template "encoded as a skill" — and skills are a *Stage 3* play. Stage 2 Design requires "brand, security, compliance, and UX policies written as skills," meaning the second stage depends on the fifth play of the third stage. A reader adopting in stage order stalls immediately. The article's own advice ("Start with any clay play — nothing points into it") is the right reading, but the per-play Prerequisites boxes don't support it.
- **"No engineering skill is required" is not true of the Design play.** The same play's step 2 asks the product owner to "codify it as an organization-level slash command… with a non-interactive job that fires on the merge… and commit `spec.md` as a pull request." That is platform engineering work described inside a play whose Infrastructure box says a product owner with Claude access suffices.
- **The human gate absorbs everything the automation displaces.** Every escalation path terminates at a person: flagged spec concerns go to policy owners, higher-risk plans to a tech lead, all merges to a code owner, all findings to a service owner's triage queue, production releases to a release manager, plus a monthly review-tuning session. The article's own premise is that human-speed steps are the constraint — yet the design routes strictly more decisions through them, faster. There is no discussion of what happens when the triage queue itself saturates, which is the failure the piece opens by diagnosing.
- **The measurement plan has no baselines and several perverse incentives.** "Time to first review… should fall to minutes" and elicitation falling "to hours" are targets with no stated starting point. "Share of changes that merge from the first implementation pass" rewards splitting changes small; "changes merged per engineer per week" is a throughput metric the article hedges with "read alongside the rework rate" but does not otherwise defend; "PR review findings citing the policy… should fall towards zero" is a metric that also falls to zero if the reviewer stops looking.
- **Auto-accept mode is introduced with conditions and then generalized.** The gating conditions are stated well ("a tight `spec.md`, a small blast radius, and code the tests already cover") but the section closes by calling it "fundamental to running the SDLC autonomously," and Stage 6 assumes it. A reader who reaches Stage 6 without the Stage 3–4 guardrails mature has built an unattended loop with no brakes.
- **`REVIEW.md` and `intent.md` are conventions, not features.** They are presented in the same typographic register as `CLAUDE.md`, `.claude/skills/`, `.claude/agents/` and `.claude/settings.json`, which *are* loaded by the harness. A reader may reasonably expect the tool to pick up `REVIEW.md` automatically; nothing in the article says it is a file you must explicitly reference in a prompt or action config.
- **"5 min" reading time.** The document is roughly 9,000 words — call it 35–45 minutes with the code blocks. Minor, but it is a number stated as fact on the page and it is wrong by roughly 7×, which is a reasonable proxy for how much the surrounding metadata was checked.

---

## 5. Numbers, and currency-risk list

### Every figure in the piece

| Figure | Attributed to | Note |
|---|---|---|
| "Reading time 5 min" | page metadata | **Unsourced and wrong** — ~9,000 words |
| "six stages" | "Most organizations run some version of the same six stages" | Convention, not measurement |
| "20 to 50 real tasks" (eval corpus) | none | **Folklore-shaped** — plausible, no derivation |
| "Two or three sessions is a sensible starting point" | none | Anecdotal heuristic |
| "Two or three rounds is normal" (visual iteration) | none | Anecdotal heuristic |
| "Keep it under a page" (`CLAUDE.md`) | rationale given: full file is read each session | Reasoned, not measured |
| "at most five nits per review" | example `REVIEW.md` | Illustrative default |
| "Once a month the tech lead tunes the setup" | none | Cadence assertion |
| "Weekly is a sensible default" (scan schedule) | none | Cadence assertion |
| 1σ / 2σ / 3σ tiers | Western Electric rules | Method is real and named; **the mapping of σ-band to autonomy level is arbitrary** and has no stated derivation |
| `rolling_30d` baseline | example `bands.yaml` | Illustrative |
| "roughly a third of call time" | inside the fictional sample `intent.md` | **Fictional** — do not cite |
| "50 rps" claims-core rate limit | inside the fictional sample `plan.md` | **Fictional** |
| "Java 21, Spring Boot 3" | inside the fictional sample `CLAUDE.md` | **Fictional** |
| `"requiredMinimumVersion": "2.1.193"` | managed-settings example | **Real and dated** — a specific version floor |
| `exit 2` | hook script | Real documented protocol value |
| `actions/checkout@v4` | workflow example | Pinned, will age |
| "3 a.m." alert, "10pm Slack message" | rhetorical | Not data |
| "one year ago" | opening line | Undated relative claim in a dated article |

### Re-verify before acting

Ordered by how likely it is to have moved and how much breaks if it has.

1. **`Claude Mythos 5`** (Claude Security scanning model). Named once, nowhere else in the article, and inconsistent with every other model reference. Verify the model, its rates, and whether that name is current at all — the entire cost estimate for scheduled scanning rests on it.
2. **`"requiredMinimumVersion": "2.1.193"`.** A hard floor. Copying it verbatim later will either be a no-op or will refuse to start engineers on builds you meant to allow.
3. **Every key in the managed-settings block** — `allowManagedPermissionRulesOnly`, `disableBypassPermissionsMode`, `allowManagedHooksOnly`, `disableSideloadFlags`, `allowManagedMcpServersOnly`, `strictKnownMarketplaces`, and the whole `sandbox`/`credentials` sub-tree. The article itself points to the settings reference for this reason. A silently-renamed key in a *deny* list fails open.
4. **The two security gap claims (#30, #31)** — that a sandboxed shell command can read `~/.ssh` and `~/.aws/credentials` unless the `credentials` block denies them, and that a `WebFetch` deny does not stop shell egress. These are the justification for the sandbox layer; test them in your own configuration rather than assuming either the gap or its closure.
5. **Four beta/preview products:** Claude Design (beta), managed Code Review (research preview), Claude Security (public beta), Claude Tag (public beta, Slack only). Availability, entitlement requirements, and behavior are all in motion. The Claude Security prerequisite list in particular — GitHub App on cloud-hosted github.com only, Claude Code on the Web, Extra Usage with spend limit, premium seats, a named admin URL — is exactly the kind of list that changes quietly.
6. **`@claude` semantics differ by deployment.** The article states that in claude-code-action a tag makes Claude fix and push, while in the managed service `@claude review` requests a fresh review. Confirm which behavior your installation has before writing a runbook around it.
7. **Plan-mode enforcement (#13).** "Claude cannot edit files until the engineer accepts the plan" is load-bearing for the governance claim that design review precedes code generation. Verify in your version rather than in the docs page.
8. **OpenTelemetry export contents (#19, #20).** Both the hook-latency metric and the session-transcript audit trail assume specific fields exist in the export. Confirm the schema before promising an auditor either one.
9. **`claude --worktree` flag and `.claude/agents/` frontmatter schema** (`name`, `description`, `tools`). Cheap to check, and both appear in copy-paste artifacts.
10. **Hook exit-code protocol** (`exit 2` blocks; stderr goes to Claude). Documented behavior, but it is the mechanism the entire deterministic-control argument rests on.

---

## 6. Flags

### 6a. Text addressed to an agent rather than to the reader

All of the following are **inside fenced code blocks or clearly labeled examples**, presented to the reader as templates to adapt. I read none of it as concealed or as directed at me; I quote it as the rubric requires and **did not act on any of it**.

Prompts written to be handed to a model:

> "Read the attached intent.md and produce a requirements and design spec for integrating it into our existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines, security policies and UX standards. Document the spec fully as spec.md, ready to hand to the engineering team. Describe clearly any areas of concern, especially where you cannot satisfy contradicting policies."

> "Read the build log at out/build.log. Identify the most likely cause, say whether the failure looks flaky or real, and write a three-line summary for the PR thread."

Skill body — second-person imperatives to an agent:

> "When you create or change an API endpoint: 1. Authentication: every endpoint requires the gateway JWT; no anonymous routes outside /health… Run scripts/check-endpoints.sh and include its output in your summary."

Subagent definition — second-person imperatives to an agent:

> "Start the app with make run. Exercise the changed behavior and the two nearest neighboring flows. Report what you ran, what you saw, and any behavior that does not match plan.md. Do not fix anything; report only."

Memory-file block — instructions an agent is expected to obey each session:

> "Run all three before reporting any task complete, and paste the output. If a test fails, fix the code, not the test."

> "Do not bump dependency versions; the platform team owns them." / "The legacy v1/ package is frozen; changes go in v2/."

Review-policy file — instructions to a reviewing agent:

> "Run three passes and tag each finding with its pass… Reserve Important for findings that would break behavior, leak data or breach a policy. Style and naming are nits."

### 6b. Instructions to install content into agent configuration

The article repeatedly directs the reader to write files into agent-config locations. This is the article's legitimate subject matter — it is a configuration playbook — but it is exactly the pattern worth flagging in a clean-room read, because a reader who pastes these blocks is modifying what their agent obeys:

> "Put the skill in the repo at `.claude/skills/<name>/` so it ships with the code, or distribute it organization-wide through a plugin."

> "Check `CLAUDE.md` into git at the repo root so the whole team shares one version and changes are reviewed like code."

> "Turn repeated jobs into subagents, as defined in markdown files in `.claude/agents/`… Check the definitions into git so the whole team shares them."

> "Team hooks go in `.claude/settings.json` in git, and non-negotiable hooks go in managed settings owned by the platform or IT admin, where individual engineers cannot switch them off."

> "Deployed by the platform team via MDM or the admin console; engineers cannot edit or override any of it." — followed by a full managed-settings JSON block.

> "npm install -g @anthropic-ai/claude-code" — inside the CI workflow example.

The managed-settings block is the one to treat most carefully: it is a policy artifact intended to be *unoverridable by the engineers it governs*. The article does append the right caveat, and it deserves quoting alongside the block:

> "Consider the above a starting point to tailor, rather than a recommendation to copy. Every deny trades against capability, and the right balance depends on the data classification of the repo."

### 6c. Commercial disclosure

Not an injection concern, but material to reading the evidence: the article is published by the vendor whose products it recommends, written by that vendor's Applied AI team, and every one of its ~25 outbound links resolves to a claude.com or anthropic-owned property — including the two links offered as further evidence ("how Anthropic secures its AI-native SDLC", "how Claude Tag runs on-call for CI/CD at Anthropic"). There is no external corroboration anywhere in the piece. The engineering reasoning is sound enough to stand on its own; the outcome claims should be read as marketing until independently measured.
