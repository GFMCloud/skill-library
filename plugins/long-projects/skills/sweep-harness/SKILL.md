---
name: sweep-harness
description: >-
  Scaffold a sweep harness for N items that need identical treatment across more
  work than fits in one context: a frozen manifest, one state file per item, and
  a poisoned item that proves the failure gate before it is trusted. Use for
  "validate every skill in the library", "run this across all our repos",
  "re-check every file in this corpus", "sweep harness", "batch job with more
  items than fit in a context window", or any flat, homogeneous per-item task
  where "am I done?" needs to be a count, not a vibe. Not for a handful of
  distinct, ordered phases (that is `phased-harness`).
metadata:
  maturity: incubator
---

# Sweep harness: scaffold a resumable batch sweep

This skill **interviews and scaffolds**. It does not run the sweep. It births a
`sweep-<name>/` directory; the generated harness (with its own `/sweep` dispatch
skill) does the actual work in later sessions, resumable from disk at any point.

Rationale behind every rule below: [references/doctrine.md](references/doctrine.md).

## Step 1: Fit test

Build a sweep harness only when **all three** hold:

1. **N items, one treatment.** Every item gets the same per-item procedure. If items
   need genuinely different handling, this is not a sweep; it is either several small
   sweeps or a job for `phased-harness`.
2. **More work than fits one context.** Either N is large, or each item's treatment is
   expensive enough that doing them all in one session risks losing track of where you
   are.
3. **Per-item done is checkable.** You can state, for one item, what evidence proves
   it is finished. If you cannot, the sweep has nothing to gate on.

**Decline, and say why, when:**

- N is small enough to just do it in one pass → no harness needed.
- Items are heterogeneous in kind → route to `phased-harness` (ordered, distinct
  phases) or just do the work directly.
- There is no per-item completion check → fix that first; a sweep over an ungated
  task just produces N unverifiable claims of "done".

## Step 2: Interview

Ask in one batch. Do not scaffold with any of these unresolved:

| # | Extract | Why it is load-bearing |
|---|---|---|
| 1 | **How to enumerate the items**: the query, script, or listing that produces the full set | Becomes the one-time generation step for `MANIFEST.tsv` |
| 2 | **The per-item treatment**: what a worker actually does to one item | Becomes `WORKER.md` |
| 3 | **The per-item done check**: the evidence that proves one item finished | Goes in `WORKER.md` and the `item-state` template's evidence field |
| 4 | **A poisoned item**: one entry that must fail the treatment | Required; see Step 3 |
| 5 | **Batch size / parallelism**: how many items to dispatch to subagents at once | Goes in the generated `CLAUDE.md` and dispatch skill |
| 6 | **Project directory**: where `sweep-<name>/` lives | Separate from the corpus being swept |
| 7 | **Who commits**: orchestrator only, confirmed | Binds the generated `CLAUDE.md` |

## Step 3: Scaffold

Create the project directory and instantiate every template. Generated tree:

```text
sweep-<name>/
├── MANIFEST.tsv            ← MANIFEST.template.tsv: frozen enumeration, one row per item
├── CLAUDE.md                ← CLAUDE.template.md: guardrails, ownership, do-not-touch
├── WORKER.md                 ← WORKER.template.md: the per-item runbook
├── state/
│   └── item-0001.md          ← item-state.template.md: ONE FILE PER ITEM
├── failures.md                ← failures.template.md: triage queue, orchestrator only
└── .claude/skills/sweep/
    └── SKILL.md                ← dispatch-SKILL.template.md
```

Templates: [MANIFEST](templates/MANIFEST.template.tsv) ·
[CLAUDE](templates/CLAUDE.template.md) · [WORKER](templates/WORKER.template.md) ·
[item-state](templates/item-state.template.md) ·
[failures](templates/failures.template.md) ·
[dispatch SKILL.md](templates/dispatch-SKILL.template.md)

Rules while instantiating:

1. **Generate the manifest by actually running the enumeration**, not by guessing at a
   count. Write every row, including the poisoned one, then **commit it before any
   worker runs.** Freezing the manifest is what turns "am I done?" into `pending == 0`:
   a manifest that can still grow mid-sweep never reaches zero honestly.
2. **The poisoned item is mandatory.** Add one row that names a target guaranteed to
   fail the treatment (a nonexistent path, a malformed input, whatever "must fail"
   means for this sweep). Label it in the `poisoned` column. The sweep is not proven
   correct until that row lands in `failures.md` with a real failure recorded against
   it. If it lands as `done`, the worker or the done-check is broken, not the item.
3. **Per-item state files, never a shared tracker.** Every worker writes exactly one
   file, its own `state/item-<ID>.md`, and touches nothing else. `MANIFEST.tsv` and
   `failures.md` are orchestrator-only, always.
4. **Replace every `<PLACEHOLDER>`.** Grep the generated tree for `<` before
   finishing.
5. Do not run the sweep here: scaffolding only. The generated `/sweep` skill runs it
   in a later session.

After writing, verify: `MANIFEST.tsv` has a row for every enumerated item plus the
poisoned one; every relative link in the generated files resolves; the dispatch skill
at `.claude/skills/sweep/SKILL.md` names the manifest and state directory correctly.
Report the tree with row/line counts.

## Generation rules: bake these into every harness

- **The worker is idempotent.** Before doing anything, `WORKER.md` requires reading
  the item's own state file if one exists. `status: done` → stop and report already
  done. Anything else → proceed (or retry). A worker that redoes finished work on
  every dispatch turns "resume" into "restart".
- **Failures do not block the sweep.** A failed item gets its state file marked
  `status: failed` with the evidence, and a row in `failures.md`. The orchestrator
  moves on to the next batch; failures are triaged at the end, not mid-run.
- **Resume is re-reading the directory.** `pending = { ids in MANIFEST.tsv } - { ids
  with a terminal state file }`. No other bookkeeping. A crashed session's next
  `/sweep` recomputes this from disk with zero setup.
- **Orchestration**: the session running `/sweep` is the orchestrator. It owns git,
  `MANIFEST.tsv`, and `failures.md`, and never delegates a write to any of them.
  Workers are dispatched as subagents against `WORKER.md`, each given exactly one item
  id and told, explicitly, which files it may not touch.
- **Compose with `rulings-harness`.** When the per-item treatment *is* a ruling (a
  measured, falsifiable routing rule: "try tool A, fall back to tool B on error"),
  point `WORKER.md` at that ruling file instead of restating the rule. The ruling
  changes; the worker changes with it, automatically.

## Done when

- The tree above exists, fully substituted, no stray `<PLACEHOLDER>`.
- `MANIFEST.tsv` is committed and includes the poisoned item.
- `WORKER.md` states the per-item treatment, the done check, and the idempotency
  check explicitly.
- `state/` is empty (no items pre-claimed) and `failures.md` has only its header.
- You told the user the one command that starts the sweep: open a session in the
  project dir and run `/sweep`.
