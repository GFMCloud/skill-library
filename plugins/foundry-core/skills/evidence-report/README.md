# Writing up the evidence

Part of the [foundry-core](../../README.md) pack.

This skill fixes the shape of the report you get when Claude Code says work is verified, so you can tell what was checked from what was assumed without reading closely. Every claim gets four things: the claim itself, the command that tested it, that command's actual output quoted rather than described, and a verdict saying which way the work could have failed and now cannot. Every report closes with a list of what was not checked, which is the part most likely to be dropped and the part that makes the rest worth trusting. A small program that ships with the skill reads a finished report and tells you which of those parts are missing.

## Say this to use it

Any of these will do:

- "write this up as an evidence report"
- "report what you checked in the four-field format"
- "check this report has everything it should"

Or, to be certain this skill and no other one runs:

```
/foundry-core:evidence-report
```

It will ask which claims the report covers, and, if you want the report checked mechanically, the path of the report file to run the checker over.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
CLAIM:   The export writes one row per order
CHECK:   wc -l out/orders.csv
OUTPUT:  1284 out/orders.csv
VERDICT: VERIFIED, rules out the silent-drop case (1283 orders plus header)

CLAIM:   The nightly job still runs after the rename
CHECK:   could not run, the schedule lives on the server
OUTPUT:
VERDICT: UNVERIFIED

NOT VERIFIED
- The nightly job: no access to the server from here. Command to paste is in the note above.
- Behaviour with an empty input file: no sample to hand.
```

## Good to know

- **It changes nothing on your computer.** The checker reads the one report file you give it. It writes no files, moves and deletes nothing, and never goes online.
- **The checker is a small Python program and needs `python3`.** It takes exactly one file path and does nothing else.
- **The checker cannot tell whether a check was actually run.** It can only see whether the output field is empty. Its own notes say so. A made-up output would pass it.
- **Its test for an identifier is a guess.** It counts any number, code, timestamp or file path in the claim or the output as enough to identify what the check ran against.
- **A verdict without a failure mode is treated as incomplete.** Saying a claim is verified is not enough; the report has to say what that result rules out.
- **It never asks for a key, a password or a sign-in.**

## What next

- The standard this format reports against, including what counts as evidence in the first place: [Proving work is done](../proof-of-work/).
- Set the target before the work so there is something to report against: [Agreeing what done means](../goal-spec/).
- To have someone else run the real checks before you are told the work is done, the `pre-delivery-verifier` agent on the [verification-kit page](../../../verification-kit/README.md).
- Back to the [foundry-core pack](../../README.md), or to [skill-library](../../../../README.md).
