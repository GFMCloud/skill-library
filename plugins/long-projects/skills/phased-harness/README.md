# Setting up a long job in gated phases

Part of the [long-projects](../../README.md) pack.

Some jobs are too big for one sitting and end in something you cannot take back: deleting the old copies, publishing the site, switching customers over. This skill does not do that job. It asks you a set of questions and then creates one folder of written instructions for it: what the finished state looks like, which step is the one you cannot undo, what Claude Code may do without asking you, what it must always ask about, and one runbook per phase with a checkable "done when" list. Later sessions open that folder and work through it, picking up from the files rather than from anything remembered. Before it builds anything it checks the job is really this shape, and if it is not, it says which test the job failed and where to go instead.

## Say this to use it

Any of these will do:

- "set this up as a phased project"
- "build me a phased harness for the archive migration"
- "this will take several sessions and ends in a delete, plan it properly"

Or, to be certain this skill and no other one runs:

```
/long-projects:phased-harness
```

It asks everything in one batch: the end state stated as a state rather than a list of tasks, the step that cannot be undone, what it may do without asking, what it must never do without asking, the phases with a "done when" for each, where the folder should live, which decisions are yours alone, and the paths and names it will need. It proposes the phase breakdown itself from what you described, for you to correct. Anything you cannot answer is left in the files as the word `TBD`, and every later session stops on it rather than guessing.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Created /Users/you/work/photo-archive-move/

  CLAUDE.md          48 lines   the guardrails every session here must follow
  CONFIG.md          61 lines   paths, and what may proceed without asking you
  STATE.md           29 lines   the resume point: phases, all unchecked
  README.md          22 lines   why this exists and how to run it
  docs/end-state.md  18 lines   "every photo has exactly one home, on the NAS"
  prompts/phase-0-survey.md      54 lines
  prompts/phase-1-copy.md        71 lines
  prompts/phase-2-verify.md      66 lines
  prompts/phase-3-retire.md      58 lines   the step you cannot undo
  .claude/skills/phase/SKILL.md  40 lines

Two things you should know. The end-state doc settles any argument later
sessions have about what you meant. Nothing gets deleted before phase 3, and
phase 3 asks you first, item by item.

To start: open a session in that folder and run /phase
```

## Good to know

- **It writes one new folder and nothing else.** The folder holds written instructions and templates. It changes nothing in the project you are actually working on, and deletes nothing.
- **Running the job later is what touches your real files.** This skill only prepares. Read the generated guardrails before you run `/phase`.
- **It declines jobs that do not fit.** All four of these must hold: more than about a day's work, phases of genuinely different kinds, an end state you can state as a state, and a final step that cannot be undone. If one fails it says which and points you elsewhere.
- **It checks each target folder for git first.** git is the tool programmers use to track changes, and it is what makes the work undoable. The instructions it writes are built around renaming a replaced file with `.superseded` rather than deleting it, and deleting only at the final step after you confirm.
- **It refuses to build if a target folder is not tracked by git and you decline to start tracking it.** Renaming would not be reversible there, which is the guarantee the whole design rests on.
- **One generated instruction reaches your permission settings.** The setup phase of the harness it writes tells a later session to run Claude Code's `/fewer-permission-prompts` against each target project and save the resulting allow rules before the first phase that deploys anything. That is a change to that project's settings, made by that later session rather than by this skill, and it is the only place in this pack where generated instructions touch permission settings.
- **Nothing goes online while it builds.** A harness it generates may later check something external, such as whether you can publish to a shared project, if the job needs it.
- **It handles no passwords or keys.** Where it writes a step that starts tracking a folder with git, that step includes a scan for secrets and a file listing what git should ignore.
- **Later sessions of the generated harness may run several Claude helpers at once**, one per chunk of work, which costs tokens.
- **The generated files name skills from other packs:** [turn-reduction](../../../turn-reduction/README.md), [foundry-core](../../../foundry-core/README.md), [verification-kit](../../../verification-kit/README.md) and [consistency-checker](../../../consistency-checker/README.md). Without them installed, those steps have nothing to call.

## What next

- Many similar items rather than a few different phases: [sweep-harness](../sweep-harness/) instead.
- Long but nothing irreversible at the end: [handoff](../handoff/) carries the work between sessions without the ceremony.
- One routine code change, not a whole project: [orch-pipeline](../orch-pipeline/).
- To agree the risky step before it happens: [plan-gate](../../../turn-reduction/skills/plan-gate/).
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
