# foundry-core

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

Claude Code says a task is done when the work looks done. The file was written but never run. The tests were added but never executed. A tool printed "success" and nobody opened what it claimed to produce. All of that reads as finished and fails later, when it costs more. The same problem runs the other way too: asked to fix something, Claude Code will try, check nothing, try again, and keep going with no limit and no record of what it already tried.

This pack sets one rule, that work is done when there is evidence it ran, and gives Claude Code the pieces to produce that evidence. There is a standard for what counts as evidence, a format for writing it down, a way to agree what "done" means before work starts, a way to measure how often something works instead of whether it worked once, and an automatic check that runs your own test command after every turn and gives up after a set number of attempts.

## When would I use this?

- Claude Code told you something works and you want to see the command that proves it.
- You are about to ask for a fix and you do not want it retried forever.
- Your request is vague, such as "clean this up", and you want an agreed target before any work happens.
- You changed a skill or a prompt and want to know whether it still works as often as it did.
- You are reading a report full of the word "verified" and want to know what was actually run.
- Claude Code keeps handing you half a file with a comment saying the rest is similar.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/foundry-core/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [bounded-loop](skills/bounded-loop/README.md) | Sets up an automatic check that runs after every turn, blocks a turn whose check failed with the check's real output, and gives up after a set number of attempts with a written report. | "keep fixing this until the tests pass, but stop after three tries" | Either "target met at attempt N" with the check's own output, or a report saying why it stopped trying. | Adds an entry to your project's `.claude/settings.json` so your check command runs by itself at the end of every turn. Reads every file in the project each time, and writes a state file and a failure report into a `.bounded-loop` folder there. |
| [eval-harness](skills/eval-harness/README.md) | Writes tests for a skill, prompt, hook or agent workflow before it is changed, runs each case several times, and reports how often it passed rather than whether it passed once. | "write evals for this skill and tell me how reliable it is" | An eval file, a log of every trial, and a table of pass rates per case with what no eval covers. | Writes an eval file and a trial log in an `evals` folder beside the thing being tested, and runs that thing several times over, which costs tokens and time. |
| [evidence-report](skills/evidence-report/README.md) | Formats verification results so a reader can tell checked from assumed: one block per claim with the command, its real output and a verdict, closing with a list of what was not checked. | "write this up as an evidence report" | A report in a fixed four-field format, and the result of a script that says whether the report has all its parts. | Runs a small Python program over the one report file you name and prints what is missing. It reads that file only, and writes, moves and deletes nothing. |
| [full-output-enforcement](skills/full-output-enforcement/) | Stops Claude Code cutting its output short: no placeholder comments, no "the rest follows the same pattern", and a clean resumable stopping point when a reply gets too long. | "write the whole file, no placeholders" | Complete files and complete lists, with a marked pause point if the reply has to be split across two messages. | Nothing |
| [goal-spec](skills/goal-spec/README.md) | Turns a vague ask such as "clean this up" into a written target: a check command that can actually be run, a starting measurement taken before work begins, and a limit on attempts. | "turn this into a proper goal before you start" | A short goal file naming the check, the starting measurement, the attempt limit, and who decides it is finished. | Writes a goal file where you agree, runs a one-line validator over it, and runs your own check command once to record where things stand before work starts. |
| [proof-of-work](skills/proof-of-work/README.md) | Requires executed evidence before work is called done: run the thing against real input and show what came back, and confirm any tool that reports its own success by inspecting what it produced. | "prove this actually works before you tell me it's done" | Each claim with the command that tested it, that command's real output, and a list of anything that could not be checked. | Runs your project's own build, type check, lint, test and secret-scan commands plus `git diff --stat`, reads the whole project tree during the secret scan, and saves each command's full output into a log folder you name. |
<!-- /generated:whats-inside -->

