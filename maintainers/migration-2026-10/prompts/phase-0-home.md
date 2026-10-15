# Phase 0 (home) - Protect main, add the denylist scan, commit the updater's plist, run the home proofs

**Nature:** greenfield build on the public repo and this laptop's `~/.claude`. It changes
nothing on the work laptop and disables nothing anywhere. Each deliverable is its own PR.

**Machine:** home laptop only. **Prerequisite:** the harness PR is open (this runbook, the
state files and `CONFIG.md` exist on a branch). Phase -1 on the work laptop is **not** a
prerequisite; the two Phase 0 halves are independent.

## Step 0: machine detection

```bash
gh api user --jq .login
```

Expected: `GFMCloud`. Anything else: **stop here**.

Negative control, run once in this phase and recorded in `STATE-home.md`:

```bash
gh auth switch --user gmorris1221 && gh api user --jq .login; gh auth switch --user GFMCloud && gh api user --jq .login
```

Expected: `gmorris1221` on the first line (the step above would have stopped), `GFMCloud` on
the second (switched back). A read-only switch; nothing is written as gmorris1221.

## Steps

### 1. Branch protection on `main` (its own PR carries the evidence)

Before, expected `Branch not protected (HTTP 404)`:

```bash
gh api repos/GFMCloud/skill-library/branches/main/protection
```

Apply, covered by `auth_branch_protection`. Required check context per
`required_status_check` in `CONFIG.md`; no required approvals (Graham holds both accounts);
`enforce_admins` on, otherwise the GFMCloud admin account bypasses the check from this laptop;
`strict` off, so stacked PRs need not be rebased before each merge:

```bash
gh api -X PUT repos/GFMCloud/skill-library/branches/main/protection --input - <<'JSON'
{"required_status_checks":{"strict":false,"contexts":["validate"]},"enforce_admins":true,"required_pull_request_reviews":null,"restrictions":null}
JSON
```

After, expected JSON with `required_status_checks.contexts == ["validate"]`,
`enforce_admins.enabled == true`, no `required_pull_request_reviews` key:

```bash
gh api repos/GFMCloud/skill-library/branches/main/protection --jq '{contexts: .required_status_checks.contexts, strict: .required_status_checks.strict, enforce_admins: .enforce_admins.enabled, reviews: (.required_pull_request_reviews != null)}'
```

**Negative control (6b):** a direct push to `main` from a clean clone must be refused. Only
after the GET above shows the protection; an empty commit, so that if the gate failed open
the only damage is a visible empty commit on `main`:

```bash
git clone --quiet https://github.com/GFMCloud/skill-library.git "$TMPDIR/sl-negative" && git -C "$TMPDIR/sl-negative" commit --allow-empty -q -m "negative control: direct push to main must be refused" && git -C "$TMPDIR/sl-negative" push origin main; echo "push exit=$?"; rm -rf "$TMPDIR/sl-negative"
```

Expected: `remote: error: GH006: Protected branch update failed for refs/heads/main` with
`Required status check "validate" is expected`, and `push exit=1`. A `push exit=0` means the
gate is open: remove the protection, record the anomaly, stop.

Later, once the denylist PR (step 2) is merged and `main` carries the `denylist` job, add it
to the contexts with the same PUT, `"contexts":["validate","denylist"]`, and record the GET.
Adding it earlier blocks every PR whose branch predates the job.

### 2. Denylist scan: script, CI job, secret, local file (its own PR)

The scan reads one extended regex per line from `denylist_file` (`DENYLIST_FILE`, default
`~/.claude/denylist.txt`), refuses a pattern file inside the repo, refuses a missing or
empty pattern file (exit 2), scans every tracked file (`--staged`: the index) with
`git grep -I -i -E`, and exits 1 on any match. CI takes the patterns from the repository
secret `denylist_ci_secret`, writes them to `$RUNNER_TEMP`, and runs the same script.

