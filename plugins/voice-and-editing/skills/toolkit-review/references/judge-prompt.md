You are judging one capability slot in a toolkit evaluation. Slot: **[slot name]**.
Purpose of the slot: [one line].

The current directory holds two reports, `[first].md` and `[second].md`. Each describes
one candidate set of tools for this slot. The reports were written by separate readers
from the source files, to a fixed template, with names removed. You cannot see the source
files and must not try to work out where either candidate came from. If you believe you
can tell, say so in your last section and judge on the content anyway.

Read `[first].md` first, then `[second].md`.

## The bar every candidate must clear

The owner works to three behaviors. A candidate that cannot coexist with all three fails
the slot, whatever else it scores.

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

### Steelman [first]
The strongest honest case for the candidate in `[first].md`, before any scoring.

### Steelman [second]
The strongest honest case for the candidate in `[second].md`, before any scoring.

### Scores
One table, both candidates, each criterion scored 0 to 3 with one sentence of evidence
per cell, citing the report.

| Criterion | 0 | 3 |
|---|---|---|
| Fit with the bar | Cannot coexist with one of the three behaviors | Reinforces them, or is neutral |
| Enforcement mechanism | Prose instruction only | A hook, script or tool-layer limit that blocks or verifies |
| Context cost | Always loaded and long | Loaded on demand and short. Use the counted facts in the report, do not estimate. |
| Maintenance burden | Needs a runtime, service or install step the reports say is absent | Runs with what the reports say is already present |
| Specificity | Generic advice | Concrete checklists, failure modes, stop conditions |

A 0 on "Fit with the bar" fails that candidate for the slot. No other score is
disqualifying alone. Do not reward a candidate for having more items or more text.

### Per-item rows
One row for every item id that appears in either report, as one markdown table with
exactly three columns: `| Item | Class | Note |`. Class is exactly one of these, written
as shown, with the id of an item from the other report where one is required:

- `SUPERSEDES item-xxxxxxxx`: this item should replace the named item.
- `SUPERSEDED BY item-xxxxxxxx`: the named item should replace this one.
- `COMPLEMENT`: fills a gap the other candidate's set has; the note names the gap.
- `FRAGMENT -> item-xxxxxxxx`: not wanted whole; the note names the sections that would
  improve the named item.
- `REDUNDANT item-xxxxxxxx`: the named item does the same job at least as well; nothing
  to take.
- `DISCARD`: nothing to take from it, for a reason in the note that is not about the
  other candidate.

Write `SUPERSEDES` on the better item and `SUPERSEDED BY` on the weaker one, never the
reverse, and never both ways for one pair. An item never names itself.

### Deciding criteria
One line naming the one or two criteria from the score table that settled the rows above.

### What I could not assess from reading alone
What a behavioral test would need to show. If you think you recognized a candidate's
origin, say so here.

Do not write a slot verdict; it is computed from your rows. Write the whole answer as
your reply. Do not try to write a file.
