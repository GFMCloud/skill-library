# Skill migration inventory

Produced by Phase 1 (read-only sweep, 2026-08-09) with a **Proposed** disposition per
row; the **Ruling** column is filled at Gate A (Phase 2) from the user's batch ruling —
Phase 3 executes only ruled rows. Checked off row-by-row during Phase 3. Kept
permanently as the historical record of where every skill came from.

Disposition values: `library:<plugin>` | `project` | `deprecate` | `archive`
Drifted rows additionally carry `winner: project|library|merge`.

Sweep sources: three read-only subagent reports (`~/.claude` tree; project repos;
home-wide stray sweep), merged and drift-diffed by the orchestrator. Raw reports
preserved in the migration harness session scratchpad.

## Proposed plugin list

| Plugin | Contents | Origin |
|---|---|---|
| `foundry-core` | evidence-report, proof-of-work | gfm-foundry (installed, in daily use) |
| `turn-reduction` | capability-preflight, output-lint, standing-authorization | gfm-foundry (installed) |
| `data-wrangler` | identity-resolution + agent data-pipeline-owner | gfm-foundry (installed) |
| `verification-kit` | fact-currency-check + agent pre-delivery-verifier | gfm-foundry (not installed) |
| `consistency-checker` | spec-artifact-diff + agent cross-document-checker | gfm-foundry (not installed) |
| `deploy-ops` | deploy-verify-fix + agent deploy-loop-owner | gfm-foundry (not installed) |
| `decks` | deck-build (4) + deck-critique (2) merged: cd-to-pptx, chart-discipline, deck-scaffolding-builder, html-diagram, layout-critique, sales-lens-review | gfmcloud-skills |
| `frontend-design` | design-taste-frontend, image-taste-frontend, minimalist-ui, redesign-existing-projects, frontend-design (from SCL v2 repo), emil-design-eng (from Documents archive) | gfmcloud-skills + strays |
| ~~`scl`~~ | ~~scl-keeper-logic-validator, scl-module-deploy-checklist, scl-session-startup-enforcer~~ | **Dropped at Gate A** — user ruled SCL skills stay project-local in sloshball-champions-league-v2 |
| `workbench` | adhd, capability-index, fable-project-review, folder-to-repo, handoff, llama-offload, model-effort-advisor, project-kb-builder, project-setup-wizard, skill-discovery, supahcode-review, systems-design, graham-voice | gfmcloud-skills (voice folded in) |
| `_incubator` | pipeline-foundry, devshell-init, new-project | unproven/unlisted/orphan |

11 plugins exceeds the end-state's ~3–7 guideline. Reasoning: groupings follow proven
install units — the user already selectively installs 3 of gfm-foundry's 6 plugins,
which demonstrates finer granularity is load-bearing. Only merge performed: deck-build
+ deck-critique → `decks` (always enabled together); voice folded into `workbench`.

## Inventory — `library:*` rows (move into skill-library)

Sources: `foundry` = `~/gfm-foundry` (canonical clone; byte-identical duplicate at
`~/work/GitHub/gfm-foundry`); `gfmcloud` = `~/gfmcloud-skills-marketplace` (source repo;
registered marketplace clone at `~/.claude/plugins/marketplaces/gfmcloud-skills` is
same commit `0b0a897`). FM = frontmatter completeness ("n+d" = name + desc ≥40 only).