1. Write `scripts/denylist-scan.sh` and add the `denylist` job to
   `.github/workflows/validate.yml`. Add both to the `CONTRIBUTING.md` layout list.
2. Seed `~/.claude/denylist.txt` on this laptop (covered by `auth_local_denylist`): the
   company name, the work laptop's user name, the brand prefix, plus one fixture-only token
   `DENYLIST-FIXTURE-TOKEN-2026-10` so the negative control never needs a real name in a
   public commit. The file's content is never pasted anywhere in this repo; record only
   `wc -l`. The work laptop builds its own file from the sanitize list in Phase 0 work.
3. Set the secret (covered by `auth_actions_secret`):

   ```bash
   gh secret set DENYLIST_PATTERNS --repo GFMCloud/skill-library < ~/.claude/denylist.txt && gh secret list --repo GFMCloud/skill-library
   ```

   Expected: a `DENYLIST_PATTERNS` row with today's date.

**Negative controls (6b), local, all four recorded:**

```bash
printf 'planted DENYLIST-FIXTURE-TOKEN-2026-10 here\n' > maintainers/migration-2026-10/fixture.tmp && git add maintainers/migration-2026-10/fixture.tmp && bash scripts/denylist-scan.sh --staged; echo "staged exit=$?"
```

Expected: the match line (file, line number) and `staged exit=1`. Then:

```bash
git rm -q --cached maintainers/migration-2026-10/fixture.tmp && rm maintainers/migration-2026-10/fixture.tmp && bash scripts/denylist-scan.sh; echo "clean exit=$?"
```

Expected: `denylist: clean (<n> tracked files, <m> patterns)` and `clean exit=0`. Then the
two misconfigurations, both expected `exit=2`:

```bash
DENYLIST_FILE=/nonexistent bash scripts/denylist-scan.sh; echo "missing exit=$?"; DENYLIST_FILE=CONTRIBUTING.md bash scripts/denylist-scan.sh; echo "inside-repo exit=$?"
```

**Negative control, CI:** push a throwaway branch `preflight/denylist-negative-control` off
the denylist PR's branch with the planted fixture committed, open a PR, wait for the
`denylist` job to fail, record its conclusion, close the PR unmerged and delete the branch.
The denylist PR itself must then show `denylist` green. GitHub masks the matched text in the
log because it equals a secret; the file and line number are enough.

```bash
gh pr checks <throwaway PR number> --repo GFMCloud/skill-library
```

Expected: `denylist  fail` and `validate  pass`.

### 3. The updater's launchd plist (its own PR)

```bash
cp ~/Library/LaunchAgents/com.gfm.skill-library-plugin-update.plist scripts/ && diff ~/Library/LaunchAgents/com.gfm.skill-library-plugin-update.plist scripts/com.gfm.skill-library-plugin-update.plist && echo identical
```

