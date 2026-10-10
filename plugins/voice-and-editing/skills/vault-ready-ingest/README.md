# Move saved-link notes into your knowledge vault, checked against the original

Part of the [voice-and-editing](../../README.md) pack.

The readwise-links job turns links you tap "Vault" on into draft notes, written by a model. Your vault's rule is that generated text is not a source, so those drafts cannot go in as they are. This skill rewrites each draft so that every point it keeps carries a word-for-word quote from the saved article, and a script checks each quote really is in the part of the article it cites. Points nobody can quote are dropped and listed for you. It then adds the notes to one project, re-runs the vault's retrieval test, and saves the batch as one commit you can undo.

## Say this to use it

- "put #30 and #31 in the vault under Claude agent practice"
- "ingest these vault-ready items"
- "add the saved links I tapped Vault on to my knowledge center"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:vault-ready-ingest
```

It asks which project the batch belongs to. If that project has no page in the vault yet, it asks you for the 3 to 5 questions the project should answer before doing anything else, because the vault's import guide makes those your call.

## What you'll get

*This output is from the skill's live test on made-up test data (a fake post and a fake linked page), not a finding about a real saved link.*

```text
new #30
written #30: Knowledge/Opus leads, Sonnet teammates own folders, Fable reviews read-only.md
dropped: 2 point(s), listed in .../logs/dropped.md
retrieval: 3 question(s), 1 pass, 2 gap
committed 7ee1611 in .../vault
```

The note lists five points, each linked to the saved article's record and the section it came from. The planted claim "teams cut token cost by 60 percent", which the test article never makes, is in the dropped list instead.

## Good to know

- **It only works on one particular setup.** It reads `~/work/readwise-links` (and runs that folder's Python environment and scripts) and writes into `~/knowledge-center`; on another computer you would have to change both paths.
- **It writes into your vault and commits there.** It adds files under `Sources/` and `Knowledge/`, edits the project page, `Home.md` and `Retrieval test.md`, and makes one git commit in the vault; it refuses to start if the vault has uncommitted changes or is not a git folder.
- **It runs a program and calls Claude without tools.** The script `scripts/ingest.py` runs `claude -p` with every tool switched off, two to four times per item and once or twice for the retrieval test, using your existing Claude sign-in; nothing else goes online.
- **A quote proves the words are there, not that the point is fair.** A model can quote a true sentence and overstate it, so new notes are marked `draft` until you promote them.
- **Running it twice on the same items does nothing.** Items already in the vault and unchanged are skipped without calling the model.

## What next

- For links you tapped "Intake" on, use [intake-review-compare](../intake-review-compare/) to compare each review with the skills you already have.
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
