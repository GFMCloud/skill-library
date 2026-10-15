# Project configuration

Parameters for the 2026-10 two-laptop skill sync. Sessions **must stop and ask** if any value
is `TBD`. This is the only setup interruption.

## Parameters

| Key | Value | Notes |
|-----|-------|-------|
| `library_repo` | `GFMCloud/skill-library` | Public. The one editable home for generic skills, agents, hook scripts and shared rules. |
| `library_clone` | `~/skill-library` | Writable checkout on both machines. The updater never runs scripts from it. |
| `home_account` | `GFMCloud` | `gh api user --jq .login` must print this on the home laptop. Admin on `library_repo`. |
| `work_account` | `gmorris1221` | Must print this on the work laptop. Collaborator on `library_repo` with pull, push, triage (read 2026-10-15). Never written to from the home laptop. |
| `company_marketplace_repo` | `gmorris1221/awsp-skill-marketplace` | Private marketplace, written `<brand>-skills` here. Holds the company-only packs and, after Phase 1, `git-subdir` entries for the generic packs. Work laptop only. |
| `work_config_repo` | `gmorris1221/personal-claude-config` | The work laptop's `~/.claude`, allowlist `.gitignore`. Holds the work rule files and the denylist. |
| `home_config_repo` | `GFMCloud/claude-config` | Created in Phase 3. Exists today as a one-commit 2026-07-29 snapshot (archive review 2026-10-15); reset or start clean is a Gate A row. |
| `weekly_maintainer` | `gmorris1221/claude-weekly-maintainer`, a Claude Desktop scheduled task firing Tuesdays 14:30 local on the work laptop | Paused in Phase -1 for the length of Phase 1; it makes local commits to skills. |
| `base_commit` | `ecbab9121c0746d464db1b13980e6d9b494b68a6` (`ecbab91`, 2026-09-28) | The skill-library commit 36 of the 41 work copies record as their source. Base of every three-way merge. |
| `shared_skills` | 41, enumerated in [gate-a-direction-table.md](gate-a-direction-table.md) | The only place the list and the count live. 36 carry `base_commit`; 5 do not. |
| `packs` | 12, enumerated by `.claude-plugin/marketplace.json` | foundry-core, turn-reduction, data-wrangler, verification-kit, consistency-checker, deploy-ops, decks, frontend-design, long-projects, project-starters, agent-tooling, voice-and-editing. |
| `required_status_check` | `validate` | The check-run name the `validate-skills` workflow's job reports (job id `validate`, read from `commits/main/check-runs` 2026-10-15). The `denylist` job joins it once its PR is merged. |
| `denylist_file` | `~/.claude/denylist.txt`, overridable with `DENYLIST_FILE` | One extended regex per line, `#` comments. Never a path inside `library_repo`; the scan refuses one. Seeded on the work laptop from the sanitize list Phase -1 locates. |
| `denylist_ci_secret` | `DENYLIST_PATTERNS` | GitHub Actions repository secret on `library_repo`, same content as `denylist_file`. Set and rotated as `home_account`. |
| `launchd_label` | `com.gfm.skill-library-plugin-update` | Daily 09:30. Plist committed at `scripts/com.gfm.skill-library-plugin-update.plist`; install note in `CONTRIBUTING.md`. |
| `work_env` | `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`, `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` | `env` entries in the work `settings.json` (private marketplace, credential helper). |
| `work_commit_email` | `280596865+gmorris1221@users.noreply.github.com` | Per-repo `user.email` on the work checkout of `library_repo` so the company mailbox never enters public history. User id read from the public API 2026-10-15. |
| `claude_version_home` | `2.1.300` (2026-10-15) | The work version is a Phase -1 row. |
| `version_compare` | `claude plugin list --json \| jq -r '.[] \| select(.id \| endswith("@skill-library")) \| "\(.id \| split("@")[0]) \(.version)"' \| sort` | Identical output on both laptops means both run the same skill-library. The design's original command selected on a `.marketplace` key the JSON does not have (proof 3 in STATE-home.md). |
| `hook_checksum` | `shasum ~/.claude/hooks/*.py ~/.claude/rules/shared-agreements.md` | Compared between machines after Phase 2 and Phase 3. |
| `work_copies_for_dry_run` | shallow clones under the design session's scratchpad; path recorded in `STATE-home.md` | Ephemeral. If gone, the Phase 0 dry run is skipped and noted; Phase 1 re-reads them with a read-only gmorris1221 clone. |