Expected: `identical`. Add the install note to `CONTRIBUTING.md`: copy with the home
directory substituted (the committed file carries this laptop's `/Users/gfm`), then
`launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/<label>.plist`. Check the live job:

```bash
launchctl print "gui/$(id -u)/com.gfm.skill-library-plugin-update" | grep -E 'state|program|last exit' | head -5
```

Expected: a `state = ...` line and `program = /bin/zsh`.

### 4. Home proofs (6b, "proofs that can run on the home laptop now"), recorded in `STATE-home.md`

**4a. Fresh-machine restore.** An empty config dir plus a `settings.json` that declares
`extraKnownMarketplaces` and `enabledPlugins`; then one Claude Code start. Docs claim: the
missing marketplace is cloned and the enabled packs cached.

```bash
mkdir -p "$TMPDIR/fresh-claude" && printf '{"extraKnownMarketplaces":{"skill-library":{"source":{"source":"github","repo":"GFMCloud/skill-library"}}},"enabledPlugins":{"foundry-core@skill-library":true}}\n' > "$TMPDIR/fresh-claude/settings.json" && CLAUDE_CONFIG_DIR="$TMPDIR/fresh-claude" claude -p "Say OK" --model haiku; echo "exit=$?"; ls "$TMPDIR/fresh-claude/plugins/marketplaces" "$TMPDIR/fresh-claude/plugins/cache/skill-library" 2>&1
```

Expected: `OK`, then `skill-library` under `marketplaces/` and `foundry-core` under
`cache/skill-library/`. If the fresh config dir has no credentials and the run stops at sign
in, record that: the restore story then needs one interactive sign-in first, which Decision
C already lists for the work machine.

**4b. Three-way merge dry run** on three of the 41 (rows 22, 25, 28 of the direction table:
`output-lint`, `plan-gate`, `proof-of-work`), base = `base_commit`, ours = `main`, theirs =
the work copy from `work_copies_for_dry_run`. `git merge-file` exits with the number of
conflicts:

```bash
git show ecbab91:plugins/turn-reduction/skills/plan-gate/SKILL.md > "$TMPDIR/base.md" && cp plugins/turn-reduction/skills/plan-gate/SKILL.md "$TMPDIR/ours.md" && cp "<work_copies_for_dry_run>/awsp-skill-marketplace/plugins/workbench/skills/plan-gate/SKILL.md" "$TMPDIR/theirs.md" && git merge-file -p --diff3 -L library -L base -L work "$TMPDIR/ours.md" "$TMPDIR/base.md" "$TMPDIR/theirs.md" > "$TMPDIR/merged.md"; echo "conflicts=$?"; grep -c '^<<<<<<<' "$TMPDIR/merged.md"
```

Record per skill: lines changed on each side since the base (`diff base ours | grep -c '^[<>]'`,
same for theirs), the conflict count, and how many hunks resolved themselves. Fill the
`note` column of the direction table for those rows. If the work copies are gone, record
that and skip.

**4c. Version comparison command** per `version_compare` in `CONFIG.md`, so the expected
output is known before the work laptop runs it. Record the output verbatim: 12 lines, one
pack per line with its version.

### 5. Record

`STATE-home.md`: Phase 0 home checked, every command above with its output under Evidence,
anomalies logged, the PR numbers, and the `main` SHA this laptop was brought to after the
last of these PRs merged (`git -C ~/skill-library rev-parse --short origin/main`).

## Anomalies

Anything this runbook did not anticipate goes in `STATE-home.md` under Anomalies with a
one-line recommendation, reviewed at Gate A. Interrupt only for a gate that fails open.

## Rollback (6b: "Phase 0: nothing else changed")

- Branch protection: `gh api -X DELETE repos/GFMCloud/skill-library/branches/main/protection`.
- Denylist: revert the denylist PR (`git revert` of its merge commit; this is not a shallow
  clone, check `git rev-parse --is-shallow-repository` first), `gh secret delete
  DENYLIST_PATTERNS --repo GFMCloud/skill-library`, `rm ~/.claude/denylist.txt`.
- Plist: revert its PR; the live launchd job was never touched.
- Proofs: `rm -rf "$TMPDIR/fresh-claude"`; the dry run wrote only to `$TMPDIR`.

## Done when

- The protection GET shows `validate` required with `enforce_admins` on, and the direct push
  was refused with `GH006` (output recorded).
- The planted fixture failed the scan locally (`exit=1`) and on CI (`denylist fail` on the
  throwaway PR); the clean tree passed both; missing and inside-repo pattern files exit 2.
- `scripts/com.gfm.skill-library-plugin-update.plist` is byte-identical to the live plist and
  `CONTRIBUTING.md` says how to install it.
- Proofs 4a, 4b and 4c have their output in `STATE-home.md`, and the direction table's note
  column carries the dry-run numbers for its three rows.
- The harness PR, the three Phase 0 PRs and the proofs PR are open or merged with CI green.
- `STATE-home.md`: Phase 0 home checked, evidence recorded, SHA recorded, session log line
  added; `STATE-work.md` still reads `Phase -1 survey not started`.
