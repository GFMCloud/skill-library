# long-projects

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

Work that lasts longer than one conversation loses things. The next session does not know which approach was already tried and abandoned. A change gets written and committed without anyone deciding first whether the plan was right. A number that was measured once gets quoted a year later, after it stopped being true. A hundred files all need the same treatment and nobody can say how many are done.

This pack covers those moments. Some of its skills interview you and write a folder of instructions that later sessions follow, so the plan survives when the conversation does not. Some stop and wait for your approval before the step you cannot undo. Some bring in separate Claude helpers that never saw your conversation, to review a change or argue against a decision. One sets up a check that keeps running on a schedule after you have stopped watching.

## When would I use this?

- A conversation is getting long and you want the next one to pick up where this one stopped.
- A job will take days and ends in something you cannot undo, such as deleting the old copy.
- Many files or repositories all need the same treatment and you keep losing count of which are done.
- You are about to make an everyday code change and want the plan approved before code is written, and the change reviewed before it is committed.
- A decision has two or three credible answers and you are not sure you are seeing it straight.
- Something you deployed should be watched, and you want to hear about it only when it changes.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/long-projects/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [change-watch](skills/change-watch/README.md) | Watches one thing that changes on its own timeline, such as an alarm or a pull request, and reports only when it changes, not every time it is checked. | "watch this alarm and only tell me when it changes" | A report on each change, with a diagnosis and any follow-up action either done or queued for your approval. | Sets up a check that keeps running on a schedule afterwards, keeps a small file per watched thing that it rewrites on every check, and runs the reading command you gave it. Needs Python. |
| [council](skills/council/README.md) | Gets three fresh opinions on a decision from helpers that never saw your conversation, after writing its own position down first. | "give me second opinions on this decision" | Four positions side by side, the strongest disagreement named, and a recommendation that says whether it moved. | Runs three extra Claude helpers, which costs tokens and time. It changes nothing on disk. |
| [experiment-harness](skills/experiment-harness/README.md) | Sets up a folder for modeling or analysis work that records each idea and its prediction before you see the result, and keeps a list of ideas already killed. | "set up an experiment harness for this model" | A new project folder with a register of hypotheses, a frozen check to score predictions against, a dead-ideas list, and two commands for later sessions. | Creates one new folder of template files where you tell it to. Later runs use whatever experiment command you write into a run file. |
| [handoff](skills/handoff/README.md) | Writes a summary file that carries one session's work into the next, with each checkable claim tied to the command that proves it, and re-runs those commands when you resume. | "handoff" or "context is getting long, wrap this up" | A markdown file to keep, a prompt block to paste into the next session, and on resume a table of each claim, its command, the real output, and whether it matched. | Writes a handoff file, and when you resume from one it runs every command written inside that file through a shell. Needs Python, the PyYAML package and git. |
| [orch-pipeline](skills/orch-pipeline/README.md) | Takes one ordinary code change through sized steps: plan, stop for your approval, write the failing test first, review, stop again before committing. | "run this fix through the pipeline" | A plan you approve, code and tests changed in your repo, review findings, and commits you confirm before they are made. | Changes source and test files in the repo you point it at, runs that repo's own test command repeatedly, and makes git commits after you confirm. It never pushes. |
| [orch-review](skills/orch-review/README.md) | Reviews a code change with several separate reviewers at once, checks the serious findings a second time, and refuses to say approved when any part of the review did not run. | "review this PR with multiple reviewers" | Findings split into blocking and advisory, each with its reason, and a plain statement when part of the review did not run. | Reads a change and runs several Claude helpers over it. Uses git, and for a pull request the GitHub command line tool gh and the GitHub sign-in you already have. It changes no files. |
| [phased-harness](skills/phased-harness/README.md) | Interviews you about a job that spans many sessions and ends in something you cannot undo, then creates a folder of step-by-step runbooks with approval points that later sessions follow. | "set up a phased project for this migration" | A new project folder with a config file, a state file, an end-state document, one runbook per phase, and a command that resumes the work from disk. | Creates one new folder of instructions and templates. Running the job later is what touches your real files, and it is written to stay undoable until you confirm the final step. |
| [retro](skills/retro/README.md) | Decides whether a session earned a short write-up, and if it did, writes one and proposes where each lesson belongs. | "retro" | One short note for a session that produced a commit, a failure or a decision, with a proposed destination per lesson, or nothing at all. | Reads your past Claude Code conversations stored on your computer, runs git log and git status, and writes one markdown file into the project's .claude/retros/ folder. |
| [rulings-harness](skills/rulings-harness/README.md) | Turns measured decisions into one file each, carrying the evidence, what would prove the decision wrong, and a command to re-check it later. | "turn this benchmark finding into something we re-check" | A rulings folder with an index and one file per decision, plus a command that later flags which decisions may have gone stale. | Creates a folder of decision files with an index, and later runs the re-check command you wrote into each one. It never edits your CLAUDE.md; a migration is handed to you as a proposal. |
| [santa-method](skills/santa-method/README.md) | Has two independent reviewers judge finished writing against one written rubric, for work no test or build can decide. | "check this twice before I publish it" | Both reviewers' verdicts, what each flagged, and either a pass or an escalation to you after three rounds. | Runs two extra Claude helpers per round, up to three rounds, which costs tokens and time. It writes nothing and sends nothing. |
| [sweep-harness](skills/sweep-harness/README.md) | Sets up a batch job over many items that all need the same treatment, with a frozen list, one state file per item, and a deliberately broken item that proves the failure check works. | "run this same check across every repo" | A new folder with the frozen list of items, a worker runbook, a failures file, and a command that works through the items in batches. | Runs your enumeration command once and uses git to commit the frozen list. The later sweep applies your own per-item procedure to every item, in batches, without stopping to ask between batches. |