## Standing authorizations (for continuous runs)

These grant permission up front so the run does not stop to ask. `no` forces a pause.

| Key | Value | Covers |
|-----|-------|--------|
| `auth_library_pr` | `yes` | Branches, commits and PRs on `library_repo` from either machine; pushes of the session's own commits under the global push carve-out. |
| `auth_branch_protection` | `yes` | The Phase 0 protection PUT on `main` and adding `denylist` to its required checks. Any later change to protection asks. |
| `auth_actions_secret` | `yes` | Setting or rotating `denylist_ci_secret` on `library_repo` as `home_account`. |
| `auth_local_denylist` | `yes` | Writing `denylist_file` on either machine. |
| `auth_plugin_install_work` | `yes` | Phase 0 work: clone, add the marketplace, install the 12 packs, set `work_env`, install the launchd updater, install the pre-commit hook. |
| `auth_local_rules_files` | `yes` | Writing `~/.claude/rules/*.md` on either machine, committed to that machine's config repo. |
| `auth_pause_maintainer` | `yes` | Pausing `weekly_maintainer` in Phase -1 and resuming it after Phase 1 work, each recorded with its undo. |
| `auth_pack_drop` | `no` | Dropping an emptied pack from `company_marketplace_repo` pauses for a ruling each time (coworkers are affected). |
| `auth_settings_rewire` | `no` | Rewiring the hooks block of a `settings.json` (Phase 2) pauses: it is the safety layer. |
| `auth_merge_pr` | `no` | Merging any PR this harness produces needs the fresh same-or-higher-tier review first. |

Resolve every question against this table before asking Graham anything. The table is
human-readable only; `turn-reduction:standing-authorization` ships `authz.py`, which reads
JSON, so a session that wants its `check` and `validate` tooling copies that skill's
`authorization.example.json` beside this file as `authorization.json`, cut down to the same
grants. If the two ever disagree, this table wins.

**Never pre-authorizable:**

- The Gate B deletion list (Phase 3): `.superseded` copies on both machines, the old hook
  scripts, the disabled company copies of generic packs. Always an enumerated list with where
  each item remains recoverable, confirmed explicitly.
- Each pack drop in Phase 1 work (`auth_pack_drop`): `forceRemoveDeletedPlugins` uninstalls
  the pack from every coworker's machine at their next session start. Coworkers are told
  first; the drop and the `CLAUDE.md` reference rewrite go in one commit.
- Any write to GitHub as `work_account` from the home laptop; any `home_account` credential
  on the work laptop.
- Disabling or dropping any company pack in Phase 0.
- Creating, renaming or archiving a repository (`home_config_repo` in Phase 3 is a Gate A
  row; the archive review of other repos is a separate project).
- Committing content that matches the denylist, or changing `scripts/denylist-scan.sh` or
  its CI job so that a match passes.
- Merging a PR without the fresh review (`auth_merge_pr`).

The gates this project defines, enumerated here and nowhere else: **Gate A** (Phase 1, the
direction table and the other Gate A rows), **one gate per pack drop** (Phase 1 work, under
`auth_pack_drop`), **Gate B** (Phase 3, the deletion list). Actions taken under a standing
authorization are still logged in the state files.

## Decisions A to F

Carried from the 2026-10-15 design, section 4, verbatim except for the redactions this
public directory requires: the company's name is written "the company", its brand packs
`<brand>-core`, `<brand>-decks`, `<brand>-design`, its marketplace `<brand>-skills`, and the
provenance pack label after each `ecbab91` source tag is dropped. Nothing else is reworded.

### Decision A: one home for generic skills, on both machines (do this first)

| Repo | Account | Visibility | Holds | Both machines? |
|---|---|---|---|---|
| `skill-library` | GFMCloud | public | Every generic skill, agent and hook script. Already exists. | Installed on both; writable checkout at `~/skill-library` on both. |
| `<brand>-skills` marketplace | gmorris1221 | private | Company-only packs. For coworkers and other surfaces it also lists the generic packs by reference (below). | Work machine only. |

