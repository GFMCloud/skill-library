---
name: model-effort-advisor
description: >
  use this skill any time it's unclear which claude model or reasoning effort level to use
  for a task, prompt, or part of a larger build - including questions like "which model
  should I use for this", "what effort/thinking level", "should this be a subagent",
  "should I use a build/review agent pair", or "break this project down by model and
  effort". always trigger before spawning a subagent with an unspecified model, and before
  starting any task where the model or effort choice isn't already obvious. has two modes:
  quick pass (default - one task or decision, fast answer) and deep planning (full
  project/epic broken into per-task model + effort + subagent recommendations, only on
  explicit request). scoped to routing decisions within the current session only - does
  not decide whether work should leave the session for a separate claude code / ultracode
  workflow, that call belongs to supahcode-review.
metadata:
  maturity: incubator
---

# Model + Effort Advisor

## Objective

Give a fast, practical recommendation for:

- Which Claude model to use
- What reasoning effort level to set
- Whether to run the work inline or delegate to subagent(s), and if so, what model + effort each subagent should run at

This is a routing tool, not a planning tool. Favor speed and a usable answer over exhaustive analysis.

---

## Two Modes

### Quick Pass (default)

Use for a single task, prompt, or decision point. Output is a short block, not a table. This is the mode almost every invocation should use.

### Deep Planning

Use for a full project, epic, or multi-task build that needs a task-by-task breakdown. Only enter this mode on explicit signal.

### Mode Selection Rule

If the user's request clearly names a mode (or clearly hands over a single task vs. a project/epic), use that mode without asking.

If it's ambiguous, ask before doing anything:

"Quick pass on this one thing, or deep planning across the full breakdown?"

Never guess silently. Getting the mode wrong wastes more time than asking once.

---

## Quick Pass Workflow

1. Read the task or prompt
2. Score it against `references/decision-rubric.md` (Reasoning, Creativity, Risk, Repetition, Human Oversight)
3. Pick the model and reasoning effort using `references/model-catalog.md` and `references/effort-sizing.md`
4. Decide inline vs. subagent(s) using `references/subagent-routing.md`
5. Output the Quick Pass block from `references/output-template.md` - nothing else, no extra sections

Do not read `references/examples.md` deep-planning example or any deep-mode-only content for a quick pass. Keep this mode light.

---

## Deep Planning Workflow

Only enter this workflow when the mode selection rule above resolves to Deep Planning.

1. Read the project, epic, or task list
2. Break it into meaningful tasks (not microscopic subtasks)
3. Score each task against `references/decision-rubric.md`
4. Assign model + reasoning effort per task using `references/model-catalog.md` and `references/effort-sizing.md`
5. Identify which tasks should fan out to subagents and how, using `references/subagent-routing.md`
6. Identify required human review checkpoints
7. Output the Deep Planning format from `references/output-template.md`

---

## Reference Files

Consult these as needed - quick pass should only need the first three:

- `references/decision-rubric.md` - qualitative task classification (shared by both modes)
- `references/model-catalog.md` - current Claude model guidance
- `references/effort-sizing.md` - reasoning effort levels and model/effort tradeoffs
- `references/subagent-routing.md` - inline vs. subagent decision logic, build/review pairing
- `references/output-template.md` - required formats for both modes
- `references/examples.md` - one quick pass example, one deep planning example

---

## Operating Principles

- Default to Sonnet unless Haiku or Opus is clearly better - see model-catalog.md
- Recommend the lowest-cost model and effort level capable of producing high-quality output
- Use higher reasoning effort or Opus only when ambiguity, risk, or architecture-level reasoning justifies it
- Use Haiku or low effort only when speed/cost matter more than maximum quality and the task is well-defined
- State assumptions when inputs are incomplete - do not block on missing information
- This skill does not decide whether to leave the current session for a separate Claude Code workflow - if that question comes up, point to supahcode-review instead

---

## Surface Behavior

- **Claude Code / Cowork**: this skill's recommendation can be acted on directly - set the model/effort, spawn the subagent(s) recommended
- **Claude.ai chat / Projects**: advisory only - state the recommendation, take no action
