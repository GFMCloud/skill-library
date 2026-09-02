---
name: experiment-harness
description: >-
  Scaffold a hypothesis register and run log for an open-ended modeling project
  that has no terminal gate: enforces writing the prediction before you look at
  the result, one file per run with the config that produced it, and a dead-ideas
  list so a killed idea never gets silently re-run. Use for "I keep re-deriving the
  same finding for my model", "track hypotheses for this analysis", "experiment
  harness", "stop me from rationalizing results after I see them", or any
  modeling/analysis project that will never reach a finished state the way a
  migration does. Not for work with a terminal, irreversible finish: that is
  `phased-harness`. Not for N items needing identical treatment: that is
  `sweep-harness`.
metadata:
  maturity: incubator
---

# Experiment harness: scaffold a hypothesis register and run log

This skill **interviews and scaffolds**. It does not run experiments. It births an
`experiment-<name>/` directory with two entry points (`/hypothesis` and `/run`) that
carry the actual predict-then-look discipline in later sessions.

**Design note:** unlike its two siblings, this archetype was recovered as one
paragraph of intent, not a file tree. Everything below the intent statement in Step 1
is this skill's own design, built to deliver that intent and to read as one family
with `sweep-harness` and `rulings-harness`. See
[references/doctrine.md](references/doctrine.md) for exactly what was recovered
versus invented, and why each invented piece takes the shape it does.

## Step 1: Fit test

Recovered intent, stated in full because it is short: a hypothesis register and run
log rather than phases, because a modeling project has no terminal gate. The failure
mode is not losing your place: it is **re-running an idea you already killed** and
**rationalizing a result after seeing it**. `phased-harness` is linear, gated, and
terminal, which fits migrations and launches; a modeling project never finishes.

Build this harness only when **both** hold:

1. **No terminal gate.** The work is iterative modeling, tuning, or analysis with no
   single finish line, a project that keeps generating new hypotheses rather than
   converging on a done state. If there is a terminal, irreversible finish, use
   `phased-harness` instead.
2. **Ideas are cheap to state and easy to re-run by accident.** The project has
   enough hypotheses in flight, or spans enough sessions, that "didn't I already try
   this?" is a real risk, and where seeing a result before committing to a prediction
   is a real risk of post-hoc rationalization.

**Decline, and say why, when:**

- The work has a terminal finish → `phased-harness`.
- It is one-off, single-session analysis with no risk of re-litigating a killed idea
  → just do the analysis; the register buys nothing for a single run.
- There is no way to freeze a holdout or fixed check for predictions to be scored
  against → say so; a register with nothing to predict against cannot gate on
  "before you looked."

## Step 2: Interview

Ask in one batch:

| # | Extract | Why it is load-bearing |
|---|---|---|
| 1 | **What is being modeled**, one paragraph | Frames `CLAUDE.md` and the register header |
| 2 | **The holdout**: the data, scenario set, or fixed check that predictions get scored against, and how it gets frozen | Becomes `HOLDOUT.md`; without it there is nothing to predict against |
| 3 | **Project directory**: where `experiment-<name>/` lives, separate from the model code it studies | Same separation rule as the other two harnesses |
| 4 | **Naming convention for hypotheses/runs**: short slugs, numbering | Used in `REGISTER.md` and `runs/run-NNNN-<slug>.md` |
| 5 | **Who commits**: orchestrator only, confirmed | Binds the generated `CLAUDE.md` |

## Step 3: Scaffold

Create the project directory and instantiate every template. Generated tree:

```text
experiment-<name>/
├── CLAUDE.md                    ← CLAUDE.template.md: the predict-before-look gate, ownership
├── REGISTER.md                   ← REGISTER.template.md: one row per hypothesis, append-only
├── HOLDOUT.md                     ← HOLDOUT.template.md: the frozen check predictions are scored against
├── dead-ideas.md                   ← dead-ideas.template.md: killed hypotheses with reasons
├── runs/
│   └── run-0001-<slug>.md            ← run.template.md: ONE FILE PER RUN
└── .claude/skills/
    ├── hypothesis/SKILL.md            ← hypothesis-dispatch.template.md: `/hypothesis`
    └── run/SKILL.md                    ← run-dispatch.template.md: `/run`
```

Templates: [CLAUDE](templates/CLAUDE.template.md) ·
[REGISTER](templates/REGISTER.template.md) ·
[HOLDOUT](templates/HOLDOUT.template.md) ·
[dead-ideas](templates/dead-ideas.template.md) ·
[run](templates/run.template.md) ·
[hypothesis dispatch](templates/hypothesis-dispatch.template.md) ·
[run dispatch](templates/run-dispatch.template.md)

Rules while instantiating:

1. **Freeze the holdout before any run happens**, and record how, in `HOLDOUT.md`.
   A holdout that can still change is not a check; it is another thing being fit to.
2. **`REGISTER.md` is append-only.** New hypotheses get a new row; existing rows are
   never edited except to flip status (`open` → `tested` → `killed`) and link the run
   that decided it. Rewriting a row's prediction after the fact is exactly the
   rationalization this harness exists to prevent.
3. **Replace every `<PLACEHOLDER>`.** Grep the generated tree for `<` before
   finishing.
4. Do not run any experiment here, scaffolding only.

After writing, verify: `REGISTER.md`, `HOLDOUT.md`, and `dead-ideas.md` all exist with
only their headers filled in (no fabricated example rows); both dispatch skills exist
and name the right files; every relative link resolves. Report the tree with line
counts.

## Generation rules: bake these into every harness

- **The per-run gate: did you state the prediction before you looked.** A run file's
  Hypothesis, Prediction, and Config sections must be written and saved *before* the
  run executes. `/run` refuses to fill in Result/Verdict on a run file whose
  Prediction section is empty: that is the entire enforcement mechanism, and it is a
  per-run gate, not a phase-sequence gate the way `phased-harness` gates work.
- **One result per file, with the config that produced it.** Every run gets its own
  `runs/run-<NNNN>-<slug>.md`; nothing is overwritten. A result without its exact
  config next to it cannot be reproduced or trusted later.
- **Check `dead-ideas.md` before registering a new hypothesis.** `/hypothesis` reads
  it first. A hypothesis that matches a killed one, even worded differently, gets
  flagged for the user to confirm before a new run file is created: this is the
  structural fix for "re-running an idea you already killed."
- **Killing an idea records why.** When a run's verdict is "refuted" or a hypothesis
  is abandoned without running, `/run` or `/hypothesis` appends one row to
  `dead-ideas.md`: the hypothesis, the reason, and a link to the run (if any) that
  decided it.
- **Orchestration**: the session is the orchestrator and owns `REGISTER.md`,
  `HOLDOUT.md`, and `dead-ideas.md`. If a run is delegated to a subagent (e.g. an
  expensive model fit), the subagent writes only its own `runs/run-<NNNN>-<slug>.md`
  and returns; the orchestrator updates `REGISTER.md` and `dead-ideas.md` afterward.
  This is the same per-writer-per-file discipline `sweep-harness` uses, applied to a
  register instead of a manifest.

## Done when

- The tree above exists, fully substituted, no stray `<PLACEHOLDER>`.
- `HOLDOUT.md` states what is frozen and since when.
- `REGISTER.md` and `dead-ideas.md` exist with headers only, ready to append to.
- Both `.claude/skills/hypothesis/SKILL.md` and `.claude/skills/run/SKILL.md` exist
  and each state, explicitly, the predict-before-look gate.
- You told the user the two commands: `/hypothesis` to register and predict,
  `/run` to execute and score.