**The loop on either machine:** edit in `~/skill-library`, bump the pack `version`, run the
validator, open a PR, merge after CI. The other machine's daily updater pulls it. From the
work machine the PR is authored by gmorris1221, which **already has push access**
(collaborator list read 2026-10-15: `gmorris1221 pull,push,triage`). One `gh` identity per
machine; the work machine's rule that it connects only as gmorris1221 stays intact.
`main` on skill-library is not protected today (API read 2026-10-15); protect it to require
the CI status check. Required approvals would add nothing, since you hold both accounts.

**Environment context stops living in generic bodies.** It moves into **path-scoped rule
files** under `~/.claude/rules/` in each machine's config repo (Decision C). Claude Code
loads a rule file with a `paths:` frontmatter only when the session touches a matching file
("These conditional rules only apply when Claude is working with files matching the
specified patterns", docs `memory`), and user-level rules "apply to every project on your
machine". So the work machine carries `~/.claude/rules/partner-central.md` (Partner Central
writes and CloudFront boards are blast radius; delegate live reads to `aws-readonly-recon`)
and the home machine carries `~/.claude/rules/homelab.md` (restic, Traefik, Proxmox). The
generic skill body says nothing about either. This needs **no change to skill-library** and
costs no tokens on the machine that lacks the rule. The first draft proposed an overlay seam
read by every generic skill; the advisor review showed it leaky (paid on every invocation on
both machines, and it breaks the public authoring rule that a pack loads nothing outside
itself), so it is withdrawn. Where a skill genuinely needs machine data at run time, the
documented tool is `!`command`` injection in the skill body, written fail-safe
(`cat ~/.claude/x.md 2>/dev/null || true`), since a failed command aborts the skill.
Trigger phrases in a skill's `description` cannot be scoped this way; those stay generic, and
a line in the work `CLAUDE.md` covers trigger-time routing.

**Pack names are the namespace.** Once the work machine runs `skill-library` packs,
`workbench:x` becomes `foundry-core:x`, `turn-reduction:x` and so on. The work `CLAUDE.md`
and the company skills that cross-reference `workbench:*` change in the same PR that drops
the pack. The marketplace `renames` map moves an install within one marketplace only, so
this is an uninstall-and-install, not a rename.

**Coworkers and other surfaces.** On claude.ai and Cowork, plugins come from the account's
marketplaces, and a cross-marketplace dependency counts as met only if the user installed it
from its own marketplace. So the company catalog should be **self-contained**: list the
generic packs it depends on as `git-subdir` entries pointing at `GFMCloud/skill-library`
with a pinned `sha`, exactly how `anthropics/claude-plugins-official` lists 53 third-party
plugins today. The pin bump is your deliberate second look before anything public-sourced
reaches a coworker. Your own work machine installs the generic packs from `skill-library`
directly and leaves the `@<brand>-skills` copies disabled, so nothing is loaded twice.

**Leak control, because the destination is public.** You have said IP is not a concern. The
remaining risk is customer names, 12-digit account IDs, opportunity IDs and internal
hostnames reaching a public repo from a work-laptop edit, and those cannot be rotated. A
secret scan does not catch them. Phase 0 adds a denylist scan (company, customer, people,
account-ID and hostname patterns, list kept in the private company repo, never in the public
one) as CI on skill-library and as a pre-commit hook on the work checkout. Commits from the
work checkout use a per-repo `user.email` set to the gmorris1221 noreply address so the
company mailbox never enters public history.

**Version policy and dependencies.** Claude Code computes a plugin's version from the
manifest first, so an unbumped pack never updates anywhere; the validator already enforces
the bump (F17). Company packs declare `dependencies` on skill-library packs; unconstrained
dependencies resolve without tags, and version ranges need `<plugin>--v<version>` git tags,
which skill-library does not yet publish. Start unconstrained.

### Decision A, worked example: how the work machine knows and enforces the company brand

