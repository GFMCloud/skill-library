# Phase 3 — Migrate

**Nature:** executes the ratified Ruling column of `MIGRATION.md` (Gate A). Makes no
disposition decisions — unratified rows are skipped and reported at the end.
**Prerequisite:** Phase 2 marked complete in `STATE.md`.

## Per `library:*` row

1. Create the target plugin under `plugins/<name>/` if it doesn't exist (manifest +
   `marketplace.json` entry).
2. **Move** the skill into `plugins/<name>/skills/<skill>/` — never copy. For drifted
   rows, move the marked winner; for `winner: merge`, merge per the row's notes and
   record what was merged in the row.
3. The vacated source location is renamed with a `.migrated-off` suffix (file or
   directory as appropriate). Exception: sources inside plugin caches or marketplace
   clones are left untouched — they're superseded by deregistration in Phase 4.
4. Normalize to `docs/authoring-standard.md`: frontmatter contract (`metadata:`
   block, maturity, version `1.0.0` for skills entering as stable, today's
   `reviewed:` date); `name` = directory name; body under 500 lines with long
   material moved to `references/`; description rewritten router-style if vague —
   **preserving the skill's behavior; normalization is packaging, not rewriting.**
   Behavior-affecting edits found necessary get logged in `STATE.md` Anomalies, not
   silently made.
5. Check the row off in `MIGRATION.md` **as you go** — this file is the resume point
   if the session dies mid-phase.

## Per `deprecate` row

As above, plus `maturity: deprecated` and `metadata.supersedes` per the row.

## Per `project` row

No move. Verify the skill's name doesn't collide with any library skill (rename it in
the project if it does — that's a project commit; note it in the row). Frontmatter
normalization is optional and belongs to the project, not this repo.

## Per `archive` row

Nothing moves in this phase. Confirm the row records where the content will remain
recoverable (git history or an archive path); removal happens in Phase 5.

## Gate and commit

- Run `scripts/validate-skills.sh` until fully green.
- One commit (or PR, if you want CI exercised now) **per plugin**, message naming the
  skills that moved and where from.
- Update the library `CHANGELOG.md`: one migration entry per plugin.

## Done when

- Every dispositioned row is checked off or listed in a final "skipped/blocked"
  report; validator green; commits pushed.
- `STATE.md` here: Phase 3 checked; anomalies logged; session log line added.
