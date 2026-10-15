# Project state: home laptop

**The resume point for the home laptop.** Keep it current as you work. The next session on
this machine continues from this file plus the runbooks alone. Machine detection:
`gh api user --jq .login` prints `GFMCloud` here; every entry below was written on that
machine, as that account.

**Status:** Phase 0 home complete (2026-10-15); its five PRs await the fresh review and the
merge in stack order (#52, #53, #54, #56, then the proofs PR)

**Commit of `GFMCloud/skill-library` this machine was last brought to:** `main` is `90711b2`
(2026-10-15; nothing of this harness is merged yet). The working checkout is on the proofs
branch; the stacked branch tips are `50cde2b` (harness), `bec450d` (0a), `fc8fb83` (0b),
`64c97fd` (0c).

## Phase tracker

- [x] Phase 0 home - branch protection, denylist scan, plist, home proofs (`prompts/phase-0-home.md`) (2026-10-15; PRs #52, #53, #54, #56 and the proofs PR open, CI green on each)
- [ ] Phase 1 Gate A - rulings recorded (`prompts/phase-1-gate-a.md`); may run on either machine; needs Phase -1 and Phase 0 complete on both
- [ ] Phase 1 home - three-way merges into skill-library (`prompts/phase-1-home.md`)
- [ ] Phase 2 home half - hooks and agents (`prompts/phase-2.md`); needs Phase 1 work complete in `STATE-work.md`
- [ ] Phase 3 home half - config repo, rules file, shared rules, Gate B (`prompts/phase-3.md`)

## Decision log

<!-- Append: date - decision - one-line rationale. Never rewrite old entries. Gate rulings
     are recorded in gate-a-direction-table.md and summarised here. -->

- 2026-10-15 - Harness scaffolded on branch `migration-2026-10/harness` from
  `long-projects:phased-harness`, without a `/phase` dispatch skill: the archived 2026-08
  harness under `maintainers/migration/harness/.claude/skills/phase` already owns that skill
  name in this repo. Dispatch is by hand per `README.md`.
- 2026-10-15 - The required status check context is `validate`, not `validate-skills`: the
  workflow is named `validate-skills` but its job id is `validate`, and the check-run on
  `main` reports under the job id (`gh api repos/GFMCloud/skill-library/commits/main/check-runs`
  printed `validate | success | github-actions`). Protection names the real context.
- 2026-10-15 - The design's version comparison command selects on `.marketplace`, a key
  `claude plugin list --json` does not emit (keys: `enabled,id,installPath,installedAt,
  lastUpdated,projectEnabled,scope,version`); it printed nothing on 2.1.300. CONFIG.md
  `version_compare` selects on the `id` suffix instead.
- 2026-10-15 - The fresh-machine restore needs an interactive sign-in before the first
  start: with an empty `CLAUDE_CONFIG_DIR`, `claude -p` stops at "Not logged in" and the
  plugin CLI does not read `extraKnownMarketplaces` from `settings.json` (proof 4a). The docs
  claim that a declared marketplace is cloned on start is unverified on this laptop; Decision
  C's restore steps gain `claude login` ahead of the first start, and Phase 3 home step 5
  repeats the proof after sign-in. Recorded in `prompts/phase-3.md`.
- 2026-10-15 - A bare 12-digit account-ID pattern is not seeded in the home denylist: it
  matches 100 lines of existing tracked content (`git grep -E '[0-9]{12}'`). The work
  laptop's list carries the real account-ID shapes from the sanitize list (Phase 0 work
  step 2).
- 2026-10-15 - The first denylist scan failed on the Phase 0 runbook itself, which spelled
  the fixture token out. The runbook now takes it from the pattern file's last line. The
  gate caught its own harness before CI ever ran.

## Evidence

<!-- Executed evidence, not checkmarks: the command run and its actual output. Negative
     controls go here verbatim. Format per foundry-core:evidence-report. -->

### Harness scaffold (2026-10-15)

Work copies used for the Phase 0 dry run (`work_copies_for_dry_run` in CONFIG.md): shallow
clones made by the design session on 2026-10-15 under its scratchpad,
`.../1c215210-37ed-4365-bae4-7039cf9aa205/scratchpad/work-repos/{awsp-skill-marketplace,
personal-claude-config,claude-weekly-maintainer}`. They are deleted with that session.

### Phase 0 step 0: machine detection and its negative control (2026-10-15)

```
$ gh api user --jq .login
GFMCloud
$ gh auth switch --user gmorris1221; gh api user --jq .login
✓ Switched active account for github.com to gmorris1221
gmorris1221
$ gh auth switch --user GFMCloud; gh api user --jq .login
✓ Switched active account for github.com to GFMCloud
GFMCloud
```

With the wrong account active the step prints `gmorris1221`, which is the stop condition.
Nothing was written as gmorris1221.

### Phase 0 step 1: branch protection on main (2026-10-15)

Before:

```
$ gh api repos/GFMCloud/skill-library/branches/main/protection
{"message":"Branch not protected","documentation_url":"https://docs.github.com/rest/branches/branch-protection#get-branch-protection","status":"404"}
gh: Branch not protected (HTTP 404)
```

Applied (PUT, `auth_branch_protection`) with `{"required_status_checks":{"strict":false,
"contexts":["validate"]},"enforce_admins":true,"required_pull_request_reviews":null,
"restrictions":null}`. After:

```
$ gh api repos/GFMCloud/skill-library/branches/main/protection --jq '{contexts: .required_status_checks.contexts, strict: .required_status_checks.strict, enforce_admins: .enforce_admins.enabled, reviews: (.required_pull_request_reviews != null), restrictions: (.restrictions != null)}'
{"contexts":["validate"],"enforce_admins":true,"restrictions":false,"reviews":false,"strict":false}
```

Negative control (6b): fresh clone into the scratchpad, one empty commit, direct push to
`main`:

```
$ git clone --quiet https://github.com/GFMCloud/skill-library.git <scratchpad>/sl-negative
$ git -C <scratchpad>/sl-negative commit --allow-empty -q -m "negative control: direct push to main must be refused"
$ git -C <scratchpad>/sl-negative push origin main
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote:
remote: - Required status check "validate" is expected.
To https://github.com/GFMCloud/skill-library.git
 ! [remote rejected] main -> main (protected branch hook declined)
error: failed to push some refs to 'https://github.com/GFMCloud/skill-library.git'
push exit=1
$ gh api repos/GFMCloud/skill-library/branches/main --jq '.commit.sha[0:7] + " " + (.commit.commit.message | split("\n")[0])'
90711b2 deny-destructive: forced branch delete passes for branches already on origin/main (registry, fixture, changelog) (#50)
```

The clone was removed afterwards. Pending: once the denylist PR is merged and `main` carries
the `denylist` job, add it to the required contexts (Phase 0 home runbook, step 1, last
paragraph). Owner: the session that merges that PR.

### Phase 0 step 2: denylist scan (2026-10-15), PR #54

Local pattern file `~/.claude/denylist.txt`: 16 lines, 4 patterns; content never recorded
here. Secret:

```
$ gh secret set DENYLIST_PATTERNS --repo GFMCloud/skill-library < ~/.claude/denylist.txt && gh secret list --repo GFMCloud/skill-library
DENYLIST_PATTERNS	2026-10-15T12:40:26Z
```

Negative controls, local, token written `<fixture token>` here:

```
$ printf 'planted %s here\n' "$(tail -1 ~/.claude/denylist.txt)" > maintainers/migration-2026-10/fixture.tmp && git add maintainers/migration-2026-10/fixture.tmp && bash scripts/denylist-scan.sh --staged; echo "staged exit=$?"
maintainers/migration-2026-10/fixture.tmp:1:planted <fixture token> here
maintainers/migration-2026-10/prompts/phase-0-home.md:83:   `<fixture token>` so the negative control never needs a real name in a
maintainers/migration-2026-10/prompts/phase-0-home.md:97:printf 'planted <fixture token> here\n' > ...
denylist: 3 match(es) in tracked files (index; 4 patterns from /Users/gfm/.claude/denylist.txt)
staged exit=1
```

Two of the three matches were the runbook itself spelling the token (decision log). After
rewording the runbook and removing the fixture:

```
$ git rm -q --cached maintainers/migration-2026-10/fixture.tmp && rm maintainers/migration-2026-10/fixture.tmp && bash scripts/denylist-scan.sh; echo "clean exit=$?"
denylist: clean (1413 tracked files, 4 patterns, tree)
clean exit=0
$ bash scripts/denylist-scan.sh --staged; echo "staged exit=$?"      # after staging the reworded runbook
denylist: clean (1414 tracked files, 4 patterns, index)
staged exit=0
$ DENYLIST_FILE=/nonexistent bash scripts/denylist-scan.sh; echo "missing exit=$?"
denylist: no pattern file at /nonexistent (set DENYLIST_FILE)
missing exit=2
$ DENYLIST_FILE=CONTRIBUTING.md bash scripts/denylist-scan.sh; echo "inside-repo exit=$?"
denylist: pattern file /Users/gfm/skill-library/CONTRIBUTING.md is inside the repository; the denylist never lives in this public repo
inside-repo exit=2
```

Negative control, CI: throwaway PR #55 (branch `preflight/denylist-negative-control` off the
denylist branch, one committed file carrying the fixture token):

