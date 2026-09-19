# Working through a long list of items

Part of the [long-projects](../../README.md) pack.

Four hundred files that all need the same treatment will not fit in one conversation, and halfway through nobody can say how many are actually done. This skill sets that job up so the answer is a count rather than an impression. It runs your own listing command once, writes every item into a frozen list, and creates a folder holding that list, the instructions for treating one item, one state file per item, a file for the failures, and a `/sweep` command that later sessions run. Because the list cannot grow once it is frozen, "how many are left" is the items with no finished state file. It also insists on one item that is certain to fail, so you can see the failure handling work before you trust it.

## Say this to use it

Any of these will do:

- "set up a sweep over all 400 of these"
- "I need to re-check every file in this folder, more than fits in one go"
- "sweep harness for every repo in the org"

Or, to be certain this skill and no other one runs:

```
/long-projects:sweep-harness
```

It asks seven things in one batch: the command that lists the items, what to do to one item, what proves one item is finished, one item you know will fail, how many to work on at a time, where the folder should go, and confirmation that one session does all the recording. It will not build the folder with any of those unanswered.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Ran your listing command. 412 items found, plus the item meant to fail: 413.

Created sweep-alt-text/

  MANIFEST.tsv     413 rows   the frozen list, recorded in the project history
  CLAUDE.md         44 lines  who may write what, and what not to touch
  WORKER.md         58 lines  the treatment for one item, and its done check
  state/                      empty, one file per item will appear here
  failures.md        3 lines  header only
  .claude/skills/sweep/SKILL.md   36 lines

Row 413 is images/does-not-exist.png, marked poisoned. It must end up in
failures.md. If it ever lands as done, the done check is broken, not the row.
Do not fix it or remove it.

To start: open a session in sweep-alt-text and run /sweep
```

## Good to know

- **It creates one new folder and does not run the sweep.** What the sweep later does to your files is whatever treatment you wrote, so read `WORKER.md` before running it.
- **It runs your listing command once, while building**, to get the real items instead of a guessed count. If your listing command goes online, that one run goes online. Nothing else here does.
- **It needs git**, the tool programmers use to track changes, to record the frozen list before any work starts. A list that can still grow never reaches zero.
- **The later sweep does not stop between batches.** It works through batch after batch until every item is done or failed. That is deliberate, and it is the thing to be certain about before pointing it at a treatment that changes or removes files.
- **The later sweep starts one Claude helper per item**, several at a time, which costs tokens in proportion to the number of items.
- **One item is required to fail.** It stays in the list permanently as the proof that failures are actually caught.
- **A failed item does not stop the run.** Its state file is marked failed with the evidence, a row goes into `failures.md`, and everything is looked at together at the end.
- **Re-running is safe.** Each item's worker reads that item's own state file first and stops if it is already finished, so resuming after a crash does not redo work.
- **Each worker writes one file and only that file.** The frozen list and the failures file belong to the session running the sweep, never to a helper.
- **It handles no passwords or keys, and creates nothing that runs on a schedule.**

## What next

- A few phases of different kinds rather than many identical items: [phased-harness](../phased-harness/) instead.
- If the treatment is a measured rule that might change, keep it in one file the worker points at: [rulings-harness](../rulings-harness/).
- Checking a batch of generated results without reading every one: [santa-method](../santa-method/).
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
