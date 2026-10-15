# Phase 3 - Config repos and shared rules, then verify, then Gate B

**Nature:** execution of ratified decisions, then verification from scratch, then the
irreversible finish (Gate B deletions). Writes go to `~/skill-library` (the shared rules
file and the updater), to each machine's `~/.claude` and its config repo, and to the state
files. The home half creates `home_config_repo`; nothing else creates, renames or archives a
repo.

**Prerequisite:** Phase 2 complete on both machines. Gate A rows G1 (home config repo) and
G3 (shared rules location) are ruled.

## Step 0: machine detection

```bash
gh api user --jq .login
```

Expected: this machine's account per `CONFIG.md`. Record which half runs.

## Steps, home half first

1. **Create `home_config_repo`** per the G1 ruling (reset the 2026-07-29 snapshot, or start
   clean). Copy the allowlist `.gitignore` from the work config repo (Phase 1 home step 1's
   read-only clone; the gitignore is the one file worth copying, and it is a copy, not a
   move, because both repos need it). Add it as `origin` of the local `~/.claude` git repo,
   which exists already and tracks `CLAUDE.md` and `.gitignore`. Check: `git -C ~/.claude
   remote -v` shows `github.com/GFMCloud/claude-config`; `git -C ~/.claude status --short`
   lists only allowlisted files; `gitleaks dir ~/.claude` clean before the first push; the
   secret scan is a hard stop.
2. **Extract the shared rules file** into skill-library at the G3 location: every general
   working agreement both `CLAUDE.md` files restate, written once, with the home-only line
   "`dataviz` ... its colors win" scoped to home (at work, brand tokens win). Add the
   updater install step: copy it to `~/.claude/rules/shared-agreements.md` after the hook
   copy step. PR, review, merge, updater by hand. Check: `shasum
   ~/.claude/rules/shared-agreements.md` equals the repo file's.
3. **Cut `~/.claude/CLAUDE.md` to machine lines** and commit to the config repo. Check: no
   line in `CLAUDE.md` restates a line of `shared-agreements.md` (`consistency-checker:
   cross-document-checker` on the two files).
4. **Write `~/.claude/rules/homelab.md`** if Phase 1 home did not already, commit. Check: a
   session touching a matching path lists it under `/memory`; a non-matching session does
   not.
5. **Fresh-machine restore, for real this time:** `CLAUDE_CONFIG_DIR` at an empty directory,
   clone the config repo into it, start Claude Code once, confirm the marketplace is cloned
   and the packs cached (Phase 0 proof 4a's method, now with the real `settings.json`).

## Steps, work half

1. Updater by hand; `shared-agreements.md` installed; `shasum` equals home's.
2. Cut the work `CLAUDE.md` to machine lines; the line that covers trigger-time routing for
   company skills stays. Commit to the work config repo.
3. `~/.claude/rules/brand.md` and `partner-central.md` exist from Phase 1 work; confirm they
   are committed and that `settings.json` carries no absolute path (`grep -c
   '/Users/' ~/.claude/settings.json` prints `0`).
4. The work config repo now holds `settings.json`, `CLAUDE.md` machine lines, `rules/`,
   plans, lessons, the denylist, and no skills, agents or hook scripts that live in packs
   (`ls ~/.claude/skills ~/.claude/agents ~/.claude/hooks` shows only company-only or
   `.superseded` entries).

## Verification, from scratch, in a fresh context (both machines)

Run the definition-of-done checks in `docs/end-state.md` as written, routed to
`verification-kit:pre-delivery-verifier` and `consistency-checker:cross-document-checker`,
not by re-reading the state files. Record each check's command and output in that
machine's state file. Any check that fails sends the run back to the phase that owns it;
Gate B does not open on a red check.

Regenerate every generated artifact after the last content edit: `bash
maintainers/scripts/generate-inventory.sh`, `python3 maintainers/scripts/generate-pack-map.py`,
then `bash scripts/validate-skills.sh` exit 0; the validator's staleness checks are part of
Gate B.

## Gate B (never pre-authorized)

Present the enumerated deletion list with where each item remains recoverable:

- `find ~/skill-library ~/.claude -name '*.superseded'` on both machines (the old hook
  scripts in `~/.claude/hooks/`, the moved skills' sources in the company marketplace clone,
  any pack directory superseded in Phase 1), each recoverable from git history of the repo
  it was in.
- The disabled `@<brand>-skills` copies of generic packs on the work laptop (`claude plugin
  uninstall`), recoverable by `claude plugin install`.
- The design session's scratchpad clones, already gone with that session.

Wait for explicit confirmation of the list. Execute only the confirmed items, on each
machine in turn. Post-deletion smoke: validator exit 0 on both clones, `version_compare`
identical, a fresh headless session resolves one skill per pack exactly once.

## Residue

Before this harness closes, every open item in both state files has a destination:

- The weekly maintainer fold (design Phase 4, Decision F) is a named successor project; its
  starting point is this harness's `CONFIG.md` and the paused-or-resumed state of the
  maintainer recorded in `STATE-work.md`.
- The archive review of other repos (`GFMCloud/claude-config` snapshot, `gfm-foundry`
  templates, the two superseded weekly routines) stays with the archive review session; this
  harness only resets or reuses `claude-config` per G1.
- Anything else found and not closed: an owned open item in the state file, or dropped with
  the reason written next to it. "Nobody owns this" is written down as such, never implied.

## Rollback (6b: "config repos are new; deleting the remote leaves ~/.claude as it was")

Before Gate B: delete the config repo remote (`git -C ~/.claude remote remove origin`); the
local `~/.claude` is unchanged by the remote's existence, and the `CLAUDE.md` cut is one
commit to `git checkout`. The shared rules file and the updater step are one skill-library
PR to revert. After Gate B there is no rollback; that is why it is a gate.

## Done when

- Both config repos exist with the allowlist gitignore, each machine's `~/.claude` pushes
  to its own, and the fresh-machine restore (home step 5) succeeded with the real settings.
- `shared-agreements.md` is installed on both machines with identical checksums, and neither
  `CLAUDE.md` restates a line of it.
- Every definition-of-done check in `docs/end-state.md` passed from scratch, output recorded.
- Gate B confirmed and executed; `find ... -name '*.superseded'` empty on both machines;
  post-deletion smoke green.
- Residue has a destination for every open item in both state files.
- Both state files: status `COMPLETE (date)`, SHA recorded; `maintainers/MIGRATION.md`
  gains a dated section pointing at this directory as the permanent record.
