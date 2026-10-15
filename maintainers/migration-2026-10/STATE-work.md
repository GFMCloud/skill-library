# Project state: work laptop

**The resume point for the work laptop.** Keep it current as you work. The next session on
this machine continues from this file plus the runbooks alone. Machine detection:
`gh api user --jq .login` prints `gmorris1221` here; every entry below was written on that
machine, as that account. Redact before pasting: the home directory is written `~`, coworker
logins are counted not listed, and no company, customer or person name appears.

**Status:** Phase -1 survey not started

**Commit of `GFMCloud/skill-library` this machine was last brought to:** none (no clone yet)

## Phase tracker

- [ ] Phase -1 - read-only survey (`prompts/phase-minus-1-work-survey.md`)
- [ ] Phase 0 work - clone, marketplace, packs, env, updater (`prompts/phase-0-work.md`); needs Phase 0 home complete in `STATE-home.md`
- [ ] Phase 1 Gate A - rulings recorded (`prompts/phase-1-gate-a.md`); may run on either machine
- [ ] Phase 1 work - work-only generic skills in, packs dropped when empty (`prompts/phase-1-work.md`); needs Phase 1 home complete
- [ ] Phase 2 work half - hooks and agents (`prompts/phase-2.md`)
- [ ] Phase 3 work half - config repo, rules files, shared rules, Gate B (`prompts/phase-3.md`)

## Phase -1 survey

<!-- One subsection per survey row, in runbook order: the command as run and its output,
     redacted. The runbook says what each row's expected output looks like and what finding
     would change the plan. -->

## Decision log

<!-- Append: date - decision - one-line rationale. Never rewrite old entries. Gate rulings
     are recorded in gate-a-direction-table.md and summarised here. -->

## Evidence

<!-- Executed evidence, not checkmarks: the command run and its actual output. Negative
     controls (the pre-commit hook refusing a planted fixture, the pack-drop rollback) go
     here verbatim. -->

## Anomalies

<!-- date - what/where - why it does not fit - one-line recommendation. Reviewed at the next
     gate, never resolved silently mid-run. -->

## Open items

<!-- Residue: what - why it is still open - who owns it next. -->

- Phase -1 has not run. Owner: the first session on the work laptop after the harness PR is
  merged to `main`.

## Session log

<!-- One line per session: date - phase worked - outcome / stopping point. -->
