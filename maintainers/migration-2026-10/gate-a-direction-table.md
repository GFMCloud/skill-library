# Gate A: direction per shared skill

The 41 skills that exist under the same name in `GFMCloud/skill-library` and on the work side
(the company marketplace plus the work config repo's `skills/`), measured by the design
session's `compare-skills.sh` on 2026-10-15: 74 skills at home, 101 at work, 41 shared, 0 of
the 41 byte-identical. This file is the one place the list and the count live.

**Columns.** `library pack` and `work pack` are where each copy lives today (company brand
packs redacted as `<brand>-*`). `base commit` is the skill-library commit the work copy's
`source:` tag records (`ecbab91` = `base_commit` in CONFIG.md), or `none`. `direction` is the
**proposal**, one of `library wins`, `work wins`, `merge`; `merge` means a three-way merge
from the base where there is one and a two-way read where there is none. `note` holds what
the proposal rests on, and is extended by the Phase 1 dry runs (hunks resolved, conflicts).
`ruling` is Graham's, filled at Gate A in one batch; a blank ruling after Gate A means "as
proposed" only if the batch said so. Overridden rows reassign their side effects in the
decision log.

Line counts are the two `SKILL.md` bodies on 2026-10-15 (home / work).

| # | skill | library pack | work pack | base commit | direction | note | ruling |
|---|---|---|---|---|---|---|---|
| 1 | bounded-loop | foundry-core | workbench | ecbab91 | merge | 119 / 147 | |
| 2 | capability-preflight | turn-reduction | workbench | none | merge | work tag: "kept over personal rebase after bake-off 2026-10-02"; home since gained 1.2.0 (negative control first, 2026-10-11). Two-way read, work body as the base text. 180 / 153 | |
| 3 | cd-to-pptx | decks | `<brand>`-decks | ecbab91 | merge | work tag: "merged with ecbab91 decks/cd-to-pptx 2026-10-02"; brand text out to `rules/brand.md`. 129 / 171 | |
| 4 | chart-discipline | decks | `<brand>`-decks | ecbab91 | merge | brand tokens out to `rules/brand.md`. 121 / 123 | |
| 5 | council | long-projects | verification | ecbab91 | merge | 104 / 108 | |
| 6 | deck-scaffolding-builder | decks | `<brand>`-decks | ecbab91 | merge | work tag: "rules ported from ecbab91". 123 / 132 | |
| 7 | design-taste-frontend | frontend-design | `<brand>`-design | none | separate decision | work tag: "kept over personal rebase after bake-off 2026-10-02; absorbs minimalist-ui". About 520 lines apart per the design. Options: work wins and minimalist-ui stays absorbed; library wins; split. 332 / 439 | |
| 8 | eval-harness | foundry-core | verification | ecbab91 | merge | 143 / 137 | |
| 9 | fact-currency-check | verification-kit | verification | ecbab91 | merge | 68 / 78 | |
| 10 | folder-to-repo | voice-and-editing | workbench | none | merge | work tag: "existing work skill, reconciled 2026-10-02". Two-way read. 191 / 228 | |
| 11 | goal-spec | foundry-core | workbench | ecbab91 | merge | 124 / 112 | |
| 12 | graham-voice | voice-and-editing | `<brand>`-core | ecbab91 | merge | work tag: "work body; rule r04 ported from ecbab91". Company voice context out to a work rule file. 275 / 285 | |
| 13 | handoff | long-projects | workbench | ecbab91 | merge | home 0.6.5 / work 0.7.0. 337 / 306 | |
| 14 | humanizer | voice-and-editing | `<brand>`-core | ecbab91 | merge | 397 / 405 | |
| 15 | identity-resolution | data-wrangler | workbench | ecbab91 | merge | home 1.0.1 / work 1.0.0. 106 / 121 | |
| 16 | image-taste-frontend | frontend-design | `<brand>`-design | ecbab91 | merge | brand text out to `rules/brand.md`. 232 / 261 | |
| 17 | jev | agent-tooling | workbench | ecbab91 | merge | 179 / 190 | |
| 18 | layout-critique | decks | `<brand>`-decks | ecbab91 | merge | 79 / 80 | |
| 19 | model-effort-advisor | agent-tooling | workbench | ecbab91 | merge | work copy references `<brand>-core:background-task-triggers`; that line out to a work rule file. 108 / 109 | |
| 20 | orch-pipeline | long-projects | workbench | ecbab91 | merge | 124 / 124 | |
| 21 | orch-review | long-projects | workbench | ecbab91 | merge | 127 / 105 | |
| 22 | output-lint | turn-reduction | verification | ecbab91 | merge | Phase 0 dry run row. 114 / 126 | |
| 23 | phased-harness | long-projects | workbench | ecbab91 | merge | work tag: "work pack; rules ported from ecbab91". 295 / 345 | |
| 24 | pipeline-foundry | project-starters | workbench | ecbab91 | merge | 386 / 285 | |
| 25 | plan-gate | turn-reduction | workbench | ecbab91 | merge | the design's sample: work added Partner Central and CloudFront context (out to `rules/partner-central.md`), removed homelab paragraphs (out to `rules/homelab.md`), home added "Design and pipeline proposals" 2026-10-10. Phase 0 dry run row. 141 / 159 | |
| 26 | project-kb-builder | project-starters | workbench | ecbab91 | merge | work names a company house convention; out to a work rule file. 212 / 215 | |
| 27 | project-setup-wizard | project-starters | workbench | ecbab91 | merge | 238 / 240 | |
| 28 | proof-of-work | foundry-core | workbench | ecbab91 | merge | home 1.6.0 / work 1.1.0. Phase 0 dry run row. 157 / 230 | |
| 29 | redesign-existing-projects | frontend-design | `<brand>`-design | none | merge | both derive from leonxlnx/taste-skill@ccbc156; work tag names only the upstream. Two-way read with the upstream as base. 184 / 188 | |
| 30 | retro | long-projects | workbench | none | library wins | work copy has no `source:` tag and no version; confirm nothing work-only in its 93 lines before ruling. 173 / 93 | |
| 31 | sales-lens-review | decks | `<brand>`-decks | ecbab91 | merge | largest divergence among the tagged rows. 241 / 110 | |
| 32 | santa-method | long-projects | verification | ecbab91 | merge | 119 / 121 | |
| 33 | security-audit | verification-kit | security-scan | ecbab91 | merge | vendored upstream at home; work adds a boundary paragraph naming the company `security-scan` skill (stays at work). 207 / 216 | |
| 34 | skill-discovery | voice-and-editing | workbench | ecbab91 | merge | 303 / 303 | |
| 35 | source-intake | voice-and-editing | workbench | ecbab91 | merge | 226 / 209 | |
| 36 | spec-artifact-diff | consistency-checker | verification | ecbab91 | merge | 162 / 124 | |
| 37 | standing-authorization | turn-reduction | workbench | ecbab91 | merge | home 1.2.0 / work 1.1.0. 220 / 152 | |
| 38 | sweep-harness | long-projects | workbench | ecbab91 | merge | 134 / 137 | |
| 39 | systems-design | project-starters | workbench | ecbab91 | merge | 268 / 281 | |
| 40 | toolkit-review | voice-and-editing | workbench | ecbab91 | merge | 188 / 188 | |
| 41 | x-read | voice-and-editing | workbench | ecbab91 | merge | 75 / 92 | |

Rows with `base commit` = `ecbab91`: 36 (rows 1, 3 to 6, 8, 9, 11 to 28, 31 to 41). Rows
without: 5 (rows 2, 7, 10, 29, 30).

## Other Gate A rows

These are decisions only Graham can make; each is presented in the same batch as the table.

| # | Decision | Proposal | Reasoning |
|---|---|---|---|
| G1 | `home_config_repo`: reset the 2026-07-29 `GFMCloud/claude-config` snapshot, or start clean | reset it (force-push a new root is a rewrite of a one-commit repo nobody consumes) | keeps the name the design and the archive review both use |
| G2 | Which skill-library pack holds the hook scripts (Phase 2) | `agent-tooling` | it already holds the machine-facing tooling and is installed on both |
| G3 | Where the shared rules file lives in skill-library (Phase 3) | `rules/shared-agreements.md` at the repo root | it is not a skill and no pack should own it |
| G4 | Whether the `git-subdir` catalog entries are needed on day one | depends on the Phase -1 Cowork row | needed on day one only if coworkers or Cowork load generic packs today |
| G5 | The coworker notice text before the first pack drop | drafted at Gate A from the Phase -1 collaborator count | `forceRemoveDeletedPlugins` removes a pack at their next session start |
| G6 | Resume the weekly maintainer after Phase 1 work, or keep it paused until Phase 3 | resume after Phase 1 work | it edits skills, and after Phase 1 the only skills it can edit live in skill-library behind CI |
