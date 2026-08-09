# Effort Sizing

Reasoning effort is a separate dial from model choice, a strong model at low effort can still beat a weaker model at max effort on some tasks, and burning max effort on a simple task just adds latency for no quality gain.

## Effort Levels

**Low**: quick, direct answer. Use when the task is well-defined, low-reasoning, and there's no ambiguity to resolve. Matches Haiku most of the time, but a low-effort Sonnet call is also common (fast Sonnet answer to something simple, without wanting Haiku's ceiling).

**Medium**: the default for most real work. Enough room to weigh a couple of options, check assumptions, and produce a considered answer without over-deliberating.

**High**: full deliberation. Use when Reasoning or Risk scored high on the decision rubric, when the task has multiple interacting constraints, or when the cost of a wrong turn is expensive to unwind later.

## Model x Effort Combinations Worth Naming

- **Sonnet, medium**: the default combination for most day-to-day work. Start here unless something on the rubric pushes you off it.
- **Opus, high**: reserved for genuinely hard problems: multi-system architecture calls, ambiguous requirements with real stakes, anything where a wrong first move is expensive to walk back.
- **Haiku, low**: mechanical, well-defined, high-repetition work. Ten similar file renames, a quick classification pass, a scheduled task doing a status check.
- **Sonnet, low**: a quick but not-mechanical task: a fast draft, a simple lookup that still needs a sentence of judgment, one step in a larger pipeline that doesn't need the parent's full effort level.

## Mismatches to Avoid

- Opus at low effort, rarely useful. If the task needs Opus's reasoning ceiling, it usually also needs the effort budget to use it.
- Haiku at high effort, doesn't meaningfully improve output on tasks that need real reasoning; if the task needs high effort, it probably needs a stronger model too.
- Defaulting everything to Opus + high effort "to be safe", this is the anti-pattern the whole advisor exists to prevent. Match the tool to the job.