The home laptop has no brand guideline; every visual deliverable at work must follow the
company's guidelines. Today that is handled by forking the visual packs (`<brand>-decks`,
`<brand>-design` "replaces frontend-design") and baking the brand into the copies. Under this
design the forks go away, so the brand arrives by three mechanisms, each doing one job. All
three live in the company pack `<brand>-core` or the work config repo, so none exists at home.

| Job | Mechanism | Where it lives | Evidence and limits |
|---|---|---|---|
| **Know** that brand applies | One path-scoped rule file, `~/.claude/rules/brand.md`, with `paths: ["**/*.html", "**/*.css", "**/*.pptx", "**/*.docx"]`: every visual deliverable uses `<brand>-core:<brand>-brand-guidelines`, assets enter a project only through `brand-assets.py install`, and brand tokens override `dataviz` palette defaults. | Work config repo | Loads only when a visual file is touched; zero cost otherwise; no change to any generic skill. The shared rules file must drop the home line "`dataviz` ... its colors win" or scope it to home, since at work brand tokens win. |
| **Verify** a deliverable | The existing `brand-compliance-review` skill and `brand-qa` agent, both company-owned, invoked before any publish. | `<brand>-core` / `<brand>-decks` company packs | Already built. They move from the fork into the company pack unchanged. |
| **Enforce** before it leaves | A `PreToolUse` hook shipped by `<brand>-core` in `hooks/hooks.json`, matcher `Bash`, that fires on the publish and conversion commands (`publish-deliverable`, `cd-to-pptx` render, `brand-assets.py install`-less renders) and denies when `brand-assets.py check` fails or a content lint finds a non-brand token in the folder. A second `PreToolUse` on `Write\|Edit` lints hand-written `.html`/`.css` content. | `<brand>-core` company pack | The first draft said `PostToolUse` with a deny. Docs: "The tool has already run by the time the hook fires... To prevent or modify a tool call before it runs, use a PreToolUse hook instead." `PreToolUse` on Write sees `content`; on Edit only the replaced fragment. `.pptx` and `.docx` never pass through Write (python-pptx runs via Bash), so the Bash matcher on the publish and convert commands is the gate that covers every production path, and the work `CLAUDE.md` already names it ("`check` before any render or conversion"). |

**A gap the advisor found:** `brand-assets.py check` today compares bundled asset hashes
to canon only; a missing asset is skipped (`if not target.exists(): continue`) and it never
reads HTML. So "enforce" needs the lint written first. Until the fixture below passes, the
brand rule is "know and verify", not "enforce".

What stays a company skill: skills whose whole body is brand, such as
`<brand>-brand-guidelines`, `<brand>-html-deck`, the branded templates in
`aws-practice-docs`. They declare `dependencies` on the generic packs (`decks`,
`frontend-design`) and call them. What becomes generic: `cd-to-pptx`, `chart-discipline`,
`layout-critique`, `image-taste-frontend`, `redesign-existing-projects`, which differ from
the home copies mainly by brand text and company cross-references. `design-taste-frontend`
differs by about 520 lines and gets its own merge decision in Phase 1.

Proof before relying on it: a fixture that runs the publish command on a folder with no
brand assets and shows the deny, then on a branded folder and shows it pass. A second fixture
writes an unbranded `index.html` and shows the Write lint deny.

### Decision B: hooks get a remote, but safety hooks stay in settings.json

Hook scripts move into a `skill-library` pack so they are versioned and reviewed in one place.
How they are **installed** differs by kind:

- **Blocking safety hooks** (`deny-destructive.py` at home, `partner-write-ask.sh` at work)
  stay wired in `settings.json`. A hook shipped by a plugin is switched off by disabling the
  plugin, by a cloned repo's committed `enabledPlugins: false` (project scope outranks user),
  by `disableAllHooks`, or by a same-named `--plugin-dir` plugin shadowing it silently. A
  `settings.json` hook has none of those off switches. The reviewer's first-draft objection
  here was correct and the earlier idea of the hook denying its own disable was not
  enforceable.
- **Install path:** the daily updater copies hook scripts from the pack it just verified
  into `~/.claude/hooks/`, after its existing hook-surface diff gate, and `settings.json`
  wires them as `python3 ~/.claude/hooks/x.py`. The `~` makes the wiring identical on both
  machines. Scripts are never run from the working checkout, which can be mid-edit or on a
  branch.
