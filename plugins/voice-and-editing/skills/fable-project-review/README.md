# Reviewing a project you already built

Part of the [voice-and-editing](../../README.md) pack.

This reviews a whole project you point it at, not one file: how it is organised, whether the code is sound, whether the README still describes reality, how the thing looks to whoever uses it, and what its stated goal promises that it does not yet deliver. Findings are ranked from critical down to polish, and each one names the file and the lines. It then writes the findings into a dated plan file designed to be carried out by a later session that remembers nothing about this one, so every item carries the exact path, the current state, the wanted end state and a check that says whether the item is done. Later, after the work has been done, you can point it back at the same project and it marks each item done, partly done or missed.

## Say this to use it

Any of these will do:

- "review this project and tell me what you'd improve"
- "audit what I've built here and write me an improvement plan"
- "check this project against the plan from last week"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:fable-project-review
```

It will ask for the project's goal in one sentence, if no README or document states one. It stops and shows you the plan before it writes the handoff, so that is where you cut or reorder items. It also tells you which model it is running on, because it was written for one particular model and says so when it is on another.

## What you'll get

A review by dimension, then a plan file in the project folder that reads as instructions to somebody who was not here.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Critical (1)
  src/export.py:88  Writes the output file before checking the row
                    count, so a failed run leaves a half file behind.

High (2)
  README.md:14      Setup says `npm start`. There is no start script.
  src/cli.py:200    Same date parsing copied in three places.

Docs: accurate apart from the line above.
Consistency: clean.

Wrote improvement-plan-2026-09-19.md (6 items, ordered).

Item 2 of 6
  File: README.md, "Getting started"
  Now:  "Run `npm start`."
  Want: the real command, taken from package.json scripts.
  Done when: the command in the README runs without error.
  Not in scope: rewriting the rest of the README.
```

## Good to know

- **It writes one or two files into your project folder.** A plan named `improvement-plan-` and today's date, and, in verify mode, a `verification-` file with today's date beside it. Nothing else in your project is changed.
- **It never overwrites an earlier plan.** If one with today's name is already there it adds `-v2`, because the older plan is the record that verify mode checks against.
- **It reads your project and runs one command that only looks.** It walks the directory tree, reads the README, documents, settings and source, and runs `git log --oneline -20` to see what changed recently. Git is the tool programmers use to track changes to files, and that command only prints history.
- **It stops for your approval before the handoff.** Carrying out the plan can take hours, so the plan is where it pauses.
- **It hands you a command rather than running it.** The final step prints a `claude --model ...` line for you to paste into a fresh session. It does not start that session or spend anything on your behalf.
- **It goes online for nothing and uses no account, key or password.**
- **The model names in it will date.** It was written for one specific model and recommends two others by name for carrying out the plan. Those names age faster than the method does, and it will say plainly if you are running it on something else rather than proceeding quietly.

## What next

- To check a single document against the files it describes, rather than review a whole project, see [spec-artifact-diff](../../../consistency-checker/skills/spec-artifact-diff/).
- To list what could be deleted rather than what could be improved, see [overengineering-review](../../../verification-kit/skills/overengineering-review/).
- To carry a plan across sessions without losing the thread, see [handoff](../../../long-projects/skills/handoff/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
