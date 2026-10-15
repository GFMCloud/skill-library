# Phase -1 - Read-only survey of the work laptop

**Nature:** STRICTLY READ-ONLY survey. Nothing on this laptop or in any repo is modified,
moved, renamed or deleted, with two stated exceptions: step 4 pushes and deletes a throwaway
branch on the public repo (the only way to prove push end to end), and step 8 pauses the
weekly maintainer (recorded with its undo). The only file written is `STATE-work.md`.

**Machine:** work laptop only. **Prerequisite:** the harness PR is merged to `main` of
`GFMCloud/skill-library` so this runbook can be read from a clone; nothing else.

Every row below is a command. Its output is pasted into `STATE-work.md` under "Phase -1
survey", one subsection per row, **redacted**: the home directory written as `~`, coworker
logins replaced by a count, no customer or company name. The expected output says what a
healthy result looks like; the "changes the plan if" column is what to look for.

## Step 0: machine detection

```bash
gh api user --jq .login
```

Expected: `gmorris1221`. Any other login (including `GFMCloud`): **stop here**, this runbook
does not run on that machine. Record the output.

Negative control for machine detection (the design's 6b): this runbook's step 0 run on the
home laptop prints `GFMCloud` and stops. `STATE-home.md` records that run from the Phase 0
home runbook; it is not repeated here.

## Steps

| # | Check | Command | Expected | Changes the plan if |
|---|---|---|---|---|
| 1 | Managed settings | `ls -la "/Library/Application Support/ClaudeCode/" 2>&1; cat "/Library/Application Support/ClaudeCode/managed-settings.json" 2>/dev/null; ls "/Library/Managed Preferences/$(whoami)/" 2>&1; claude config list 2>&1` | `No such file or directory` for the directory and the managed preferences, or files that set none of the keys at right | Any of `strictKnownMarketplaces`, `blockedMarketplaces`, `disableSideloadFlags`, `allowManagedHooksOnly` present: **stop the whole project**; adding `skill-library` or running user hooks is blocked and the design changes |
| 2 | Claude Code version | `claude --version` | `2.1.300 (Claude Code)` or later | Older than 2.1.300: the plugin-event fixtures in Phase 2 run against this version, not home's |
| 3 | Identity and credential helper | `gh auth status 2>&1; git config --global --get-all credential.helper` | Exactly one account, `gmorris1221`, active; a credential helper line (`osxkeychain` or `!gh auth git-credential`) | A second account, or no helper: the private marketplace clone and the push test will not work the way Decision C assumes |
| 4 | Push capability, end to end | `git clone --depth 1 https://github.com/GFMCloud/skill-library.git "$TMPDIR/sl-preflight" && git -C "$TMPDIR/sl-preflight" checkout -b preflight/work-2026-10 && git -C "$TMPDIR/sl-preflight" push -u origin preflight/work-2026-10 && git -C "$TMPDIR/sl-preflight" push origin --delete preflight/work-2026-10; rm -rf "$TMPDIR/sl-preflight"` | `* [new branch] preflight/work-2026-10 -> preflight/work-2026-10` then ` - [deleted] preflight/work-2026-10` | `remote: Permission to GFMCloud/skill-library.git denied`: the collaborator grant or the helper is not live; Phase 0 work cannot start. Only `main` is protected, so a new branch push is allowed |
| 5 | Live `~/.claude` versus its repo | `git -C ~/.claude status --short; git -C ~/.claude log -1 --format='%h %ad %s' --date=short; cat ~/.claude/settings.local.json 2>&1; echo "PLUGIN_DIRS=$CLAUDE_CODE_PLUGIN_DIRS"; jq '.env' ~/.claude/settings.json` | Empty status, a recent commit, no `settings.local.json`, empty `PLUGIN_DIRS`, an `env` object (or `null`) | Uncommitted edits or an `@inline` plugin dir: the clone the design read is not what runs; record the diff summary |
| 6 | Installed packs and versions | `claude plugin list --json \| jq -r '.[] \| "\(.id) \(.version) enabled=\(.enabled)"' \| sort; jq 'to_entries \| map({key, autoUpdate: .value.autoUpdate})' ~/.claude/plugins/known_marketplaces.json` | 11 catalogued packs plus `codex` from the company marketplace, each `enabled=true` or `false`; `autoUpdate` per marketplace | Fewer enabled packs than the catalog, or `autoUpdate: true` on the company marketplace: the Phase 1 pack-drop order and the coworker notice depend on it |
| 7 | Hook events actually wired | `jq -c '.hooks \| keys' ~/.claude/settings.json; jq -r '.hooks[][].hooks[].command' ~/.claude/settings.json \| sed "s#$HOME#~#g"` | The 2026-10-15 clone shows `["Notification","PermissionDenied","PostToolUse","PreToolUse","SessionStart","Stop","SubagentStop"]`; commands under `~/.claude/hooks/` | Any event or command not in the clone: Phase 2's fixture list is built from this live output, not the clone |
| 8 | Scheduled automation, and pause the weekly maintainer | `ls ~/Library/LaunchAgents; launchctl list 2>/dev/null \| grep -i -E 'claude\|maintainer\|skill' \|\| echo "no matching launchd jobs"; ls ~/.claude/scheduled-tasks/ 2>&1` then, in a Claude Desktop session, list the scheduled tasks and **pause** the weekly maintainer task (disable it; do not delete it). Record its task id and the exact resume action. | The maintainer appears as a Claude Desktop scheduled task (its STATE records registry `nextRunAt` values and a 14:30 local fire); after the pause it shows as disabled | It is scheduled some other way (launchd, cron): pause it by that mechanism instead and record the undo. **Phase 1 does not start while it is active**; it makes local commits to skills |
| 9 | Cowork and claude.ai use | `ls ~/Documents/Claude/ 2>&1; ls ~/Documents/Claude/_shared/ 2>&1; find ~/Documents/Claude -maxdepth 4 -name marketplace.json 2>/dev/null \| sed "s#$HOME#~#g"` and record Graham's answer to: "Do you use Cowork with the company marketplace on this Mac?" | The marketplace clone's location under `~/Documents/Claude`, and a yes or no | Yes, or coworkers load it through Cowork: `~/skill-library` also needs a copy or symlink under `~/Documents/Claude`, and the `git-subdir` entries are needed on day one (Gate A row G4) |
| 10 | Who else consumes the private marketplace | `gh api repos/gmorris1221/awsp-skill-marketplace/collaborators --jq 'length'` and, kept on this laptop only, `gh api repos/gmorris1221/awsp-skill-marketplace/collaborators --jq '.[].login'` | A count; the login list stays in the work config repo, not in this file | More than one collaborator: coworkers are told before any pack drop (Gate A row G5) |
| 11 | Source of the denylist | `grep -n -i sanitiz ~/.claude/.gitignore; grep -rl -i 'sanitize' ~/.claude --include='*.md' --include='*.txt' --include='*.json' 2>/dev/null \| grep -v '/projects/' \| sed "s#$HOME#~#g"` | The `.gitignore` comment ("customer names on a sanitize list") and the path of the list itself; record the path and `wc -l`, **never its contents** | No list found: the denylist is built by hand from Graham's knowledge before Phase 0 work step 3, and `STATE-work.md` says so |
| 12 | Uncommitted work in the two work repos | `find ~ -maxdepth 4 -type d -name awsp-skill-marketplace 2>/dev/null \| sed "s#$HOME#~#g"; git -C "$(find ~ -maxdepth 4 -type d -name awsp-skill-marketplace 2>/dev/null \| head -1)" status --short \| wc -l; git -C ~/.claude status --short \| wc -l` | The clone path and `0` twice | Non-zero: those edits are not in the clone the design read; commit or record them before Phase 1 merges |

## Record

1. Paste every row's output into `STATE-work.md` under "Phase -1 survey", redacted as the
   header says. Set the status line to `Phase -1 complete (date)` and tick the tracker.
2. Commit on a branch `survey/work-2026-10` in the work clone made in Phase 0 work step 1
   (or, if Phase 0 work has not run, in the throwaway clone of step 4 before deleting it:
   keep the clone until the commit is pushed). Author email per `work_commit_email` in
   `CONFIG.md`. Open a PR as `gmorris1221`. CI's denylist scan is the mechanical check on the
   redaction; a red `denylist` job means the paste leaked a pattern, fix the paste.

## Anomalies

Anything this runbook did not anticipate goes in `STATE-work.md` under Anomalies with a
one-line recommendation, reviewed at Gate A. Do not interrupt the run for it. Interrupt only
for step 1 finding a managed lockdown or step 4 finding no push access.

## Rollback

- Step 4: the throwaway branch is deleted by the command itself; if the delete failed, `git
  push origin --delete preflight/work-2026-10` from any clone as `gmorris1221`.
- Step 8: re-enable the scheduled task by the recorded resume action. Nothing else changed.

## Done when

- Every row of the table has its command and redacted output in `STATE-work.md`.
- Row 1 found no managed lockdown, or the project is stopped with the finding recorded.
- Row 4 printed both the `[new branch]` and the `[deleted]` lines.
- Row 8's pause is recorded with the task id and the resume action.
- Row 11 recorded the sanitize list's path, or recorded that none exists.
- `STATE-work.md` status reads `Phase -1 complete`, with the PR number of the survey commit.
