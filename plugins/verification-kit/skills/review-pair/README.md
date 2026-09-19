# A second opinion before a change is made

Part of the [verification-kit](../../README.md) pack.

When Claude Code writes a change and then reviews its own change, it has already decided the change is right. Asking it again in the same conversation gets the same answer in different words. This skill hands the proposed change to a separate reviewer that has never seen the conversation it came from, and that reviewer gives a plain pass or fail against what the change was supposed to achieve. On a pass the change is applied. On a fail you get the reasons, and one more attempt. On a second fail that raises nothing new, it stops and waits for you.

## Say this to use it

Any of these will do:

- "gate this change with review-pair"
- "get an independent reviewer on this before you apply it"
- "do not apply that until something else has checked it"

Or, to be certain this skill and no other one runs:

```
/verification-kit:review-pair
```

It will ask for two things before it starts. First, a statement of what the change is for: the ask, what done looks like, the check that proves it, and the limits it has to respect. Second, the change itself, not yet applied. If either is missing it stops and asks rather than reviewing against a guess. It will also want a second model, different from the one that wrote the change.

## What you'll get

A written verdict: pass or fail, the reasons, how sure the reviewer is, and for every problem raised, the check that was run and what it printed. The verdict is written down before anything is applied.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
result: fail
severity: high
confidence: 0.8
new_information: true
issues:
  - The change adds the cache but never clears it when a user signs out.
    evidence: rg -n "cache.clear" src/ -> no matches
  - The goal says reads must stay under 200ms. No timing check was run.
    evidence: not-checked: no benchmark exists in this repo

verdict-check.sh: OK (every required field present)
Not applied. Handing the two issues back for one more attempt.
```

## Good to know

- **On a pass, the change is applied to your files.** This is the one skill in this pack that writes to a real target. It applies only on a pass, and only after the verdict has been written down.
- **It starts a second Claude helper for each round of review.** That costs model usage. The helper stops when it returns its verdict.
- **The reviewer is set up to look, not touch,** and it is given only the goal and the change, never the conversation that produced them. It does have a shell, so it can run checks, and whatever access your session has it inherits.
- **It needs a second model, different from the one that wrote the change.** If one is not configured, it stops. Running the reviewer on the same model undoes the whole point.
- **A small checking script runs on the reviewer's answer.** It is `scripts/verdict-check.sh`, it reads only the verdict files it is given, and it changes nothing. It checks the shape of the answer: that every field is there, that a fail lists problems, and that each problem cites a check that was actually run rather than a quoted opinion.
- **That script cannot tell whether a quoted check was really run.** It checks the form of the evidence, not its truth. The reviewer's separation is what the truth rests on.
- **Two fails in a row with nothing new in the second, and it stops.** It will not keep trying. The change is held for you to rule on.
- **One part of the reviewer's instructions points at a file that is not inside the pack.** The list of fields a verdict must carry lives in this repository's `maintainers/` folder, which is not shipped when you install. The reviewer is told to stop rather than invent the fields, so a review may halt asking for that list.
- **It never goes online by itself, and never touches an account, key or password.**

## What next

- No clear statement of what the change is for yet? [goal-spec](../../../foundry-core/skills/goal-spec/) writes one.
- Checking finished work against its acceptance list, rather than gating a change before it lands? That is the `pre-delivery-verifier` agent, described on the [pack page](../../README.md).
- Reviewing writing rather than code? [santa-method](../../../long-projects/skills/santa-method/) uses two independent reviewers on text.
- Back to the [verification-kit pack](../../README.md), or to [skill-library](../../../../README.md).
