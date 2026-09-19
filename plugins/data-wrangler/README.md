# data-wrangler

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

Data arrives in pieces that do not line up. One file calls a customer "Acme Corp.", another calls it "acme co", and a third has an account number and no name at all. Moving that into one clean table looks like a small job until the counts stop matching: a thousand rows went in, nine hundred and forty came out, and nobody can say where the rest went.

This pack gives Claude Code a method for that work. It profiles the data before changing it, matches records by the strongest rule available and never by a guess, and writes down what it decided as a file you keep. Records it cannot match are listed with a reason rather than filled in with something plausible.

## When would I use this?

- You are joining two exports and the names nearly match but not exactly.
- A report is built from several sources and you want to know which rows were dropped and why.
- You are about to assume two similarly named companies, people or products are the same thing.
- The same name cleanup has been done by hand three times and you want it written down once.
- Data has to move from one system or file shape into another and the counts in and out are meant to agree.
- You were handed a finished dataset and want to see the rules it was built with.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/data-wrangler/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [identity-resolution](skills/identity-resolution/README.md) | Decides which records from different sources refer to the same person, company or thing, working down from exact identifiers to agreed name matching, and never guessing. | "do these two customer lists refer to the same companies?" | A mapping table of every spelling and what it was matched to, plus a list of the records it could not match and the reason for each. | Reads the record files you give it and writes a mapping table and a list of unmatched records every time it runs. It deletes and moves nothing. |

This pack also ships agents. An **agent** is a helper that Claude Code hands a whole job to; it works on its own and reports back.

| Agent | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [data-pipeline-owner](agents/data-pipeline-owner.md) | Takes a whole data job from start to finish: looks at the data before changing it, cleans and reshapes it, matches records across sources, and reports rows in, rows out and rows rejected at each stage. | "turn these three exports into one clean table" | The transformed data, the matching rules written down as a file you keep, a list of everything that did not resolve, and a command that reproduces the output from the original files. | Reads the data files you point it at and writes new output files, a mapping table and a reject list every time it runs. It is instructed never to move or delete your originals. |
<!-- /generated:whats-inside -->

Use the skill when the question is only "are these two records the same thing?". Use the agent when a whole job has to be done, from reading the source files to producing the cleaned output.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | `identity-resolution` reads only the record files you give it, plus any mapping table you already have for the same things.<br>The `data-pipeline-owner` agent reads whatever source data you point it at. It also reads instruction files: `identity-resolution` from this pack, and `proof-of-work` and `evidence-report` from the `foundry-core` pack. |
| Files written | Both write files, every time they run. `identity-resolution` writes a mapping table, which lists each spelling and what it was matched to, and a reject ledger, which lists every record it could not match and why. The `data-pipeline-owner` agent writes those two as well, plus the transformed data itself. All of them are new files. |
| Files deleted or moved | None. Neither one deletes or moves your original data. The agent's instructions tell it to copy and write new files and never to move or destroy a source. |
| Programs and scripts | No programs ship with this pack. Both are written instructions only. Neither names a program or script of its own to run. |
| Internet access | None. Nothing here fetches a page or sends anything anywhere. |
| Accounts, keys or passwords | None. |

One limit. The agent's promise not to move or destroy your source files is a written instruction, not something the software prevents. Claude Code can restrict a helper to a fixed set of tools, but this one has to be able to write files, and the tool layer cannot tell the difference between writing a new output and overwriting a source. The agent's own text says this in as many words. If the data is the only copy you have, keep a copy elsewhere before you start.

## How the skills work together

The skill is one step of the job. The agent is the whole job, and it uses that step inside itself.

1. For a matching question on its own, such as whether two lists of company names refer to the same companies, ask for `identity-resolution`. It gives you the mapping table and the list of what did not match.
2. For a whole job, such as turning three exports into one clean table, ask for the `data-pipeline-owner` agent. It looks at the data before changing it, does the matching with the same method, and reports rows in, rows out and rows rejected at every stage.
3. Either way, the mapping table is the part worth keeping. The next time the same names turn up, hand it back and the work is not repeated.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install data-wrangler@skill-library
```

The first line is only needed once, however many packs you install.

This pack needs the `foundry-core` pack, so Claude Code installs that one at the same time. The install message says `+ 1 dependency: foundry-core`.

Nothing in this pack needs other software. The `data-pipeline-owner` agent also draws on two skills from the `foundry-core` pack, `proof-of-work` and `evidence-report`, for its counting and reporting steps. It runs without that pack installed, and does more of what its instructions describe with it.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
