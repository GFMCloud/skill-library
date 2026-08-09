# Phased-harness doctrine — why each rule exists

Distilled from a real run: the machine-wide skill migration executed 2026-08-09
(six phases, two gates, ~63 dispositioned items, completed in one continuous session).
The harness for that run is preserved at `docs/migration/harness/` in this repo and is
the worked example every template here generalizes.

## Why a harness at all

Long-horizon work fails in three specific ways, and each has a structural fix:

| Failure | Fix |
|---|---|
| Context dies mid-run; the next session cannot reconstruct where it was | Files are the source of truth; `STATE.md` is a single resume point kept current *during* work |
| The model asks permission constantly, or asks for none and does something unwanted | Standing authorizations in a file, plus exactly two designed stop points |
| Ambiguity is resolved differently in phase 4 than in phase 1 | One end-state doc, named in advance as the tiebreaker |

A harness is worth its overhead only when the work actually spans sessions and ends
in something irreversible. Below that, it is ceremony — hence the fit test.

## Why the invariant is stated as a state, not tasks

A task list tells you what to do; it cannot tell you whether you are done, and it
cannot arbitrate a question the list did not anticipate. "Every skill has exactly one
editable home" can be checked at any moment, by anyone, without knowing the history —
and it decided a dozen small questions mid-run that no runbook had covered. Any
project whose end state cannot be phrased this way is not a harness candidate; it is
exploration, and the gates have nothing to bind to.

## Why exactly two gates

Every additional gate is a session boundary the user has to be present for. Two is the
minimum that covers the two genuinely different kinds of decision:

- **Gate A is judgment** — dispositions, precedence, which copy wins. Claude can
  *propose* all of it and be right most of the time, but the user owns the call. So
  propose everything, batch it, default to "as proposed", and take one interruption
  however large the table is. Row-by-row confirmation of 63 rows would have been the
  project's dominant cost.
- **Gate B is irreversibility** — the deletions. No amount of prior verification makes
  this delegable, because the cost of being wrong is unbounded. Enumerate, show where
  each item remains recoverable, confirm explicitly.

Everything between them is execution of ratified decisions, and asking "shall I
continue?" there converts a continuous run back into a stop-start one for no
information gain. Anomalies encountered mid-run are the pressure that makes people add
a third gate; logging them with a recommendation and reviewing them at the next gate
relieves that pressure without spending an interruption.

## Why reversibility until Gate B

Renaming with a suffix instead of deleting means every intermediate state is undoable
and — importantly — *inspectable*. The final verification sweep can distinguish "a
live copy that should not exist" from "a retired copy awaiting deletion" by name
alone. That distinction is what made the single-home check mechanically checkable
rather than a judgment call. It also means a mid-run abort leaves a recoverable
system, which is what lets the run be continuous in the first place.

"Move, never copy" is the same principle at the item level: a copy forks silently the
first time someone edits one side, and nothing detects it. This is usually the exact
problem the project exists to fix, so committing it during the fix is self-defeating.

## Why the orchestrator owns shared files

Subagents are cheap and parallel, and the temptation is to let each one update the
tracker as it finishes. Two subagents writing `STATE.md` concurrently produce a file
that is neither one's version — and `STATE.md` is the resume point, so corrupting it
costs the whole run's recoverability. The rule that fell out: subagents get disjoint
subtrees and write their results to their own files; the orchestrator reads those and
is the sole writer of anything shared.

The corollaries are all about keeping the orchestrator's context thin enough to carry
the whole run in one session: subagents read the bulky material and report rows and
diffs, never full bodies; results land in files before the orchestrator moves on; and
the orchestrator's model stays top-tier because it is doing nothing *but* judgment.

Delegation never weakens a guardrail. A subagent that was not told "read-only" will
not infer it, so every prompt restates the guardrails that bind it and names an
explicit do-not-touch list.

## The overridden-plan failure (2026-08-09)

At Gate A the user overrode one proposal: a group of project-specific skills would
*not* become a library plugin but stay where they were. The ruling was recorded
correctly. But the proposal it replaced had carried a side effect nobody restated —
under the original plan, executing that row would have vacated the source directory
and renamed it with the retirement suffix. With the row overridden, no execution task
owned that directory, and it stayed live in a repo that was otherwise fully retired.

Nothing caught it until the final phase's from-scratch sweep, which failed its first
check. The fix was trivial; the lesson is not. **A gate ruling that overrides a
proposal silently orphans that proposal's side effects.** So: whenever a ruling
overrides a proposal, name the side effects it carried — cleanup, retirement,
renaming, deregistration — and explicitly assign each to an owner in a later phase, in
the same breath as recording the ruling.

This is also the argument for the final phase re-verifying the invariant **from
scratch** rather than re-reading the per-phase notes. Every per-phase note was
accurate. The gap was between them.

## Why evidence, not checkmarks

Two things from the same run:

- The validator was proven by writing fixture skills that *had* to fail, running it,
  recording the verbatim failure output, then removing them. A validator that has
  never failed is not known to work — it is known to exit 0, which an empty loop also
  does. The same applies to CI: a deliberately broken PR was opened, confirmed to
  fail, and closed unmerged.
- Verification stalled because headless `claude -p` returned an expired-OAuth error —
  a capability two of the six final checks depended on. A one-line preflight
  (`claude -p "Say OK"`) at the top of the phase would have surfaced it before any
  check was designed around it. Preflight every capability a phase depends on, with a
  real read and a real write, before the phase starts.

`STATE.md` therefore records commands and their actual output. A checkmark records
that someone believed something.

## What this is not

- Not a task runner. The harness does not execute; it constrains and resumes.
- Not for single-turn orchestration or repeatable pipelines — those want a dynamic
  workflow, not a file-based multi-session harness.
- Not a planning document. A plan describes intended actions; the end-state doc
  describes the target state, and the two behave completely differently when
  something unanticipated shows up.
