# Cache Economics

Prompt caching changes what a model costs more than model choice does on a long agentic
session, so it belongs in the routing decision. Numbers below are from Anthropic's
release notes and Claude Code changelog as of 2026-09-07, with a dated section of what
changed through 2026-10-06; re-verify before quoting them after a model or CLI release.

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

## What changed since 2026-09-07 (read 2026-10-06)

- Prices: Opus 5.5 (2026-09-22) reads the cache at USD 0.20 per MTok (0.05x its USD 4
  base) and writes the 1-hour cache at USD 8; Sonnet 5.5 (2026-09-28) keeps Sonnet 5's
  prices, reads at USD 0.20. Fable 5.1's 0.025x read stays the lowest ratio.
- Cache diagnostics went GA on 2026-09-23: the response's `diagnostics` object says why a
  request missed, with no beta header.
- Claude Code fixes that stop a miss you did not cause, by version: 2.1.265 to 2.1.269,
  subagents and `--system-prompt` sessions record the prompt and tool definitions once,
  `/model` no longer re-sends every tool definition, a `-p` conversation resumed
  interactively keeps its prefix, and a cut-off-then-resumed response no longer partially
  invalidates the cache; 2.1.267 adds `maxEffortLevel`; 2.1.273, `/login` no longer
  discards thinking; 2.1.275, global caching of the system prompt up to its dynamic
  boundary; 2.1.278, SessionStart hook output after `/clear` no longer forces a full miss
  (this touches the session-carryover hook here); 2.1.280, `/cost` names a thinking-mode
  change as a miss cause, and a host-app model switch no longer misses; 2.1.286, a
  worktree subagent no longer loads CLAUDE.md twice; 2.1.287, a folder CLAUDE.md is not
  re-attached after resume or compaction; 2.1.288, `--resume` keeps context a compaction
  restored and conversations from 2.1.286 or earlier keep their earlier thinking; 2.1.290,
  a resumed subagent keeps its thinking and cache after a mid-run message.
- A model switch mid-conversation resets the prefix cache like a compaction does. A
  production trace study (Azure Research, 761M calls, as relayed on 2026-10-05: cross-turn
  prefix coverage falls to about 8 percent after a switch) and Accenture's emulation
  (arXiv 2609.28919: cache-safe model and subagent routing recovers 14 to 21 percent of
  spend) say the same thing from two sides: pin the model and the subagent models at
  session start, and change them at a boundary, not mid-task.
- Measured here: the Agent-tool subagent's starting context fell from about 74k to 63k
  tokens between 2.1.283 and 2.1.289 after the double-load fixes (one probe each).

## Measure it

Cost per completed task, not per call (see `effort-sizing.md`). For a headless call,
`--output-format json` returns `total_cost_usd`; compare a run inside the window with the
same run after an hour idle before deciding a longer TTL is worth its write cost.

Sources: platform release notes 2026-09-01 (Fable 5.1 cache pricing); Claude Code
changelog 2.1.243, 2.1.248, 2.1.260; Kenn Ejima, x.com/kenn/status/2095021598436974744
(1-hour window and the /compact habit). For the 2026-10-06 section: the Opus 5.5 and
Sonnet 5.5 What's new pages, platform release notes 2026-09-23, Claude Code changelog
2.1.265 to 2.1.290, arXiv 2609.28919, and x.com/raja_sudireddy/status/2107132202492506420
(secondhand; the paper was not read).
