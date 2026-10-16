General working agreements live in `~/.claude/CLAUDE.md`. This file adds only what is
specific to `<PROJECT-NAME>`.

# `<PROJECT-NAME>` - session instructions

This directory is the harness for `<GOAL, one sentence>`. You are here to execute one
phase of it.

## Orientation (do this first, every session)

The normal entry point is the `/phase` skill (`.claude/skills/phase/`) - if the user
invoked it, follow its dispatch. If they asked for project work without it, do the
same by hand:

1. Read `STATE.md` - it says which phases are complete and holds the decision log,
   the evidence, and the anomalies.
2. Read `CONFIG.md` - parameters and standing authorizations. **If any field is still
   `TBD`, stop and ask the user to fill it in before doing anything else.**
3. Load the runbook for the first incomplete phase from `prompts/phase-N-*.md` and
   execute it. If the user asks for a specific phase, confirm its predecessors are
   marked complete in `STATE.md` first; if they are not, say so and stop.
4. `docs/end-state.md` defines the invariant and what "done" means. When any
   instruction here or in a prompt seems ambiguous, the end-state doc is the
   tiebreaker.

## Hard guardrails - these override convenience, always

- **Phase `<READ-ONLY-PHASE-N>` is strictly read-only.** Survey only. Do not modify,
  move, rename, or delete anything found during it. Prefer plan mode.
- **Never touch `<OFF-LIMITS-PATHS>`.** `<One line on why - the structural reason.>`
- **A collision with an invariant is a stop, not a tiebreak.** If a phase's plan
  collides with the invariant in `docs/end-state.md`, a guardrail here, or the
  never-pre-authorizable list in `CONFIG.md`, the phase bends and the invariant does
  not. Record it in `STATE.md` and stop for a ruling; never resolve it in flight.
  This is not the end-state doc's tiebreaker role, which settles an instruction that
  is *ambiguous*; this is a plan colliding with one that is not. Amending an invariant
  is its own gated act with its own approval.
- **Move, never copy** (global rule; here it binds `<The thing being migrated/changed>`,
  which must not remain in its old location).
- **Deletion gate:** Phase `<FINAL-PHASE-N>` (global supersede rule).
- **Decisions are proposed by Claude, ratified by the user.** The survey phase
  produces a fully proposed decision table; the user rules on it in ONE batch
  (Gate A) before execution. Execution phases run only ratified rows - unratified
  rows are skipped and reported, never guessed at.
- **`<IRREVERSIBLE-STEP>` requires explicit confirmation of an enumerated list**
  (Gate B). It is never covered by a standing authorization.
- **Continuous by default.** `/phase` runs all remaining phases end-to-end, updating
  `STATE.md` as it goes. Interruptions are limited to the gates enumerated in the
  `/phase` skill and the blocker policy defined there - never "shall I continue?"
  between phases.

## Working conventions

- `STATE.md` is this project's resume point (global resume-point rule).
- Record **executed evidence** in `STATE.md` per the global evidence rule, formatted
  per `foundry-core:proof-of-work` / `foundry-core:evidence-report`. Prove this
  project's own gates and validators by deliberate failure before trusting them.
- Anomalies (things that do not fit, drifted duplicates, situations the prompts did
  not anticipate) get logged in `STATE.md` under Anomalies with a one-line
  recommendation - they do not get silently resolved, and they are reviewed at the
  next gate rather than raised one-by-one.
- Subagents never receive `<WHAT NO SUBAGENT GETS IN THIS PROJECT: a path, a tool, a
  credential>` (global subagents and fan-out rules).
- **Git in this harness dir:** no commits unless the user asks; if it should become a
  repo, use `voice-and-editing:folder-to-repo`. (Default; replace only if this project wants
  its harness under version control from the start.)
- **Commits in `<REPOS THIS PROJECT CHANGES>`:** path-scoped staging,
  `git diff --cached --stat` read before each commit, no push without the global
  carve-out. `<Add granularity and message style. Delete this line if the project
  touches no other repo.>`
- **At close-out** the final phase rewrites this file from the phased-harness skill's
  `templates/project-CLAUDE-closed.template.md` and marks
  `.claude/skills/phase/SKILL.md` ARCHIVED (see the final-phase runbook).
