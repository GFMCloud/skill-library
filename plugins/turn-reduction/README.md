# turn-reduction

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

A lot of the time you spend with Claude Code is spent on the same few things. It starts a job, gets halfway, and discovers it cannot reach a system it needed, so you finish the step by hand. It asks whether it may commit, for the fourth time today. It hands you a command to run that has a blank left in it, so the command fails and you go round again. It changes something important before you saw what it was going to change.

This pack turns each of those into something done once, at the start. Prove the access before the work. Write down what it may do without asking. Read the plan before the change. Check the message before it reaches you.

## When would I use this?

- A job needs a server, a cloud account or a repository, and you would rather find out now than halfway through that it cannot get there.
- You are tired of answering the same permission question in every session.
- Claude Code is about to change cloud settings, a database, a domain or anything you cannot undo, and you want to read the plan first.
- You were handed a command to paste and it did not run as written.
- You keep having to ask "so what do you actually want me to do?" after a long status message.
- A step is about to be handed back to you as impossible, and nobody has tested whether it really is.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/turn-reduction/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [capability-preflight](skills/capability-preflight/README.md) | Proves in one pass that every system a job needs is really reachable, with a real read and a real write each, before the job starts. | "check we can actually reach everything before we start" | A pass or fail report per system, and one combined list of what is blocked with the fix for each. | Runs the shell commands you wrote into a manifest file, which can read, write and delete anything your account can, then prints a pass or fail report. Needs Python. |
| [plan-gate](skills/plan-gate/README.md) | Investigates your project and the live systems a change would touch, then hands back a plan with a goal, up to three questions, numbered assumptions and the files it would change, and stops. | "plan this first, don't write any code yet" | A written plan in four parts, with each assumption stated so you can disagree with it, and nothing changed. | Reads your project files and runs look-only cloud and container commands using logins you already have, then hands back a written plan and stops. |
| [standing-authorization](skills/standing-authorization/README.md) | Keeps a project file of what Claude Code may already do without asking, what it must always ask about, and the limits on each, and checks a question against it. | "set up standing authorization for this project" | A starter permissions file, and on any later question a verdict of already granted, must ask, or not covered yet. | Writes one starter file, and that file then tells Claude it may edit and delete files in the project, run builds, commit, push branches and open pull requests without asking you first, until you cut the list down. Needs Python. |
| [output-lint](skills/output-lint/README.md) | Checks a message or document you are about to send for six specific faults, such as a command with a blank left in it, or a count with nothing behind it. | "lint this before I send it" | A list of what it found, with the line, and a footer naming the two things it did not check. | Runs a small Python program that reads the one draft you point at and prints what it thinks is wrong with it, changing nothing. |
<!-- /generated:whats-inside -->

Two of these are about access and permission: `capability-preflight` asks whether Claude Code *can* reach a system, `standing-authorization` records whether it *may* act without asking you. The other two are about what it gives you: `plan-gate` before a risky change, `output-lint` before a message or instruction reaches you.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | `plan-gate` reads the project the request concerns: code, tests, settings and dependency lists.<br>`output-lint` reads the one draft you point at, and nothing else.<br>`capability-preflight` reads the manifest file you point at, plus whatever the commands you wrote into it read.<br>`standing-authorization` reads the permissions file you name, and the starter example shipped with the pack.<br>Each of the three programs also reads `~/.claude/plugins/installed_plugins.json`, the list Claude Code keeps of where it put your packs, to find itself. `~` means your home folder. |
| Files written | `output-lint` and `plan-gate` write nothing.<br>`standing-authorization` writes one new permissions file at the path you give it, and refuses if a file is already there. Entries in that file then name a file, such as `PROGRESS.md`, that Claude Code is told to log actions into.<br>`capability-preflight` writes its full record to a file only if you ask for it with `--json`. Separately, every system it checks must carry a write test, so a manifest always writes something somewhere. The example in the skill creates a small `.probe` file in your project folder. |
| Files deleted or moved | None by the programs themselves. The example write test in `capability-preflight` removes the `.probe` file it created, and any delete command you put in a manifest will run. |
| Programs and scripts | Three small Python programs ship with the pack, one each for `capability-preflight`, `output-lint` and `standing-authorization`. `plan-gate` ships no program.<br>`capability-preflight` runs every command in your manifest through `bash`, with your own account and settings, so it will run whatever the manifest contains. Before running anything it refuses a manifest containing a few patterns that can hide a failure, such as `||` or `; true`. That is a check on whether the test could report failure, not a limit on what the commands may do.<br>`plan-gate` has Claude Code run look-only commands against live systems: `terraform state list` and `terraform plan -refresh-only`, AWS `describe`, `get` and `list` calls, `kubectl get` and `describe`, and `docker compose ps`. Changing anything at this stage is forbidden.<br>The file `standing-authorization` generates tells Claude Code it may run your tests, linters, formatters and builds, and commit, without asking first. |
| Internet access | None of the three programs makes a network call of its own.<br>`plan-gate` goes online indirectly: the cloud and cluster commands above talk to remote services.<br>A `capability-preflight` manifest can reach the internet, because the skill tells you to write tests for the APIs your work depends on.<br>The starter file from `standing-authorization` pre-approves pushing a branch to a remote and opening a draft pull request. Both go online when Claude Code acts on them. |
| Accounts, keys or passwords | No skill here reads a store of passwords, and none asks you to paste a key into the conversation.<br>`plan-gate` uses the cloud, cluster and container sign-ins already on your computer. It is told never to ask you for a key or token, and to flag any plan that would need one written out in plain text.<br>A `capability-preflight` test that signs in uses the sign-in you already have. The program tries to blank out anything that looks like a token or password before printing what a test returned.<br>The pre-approved push and pull request from `standing-authorization` use your existing GitHub sign-in. Its stop list is written to keep credentials, spending and production on the side that always asks you. |

Two limits. First, `output-lint` prints pieces of your own draft back in its findings, and unlike the other two programs here it blanks nothing out, so a password sitting in a draft will appear in the output. Second, the file `standing-authorization` generates grants a lot out of the box, and the skill tells you twice to cut the list down after generating it. The skill reports that the starter file grants none of ten dangerous test questions, but that result is about how narrowly the wording is matched, not about how far the actions it does grant reach. Read the granted list yourself before relying on it.

## How the skills work together

They are independent, and each covers a different moment. In the order a longer piece of work meets them:

1. **Before the first step:** `capability-preflight` proves every system the work needs is really reachable, and gives you one list of what is not.
2. **Before a change you cannot undo:** `plan-gate` investigates, writes the plan, and stops until you approve it.
3. **Once, per project:** `standing-authorization` records what Claude Code may do without asking, so the same question stops coming back.
4. **Before a message or instruction reaches you:** `output-lint` checks it for faults that would cost you a round trip.

You can use any one of them on its own. `standing-authorization` and `output-lint` work on the same problem from opposite ends: one removes the question, the other improves the questions that are left.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install turn-reduction@skill-library
```

The first line is only needed once, however many packs you install.

This pack needs the `foundry-core` pack, so Claude Code installs that one at the same time. The install message says `+ 1 dependency: foundry-core`.

`capability-preflight`, `output-lint` and `standing-authorization` each need Python 3.9 or newer, a free programming tool that most computers set up for programming already have. `capability-preflight` also needs `bash`, and whichever command-line tools your own tests call. `plan-gate` needs nothing bundled; to look at live systems it uses whichever of `terraform`, the AWS command-line tool, `kubectl` or `docker` you already use and are already signed in to. This pack lists `foundry-core`, another pack from this library, as one it depends on.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