| ✓ | Skill | Current path | Consumed via | FM | Lines | Drift | Proposed | Ruling |
|---|-------|--------------|--------------|----|-------|-------|----------|--------|
| ☑ | evidence-report | foundry/plugins/foundry-core/skills/… | installed plugin | n+d | 66 | — | library:foundry-core — installed, in daily use | as proposed |
| ☑ | proof-of-work | foundry/plugins/foundry-core/skills/… | installed plugin | n+d | 68 | — | library:foundry-core | as proposed |
| ☑ | capability-preflight | foundry/plugins/turn-reduction/skills/… | installed plugin | n+d | 130 | — | library:turn-reduction | as proposed |
| ☑ | output-lint | foundry/plugins/turn-reduction/skills/… | installed plugin | n+d | 86 | — | library:turn-reduction | as proposed |
| ☑ | standing-authorization | foundry/plugins/turn-reduction/skills/… | installed plugin | n+d | 104 | — | library:turn-reduction | as proposed |
| ☑ | identity-resolution | foundry/plugins/data-wrangler/skills/… | installed plugin | n+d | 73 | — | library:data-wrangler | as proposed |
| ☑ | data-pipeline-owner (agent) | foundry/plugins/data-wrangler/agents/… | installed plugin | n+d | 93 | — | library:data-wrangler — moves with its plugin | as proposed |
| ☑ | fact-currency-check | foundry/plugins/verification-kit/skills/… | marketplace clone only | n+d | 62 | — | library:verification-kit | as proposed |
| ☑ | pre-delivery-verifier (agent) | foundry/plugins/verification-kit/agents/… | marketplace clone only | n+d | — | — | library:verification-kit | as proposed |
| ☑ | spec-artifact-diff | foundry/plugins/consistency-checker/skills/… | marketplace clone only | n+d | 156 | — | library:consistency-checker | as proposed |
| ☑ | cross-document-checker (agent) | foundry/plugins/consistency-checker/agents/… | marketplace clone only | n+d | — | — | library:consistency-checker | as proposed |
| ☑ | deploy-verify-fix | foundry/plugins/deploy-ops/skills/… | marketplace clone only | n+d | 87 | — | library:deploy-ops | as proposed |
| ☑ | deploy-loop-owner (agent) | foundry/plugins/deploy-ops/agents/… | marketplace clone only | n+d | — | — | library:deploy-ops | as proposed |
| ☑ | pipeline-foundry | foundry/plugins/pipeline-foundry/skills/… | orphan (unlisted in marketplace.json — A1) | n+d | 374 | — | library:_incubator — content complete but never installable, unproven | as proposed |
| ☑ | cd-to-pptx | gfmcloud/plugins/deck-build/skills/… | marketplace clone (never installed) | n+d | 127 | — | library:decks | as proposed |
| ☑ | chart-discipline | gfmcloud/plugins/deck-build/skills/… | marketplace clone (never installed) | n+d | 102 | — | library:decks | as proposed |
| ☑ | deck-scaffolding-builder | gfmcloud/plugins/deck-build/skills/… | marketplace clone (never installed) | n+d | 121 | — | library:decks | as proposed |
| ☑ | html-diagram | gfmcloud/plugins/deck-build/skills/… | marketplace clone (never installed) | n+d | 99 | — | library:decks | as proposed |
| ☑ | layout-critique | gfmcloud/plugins/deck-critique/skills/… | marketplace clone (never installed) | n+d | 65 | — | library:decks | as proposed |
| ☑ | sales-lens-review | gfmcloud/plugins/deck-critique/skills/… | marketplace clone (never installed) | n+d | 239 | — | library:decks | as proposed |
| ☑ | design-taste-frontend | gfmcloud/plugins/frontend-design/skills/… | marketplace clone (never installed) | n+d, **broken YAML** (A2) | 241 | — | library:frontend-design — fix YAML quoting in normalization | as proposed |
| ☑ | image-taste-frontend | gfmcloud/plugins/frontend-design/skills/… | marketplace clone (never installed) | n+d, **broken YAML** (A2) | 199 | — | library:frontend-design | as proposed |
| ☑ | minimalist-ui | gfmcloud/plugins/frontend-design/skills/… | marketplace clone (never installed) | n+d, **broken YAML** (A2) | 91 | — | library:frontend-design | as proposed |
| ☑ | redesign-existing-projects | gfmcloud/plugins/frontend-design/skills/… | marketplace clone (never installed) | n+d | 182 | — | library:frontend-design | as proposed |
| ☑ | frontend-design (skill) | sloshball-champions-league-v2/.claude/skills/frontend-design | project copy | n+d + license | 50 | — | library:frontend-design — generic (not SCL-specific); carries LICENSE.txt with it | as proposed |
| ☑ | emil-design-eng | Documents/…/SCL-MIGRATED-2026-08-04-DO-NOT-EDIT/.claude/skills/… | orphan in frozen archive | n+d | 675 | — | library:frontend-design — reusable UI-review guidance stranded in a do-not-edit folder (A4); body >500 → split to references/ | as proposed |
| ☑ | scl-keeper-logic-validator | gfmcloud/plugins/scl/skills/… (+3 stale copies) | marketplace clone (never installed) | n+d | 199 | D1 | library:scl, winner: library (marketplace copy) | **OVERRIDDEN: project** — SCL stays project-local in sloshball-champions-league-v2; marketplace copy retires with repo (recoverable on GitHub) |
| ☑ | scl-session-startup-enforcer | gfmcloud/plugins/scl/skills/… (+2 stale copies) | marketplace clone (never installed) | n+d | 166 | D2 | library:scl, winner: library | **OVERRIDDEN: project** — same ruling |
| ☑ | scl-module-deploy-checklist | gfmcloud/plugins/scl/skills/… (+2 stale copies) | marketplace clone (never installed) | n+d | 219 | D3 | library:scl, winner: library (structural superset) | **OVERRIDDEN: project** — same ruling; note the references/ refactor stays behind with the retired repo |
| ☑ | graham-voice | gfmcloud/plugins/voice/skills/… | marketplace clone (never installed) | n+d | 269 | zip echo (D8) | library:workbench — voice folded in; alt: keep 1-skill voice plugin | as proposed |
| ☑ | adhd | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d | 126 | — | library:workbench | as proposed |
| ☑ | capability-index | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d, **broken YAML** (A2) | 57 | — | library:workbench — premise mismatch noted (A5) | as proposed |
| ☑ | fable-project-review | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d | 94 | zip echo (D8) | library:workbench | as proposed |
| ☑ | folder-to-repo | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d | 189 | — | library:workbench | as proposed |
| ☑ | handoff | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d, **broken YAML** (A2) | 234 | zip echo (D8) | library:workbench | as proposed |
| ☑ | llama-offload | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d | 85 | — | library:workbench | as proposed |
| ☑ | model-effort-advisor | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d | 106 | — | library:workbench | as proposed |
| ☑ | project-kb-builder | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d | 210 | — | library:workbench | as proposed |
| ☑ | project-setup-wizard | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d | 236 | — | library:workbench | as proposed |
| ☑ | skill-discovery | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d | 382 | — | library:workbench | as proposed |
| ☑ | supahcode-review | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d | 170 | — | library:workbench | as proposed |
| ☑ | systems-design | gfmcloud/plugins/workbench/skills/… | marketplace clone (never installed) | n+d | 266 | — | library:workbench — adjacent systems-design.skill zip is a build artifact, superseded | as proposed |
| ☑ | new-project | ~/work/new-project.skill (packaged zip, no source) | orphan | n+d (inside zip) | ~200 | — | library:_incubator — unpack; real skill (scaffolder + 4 archetype refs), zip is its only home | as proposed |
| ☑ | devshell-init | ~/src/mac-setup/.claude/skills/devshell-init | project copy | n+d | 60 | — | library:_incubator — promote: targets arbitrary repos, not mac-setup itself; alt: project | as proposed |

