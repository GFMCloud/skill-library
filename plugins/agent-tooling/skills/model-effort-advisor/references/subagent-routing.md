# Subagent Routing

Decides whether work runs inline or gets delegated to one or more subagents, and how those subagents should be modeled/effort-sized.

## When to Stay Inline

- The task is a single coherent unit of work with no natural split points.
- Steps depend heavily on each other in sequence (can't parallelize without one step needing the prior step's exact output first).
- The task is small enough that spinning up a subagent costs more overhead than it saves.

## When to Fan Out to Subagents

- **Repetition is high**: 10+ similar items (files, sessions, records) with no per-item judgment call needed between them. Classic fan-out case.
- **Independent research branches**: several angles that don't depend on each other's findings (e.g. scanning different batches of the same dataset, as this very skill audit did across 5 parallel session-scanning agents).
- **Context isolation matters**: a subtask would pollute the main thread's context with a lot of raw detail the parent doesn't need to see, only the synthesized result.

## Build/Review Pairing

For higher-risk generative work, consider a two-agent pattern instead of a single pass:
- **Build agent** produces the work (code, document, analysis).
- **Review agent**, ideally a fresh context with no attachment to the build agent's choices, checks it against the success criteria before it's presented as done.
- Hand the review agent the artifact and the success criteria only, never the build agent's reasoning or rationale. A persuasive explanation of why a choice was made is exactly the channel through which a bad choice gets waved through; the reviewer judges what was produced, not why.

Use this pairing when Risk is high on the decision rubric and a single self-reviewing pass isn't enough assurance. Skip it for low-risk, low-reasoning work, it's overhead without payoff there.

## Sizing the Subagents Themselves

Each subagent gets its own model/effort call using the same rubric, a subagent doing one narrow, mechanical slice of a larger fan-out can run Haiku/low even if the parent orchestration is Sonnet/medium. Don't default every subagent to the parent's model tier; size each one to its own actual job.

## Early-Check Escalation

When a cheaper model runs a long loop, pick one cheap observable to check in its first few turns. Good checks: the code compiles, the first targeted test passes, the edits touch the files the task names. Decide the check before the run starts and write it into the prompt or the parent's plan. A model cannot be told to "notice the task is hard" and be trusted to do it.

If the check fails, stop the run. Restart it cleanly on a stronger model with the original prompt and inputs, not the failed run's history. Example: a Sonnet subagent fixing a failing test should have that test passing within its first few turns; if it does not, hand the same task to Opus from scratch.

## Fan-Out Mechanics

- Batch subagents into a single message with multiple tool calls when they're independent, don't run them one at a time if nothing blocks parallelism.
- Give each subagent a self-contained prompt: it has no memory of the parent conversation, so include everything it needs (context, exact inputs, expected output format, length limits).
- Ask for compact returns. A subagent that dumps full raw content back defeats the point of offloading context, instruct it to synthesize and report concisely.
