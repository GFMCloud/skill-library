# Writing up what a session taught you

Part of the [long-projects](../../README.md) pack.

Most working sessions teach you nothing you need to keep. A few teach you something you will otherwise learn again the hard way in a fortnight. This skill checks which kind the session was, and writes a short note only when it was the second kind. It decides that from the record rather than from what Claude Code remembers: it looks at whether anything was actually recorded in the project's history, and it has a helper read back the session transcript for a failure that got fixed or a decision that got made. If none of those happened it writes nothing and says one line. If something did, it writes one short file and says, for each lesson, where that lesson belongs: a standing preference, a note about this project, a structural decision, a check a script could do, or nowhere at all.

## Say this to use it

Any of these will do:

- "retro"
- "log a retro for this session"
- "was there anything worth keeping from today?"

Or, to be certain this skill and no other one runs:

```
/long-projects:retro
```

It asks you nothing. It works out on its own whether the session qualifies, and tells you when it does not. It proposes where each lesson should go and leaves the actual change to you.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Wrote .claude/retros/2026-04-18-image-upload-retry.md

Gate reason: one commit, and one failure that was diagnosed and fixed.

Lesson 1  The uploader retried on a 413 response, which can never succeed.
  Evidence: session transcript line 2210, then commit 8fd41c2.
  Confidence: high.
  Destination: a check, not prose. Proposed as a test case, not written.
  Status: proposed, not applied.

Lesson 2  You prefer the failing output pasted in full rather than summarised.
  Evidence: you said so twice, transcript lines 640 and 1502.
  Destination: your standing preferences.
  Status: proposed. I have not edited anything. Say the word and I will.

Nothing else from this session was worth keeping.
```

## Good to know

- **It reads your own session transcripts.** Those live under `~/.claude/projects/` (`~` means your home folder) and contain whatever you discussed, including anything sensitive you pasted. It passes the reading to a helper and asks that helper only for specific findings, but the material being read is all of it.
- **It writes one file, in one place.** `.claude/retros/` under the project folder, one file per qualifying session, creating that folder if it is not there. It writes nothing anywhere else.
- **It never edits your preferences, your project's CLAUDE.md, or a decisions folder.** It proposes a destination and stops. The edit is yours, or the session's after you agree.
- **Most sessions produce no file at all.** No recorded change, no failure, no decision means one line of explanation and nothing written.
- **It runs `git log` and `git status`** to decide whether anything was recorded. If the project is not tracked by git, the tool programmers use to track changes, that test never passes and the decision rests on the transcript alone.
- **It starts one Claude helper** to read the transcripts, which costs tokens. It does not read them in the main conversation.
- **It goes online for nothing, and creates no scheduled or repeating task.**
- **It needs the [agent-tooling](../../../agent-tooling/README.md) pack**, for the transcript reading helper it calls by name. Without that pack installed the transcript half does not run.
- **On the third time the same thing goes wrong**, it stops proposing a fourth rule and tells you that the two rules already covering it are not working.
- **There is no weekly or cross-session review.** It writes one retro at a time. Nothing reads the collected retros back except its own check for a repeated failure.

## What next

- Carrying the work itself, not the lessons, into the next session: [handoff](../handoff/).
- A lesson that is a measured finding with a shelf life belongs in a register that re-checks it: [rulings-harness](../rulings-harness/).
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
