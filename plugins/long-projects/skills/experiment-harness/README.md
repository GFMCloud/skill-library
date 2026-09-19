# Keeping track of experiments you have already run

Part of the [long-projects](../../README.md) pack.

Modeling and analysis work never really finishes. It just keeps producing new ideas to try. Two things go wrong over months of that: you re-run an idea you already killed and forgot about, and you look at a result first and then decide what you had expected, which makes almost any result look like a success. This skill does not run experiments. It asks you a handful of questions and creates a project folder built to prevent both, with a register of every idea, one file per run holding the exact settings that produced it, a list of killed ideas with the reason each one died, and a frozen check that predictions are scored against. Later sessions fill those in, and they refuse to record a result for a run whose prediction was left blank.

## Say this to use it

Any of these will do:

- "set up an experiment harness for this model"
- "I keep re-deriving the same finding, help me track hypotheses"
- "stop me rationalizing results after I see them"

Or, to be certain this skill and no other one runs:

```
/long-projects:experiment-harness
```

It will ask what is being modeled, what the frozen check is and how it gets frozen, where the new folder should live, how you want runs and ideas named, and who makes the commits. It asks all of that in one batch. Before any of it, it checks that the work fits: if your project has a real finish line, or is a single afternoon's analysis, it says so and points you elsewhere instead of building the folder.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Created experiment-churn-model/

  CLAUDE.md          the predict-before-you-look rule, and who commits
  REGISTER.md        one row per idea, added to and never rewritten
  HOLDOUT.md         the frozen check, and the date it was frozen
  dead-ideas.md      killed ideas, each with its reason
  runs/              one file per run, with the settings that produced it
  .claude/skills/    two commands for later sessions

Two commands from here on:
  /hypothesis   register an idea and write the prediction down
  /run          run it and score it against the prediction
```

## Good to know

- **It creates one new folder and writes nothing else.** The folder holds markdown files with their headings filled in and nothing invented in them. It does not touch the model code it is about, which is meant to live somewhere separate.
- **It runs no experiment, now or later.** The commands it leaves behind run whatever experiment command you write into a run file. Those commands are yours, so whatever they do on your computer is yours too.
- **Nothing it creates is overwritten.** The register is only ever added to, rows change only to move an idea from open to tested or killed, each run gets its own file, and the frozen check is never rewritten after it is frozen.
- **The one enforced rule is the blank prediction.** A run file whose prediction section is empty will not have its result filled in. Everything else in the folder is a written rule that later sessions are asked to follow.
- **The caps are counted by hand.** Rules such as stopping after two runs in a row that answered nothing, or three that failed against the current best, are counted by the session reading the run files, not by any program.
- **It goes online never, and handles no keys or passwords.**
- **Most of its design was invented rather than recovered.** The skill says so in its own text, and a reference file in the skill sets out which parts came from the original intent and which were designed to deliver it.

## What next

- Does your project have a real finish line and a step you cannot undo? Use [phased-harness](../phased-harness/) instead.
- Do many items need the same treatment rather than one idea at a time? Use [sweep-harness](../sweep-harness/) instead.
- Has an experiment produced a measured decision worth re-checking later? [rulings-harness](../rulings-harness/) keeps those.
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
