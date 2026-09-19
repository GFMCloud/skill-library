# Deciding once what Claude Code may do

Part of the [turn-reduction](../../README.md) pack.

Claude Code asks permission a lot, and often for the same thing it asked about an hour ago. This skill replaces the repeated asking with one file per project. The file has three parts: a list of things it may do without asking, a list of things it must always ask about, and limits on the ones it may do, such as how many commits it may make before you look. Before sending a question that starts "should I", Claude Code checks the question against that file. If the file already answered it, the question is not sent and the action is taken and logged. If the file says stop, asking is correct. If the file has nothing to say, you get the question, and the answer goes into the file so it cannot be asked a third time.

The skill can generate a starter file for a new project. That starter is deliberately broad, and you are meant to cut it down.

## Say this to use it

Any of these will do:

- "set up standing authorization for this project"
- "stop asking me this every session, write it down"
- "is this something I already said yes to?"

Or, to be certain this skill and no other one runs:

```
/turn-reduction:standing-authorization
```

It will ask for the project's name and for the limits you want, such as how many commits on one branch before you review. A branch is a separate copy of the work kept by git, the tool programmers use to track changes. It refuses to write over a permissions file that already exists.

## What you'll get

A starter permissions file, and from then on a verdict on any question that was about to be asked.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
$ authz.py check authorization.json --ask "should I commit these?"

ALREADY-GRANTED
  action:  commit to a branch that is not the default branch
  ceiling: 10 commits on one branch
  log to:  git history plus a PROGRESS.md line

The question is the defect. Take the action, stay inside the limit, log it.
```

```
$ authz.py check authorization.json --ask "ok to force push this?"

STOP-LISTED
  action: rewrite history

Asking is correct, and stays correct.
```

## Good to know

- **The file it generates grants a lot out of the box.** It tells Claude Code it may create, edit and delete files anywhere in the project, run your tests, linters, formatters and builds, commit, push a branch and open a draft pull request, all without asking you first. The skill says twice to trim that list after generating it. Read it before you rely on it.
- **This is the one skill here that changes what Claude Code does, not what a program does.** The program itself writes one file. The effect comes from Claude Code reading that file and acting on it.
- **Pushing and opening a pull request go online.** They use the GitHub sign-in already on your computer. Nothing here asks you for a key or a password, and it never touches a store of passwords.
- **The stop list is written to keep credentials, spending and production on the asking side.** That is a starting point you should check against your own project, not a guarantee.
- **The "already granted" answer is deliberately reported as a failure.** A question the file had already answered is treated as a defect with a location, not a matter of style, so it can be caught by a check.
- **It matches questions by wording, so it can miss.** A question phrased in words the file did not anticipate comes back as not covered, which means ask. The fix is to add that phrasing, not to widen the wording until everything matches.
- **It checks the shape of the file, not the sense of it.** The check refuses a limit that is named but never given a value, a limit with no unit, an action that mentions a cap without naming one, a granted entry with nowhere to log, and the same wording appearing on both lists. Whether the granted list is the right list for your project is yours to decide.
- **The file covers one project and says nothing about any other.**
- **What it needs first.** Python 3.9 or newer. For the pre-approved commit, push and pull request entries to mean anything, git and a GitHub account of your own.

## What next

- [capability-preflight](../capability-preflight/) proves Claude Code can reach the systems these granted actions assume.
- [output-lint](../output-lint/) improves the questions that are left after this file removes the rest.
- [proof-of-work](../../../foundry-core/skills/proof-of-work/) in the `foundry-core` pack is what should happen after an action taken without asking.
- Back to the [turn-reduction pack](../../README.md), or to [skill-library](../../../../README.md).
