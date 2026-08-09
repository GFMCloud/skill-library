# Project state

**PROJECT COMPLETE (2026-08-09).** All phases done; both gates passed; deletions
executed. `~/skill-library` (github.com/GFMCloud/skill-library) is the single
canonical home of every reusable skill; MIGRATION.md there is the permanent record.

## Phase tracker

- [x] Phase 0 — Repo skeleton (2026-08-09)
- [x] Phase 1 — Inventory (read-only) (2026-08-09)
- [x] Phase 2 — Disposition / Gate A (2026-08-09)
- [x] Phase 3 — Migrate (2026-08-09)
- [x] Phase 4 — Wire consumption (2026-08-09)
- [x] Phase 5 — Verify, then delete (2026-08-09)

## Decision log

<!-- Append: date — decision — one-line rationale. Never rewrite old entries. -->

- 2026-08-09 — Phase 0 built repo at `~/skill-library`, pushed to
  `github.com/GFMCloud/skill-library` (private). Three commits: skeleton,
  validator, CI.

### Phase 0 validator evidence (deliberate-failure test)

Fixtures `fixture-a` (F3) and `fixture-b` (F5+F10) produced, verbatim:

```
FAIL F3 plugins/_incubator/skills/fixture-a: missing name
FAIL F5 plugins/_incubator/skills/fixture-b: name 'wrong-name' != directory 'fixture-b'
FAIL F10 plugins/_incubator/skills/fixture-b: stable without semver version ('')
FAIL F10 plugins/_incubator/skills/fixture-b: stable without ISO reviewed date ('')
FAIL F12 plugins/_incubator/skills/fixture-b: _incubator skill marked stable

2 skills checked: 5 failures, 0 warnings
exit=1
```

After removing fixtures: `0 skills checked: 0 failures, 0 warnings`, exit 0.
Fresh clone from GitHub also passes with exit 0.

- 2026-08-09 — Gate A rulings (one batch, AskUserQuestion): absorb BOTH personal
  marketplaces (gfm-foundry, gfmcloud-skills) into skill-library; **SCL proposal
  overridden** — no scl plugin, the three SCL skills stay project-local in
  sloshball-champions-league-v2 (user accepts that marketplace copies retire with
  their repo); emil-design-eng migrates out of the frozen archive folder;
  graham-voice→workbench, devshell-init→_incubator, new-project unpacked
  →_incubator, decks merge — all approved. All other rows "as proposed"
  (MIGRATION.md commit c291343).
- 2026-08-09 — Final plugin list (10): foundry-core, turn-reduction,
  data-wrangler, verification-kit, consistency-checker, deploy-ops, decks,
  frontend-design, workbench, _incubator.
- 2026-08-09 — Phase 4 deregistrations: uninstalled foundry-core@gfm-foundry,
  turn-reduction@gfm-foundry, data-wrangler@gfm-foundry; removed marketplaces
  `gfm-foundry` and `gfmcloud-skills`. Registered `skill-library`
  (GFMCloud/skill-library), installed all 9 real plugins (not _incubator).
  enabledPlugins now: 9× @skill-library + github@claude-plugins-official +
  visualize@careerhackeralex. Old gfm-foundry cache dirs remain on disk
  (uninstalled; candidates for Gate B / `claude plugin prune`).
- 2026-08-09 — Shadow neutralization: SKILL.md inside the four project-side
  `.migrated-off` dirs renamed to `SKILL.md.migrated-off` (mac-setup
  devshell-init, SCL-v2 frontend-design, sloshy scl-keeper-logic-validator,
  frozen-archive emil-design-eng) so nothing loads twice; fully reversible.
