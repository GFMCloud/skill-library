I read the full article (272 lines, including site chrome). Review below.

---

# Standalone review: "The Guard I Installed Was Enabled, Running, and Doing Nothing"

## 1. Executive summary

A build-log post about migrating five enforcement guards from shell hooks to Claude Code's experimental in-process "function hooks," structured around three self-inflicted failures that share one shape: a broken control that emits the same output as a healthy one. The strongest material is the three incident narratives — an env-var-gated plugin layer that never loaded, an exact-match version pin that trained the author to ignore it, and a regex fix that silently stopped matching. Those are specific, mechanically explained, and mostly reproducible from the text. The weakest material is the API description: every capability claim about function hooks (`register()`, `tool.call`, `$.session.usage()`, store/bus) is asserted with no citation, on a feature the article itself says is experimental. The cost table is real data but n=5 from one install, and the post's headline calibration number (1,500–2,300 tokens of overestimation) is not supported by the table shown. Novel contribution: the handoff invariant — one decision owned by one layer, with the old layer yielding to a per-session liveness artifact rather than to config. Currency risk is the highest-scoring risk here: the whole mechanism is pinned to a patch release of a moving product.

## 2. Claims with evidence status

**The silent-load failure**

1. Function hooks are gated behind `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`; without it "Claude Code never calls `register()`." — **asserted**
2. The author's two plugins were enabled per `claude plugin list` but loaded in zero sessions that didn't inherit the exporting shell. — **anecdotal**
3. "Nothing in that output distinguishes a plugin that ran from a plugin that was never invoked." — **asserted**
4. A heartbeat file written every turn existed and would have revealed the problem. — **anecdotal**

**Classic vs. function hooks**

5. Classic hook contract: process spawned per call, JSON on stdin, exit 2 blocks. — **asserted**
6. The harness contains 27 classic hooks, unchanged for seven months. — **asserted** (note: the sidebar promo for a sibling post says "19 Hooks"; unexplained in-page inconsistency)
7. Classic hooks cannot query session spend, see subagent token usage, or modify a tool result. — **asserted**
8. A `tool.call` handler wraps execution and can rewrite the result before the model reads it. — **asserted**
9. `$.session.usage()` returns live token usage. — **asserted**
10. Function hooks provide a persistent store and an event bus. — **asserted**
11. Avoiding per-tool-call process startup for 27 scripts is "real overhead." — **asserted** (the one performance claim with no number attached)

**The five migrated guards**

