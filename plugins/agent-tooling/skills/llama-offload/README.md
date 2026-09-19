# Bulk text work, done on your own computer

Part of the [agent-tooling](../../README.md) pack.

Some jobs are hundreds of items that all need the same small, mechanical change: names spelled four different ways that have to match one list, free-text notes that each need a label from a fixed set, scraped pages that each need the same handful of fields pulled out. This skill hands that grind to a free AI model running on your own computer, through a program called Ollama, and keeps Claude for the parts that need care: designing the instruction, checking a sample, and dealing with the items the local model could not decide. Two things follow from that. It uses far less of your Claude usage, and the data never leaves your machine.

## Say this to use it

Any of these will do:

- "normalize all the names in this spreadsheet against the roster"
- "tag every one of these 400 notes with a stage from this list"
- "run this batch through Ollama locally"

Or, to be certain this skill and no other one runs:

```
/agent-tooling:llama-offload
```

It will check that Ollama is running and that you have a model downloaded. Then it checks the job is the right shape: at least twenty similar items, each one self-contained, wrong answers you could spot by looking, and no judgment needed per item. If any of that does not hold, it tells you and does not hand the work over. Then it runs five to ten items, including messy ones, shows you the results, and waits for you to say yes before doing the rest.

## What you'll get

A sample to approve, then a results file and a count of what happened.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Sample: 6 of 412 items. Approve before I run the rest.

"J. Rodriguez"       ->  Julio Rodriguez
"Rodriguez, Julio"   ->  Julio Rodriguez
"jrod (Sea)"         ->  Julio Rodriguez
"J Rodriguez (LAA)"  ->  UNSURE
"Mike Trout"         ->  Mike Trout
"trout, m"           ->  Mike Trout

Run the full batch? (y/n)

[after you say yes]

Processed: 412 items, written to normalized-names.csv
Format check: 412 of 412 came back in the expected shape
Spot check: 21 items compared against the source, 21 correct
Needs you: 9 items came back UNSURE, listed below
Model check: every response came from the model that was asked for
```

## Good to know

- **You need Ollama already installed and running, with a model downloaded.** The skill checks first. If it is missing, it stops and asks you whether to start it, download a model, or have Claude do the work itself. It will not quietly do the bulk work in the conversation instead.
- **Nothing goes over the internet.** Items are sent to Ollama at `localhost:11434`, a program on your own computer. No website is contacted, and your data does not leave the machine.
- **It writes a marker file while it works.** The file is `~/.claude/state/llama-offload-active` (`~` means your home folder), created at the start and removed at the end, whatever the outcome. It creates the folder if it is not there. That file is the only thing this skill deletes.
- **Results go to a file, not only to the screen.** They are written as the batch runs, so a long job is not lost.
- **It stops for your approval after the sample.** The full batch does not start until you have seen real input and output pairs and said yes.
- **Text that looks like a password is put in front of you first.** If an item contains something shaped like a key, token or password, you see it before it is sent to the local model. It is not removed quietly and not forwarded quietly.
- **No program ships with this skill.** Claude Code writes a short throwaway script for your batch each time, stored beside your task, and its only job is to pass items to Ollama.
- **One safeguard it mentions is not included here.** The instructions refer to a hook that blocks a very large file being read into the conversation while a batch is active. That hook is not part of this pack, so unless you have it from elsewhere, that protection is not in place.
- **It refuses some work on purpose.** Anything needing judgment on each item, money figures and valuations, and writing meant for a customer stay with Claude, however many items there are.

## What next

- Not sure whether a task needs a bigger model or a separate helper at all? [model-effort-advisor](../model-effort-advisor/) answers that before you start.
- Wondering whether the whole job should be run as a large automated workflow instead? [supahcode-review](../supahcode-review/) scores that and often says no.
- Back to the [agent-tooling pack](../../README.md), or to [skill-library](../../../../README.md).
