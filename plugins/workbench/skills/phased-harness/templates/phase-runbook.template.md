# Phase `<N>` — `<PHASE-NAME>`

**Nature:** `<one of: greenfield build | STRICTLY READ-ONLY survey | decision gate |
execution of ratified decisions | verification | irreversible finish>`. `<One line
spelling out what that nature forbids — e.g. "The only writes permitted are the two
output files listed at the bottom.">`

**Prerequisite:** Phase `<N-1>` marked complete in `STATE.md`. `<Plus any capability
that must be preflighted before this phase starts — prove it with
turn-reduction:capability-preflight, do not assume it.>`

## Steps

1. `<Step — imperative, concrete, naming the exact paths/commands/files involved.>`
2. `<Step. Where a step interpolates a parameter, name the CONFIG.md key:
   "per `<param_1>` in CONFIG.md".>`
3. `<Step. Where a step is bulk mechanical work, say so explicitly and say how it
   fans out: one subagent per <unit>, each given only its own subtree, an explicit
   do-not-touch list, and the guardrails restated. Results written to files before
   the orchestrator proceeds.>`
4. `<Step. Where a step supersedes something, it is RENAMED with the .superseded
   suffix — never deleted. Deletion happens only in the final phase, after Gate B.>`
5. Record executed evidence in `STATE.md` as you go — the command and its actual
   output, not a checkmark. Check items off in the tracking file **as you go**: that
   file is the resume point if the session dies mid-phase.

<!-- For a PHASE 0 (greenfield / setup) runbook, the Steps list above is REQUIRED to
     include these, not optional additions:
     - Prove every capability this project depends on, in Phase 0, before any of it is
       needed: one real read and one real write per target system named in CONFIG.md,
       each with a negative control that must fail. Compose
       `turn-reduction:capability-preflight`. Record the command and its actual
       output. A capability assumed in Phase 0 and discovered dead in Phase 5 costs
       the whole run.
     - Run `/fewer-permission-prompts` against each active target repo and write the
       allow rules before the first phase that deploys, not reactively at cutover.
     - Before assuming exclusive access to the target tree, check whether another
       harness or session is already on it: list live sessions on those paths, read
       the recent commits, and check file mtimes against the last recorded run. Treat
       an unexplained recent change as possibly-live work by someone else, not as
       history. -->

<!-- For a GATE phase, replace the steps above with:
     ## Present
     One consolidated package, in ONE batch: (1) summary counts; (2) the short list of
     rows where the call is genuinely the user's, each with the proposal, the
     alternative, and one line of reasoning; (3) everything else as a compact table,
     ratified by default unless the user objects. Use AskUserQuestion where choices
     enumerate. Wait for the rulings.
     ## Record
     Write every ruling — including "as proposed" — into the tracking file and the
     STATE.md decision log. For any ruling that OVERRIDES a proposal, explicitly
     reassign that proposal's side effects (cleanup, retirement, suffix-renaming) to a
     named owner in a later phase; they vanish silently otherwise.
     Then proceed directly to the next phase — no further confirmation. -->

## Anomalies

Anything this runbook did not anticipate gets logged in `STATE.md` under Anomalies
with a one-line recommendation, and is reviewed at the next gate. Do not silently
resolve it; do not interrupt the run for it. Interrupt only for a genuine blocker —
something that cannot be safely deferred — and only after trying the obvious fix.

## Done when

- `<Checkable condition 1 — an observable state, not "did the work".>`
- `<Checkable condition 2.>`
- `<Checkable condition 3.>`
- `STATE.md`: Phase `<N>` checked, evidence recorded, anomalies logged, session log
  line added.