```
$ gh pr checks 55 --repo GFMCloud/skill-library
denylist	fail	8s
validate	pass	6s
```

The job log (`gh run view 38736634890 --job 116427479497 --log`), GitHub masking the token
because it equals a secret line:

```
maintainers/migration-2026-10/fixture-negative-control.tmp:1:planted *** here (CI negative control for the denylist scan; this PR is closed unmerged)
denylist: 1 match(es) in tracked files (tree; 4 patterns from /home/runner/work/_temp/denylist.txt)
##[error]Process completed with exit code 1.
```

PR #55 closed unmerged, branch deleted (`gh api .../branches/preflight/denylist-negative-control`
returns 404). The denylist PR itself:

```
$ gh pr checks 54 --repo GFMCloud/skill-library
denylist	pass	5s
validate	pass	6s
```

### Phase 0 step 3: the updater's launchd plist (2026-10-15), PR #56

```
$ cp ~/Library/LaunchAgents/com.gfm.skill-library-plugin-update.plist scripts/ && diff ~/Library/LaunchAgents/com.gfm.skill-library-plugin-update.plist scripts/com.gfm.skill-library-plugin-update.plist && echo identical
identical
$ plutil -lint scripts/com.gfm.skill-library-plugin-update.plist
scripts/com.gfm.skill-library-plugin-update.plist: OK
$ launchctl print "gui/$(id -u)/com.gfm.skill-library-plugin-update" | grep -E 'state =|program =|last exit code'
	state = not running
	program = /bin/zsh
	last exit code = 0
$ gh pr checks 56 --repo GFMCloud/skill-library
denylist	pass	4s
validate	pass	5s
```

