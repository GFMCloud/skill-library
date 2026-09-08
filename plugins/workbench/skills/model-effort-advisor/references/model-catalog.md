# Model Catalog

Current Claude model lineup and what each is for. Verify against docs.claude.com if it's been more than a few months since this file was last touched, model lineups change.

## claude-opus-4-8

The strongest reasoning model in the lineup. Reach for it when:
- The task has real architecture-level ambiguity, multiple valid approaches, real tradeoffs, no obviously-correct answer.
- Risk is high (Risk axis) and getting it wrong is expensive or hard to undo.
- The task requires holding a lot of context/nuance simultaneously (e.g. a build with many interacting constraints).

Cost and latency are both higher than Sonnet. Don't default to Opus for tasks Sonnet handles fine, that's paying a premium for headroom you're not using.

## claude-sonnet-5

The default. Handles the large majority of real work: drafting, coding, analysis, most subagent tasks, most single-session work. If nothing about the task specifically calls for Opus's extra reasoning depth or Haiku's speed/cost, this is the pick.

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

See `cache-economics.md` for what the cache-read price means on a long session.

## Quick Pick Heuristic

- Default to Sonnet.
- Move to Opus only when Risk or Reasoning is clearly high.
- Move to Haiku only when the task is well-defined, low-risk, and either fast-turnaround or high-repetition.
