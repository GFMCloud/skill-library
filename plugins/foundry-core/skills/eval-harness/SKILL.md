---
name: eval-harness
description: >-
  Define and run a formal eval for an agent workflow, prompt, skill or hook before it is
  trusted or changed: capability evals and regression evals written before the change,
  three grader types, and pass@k / pass^k reliability numbers from repeated trials. Use
  when the user says "write evals for this", "eval-driven", "pass@k", "is this skill
  reliable", "did the prompt change regress anything", or before promoting a skill that
  has no eval cases. Not for verifying one finished artifact once (that is
  proof-of-work), and not a test framework for product code. Costs repeated runs: k
  trials per eval case.
metadata:
  maturity: incubator
---

# Eval harness

A check run once says the work passed once. An agent workflow is not deterministic, so
the question that matters is how often it passes. This skill writes the evals before the
change, runs each one more than once, and reports a rate.

Adapted from the ECC project's `eval-harness` skill (MIT, v2.2.1), reviewed 2026-09-17.
Record: `maintainers/reviews/2026-09-17-ecc/`. The source's `/eval` commands and `SHIP IT`
status were not carried over: nothing here declares its own work shippable.

## Inputs

- The workflow, prompt, skill or hook under test, and the change proposed to it (or
  "none, measuring a baseline").
- Where eval files live. Default: `<target>/evals/`, beside the thing under test and
  versioned with it (never in this skill's directory).
- `k`, the trials per case. Default 3.

## Two kinds of eval, both written before the change

**Capability eval**: something the workflow should do after the change that it may not
do now.

```
CAPABILITY EVAL: <name>
Task:      <what the agent is asked to do, verbatim>
Pass when: <observable criteria, each checkable without asking the author>
Grader:    code | model | human
```

**Regression eval**: something that passes today and must keep passing.

```
REGRESSION EVAL: <name>
Baseline:  <commit SHA or checkpoint the pass was recorded at>
Check:     <the command or case>
Grader:    code | model | human
```

When a change is made to fix a failing case, that case is the boundary set and every
case that already passed is the retention set. Both are reported; showing only the
retention set is how a change that fixed nothing gets merged.

## Graders, in order of preference

1. **Code grader.** A command with an exit code: a test, a build, a schema check, a
   `grep -q` for a required pattern. Use it whenever the criterion can be stated
   mechanically.
2. **Model grader.** A separate run scores the output against a written rubric. When
   used, the rubric is in the eval file, the grader does not see which variant it is
   scoring, and its known weakness is stated beside the score: it is a second opinion,
   not a measurement.
3. **Human grader.** Required, never optional, for any change that widens tool
   permissions, touches credentials or secrets, or weakens a safety control. The eval
   is `BLOCKED` until the human's decision is recorded in the eval file.

A flaky grader (one that disagrees with itself on identical input) is removed from the
gate until fixed. Prove each code grader by making it fail once on purpose.

## Metrics

Run every case `k` independent times and record every trial, including failures.

- **pass@k**: at least one of k trials passed. Reliability with retries. Target for
  capability evals: pass@3 at or above 0.90 across the cases.
- **pass^k**: all k trials passed. Stability. Target for regression evals on critical
  paths: pass^3 of 1.00.
- Report cost and wall time per trial beside the rates. A pass rate bought with a
  tripled cost is a finding, not a success.
- Read a before/after difference against noise. It counts only when it exceeds the
  baseline's own run-to-run spread, measured by running the unchanged baseline more
  than once. At k=3 one flipped trial moves a case's pass fraction by a third.

## Traps

- Tuning the prompt until the known cases pass. Hold back at least one case that the
  change was never run against until the final report.
- Measuring only the happy path. Every eval set has at least one case that should be
  refused, stopped or escalated.
- Reporting a rate from one trial. One trial has no rate.

## Verify

The report below exists, every number in it traces to a recorded trial in the run log,
and each code grader has one recorded deliberate failure. Pass means a reader can re-run
any single trial from the file alone and get a result of the same kind.

## Done when

`<target>/evals/<name>.md` holds the definitions, `<target>/evals/<name>.log` holds every trial, and the
report states pass@k and pass^k per case with status `READY FOR REVIEW` or `BLOCKED`.

## Stop when

- A criterion cannot be made observable: hand back the criterion, do not grade it by feel.
- A human-graded case is waiting on its human.
- The trial budget (cases x k) would exceed the token or time budget the user gave; ask
  before running, do not shrink k silently.
- The same trial fails identically twice for an environmental reason (missing tool,
  auth): report it as `not runnable`, not as a failed eval.

## Output contract

Version 1. Consumed by `long-projects:harness-optimizer`.

```
EVAL REPORT: <name>            k=<k>   baseline=<sha>
Capability:  <case>  trials: P F P   pass@k: yes  pass^k: no
Regression:  <case>  trials: P P P   pass@k: yes  pass^k: yes
Cost:        <tokens or seconds per trial, min to max>
Held-out:    <case>  <result>
Not checked: <what no eval covers>
Status:      READY FOR REVIEW | BLOCKED (<which human decision is pending>)
```
