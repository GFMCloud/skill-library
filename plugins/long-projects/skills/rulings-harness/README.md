# Keeping decisions that can go out of date

Part of the [long-projects](../../README.md) pack.

"Tool A is forty times faster than tool B, so use A" is a decision that was true when someone measured it. Written into a notes file, it stays there long after tool B gets rewritten, and nobody ever finds out. This skill turns findings like that into one small file each: the decision in a line, what was measured and when, the thing that would prove it wrong, the command that would show it, and a date to look again. It puts them in a folder with an index, and it can add a `/rulings` command so later sessions can record a new one or re-run every check and tell you which decisions may have gone stale. It separates these from plain preferences, which nothing can measure and which it leaves where they are.

## Say this to use it

Any of these will do:

- "set up a rulings register for this project"
- "turn this benchmark into something we re-check later"
- "my notes file is full of findings that might be out of date"

Or, to be certain this skill and no other one runs:

```
/long-projects:rulings-harness
```

It asks four things in one batch: where the `rulings/` folder should live, which real decisions to start it with, who is allowed to write the index, and how far ahead a revisit date should default to when you have no better answer. It will not build an empty register, so at least one real measured finding has to exist first.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Created rulings/ in /Users/you/work/notes-pipeline/

  rulings/INDEX.md                   14 lines   one row per decision
  rulings/pdf-extractor-choice.md    21 lines
  rulings/never-parse-rtf-with-b.md  19 lines   from a real incident
  .claude/skills/rulings/SKILL.md    37 lines

rulings/pdf-extractor-choice.md reads:

  Use tool A for PDFs. Fall back to tool B when A exits with an error.
  Evidence:    measured 2026-04-11, median of 5 runs on 12 sample PDFs:
               A 28ms, B 692ms. Method and files in evidence/2026-04-11/.
  Revisit-by:  2026-10-11
  Falsifier:   B's extraction time drops below 2x A's on the same files.
  Re-test:     bash evidence/2026-04-11/bench.sh

Two commands from now on: /rulings new to record one, /rulings check to
re-verify the register.
```

## Good to know

- **It creates a `rulings/` folder and, if you want it, one small command.** Nothing else is written, and nothing is deleted or moved.
- **It never edits your project's standing instructions.** If you ask it to move findings out of a CLAUDE.md, the file of standing instructions Claude Code reads at the start of every session in that project, it writes the new ruling files and hands you a written proposal of what to remove. You make that edit yourself.
- **The later check runs commands you wrote.** Each ruling file holds a re-test command that you put there. `/rulings check` runs those. Nothing in the skill runs a command of its own, and nothing of its own goes online, though your re-test command will if that is what it does.
- **The check reports, it does not decide.** A decision whose evidence no longer holds is listed as needing re-deciding. Re-deciding is yours, and is recorded as a new version.
- **It refuses to build a register with nothing in it.** No measured, falsifiable finding in scope means it declines and says so.
- **It separates preferences from findings.** "Do not open generated files automatically" is a preference: no evidence could disprove it, so it stays in your standing instructions rather than becoming a ruling.
- **A decision learned from a real incident never expires.** It goes in with no falsifier and a link to the incident instead.
- **It handles no passwords or keys, starts no helpers, and creates nothing that runs on a schedule.**

## What next

- If the decision is the rule a long batch job applies to every item, point that job's runbook at the ruling file instead of restating it: [sweep-harness](../sweep-harness/).
- A lesson from a single session, before it is measured enough to be a ruling: [retro](../retro/).
- When the decision is still open and you want the case against it argued: [council](../council/).
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