### Phase 0 step 4a: fresh-machine restore (2026-10-15)

```
$ mkdir -p <scratchpad>/fresh-claude && printf '{"extraKnownMarketplaces":{"skill-library":{"source":{"source":"github","repo":"GFMCloud/skill-library"}}},"enabledPlugins":{"foundry-core@skill-library":true}}\n' > <scratchpad>/fresh-claude/settings.json
$ CLAUDE_CONFIG_DIR=<scratchpad>/fresh-claude timeout 150 claude -p "Say OK" --model haiku
Not logged in · Please run /login
exit=1
$ ls -R <scratchpad>/fresh-claude          # after
backups/  plugins/installed_plugins.json  plugins/marketplaces/ (empty)  plugins/store/  projects/  sessions/  settings.json
$ cat plugins/installed_plugins.json
{"version": 2, "plugins": {}}
$ CLAUDE_CONFIG_DIR=<scratchpad>/fresh-claude claude plugin marketplace list
Configured marketplaces:
  ❯ anthropic-plugin-directory
    Source: Built in (Anthropic Directory)
$ CLAUDE_CONFIG_DIR=<scratchpad>/fresh-claude claude plugin marketplace update skill-library
Updating marketplace: skill-library...✘ Failed to update marketplace(s): Marketplace 'skill-library' not found. Available marketplaces: anthropic-plugin-directory
exit=1
```

Result: **not proven**. Without a sign-in in the fresh config dir nothing clones the declared
marketplace, headless or through the plugin CLI (`known_marketplaces.json` was never
written). The restore story needs `claude login` first; Phase 3 home step 5 repeats this
proof after an interactive sign-in. The config dir was removed.

