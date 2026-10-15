# Phase 1, Gate A - Direction per shared skill, and the other rulings

**Nature:** decision gate. The only writes are `gate-a-direction-table.md` (the `note` and
`ruling` columns) and the two state files' decision logs. No skill is touched.

**Machine:** either, but the preparation reads the work copies, so it is simplest on the
work laptop; on the home laptop the work copies come from a read-only `gmorris1221` clone
into the scratchpad, with `gh auth switch --user GFMCloud` immediately after.
**Prerequisite:** `STATE-work.md` shows Phase -1 and Phase 0 work complete; `STATE-home.md`
shows Phase 0 home complete. The weekly maintainer is paused (Phase -1 row 8).

## Step 0: machine detection

```bash
gh api user --jq .login
```

Expected: the account that belongs to this machine (`home_account` or `work_account` in
`CONFIG.md`). Record which machine ran the gate.

## Prepare (before presenting; mechanical, may fan out)

1. For every row of the direction table with `base commit` = `ecbab91`, run the three-way
   dry run from the Phase 0 home runbook step 4b (base `ecbab91`, ours `main`, theirs the
   work copy) and write into the `note` column: lines changed each side, hunks resolved,
   conflicts. One subagent per pack, each given only its pack's rows, a do-not-touch list of
   every other file, and the redaction rule restated; results written to a scratch file the
   orchestrator copies into the table. The three rows Phase 0 already measured are kept.
2. For the 5 rows without a base, run a plain `diff --stat` and note the size.
3. For row 30 (`retro`), read the 93-line work copy and note whether anything in it is
   work-only.
4. Draft the coworker notice (row G5) from the Phase -1 collaborator count, no logins.
5. Re-check that `STATE-work.md` row 9 answered the Cowork question (row G4).

## Present

One consolidated package, in ONE batch, with `AskUserQuestion` where choices enumerate:

1. Summary counts: 41 rows, 36 with a base, the dry-run totals (hunks resolved, conflicts).
2. The rows where the call is genuinely Graham's, each with the proposal, the alternative,
   and one line of reasoning: row 7 (`design-taste-frontend`, the separate decision), row 2
   and row 10 (bake-off and work-origin bodies with no base), row 30 (`retro`), and any row
   whose dry run produced more than a handful of conflicts.
3. Everything else as the compact table, ratified as proposed unless Graham objects.
4. The other Gate A rows G1 to G6.

Wait for the rulings. One interruption, however many rows.

## Record

1. Write every ruling into the `ruling` column, including "as proposed", and the G rows'
   rulings into both state files' decision logs with the date.
2. For any ruling that overrides a proposal, reassign that proposal's side effects in the
   decision log: which file is renamed `.superseded`, which rule file receives the
   environment text, who does it and in which phase. Overridden rows lose their execution
   task and the side effects vanish silently otherwise (the 2026-08 migration's `scl` straggler
   is the precedent, `maintainers/migration/harness/STATE.md`).
3. Commit the table and the state files on a branch `gate-a/rulings-2026-10`, open the PR,
   and proceed to Phase 1 home without further confirmation.

## Negative control

The gate introduces no mechanical check. The control is procedural: Phase 1 home and Phase 1
work refuse any row whose `ruling` cell is empty (they list those rows and skip them).

## Rollback

Rulings are text in a PR; closing the PR unmerged restores the table. No skill changed.

## Done when

- Every one of the 41 rows has a non-empty `ruling`, and the `note` column carries the
  dry-run numbers for all 36 based rows.
- G1 to G6 are ruled and logged in both state files.
- Every overridden row's side effects have a named owner and phase in the decision log.
- The rulings PR is open; both state files tick "Phase 1 Gate A".
