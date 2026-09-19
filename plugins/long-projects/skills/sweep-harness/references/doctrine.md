# Sweep-harness doctrine: why each rule exists

Recovered from a design session (2026-08-12) that named three specific failure modes
of large batch jobs, and traced the fix for the third straight back to a real
incident: the 2026-08-09 skill-migration retro, where two agents appending to one
tracker "only worked by luck." That retro is a harness spec that was never written
down as one until this skill.

## The three failure modes this harness fixes

| Failure | Fix |
|---|---|
| You can't tell when you're done | A frozen manifest turns "done" into `pending == 0`, a count, not a judgment call |
| Interruption is expensive | Per-item state files make resume free: re-read the directory, recompute pending |
| Parallel agents clobber shared state | Workers never share a write target; only the orchestrator writes shared files |

## Why enumeration is its own gated step

Discovering the item list and starting work in the same breath means the list can
still grow or shrink while work is in flight, and nothing can ever prove the sweep
finished: the target was moving. Freezing the manifest first, and committing it
before any worker runs, converts "am I done?" from a judgment call into arithmetic:
count the rows, count the terminal state files, subtract. If scope needs to change
mid-sweep, that is a new decision (a new manifest version), not a silent edit to the
frozen one.

## Why per-item state files, never a shared tracker

Two agents writing the same file concurrently produce a file that is neither agent's
version. This is not a hypothetical, it happened during the skill-migration run this
harness generalizes from. The structural fix is not "be more careful," it is "make the
collision impossible": give every worker a target only it will ever write. A worker
that touches `state/item-0001.md` and nothing else cannot corrupt `item-0002.md` no
matter how many workers run at once. The orchestrator is the sole writer of anything
more than one item needs to know about (`MANIFEST.tsv`, `failures.md`), so there is
exactly one place where "two writers, one file" could recur, and it is a single
single-threaded session, not N parallel subagents.

## Why the poisoned item is mandatory, not optional

A validator, gate, or done-check that has never been observed to fail is not known to
work. It is only known to exit cleanly, which an empty loop also does. Planting one
manifest entry that is guaranteed to fail the treatment (a target that does not exist,
an input that cannot parse, whatever "must fail" means for this sweep) and watching it
land in `failures.md` with real evidence is the sweep harness's version of the
machine-wide rule: a gate is trusted only after being proven by deliberate failure. If
the poisoned item comes back `done`, the bug is in the worker's done-check, and every
other "done" in the manifest is now suspect too: that is exactly the failure mode
this catches before it reaches a real item.

## Why failures never block the sweep

A batch job that halts on the first failure turns N-1 successful items into zero
progress reported. Recording the failure and moving on keeps the sweep's throughput
independent of any single item's outcome; `failures.md` exists precisely so failures
have somewhere to land that is not "stop everything." Triage happens once, at the end
or at a natural pause, over the accumulated list, not item by item as they occur.

## Why idempotency is a worker requirement, not a nice-to-have

Sweeps get interrupted: context limits, crashes, a batch that only partially
dispatches. The recovery story only works if re-running a worker against an
already-done item is a no-op that costs one file read, not a redo of real work. This
is also what makes "resume is just re-reading the directory" true rather than
aspirational: if workers were not idempotent, resuming would require reconstructing
exactly where the last run stopped, which is the state of affairs this harness exists
to avoid.

## Relationship to rulings-harness

A sweep's per-item treatment is often, itself, a measured routing rule: "try tool A,
fall back to tool B" is the anydoc-vs-markitdown ruling made into a worker. When that
is the case, `WORKER.md` should point at the ruling file rather than re-deriving the
rule in its own words. The ruling is the worker logic; when the ruling changes (a
falsifier fires, a re-test moves the numbers), the worker changes with it without
anyone having to remember to update two places.

## What this is not

- Not for heterogeneous work. A sweep assumes one treatment for every item; if the
  treatment forks by item type, that is several sweeps or a `phased-harness` job.
- Not a task runner for open-ended work. Every item must have a checkable done state
  up front, or the manifest is just a list, not a gate.