- **Advisory hooks** (evidence-guard, session-carryover, pre-compact-state) may instead ship
  in `hooks/hooks.json` once a fixture proves the event fires from a plugin on the installed
  version. Issue 16288 (open since 2026-01-04) reports `SubagentStart` and `SubagentStop`
  not firing from plugin hooks on earlier builds; the report has not been re-tested on
  2.1.300, so this is a fixture question, not a known fact. Either route keeps one editable
  home.

### Decision C: one config repo per machine, never one for both

| Repo | Account | Holds |
|---|---|---|
| `claude-config` (revive the 2026-07-30 repo or start clean) | GFMCloud | Home `~/.claude`: `settings.json`, `CLAUDE.md` machine lines, `rules/` (path-scoped environment rules), plans, lessons. Allowlist `.gitignore` copied from the work repo. |
| `personal-claude-config` | gmorris1221 | Work `~/.claude`, as today, minus the skills, agents and hook scripts that move to packs. |

There is no user-level `settings.local.json`, so `settings.json` cannot be split into shared
and machine halves, and two independent 2026 write-ups abandoned syncing it verbatim
(dotclaude on 2026-09-26: "only conflicts"). The two files legitimately differ: autoMode
grants name GFMCloud repos at home and gmorris1221 at work. Once hook scripts install to
`~/.claude/hooks/`, the remaining absolute paths are `CLAUDE_CODE_PLUGIN_DIRS`,
`additionalDirectories` and autoMode prose; all accept `~`.

MCP server definitions stay per machine in `~/.claude.json` with sign-in state, and OAuth
secrets sit in the keychain. Your hunch is right: definitions are portable, connections are
not. A company pack may ship `.mcp.json` for a server coworkers share, with `${VAR}` for
machine values. Auto memory is machine-local by design and the work gitignore already keeps
`projects/` out of git for customer-name reasons; neither is synced.

**Fresh-machine restore:** clone the config repo to `~/.claude`, clone `skill-library` to
`~/skill-library`, start Claude Code once. Docs: a marketplace declared in settings but
missing on disk is cloned in the background and enabled plugins not cached are downloaded.
The work machine first needs `gh auth login` and `gh auth setup-git` (private marketplace,
credential helper), plus two `env` entries: `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` and
`CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1`. The launchd plist joins the repo.

### Decision D: shared rules in one file, installed, not imported

The general rules both `CLAUDE.md` files restate get one home in `skill-library`. The
updater installs that file into `~/.claude/rules/shared-agreements.md` on each machine, the
same way it installs hook scripts. Each machine's `CLAUDE.md` keeps only machine lines. A
`@~/skill-library/...` import would also work in Claude Code (user-scope imports load without
a dialog), but Cowork on the work machine skips any user-scope import that resolves outside
the session's working directory, so the installed copy is the safer shape. Cowork's own
instruction file under `~/Documents/Claude` stays as it is today.

### Decision E: the account structure (resolved 2026-10-15, no change needed)

GitHub's Terms of Service (effective 2026-04-27, section B.3): "One person or legal entity
may maintain no more than one free Account". Both accounts are on the free plan. The first
draft read that as a conflict, treating both as your personal accounts. You then clarified
that **GFMCloud is held by your company, GFM Cloud, and gmorris1221 is your personal
account**. Those are two holders, a legal entity and a person, with one free account each,
which is what the clause allows. No upgrade and no reorganization is needed. (A reading of
the terms text, not legal advice; GitHub also offers organizations for company use, but the
terms do not require one.)

What still holds from this decision: do not collapse to one identity. A `repo`-scoped
GFMCloud token on the company-managed laptop would cross the boundary your home rules exist
to hold. Two identities, one per machine, with gmorris1221 as a collaborator on
`GFMCloud/skill-library`, is the shape.

### Decision F, later: one weekly maintainer

Its code becomes one pack in `skill-library`; its per-machine `CONFIG.md` and `STATE.md`
live in that machine's config repo. It runs per machine because it reads that machine's
transcripts. Do this after the skills are unified.
