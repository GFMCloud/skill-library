---
name: phase
description: >-
  Run the next phase of the `<PROJECT-NAME>` project (or a specific phase, e.g.
  "/phase 3"). Use when the user opens this project and wants to start, continue,
  or resume the work.
metadata:
  maturity: stable
  version: 1.0.0
  reviewed: <YYYY-MM-DD>
---

# Run a `<PROJECT-NAME>` phase

`<GOAL, one sentence.>` You are dispatching one phase of it.

## Dispatch

1. Read `STATE.md` (phase tracker, decision log, evidence, anomalies) and `CONFIG.md`
   (parameters and standing authorizations). **If any CONFIG.md value is `TBD`, stop
   and ask the user to fill it in — this is the only setup interruption.**
2. Mode:
   - **No argument (default): continuous run.** Execute every remaining phase in
     order, `<0>` → `<FINAL-PHASE-N>`, without stopping between phases. Resume from
     wherever `STATE.md` says the last run stopped.
   - Argument `N` (e.g. `/phase 3`) → run only that phase, if its predecessors are
     checked in `STATE.md`; otherwise say which prerequisite is missing and stop.
3. For each phase, read the runbook `prompts/phase-<N>-*.md` in full and execute it
   exactly. Update `STATE.md` as each phase completes, not just at the end.
4. Guardrails in `CLAUDE.md` are binding. `docs/end-state.md` is the tiebreaker for
   any ambiguity.

## Orchestration — this session is the harness, subagents do the heavy lifting

Keep this session's context thin so one session can carry the whole run: dispatch,
gate presentations, and shared-file updates happen **here**; bulk work is delegated to
subagents that write their results to files and return short summaries.

- Run this orchestrator session on a top-tier model at high effort — it owns every
  judgment call (proposals, anomaly-vs-blocker decisions, gate rulings, git).
- **Shared files stay with the orchestrator**: `STATE.md`, the tracking file, any
  catalog or manifest. Concurrent subagent writers corrupt the resume point.
- Fan out mechanical work to parallel subagents on a smaller model. Each gets: a
  **disjoint file subtree**, an explicit **do-not-touch list**, the guardrails
  **restated in its prompt**, and instructions to write results to a file.
- `<Per-phase delegation plan: which phases fan out and along what axis, which are
  small enough to run inline.>`
- Files are the source of truth — never conversation memory. Any subagent must be
  able to do its job from disk plus its prompt, and the whole run must be resumable
  from disk alone.
- Before a phase that depends on an external capability, **preflight it** (a real
  read and a real write, each with a negative control) rather than discovering it is
  dead mid-verification. Use `turn-reduction:capability-preflight` if installed.

## Interruption policy — stop ONLY at these points

The user has asked not to be consulted except where their ruling is required:

- **Gate A (after Phase `<GATE-A-PHASE-N>`):** present the full proposed decision
  table in one batch and wait for rulings. One interruption, however many rows exist.
  For any ruling that overrides a proposal, explicitly reassign that proposal's side
  effects to a named owner in a later phase — they vanish silently otherwise.
- **Gate B (Phase `<FINAL-PHASE-N>`):** present the enumerated `<IRREVERSIBLE-STEP>`
  list, with where each item remains recoverable, and wait for explicit confirmation.
  Never pre-authorized.
- **Blockers:** something a runbook did not anticipate that cannot be logged as an
  anomaly and safely deferred. Try the obvious fix first; interrupt only if genuinely
  stuck.

Everything else proceeds under the standing authorizations in `CONFIG.md`. Do not ask
"shall I continue?" between phases. Anomalies get logged in `STATE.md` with a
recommendation and reviewed at the next gate, not raised one-by-one.
