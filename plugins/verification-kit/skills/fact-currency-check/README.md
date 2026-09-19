# Checking whether a fact is still true

Part of the [verification-kit](../../README.md) pack.

Research, documentation and notes are written on a particular day, and they keep reading as current long after they stop being true. A version number moves on. A feature that was missing gets built. A page that described how something behaves describes how it used to behave. This skill takes the claims a decision rests on and checks each one against its source today, then tells you which ones changed and what the change breaks. It does not check every claim in a document, on purpose: checking everything is how this step gets skipped.

## Say this to use it

Any of these will do:

- "is this still true?"
- "check these claims before we act on them"
- "that issue is still open, does that mean the feature is missing?"

Or, to be certain this skill and no other one runs:

```
/verification-kit:fact-currency-check
```

It starts by separating the claims that would change your decision from the ones that would not, and it tells you which ones it is leaving unchecked. For anything about how software behaves, it will want to reach the software itself, because the official documentation is not accepted as proof of behavior.

## What you'll get

One line per checked claim: the claim, the source it was checked against, the date it was checked, and whether it is still current, has changed, or could not be checked.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
claim:   Python 3.8 is the oldest version Python still supports
         load-bearing: it sets the floor tiny-notes installs against
source:  python.org release schedule, checked <date>
verdict: CHANGED
new:     <the oldest version that page lists as still supported, on that date>
breaks:  setup.py pins python_requires=">=3.8" on the strength of this claim,
         and the README repeats the number. Both are stale if the floor moved.

claim:   tiny-notes runs unchanged on the oldest supported version
         load-bearing: it decides whether this is a one-line edit or a port
source:  the test suite run under that interpreter
verdict: UNVERIFIABLE, no interpreter of that version on this computer

Not checked, because no decision turns on them:
- the README's "12 tests" figure, a claim about this repo rather than
  about the world
- the wording of the export command's help text
```

## Good to know

- **It goes online.** Checking a claim means going to the first-party source, the published documentation, or the system that records the answer, and reading it today.
- **It may run the software the claim is about.** For a claim about how something behaves, documentation does not count as proof. If the only way to settle it is to run the thing, it runs the thing.
- **It changes nothing.** It reads and reports. No file is written, moved or deleted by it.
- **Without a way to reach the web or the system in question, every claim comes back unverifiable.** It says so rather than guessing at an answer.
- **Every confirmed claim carries the date it was confirmed.** A claim with no date is a claim about an unspecified past, so it treats one as unchecked.
- **An open issue is not proof that something is still missing.** Tickets go stale open far more often than they go stale closed, so it checks whether the work was done, not whether the ticket was tidied.
- **"Nothing found" is treated as a failed search, not as an answer.** It searches again a different way before recording that something does not exist.

## What next

- Checking a document against the code or files it describes, rather than against the outside world? That is [spec-artifact-diff](../../../consistency-checker/skills/spec-artifact-diff/).
- Want the same discipline applied to your own finished work before you call it done? [proof-of-work](../../../foundry-core/skills/proof-of-work/) runs the real check and shows the real output.
- Back to the [verification-kit pack](../../README.md), or to [skill-library](../../../../README.md).
