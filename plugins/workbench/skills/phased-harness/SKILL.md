---
name: phased-harness
description: >-
  Interview the user and scaffold a phased, gated, file-based project harness for
  long-horizon work — CONFIG/STATE/end-state docs, per-phase runbooks, a guardrail
  CLAUDE.md, and a /phase dispatch skill that runs continuously and resumes from
  disk. Use on "phased harness", "set up a phased project", "run this like the
  skill migration", "gated multi-phase project", "long-running project with
  gates", "multi-session plan I can resume", or any effort spanning several
  sessions that ends in an irreversible step.
metadata:
  maturity: stable
  version: 1.0.0
  reviewed: 2026-08-09
---

# Phased harness — scaffold a gated, resumable project

This skill **interviews and scaffolds**. It does not execute the project. It births a
per-project harness directory; the generated harness — with its own `/phase` dispatch
skill — runs the work in later sessions.

Rationale behind every rule below: [references/doctrine.md](references/doctrine.md).

## Step 1 — Fit test (do this before anything else)

Build a harness only when **all four** hold:

1. **Multi-session.** The work exceeds roughly a day, or will certainly cross a
   context boundary.
2. **Ordered phases of distinct nature.** It decomposes into a read-only survey → a
   decision point → execution → verification → an irreversible finish. Phases that
   are all the same kind of work are a task list, not a harness.
3. **Nameable invariant.** The user can state the end state as a *state*, not a task
   list ("every X has exactly one editable home"), before work starts.
4. **Ends irreversibly.** There is a final step — deletion, publication, cutover,
   send — that cannot be undone.

**Decline, and say why, when:**

- The work is under ~a day or single-session → just do it, or use a todo list.
- It is exploratory or creative with no end state nameable up front → the harness's
  invariant and gates have nothing to bind to.
- It is single-turn orchestration or a repeatable pipeline → that is an ultracode /
  dynamic-workflow job, not a harness.
- Nothing irreversible ever happens → Gate B is empty; the ceremony buys nothing.

State the failing criterion plainly and stop. Do not scaffold a harness "just in
case" — an unused harness is pure overhead the user has to read past.

## Step 2 — Interview

Ask in **one batch** (AskUserQuestion where the options enumerate). Do not scaffold
with any of these unresolved; an unfilled parameter becomes a `TBD` that stops every
future session.

| # | Extract | Why it is load-bearing |
|---|---|---|
| 1 | **End state + its invariant**, stated as a state | Becomes `docs/end-state.md`, the tiebreaker for every ambiguity later |
| 2 | **The irreversible step** | Defines Gate B and what "reversible until then" means |
| 3 | **Standing authorizations** — what may proceed without asking | Becomes the CONFIG table; this is what makes a continuous run possible |
| 4 | **Never-pre-authorized list** | Always includes the irreversible step; ask what else |
| 5 | **Phase breakdown** — name + nature + "done when" for each | Becomes `prompts/phase-N-*.md` |
| 6 | **Project directory** — where the harness lives | Its own dir, separate from the artifact being worked on |
| 7 | **Decisions that are the user's alone** | Gate A material; everything else Claude proposes and executes |
| 8 | **Parameters** — repos, paths, orgs, thresholds, targets | Becomes the CONFIG parameter table |

Propose a phase breakdown yourself from what the user described, then have them
correct it. Users describe tasks; you convert to phases-with-natures. Name the nature
of each phase explicitly (read-only survey / decision gate / execution / verification
/ irreversible finish) — the nature is what the guardrails attach to.

## Step 3 — Scaffold

Create the project directory and instantiate every template, substituting the
interview answers. Generated tree:

```text
<project-dir>/
├── CLAUDE.md              ← project-CLAUDE.template.md — orientation + hard guardrails
├── CONFIG.md              ← CONFIG.template.md — parameters + standing authorizations
├── STATE.md               ← STATE.template.md — the single resume point
├── README.md              ← short: why, how to run (`/phase`), phase table
├── docs/
│   └── end-state.md       ← end-state.template.md — the invariant + tiebreaker
├── prompts/
│   ├── phase-0-<name>.md  ← phase-runbook.template.md, one per phase
│   └── ...
└── .claude/skills/phase/
    └── SKILL.md           ← dispatch-SKILL.template.md
```

Templates: [CONFIG](templates/CONFIG.template.md) ·
[STATE](templates/STATE.template.md) ·
[end-state](templates/end-state.template.md) ·
[phase runbook](templates/phase-runbook.template.md) ·
[project CLAUDE.md](templates/project-CLAUDE.template.md) ·
[dispatch SKILL.md](templates/dispatch-SKILL.template.md)

Rules while instantiating:

- **Replace every `<PLACEHOLDER>`.** A placeholder surviving into the generated
  harness is a bug — grep the tree for `<` before finishing.
