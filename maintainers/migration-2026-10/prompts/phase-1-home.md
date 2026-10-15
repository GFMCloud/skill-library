# Phase 1 (home) - Reconcile the 41 into skill-library, one PR per pack

**Nature:** execution of ratified decisions. Writes go to `~/skill-library` on branches, to
`~/.claude/rules/homelab.md`, and to `STATE-home.md`. Nothing on the work laptop changes;
nothing in the company marketplace changes (that is Phase 1 work).

**Machine:** home laptop. **Prerequisite:** Gate A rulings recorded (every row has a
ruling). The work copies are read from a read-only `gmorris1221` shallow clone of
`company_marketplace_repo` into the scratchpad; `gh auth switch --user GFMCloud` right
after the clone, and `gh api user --jq .login` printing `GFMCloud` before any write.

## Step 0: machine detection

```bash
gh api user --jq .login
```

Expected: `GFMCloud`. Anything else: **stop here**.

## Steps

1. **Refresh the work copies, read only.** `gh auth switch --user gmorris1221`, shallow
   clone `company_marketplace_repo` and `work_config_repo` into the scratchpad, `gh auth
   switch --user GFMCloud`, confirm the login. Record the clone commit SHAs.
2. **One branch per skill-library pack** (`reconcile/<pack>-2026-10`), rows grouped by the
   `library pack` column. Bulk mechanical work: one subagent per pack, given only its pack's
   ruled rows, the three paths per row (base from `git show ecbab91:<path>`, ours, theirs),
   a do-not-touch list of every other pack, and the guardrails restated (ruled rows only,
   redaction rule, no environment text in a generic body, no deletion). Results written to
   files before the orchestrator proceeds. The orchestrator owns git, `CHANGELOG.md`,
   `marketplace.json` and the state file.
3. **Per row, by ruling:**
   - `merge`: `git merge-file --diff3` with the recorded base; non-overlapping hunks resolve
     themselves; read only the conflict hunks. Two-way rows (no base) are read in full with
     the ruled side as the base text.
   - `library wins`: the work copy's body is not merged; note any work-only line found and
     send it to Phase 1 work as a rule-file candidate.
   - `work wins`: the work body replaces the library body, then environment text comes out.
   - **Environment text leaves the body either way.** Home lines (restic, Traefik, Proxmox)
     go to `~/.claude/rules/homelab.md` with a `paths:` frontmatter (`auth_local_rules_files`);
     work lines (Partner Central, CloudFront, brand, company cross-references) are listed per
     skill in `STATE-home.md` under "Rule-file candidates for the work laptop" for Phase 1
     work to place. The merged body names no machine.
   - Cross-references use canonical pack names (`foundry-core:proof-of-work`, never
     `workbench:proof-of-work`).
4. **Per pack:** bump the pack `version` (validator F17), update `metadata.version` and
   `reviewed` on stable skills, add the `CHANGELOG.md` entry describing the behavior change,
   run `bash scripts/validate-skills.sh` (exit 0), run `gitleaks dir .` and `bash
   scripts/denylist-scan.sh` (both clean), commit, push own commits under the carve-out,
   open the PR. The fresh same-or-higher-tier review happens before merge (`auth_merge_pr`
   is `no`).
5. **After each merge:** run the updater by hand (`zsh scripts/update-installed-plugins.sh`)
   so this laptop runs the merged pack; expected `=== done` with no `REFUSED`. Record the
   `main` SHA.
6. **Check command, per skill:** the merged skill resolves under its canonical name in a
   fresh headless session:

   ```bash
   claude -p "List the installed skills whose name is <skill>; print pack:name only" --model haiku
   ```

   Expected: exactly one line, `<pack>:<skill>`.

## Negative control

The gate this phase relies on is the validator plus the denylist job on every PR, both
already proven in Phase 0. Per pack, before the first merge, one deliberate failure: leave
the pack `version` unbumped on the branch, run the validator, expect an F17 failure naming
the pack, then bump and expect exit 0. Record once per pack.

## Anomalies

A row whose merge produces conflicts the ruling does not cover is logged in `STATE-home.md`
and skipped, not resolved by guesswork; it is reviewed at the next gate (the first pack-drop
gate in Phase 1 work). Do not interrupt the run for it.

## Rollback (6b: "skills moved into skill-library stay, harmlessly")

A merged pack PR is reverted by `git revert` of its merge commit and a further version bump;
the updater then installs the reverted version. `~/.claude/rules/homelab.md` is one file;
remove it. Nothing on the work laptop changed.

## Done when

- Every ruled row whose `library pack` is in `packs` is merged to `main`, with its PR number
  in the direction table's `note` column, or listed under Anomalies with the reason.
- `version_compare` on this laptop shows every pack at the bumped version.
- Step 6 printed exactly one line for every merged skill.
- `~/.claude/rules/homelab.md` exists with a `paths:` frontmatter and no generic skill body
  mentions restic, Traefik or Proxmox (`git grep -i -l -E 'restic|traefik|proxmox' plugins/`
  prints nothing).
- `STATE-home.md` carries the rule-file candidates for the work laptop, the SHA, evidence,
  session log line; Phase 1 home ticked.
