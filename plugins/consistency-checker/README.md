# consistency-checker

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

Documents go out of date without anyone noticing. A README says "18 files" and there are 21. A plan says "every step is tested" and two are not. A design note points at "section 8" of a document that now has seven sections. The files changed and the words did not.

Claude Code reads such a document and believes it. This pack teaches it to do the opposite: treat every checkable sentence as a claim, run a command that could prove the claim wrong, and show you the result.

## When would I use this?

- You are about to publish a README and want to know that its numbers and file names are still true.
- You edited a specification and three other documents repeat parts of it. You want to know which ones are now wrong.
- Someone handed you a status report that says "done" and "verified", and you want to see what that rests on.
- Two documents disagree and you need to know which one matches the real files.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/consistency-checker/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [spec-artifact-diff](skills/spec-artifact-diff/) | Checks one document against the thing it describes, one claim at a time: counts, words like "every" and "only", version numbers, references to other sections. | "does this README still match the code?" | A list of each claim it checked, the command that checked it, and whether the claim held. | Reads the document and the files it describes, and runs commands that only look, such as `find`, `wc` and `git log`. It changes the document only if you then ask it to fix what it found. |

This pack also ships agents. An **agent** is a helper that Claude Code hands a whole job to; it works on its own and reports back.

| Agent | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [cross-document-checker](agents/cross-document-checker.md) | Checks a whole set of documents against each other and against the files they describe, and reports every place two of them disagree. | "check these three docs against each other and against the repo" | A report with four things per problem: the claim, where it is written, what is actually true, and the command that proved it. | Reads the documents and files you point it at and runs commands that only look. It is written never to change a file, even if asked. |
<!-- /generated:whats-inside -->

Use the skill for one document. Use the agent for several documents at once. The agent gives a more trustworthy answer on a set, because it starts fresh and did not write any of the documents it is checking.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | The documents you name, and the files, folders and git history those documents describe. |
| Files written | None by the agent. The skill writes nothing on its own. If you ask it to correct a document after it reports, it edits that document. |
| Files deleted or moved | None. |
| Programs and scripts | No programs ship with this pack. Its instructions have Claude Code run commands that only look at things, such as listing files, counting lines and reading a project's history. For technical readers, those are `ls`, `find`, `wc`, `diff`, `stat`, `git log`, and `claude plugin validate` when the thing being checked is a Claude Code pack. |
| Internet access | None. Nothing here fetches a page or sends anything anywhere. |
| Accounts, keys or passwords | None. |

One limit. The agent is set up without Claude Code's file-editing tools, but it can still run commands, and a command can write a file. What stops it is its written instructions, which tell it to refuse any request to change a file and to report that it refused. That instruction exists because in August 2026 an earlier version, told to "fix the prose while you're in there", did rewrite a file that way. A missing tool is not a guarantee, so we say so here.

## How the skills work together

The skill is the method. The agent is the same method run by a separate helper.

1. For one document, say what you want checked. Claude Code uses `spec-artifact-diff` in your current conversation.
2. For a set of documents, ask for the `cross-document-checker` agent. It follows the same steps, checks the documents against each other as well as against the files, and hands back a report.
3. You decide what to fix. If the document is wrong, the document gets corrected. If the files are wrong, that is separate work. Neither one ever changes the files to make a document come true.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install consistency-checker@skill-library
```

The first line is only needed once, however many packs you install.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
