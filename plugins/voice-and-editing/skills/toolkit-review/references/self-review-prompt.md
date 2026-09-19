You are reviewing one set of tool files against a bar. Slot: **[slot name]**. Purpose of
the slot: [one line].

The current directory holds one report, `R.md`, written by a separate reader from the
source files, to a fixed template, with names removed. No other set exists for comparison.
Judge each item on whether it earns its place in the set: whether it does its job in a
way the bar can rely on, at a context cost its use justifies. You cannot see the source
files and must not try to work out who wrote them.

## The bar

The owner works to three behaviors. An item that cannot coexist with all three fails.

1. **Plan, then stop.** Before work with real consequences: restate the goal, ask at most
   three blocking questions with defaults, list numbered falsifiable assumptions, give a
   file-level plan, and wait for approval.
2. **Executed evidence before "done".** Run the thing, inspect the result, show the
   output. A tool reporting its own success is not evidence.
3. **Say what was and was not checked.** Every report states what was checked, what it
   returned, and what was left unchecked.

## What to write, in this order

A mechanical check enforces these headings, the row format and the class vocabulary;
a reply that breaks them is re-run.

### Steelman
The strongest honest case for the set exactly as it is, before any scoring.

### Scores
One table, one row per item, each criterion scored 0 to 3 with one sentence of evidence
per cell, citing the report.

| Criterion | 0 | 3 |
|---|---|---|
| Fit with the bar | Cannot coexist with one of the three behaviors | Reinforces them, or is neutral |
| Enforcement mechanism | Prose instruction only | A hook, script or tool-layer limit that blocks or verifies |
| Context cost | Always loaded and long | Loaded on demand and short. Use the counted facts in the report, do not estimate. |
| Maintenance burden | Needs a runtime, service or install step the report says is absent | Runs with what the report says is already present |
| Specificity | Generic advice | Concrete checklists, failure modes, stop conditions |

### Per-item rows
One row for every item id in the report, as one markdown table with exactly four columns:
`| Item | Class | Criterion | Note |`. Class is exactly one of:

- `KEEP`: earns its place as written.
- `TIGHTEN <section or field>`: earns its place, and the named section or field is where
  it falls short; the note says what a tighter version would state.
- `SPLIT`: does two jobs that would route or load better as two items; the note names them.
- `RETIRE`: does not earn its place; the note says why, and what covers the job instead
  if anything in the report does.

Criterion is the one score-table criterion that decided the class.

### Deciding criteria
One line naming the one or two criteria that settled most rows.

### What I could not assess from reading alone
What a behavioral test would need to show.

Write the whole answer as your reply. Do not try to write a file.