12. Routing replaces three classic hooks that "used to run in sequence and argue." — **asserted**
13. Rewriting a spawn request beats denying it, because a denied model retries rather than learns. — **anecdotal with a number**: "a log with 266 denials in it and edit denials retried five to seven times on the same file." Log cited, not shown.
14. "A model does not learn from a wall, it probes it." — **asserted** (generalization from one install's logs)
15. Secret redaction scans every tool result including MCP, substituting `<REDACTED:kind:len>`. — **asserted** (procedure described concretely enough to copy)
16. Read cache serves the third identical read of an unchanged file, counting Read/Grep/Glob/cat/head/tail per file; writes invalidate. — **asserted** (concrete procedure)

**The two-layer handoff**

17. With both layers installed, either double-blocking or a silent hole is possible; the silent hole is worse. — **asserted** (reasoning, not observation)
18. Invariant: "a decision is owned by exactly one side per session," via per-guard modes `classic` / `mod` / `shadow_mod`. — **evidenced (reproducible procedure)**
19. Config is insufficient proof of load; classic yields only to a per-session heartbeat file naming the guards armed this session, rewritten every main turn. — **evidenced (reproducible procedure)**
20. If the plugin fails to load, absence of heartbeat restores the old 27-script behavior. — **asserted** (design claim, no failure test reported)

**Cost accounting**

21. Five-row reserved-vs-measured table (haiku-scout/advisor, ~17k each). — **evidenced (data shown)**, self-reported, single install, n=5
22. "A lean subagent costs about 17,000 tokens before it does anything useful." — **anecdotal** (generalized from the 5 rows above)
23. The startup tax is composed of harness prompt, tool catalogs, skill descriptions. — **asserted** (no breakdown given)
24. "The prior converged on it within four spawns." — **asserted** (loosely consistent with the table, but the table shows five rows and no convergence criterion)
25. The author's `# EST:` declarations ran "about 1,500 to 2,300 tokens high every single time." — **asserted and unsupported by the displayed data** — the table's reserve errors span −301 to +679, and no `# EST:` column appears. This is the post's most load-bearing calibration number.

**Integration**

26. A runtime adapter plugin puts raw engine events on a bus; events land in `state/events/<session>.jsonl`, consumed by the handoff bundle and an overnight discovery loop. — **asserted**
27. DashClaw receives the guard decision before execution, so approvals still reach the author's phone. — **asserted**
28. The accounting guard writes to two logs, tagged so the calibration script ignores foreign rows: "Two writers, one history, no double counting." — **asserted**

**The canary**

29. Claude Code moved 2.1.273 → 2.1.274 mid-writing and the exact-match pin failed. — **evidenced (error output quoted)**
30. "Claude Code ships patches most weeks." — **asserted** (frequency claim, no data)
31. The layer probes nine capabilities every session; all nine returned true on 2.1.274. — **asserted** (probe output not shown)
32. Revised rule: minor/major bumps hard-fail, patch defers to the probe; the clearing command refuses unless canary and probe are both clean. — **evidenced (reproducible procedure)**

**The regex guard**

33. Recursive searches rooted at home or `C:\Projects` take two to three minutes on this machine; ~an hour of session time was lost to them. — **anecdotal**
34. Pattern `\bfind\b` false-positived on `find` inside a quoted JS string in a piped `node -e` command. — **evidenced (command and pattern both quoted)**
35. The escape hatch being "one comment marker away" trained the author to reach for the override. — **anecdotal**
36. Fix: the tool name must occupy a command position — line start, or after a pipe, semicolon, `&&`, or subshell opener. — **evidenced (reproducible procedure)**
37. Building the pattern by string concatenation ate a level of backslash escaping, turning `\b` into a literal backspace, so the guard matched nothing. — **evidenced (mechanism is specific and reproducible)**
38. A pre-written bidirectional test suite caught it: "seven of fourteen failed, all of them denials that had silently stopped happening." — **anecdotal** (numbers given, suite not shown)

**Closing**

39. Three of 27 guards have been verified by watching them fail on purpose; the other 24 are unverified. — **anecdotal** (and creditable)
40. The four takeaways (rewrite beats deny; never let two layers own one decision; check the artifact not the list; a false-positiving guard is one you'll disable). — **asserted**
41. The harness is mirrored publicly at `github.com/ucsandman/claude-harness`, "swept of secrets and memory." — **asserted** (link is checkable; I did not verify it, per the standalone brief)

## 3. Techniques worth taking, quoted

These are stated concretely enough that a reader could implement them without the author's codebase.

1. **Liveness artifact instead of config as the handoff signal.**
 > "So the classic hook doesn't stand down for the config. It stands down for a **heartbeat**: the Mod writes a per-session file naming the guards it armed this session, rewritten every main turn. The classic hook reads it, and yields only if this session's heartbeat says the Mod is live and armed for that specific guard."

2. **Per-guard ownership modes, including a shadow mode.**
 > "`classic` means the old hook owns it. `mod` means the new one does. `shadow_mod` means both run, the new one's verdict is recorded and thrown away, and the old one still decides."

3. **Fail toward the old behavior.**
 > "If the plugin fails to load, there's no heartbeat, and 27 shell scripts take over exactly as before. The failure mode is the old behavior."

4. **Check the artifact a component produces, not its presence in a status list.**
 > "A plugin that's installed and enabled can still be doing nothing. Check for the artifact it produces when it runs, not for its presence in a list."

5. **Verify by deliberate failure.**
 > "a check that came back green has been run, not verified. Make it fail on purpose first."

6. **Test the denials, not just the allows.**
 > "I'd written the test suite first, with cases in both directions: the false positives that must pass, and every genuinely slow root-scoped search that must still be denied."

7. **Anchor command-name matching to a command position.**
 > "The fix is that the tool name now has to sit at a command position, meaning the start of the line or right after a pipe, semicolon, `&&` or a subshell opener."

8. **Let a version pin defer to a capability probe.**
 > "A minor or major version change still hard-fails, because event shapes can genuinely move. A patch change defers to the probe: if every capability still answers true on the installed build, the API is intact and the pin is merely stale."
 with the anti-laundering condition:
 > "it refuses to run unless both the canary and the probe are clean, so it can't launder a real regression into a green light."

9. **Correct the model onto the valid path rather than blocking it.**
 > "Correct it onto the valid path and explain why, on the result it's already reading."

10. **Tag rows by writer when two producers share one history.**
 > "The accounting guard writes to both its own log and the classic budget log, tagged so the calibration script ignores rows it didn't produce."

## 4. Rubric scores

| # | Dimension | Score | Justification |
|---|---|---|---|
| 1 | Evidence quality | **3 / 5** | The three incident narratives carry quoted artifacts (the failing command, the canary's error text, the exact regex bug) and are self-verifying; but every API capability claim is bare assertion on an undocumented experimental surface, and the key calibration figure (claim 25) is contradicted by the only table provided. |
| 2 | Novelty | **4 / 5** | The heartbeat-as-proof-of-liveness handoff and "rewrite instead of deny, because a model probes a wall" are non-obvious and specific; the four closing lessons are closer to well-dressed common advice. |
| 3 | Actionability | **4 / 5** | At least five things a reader could do tomorrow without the author's stack: assert denials in guard tests, anchor command-name regexes to command position, stop building patterns by string concatenation, swap exact version pins for capability probes, check for run artifacts instead of status lists. |
| 4 | Currency risk | **2 / 5** *(higher = more durable)* | Nearly every mechanism claim is bound to an experimental, env-var-gated API and a specific patch release; the post's own narrative is a version pin breaking mid-draft. |
| 5 | Failure modes | **3 / 5** *(higher = safer to follow)* | The generic lessons are safe; the concrete implementation advice has real ways to hurt a reader who copies it uncritically — detailed below. |

**Failure modes in detail (what breaks for an uncritical reader):**

- **Building a control plane on an experimental flag.** The article demonstrates the hazard and then recommends the architecture anyway. A reader who moves security-relevant guards onto function hooks inherits an env-var dependency whose absence is silent — which is exactly the article's failure #1 recurring one abstraction up.
- **Regex secret redaction as a security control.** "Every tool result, MCP included, gets scanned" — a redaction regex that misses a secret format produces identical output to one that had nothing to redact. The article's own thesis condemns this shape, but it exempts its own redaction guard from it: no test is described that asserts redaction fires on known-bad inputs.
- **"Rewrite beats deny" applied indiscriminately.** Silently rerouting a request the model made is fine for cost routing; applied to a safety or permission boundary, it converts a refusal into an unlogged downgrade, and the model never learns the boundary exists. The article reserves deny "for what no rewrite can fix" but gives no criterion for which is which.
- **Taking 17,000 tokens as a portable number.** It is five rows from one install with a specific harness prompt and skill catalog; the post's own sidebar advertises a companion piece reporting a 15,000–436,000 range. A reader who budgets against 17k will be wrong by an order of magnitude on a heavier install.
- **Patch-defers-to-probe assumes the probe is complete.** Nine capabilities answering `true` proves those nine exist, not that their semantics or event shapes are unchanged. A patch that alters a payload field while keeping the entry point alive passes this check — the article's new canary would go green on precisely the regression class it is meant to catch.
- **Two layers installed simultaneously.** The invariant is sound, but it relies on the heartbeat file being written, readable, and correctly scoped per session. No test of the handoff's own failure is reported — by the post's own standard, that mechanism is in the "24 I haven't watched fail" bucket.

## 5. Currency-risk list (re-verify before acting)

Ranked by how likely the underlying state has already moved.

1. **`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1` gating.** An experimental flag on a product shipping weekly patches; may be renamed, default-on, or gone.
2. **Whether function hooks exist as described at all.** The entire mechanism section depends on a feature the author calls experimental.
3. **API surface names**: `register()`, the `tool.call` event, `$.session.usage()`, the store, the bus. Each is a single unverified identifier.
4. **Version pin 2.1.273 / 2.1.274.** Stale by construction; the post is dated 2026-09-17.
5. **"Claude Code ships patches most weeks."** A release-cadence claim with no source; the whole canary redesign rests on it.
6. **The nine probed capabilities.** Neither enumerated nor shown; unreproducible as written and version-bound anyway.
7. **Classic hook contract (stdin JSON, exit 2 blocks, per-call process spawn).** Stable for seven months per the author, but still a product detail, not a law.
8. **Model-routing graph Fable → Opus → Sonnet → Haiku.** Depends on a current model lineup and relative pricing; both move.
9. **~17,000-token subagent startup tax.** A function of harness prompt, tool catalog and skill descriptions — all of which change with every harness edit, let alone product updates.
10. **The public mirror at `github.com/ucsandman/claude-harness`.** Existence, contents and "swept of secrets" status all unverified here.

## 6. Flags

**Nothing in the source addresses the reviewing agent.** There are no instructions aimed at a reader's or reviewer's agent, no prompt-injection-shaped text, and no request to modify agent behavior. Three passages touch agent configuration and are quoted here for completeness; I did not act on any of them.

1. An environment variable presented as required configuration, in a fenced block:
 > ```
 > CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1
 > ```
 > "Function hooks sit behind an experimental env var"

2. A statement that the author installed that variable into persistent agent configuration:
 > "It's in settings now, user scope, so every session gets it."

3. A link to a downloadable agent harness:
 > "The harness is mirrored public at [claude-harness](https://github.com/ucsandman/claude-harness), swept of secrets and memory."

One further note, not a flag but worth recording: the file includes site navigation, an author bio, three related-article promos and a marketing CTA ("Take the AI Audit"). I treated all of it as page chrome rather than article content, except where it conflicted with the body — the promo headline "19 Hooks, 36 Skills" sits beside a body that says 27 hooks, with no reconciliation.