This pack also ships agents. An **agent** is a helper that Claude Code hands a whole job to; it works on its own and reports back.

| Agent | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [harness-optimizer](agents/harness-optimizer.md) | Audits the configuration of a Claude Code setup, proposes small changes, and proves each one by running a check you name three times. | "tune this harness, it is slow and flaky" | A list of changes tried, the trial results for each, which ones stayed, and which were marked BLOCKED for you to decide. | Edits configuration files in the tree you point it at, after recording how to restore each one, and runs your named check repeatedly. It puts a file back when a check fails, and never applies a permission, credential or safety change. |
| [loop-operator](agents/loop-operator.md) | Watches a job that is already running in a loop and says whether to continue, pause, shrink it, or stop and get a person. | "is this sweep stuck, or should I let it keep going" | One recommendation per checkpoint with its reason, and a plain statement when it cannot supervise because the loop writes nothing down. | Reads the state file and log the running job writes, and runs commands that only look. Its setup blocks the file-editing tools, so it changes nothing. |
<!-- /generated:whats-inside -->

The skills whose names end in `harness` do not do the work themselves. They ask you questions and create a folder of instructions that later sessions follow, and they differ by the shape of the job: a job with an end and a point of no return goes to `phased-harness`, many items needing one treatment to `sweep-harness`, measured decisions that could go stale to `rulings-harness`, and modeling work that never finishes to `experiment-harness`. Everything else acts inside the conversation you are already in, and `handoff` is the one to try first.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | The project or repository you point a skill at, and for `orch-pipeline` and `orch-review` the change itself.<br>`retro` reads your past Claude Code conversations, which are stored on your computer under `~/.claude/projects/` (`~` means your home folder).<br>`handoff` reads a handoff file you point it at, and whatever repository, address or state file its claims name.<br>`change-watch` reads a small state file for each thing being watched, a rules file saying which follow-up actions are allowed, and whatever its reading command returns.<br>The `harness-optimizer` agent reads a Claude Code setup's own configuration files, never product code. The scaffolding skills read your answers to their questions. |
| Files written | `handoff` writes a handoff markdown file, appends a line to one you resume from, and may write a project state file before the conversation is compacted.<br>`retro` writes one short note into `.claude/retros/` in the project, creating that folder if it is missing.<br>`experiment-harness`, `phased-harness`, `sweep-harness` and `rulings-harness` each create one new folder where you tell them to, holding markdown files and templates.<br>`change-watch` rewrites its state file on every check, whether anything changed or not, and writes a report where you said to put one.<br>`orch-pipeline` changes source and test files in the repository you named.<br>The `harness-optimizer` agent edits configuration files, after first recording how to restore each one exactly.<br>`council`, `santa-method`, `orch-review` and the `loop-operator` agent write nothing. |
| Files deleted or moved | None by this pack as its job. `orch-pipeline` moves or removes files only where the change you asked for does, such as a refactor. One test script bundled with `handoff` deletes and rebuilds a throwaway folder at `/tmp/handoff-fixture-repo`, and only that path. The project folders `phased-harness` creates are built around renaming a replaced file with a `.superseded` ending and deleting nothing until its final step, which you confirm. |
| Programs and scripts | Two skills ship small programs of their own, both in Python: `change-watch` ships one that updates its state file and one that decides whether a follow-up action is allowed, and `handoff` ships one that re-checks a handoff's claims plus two test scripts that build a throwaway git repository. Nothing else here ships a program.<br>Skills also run tools already on your computer: your repository's own test command and `git` for `orch-pipeline`, `git` for `retro`, `orch-review` and `sweep-harness`, and the GitHub command line tool `gh` when `orch-review` is given a pull request.<br>Several run commands that you wrote yourself: the reading command in `change-watch`, the experiment command in `experiment-harness`, the re-check command in `rulings-harness`, the enumeration and per-item work in `sweep-harness`, the baseline check named for the `harness-optimizer` agent, and every claim's command in `handoff`.<br>`change-watch` also registers a repeating check that keeps running after you stop: a scheduled task on your computer, or a job in Anthropic's cloud. You register it yourself, and it is the point of the skill.<br>`council`, `santa-method`, `orch-review`, `orch-pipeline`, the generated sweeps and both agents start extra Claude helpers, which costs tokens and time. |
| Internet access | `orch-review` contacts GitHub through `gh` when you give it a pull request; its local mode makes no network calls. `orch-pipeline` may look online for an existing implementation before new code is written. `change-watch` goes online only if the thing being watched is online: two of its three ways of running use Anthropic's cloud or accept an incoming request from a monitoring service, and the local way makes no network calls of its own. `handoff` goes online only if one of the claims you wrote checks something online, such as a deployed address. Nothing else here goes online, and nothing sends your files anywhere. |
| Accounts, keys or passwords | None handled by this pack. `orch-review` uses the GitHub sign-in you already have on your computer, through `gh`, when it is given a pull request. `handoff` tells you to strip keys, tokens and account numbers out of a handoff file before saving it, and to name where the secret lives instead of copying the value. The `harness-optimizer` agent writes up any change that would read or move a credential, widen permissions or weaken a safety control, marks it BLOCKED, and does not apply it. |

