# Phase 1 (work) - Work-only generic skills in, environment text to rule files, packs dropped only when empty

**Nature:** execution of ratified decisions, with **one gate per pack drop**
(`auth_pack_drop` is `no`). Writes go to `~/skill-library` on branches (as `gmorris1221`),
to the company marketplace and the work config repo (as `gmorris1221`), and to
`STATE-work.md`.

**Machine:** work laptop only. **Prerequisite:** `STATE-home.md` shows Phase 1 home complete;
the updater has brought this laptop to that `main` SHA (`version_compare` matches); the
weekly maintainer is still paused.

## Step 0: machine detection

```bash
gh api user --jq .login
```

Expected: `gmorris1221`. Anything else: **stop here**.

## Steps

1. **Bring the clone to home's SHA.** `git -C ~/skill-library pull --ff-only` and the
   updater by hand; `version_compare` must equal the output in `STATE-home.md`. Record.
2. **Rule files first.** From `STATE-home.md` "Rule-file candidates for the work laptop" and
   the direction table notes, write `~/.claude/rules/partner-central.md` and
   `~/.claude/rules/brand.md` with `paths:` frontmatter (Decision A worked example), commit
   to the work config repo (`auth_local_rules_files`). Check: open a session that touches a
   `.html` file and confirm the brand rule loaded (`/memory` lists it); touch a `.py` file
   and confirm it did not.
3. **Work-only generic skills into skill-library.** The work-only list is in the design
   session's `compare-skills.sh` output (60 names); the generic ones among them (the design
   names `freeze` and its hook, `learn`, `doc-coauthoring`, `skill-creator` as the work-only
   skills still living in `workbench`; which are generic is a Gate A ruling if not already
   obvious) move into the skill-library pack they belong to: `git mv` from the company
   marketplace clone is not possible across repos, so copy in, validate, PR as
   `gmorris1221`, then rename the source `skills/<name>` to `skills/<name>.superseded` in
   the company marketplace in the same work session. Move, never copy: the `.superseded`
   rename is what makes it a move. Each PR: version bump, CHANGELOG, validator exit 0,
   denylist pre-commit and CI green, fresh review before merge.
4. **Per company pack that overlaps** (`workbench`, `verification`, `security-scan`,
   `<brand>-decks`, `<brand>-design`, and `<brand>-core` for its generic rows):
   1. List what is left in the pack after steps 2 and 3: every generic skill is now in
      skill-library (check: `version_compare` shows the pack version that carries it, and
      the fresh-session check from Phase 1 home step 6 prints the canonical name), every
      work-only skill either moved or stays because its body is company. Everything that
      moved is `.superseded` in the pack.
   2. **If the pack is not empty, it stays enabled.** Record what remains and why.
   3. **If the pack is empty:** stop for the pack-drop gate. Present: the pack name, the
      coworker notice (Gate A row G5) and when it was sent, the `CLAUDE.md` references that
      change (`grep -rn 'workbench:' ~/.claude/CLAUDE.md` and the company skills that
      cross-reference it), the `git-subdir` entries to add. Wait for the ruling.
   4. On a yes: **one commit** in the company marketplace that removes the pack directory,
      adds the pack to `renames` as `null`, adds the `git-subdir` entries for the generic
      packs it depended on pinned to the current skill-library `main` `sha`, and rewrites
      every `workbench:x` reference to the canonical `pack:x`. Then `claude plugin
      uninstall <pack>@<brand>-skills` on this laptop. Check: `claude plugin list` no longer
      lists it; `grep -rn 'workbench:' ~/.claude/CLAUDE.md` prints nothing; a fresh session
      resolves each former `workbench:x` under its canonical name.
5. **Leave the `@<brand>-skills` copies of generic packs disabled** on this laptop once a
   `git-subdir` entry exists for them, so nothing loads twice (`claude plugin disable`).
   Check: the fresh-session check prints each skill name exactly once.
6. **Resume the weekly maintainer** if Gate A row G6 ruled so; record the action.
7. **Record** in `STATE-work.md`: per pack, what remained or the drop commit SHA; the
   skill-library `main` SHA; evidence; session log line. PR as `gmorris1221`.

## Negative control, per gate introduced

- The pre-commit hook on this clone (Phase 0 work) is re-proven once at the start of this
  phase with the planted fixture (expected refusal), because it guards every PR this phase
  opens.
- The pack-drop rollback is rehearsed on the first drop before the second: `git revert` the
  drop commit in the company marketplace, `claude plugin install <pack>@<brand>-skills`,
  confirm the pack is back, then re-apply. Record both directions.

## Anomalies

A pack that will never be empty (its remaining skills are all company) is not an anomaly;
record it as "stays". A generic skill with no obvious pack is an anomaly for the next gate.

## Rollback (6b)

A dropped pack is one commit in the company repo; `git revert` restores it and `claude
plugin install` re-enables it. Skills moved into skill-library stay, harmlessly. Rule files
are two files in the work config repo; `git checkout` restores the previous state.

## Done when

- Every overlapping pack is either dropped (commit SHA recorded, references rewritten in
  that commit, `git-subdir` entries added, coworkers told first) or recorded as staying with
  its remaining company-only contents listed.
- `grep -rn 'workbench:' ~/.claude/CLAUDE.md` prints nothing, and the company skills that
  cross-reference generic skills use canonical names.
- `compare-skills.sh` (or its equivalent run against the live trees) reports 0 shared names
  between skill-library and the company marketplace, `git-subdir` entries aside.
- The two rule files exist, load on a matching path, and do not load otherwise.
- `STATE-work.md`: Phase 1 work ticked, SHA recorded, evidence recorded.
