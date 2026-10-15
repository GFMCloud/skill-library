# Two-laptop skill sync: migration harness (2026-10)

This directory is the harness for making `GFMCloud/skill-library` the one editable home of
every generic skill on both of Graham's laptops: the home laptop (GitHub account GFMCloud) and
the company-managed work laptop (GitHub account gmorris1221). It is scaffolded from
`long-projects:phased-harness` and follows the shape of the repo's earlier migration
(`maintainers/MIGRATION.md`, `maintainers/migration/harness/`).

The design this harness executes is the 2026-10-15 proposal "One toolkit, two accounts". Its
decisions are carried verbatim in [CONFIG.md](CONFIG.md); its migration path and hardening
checks are carried by the runbooks under `prompts/`. The design document itself is not in this
repo, because it names the company, its packs and its people, and this repo is public.

## How to run it

There is no `/phase` dispatch skill here: `maintainers/migration/harness/.claude/skills/phase`
already owns that name in this repo and names are unique. Dispatch by hand:

1. Open a session in `~/skill-library`.
2. Read the state file for the machine you are on: [STATE-home.md](STATE-home.md) on the home
   laptop, [STATE-work.md](STATE-work.md) on the work laptop. It says which phase is next and
   which commit that machine was last brought to.
3. Read [CONFIG.md](CONFIG.md). Stop on any `TBD`.
4. Run the next runbook from the table below. Every runbook starts with a machine detection
   step that stops the run on the wrong laptop.
5. Record executed evidence (command and output) in that machine's state file as you go, and
   the commit SHA the machine was brought to when the phase ends.

[CLAUDE.md](CLAUDE.md) carries the guardrails; [docs/end-state.md](docs/end-state.md) is the
tiebreaker for any ambiguity.

## Phases

| Phase | Runbook | Machine | Nature |
|---|---|---|---|
| -1 | [prompts/phase-minus-1-work-survey.md](prompts/phase-minus-1-work-survey.md) | work | read-only survey, output pasted into STATE-work.md |
| 0 | [prompts/phase-0-home.md](prompts/phase-0-home.md) | home | greenfield: branch protection, denylist scan, plist, home proofs |
| 0 | [prompts/phase-0-work.md](prompts/phase-0-work.md) | work | greenfield: clone, marketplace, packs, env, updater; disables nothing |
| 1 | [prompts/phase-1-gate-a.md](prompts/phase-1-gate-a.md) | either | decision gate: the direction table in [gate-a-direction-table.md](gate-a-direction-table.md) |
| 1 | [prompts/phase-1-home.md](prompts/phase-1-home.md) | home | execution: three-way merges into skill-library |
| 1 | [prompts/phase-1-work.md](prompts/phase-1-work.md) | work | execution: work-only generic skills in, packs dropped when empty |
| 2 | [prompts/phase-2.md](prompts/phase-2.md) | both | execution: hooks and agents |
| 3 | [prompts/phase-3.md](prompts/phase-3.md) | both | execution, verification, Gate B |

Phase 4 of the design (one weekly maintainer) is a successor project, not a phase here; Phase 3
names it as the owner of that residue.

## Redaction rule for this directory

This directory lives in a public repository. Nothing in it names the company, its brand, its
customers, its people, its account IDs, its internal hostnames, or the work laptop's user
name. Company pack names are written `<brand>-decks`, `<brand>-design`, `<brand>-core`; the
work laptop's home directory is written `~`. The denylist scan (`scripts/denylist-scan.sh`,
patterns outside the repo) enforces this on every PR once Phase 0 lands.
