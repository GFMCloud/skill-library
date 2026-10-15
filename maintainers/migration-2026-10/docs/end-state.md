# End state: what "done" means

This document is the contract the migration works toward. **When any instruction in
`CLAUDE.md` or a runbook is ambiguous, this document is the tiebreaker.**

## The invariant

> Every generic skill, agent, hook script and shared rule has exactly one editable home,
> `GFMCloud/skill-library`, installed on both laptops from the same marketplace; environment
> text lives only in that machine's config repo under `~/.claude/rules/`; company-only
> material lives only in the private company marketplace; and nothing that identifies the
> company, its customers or its people exists in the public repo.

Everything below explains or enforces that sentence. If a rule below conflicts with it, the
invariant wins.

## The model in one paragraph

Git is the sync. Both laptops hold a writable checkout at `~/skill-library` and install the
same 12 packs from the `skill-library` marketplace; the daily updater brings each machine to
some commit of `main`, and the installed pack versions say which. A generic edit on either
machine is one PR to skill-library, authored by that machine's GitHub account (GFMCloud at
home, gmorris1221 at work), merged after CI (validator plus denylist scan) and a fresh review.
Environment text (homelab at home; brand and Partner Central at work) lives in path-scoped
rule files in each machine's config repo, never in a generic skill body. Company-only packs
stay in the private company marketplace, which lists the generic packs it depends on by
`git-subdir` entries pinned to a skill-library commit, for coworkers and for Cowork and
claude.ai. Blocking safety hooks stay wired in each machine's `settings.json`; their scripts
are versioned in a skill-library pack and installed into `~/.claude/hooks/` by the updater
after its hook-surface gate. The 41 skills that today exist as two diverged copies exist once.

## Why this shape and not the alternatives

- Keep porting by hand at a pinned commit (today): rejected, 41 forks, 0 identical, each
  round harder than the last.
- Git subtree or submodule of skill-library inside the company marketplace: rejected, Claude
  Code installs copied plugin caches, so a `git-subdir` catalog entry gives the same result
  with no second copy to merge.
- One private monorepo with a generated public mirror: rejected, a generated mirror drifts
  and company material lands in a personal account.
- Install the company marketplace at home: rejected, no use at home, and every loaded pack
  costs tokens per session.
- One `~/.claude` dotfiles repo for both machines: rejected, `settings.json` cannot be split
  at user scope, MCP and memory are machine-local, the machines trust different accounts.
- `~/skill-library` as a local-directory marketplace: rejected, it runs the working tree
  mid-edit and removes the hook-surface refusal.
- Plugin-shipped safety hooks: rejected, switched off by plugin disable, project-scope
  `enabledPlugins`, `disableAllHooks` or `--plugin-dir` shadowing.

## Target layout

```text
GFMCloud/skill-library (public)        every generic skill, agent, hook script, shared rules
  plugins/<12 packs>/                   installed on both laptops from the same marketplace
  scripts/denylist-scan.sh              CI gate; patterns live outside the repo
  scripts/com.gfm.skill-library-plugin-update.plist   the daily updater's launchd job
gmorris1221/<company marketplace> (private, work only)
  plugins/<company-only packs>/         brand, partner ops, practice docs, personas, boards
  .claude-plugin/marketplace.json       plus git-subdir entries for the generic packs, pinned
gmorris1221/personal-claude-config     the work ~/.claude: settings.json, CLAUDE.md machine
  rules/brand.md, rules/partner-central.md   lines, path-scoped rule files, plans, lessons
GFMCloud/claude-config                 the home ~/.claude: same shape
  rules/homelab.md
~/.claude/hooks/*.py                   installed by the updater on both machines, wired by ~ path
~/.claude/rules/shared-agreements.md   installed by the updater on both machines
```

## Rules that follow from the invariant

| Situation | Correct home |
|---|---|
| A skill useful on both machines | skill-library, the pack it belongs to |
| A skill whose whole body is company brand or company process | the company marketplace |
| Text that only applies on one machine (homelab, Partner Central, brand) | that machine's config repo, `~/.claude/rules/<topic>.md` with `paths:` frontmatter |
| A blocking safety hook | script in a skill-library pack; wiring in that machine's `settings.json` |
| An advisory hook | plugin `hooks/hooks.json` only once a fixture shows the event fires from a plugin |
| A general working agreement both CLAUDE.md files restate | `rules/shared-agreements.md` in skill-library, installed by the updater |
| Machine-specific CLAUDE.md lines | that machine's config repo |
| The denylist of company and customer patterns | the work config repo and `~/.claude/denylist.txt`; never skill-library |

Never both: a skill name exists in skill-library or in the company marketplace, not in both.

## Enforcement

Mechanical: `scripts/validate-skills.sh` (CI, required status check on `main`),
`scripts/denylist-scan.sh` (CI with patterns from a repository secret; pre-commit on the work
checkout), the updater's hook-surface diff gate, the version comparison command in
`CONFIG.md`, and `compare-skills.sh` run against both trees (the shared-name count must reach
zero). Discipline: the redaction rule in `CLAUDE.md`, the fresh review before each merge, and
the per-pack gate before any drop.

## Definition of done (final-phase gate)

Route these checks to the installed agents: the fresh-context pass goes to
`verification-kit:pre-delivery-verifier`, and the document-against-artifact checks go to
`consistency-checker:cross-document-checker`.

The final phase re-verifies each of these from scratch, in a fresh context:

1. The version comparison command in `CONFIG.md` prints identical output on both laptops.
2. The shared-name count between skill-library and the company marketplace is zero, with
   the company catalog's `git-subdir` entries resolving to the pinned skill-library commit.
3. `find ~/skill-library ~/.claude -name '*.superseded'` is empty on both machines after
   Gate B, and before Gate B every item on the deletion list is on that output.
4. The denylist scan has failed a planted fixture and passed the clean tree, on CI and on the
   work pre-commit hook, with the output recorded.
5. `shasum ~/.claude/hooks/*.py ~/.claude/rules/shared-agreements.md` is identical on both
   machines, and every event in each live `settings.json` either fired from a plugin in its
   fixture or stayed wired in `settings.json`.
6. The Gate B deletions are done, the only irreversible step in the project.
7. Residue named and owned: every gap found and not closed, every deferred check, everything
   scoped out, has a destination written in the state files (an owned open item, the named
   successor project for the weekly maintainer, or dropped with the reason).
