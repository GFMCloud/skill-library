# Model Catalog

Current Claude model lineup and what each is for. Verify against docs.claude.com if it's been more than a few months since this file was last touched, model lineups change.

## claude-opus-5-5

The Claude Code CLI default since 2.1.280 (released 2026-09-22) and the strongest
non-Fable tier. USD 4 / 20 per MTok (below Opus 5's 5 / 25), cache reads USD 0.20 per
MTok (0.05x base), 1-hour cache writes USD 8, 5-minute writes USD 5; 512-token minimum
cacheable prompt. Anthropic's routing advice is unchanged from Opus 5: start here for most
workloads, move to Fable only when evals at higher effort still fall short. Constraints and
behavior changes to design around (What's new page, read 2026-10-06):

- Adaptive thinking is always on; `thinking: disabled` or a manual budget returns a 400.
  Effort is the only depth control.
- The default effort is `medium` (Opus 5 ran at `high`), and the model thinks more per
  turn at a given level, most at `xhigh` and `max`. Re-run the effort sweep; a setting
  carried over from Opus 5 is a different setting.
- `tool_choice` types `any` and `tool` return a 400; use strict tool use or structured
  outputs.
- Thinking blocks are tied to the model and the conversation: Opus 5.5 reads blocks from
  Opus 5, Sonnet 5.5 and earlier models, and only Fable 5.1 and Mythos 5.1 read its blocks.
  Moving a conversation from Opus 5.5 to any model other than those two drops its
  reasoning; moving it up to Fable 5.1 on the Claude API keeps it. The prefix
  check that Fable 5.1 enforces applies here too: keep the history append-only.
- Text between tool calls arrives as progress-update `thinking` blocks, empty at the
  default `display`; a harness that reads narration between tool calls goes quiet.
- The `computer_20251124` tool is refused on the Claude API and Google Cloud; use the
  `computer_toolset_20260801` toolset.

## claude-opus-4-8

The strongest reasoning model of the 4.x lineup, superseded as the default Opus by
`claude-opus-5-5` above. Reach for it when:
- The task has real architecture-level ambiguity, multiple valid approaches, real tradeoffs, no obviously-correct answer.
- Risk is high (Risk axis) and getting it wrong is expensive or hard to undo.
- The task requires holding a lot of context/nuance simultaneously (e.g. a build with many interacting constraints).

Cost and latency are both higher than Sonnet. Don't default to Opus for tasks Sonnet handles fine, that's paying a premium for headroom you're not using.

## claude-sonnet-5-5

The default, and the model the Claude Code `sonnet` alias resolves to since 2.1.284
(released 2026-09-28; `claude-sonnet-5` stays available by id). Handles the large majority
of real work: drafting, coding, analysis, most subagent tasks, most single-session work. If
nothing about the task specifically calls for Opus's extra reasoning depth or Haiku's
speed/cost, this is the pick. Same prices as Sonnet 5 (USD 2 / 10 per MTok, cache reads
USD 0.20), 1M context, same tokenizer. Constraints and behavior changes (What's new page,
read 2026-10-06):

- Effort levels are recalibrated: a level does not produce the same thinking as on
  Sonnet 5, and the API default is `high`. Re-run the sweep. Start at `high` unless the
  workload is agentic or latency-sensitive; for agentic coding and multistep tool use start at `medium`
  for well-specified tasks and move to `high` for harder or longer ones; for chat and
  latency-sensitive work start at `medium` or `low`.
- Up-front thinking is turned off with `thinking: {"type": "between_tools"}` (at `high`
  effort or below), never `disabled`, which returns a 400.
- `tool_choice` types `any` and `tool` return a 400.
- Thinking blocks are tied to the model, the conversation and the account: only Opus 5.5
  reads Sonnet 5.5 blocks, and blocks sent from another account are dropped silently.
- The advisor tool refuses Opus 4.8, Opus 4.7 and Sonnet 5 as advisors for a Sonnet 5.5
  executor; `computer_20251124` is refused on the Claude API and Google Cloud.
- Text between tool calls longer than a sentence or two arrives as `thinking` blocks.

Every effort sweep is re-run on a new model. Both 5.5 releases moved their calibration,
and the sweep is the only way to know what a carried-over setting now costs.

## claude-haiku-4-5-20251001

Fast and cheap. Reach for it when:
- The task is well-defined and mechanical (classification, extraction, simple formatting, short lookups).
- Speed matters more than depth (a scheduled task doing a quick check, a subagent doing one narrow repetitive step in a larger fan-out).
- The task is one of many identical/near-identical items (Repetition axis is high) and each item doesn't need deep reasoning.

Don't use Haiku for anything with real Risk or Reasoning weight, it will produce an answer, just not necessarily the right one for anything subtle.

## claude-fable-5

Narrower use case, check current docs before assuming it's the right fit for a given task; it's not a default substitute for the other three in day-to-day AWS Practice work. Superseded by `claude-fable-5-1` (below) as of 2026-09-01; same price, cheaper cache reads.

## claude-fable-5-1

Launched 2026-09-01 as the successor to Fable 5 for long-running agentic coding, knowledge
work, and research: 1M-token context by default, 128k max output, always-on adaptive
thinking, USD 10 / 50 per MTok (the same as Fable 5) with cache reads at USD 0.25 per MTok
(0.025x base, against 0.1x on other models). Anthropic's own routing advice: "For most
workloads, start with Claude Opus 5"; use Fable 5.1 "for demanding reasoning and
long-horizon agentic work, or when your evals on Claude Opus 5 at higher effort still fall
short." Here that means the orchestrator of a long unattended run, where the cache-read
discount and the context window both pay off; for short or mechanical subagents it is the
wrong tier. Constraints and behavior changes to design around (all from the What's new
page, as of 2026-09-07):

- `tool_choice` types `any` and `tool` return a 400; use strict tool use or structured
  outputs to force schema-conformant tool inputs.
- Thinking blocks are preserved only for the model that produced them or a newer one, and
  editing anything before a block (system prompt, tools, an earlier message) invalidates
  every later block. Keep the history append-only; do not route a Fable 5.1 transcript to
  an older model.
- Per-message effort is in beta (`output_config.effort` on a mid-conversation `system`
  message, header `mid-conversation-output-config-2026-07-01`); changing effort no longer
  invalidates the prompt cache.
- Parallel tool calling is more variable: in agent loops it may issue one tool call per
  turn where Fable 5 batched several. Add a one-line batching instruction to harness
  prompts; the extra turns cost tokens and time, not answer quality.
- Whole-file rewrites for small edits are more likely; prefer targeted-edit tooling and say
  so in the prompt. At `low` effort it answers from memory more often, so raise effort for
  turns that need fresh reads.
- Fewer progress updates between tool calls at higher effort; ask explicitly for an opening
  line and a closing recap if the run's log depends on narration.
- In Claude Code, picking Fable in `/model` saves a default that follows the newest Fable
  (2.1.287), as the Opus and Sonnet aliases already did.

See `cache-economics.md` for what the cache-read price means on a long session.

## Quick Pick Heuristic

- Default to Sonnet (5.5).
- Move to Opus (5.5) only when Risk or Reasoning is clearly high.
- Move to Haiku only when the task is well-defined, low-risk, and either fast-turnaround or high-repetition.
