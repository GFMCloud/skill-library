# Project state: home laptop

**The resume point for the home laptop.** Keep it current as you work. The next session on
this machine continues from this file plus the runbooks alone. Machine detection:
`gh api user --jq .login` prints `GFMCloud` here; every entry below was written on that
machine, as that account.

**Status:** in progress, Phase 0 home

**Commit of `GFMCloud/skill-library` this machine was last brought to:** `90711b2` (main,
2026-10-15, before the harness PR)

## Phase tracker

- [ ] Phase 0 home - branch protection, denylist scan, plist, home proofs (`prompts/phase-0-home.md`)
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

## Evidence

<!-- Executed evidence, not checkmarks: the command run and its actual output. Negative
     controls go here verbatim. Format per foundry-core:evidence-report. -->

### Harness scaffold (2026-10-15)

Work copies used for the Phase 0 dry run (`work_copies_for_dry_run` in CONFIG.md): shallow
clones made by the design session on 2026-10-15 under its scratchpad,
`.../1c215210-37ed-4365-bae4-7039cf9aa205/scratchpad/work-repos/{awsp-skill-marketplace,
personal-claude-config,claude-weekly-maintainer}`. They are deleted with that session.

## Anomalies

<!-- date - what/where - why it does not fit - one-line recommendation. Reviewed at the next
     gate, never resolved silently mid-run. -->

## Open items

<!-- Residue: what - why it is still open - who owns it next. -->

## Session log

<!-- One line per session: date - phase worked - outcome / stopping point. -->

- 2026-10-15 - harness scaffold - directory written on branch `migration-2026-10/harness`;
  Phase 0 home steps follow in their own PRs.
