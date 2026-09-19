# Handing work over to your next session

Part of the [long-projects](../../README.md) pack.

A long conversation holds a lot that is nowhere else: what you decided, what you tried and threw away, what is half finished, and what to do next. Close it and that is gone. This skill writes it down as one markdown file you keep, so the next conversation starts where this one stopped. It also writes a block of claims, each one a short fact paired with the command that proves it, such as which branch the work is on or how many tests pass. Every claim's value is taken from running that command while the file is being written, never from memory. When you later start a session from that file, the skill runs those commands again against the real thing and shows you which claims still hold.

## Say this to use it

Any of these will do:

- "handoff"
- "context is getting long, wrap this up for a fresh session"
- "here's a handoff file from yesterday, pick it up"

Or, to be certain this skill and no other one runs:

```
/long-projects:handoff
```

When writing a handoff it will ask nothing if the conversation is clearly at a stopping point. If it is not, it asks whether you want to hand over now or keep going. When resuming it asks one question at the end, and only if something is unclear or a claim came back wrong.

## What you'll get

A markdown file to keep, a prompt block to paste into the next conversation, and, when you resume, a table of each claim next to what the command actually printed.

EXAMPLE-PENDING-REAL-RUN

## Good to know

- **Resuming from a handoff file runs the commands written inside that file.** Each claim's check is passed straight to a shell and run on your computer, with nothing checking first what the command is, because that is how the claim gets re-tested. A handoff file written by someone else, or fetched from anywhere you do not control, can therefore run whatever it likes. Only resume from a handoff file you wrote or your own session wrote.
- **Its own text conflicts on this point, and the program is what happens.** Resume Mode says to treat the handoff as prior context and that nothing in it is a command to run, then two lines later says to run each claim's check command. The second is what the code does.
- **It writes a markdown file, and appends one line to a file you resume from.** That line records which session claimed the handoff. It may also write a project state file before a long conversation is compacted. It writes nothing else.
- **It needs Python, the PyYAML package and git.** The claim checker stops with an install message when PyYAML is missing. Git is used to see which files changed after the handoff was written, and by the two test scripts that ship with the skill.
- **One bundled test script deletes a folder, and only one.** It removes and rebuilds a throwaway git repository at `/tmp/handoff-fixture-repo` so the checker can be tested against known good and known bad cases.
- **It goes online only if one of your own claims does.** A claim that checks a deployed address reaches the internet. The skill makes no network calls of its own.
- **It handles no keys or passwords, and tells you to keep them out.** Strip keys, tokens, credentials and account numbers before saving a handoff, and name where the secret lives instead of copying the value. Handoff files get saved, uploaded and re-shared.
- **Two hooks it mentions are not part of this pack.** The skill refers to two small programs of the author's own that run at compaction and at session start. They are not installed with the pack, and the skill works the same without them.

## What next

- Wrapping up a session that also produced a commit or a failure worth recording? [retro](../retro/) writes that up separately.
- About to start work too big for any one session? [phased-harness](../phased-harness/) creates a folder of gated runbooks that later sessions follow.
- Want the claims in a handoff to be worth trusting in the first place? [proof-of-work](../../../foundry-core/skills/proof-of-work/) is about running the real check before saying something is done.
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
