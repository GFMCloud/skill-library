# Checking writing twice, with two reviewers

Part of the [long-projects](../../README.md) pack.

Code has tests. A page of writing, a customer email, a set of documentation or a batch of generated entries has nothing that can say pass or fail, and the one thing that should not check it is whatever wrote it, because it will miss what it missed the first time. This skill writes down a rubric, a list of criteria each with a condition that can be judged yes or no, then gives the work to two fresh Claude reviewers that see the rubric and the work and nothing else: not the conversation, not each other. It passes only when both say pass. Otherwise it fixes only the things they flagged and sends it to two new reviewers, and after three rounds it stops and hands the open issues to you.

## Say this to use it

Any of these will do:

- "santa method this before I send it"
- "check it twice with two independent reviewers"
- "I am publishing this tomorrow, get a second and third opinion"

Or, to be certain this skill and no other one runs:

```
/long-projects:santa-method
```

It needs three things: what the work was supposed to do, the work itself, and a rubric. If you have no rubric it writes one and shows it to you before the first round. It will not keep a criterion that comes down to taste, so "make it read nicely" gets rewritten into something a reviewer can decide or dropped.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Santa: April customer newsletter   rounds: 2   result: PASS

Round 1: reviewer B FAIL, reviewer C FAIL; issues 4 (flagged by both 1, by one 3)
  both:  the 40% figure appears nowhere in the source notes
  B only: the support address in paragraph 4 is not the one in the spec
  B only: the promised "see the table below" has no table
  C only: paragraph 2 says the change is live, paragraph 6 says next month

Round 2: reviewer D PASS, reviewer E PASS

Fixed: the 40% figure removed, address corrected, table added, dates
       reconciled to next month.
Open:  none.
Not checked: tone and house style. The rubric has no criterion either
       reviewer could decide on those.
```

## Good to know

- **It writes nothing and sends nothing.** It reports, and the work stays with you. Publishing is always your own action afterwards.
- **It starts two Claude helpers per round, up to three rounds.** That costs roughly two to three times what producing the work cost. There is no single-reviewer mode: one reviewer is not this method.
- **It reads only what you give it**, the specification, the work and the rubric. It goes online for nothing and handles no passwords or keys.
- **It asks you to break something on purpose, once.** Before a rubric is trusted, it wants a known fault planted in the work so you can see both reviewers fail it. A rubric that has never rejected anything is not known to work.
- **Fixes are limited to what was flagged.** No tidying, no improvements nobody asked for, because a change nobody reviewed is a change nobody reviewed.
- **Every round gets new reviewers.** A reviewer that saw the last round is anchored by it.
- **After three rounds it stops.** You get the work, the issues still open and the history of the rounds, and the decision is yours.
- **For a large batch it checks a sample**, about fifteen percent and at least five items, then fixes patterns across the whole batch. A clean sample is evidence about the sample, and it says so along with the sample size.
- **Two reviewers can share a blind spot.** Independence reduces that, it does not remove it. For anything that really matters, read some of it yourself.
- **The effectiveness numbers from the project this was adapted from were deliberately left out**, because none of them has been measured here.
- **It needs [foundry-core](../../../foundry-core/README.md) only if you want the fix rounds run unattended** with a limit on attempts.

## What next

- For code, where several reviewers each take a different angle: [orch-review](../orch-review/).
- To gate one proposed change against its stated goal before it is made: [review-pair](../../../verification-kit/skills/review-pair/).
- If the question is which option to choose rather than whether the work is right: [council](../council/).
- To run the fix rounds with a hard attempt limit: [bounded-loop](../../../foundry-core/skills/bounded-loop/).
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
