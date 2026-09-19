# Skill Organization Project

A phased migration project that brings a Claude Code setup into compliance with a
single-source skill-management model: one canonical GitHub repo, structured as a
plugin marketplace, consumed as installed plugins on every machine.

This directory is the **project harness**, not the skill library itself. It holds the
target design, the phase-by-phase runbook, and the state tracker. The actual skill
library is a separate repo created in Phase 0 (location set in [CONFIG.md](CONFIG.md)).

## Why

Skill drift comes from the consumption layer: copies fork silently the first time
someone edits one in place, and symlinks track whatever branch a checkout happens to
be on. The fix is structural, not disciplinary — make the canonical repo the only
editable surface and let the plugin system provide namespacing, version pinning, and
a single update verb. The full rationale and target design: [docs/end-state.md](docs/end-state.md).

## How to run

1. Fill in [CONFIG.md](CONFIG.md) (target repo org/name, local clone path).
2. Open a new Claude Code session **in this directory** and type:

   ```
   /phase
   ```

   `/phase` runs **continuously through all remaining phases**, resuming from
   wherever [STATE.md](STATE.md) says it left off. It comes back to you at exactly
   two gates — Gate A: one batch ruling on the proposed disposition table; Gate B:
   confirming the final deletion list — plus genuine blockers it can't safely defer.
   Standing authorizations in CONFIG.md cover everything else (repo creation,
   pushes, plugin installs). `/phase 3` runs a single phase if you ever want
   stepwise control.

## Phases

| # | Phase | Nature | Output |
|---|-------|--------|--------|
| 0 | Repo skeleton | Greenfield build | Empty-but-valid skill-library repo, validator proven |
| 1 | Inventory | **Strictly read-only** | `MIGRATION.md` in the library repo — one row per skill, with a proposed disposition |
| 2 | Disposition | **Gate A** — one batch ruling | User ratifies/overrides the proposed table in a single pass |
| 3 | Migrate | Move + normalize | Skills in their plugins, validator green, PR per plugin |
| 4 | Wire consumption | Config changes | Marketplace registered, plugins installed, CLAUDE.md updated |
| 5 | Verify, then delete | **Gate B** — deletion confirm | Verification checklist passed; superseded copies removed |

## Directory map

```text
skill-organization/
├── README.md                  ← you are here
├── .claude/skills/phase/      # the /phase command — entry point for every session
├── CLAUDE.md                  # session orientation + hard guardrails
├── CONFIG.md                  # user-filled parameters (repo name, paths)
├── STATE.md                   # phase tracker + decision log — the resume point
├── docs/
│   ├── end-state.md           # the target design: what "compliant" means
│   ├── authoring-standard.md  # the SKILL.md contract
│   └── validator-spec.md      # what validate-skills.sh must check
├── prompts/                   # per-phase runbooks, loaded by /phase
│   ├── phase-0-skeleton.md
│   ├── phase-1-inventory.md
│   ├── phase-2-disposition.md
│   ├── phase-3-migrate.md
│   ├── phase-4-consumption.md
│   └── phase-5-verify.md
└── templates/
    ├── SKILL.template.md      # frontmatter contract as a fill-in template
    ├── MIGRATION.template.md  # inventory table format for Phase 1
    ├── validate-skills.sh     # reference validator → copy into library repo
    └── validate.yml           # GitHub Actions workflow → copy into library repo
```

## Ground rules (enforced via CLAUDE.md)

- Nothing is deleted until Phase 5 verification passes; before that, superseded
  locations are renamed with a `.migrated-off` suffix.
- Migration **moves** skills, never copies them.
- Plugin caches are never edited.
- Phase 1 is read-only, run in plan mode.
