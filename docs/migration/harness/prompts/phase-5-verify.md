# Phase 5 — Verify, then delete

**Nature:** verification gate, then the project's only deletion step. Deletions
happen **only after every check passes**, and each deletion is confirmed with the
user as a list before executing.
**Prerequisite:** Phase 4 marked complete in `STATE.md`.

## Verification checklist (record actual evidence in STATE.md, not just ✓)

1. **Single-home check** — re-run the Phase 1 sweep (read-only, same breadth).
   Every skill from `MIGRATION.md` now exists in exactly one live home; the only
   extra hits are `.migrated-off` items and plugin caches of the new marketplace.
2. **Resolution check** — in a fresh context (spawn a subagent or a headless
   `claude -p` run; don't ask the user to open windows): library skills appear once
   each under their plugin namespace; a migrated skill's slash command runs; no
   orphan names.
3. **Auto-invocation check** — same mechanism: give a prompt matching a migrated
   skill's description (don't name the skill); confirm the skill loads.
4. **Validator/CI check** — validator green locally; open a throwaway PR with a
   deliberately broken skill (violating F3/F5/F10), confirm CI **fails** it, close
   the PR without merging.
5. **CLAUDE.md check** — global file carries the consumption rules; library repo
   carries the authoring rules.
6. **Project check** — each `project`-disposition skill still works in its project
   and collides with nothing.

If any check fails: fix, or log in Anomalies and stop. Do not proceed to deletion
with a failing check.

## Deletion (only after all checks pass)

1. Enumerate every `.migrated-off` item and every `archive`-disposition source into
   a list; for each, note where the content remains recoverable (git history /
   archive location). **Show the user this list and get explicit confirmation.**
2. Delete the confirmed items.
3. Re-run the validator and check 2 once more (post-deletion smoke test).

## Close out

- `MIGRATION.md` stays in the library repo permanently as the historical record —
  add a final line noting completion date.
- `STATE.md` here: Phase 5 checked, evidence recorded, project marked **complete**.
- Suggest (don't execute) follow-ups: archive this harness directory to the library
  repo's `docs/migration/` for reproducibility on the next machine.
