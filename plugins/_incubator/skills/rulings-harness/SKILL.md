---
name: rulings-harness
description: >-
  Scaffold a rulings register (one file per measured, evidence-backed decision,
  each carrying its evidence, a falsifier, a re-test command, and a revisit date)
  so decisions can be checked instead of merely trusted, and installs a
  `/rulings check` pass that flags any whose falsifier has fired. Use when a
  CLAUDE.md or notes file is accumulating measured findings ("X is 25x faster than
  Y", "use A, fall back to B") that could go stale, when the user says "rulings
  harness", "decisions with a shelf life", "this benchmark might be out of date",
  or "turn this finding into something we re-check". Not for plain preferences:
  see the classification boundary in Step 1.
metadata:
  maturity: incubator
---

# Rulings harness: scaffold a register of checkable decisions

This skill **interviews and scaffolds**. It does not migrate an existing CLAUDE.md
wholesale: that migration is always a separate, reviewed proposal (see Step 3). It
births a `rulings/` directory plus a `/rulings` dispatch skill that records new
rulings and runs the falsifier check in later sessions.

Rationale behind every rule below: [references/doctrine.md](references/doctrine.md).

## Step 1: Fit test and the classification boundary

Build a rulings register only when there is at least one decision that crosses this
boundary, stated exactly as recovered from the original design:

> **It cost something to determine, and a future session would otherwise re-derive
> or violate it.**

Three categories fall out of that line. Get this right before scaffolding anything.
It decides what migrates into a ruling file and what is left alone:

| Category | Test | Destination |
|---|---|---|
| **Preference** | No evidence could falsify it ("don't auto-run `open` on generated files") | Stays in CLAUDE.md, unchanged |
| **Ruling** | Measured, falsifiable, has a natural expiry ("anydoc is 25–55x faster than markitdown; fall back to markitdown on error") | Moves into `rulings/`, gains provenance |
| **Burn-derived** | Learned from a real incident; does not expire because a burn stays a burn, but needs the incident linked | Moves into `rulings/`, `Falsifier: none, burn-derived`, incident cited in Evidence |

**Decline, and say why, when:**

- Nothing in scope is a measured, falsifiable finding → there is nothing for this
  harness to hold; do not scaffold an empty ceremony.
- The user wants to migrate an entire CLAUDE.md in one pass without review → that is
  out of scope for this skill. Migration is a **proposal**, never a direct edit (see
  Step 3). Point them at doing it as a reviewed batch, not through this skill acting
  unsupervised.

## Step 2: Interview

Ask in one batch:

| # | Extract | Why it is load-bearing |
|---|---|---|
| 1 | **Where `rulings/` lives**: which repo or directory, alongside which CLAUDE.md | Rulings only pay off if they are near the file they replaced content in |
| 2 | **The first ruling(s) to seed it with**: real decisions in scope, classified per Step 1 | Populates the initial files; do not scaffold an empty register with no examples |
| 3 | **Who owns `INDEX.md`**: orchestrator/single-writer, confirmed | Same shared-file discipline as every harness in this family |
| 4 | **Revisit cadence default**: how far out a `revisit-by` date should default to when the user has no better answer | Keeps the check pass meaningful instead of everything defaulting to "never" |

## Step 3: Scaffold

Create `rulings/` (and, if requested, the dispatch skill) and instantiate templates.
Generated tree:

```text
<location>/
├── rulings/
│   ├── INDEX.md               ← INDEX.template.md: the enumeration, one row per ruling
│   ├── <slug-1>.md            ← ruling.template.md, one file per ruling
│   └── <slug-2>.md
└── .claude/skills/rulings/
    └── SKILL.md                ← dispatch-SKILL.template.md: `/rulings new` and `/rulings check`
```

Templates: [INDEX](templates/INDEX.template.md) ·
[ruling](templates/ruling.template.md) ·
[dispatch SKILL.md](templates/dispatch-SKILL.template.md)

Rules while instantiating:

1. **One file per ruling**, named by slug, matching the schema in
   [ruling.template.md](templates/ruling.template.md): the ruling as one imperative
   line, **Evidence** (what was measured, when, by what method), **Revisit-by**,
   **Falsifier**, **Re-test**.
2. **`INDEX.md` is the enumeration.** Every ruling file gets exactly one row. Nothing
   else in the harness restates the count or the list. That is how a stale index
   gets caught by inspection instead of drifting silently.
3. **Migrating existing CLAUDE.md content is a proposal, not an in-place edit.**
   When seeding the register from an existing CLAUDE.md, write the candidate ruling
   files and a short diff-style summary of what would be removed from CLAUDE.md, and
   hand that to the user to apply. Never edit CLAUDE.md directly as a side effect of
   running this skill.
4. **Replace every `<PLACEHOLDER>`.** Grep the generated tree for `<` before
   finishing.

After writing, verify: every ruling file has all five required fields non-empty;
`INDEX.md` lists exactly the files present in `rulings/`; every relative link
resolves. Report the tree with line counts.

## The two operating modes of the generated `/rulings` skill

- **`/rulings new`**: classify a candidate decision against the Step 1 boundary
  first. If it is a preference, say so and stop (it does not belong here). If it is a
  ruling or burn-derived, fill the template, append one row to `INDEX.md`, and if the
  source was CLAUDE.md content, produce the removal proposal per rule 3 above rather
  than editing CLAUDE.md.
- **`/rulings check`**: walk every active ruling in `INDEX.md` (skip
  burn-derived entries with `Falsifier: none`) and evaluate its **Falsifier**
  against the world: check an installed version, run the **Re-test** fixture, compare
  against the stated numbers. Hand back a short list of rulings whose falsifier has
  fired or whose `revisit-by` date has passed, each needing re-decision. This pass
  never edits a ruling file itself: re-deciding is a human call, logged as a new
  version of the ruling once made.

## Composition with sweep-harness

A ruling is often the exact routing logic a sweep's `WORKER.md` needs (see
`sweep-harness`). When scaffolding a ruling that a sweep will execute, note the
sweep's `WORKER.md` path in the ruling's body so `/rulings check` firing is a signal
to also revisit that worker.

## Done when

- `rulings/INDEX.md` exists and lists exactly the ruling files present.
- Every seeded ruling file has all five schema fields filled, no `<PLACEHOLDER>`
  left.
- Any CLAUDE.md migration is a written proposal, not an applied edit.
- The dispatch skill at `.claude/skills/rulings/SKILL.md` exists and documents both
  `/rulings new` and `/rulings check`.
- You told the user the two commands: `/rulings new` to record a decision, `/rulings
  check` to re-verify the register.