## Inventory — `project` rows (stay where they are)

| ✓ | Skill | Current path | Kind | FM | Lines | Drift | Proposed | Ruling |
|---|-------|--------------|------|----|-------|-------|----------|--------|
| ☑ | phase | ref/skill-organization/.claude/skills/phase | skill | full | 70 | D5 | project — the migration harness itself | as proposed |
| ☑ | setup-next | src/mac-setup/.claude/skills/setup-next | skill | n+d | 55 | — | project — bound to mac-setup runbook | as proposed |
| ☑ | setup-status | src/mac-setup/.claude/skills/setup-status | skill | n+d | 28 | — | project — bound to mac-setup runbook | as proposed |
| ☑ | seam-advisor | work/scoreboard-ipad/.claude/agents/ | agent | n+d | 20 | — | project — scoreboard-specific | as proposed |
| ☑ | contract-advisor | work/scoreboard-ipad/.claude/agents/ | agent | n+d | 26 | — | project — scoreboard-specific | as proposed |
| ☑ | load-advisor | work/scoreboard-ipad/.claude/agents/ | agent | n+d | 24 | — | project — scoreboard-specific | as proposed |
| ☑ | panel-advisor | work/scoreboard-ipad/.claude/agents/ | agent | n+d | 26 | — | project — scoreboard-specific | as proposed |
| ☑ | content-builder | work/GitHub/the-michiana-trail/.claude/agents/ | agent | n+d | 28 | D4 | project, winner: work/GitHub clone (superset) | as proposed |
| ☑ | fable-advisor | work/GitHub/the-michiana-trail/.claude/agents/ | agent | n+d | 6 | D6 (identical) | project | as proposed |
| ☑ | project-constants | work/GitHub/sloshball-ff/.claude/skills/ | skill | n+d | 1188 | — | project — sloshball-ff-specific; oversize noted (A7), cleanup belongs to that project | as proposed |
| ☑ | buzz-cli | ~/.buzz/.agents/skills/buzz-cli (symlinked into .claude/.codex/.goose) | skill | n+d | 167 | — | project — cross-tool nest shared with Codex/Goose (A6); moving it breaks other tools | as proposed |
| ☑ | gfmcloud-estate-map | ~/.claude/scheduled-tasks/gfmcloud-estate-map | scheduled-task skill | n+d | 56 | — | project — belongs to the scheduler runtime, not plugin distribution | as proposed |

