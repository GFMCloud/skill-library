# Judge your installed skills, one slot at a time

Part of the [voice-and-editing](../../README.md) pack.

Once you have a few dozen skills installed, the question is which of them earn their place, and whether somebody else's version of the same thing is better. This skill answers that slot by slot. For each job a skill does, it writes a neutral description of your version and of the rival version, using separate Claude sessions that are given read-only access and are not told which side is yours. Two more sessions then judge those descriptions, in both orders, never seeing the files or the names. The verdict for each slot is worked out from their answers, and the whole thing ends in a table you rule on. The arrangement exists for one reason: asked plainly, a reviewer nearly always decides that the version already installed is the good one.

## Say this to use it

Any of these will do:

- "review my skills and tell me which ones earn their place"
- "compare my skills against this repo"
- "audit my toolkit"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:toolkit-review
```

It will ask which of three sizes to run: `spot` for one to five skills in a single sitting, `set` for a map of five to fifteen slots run as a gated project, or `full`, which adds a behaviour test for the few slots where what matters is whether something actually runs. It pushes you towards the smallest size that fits. It also asks which skills are in scope and which repositories, if any, to compare them against.

## What you'll get

One row per slot, with the verdict, what it rests on, and where that evidence sits on disk.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```text
Run: spot, one-repo.  4 slots.  Tokens used: 318k of a 400k ceiling.

slot                 verdict    judges agreed   rests on
verify-before-done   KEEP OURS  XY and YX yes   theirs checks the build, ours
                                                 checks what a visitor sees
handoff-between-     TAKE       XY and YX yes   theirs carries a re-checkable
sessions             THEIRS                      claims block, ours does not
error-messages       FRAGMENTS  XY and YX yes   two lines of theirs improve
                                                 our step 3
hook-enforcement     ESCALATED  disagreed       sent to a third judge: no
                                                 clear winner, recorded as
                                                 inconclusive

Ambiguous cells: 3, listed in AMBIGUOUS-CELLS.md, read before ruling.
Nothing has been changed in your library yet.
```

## Good to know

- **It builds a working folder and fills it.** Copies of every skill under review, the prompts it built, each description, each judgment, a ledger, a decisions table, lists of files that would change, and a record of what the run cost. It also keeps a snapshot of its own scripts for each batch, so an edit mid-run changes nothing already in flight.
- **Inside that working folder it does delete and rebuild things**, such as the copies and the script snapshot. Outside it, it deletes nothing. At the end it offers you exactly one deletion command, for the downloaded copies only, and never for the working folder itself.
- **It can end by changing files in your skill library and recording those changes in the library's history**, on a separate copy of the work rather than the main one. Sending them anywhere is not part of the run.
- **It never writes anywhere inside your `~/.claude` folder**, and it checks that folder's file list before and after to prove the run left it alone.
- **Eighteen small programs ship with it**, written in shell and Python. They start many separate Claude sessions, and use `jq`, `git`, `find` and `grep`.
- **It goes online**, through those Claude sessions and through downloading any repository you name.
- **At the largest size it runs each hook script inside a container**, which is a sealed copy of a small computer thrown away afterwards, with no internet and with your files attached read only. That part needs Docker installed, and Docker may download the container image the run names.
- **A downloaded project's own code runs only inside that container**, only after you have written a line authorising it, and never through an installer.
- **It checks your GitHub command-line sign-in and uses whatever sign-in the `claude` command already has.** No program in it reads, writes or prints a password or key, and the containers are given none of your settings. It does read your git name and email, to build a list of words the review prompts are forbidden to contain, so the judges cannot work out whose side is whose.
- **It costs real money in tokens.** Roughly a hundred thousand tokens for each side's description and fifty thousand per judge at the smallest size. The run measures its first slot, projects the total, sets a ceiling, and stops when it reaches it.
- **One of its self-test programs writes the literal text `rm -rf /` into a job file on purpose**, then checks that the runner refuses it. That text is never run: the runner accepts only four named programs and stops with an error on anything else. It is there so the safety check is proven by a real failure rather than assumed. If you search this pack for dangerous-looking strings, that is the one you will find.
- **It needs a fair amount in place first:** the Claude Code command line signed in, `jq`, `python3`, `bash`, `git`, the GitHub command-line tool, and a copy of your skill library with nothing unsaved. Docker only for the largest size.
- **It is built around one particular skill library at `~/skill-library`.** If yours lives elsewhere, that path and the review-record folder are what you would have to change.

## What next

- For a single source with no installed rival in play, this is heavier than you need: use [source-intake](../source-intake/).
- For the `set` and `full` sizes it runs as a gated multi-step project: [phased-harness](../../../long-projects/skills/phased-harness/).
- Before handing the ledger to anyone, check every instruction in it can actually be run as written: [output-lint](../../../turn-reduction/skills/output-lint/).
- To find what is missing from your toolkit rather than what is weak in it: [skill-discovery](../skill-discovery/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
