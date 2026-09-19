# Run one step of a long project on a schedule

Part of the [voice-and-editing](../../README.md) pack.

Some long jobs are set up as a project folder with numbered steps and a written instruction file for each one. This skill takes one of those projects and writes the short file that lets a single step run by itself at a set time, such as every Sunday evening, with nobody watching. Most of that file is a list of limits: what an unattended run may not do, how long one check may take before it is stopped, and how many times a failed step may be retried. The skill does not create the scheduled task. It hands you the finished file and the settings that go with it, and you set the task up yourself.

## Say this to use it

Any of these will do:

- "schedule this phase to run every Sunday"
- "set up a recurring run of my project's next step"
- "turn this harness phase into a scheduled task"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:schedule-harness
```

It will ask for the project folder, which step or mode to run, how often, and two numbers that bound an unattended run: how many seconds one check may take, and how many times a failed or rate-limited step may be retried. If a value is missing it asks for it rather than inventing one.

## What you'll get

One small instruction file on disk, a check that it is well formed, and the settings you type into the scheduler yourself.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```text
Rendered: ~/projects/report-review/scheduled/grade-pointer.md
Checked:  check-pointer.py -> OK

Register these yourself, they are not in the file:
  folder:   /Users/you/projects/report-review
  cadence:  weekly, Sunday 21:00
  model:    your usual one
  separate working copy: not needed, this step commits

Limits written into the file:
  - no sending changes to a shared server
  - no deleting files (rename to .superseded instead)
  - no passwords or keys
  - check timeout: 120 seconds
  - retries after a failed or rate-limited step: 2
  - anything the run would have asked you becomes a queued note
```

## Good to know

- **It writes exactly one file, at the path you give it.** Nothing else on your computer is changed.
- **It reads your project's own notes first.** It looks at the project's instruction files and its step-running skill to confirm the step you named exists and to pick up any settings already recorded there.
- **It runs two small Python programs, and you need Python 3 for them.** One writes the file from a template, the other checks it. If you write your input as YAML rather than JSON, you also need the PyYAML add-on.
- **It never registers the scheduled task.** That is yours to do in the Claude desktop app, or by approving the scheduling tool when it asks. The skill hands over values, never a password or key.
- **It never writes anywhere inside your `~/.claude` folder.** That is a fixed rule of the skill, stated in both of its programs.
- **It goes nowhere online.**
- **The check is about the file's shape, not the run's behaviour.** It confirms every limit line is present and filled in with real numbers. Whether a future unattended run actually honours those limits is only visible in that run's own log.
- **It assumes a project that already has numbered steps and a step-running skill.** If you do not have one, there is nothing for this skill to point at. Build the project first with [phased-harness](../../../long-projects/skills/phased-harness/). The registration side also assumes the Claude desktop app's scheduled tasks; on another scheduler you would run the step from the command line instead.

## What next

- To build the phased project this skill schedules: [phased-harness](../../../long-projects/skills/phased-harness/).
- To watch a source for changes and act when one arrives, rather than on a clock: [change-watch](../../../long-projects/skills/change-watch/).
- For deciding which model an unattended run should use: [model-effort-advisor](../../../agent-tooling/skills/model-effort-advisor/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
