# Fact-currency check (verification-kit:fact-currency-check)

As-of: 2026-09-02. Running system: Claude Code 2.1.258 at
/opt/homebrew/Caskroom/claude-code@latest/2.1.258/claude (installed 2026-09-01).
Docs: code.claude.com/docs/en/goal, /scheduled-tasks, /commands, fetched 2026-09-02.
Only load-bearing claims checked (a harvest row would name them).

| Claim (article) | Primary source | Result |
|---|---|---|
| /goal exists; a small fast model judges after each turn | docs/en/goal; binary contains "/goal"; commands page lists it | CONFIRMED. Evaluator is a session-scoped prompt-based Stop hook on the configured small fast model (Haiku by default). |
| The evaluator runs nothing itself, judges only what Claude surfaced | docs/en/goal, verbatim: "It does not call tools, so it can only judge what Claude has already surfaced in the conversation." | CONFIRMED |
| A try/turn cap can be stated in the condition | docs/en/goal: "include a turn or time clause in the condition, such as `or stop after 20 turns`" | CONFIRMED (the cap is judged by the evaluator from the transcript, not enforced mechanically) |
| One goal per session; new replaces old; /goal with no arg shows turns, tokens, last reason; /goal clear; 4,000-char limit | docs/en/goal | CONFIRMED, all five |
| /loop: machine on, session open, 1-minute minimum, local files | docs/en/scheduled-tasks comparison table | CONFIRMED. Addition the article omits: session-scoped /loop tasks expire after 7 days, and a bare /loop runs `.claude/loop.md` or `~/.claude/loop.md` if present. |
| Cloud routine: no machine, no session, 1-hour minimum, fresh clone with no local files | same table | CONFIRMED |
| Desktop scheduled task: machine on, session closed, 1-minute minimum, local files | same table | CONFIRMED |
| CLAUDE_CODE_DISABLE_CRON=1 disables scheduling | docs/en/scheduled-tasks "Disable scheduled tasks"; string present in the 2.1.258 binary | CONFIRMED |
| /schedule creates cloud routines | commands page does not list it; scheduled-tasks table says "Via `/schedule` in the CLI"; this session lists a bundled `schedule` skill | CONFIRMED by the running system |
| `isolation: worktree` for parallel agents | this session's Agent tool schema carries `isolation: "worktree"` | CONFIRMED by the running system |
| /doctor "deletes redundant prompts, catches broken settings, finds unused plugins, and optimizes for lazy loading"; output shows "Est. resident tokens" and "Verdict: trim ~N"; pinned to v2.1.198 | docs/en/commands; binary string probe | CHANGED. Current wording: finds unused skills, MCP servers and plugins versus their context cost; deduplicates local CLAUDE.md against checked-in; trims checked-in CLAUDE.md by cutting content derivable from the codebase; migrates always-loaded guidance into skills and nested CLAUDE.md; "reports findings first and asks for confirmation before changing anything". The trim check needs v2.1.206 or later (article said v2.1.198). The binary contains the string "Est. resident tokens", so the quoted output format is plausible. Downstream: no row may restate the article's feature list; cite the docs wording and the confirm-before-change behavior instead. |
| /usage breaks spend down by skills, subagents, MCPs; /workflows kills agents mid-run | binary contains "/workflows" and "usage"; commands page truncated | UNVERIFIABLE in detail, not load-bearing for any row |

Not checked (not load-bearing for any row, and the clean-room review already marks them unsourced): Karpathy 700 experiments, Shopify 19%, Stripe 1,300 PRs/week, 17,022-skill audit, all pricing. None will be imported.