- 2026-08-09 — Global `~/.claude/CLAUDE.md` edit (add-only, authorized): appended
  this exact new section at EOF:

  ```markdown
  ## Skill management

  Reusable skills live in the canonical library repo `github.com/GFMCloud/skill-library`
  (local clone: `~/skill-library`) and are consumed everywhere as installed plugins from
  the `skill-library` marketplace. They are edited ONLY in that repo — never in plugin
  caches (`~/.claude/plugins/**`) or any other copy.

  - Skill-creation requests route by reuse: project-specific → that project's
    `.claude/skills/`; reusable → `~/skill-library/plugins/_incubator/` (then follow the
    library repo's CLAUDE.md authoring rules).
  - A project-local skill that duplicates a library skill's name or content is drift —
    flag it, don't silently keep both.
  ```

## Anomalies

<!-- Skills/situations the prompts didn't anticipate. Path, what's odd, recommendation. -->

- 2026-08-09 — Phase 5 check 1 (single-home re-sweep): initial FAIL — the `scl`
  plugin was left live in ~/gfmcloud-skills-marketplace/plugins/ (its five
  siblings were suffixed but scl had no Phase 3 move task after the Gate A
  project ruling, so nothing retired it). Fixed same pattern: dir →
  `scl.migrated-off`, inner SKILL.md files → `.migrated-off`. Targeted re-check:
  zero live SKILL.md remain in either retired source repo. All other sweep
  findings match the expected taxonomy exactly (37/37 library skills; 18/18
  .migrated-off items incl. scl; marketplaces = official/careerhackeralex/
  skill-library only). Cache lacks `_incubator` because that plugin is
  deliberately not installed — expected, not a defect. → check 1 PASS after fix.
- 2026-08-09 — **Phase 5 blocker (checks 2+3):** headless `claude -p` fails with
  "OAuth session expired and could not be refreshed" (reproduced directly by the
  orchestrator; Claude Code 2.1.226). Fresh-context resolution and
  auto-invocation checks cannot run until the user re-authenticates
  (`claude login` or an interactive `claude` session). Checks 4 (CI gate: PR #1
  failed as required, closed unmerged), 5, and 6 PASS; check 1 in flight.
  Note: the check-2/3 subagent tripped a harness security warning for probing
  credential-store *existence* while diagnosing (env vars, credentials file,
  keychain entry name); it reports no modification and no values read — flagged
  here for user awareness.

- 2026-08-09 — Phase 5 checks 2+3 re-run after user re-auth — **PASS**.
  Evidence (fresh-context headless `claude -p` from neutral temp dirs):
  (2a) skill listing shows all 34 installed library skills exactly once under
  their plugin namespaces (foundry-core 2, turn-reduction 3, data-wrangler 1,
  verification-kit 1, consistency-checker 1, deploy-ops 1, decks 6,
  frontend-design 6, workbench 13); no duplicates from retired sources;
  _incubator absent as designed; (2b) `/foundry-core:proof-of-work` loaded and
  followed the skill ("Standard is loaded…"); (3) unprompted match: the
  two-CSVs-no-shared-key prompt auto-invoked the skill, transcript ends
  "SKILL USED: data-wrangler:identity-resolution". **All 6 Phase 5 checks now
  PASS.** Deletion awaits explicit Gate B confirmation.

- 2026-08-09 — Gate B (explicit user confirmation): delete all 8 core
  .migrated-off items + optional cleanups (cache removal, ~/the-michiana-trail
  duplicate clone). Executed: both retired source repos, ~/work/GitHub/gfm-foundry
  and ~/the-michiana-trail clones, 4 project-side .migrated-off items,
  new-project.skill.migrated-off, and ~/.claude/plugins/cache/gfm-foundry
  (approved via the "prune caches" option; `claude plugin prune` itself had
  nothing to prune as those weren't auto-installed). Post-deletion smoke:
  validator green (37 skills, 0/0) and fresh-context listing resolves 35
  namespaced skills (34 library + visualize). No .migrated-off item remains
  anywhere.

- 2026-08-09 — Gate B ruled (one batch): delete all 8 core items + both
  optionals (`claude plugin prune`, the-michiana-trail home clone — verified
  clean/pushed first). Executed: 3 retired source repos, 4 project-side
  `.migrated-off` dirs, orphan zip (already absent), michiana clone. Prune
  found nothing at user scope (stale gfm-foundry cache dirs were
  manually-installed, not auto — left in place as harmless, Claude-Code-managed
  cruft). Post-deletion smoke test: validator green (37 skills, 0/0); fresh
  `claude -p` confirms foundry-core:proof-of-work and workbench:graham-voice
  resolve exactly once. **Phase 5 complete; project complete.**

Phase 1 logged 10 anomalies, recorded in full as A1–A10 in the library repo's
`MIGRATION.md` (commit 116b888). Headlines: pipeline-foundry unlisted in
gfm-foundry's marketplace.json (A1); 5 gfmcloud skills with malformed YAML
frontmatter (A2); duplicate clones of the-michiana-trail with drifted agents (A3)
and of gfm-foundry (D7); emil-design-eng stranded live in a pre-existing
DO-NOT-EDIT archive folder (A4 — needs Gate A ruling); buzz-cli symlink-shared
with Codex/Goose, left untouched (A6); no swept skill has the target metadata
block (A10 — blanket Phase 3 normalization).

## Session log

<!-- One line per session: date — phase worked — outcome/stopping point. -->

- 2026-08-09 — Phase 0 — complete: skeleton built, validator proven (failed then
  clean), pushed; fresh clone passes. Continuing to Phase 1.
- 2026-08-09 — Phase 1 — complete: 3 subagent sweeps (~/.claude, project repos,
  home-wide strays) merged; drift diffs run on all duplicate groups; MIGRATION.md
  with 63 proposed rows committed (116b888). Stopped at Gate A for rulings.
- 2026-08-09 — Phase 2 — complete: rulings collected in one batch, recorded and
  sanity-checked (every row ruled, winners set, no library name collisions),
  committed c291343. Continuing to Phase 3.
- 2026-08-09 — Phase 3 — data-wrangler plugin migrated: `cp -R` from
  `~/gfm-foundry/plugins/data-wrangler` to `~/skill-library/plugins/data-wrangler`
  (`diff -r` clean), source renamed to
  `~/gfm-foundry/plugins/data-wrangler.migrated-off`. Ratified rows moved: skill
  `identity-resolution` (metadata block added — maturity: stable, version: 1.0.0,
  reviewed: 2026-08-09; name/description/body unchanged; name == dirname
  confirmed), agent `data-pipeline-owner` (moved as-is). plugin.json kept
  unchanged (name `data-wrangler`). `validate-skills.sh plugins/data-wrangler`:
  `1 skills checked: 0 failures, 0 warnings`, exit 0. No git commands run (per
  task rules) — commit still pending. Other plugins from the 10-plugin Phase 3
  list not yet migrated.
- 2026-08-09 — Phase 3 — decks plugin merged from two source plugins: `deck-build`
  (`cd-to-pptx`, `chart-discipline`, `deck-scaffolding-builder`, `html-diagram`)
  and `deck-critique` (`layout-critique`, `sales-lens-review`), both in
  `~/gfmcloud-skills-marketplace`. New `plugins/decks/.claude-plugin/plugin.json`
  written (name `decks`, version 0.1.0). All 6 skill dirs `cp -R`'d in full
  (references/assets/scripts included), each `diff -r` clean. Sources renamed to
  `~/gfmcloud-skills-marketplace/plugins/deck-build.migrated-off` and
  `deck-critique.migrated-off`. Each SKILL.md got `metadata: maturity: incubator`
  only (never installed → incubator; no version/reviewed needed per validator
  spec) — name/description/body unchanged, name == dirname confirmed for all 6.
  `validate-skills.sh plugins/decks`: `6 skills checked: 0 failures, 0 warnings`,
  exit 0. No git commands run (per task rules) — commit still pending.
  marketplace.json/CHANGELOG.md/MIGRATION.md not touched (out of scope for this
  row). Other plugins from the 10-plugin Phase 3 list not yet migrated.
- 2026-08-09 — Phase 3 — `_incubator` plugin populated (existing plugin.json
  kept, name `_incubator`): `pipeline-foundry` (`cp -R` from
  `~/gfm-foundry/plugins/pipeline-foundry/skills/pipeline-foundry`, `diff -r`
  clean, whole source plugin dir renamed to
  `~/gfm-foundry/plugins/pipeline-foundry.migrated-off`), `devshell-init`
  (`cp -R` from `/Users/gfm/src/mac-setup/.claude/skills/devshell-init`,
  `diff -r` clean, source renamed to `devshell-init.migrated-off`),
  `new-project` (unzipped `/Users/gfm/work/new-project.skill`, inner
  `new-project/` dir — SKILL.md + references/ + scripts/scaffold.sh — moved
  into `_incubator/skills/new-project`, zip renamed to
  `new-project.skill.migrated-off`). All three: `metadata: maturity: incubator`
  added to frontmatter; name == dirname confirmed for all three, no renames
  needed. `.gitkeep` removed from `_incubator/skills/` now that it has content.
  `validate-skills.sh plugins/_incubator`: `3 skills checked: 0 failures, 0
  warnings`, exit 0. No git commands run (per task rules); marketplace.json,
  CHANGELOG.md, MIGRATION.md untouched (per task rules) — commit still
  pending. Other plugins from the 10-plugin Phase 3 list not yet migrated.
- 2026-08-09 — Phase 3 — COMPLETE (orchestrator wrap-up): all 10 plugins
  migrated by parallel subagents, zero blocked rows; all 63 MIGRATION.md rows
  checked off; sloshy's superseded scl-keeper-logic-validator renamed
  `.migrated-off`; no library/project name collisions; full validator green
  (37 skills, 0 failures, 0 warnings); marketplace.json catalogs all 10
  plugins; CHANGELOG migration entries added; per-plugin commits pushed
  (b5c52e3..8b75358). Vacated sources now `.migrated-off`: 7 plugin dirs in
  ~/gfm-foundry, 5 in ~/gfmcloud-skills-marketplace, frontend-design in SCL v2
  repo, emil-design-eng in the frozen archive, devshell-init in mac-setup,
  ~/work/new-project.skill. Continuing to Phase 4.
- 2026-08-09 — Phase 4 — complete: skill-library marketplace registered, 9
  plugins installed and enabled; gfm-foundry/gfmcloud-skills deregistered and
  their 3 installed plugins uninstalled; shadow SKILL.md files neutralized in
  the four project-side .migrated-off dirs; global CLAUDE.md consumption section
  appended (exact diff in decision log). Continuing to Phase 5.
- 2026-08-09 — Phase 5 — complete: all 6 checks PASS (check 1 after retiring the
  missed scl dir; checks 2+3 after user re-auth); Gate B confirmed and executed;
  post-deletion smoke green; MIGRATION.md completion line pushed (0fa2a0d).
  **Project complete.**
- 2026-08-09 — Phase 5 — complete: 6/6 checks passed (one fix: scl straggler
  retired; one user action: headless re-auth), Gate B ruled and executed,
  post-deletion smoke test green. PROJECT COMPLETE.
