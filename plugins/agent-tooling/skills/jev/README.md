# Cheap typed judgments with Jev

Part of the [agent-tooling](../../README.md) pack.

Jev is a model from TypeSafe that does one thing: you hand it some evidence and a few narrow questions, and it returns probabilities, not prose. "Is this the same player as that record?" comes back as 0.93. "Which team should handle this ticket?" comes back as a spread across the teams, plus how sure it is. It is fast and very cheap, so it can sit inside a program and judge thousands of items. This skill finds where in your current project that would actually help, says plainly where it would not, and then builds the Jev step into the project and measures it against decisions you have already made.

## Say this to use it

Any of these will do:

- "where could Jev help in this project?"
- "add a Jev check to the matching step"
- "could a cheap typed judgment replace this LLM call?"

Or, to be certain this skill and no other one runs:

```
/agent-tooling:jev
```

It first checks that your TypeSafe key is set, without ever showing it, and that the data is allowed to go to TypeSafe. Then it looks through the project for places where something makes a judgment about each item, and tests each one against one question: can a program gather all the evidence that judgment needs? If it can, Jev is a good fit. If gathering the evidence takes research, it says Jev would add little and stops there. For a good fit it drafts the decision and its definitions from your own data, asks you at most four questions at once, builds the questions into a file you can review, and reports how often Jev agrees with your past decisions.

## What you'll get

A fit verdict first, then, for a good fit, a small set of files in your project and an agreement report.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Fit check
  strong  src/normalize/ids.py:149  player name matching; both records already in code
  weak    scripts/triage.py:88      needs docs fetched per item; the LLM step should keep it
  none    report.py                 writes prose; Jev does not generate text

Built: questions.py, test_questions.py (6 checks pass, no API call), evaluate.py
Tuning set, 18 items:   agrees with your past calls on 15; 2 sent to review
Held-out set, 12 items: agrees on 10; 1 sent to review
Spend: $0.0009
Thresholds are provisional until more held-out runs agree.
```

## Good to know

- **It sends data to TypeSafe's servers.** Each question goes over the internet to `api.typesafe.ai`. Until you have read TypeSafe's data agreement, only public data is sent; the rule lives in one file, `~/work/jev-lab/DATA-DECISION.md` (`~` means your home folder), and the skill reads it every time.
- **Your key is never shown or written down.** It is read from your Keychain through `~/.zshenv`. If it is missing, the skill gives you one line to paste into your own Terminal and stops.
- **It writes files into your project, and only there.** It copies three short Python files into the project and adapts them, and writes results files beside them. It does not touch anything outside the project.
- **It costs a little money per run, and says how much.** Every run prints its spend. Checking one item against a handful of records costs a fraction of a cent.
- **It reports agreement, not accuracy.** Your past decisions are the yardstick, so the report says how often Jev agrees with them.
- **It is new and has been tested on one project.** The numbers it quotes come from a single afternoon of lessons on the weekly scout, which turned out to be a weak fit. Treat its thresholds as starting points.
- **For the question types and the API itself it defers to TypeSafe's own skill**, `typesafe:typesafe-ai`, which reads TypeSafe's current documentation.

## What next

- A batch of text that needs rewriting or tidying rather than judging? [llama-offload](../llama-offload/) does that on your own computer.
- Not sure which Claude model a task needs? [model-effort-advisor](../model-effort-advisor/) answers that first.
- Back to the [agent-tooling pack](../../README.md), or to [skill-library](../../../../README.md).
