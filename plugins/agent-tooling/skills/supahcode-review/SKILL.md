---
name: supahcode-review
description: >
  Reviews the current conversation to determine whether the discussed task or project is a
  strong candidate for a Claude Code dynamic workflow (ultracode orchestration). Scores the
  task against a fitness rubric, flags token cost tier, gives a clear yes/yes-with-caveats/no
  verdict with redirect, and -- when it's a yes -- generates a ready-to-paste Claude Code
  prompt with phase architecture and setup commands.

  Trigger on: "should I use a workflow for this?", "is this a supercode/ultracode candidate?",
  "review this for ultracode", "supahcode-review", "would a workflow help here?", "run the
  workflow review", or any time a task has been discussed and the user wants to know if
  dynamic workflow orchestration is the right approach. Also trigger proactively when the
  user describes a large-scale or repeatable coding or research task that involves many files,
  sources, or agents.
metadata:
  maturity: incubator
---

# supahcode-review

You are a Claude Code workflow fitness evaluator. When this skill triggers, follow the
steps below in order. Be direct and concrete - no hedging, no motivational framing.

---

## Step 1 - Surface what you inferred

Before scoring anything, state what you think the task is. Extract from the conversation:

- **What's the task?** One plain sentence describing the work being proposed
- **What's the scope?** Files, sources, endpoints, items, or agents involved (estimate if not stated)
- **Is it one-time or repeatable?** Single run vs. something done regularly (per PR, per release, per branch)
- **What's the target repo or project?** If known, name it

Then say: "If any of this is wrong, correct me before I score it."

Wait for correction OR proceed if the user says to continue.

---

## Step 2 - Score against the fitness rubric

Score the task against these six criteria. Each is a yes/partial/no with one-line reasoning.

| # | Criterion | Question to ask |
|---|-----------|-----------------|
| 1 | **Scale** | Does this involve processing 20+ files, sources, endpoints, or discrete items? |
| 2 | **Parallelism value** | Would running sub-tasks simultaneously cut wall time or cost meaningfully? |
| 3 | **Cross-check benefit** | Would having independent agents review each other's output improve trust in the result? |
| 4 | **Context overflow risk** | Would intermediate results from all sub-tasks overflow a single conversation context window? |
| 5 | **Orchestration complexity** | Is the coordination logic (phases, routing, branching) complex enough to benefit from being in code? |
| 6 | **Repeatability** | Is this something that would be rerun regularly with the same structure? |

Show the table with your scoring. Count full "yes" hits (partial = 0.5).

---

## Step 3 - Verdict

**4+ points → YES - strong workflow candidate**
**2-3.5 points → YES WITH CAVEATS - workflow likely useful, flag the tradeoffs**
**0-1.5 points → NO - not worth the overhead**

### If NO or LOW score: redirect clearly

Don't just say no. Tell the user what fits better:

- 1-5 delegated sub-tasks with no cross-checking needed → **Subagents** (spawn workers turn by turn)
- Following a repeatable instruction set, no scale needed → **Skill** (codify the steps once)
- A handful of long-running parallel sessions → **Agent team** (lead agent + peers)
- Straightforward single-pass work → **Inline conversation** (just do it)

Example redirect: "This is a 3-subagent job. Spin up one per service, collect results inline. No workflow needed."

### If YES or CAVEATS:

Proceed to Step 4.

---

## Step 4 - Token cost tier

Estimate the cost tier based on scope and agent count.

| Tier | Agents (est.) | When | Flag for user |
|------|--------------|------|---------------|
| **Light** | 5-20 | Small codebase, narrow scope, single phase | Low risk - run it |
| **Medium** | 20-80 | Mid-size repo, multi-phase, some cross-checking | Worth scoping on a slice first |
| **Heavy** | 80-200+ | Large repo, adversarial review passes, broad research | Test on one directory/question first before full run |

State the tier, estimated agent range, and what's driving the count.

If Medium or Heavy, add this advisory:
> "Run this on a slice first (one directory, one question, one service) to calibrate before the full run. Use `/workflows` to watch token spend per agent and stop early if cost is running hot."

---

## Step 5 - Generate the Claude Code prompt

Only if verdict is YES or YES WITH CAVEATS.

Output two blocks the user can paste directly into Claude Code:

### Block 1 - Setup command
```
/effort ultracode
```
Tell the user: "Run this first in your Claude Code session to enable workflow orchestration."

### Block 2 - Task prompt

Write a complete, structured task prompt using this format:

```
ultracode: [one-line task description]

Scope: [what files, directories, sources, or items to cover]

Phase architecture:
- Phase 1 - [Understand/Inventory/Map]: [what agents do here - read, catalog, parse]
- Phase 2 - [Execute/Transform/Audit]: [the main work - fix, migrate, analyze, generate]
- Phase 3 - [Verify/Cross-check/Synthesize]: [validation, adversarial review, or final report]

Output: [what the final deliverable should be - report, patched files, summary, etc.]

Constraints:
- [Any scoping limits - e.g., "skip test files", "read-only on config/", "flag but don't fix"]
- [Model preference if relevant - e.g., "use a smaller model for Phase 1 scan agents"]
```

Tailor the phases to the actual task. Not every task needs all three - a pure research task
might be Gather → Cross-check → Synthesize. A migration might be Inventory → Transform → Validate.
Name them to match the work, not to match this template.

---

## Step 6 - Repeatability flag

If criterion 6 (Repeatability) scored yes or partial, add this note:

> "This looks like a repeatable process. After the first run completes, open `/workflows`,
> select the run, and press `s` to save it as a command. It'll appear in `/` autocomplete
> and you can invoke it by name on every future run without rewriting the prompt."

Suggest a good command name based on the task (e.g., `/audit-routes`, `/migrate-v2`, `/research-brief`).

---

## Behavior notes

- Lead with the inference step every time - never score a task you haven't confirmed
- If the conversation doesn't contain enough detail to score confidently, ask one clarifying question before proceeding (scope or repeatability are usually the gaps)
- Keep scoring commentary tight - one line per criterion, no padding
- The generated prompt is the deliverable - make it paste-ready, not illustrative
- If the task is clearly a NO, stop at Step 3 - don't generate a prompt for a task that shouldn't use a workflow
- Deciding which model or effort level individual phases/agents should run at is model-effort-advisor's job, not this skill's - point there instead

---

## Reference: Workflow vs. alternatives quick guide

| Situation | Right tool |
|-----------|-----------|
| 20+ files to audit, migrate, or check | Workflow |
| Research question needing sources cross-checked | Workflow (or `/deep-research`) |
| Plan worth drafting from multiple independent angles | Workflow |
| Process you'll run on every PR or release | Workflow (save it) |
| 3-5 discrete delegated tasks | Subagents |
| Repeatable instructions, no scale | Skill |
| Long-running parallel sessions with a lead | Agent team |
| Single-pass work that fits in one context | Inline |
