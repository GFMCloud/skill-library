---
name: orch-pipeline
description: >-
  Run one routine software change (new feature, behavior tweak, defect fix, refactor, or
  a first slice from a spec) through a right-sized, two-gate pipeline: classify the size,
  research and plan, stop for approval, implement test-first, review, stop again before
  commit. Use when the user says "add this feature", "fix this bug properly", "refactor
  this safely", "run this through the pipeline", or hands over a change that touches more
  than a line or two of product code. Not for multi-session projects that end in an
  irreversible step (that is phased-harness), not for infrastructure with real blast
  radius (start with plan-gate), and not for a typo. Costs up to three subagent spawns
  at the review phase.
metadata:
  maturity: incubator
---

# Orchestrated change pipeline

`phased-harness` gates a project that spans sessions. Nothing in this plugin gates the
ordinary single-session code change, which is where most changes happen. This skill
does, and it scales the ceremony to the size of the change so a one-line fix does not
get a planning document.

Adapted from the ECC project's `orch-pipeline` skill (MIT, v2.2.1), reviewed 2026-09-17.
Record: `maintainers/reviews/2026-09-17-ecc/`. The source delegated each phase to ECC's own
agents and commands, and had five thin wrapper skills, one per operation. Neither was
adopted. Phases here delegate to skills and agents already in this library, and the five
operations are the table below.

## Inputs

- The request, in the user's words.
- The repo, with its own test command and conventions (`CLAUDE.md`, contributing notes).
- For `first-slice` only: the spec or design document.

## Step 0: name the operation and the size, in one line

State both so the user can override before anything runs.

| Operation | When | First move (not optional) |
|---|---|---|
| feature | the capability does not exist yet | research reuse, then plan a thin vertical slice |
| tweak | it works, the desired behavior differs | change the existing tests first, then the behavior |
| fix | behavior is wrong | reproduce it as a failing test before touching the fix |
| refactor | behavior stays, structure improves | tests green before, green after, no behavior change in the diff |
| first-slice | bootstrapping from a spec | extract scope, locked decisions and a feature list; build one end-to-end slice |

Size is the **highest** tier any one signal reaches:

| Tier | Files touched | New dependency or contract | Design ambiguity | Phases |
|---|---|---|---|---|
| trivial | 1, a few lines | none | none | implement, review, commit |
| small | 1 file or function | none | clear after reading the code | light research, implement, review, commit |
| standard | 2 to 5 | maybe a new internal module | one real choice | research, plan, implement, review, commit |
| large | many or cross-cutting | new external dependency, public API, or a spec | several open questions | all, plus scaffold for first-slice |

Anything touching a security trigger (below) or a public contract is at least standard,
whatever the file count.

## Phases

1. **Intake.** Restate the request and what done looks like. Always runs.
2. **Research and reuse.** Look for an existing implementation in the repo, then in
   the ecosystem, before writing new code. Say what was searched.
3. **Plan.** Produce a task list of thin vertical slices. For anything with real blast
   radius use `turn-reduction:plan-gate` instead of an ad-hoc plan. **Gate 1.**
4. **Implement, test-first.** Per task: a failing test that was actually run, the change,
   the passing run. A test that was written but never executed does not count as red.
   When the check must be run until it passes, run the loop under
   `foundry-core:bounded-loop`. Never report a pass that was not executed.
5. **Review.** For standard and large changes run `orch-review` on the local diff, which
   covers the next three in parallel and fails closed. For trivial and small changes,
   inline: `verification-kit:review-pair` on the diff against the task list;
   `verification-kit:silent-failure-hunter` on the changed files; and, when a security
   trigger is touched, a security pass using `verification-kit:security-checklist`.
   High-severity findings are resolved before Gate 2.
6. **Commit.** One commit per logical change, messages in the repo's own convention.
   **Gate 2.**

## The two gates

This pipeline is gated, not autonomous.

- **Gate 1, after Plan.** Present the task list. No implementation code until the user
  approves. Trivial and small changes have no plan, so they have no Gate 1.
- **Gate 2, before Commit.** Present the diff summary, the review findings and the
  proposed messages. No commit until the user confirms. Pushing is never part of this
  skill.

Between the gates the work proceeds without check-ins.

## Security trigger

The diff touches any of: authentication or authorization, user-input handling, database
queries, file-system paths, external API calls, cryptography, secrets or credentials.

## Verify

Before Gate 2, show: the size line from Step 0; the executed failing-then-passing test
output for each task (or, for refactor, the before and after green runs); the review
verdicts; and whether the security pass ran and why. Pass means every task has executed
evidence and no high-severity finding is open. State coverage if the repo measures it;
do not invent a threshold the repo does not have.

## Done when

Gate 2 is confirmed and the commits exist, each scoped to one logical change, with new
or changed behavior covered by a test that was run.

## Stop when

- Gate 1 or Gate 2 is waiting on the user.
- The defect cannot be reproduced as a failing test: report what was tried, do not fix
  blind.
- The size turns out larger than stated (a small change reaches a public contract):
  stop, restate the tier, and re-enter at Plan.
- The bounded loop's attempt budget runs out.
- The repo has no runnable test command: say so and ask, rather than skipping phase 4's
  evidence.

## Output contract

None consumed by other skills. The task list is the only handoff artifact; it lives in
the conversation or, for large changes, in the repo's `docs/`.
