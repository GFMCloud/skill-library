# Phase 0 (work) - Install skill-library on the work laptop; disable nothing

**Nature:** greenfield build on the work laptop. It adds a clone, a marketplace, 12 packs,
two env entries, a launchd job and a pre-commit hook. **It disables and drops nothing**: the
company packs that overlap stay enabled until Phase 1 empties them, because `workbench` and
`<brand>-decks` still hold work-only skills and the work `CLAUDE.md` still names
`workbench:*` (advisor review, 2026-10-15). Duplicate descriptions cost tokens for a few
weeks, not capability.

**Machine:** work laptop only. **Prerequisite:** `STATE-work.md` shows Phase -1 complete
with no managed lockdown (row 1) and a successful push test (row 4); `STATE-home.md` shows
Phase 0 home complete (the denylist job and the plist are on `main`). Nothing in this runbook
is executed from the home laptop.

## Step 0: machine detection

```bash
gh api user --jq .login
```

Expected: `gmorris1221`. Anything else: **stop here**.

## Steps

### 1. Clone, with the noreply author email

```bash
git clone https://github.com/GFMCloud/skill-library.git ~/skill-library && git -C ~/skill-library config user.email 280596865+gmorris1221@users.noreply.github.com && git -C ~/skill-library config user.email && git -C ~/skill-library rev-parse --short HEAD
```

Expected: the noreply address (`work_commit_email` in `CONFIG.md`) and the `main` SHA;
record the SHA as the commit this machine was brought to.

### 2. The denylist and the pre-commit hook (covered by `auth_plugin_install_work`)

Build `~/.claude/denylist.txt` from the sanitize list Phase -1 row 11 located: one extended
regex per line, `#` comments allowed; the company name, customer names, people, 12-digit
account IDs (`\b[0-9]{12}\b`), opportunity-ID shapes, internal hostnames, the work user name.
Commit the file to the work config repo (it is `~/.claude`, allowlisted; add `!/denylist.txt`
to its `.gitignore`). Record `wc -l` only. Then install the hook:

```bash
printf '#!/bin/sh\nexec bash "$(git rev-parse --show-toplevel)/scripts/denylist-scan.sh" --staged\n' > ~/skill-library/.git/hooks/pre-commit && chmod +x ~/skill-library/.git/hooks/pre-commit && cat ~/skill-library/.git/hooks/pre-commit
```

**Negative control (6b):** a fixture with one planted customer name must be refused by the
hook; the same file with the name removed must pass. The planted name is typed into a file
that is never committed and never pasted into this repo:

```bash
printf 'planted name here\n' > ~/skill-library/fixture.tmp && git -C ~/skill-library add fixture.tmp && git -C ~/skill-library commit -q -m "negative control" ; echo "commit exit=$?"; git -C ~/skill-library log -1 --format=%s
```

Expected: the scan's match line, `commit exit=1`, and `git log -1` still showing the `main`
head's subject (no commit was made). Then remove the name from the file, re-stage, run
`bash scripts/denylist-scan.sh --staged; echo "exit=$?"`, expected `exit=0`; then
`git reset -q fixture.tmp && rm fixture.tmp`. Record all of it in `STATE-work.md`, with the
planted name replaced by `<name>`.

Also push the same patterns to the repository secret? **No.** The secret is set from the
home laptop as `home_account` (`auth_actions_secret`); the work laptop sends the pattern
list to Graham for that paste, or the two lists are reconciled at Gate A. Record which.

### 3. The marketplace and the 12 packs

```bash
claude plugin marketplace add GFMCloud/skill-library && claude plugin marketplace list
```

Expected: `skill-library` listed with source `github GFMCloud/skill-library`. Then, one
command per pack name in `packs` (`CONFIG.md`), twelve times:

```bash
claude plugin install foundry-core@skill-library
```

Check with the version comparison command (`version_compare` in `CONFIG.md`). Expected: the
same 12 lines `STATE-home.md` proof 4c recorded, pack for pack and version for version, once
both machines have run the updater. A missing line is an uninstalled pack; a version
mismatch means one machine is behind `main`, which is allowed, and the SHA says which.

### 4. The two env entries

Add to `~/.claude/settings.json` `env`: `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` = `1` and
`CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` = `1` (`work_env` in `CONFIG.md`). Commit to
the work config repo.

```bash
jq '.env | {CLAUDE_CODE_PLUGIN_PREFER_HTTPS, CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE}' ~/.claude/settings.json
```

Expected: both values `"1"`. Needs a Claude Code restart to take effect; say so in the
session log.

### 5. The launchd updater

Install per the `CONTRIBUTING.md` note (home directory substituted into the committed plist,
then `launchctl bootstrap`). Then run the updater once by hand and read its tail:

```bash
launchctl print "gui/$(id -u)/com.gfm.skill-library-plugin-update" | grep -E 'state|program' | head -3; zsh ~/skill-library/scripts/update-installed-plugins.sh | tail -5
```

Expected: `program = /bin/zsh`, and the updater ending `=== done (updates apply to newly
started sessions)` with no `REFUSED` line (the installed and incoming versions are the same
commit, so no hook surface differs).

### 6. Prove that nothing was disabled

```bash
claude plugin list --json | jq -r '.[] | select(.enabled) | .id' | sort
```

Expected: every id Phase -1 row 6 listed as `enabled=true`, plus the 12 `@skill-library`
ids. Any company id missing: re-enable it and record the anomaly.

### 7. Record

`STATE-work.md`: Phase 0 work checked, every command with its output under Evidence, the
SHA from step 1, session log line. Commit `STATE-work.md` on a branch `phase-0/work-2026-10`
and open a PR as `gmorris1221` (the pre-commit hook and CI's `denylist` job both run on it).

## Anomalies

Anything this runbook did not anticipate goes in `STATE-work.md` under Anomalies with a
one-line recommendation, reviewed at Gate A.

## Rollback (6b: "remove the marketplace and packs on the work laptop; nothing else changed")

```bash
claude plugin marketplace remove skill-library
```

removes the marketplace and its 12 installed packs. Then `launchctl bootout
"gui/$(id -u)/com.gfm.skill-library-plugin-update"` and remove the plist from
`~/Library/LaunchAgents`, drop the two `env` entries, `rm ~/skill-library/.git/hooks/pre-commit`,
and `rm -rf ~/skill-library` (it holds no commits of its own by the end of this phase). The
denylist file in the work config repo may stay; it is private.

## Done when

- `version_compare` on this laptop prints 12 lines matching `STATE-home.md` proof 4c.
- The pre-commit hook refused the planted fixture and passed the clean one (output
  recorded, name redacted).
- The updater ran to `=== done` by hand and the launchd job is loaded.
- Step 6 shows every company pack still enabled.
- `STATE-work.md`: Phase 0 work checked, SHA recorded, evidence recorded, PR number recorded.
