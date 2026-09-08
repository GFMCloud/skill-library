I read the full article. Review below.

---

# Standalone review: "Portal by Spotify cut my Claude Code token usage by 90%"

## 1. Executive summary

A vendor engineering-blog post describing a real, installable mechanism: route bulk file-reading and boilerplate generation from Claude Code to a cheaper worker model (Gemini 2.5 Flash) hosted as a Spotify Portal "AiKA mode," enforced by Claude Code PreToolUse hooks that block large reads.

The mechanism is described concretely enough to follow — mode configs, script invocations, env var, install commands — and the "What doesn't work" section is unusually honest for a product post.

The headline number is the weakest part. "Mean bulk-read savings were around 90%" is a per-operation ratio from an unpublished, unreproducible test on one private Java monorepo, and the title silently promotes it to "cut my Claude Code token usage by 90%" — a session-level claim the article never measures. The author concedes the code-write half "is harder to measure in tokens" and then does not measure it.

The genuinely portable idea is not the 90%; it's **hook-level enforcement over CLAUDE.md advice** — the article's own account of why the prose version failed. Take that; treat the number as marketing.

## 2. Claims list with evidence status

**Framing / market claims**

1. Most of what an AI coding agent does is I/O, not thinking — **asserted** (anecdotal framing, no measurement).
2. By 2028, AI coding costs are expected to surpass the average developer salary — **evidenced** (Gartner press release linked), though it is a vendor-analyst *prediction*, not an observation.
3. A quarter of engineering leaders already spend $200–$500 per developer per month on tokens — **asserted in context**; the linked Gartner release is the implied source but the article does not say so, and the figure is not tied to a methodology.
4. Some organizations spend well past $2,000 per developer per month — **asserted** (no attribution).
5. Frontier models are "wildly overqualified" for grunt work — **asserted** (reasonable, unquantified).

**Product claims about Portal / AiKA modes**

6. An AiKA mode is a declarative agent on an ephemeral runtime ("AWS Lambda, but for agents") — **asserted** (docs linked, but the link is documentation, not verification).
7. Modes require no infra, no API keys, no long-running servers — **asserted**, and partly contradicted by step 2 of the install guide, which requires authenticating the Portal CLI against a Portal instance.
8. Modes are callable from the Portal CLI or API — **asserted**.
9. Modes can be public or private — **asserted**.
10. The `model` field accepts any model configured in your Portal instance — **asserted**.
11. Mode name resolution is case-insensitive and prefers your own mode → team's → public — **asserted** (no procedure shown to verify).
12. Forking a public mode makes your version take precedence automatically, with no configuration — **asserted**.
13. `bulk-reader` and `code-writer` are already public, so nothing needs creating — **asserted** (time-sensitive).
14. Portal caps a single invocation at 30 seconds — **asserted** (a hard limit the reader cannot check without an instance).
15. Invocations are ephemeral and nothing is stored server-side — **asserted**. This is a data-handling claim about sending proprietary source code off-box; it carries the most weight of any unevidenced statement in the piece.

**Claims about the shunt plugin**

