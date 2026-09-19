# Taking one code change through a pipeline

Part of the [long-projects](../../README.md) pack.

Most changes to code are ordinary: add a feature, fix a defect, adjust a behavior, tidy some structure. Asked to make one, Claude Code will often start typing, and the plan, the tests and the review happen afterwards or not at all. This skill puts an order around it. It first says out loud what kind of change this is and how big, so you can correct it before anything runs. Then it looks for code that already does the job, writes a plan and stops for your approval, writes a test that fails before writing the code that makes it pass, gets the change reviewed, and stops again to show you the diff and the proposed commit messages before anything is committed. How much of that happens scales with the size, so a few-line fix does not get a planning document.

## Say this to use it

Any of these will do:

- "add this feature properly, run it through the pipeline"
- "fix this bug, test first"
- "refactor this safely"

Or, to be certain this skill and no other one runs:

```
/long-projects:orch-pipeline
```

It will tell you the kind of change and the size it judged, in one line, so you can override it. After that it asks you twice: once to approve the plan, once to approve the commit. Between those two points it works without checking in.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Operation: fix. Size: small. Phases: research, implement, review, commit.

Plan (Gate 1, waiting on you):
  1. Reproduce the empty-cart total as a failing test.
  2. Fix the rounding in the totals function.
  3. Run the whole suite.

[you approve]

  test_empty_cart_total  FAILED   (the failing test, run before the fix)
  test_empty_cart_total  passed   (after the fix)
  48 passed, 0 failed
  Review: one advisory finding, no blocking findings.

Gate 2, waiting on you. One file changed, one test added.
  Proposed message: "fix: round cart totals to 2dp when the cart is empty"
Nothing is committed until you confirm. Pushing is never part of this skill.
```

## Good to know

- **It changes code in the repository you point it at.** Source and test files are edited at the implement step. A refactor moves or removes files where your change calls for that.
- **It makes git commits, and only after you confirm.** You see the diff summary, the review findings and the proposed messages first. It never pushes.
- **It runs your repository's own test command, repeatedly.** If the repository has no test command it can run, it stops and asks instead of skipping the evidence.
- **A test that was written but never run does not count.** The skill requires the failing run and the passing run to have actually happened before a task counts as done.
- **It starts up to three extra Claude helpers at the review step.** That costs tokens and time. Small changes are reviewed inline instead.
- **It may look online once.** At the research step it can search for an existing implementation before new code is written. Nothing else in it goes online, and it handles no keys or passwords.
- **It leans on other packs of this library.** The planning, review and security steps call skills in `turn-reduction`, `verification-kit` and `foundry-core`. Those steps need those packs installed.
- **It stops rather than guessing.** A defect it cannot reproduce as a failing test is reported, not fixed blind. A change that turns out bigger than stated goes back to the planning step under its real size.
- **It was adapted from someone else's project.** The original is an MIT-licensed skill from the ECC project, and the skill records what was deliberately left behind.

## What next

- Want the review on its own, for a pull request or for changes already in your working copy? That is [orch-review](../orch-review/).
- Is the change big enough to span sessions and end in something you cannot undo? Use [phased-harness](../phased-harness/) instead.
- Is the risk in the infrastructure rather than the code? Start with [plan-gate](../../../turn-reduction/skills/plan-gate/).
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
