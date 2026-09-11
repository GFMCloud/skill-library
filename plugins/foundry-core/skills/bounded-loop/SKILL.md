---
name: bounded-loop
description: >-
  Install a script-based Stop hook that runs a goal's check command itself,
  blocks each failing turn with the check's real output, and stops the loop
  at a fixed attempt budget with a structured escalation report instead of
  retrying forever. Use for any goal whose check must be executed by the
  harness rather than judged from the transcript, and for any unattended
  `/goal` run that needs a fixed escalation format when it cannot finish. Not
  for goals `/goal` can already judge from the transcript alone, and not a
  substitute for `/goal`'s own loop — this only supplies the parts `/goal`
  lacks: running the check, guarding against test-file tampering, and a
  budget with an escalation report at the end.
metadata:
  maturity: incubator
---

# bounded-loop

`/goal` is the loop. This skill supplies what `/goal` cannot do on its own:
`/goal`'s evaluator judges only what Claude surfaces in the transcript, it
never runs a command itself (research record 2026-09-11, row 1). When the
check is a command — a test suite, a linter, a build — something has to
execute it and hold the agent to what it actually returns, not what it
claims. That something is a script-based Stop hook:
`scripts/stop-hook-verify.sh`.

See [references/stop-hook-contract.md](references/stop-hook-contract.md) for
the hook doc lines this script relies on, quoted verbatim. See
[references/escalation-report.md](references/escalation-report.md) for how
to fill and present the report this skill produces.

## Inputs

- A Goal block v1 (from `foundry-core:goal-spec`, or written by hand in that
  shape) — specifically its `check` field (a command) and `budget` field.
- A budget: the number of distinct attempts before escalating. Default **3
  attempts** if the goal block does not name one. This default is a design
  choice, not a benchmarked optimum — pick a smaller number for a check that
  is cheap to run and a larger one only if early evidence shows 3 is too
  tight for the kind of task in question.
- The repo or workspace root the check runs against (`--repo`).
- Optionally, one or more guarded paths (`--guard`) — the verifier and test
  files that must not change between attempts. Name every file the check
  itself reads to decide pass/fail; an unguarded test file can be edited to
  make a failing attempt look like it passed.

## Verify

Install the hook for the session (add an entry under `Stop` in
`.claude/settings.json` invoking `stop-hook-verify.sh` with the goal's
`--check`, `--budget`, `--repo`, and `--guard` flags — see
`scripts/stop-hook-verify.sh --help` for the full flag list). From then on,
every Stop event runs the check itself and the three-part evidence standard
(what ran, against what, what came back) is satisfied automatically: the
script's own stderr or the written `escalation.yaml` always carries the
check's verbatim output, never a paraphrase.

The gate for this skill's own correctness is the deliberate-failure proof in
`fixtures/`: `never-passing-check` (a check that can never pass) must
escalate at budget exhaustion; `test-file-guard` (a guarded file edited
between attempts) must fail automatically regardless of the check's exit
code; `passing-check` proves both the clean release path and that a repeated
diff hash does not consume an attempt. Run any of them with `bash
fixtures/<name>/run.FIXTURE.sh`.

## Done when

The check meets its target within budget: `stop-hook-verify.sh` exits 0 on
an attempt whose check exit code is 0, having attached that check's output,
and the agent reports "target met at attempt N" using the script's own
count of distinct attempts (a repeated diff hash never inflates N).

## Stop when

- **Budget exhausted.** `attempts` (distinct diff hashes) reaches the budget
  while the check still fails: the hook writes Escalation report v1 and
  releases the turn. No further attempts are made under this budget; a new
  run needs a new budget, not a silent extension of the old one.
- **A guarded file changed.** Any content change to a `--guard` path between
  attempts is an automatic fail, `cause_class: test_file_modified`,
  regardless of what the check itself returned. This does not wait for
  budget exhaustion — it escalates immediately, because a check that can be
  made to pass by editing the thing that checks it is not evidence of
  anything (research record row 11, EvilGenie test-file-edit detection).
- **No progress.** Two consecutive attempts leave the workspace snapshot
  unchanged (same diff hash back to back): `cause_class: no_progress`,
  escalate immediately rather than spend the remaining budget re-running an
  identical check against an identical workspace.
- **Scope note.** This skill's guard and budget do not scale to large,
  compositional changes — a check that only exercises one function cannot
  catch a regression three modules away (SpecBench finding, research record
  secondary findings). Use `bounded-loop` for small, boundable tasks with one
  clear check; add an integration check separately for anything that touches
  multiple modules, and do not read a green `bounded-loop` run as proof of
  more than the check it ran.

## Output contract

Produces an Escalation report v1 as defined in the harness interface spec,
section 2, on budget exhaustion, a guard failure, or a no-progress
detection — written to the `--escalation-out` path (default
`<state-dir>/escalation.yaml`) and printed once by the hook itself. On
success, no escalation report is produced; the agent states "target met at
attempt N" with the check's verbatim output attached, per the
`foundry-core:proof-of-work` evidence standard.

Consumes a Goal block v1 as defined in the harness interface spec, section 1
— specifically `check`, `budget`, and (when present) `goal_condition` for
the escalation's `goal_block` field.