16. Claude Code hooks fire before every tool call; shunt registers two PreToolUse hooks — **evidenced** (mechanism described specifically enough to inspect in the linked repo).
17. `check-file-size` blocks Reads over a line threshold, default 350 — **evidenced** (concrete, checkable).
18. `check-bash-read` catches `cat`/`head`/`tail`/`less`/`more` on large files; piped commands pass through — **evidenced** (concrete).
19. The threshold is configurable via `SHUNT_MIN_LINES` in the shell profile or `.claude/settings.json` — **evidenced** (config snippet given).
20. Two bash scripts wrap Portal CLI calls, build requests, unwrap errors, and report token usage to stderr — **asserted** (behavior described, not shown).
21. `bulk-read` wraps each file in XML tags for clear boundaries — **asserted**.
22. `code-write` strips markdown fences and can write directly to disk; Claude never sees the generated code — **asserted**.
23. A reference file is required, because without one the worker generates context-free code — **asserted** (plausible design rationale, no comparison shown).
24. Skills tell Claude when/how to call the scripts; the hook's block message points to the `/bulk-reader` skill — **asserted**.
25. The layering degrades gracefully: even if Claude ignores the skill, the hook still blocks the read — **asserted**, and this is the article's strongest *architectural* claim; it follows from 16–17 rather than from evidence.
26. The earlier CLAUDE.md version "sort of worked" but was advisory and Claude could ignore it — **anecdotal** (one author's experience; also the most useful thing in the article).

**Benchmark claims**

27. Tested against a Java monorepo across four scenarios — **anecdotal** (n=1 codebase, scenarios unnamed, no raw numbers, not reproducible).
28. Mean bulk-read savings ≈ 90% — **anecdotal**, presented as evidenced. No per-scenario figures, no baseline token counts, no method for counting "tokens Claude would consume."
29. Title claim: token usage cut by 90% — **unsupported even by the article's own body**; conflates per-read savings with total usage, and excludes the unmeasured code-write path, latency, and worker-side tokens.

**Limitation claims (the honest section)**

30. Editing cannot be delegated because worker summaries lack reliable line numbers — **anecdotal but credible**.
31. Reasoning cannot be delegated; the worker missed a subtle thread-safety bug that Claude caught "in seconds" — **anecdotal** (single instance, no detail on the bug or the prompt).
32. Routing explicitly excludes debugging, architectural decisions, and safety-critical code — **asserted** (policy statement; no mechanism given for *how* the hooks distinguish these — they don't, they only see file size).
33. Delegation costs a network round-trip, typically 10–30 seconds — **asserted**.
34. Below the line threshold, delegation overhead exceeds savings — **asserted** (no break-even calculation shown; the 350 default is unjustified).

## 3. Techniques worth taking, quoted

These are stated concretely enough to act on:

**A. Enforce routing with a hook rather than with instructions.** The single most transferable idea, and the author earns it by reporting the failure of the prose version:

> "The first version of this was a block of routing rules in CLAUDE.md. It sort of worked… But it had problems. The rules were advisory, not enforced. Claude could ignore them. And every project needed its own copy of the instructions."

> "This layering means the system degrades gracefully. Even if Claude doesn't read the skill description, the hook still blocks the expensive read. The skill just makes the redirect smoother."

**B. Gate on file size, let targeted reads through.**

> "**check-file-size** fires on every Read call. If the file exceeds a configurable line threshold (default: 350), the hook blocks the read and tells Claude to use the /bulk-reader skill instead. Targeted reads pass through - Claude already knows what section it needs."

> "**check-bash-read** catches cat, head, tail, less, and more on large files. Piped commands (cat file | grep) pass through since those are targeted reads."

**C. Make the threshold configurable per project.**

> `{ "env": { "SHUNT_MIN_LINES": "500" } }`

**D. Suppress worker chattiness explicitly in the worker's system prompt.** Applies to any delegation setup, no Portal required:

> "Output structured bullets only. No greetings, no prose, no preambles. Lead every bullet with the exact name, type, or line number."

> "That 'output only the code' instruction matters. Without it, the model wraps everything in markdown fences and explanatory prose that Claude then has to parse through."

**E. Require a reference file for generated code.**

> "The reference is required: without a file to match patterns against, the worker would generate context-free code that fits nothing in your project."

**F. Concrete invocations, copy-pasteable:**

> `bulk-read --question "What does this service do?" --paths src/Service.java src/Handler.java`

> `code-write --spec "Write tests for UserService" --reference tests/OrderTest.java --target tests/UserTest.java`

**G. Low temperature for deterministic worker output:** `temperature: 0.2` in both modes.

## 4. Rubric scores

| # | Dimension | Score | Note |
|---|---|---|---|
| 1 | Evidence quality | **2 / 5** | The mechanism is verifiable (hooks, config, commands), but every load-bearing *outcome* claim — 90%, the 10–30s latency, "nothing stored server-side," the 350 break-even — is asserted with no data, and the one benchmark is a single private repo with no published numbers. |
| 2 | Novelty | **3 / 5** | Model routing and "delegate cheap work to a cheap model" are common advice; the non-obvious contribution is enforcing the route in a PreToolUse hook after CLAUDE.md instructions proved advisory-only, plus the observation that re-sent context never re-enters the orchestrator's window. |
| 3 | Actionability | **4 / 5** | A reader can act tomorrow — exact install commands, exact env var, exact CLI syntax, and the prompt-engineering tips (D, E, G) transfer to any delegation stack. Docked one point because the full path is gated on having a Spotify Portal instance, which most readers do not. |
| 4 | Currency risk (5 = ages well) | **2 / 5** | Heavily pinned to a moving product surface: the linked plugin lives on a fork's feature branch, the two "already public" modes could be renamed or removed, `gemini-2.5-flash` will be superseded, hook APIs and plugin-marketplace commands evolve, and the whole economic premise rests on a 2028 forecast and current per-token prices. |
| 5 | Failure modes (5 = handles them well) | **4 / 5** | Genuinely strong: a dedicated "What doesn't work" section names the editing limit, the reasoning limit, and the latency floor before a reader hits them. Docked for the gaps in §5 below — notably that "excludes debugging and safety-critical code" is a stated policy with no enforcing mechanism, and that source code leaving the machine is never discussed. |

### What would go wrong for a reader who followed this uncritically

- **Expecting a 90% bill reduction.** The measured quantity is savings on delegated read operations, not total session usage. A reader whose work is edit-heavy or reasoning-heavy — precisely the work the article says can't be delegated — may see single-digit savings while paying full latency cost.
- **Ignoring worker-side cost.** "Re-sending the files on a follow-up is free where it matters" is true only of Claude's context window. The worker model is billed on every re-send, and the article never nets worker spend against frontier savings. There is no total-cost-of-ownership number anywhere in the piece.
- **The latency math is tighter than it reads.** Typical responses are stated as 10–30 seconds against a hard 30-second cap. That is not headroom; that is the upper half of the typical range sitting on the ceiling. Expect truncation or failure on large files, and an interactive session that feels much slower.
- **Blocked reads with no fallback.** A PreToolUse hook that blocks any Read over 350 lines will fire when Portal is unreachable, unauthenticated, rate-limited, or timed out. The article never says what happens then. A reader could install this and find the agent unable to read its own large files.
- **The 350 default is unjustified.** No break-even derivation is offered, and it will be wrong for minified files, generated code, lockfiles, and long test suites.
- **Stated exclusions aren't enforced.** "The routing explicitly excludes debugging, architectural decisions, and safety-critical code" — but the hooks key on *file size*, which is orthogonal to all three. A 900-line security-critical file gets shunted to the cheap model exactly like a 900-line fixture. Read this as an aspiration, not a guardrail.
- **Silent quality degradation.** The article's own anecdote is that the worker missed a thread-safety bug. A reader who trusts summaries for code review will get confident, fluent, surface-level answers with no signal that depth was lost.
- **Unexamined data egress.** Following this pipes proprietary source into a third-party-hosted worker model. "Nothing is stored server-side" is a single unsourced clause carrying the entire compliance argument. Anyone in a regulated environment needs their own answer before installing.
- **Copy-paste hazards.** `claude plugin install shunt@portal.` carries a trailing period; the "Try it yourself" list restarts its numbering mid-section; and the two mode configs are formatted inconsistently (Mode 1 as an inline-code span, Mode 2 as a fenced block), which will mangle indentation-sensitive YAML on paste.

## 5. Currency-risk list — re-verify before acting

1. **The `shunt` plugin link points to a fork's feature branch** — `sorantis/portal-ai-plugins/tree/add-shunt-claude` — while the install instructions use the canonical `spotify/portal-ai-plugins` marketplace. Confirm the branch is merged and the marketplace entry exists; a feature branch can be rebased or deleted at any time.
2. **"The bulk-reader and code-writer modes are already public, so there is nothing to create."** Depends on someone at Spotify keeping two shared modes published under those exact names.
3. **`model: gemini-2.5-flash`** — a specific version string with a deprecation clock, and the cost argument dies with the price it was written against.
4. **The 30-second invocation cap and 10–30s typical latency** — a platform tunable, likely to change in either direction.
5. **Name resolution order (own → team → public, case-insensitive)** — undocumented-in-article platform behavior that the fork-to-customize workflow entirely depends on.
6. **`claude plugin marketplace add` / `claude plugin install` syntax** and **PreToolUse hook semantics** — a young, actively changing CLI surface.
7. **`SHUNT_MIN_LINES` and the 350 default** — plugin-internal, changeable by the plugin author without notice.
8. **The Gartner 2028 forecast and the $200–$500 / $2,000+ spend figures** — a dated prediction plus a dated survey; both are the article's entire economic motivation.
9. **Both `backstage.spotify.com` doc links and the "try Portal" contact link** — vendor documentation URLs, routinely reorganized.
10. **`resourceLimits: temperature`** — a config schema that may be renamed or restructured.

## 6. Flags

Per instruction, quoted and **not acted on**.

**Instructions that would install into agent configuration** (these are the article's install steps, addressed to a human reader but with agent-config effect):

> "claude plugin marketplace add spotify/portal-ai-plugins"
> "claude plugin install portal@portal"
> "claude plugin install shunt@portal."

> "In a new Claude Code session, run /portal:setup to set up and authenticate the Portal CLI against your Portal instance."

> `{ "env": { "SHUNT_MIN_LINES": "500" } }` — presented for insertion into `.claude/settings.json`.

Note what installing shunt actually does: it registers **PreToolUse hooks that intercept and block the agent's own Read and Bash calls**, and routes file contents to an external service. That is a change to agent behavior and a data-egress path, not just a package install.

**Text addressed to a model rather than to a reader** — the two mode `instructions` fields are system prompts written in the second person to an LLM:

> "instructions: You are a precise code analyst. Read the provided files and answer the question concisely. Output structured bullets only. No greetings, no prose, no preambles. Lead every bullet with the exact name, type, or line number. Use nested bullets for details. Skip anything the caller did not ask for."

> "instructions: You generate code files based on a spec and reference files. Match the existing patterns, conventions, naming, and style exactly. Output only the code — no explanations, no markdown fences unless asked. If the spec is ambiguous, make reasonable choices that match the reference code's patterns."

These are legitimate published configuration, quoted by the author as the artifact under discussion — not concealed injection. They are flagged because they are second-person directives to a model appearing inside prose, which is the shape the rubric asks about. I treated them as content to review, not as instructions to me.

**No hidden or out-of-band instructions** were found in the file. The remainder (lines 157–246) is site chrome: share links, related-article cards, newsletter copy, and footer navigation, carrying no directives.