Two limits. First, resuming from a handoff file runs every command written inside that file, through a shell, and nothing checks what those commands are. That is how the claims get re-tested, and it means a handoff file written by someone else, or fetched from anywhere you do not control, can run whatever it likes on your computer. Only resume from a handoff file you or your own session wrote. Second, most of what keeps these skills inside their stated limits is written instruction rather than anything enforced. The `harness-optimizer` agent's definition names no list of allowed tools, so nothing but its own instructions keeps it to the configuration files it was pointed at. The project folders `phased-harness` creates include a setup step that tells a later session to run Claude Code's `/fewer-permission-prompts` against each repository the project touches and write the resulting permission rules, which is the one place here where generated instructions reach permission settings. The `loop-operator` agent is the only file in the pack whose limits are enforced by the tools it is denied.

## How the skills work together

They are mostly independent, and each covers a different moment:

1. **Before a long job starts:** pick the folder-making skill that matches its shape, as described above.
2. **Before a decision with no obvious winner:** `council` shows the disagreement before the recommendation.
3. **During an everyday code change:** `orch-pipeline` runs it, and calls `orch-review` for the review step on larger changes.
4. **On a change you did not write:** `orch-review` on its own, for a pull request or for uncommitted local changes.
5. **On finished writing that no test can judge:** `santa-method`.
6. **While a long job is running:** the `loop-operator` agent says whether to let it continue. `change-watch` reports on a source that changes on its own timeline.
7. **When a conversation ends or gets too long:** `handoff` for the next session, `retro` for what this one taught.
8. **When the setup itself is the problem:** the `harness-optimizer` agent tunes configuration and proves each change by repeated trials.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install long-projects@skill-library
```

The first line is only needed once, however many packs you install.

Some skills need other software. `handoff` needs Python, the PyYAML package and `git`; its claim checker stops with an install message if PyYAML is missing. `change-watch` needs Python. `orch-pipeline` needs a repository with a test command it can run, and stops and asks if there is none. `orch-review` needs `git`, and for pull requests the GitHub command line tool `gh` and a GitHub sign-in; without `gh` it tells you to use local mode instead. `sweep-harness` needs `git` to commit its frozen list.

Some skills call skills in other packs of this library: `orch-pipeline`, `orch-review` and `santa-method` name `verification-kit`, `turn-reduction` and `foundry-core`; `retro` names the transcript-reading agent in `agent-tooling`; `change-watch` names `schedule-harness` in `voice-and-editing` for its scheduled option and `smoke-gate` in `verification-kit` as an optional extra. Those parts do not work until the named pack is installed too.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