Start with `proof-of-work`. It is the rule the rest of the pack serves, and the others attach to a different moment around it: `goal-spec` before work starts, `bounded-loop` while it runs, `evidence-report` when it is written up. Only `bounded-loop` keeps doing anything after you set it up.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | `proof-of-work` reads the artifact you point it at, looks at `package.json`, `tsconfig.json`, `pyproject.toml` and `setup.py` in the current folder to work out which checks your project uses, and reads through the whole project tree during its secret scan.<br>`bounded-loop` reads every file in the project folder you name, every time it runs, to notice what changed between attempts.<br>`goal-spec` reads whatever your request targets, and reads `~/.claude/plugins/installed_plugins.json` to find where it was installed (`~` means your home folder).<br>`evidence-report` reads only the one report file you hand its checker.<br>`eval-harness` reads the skill, prompt or hook under test and the eval files it wrote earlier.<br>`full-output-enforcement` reads nothing. |
| Files written | `bounded-loop` writes a state file and, when it gives up, a report, by default into a `.bounded-loop` folder inside your project. It also tells Claude Code to add an entry to that project's `.claude/settings.json`, the file where Claude Code keeps settings for one project.<br>`proof-of-work` creates a log folder you name and writes one output file and one exit-code file per check, plus a summary table.<br>`goal-spec` writes a goal file, and for a judgment goal a rubric file, at paths you agree on first.<br>`eval-harness` writes an eval file and a trial log in an `evals` folder beside the thing being tested.<br>`evidence-report` and `full-output-enforcement` write nothing. |
| Files deleted or moved | Nothing of yours. `bounded-loop` replaces its own state file each run by writing a fresh copy over it. `proof-of-work`'s self-test deletes the temporary folder it made for itself when it finishes. |
| Programs and scripts | Small programs ship with the pack: one shell script and one Python program for `bounded-loop`, plus four practice scripts; one Python checker for `evidence-report`; one shell validator for `goal-spec`; one shell script and one practice script for `proof-of-work`. They need `bash` and `python3`, two free tools that computers used for programming usually have.<br>The skills also run commands that are yours, not theirs. `proof-of-work` runs your project's build, type check, lint, tests and secret scan, and `git diff --stat`; depending on your project that means npm, npx, pytest, ruff, pyright or git. A tool that is missing is reported as not run, never as passed.<br>`goal-spec` runs your check command once to record a starting measurement.<br>`bounded-loop` runs your check command through `bash` once at the end of every turn, by itself, until it passes or the attempts run out. A turn is one round of you asking and Claude Code answering.<br>`eval-harness` runs the thing under test repeatedly, three times per case by default, and runs each check you wrote for it, including once on purpose to make it fail. |
| Internet access | None from the pack's own programs. Three skills run commands you named, so if your command goes online, it goes online: `bounded-loop`'s check, `goal-spec`'s starting measurement, and `proof-of-work`'s build and tests, which commonly download from the internet. `proof-of-work` runs the type check in a mode that never downloads. `eval-harness` goes online only if the thing under test does. Nothing here sends your files anywhere. |
| Accounts, keys or passwords | No skill asks for a key or a password, and none signs in to anything. Two things to know. `proof-of-work`'s secret scan deliberately searches your files for text shaped like a key and writes what it finds into its log folder in plain text, so treat that folder as private. `bounded-loop`'s state file keeps each attempt's full output and its report keeps the last failing output word for word, so a password your check command happens to print ends up in a file inside your project. `eval-harness` requires a person's decision, written into the eval file, before any change that widens what a tool may do or touches secrets. |

Two limits. First, two of the checkers here are weaker than they sound, and both say so themselves. `evidence-report`'s script can tell that a report has an output section; it cannot tell whether the check was ever run. `goal-spec`'s validator looks for field names at the start of a line, so it accepts a goal file that is not correctly formatted as long as the names are there. Second, two skills point at the author's own computer. `goal-spec`'s instructions for running its validator name a folder that exists only on his machine, though the paragraph straight after tells an installed reader to use the installed copy's own folder instead. `proof-of-work` looks for a secret-scanning program under `~/skill-library`; on any other computer it does not find one and quietly falls back to a plain text search for key-shaped strings.

## How the skills work together

They form one sequence, and you can enter it at any point:

1. **Before work starts:** `goal-spec` turns the ask into a written target, with a check command and a limit on attempts.
2. **While work runs:** `bounded-loop` runs that check after every turn and gives up at the limit with a report. `full-output-enforcement` keeps the output whole while it is being written.
3. **Before anything is called done:** `proof-of-work` sets what counts as evidence.
4. **When it is written up:** `evidence-report` is the format, including the mandatory list of what was not checked.
5. **Over time:** `eval-harness` measures how often a skill, prompt or workflow succeeds, rather than whether it succeeded once.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install foundry-core@skill-library
```

The first line is only needed once, however many packs you install.

`bounded-loop`, `goal-spec` and `proof-of-work` need `bash`. `bounded-loop`, `evidence-report` and `proof-of-work` need `python3`. `proof-of-work` also needs whichever of npm, npx, pytest, ruff, pyright and git your own project's checks call for. `eval-harness` and `full-output-enforcement` need nothing beyond Claude Code itself.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
