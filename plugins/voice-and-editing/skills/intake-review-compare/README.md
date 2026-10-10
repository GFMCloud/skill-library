# Turn saved-link reviews into decisions about your skills

Part of the [voice-and-editing](../../README.md) pack.

When you tap "Intake" on a saved link, the readwise-links job writes an independent review of it by a model that knows nothing about your setup. This skill takes a batch of those reviews and compares each one with the skills you already have, the same way source-intake does, then writes one file with a verdict per link (adopt, take named pieces, watch, or skip) and a row per idea worth taking. It changes nothing in your skill library: the file is for you to rule on, and applying a ruling is a separate step.

## Say this to use it

- "compare the intake reviews for #29, #30 and #31"
- "what's worth taking from the links I tapped Intake on?"
- "run the intake consumer on this week's reviews"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:intake-review-compare
```

It checks that both folders are present and unchanged before starting, and stops if either has unsaved changes.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```text
decisions/2026-10-10-intake-29-31.md

#29 code-rendered video studio   HARVEST  2 rows  (target: hyperframes skills)
#30 agent teams                  SKIP     duplicate of the installed orchestration skills
#31 Opus vs Sonnet cost math     WATCH    recheck 2027-01-08

1 question for you: #29 row 2 contradicts the installed motion rules. Keep ours?
```

## Good to know

- **It only works on one particular setup.** It reads `~/work/readwise-links` and `~/skill-library`; on another computer you would have to change both paths.
- **It writes one file and nothing else.** The file goes in `~/work/readwise-links/decisions/`, a folder that repo's local settings tell git to ignore, so the daily job never sees it.
- **It runs extra Claude sessions without write access.** Each review is compared by one headless `claude -p` call allowed only to read files, using your existing Claude sign-in; each is a long read of your skill inventory and the matching skills.
- **Install commands in a review are only reported.** They are quoted under Flags in the decisions file and never run.

## What next

- To apply a row you ruled on, use [source-intake](../source-intake/) with that section of the file as its decisions table.
- For links you tapped "Vault" on, use [vault-ready-ingest](../vault-ready-ingest/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