### Phase 0 step 4b: three-way merge dry run (2026-10-15)

Base `ecbab91`, ours `main` (`90711b2`), theirs the work copy from `work_copies_for_dry_run`
(company marketplace clone, 2026-10-15). `git merge-file -p --diff3` exits with the conflict
count:

```
output-lint:   base 114 lines; library changed 0 lines in 0 hunks;  work changed 98 lines in 17 hunks;  merge-file exit=0; conflict markers=0; merged 126 lines
plan-gate:     base 139 lines; library changed 4 lines in 2 hunks;  work changed 38 lines in 10 hunks; merge-file exit=1; conflict markers=1; merged 167 lines
proof-of-work: base 143 lines; library changed 18 lines in 4 hunks; work changed 139 lines in 13 hunks; merge-file exit=2; conflict markers=2; merged 262 lines
```

What the conflicts are: `plan-gate`, the frontmatter `description` (both sides rewrote it;
the work text adds Partner Central and CloudFront triggers and `workbench:*`
cross-references, which Decision A sends to a rule file and the canonical names). `proof-of-work`,
the `metadata` block (library 1.6.0 / work 1.1.0 plus the work `source:` tag; mechanical,
library's metadata wins) and one body paragraph both sides edited. Every other hunk
resolved itself: 12 of 13 in `plan-gate`, 15 of 17 in `proof-of-work`, 17 of 17 in
`output-lint`. The merge is tractable: the true conflicts are the description, the
metadata block and the occasional paragraph, not the body.

### Phase 0 step 4c: version comparison (2026-10-15)

```
$ claude plugin list --json | jq -r '.[] | select(.id | endswith("@skill-library")) | "\(.id | split("@")[0]) \(.version)"' | sort
agent-tooling 0.2.2
consistency-checker 0.1.2
data-wrangler 0.1.3
decks 0.4.2
deploy-ops 0.2.3
foundry-core 0.6.8
frontend-design 0.5.2
long-projects 0.19.8
project-starters 0.2.1
turn-reduction 1.4.0
verification-kit 0.6.1
voice-and-editing 1.4.2
```

This is the expected output on the work laptop after Phase 0 work step 3, at the same
`main` commit. The design's original command (`select(.marketplace=="skill-library")`)
printed 0 lines on the same machine.

## Anomalies

<!-- date - what/where - why it does not fit - one-line recommendation. Reviewed at the next
     gate, never resolved silently mid-run. -->

## Open items

<!-- Residue: what - why it is still open - who owns it next. -->

- Review and merge the Phase 0 stack in order (#52 harness, #53 protection evidence, #54
  denylist, #56 plist, then the proofs PR). Each needs a fresh same-or-higher-tier review
  (`auth_merge_pr` is `no`). Owner: Graham, or a fresh reviewing session he starts.
- After #54 is on `main`: add `denylist` to the required status checks (Phase 0 home runbook
  step 1, last paragraph) and record the GET. Owner: the session that merges #54.
- Fresh-machine restore unproven without a sign-in (proof 4a). Owner: Phase 3 home step 5.
- The home denylist holds 4 seed patterns; the full list (customers, people, account-ID and
  hostname shapes) comes from the work laptop's sanitize list and the two are reconciled at
  Gate A, then the secret is re-set from the reconciled file. Owner: Phase 0 work step 2 and
  Gate A.

## Session log

<!-- One line per session: date - phase worked - outcome / stopping point. -->

- 2026-10-15 - harness scaffold - directory written on branch `migration-2026-10/harness`
  (PR #52); Phase 0 home steps follow in their own PRs.
- 2026-10-15 - Phase 0 home step 1 - branch protection applied and proven (direct push
  refused, GH006); recorded on branch `migration-2026-10/phase-0a-branch-protection` (PR #53).
- 2026-10-15 - Phase 0 home steps 2 to 4 - denylist scan written, proven locally and on CI
  (PR #54, throwaway #55 closed), plist committed (PR #56), proofs 4a to 4c run; evidence
  recorded on branch `migration-2026-10/phase-0-proofs`. Phase 0 home complete; next is the
  review and merge of the stack, then Phase -1 on the work laptop.
