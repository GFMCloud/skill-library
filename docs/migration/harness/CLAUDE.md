# Skill organization project — session instructions

This directory is the harness for a phased migration of this machine's Claude Code
skills into a single canonical plugin-marketplace repo. You are here to execute one
phase of that migration.

## Orientation (do this first, every session)

The normal entry point is the `/phase` skill (`.claude/skills/phase/`) — if the user
invoked it, follow its dispatch. If they asked for migration work without it, do the
same by hand:

1. Read `STATE.md` — it says which phases are complete and holds the decision log.
2. Read `CONFIG.md` — target repo name and paths. **If any field is still `TBD`,
   stop and ask the user to fill it in before doing anything else.**
3. Load the runbook for the first incomplete phase from `prompts/phase-N-*.md` and
   execute it. If the user asks for a specific phase, confirm its predecessors are
   marked complete in `STATE.md` first; if they aren't, say so and stop.
4. `docs/end-state.md` defines what "compliant" means. When any instruction here or
   in a prompt seems ambiguous, the end-state doc is the tiebreaker.

## Hard guardrails — these override convenience, always

- **Phase 1 is strictly read-only.** Inventory only. Do not modify, move, rename, or
  delete anything found during inventory. Prefer plan mode.
- **Never edit anything inside plugin caches or marketplace clones**
  (`~/.claude/plugins/**`). Changes to skills land only in the canonical library repo.
- **Move, never copy.** A migrated skill must not remain in its old location. The
  same skill existing in two editable places is the failure mode this whole project
  eliminates.
- **Nothing is deleted until Phase 5 verification passes.** Until then, superseded
  files/dirs are renamed with a `.migrated-off` suffix so every step is reversible.
- **Dispositions are proposed by Claude, ratified by the user.** Phase 1/2 produce a
  fully proposed disposition table; the user rules on it in ONE batch (Gate A)
  before Phase 3 executes it. Phase 3 executes only ratified rows — unratified rows
  are skipped and reported, never guessed at.
- **Continuous by default.** `/phase` runs all remaining phases end-to-end, updating
  `STATE.md` as it goes. Interruptions are limited to the gates and blocker policy
  defined in the `/phase` skill — never "shall I continue?" between phases.

## Working conventions

- `STATE.md` is the single resume point. Keep it current as you work, not just at
  the end — if the session dies, the next one must be able to continue from it.
- Anomalies (skills that don't fit the contract, drifted duplicates, things the
  prompts didn't anticipate) get logged in `STATE.md` under Anomalies with a one-line
  recommendation — they do not get silently resolved.
- Commits in the library repo: small and per-phase (Phase 3: one commit or PR per
  plugin). Commit messages state the behavior-relevant change, not the file list.
