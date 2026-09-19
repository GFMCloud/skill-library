---
name: phase
description: >-
  Run the next phase of the skill organization migration project (or a specific
  phase, e.g. "/phase 3"). Use when the user opens this project and wants to
  start, continue, or resume the migration.
metadata:
  maturity: stable
  version: 1.0.0
  reviewed: 2026-08-09
---

# Run a migration phase

This project migrates the machine's Claude Code skills into one canonical
plugin-marketplace repo. You are dispatching one phase of it.

## Dispatch

1. Read `STATE.md` (phase tracker, decision log) and `CONFIG.md` (parameters and
   standing authorizations). **If any CONFIG.md value is `TBD`, stop and ask the
   user to fill it in — this is the only setup interruption.**
2. Mode:
   - **No argument (default): continuous run.** Execute every remaining phase in
     order, 0 → 5, without stopping between phases. Resume from wherever `STATE.md`
     says the last run stopped.
   - Argument `N` (e.g. `/phase 3`) → run only that phase, if its predecessors are
     checked in `STATE.md`; otherwise say which prerequisite is missing and stop.
3. For each phase, read the runbook `prompts/phase-<N>-*.md` in full and execute it
   exactly. Update `STATE.md` as each phase completes, not just at the end.

## Orchestration — this session is the harness, subagents do the heavy lifting

Keep this session's context thin so one session carries the whole run: dispatch,
gate presentations, and STATE.md updates happen here; bulk work is delegated to
subagents that write their results to files and return short summaries.

- **Phase 1 (sweep):** delegate to read-only subagents (split the search space:
  ~/.claude + plugin config / project repos / stray-file sweep). Each returns
  findings; the orchestrator merges them into MIGRATION.md. Never pull full skill
  bodies into this context — subagents read them and report rows + drift diffs.
- **Phase 3 (migrate):** one subagent per plugin, each given only its ratified rows;
  it moves/normalizes, runs the validator on its plugin, commits, and returns a
  per-row done/blocked list.
- **Phase 5 (checks):** each verification check is a subagent; the fresh-context
  checks use a subagent or headless `claude -p` run by design.
- Phases 0, 2, and 4 are small (skeleton build, gate conversation, config changes) —
  run them inline.

Model use: run the orchestrator session on a top-tier model (Fable 5/Opus, high
effort) — it owns every judgment call (drift analysis, disposition proposals,
anomaly-vs-blocker decisions). Mechanical subagents (Phase 1 file sweep, Phase 3
per-plugin move/normalize, Phase 5 checks) may be downgraded to a smaller model
(e.g. Sonnet); keep drift diffing and proposal writing on the session model.

Files are the source of truth (`STATE.md`, `MIGRATION.md`, the repo) — never
conversation memory. Any subagent must be able to do its job from disk plus its
prompt, and the run must be resumable from disk alone. Subagent results land in
files before the orchestrator moves on. Delegation never weakens the guardrails:
subagents inherit them via their prompts (read-only in Phase 1, move-never-copy,
no deletions before Gate B).
4. Guardrails in `CLAUDE.md` are binding (read-only Phase 1 sweep; never edit plugin
   caches; move, never copy; no deletions before Phase 5 verification).
   `docs/end-state.md` is the tiebreaker for any ambiguity.

## Interruption policy — stop ONLY at these points

The user has asked not to be consulted except where their ruling is required:

- **Gate A (after Phase 1/2 proposal):** present the full proposed disposition table
  in one batch and wait for rulings. One interruption, however many skills exist.
- **Gate B (Phase 5):** present the enumerated deletion list and wait for explicit
  confirmation. Never pre-authorized.
- **Blockers:** something a runbook didn't anticipate that cannot be logged as an
  anomaly and safely deferred — e.g. a verification check fails and the fix is
  ambiguous. Try the obvious fix first; interrupt only if genuinely stuck.

Everything else — repo creation, pushes, plugin installs, global CLAUDE.md edit —
proceeds under the standing authorizations in `CONFIG.md`. Do not ask "shall I
continue?" between phases. Anomalies get logged in `STATE.md` with a recommendation
and reviewed at the next gate, not raised one-by-one.
