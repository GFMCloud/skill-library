# Output Templates

## Quick Pass Format

Keep it to a short block, no headers, no table, no restating the task back to the user.

```
Model: [model name]
Effort: [low / medium / high]
Routing: [inline / subagent, if subagent, name how many and what each runs]
Why: [one or two sentences, the axis or axes that drove the call]
```

Nothing else gets appended. If the mode-selection rule required a clarifying question first, ask that, get the answer, then output this block, don't output a block and a question in the same turn.

## Deep Planning Format

Used only when the mode selection rule resolves to Deep Planning (a full project/epic, not a single task).

```
## Task Breakdown

| Task | Model | Effort | Routing | Why |
|---|---|---|---|---|
| [task name] | [model] | [low/med/high] | [inline / subagent] | [one line] |
| ... | | | | |

## Human Review Checkpoints
- [Point in the plan where a person should look before continuing, and why]
- [Repeat for each checkpoint]

## Notes
[Anything that doesn't fit the table, sequencing dependencies, tasks that must complete before others can be sized, assumptions made because inputs were incomplete]
```

Break tasks at a meaningful grain, not so coarse that "build the whole feature" is one row, not so fine that every microscopic substep gets its own row. If in doubt, a task deserves its own row when it could plausibly run on a different model/effort than its neighbors.
