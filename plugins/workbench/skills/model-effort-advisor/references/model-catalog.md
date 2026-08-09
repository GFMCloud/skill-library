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

Narrower use case, check current docs before assuming it's the right fit for a given task; it's not a default substitute for the other three in day-to-day AWS Practice work.

## Quick Pick Heuristic

- Default to Sonnet.
- Move to Opus only when Risk or Reasoning is clearly high.
- Move to Haiku only when the task is well-defined, low-risk, and either fast-turnaround or high-repetition.
