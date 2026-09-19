# Measuring how often it works

Part of the [foundry-core](../../README.md) pack.

A check run once tells you the work passed once. Claude Code does not do the same thing every time, so the question that matters for a skill, a prompt or a saved workflow is how often it works, not whether it worked the time you watched. This skill writes the test cases before the change is made, splits them into the ones that are meant to start passing and the ones that already pass and must keep passing, runs each case several times, and reports a rate for each. It also reports the cost, because a case that only passes now because every run got three times longer is a finding rather than a win.

## Say this to use it

Any of these will do:

- "write evals for this skill and tell me how reliable it is"
- "did that prompt change break anything that used to work?"
- "run this ten times and tell me the pass rate"

Or, to be certain this skill and no other one runs:

```
/foundry-core:eval-harness
```

It will ask what is being tested, what change is proposed to it (or that you are measuring how things stand now, with no change proposed), where the eval files should live, and how many times to run each case. The default is three.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
EVAL REPORT: handoff-skill        k=3   baseline=a41c9e2
Capability:  resumes from a partial file   trials: P F P   pass@k: yes  pass^k: no
Capability:  refuses a file with no claims trials: P P P   pass@k: yes  pass^k: yes
Regression:  writes the claims block       trials: P P P   pass@k: yes  pass^k: yes
Cost:        41s to 96s per trial
Held-out:    resumes after a rename        passed
Not checked: behaviour when the project has no git history
Status:      READY FOR REVIEW
```

"pass@k" means at least one of the runs passed. "pass^k" means all of them did.

## Good to know

- **It runs the thing under test many times, so it costs many times as much.** Three runs per case by default. Tokens, which is how Claude Code counts usage, and wall clock time both multiply by the number of cases.
- **It asks before spending more than you allowed.** If the cases times the runs would exceed the budget you gave, it stops and asks rather than quietly cutting the number of runs down.
- **It writes two files beside the thing being tested.** The eval definitions and a log holding every trial, including the failed ones, in an `evals` folder there. It deletes nothing.
- **It blocks on a person for anything touching permissions or secrets.** A change that widens what a tool may do, touches secrets, or weakens a safety control cannot pass until a person's decision is recorded in the eval file.
- **It proves each of your checks by making it fail once on purpose.** A check that has never failed has not been shown to work.
- **It ships no programs of its own.** It is written instructions. The only things that run are the checks you wrote and the workflow being tested.
- **It goes online only if the thing under test does,** and it never asks for a key, a password or a sign-in.

## What next

- For checking one finished artifact once rather than measuring a rate: [Proving work is done](../proof-of-work/).
- For a loop that runs a check after every turn and gives up at a limit: [Stopping a fix loop](../bounded-loop/).
- For output with no command that can decide it, such as published writing, two independent reviewers instead: [santa-method](../../../long-projects/skills/santa-method/).
- Back to the [foundry-core pack](../../README.md), or to [skill-library](../../../../README.md).
