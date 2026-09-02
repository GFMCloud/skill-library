# Experiment-harness doctrine: recovered intent versus invented scaffold

This archetype is different from its two siblings in kind, not just detail:
`sweep-harness` and `rulings-harness` transcribe a fully designed file tree from a
recovered conversation. This one had exactly one paragraph of design, and the owner's
own ruling on it was: build it, designing the scaffold fresh, rather than pretend to
source fidelity that does not exist. This file draws the line explicitly so a future
reader never mistakes an invented default for a recovered requirement.

## What was recovered (verbatim intent, not paraphrase)

- The purpose: a hypothesis register and run log rather than phases, because a
  modeling project has no terminal gate.
- The failure mode, named exactly: not losing your place, but *re-running an idea you
  already killed* and *rationalizing a result after seeing it*.
- What it enforces: hypothesis written before the run; one result per file with the
  config that produced it; an explicit dead-ideas list with reasons.
- The entry points: `/run` or `/hypothesis`, explicitly not `/phase`.
- The gate model: "did you state the prediction before you looked", a **per-run**
  gate, contrasted directly against `phased-harness`'s **phase-sequence** gate.
- Named artifacts, in one sentence, with no filenames or schema attached: "a
  hypothesis register, a frozen holdout, and a run log."
- The motivating project: the SCL (Sloshball Champions League) fantasy player model,
  cited as actively costing repeated re-derivation.

## What was invented, and why it takes this shape

**The file tree.** No tree was ever given. The shape chosen (`REGISTER.md`,
`HOLDOUT.md`, `dead-ideas.md`, `runs/run-NNNN-<slug>.md`, two dispatch skills under
`.claude/skills/`) follows directly from the three named artifacts (register,
holdout, run log) plus the two named entry points, using the same per-file, one-writer
discipline `sweep-harness` uses for its manifest and state files. Nothing here claims
to be recovered; it is the minimal structure that makes the recovered intent
mechanically checkable.

**Two dispatch skills instead of one.** The recovered text names `/run` and
`/hypothesis` as two distinct entry points, not one skill with two modes. Slash
commands in this library are the skill directory name, so two commands means two
skill directories: `.claude/skills/hypothesis/SKILL.md` and
`.claude/skills/run/SKILL.md`. `rulings-harness`, by contrast, only ever names one
command family (`/rulings check`), so it stays one dispatch skill with two modes.

**The predict-before-look enforcement mechanism.** The recovered text states the gate
("did you state the prediction before you looked") but not how it is enforced. The
chosen mechanism: a run file's Hypothesis/Prediction/Config sections must exist and be
saved before `/run` will touch the Result/Verdict sections of that same file.
Concretely, `/hypothesis` creates the run file with only the first three sections
filled; `/run` is the only entry point that ever writes Result/Verdict, and it refuses
to do so on a run file whose Prediction section is empty. This makes "did you predict
first" a file-existence check, not a promise: the same move `sweep-harness` makes
turning "am I done" from a judgment call into a count.

**Register append-only, not free-form.** Not stated explicitly, but implied by the
failure mode itself: if a hypothesis's row can be edited after its run lands, nothing
stops a prediction from being quietly reworded to match the result, which is exactly
the rationalization-after-seeing-the-result failure this harness exists to prevent.
Append-only with status transitions (`open` → `tested` → `killed`) is the invented
mechanism that makes the recovered failure mode structurally hard to reproduce.

**Dead-ideas check happens on `/hypothesis`, before a run file is created.** The
recovered text says the harness maintains "an explicit dead-ideas list with reasons"
but does not say when it gets consulted. Checking it at hypothesis-registration time,
before any run file exists, is the natural point: that is exactly the moment
"re-running an idea you already killed" would otherwise happen unnoticed.

**The holdout as a named, frozen artifact.** The recovered text lists "a frozen
holdout" alongside the register and run log but never elaborates. This harness treats
it the same way `sweep-harness` treats its manifest: generated once, frozen, and
never touched by ordinary work afterward. Without a frozen check to predict against,
"did you predict before looking" has no target: the holdout is what the prediction
is a prediction *of*.

## Why this reads as one family with sweep-harness and rulings-harness despite being
invented rather than transcribed

All three share the same three moves, applied to different problems:

| Move | sweep-harness | rulings-harness | experiment-harness |
|---|---|---|---|
| Freeze something once, gate on it | the manifest | (less central, rulings accumulate) | the holdout |
| One file per unit, one writer | `state/item-<ID>.md` | `rulings/<slug>.md` | `runs/run-<NNNN>-<slug>.md` |
| A structural proof the gate actually fires | the poisoned item | the falsifier + re-test | the predict-before-look file-order check |

The poisoned item and the predict-before-look check are structurally the same idea
(a gate is not trusted until something forces it to actually fire) applied to two
different domains: a batch job proves its failure detection works; a modeling project
proves its predictions are genuinely prior, not written to match what already
happened.

## What this is not

- Not a phase sequence. There is no "done" for the harness itself; individual runs
  finish, the project does not.
- Not a substitute for `phased-harness` when the modeling work does eventually feed
  into a terminal, irreversible step (e.g. "ship model v2 to production"). That
  terminal step, if and when it exists, is its own `phased-harness` project that can
  cite this register as its evidence trail.
- Not a data pipeline or experiment-tracking platform. It is a discipline for two
  specific failures (silent re-runs and post-hoc rationalization), not a general
  MLOps tool.
