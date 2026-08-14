# experiment-<NAME>: guardrails

Pointer: general working agreements live in `~/.claude/CLAUDE.md`. This file states
only what is specific to this experiment harness.

## What this project is

`<ONE PARAGRAPH: what is being modeled or analyzed, and why re-derivation was
costing time before this harness existed.>`

## Ownership

- **The orchestrator (the session running `/hypothesis` or `/run`) owns:**
  `REGISTER.md`, `HOLDOUT.md`, `dead-ideas.md`. Nothing else writes these files.
- **Each run owns exactly one file:** its own `runs/run-<NNNN>-<slug>.md`.

## The predict-before-look gate

`/run` will not fill in a run file's Result or Verdict section unless that file's
Hypothesis, Prediction, and Config sections already exist and were saved *before* the
run executed. This is the harness's core rule: **state the prediction before you
look.** Do not work around it by writing Prediction and Result in the same pass.

## The holdout is frozen

`HOLDOUT.md` names what is frozen and since when. Do not fit, tune, or adjust
anything against the holdout after it is frozen: that defeats the reason it exists.
Any change to the holdout is a new freeze, dated, with the old one superseded and
named in `HOLDOUT.md`, not silently overwritten.

## Do-not-touch

- `REGISTER.md`: append-only. Existing rows change status only (`open` → `tested` →
  `killed`); never rewrite a Prediction after its run has landed.
- `dead-ideas.md`: append-only.
- Any other run's `runs/run-*.md`.

## Commits

`<WHO/WHEN: e.g. orchestrator commits after every run, and after every dead-ideas
entry.>`
