# agent-tooling

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

Claude Code takes whatever you ask in whatever way it happens to start. Two hundred rows that all need the same tiny edit get the same care, and cost the same, as one hard design decision. A job that would be quicker split between several helpers gets done a step at a time instead. And something you worked out three weeks ago in another session is often easier to decide again than to find.

This pack is about how a piece of work gets run, rather than about the work itself. It recommends a model and a thinking level before a task starts, judges whether a job is big enough to deserve a large automated workflow, sends bulk mechanical text work to a model running on your own computer, and looks facts up in your past sessions.

## When would I use this?

- You are about to start a task and do not know whether to use the fastest Claude model or the most capable one.
- You have a few hundred rows, records or notes that all need the same small change made to them.
- The data should not leave your computer, and the work on it is mechanical.
- Someone has suggested running a big automated workflow and you want to know whether it is worth the cost.
- You remember settling something in an earlier Claude Code session and cannot find what you decided.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/agent-tooling/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [llama-offload](skills/llama-offload/README.md) | Hands a large batch of similar, mechanical text jobs to a free AI model running on your own computer, instead of doing each one in the conversation. | "normalize all the names in this spreadsheet against the roster" | A sample you approve first, then a results file and counts of what was processed and what it could not decide. | Writes a marker file under `~/.claude/state` and writes results to a file, and sends each item to an Ollama program already running on your own computer. It shows you a sample and waits for your approval before processing the whole batch. |
| [model-effort-advisor](skills/model-effort-advisor/) | Recommends which Claude model and how much thinking to use for a task, and whether to hand parts of it to separate helpers. | "which model should I use for this?" | A short recommendation naming the model, the effort level, and whether to split the work, with the reasons. | Nothing |
| [supahcode-review](skills/supahcode-review/) | Judges whether the task you have been discussing is large enough to be worth running as a big multi-step automated workflow, and says no when it is not. | "would a workflow help here?" | A score against six criteria, a yes or no verdict, a cost estimate, and on a yes, text you can paste into Claude Code yourself. | Nothing |

This pack also ships agents. An **agent** is a helper that Claude Code hands a whole job to; it works on its own and reports back.

| Agent | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [transcript-scanner](agents/transcript-scanner.md) | Searches your past Claude Code conversations, which are stored on your computer, for specific facts and reports them with the exact file and line. | "find every time I corrected you about deploys last month" | A list of findings, each quoted with the file and line it came from, and a plain statement where nothing was found. | Reads small pieces of your own session log files under `~/.claude/projects`. It writes nothing, changes nothing and goes online for nothing. |
<!-- /generated:whats-inside -->

`model-effort-advisor` answers the question you have before almost any task: which model, and how much thinking. `supahcode-review` answers a larger version of the same question, about whether a whole job should be run as a big automated workflow at all. `llama-offload` is for volume, when the same small change has to be made hundreds of times. The `transcript-scanner` agent is for finding something in work you already did.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | `llama-offload` reads the files you name for a batch job.<br>The `transcript-scanner` agent reads small pieces of your past Claude Code session logs, which are stored on your computer under `~/.claude/projects` (`~` means your home folder).<br>`model-effort-advisor` reads only its own notes.<br>`supahcode-review` reads no files at all; it works from what is already in the conversation. |
| Files written | `llama-offload` writes a marker file at `~/.claude/state/llama-offload-active` while it is working, creating that folder if it is not there, and writes the batch results to a file as it goes.<br>Nothing else in this pack writes anything. |
| Files deleted or moved | Only the marker file that `llama-offload` created itself, which it removes at the end of the run.<br>Nothing else. |
| Programs and scripts | No programs ship with this pack. For a batch job, `llama-offload` has Claude Code write a short throwaway script each time, kept beside your task rather than inside the pack, whose only job is to pass items to Ollama.<br>The `transcript-scanner` agent runs ordinary search tools already on your computer: `grep`, `jq` and `python3`. |
| Internet access | None. `llama-offload` sends items to Ollama at `localhost:11434`, a program running on your own computer, not a website. `model-effort-advisor`'s notes say its list of Claude models can go out of date and name the official documentation page to compare against, but the skill does not go and fetch it. Nothing here loads a page or sends your files anywhere. |
| Accounts, keys or passwords | None. No skill here asks for a key or signs in to anything. Two related rules are worth knowing. If a piece of your batch text looks like a key, token or password, `llama-offload` shows it to you before sending it to the local model; it neither removes it quietly nor forwards it quietly. If the `transcript-scanner` agent finds something credential-shaped in an old conversation, it reports that one exists and where it is, never the value itself. |

Two limits. First, `llama-offload`'s instructions mention a safeguard that stops a very large file being read into the conversation by accident while a batch is running. That safeguard is a hook, and it is not part of this pack. Unless you have it from somewhere else, that particular protection is not there, and the rest of the skill still works. Second, `model-effort-advisor` produces advice, but its own text says that in Claude Code the advice can be acted on straight away, so the session may go on to set a model or start helpers on the strength of it. In the Claude.ai chat app it says the advice is for you to read and nothing more.

## How the skills work together

They do not depend on each other. Each covers a different moment:

1. **Before starting a task:** `model-effort-advisor` says which model, how much thinking, and whether to split the work between helpers.
2. **When the job looks very large:** `supahcode-review` decides whether it deserves a full multi-step workflow, and often says no and names something smaller.
3. **When the volume is mechanical:** `llama-offload` moves the grind off Claude entirely, onto a model running on your own computer.
4. **When you need a fact from earlier work:** the `transcript-scanner` agent finds it in your past sessions and quotes it with its source.

The first two are easy to confuse. `model-effort-advisor` chooses how to run the job you are doing now. `supahcode-review` decides whether the job should be run in a different way altogether.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install agent-tooling@skill-library
```

The first line is only needed once, however many packs you install.

`llama-offload` needs Ollama, a free program that runs an AI model on your own computer, installed and running, with a model already downloaded. The skill checks for this first. If it is missing, it stops and asks you what to do rather than quietly doing the bulk work in the conversation instead. The other skills and the agent need nothing extra.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