## Inventory — `archive` rows (leave recoverable; no active use)

| ✓ | Skill | Current path | FM | Lines | Drift | Proposed | Ruling |
|---|-------|--------------|----|-------|-------|----------|--------|
| ☑ | scl-keeper-logic-validator (stale) | Documents/…/sloshy/.claude/skills/ | n+d (frontmatter claims authority; body says SUPERSEDED) | 386 | D1 | archive — recoverable in sloshy git history; rename `.migrated-off` in Phase 3, remove at Gate B | as proposed |
| ☑ | scl-keeper-logic-validator (v2 project copy) | work/GitHub/sloshball-champions-league-v2/.claude/skills/ | n+d | 186 | D1 | archive — superseded by library:scl; `.migrated-off` in Phase 3 (recoverable in v2 git history) | **OVERRIDDEN: project — stays live**; SCL skills remain project-local (Gate A) |
| ☑ | scl-session-startup-enforcer (v2 project copy) | same repo | n+d | 161 | D2 | archive — superseded by library:scl | **OVERRIDDEN: project — stays live** |
| ☑ | scl-module-deploy-checklist (v2 project copy) | same repo | n+d | 218 | D3 | archive — superseded by library:scl | **OVERRIDDEN: project — stays live** |
| ☑ | SCL archive sources ×3 | Documents/…/SCL-MIGRATED…/04 Skills/ | — | 399/152/204 | D1–D3 (oldest generation) | archive — already frozen in do-not-edit folder; no action, not touched | as proposed |
| ☑ | .skill zip exports ×6 | Documents/…/SCL-MIGRATED…/09 Migration/skills/ | — | — | D8 | archive — stale 2026-07-15 exports of live marketplace skills; no action, not touched | as proposed |
| ☑ | systems-design.skill | gfmcloud/plugins/workbench/skills/systems-design/ | — | — | — | archive — build artifact beside its own source; superseded when repo migrates | as proposed |

## Out of scope (upstream-owned or runtime artifacts — no rows, no action)

- `claude-plugins-official` marketplace clone: ~74 catalog skills, 30 commands, 38
  agents — Anthropic upstream; consumed, never edited. Includes upstream defects
  (3 skill-creator agents missing `name:`, malformed silent-failure-hunter YAML,
  access/configure name collisions) — not ours to fix.
- `careerhackeralex` marketplace + `visualize@0.4.0` cache — third-party plugin,
  consumed as installed.
- Plugin cache copies of gfm-foundry/visualize skills (incl. 10 orphaned stale-version
  files) — cache artifacts; superseded by Phase 4 deregistration, never edited.
- Claude Desktop `local-agent-mode-sessions` (14 SKILL.md) — app session cache,
  regenerates.
- Playwright (9) and GitHub Desktop.app (2) SKILL.md files — filename collisions,
  not Claude Code skills.
- `ref/skill-organization-template/.claude/skills/phase` — fixture inside an
  unconfigured template scaffold (D5), not a live skill.
- `~/claude-context/skills/README.md` — empty placeholder of a separate scaffold
  project; noted to avoid future divergence (A8).

## Drift details

- **D1 — scl-keeper-logic-validator** (4 copies): marketplace copy vs SCL-v2 project
  copy differ only in punctuation (8 diff lines, em-dashes→commas — a sanitization
  pass). The `sloshy` copy (386 ln) and Documents-archive copy (399 ln) are a older
  generation, pre-Rulings-8–15, and the sloshy body carries an explicit "⛔ SUPERSEDED
  DO NOT USE" banner (contradicting its own frontmatter). *Recommendation: marketplace
  copy → `library:scl`; v2 project copy `.migrated-off`; sloshy/archive copies archive.*
- **D2 — scl-session-startup-enforcer** (3 copies): marketplace vs v2 differs only in
  description reflow + punctuation; content-equivalent. Archive copy is an older
  152-line generation. *Recommendation: marketplace → library.*
- **D3 — scl-module-deploy-checklist** (3 copies): real structural drift. Marketplace
  copy is a deliberate library-ization: volatile status externalized to
  `references/project-status.md` (same 2026-07-07 status content preserved), Step-8
  verification wording generalized from Contracts-DB-specific to any module, explicit
  DNS HARD GATE added. No unique v2 content lost. *Recommendation: marketplace →
  library (structural superset, matches authoring standard).*
