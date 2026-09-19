# Proving work is done

Part of the [foundry-core](../../README.md) pack.

This skill stops Claude Code telling you a job is finished because it looks finished. Instead it has to run the thing, against real input, and show you what came back: the command, what it was run against, and the output. It applies the same suspicion to tools that announce their own success, so a message saying "validation passed" is followed by opening the thing that was supposedly validated. Where a check genuinely cannot be run, it says so in those words and puts it on a list at the end of the report, rather than filling the gap with reasoning about why it probably works.

## Say this to use it

Any of these will do:

- "prove this actually works before you tell me it's done"
- "run the real checks and show me the output"
- "it says the deploy succeeded, verify that"

Or, to be certain this skill and no other one runs:

```
/foundry-core:proof-of-work
```

It will ask what kind of thing it is checking (code, a document, something you deployed, data, or a settings file) and what to run it against. For code it will also ask where to put the log folder, because it saves each check's full output there.

## What you'll get

A short report in which every claim carries the command that tested it, that command's real output, and a closing list of anything that could not be checked and why.

EXAMPLE-PENDING-REAL-RUN

## Good to know

- **It runs your project's own commands, not its own.** Build, type check, lint, tests, a secret scan, and `git diff --stat`. Which ones actually run depends on your project, so that may mean npm, npx, pytest, ruff, pyright or git.
- **A missing tool is reported as not run, never as passed.** If your computer has no `pytest`, that check is recorded as not done and goes on the not-checked list.
- **It saves every command's full output into a log folder you name.** One output file and one exit-code file per check, plus a summary table.
- **Its secret scan copies what it finds into that log.** The scan looks through your whole project for text shaped like a key or a password, and writes the matches into a plain text file in the log folder. Treat that folder as private, and delete it when you are done with it.
- **Your build and tests commonly download things.** The skill itself contacts nothing. The type check is run in a mode that never downloads.
- **It looks for a secret-scanning program under `~/skill-library`.** That is a folder on the author's own computer (`~` means your home folder). On any other computer it does not find one and falls back to a plain text search for key-shaped strings.
- **It never asks for a key, a password or a sign-in.**
- **It needs `bash` and `python3`,** two free tools that computers used for programming usually have.

## What next

- Once the evidence exists, [Writing up the evidence](../evidence-report/) is the format it goes into, including the list of what was not checked.
- Agree the target before the work rather than after: [Agreeing what done means](../goal-spec/).
- For a fix that has to be retried until a check passes, with a limit: [Stopping a fix loop](../bounded-loop/).
- For a document rather than code, the check is its claims against the files it describes: [spec-artifact-diff](../../../consistency-checker/skills/spec-artifact-diff/).
- Back to the [foundry-core pack](../../README.md), or to [skill-library](../../../../README.md).
