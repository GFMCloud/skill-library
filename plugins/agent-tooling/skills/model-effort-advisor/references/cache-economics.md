# Cache Economics

Prompt caching changes what a model costs more than model choice does on a long agentic
session, so it belongs in the routing decision. Numbers below are from Anthropic's
release notes and Claude Code changelog as of 2026-09-07; re-verify before quoting them
after a model or CLI release.

## The window

- Claude Code runs a 1-hour prompt-cache window, not the API default of 5 minutes.
  Everything sent within an hour of the last request is a cache read; the first request
  after the window closes rewrites the whole prefix as a 1-hour cache write.
- On Claude Fable 5.1 a cache read is 0.025x the base input price (0.1x on other
  models); a 1-hour cache write is 2x base. Resuming a long thread just past the window
  therefore costs about 80x what resuming inside it costs, on the same context.
- Per-agent control: `experimental.cacheTtl: "1h"` in an agent definition's frontmatter
  (Claude Code 2.1.248); `promptCacheTtl` and `subagentPromptCacheTtl` settings
  (2.1.243). Set 1h on a long-running scanner or orchestrator that pauses between
  bursts; leave the default on short subagents that finish inside five minutes.

## Habits that keep the cache warm

- Run `/compact` before stepping away from a long session. A compacted context that
  misses the window is a small write; an uncompacted one is a large write.
- Keep the prefix stable: tool definitions, system prompt, and CLAUDE.md content sit in
  front of every turn, so editing them mid-session invalidates the cache from that
  point. Since 2.1.260, `/cost` and the status line's `prompt_cache` field name the
  likely cause of a miss (tool definitions or system prompt changed, idle past the TTL);
  read it before assuming the model got slower or dearer.
- On Fable 5.1, `/effort` changes mid-session no longer invalidate the cache (2.1.260),
  and the context attached after tool results is now covered by the cache; before that
  fix it was re-sent uncached on every tool-call turn.
- Subagents: each spawn starts a new prefix. A fan-out of ten Sonnet scanners pays ten
  cache writes; that is still cheaper than one orchestrator reading everything, but it
  is the reason a subagent earns its place only for a self-contained task (see
  `subagent-routing.md`).

## Measure it

Cost per completed task, not per call (see `effort-sizing.md`). For a headless call,
`--output-format json` returns `total_cost_usd`; compare a run inside the window with the
same run after an hour idle before deciding a longer TTL is worth its write cost.

Sources: platform release notes 2026-09-01 (Fable 5.1 cache pricing); Claude Code
changelog 2.1.243, 2.1.248, 2.1.260; Kenn Ejima, x.com/kenn/status/2095021598436974744
(1-hour window and the /compact habit).