- **D4 — content-builder agent** (2 clones of the-michiana-trail): work/GitHub copy
  (28 ln) adds a "the validator is not optional" section missing from the home-dir
  clone's 5-line copy. *Recommendation: winner work/GitHub clone; home-dir clone is a
  stray checkout (A3).*
- **D5 — phase skill**: harness copy vs template-scaffold copy byte-identical;
  template is boilerplate, out of scope.
- **D6 — fable-advisor agent**: byte-identical across both michiana-trail clones.
- **D7 — gfm-foundry repo duplicated**: `~/gfm-foundry` and `~/work/GitHub/gfm-foundry`
  byte-identical at the same commit; both become superseded once plugins migrate.
  *Recommendation: migrate from `~/gfm-foundry`; both clones on the Gate B list.*
- **D8 — .skill zip exports vs live marketplace skills** (graham-voice, handoff,
  fable-project-review, scl×3): zips dated 2026-07-15 predate the marketplace repo's
  final commit (2026-07-23, "vendor customized fork into workbench"). *Recommendation:
  marketplace copies win everywhere; zips stay archived.*

## Not migrated / anomalies

- **A1** — `pipeline-foundry` plugin exists on disk in gfm-foundry but is missing from
  its `marketplace.json`, so it was never installable. Rec: enters library as
  `_incubator` (unproven by definition).
- **A2** — 5 gfmcloud-skills SKILL.md files have genuinely malformed YAML frontmatter
  (unquoted `description:` containing `": "`): design-taste-frontend,
  image-taste-frontend, minimalist-ui, capability-index, handoff. Rec: fix quoting
  during Phase 3 normalization (packaging fix, behavior-neutral).
- **A3** — Two clones of `the-michiana-trail` (home dir on a `claude/…` branch;
  work/GitHub on main) with drifted agent content. Rec: work/GitHub is canonical;
  home-dir clone offered on the Gate B cleanup list (user call — it's a git clone,
  may hold unpushed work; verify before deletion).
- **A4** — `emil-design-eng` is live inside a folder named
  `SCL-MIGRATED-2026-08-04-DO-NOT-EDIT` (a pre-existing freeze marker from an earlier,
  unrelated migration — not this project's convention). Migrating it out technically
  edits a do-not-edit folder. Rec: migrate (the freeze predates this project and the
  skill is the folder's only live content); needs explicit Gate A ruling.
- **A5** — `capability-index` describes "installed but disabled" skill packs — a
  premise that doesn't match this machine (the packs were never installed). Rec:
  migrate as-is; content refresh is post-migration authoring work, noted in library
  CHANGELOG as a known gap.
- **A6** — `buzz-cli` is reachable via symlink shared across `.claude`/`.codex`/`.goose`
  in `~/.buzz`; real file in `.agents/skills/`. Rec: leave untouched — migrating would
  break two non-Claude tools; two-homes rule not violated (one real file).
- **A7** — `project-constants` (sloshball-ff) is 1188 body lines, part research log.
  Rec: stays project; flag to user that it violates the 500-line guidance if ever
  promoted.
- **A8** — `~/claude-context/skills/` is an empty placeholder of a separate planned
  scaffold ("mirrored from ~/.claude"). Rec: user should reconcile that project's plan
  with this migration to avoid recreating the two-homes problem.
- **A9** — `scoreboard-ipad` repo has no git remote; its agents stay project-local
  regardless. Informational.
- **A10** — Every one of the 88 swept skills lacks the target `metadata:` block
  (maturity/version/reviewed). Blanket normalization in Phase 3, not per-row drift.

---

**Migration completed 2026-08-09.** All 63 rows executed or ruled; all six Phase 5
checks passed; Gate B deletions confirmed by the user and executed (both retired
source repos, the duplicate gfm-foundry and the-michiana-trail clones, all
project-side `.migrated-off` items, the orphan zip, and the stale gfm-foundry
plugin cache). This file is the permanent historical record.

---

**Migration completed 2026-08-09.** All 63 rows executed or ruled; Gate B deletions
confirmed and performed (3 retired source repos, 5 project-side `.migrated-off`
items, the orphan zip, and the duplicate the-michiana-trail clone). Post-deletion
smoke test: validator green (37 skills), fresh-context resolution confirmed. This
file is the permanent historical record.
