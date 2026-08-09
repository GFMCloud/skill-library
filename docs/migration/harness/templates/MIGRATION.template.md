# Skill migration inventory

Produced by Phase 1 (read-only sweep) with a **Proposed** disposition per row; the
**Ruling** column is filled at Gate A (Phase 2) from the user's batch ruling —
Phase 3 executes only ruled rows. Checked off row-by-row during Phase 3. Kept
permanently as the historical record of where every skill came from.

Disposition values: `library:<plugin>` | `project` | `deprecate` | `archive`
Drifted rows additionally carry `winner: project|library|merge`.

## Inventory

| ✓ | Skill | Current path | Consumed via | Frontmatter | Lines | Drift | Proposed | Ruling |
|---|-------|--------------|--------------|-------------|-------|-------|----------|--------|
| ☐ | example-skill | ~/somewhere/example-skill/SKILL.md | orphan copy | name+desc only | 210 | — | library:core — reusable, proven | |
| ☐ | drifted-skill | projA/.claude/skills/drifted-skill | project copy | full | 340 | see D1 | library:core, winner: project | |

## Drift details

One entry per drifted skill: what actually differs between copies (sections, rules,
frontmatter — not "files differ"), plus a recommendation and one line of reasoning.

- **D1 — drifted-skill**: project copy adds a validation section (~40 lines) absent
  from the marketplace copy; marketplace copy has newer frontmatter.
  *Recommendation: winner: project (behavior superset), re-add marketplace frontmatter.*

## Not migrated / anomalies

Anything skill-shaped that didn't fit the table (archives marked do-not-edit,
non-Claude skill systems, zips), with path and one-line note.