- **Parameters the user did not supply stay literally `TBD`** in CONFIG.md, and the
  generated CLAUDE.md + dispatch skill both stop on `TBD`. Never invent a value.
- **One runbook per phase**, each carrying: nature, prerequisite phase, numbered
  steps, and an explicit "Done when" list. A phase with no checkable "done when" is
  not yet a phase.
- **Phase numbering starts at 0** when there is a greenfield setup step.
- Keep the harness dir separate from the thing being changed, so the harness survives
  the work and can be archived afterwards as the record.
- Do not create the project's real artifacts here — scaffolding only.

After writing, verify: every relative link in the generated files resolves; every
phase named in STATE.md's tracker has a runbook file; CONFIG keys referenced by
runbooks exist in CONFIG.md. Report the tree with line counts.

## Generation rules — bake these into every harness

These are not optional flavor. Every generated harness carries all of them.

### Exactly two gates

- **Gate A** — after the survey/proposal phase. Every decision the user must make is
  presented in **ONE batch**, each with Claude's recommendation and one line of
  reasoning. Rows the user does not object to are ratified as proposed. Execution
  phases run only ratified decisions; unratified rows are skipped and reported, never
  guessed at.
- **Gate B** — before the irreversible step. The **enumerated** list of what will be
  done, plus where each item remains recoverable, and explicit confirmation. Never
  pre-authorizable, never covered by a standing authorization.
- Between gates the run **never asks "shall I continue?"**. Anomalies are logged in
  STATE.md with a one-line recommendation and reviewed at the next gate. A genuine
  blocker — something a runbook did not anticipate that cannot be safely deferred —
  is the only other permitted interruption, and only after the obvious fix is tried.

### Reversibility until Gate B

- Nothing is deleted before the final verification passes. Superseded items are
  **renamed with a suffix** (`.migrated-off`, `.retired`, `.superseded` — pick one and
  use it consistently) so every step is undoable.
- **Move, never copy.** Two editable copies of the same thing is the failure mode most
  of these projects exist to eliminate.

### Orchestration

- The session model is the **orchestrator**: top-tier model, high effort. It owns
  judgment, gate presentations, git, and **all shared files** (STATE.md, the tracker,
  any catalog). Shared files never go to a subagent — concurrent writers corrupt the
  resume point.
- Bulk mechanical work **fans out to parallel subagents** on a smaller model, each
  given a **disjoint file subtree**, an explicit **do-not-touch list**, and the
  guardrails **restated in its prompt** (delegation never weakens a guardrail).
- Subagent results are **written to files before the orchestrator proceeds**.
- **Files are the source of truth**, never conversation memory. Test: could a fresh
  session with no history resume this run from disk alone? If not, the harness is
  incomplete.

### Overridden-plan rule

When a gate ruling overrides a proposed action, **explicitly reassign that action's
side effects** — cleanup, retirement, suffix-renaming — to a named owner in the same
breath. Overridden rows lose their execution task, and the side effects they carried
vanish silently. This is a real failure that reached the final verification sweep in
the run this skill generalizes (see doctrine).

### Evidence discipline

- STATE.md records **executed evidence** — the command and its actual output — not
  checkmarks.
- **Prove every gate by deliberate failure before trusting it.** A validator or CI
  check that has never failed is not known to work; feed it a fixture that must fail,
  record the output, then remove the fixture.
- **Preflight depended-on capabilities** before the phase that needs them (e.g.
  headless `claude -p "Say OK"`, API auth, push access). Discovering a dead capability
  mid-verification costs a whole phase.
- The **final phase re-verifies the invariant from scratch** — a fresh sweep in a
  fresh context, not a re-read of earlier notes.

### Compose, don't duplicate

The generated harness **points at** these library skills where installed rather than
restating them:

- `turn-reduction:standing-authorization` — reading authorizations out of CONFIG.md
  instead of asking.
- `turn-reduction:capability-preflight` — the per-phase capability proofs.
- `foundry-core:proof-of-work` and `foundry-core:evidence-report` — evidence format
  for STATE.md and gate presentations.
- `verification-kit:pre-delivery-verifier` — the final-phase verification pass.

Reference them by name; do not copy their content into the harness.

## Done when

- The tree above exists, fully substituted, with no stray `<PLACEHOLDER>`.
- `docs/end-state.md` states the invariant as a state and is named as the tiebreaker
  by both CLAUDE.md and the dispatch skill.
- CONFIG.md lists every parameter (unknowns as `TBD`) and the standing-authorization
  table with the never-pre-authorized list.
- Each phase has a runbook with nature + steps + "done when"; STATE.md's tracker lists
  exactly those phases, all unchecked.
- You told the user the one command that starts the work: open a session in the
  project dir and run `/phase`.
