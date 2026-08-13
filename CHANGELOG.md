# Changelog

Behavior changes only — not wording tweaks. Newest first.

## 2026-08-12 — phased-harness 1.1.0: generated harnesses defer to the global rules

Four changes referred from the `claude-md-consolidation` project, which found that
generated harnesses were emitting their own variants of rules the global
`~/.claude/CLAUDE.md` now owns. workbench bumped to 0.3.0.

- **Generated CLAUDE.md now opens with the pointer line** to `~/.claude/CLAUDE.md` and
  states only the project-specific *binding* of a global rule (move-never-copy,
  `.superseded`, executed evidence, proven-by-deliberate-failure) instead of
  restating the rule. A restated global rule is the second editable copy these
  projects exist to eliminate.
- **`.superseded` is now the only retirement suffix the skill offers.** The former
  menu (`.migrated-off` / `.retired` / `.superseded`, pick one) is retired; one
  suffix means one grep finds every retired item on the machine. A repo with its own
  established convention (e.g. `archive/`) keeps it, declared in the harness.
- **Nothing in a generated harness asserts a gate count.** Two gates remain the
  default, a third is legitimate when a project has a second decision of Gate B's
  weight (scl-player-model has three); the dispatch skill's interruption policy is now
  the single place gates are enumerated. Previously "the two gates" was hardcoded into
  every generated CLAUDE.md and went stale silently.
- **Harness-dir git conventions are pre-filled** with the default that was being
  hand-written near-identically into every project (no commits unless asked;
  `workbench:folder-to-repo` if it should become a repo). The open slot now asks only
  about the repos the project *changes*.

## 2026-08-09 — phased-harness promoted to workbench

- `phased-harness` promoted out of `_incubator` into **workbench** (`git mv`,
  content unchanged), entering as `stable` 1.0.0. Promoted by user ruling ahead
  of the two-real-projects guideline. workbench bumped to 0.2.0.

## 2026-08-09 — phased-harness added to _incubator

- New skill `phased-harness`: interviews for end-state invariant, irreversible
  step, and standing authorizations, then scaffolds a gated multi-phase project
  harness (CONFIG/STATE/end-state/runbooks/dispatch skill). Distilled from the
  skill-migration retro; doctrine and templates included. Incubator — graduates
  after scaffolding two real projects.

## 2026-08-09 — Phase 3 migration

- **foundry-core** (evidence-report, proof-of-work), **turn-reduction**
  (capability-preflight, output-lint, standing-authorization), **data-wrangler**
  (identity-resolution + data-pipeline-owner agent): migrated from gfm-foundry,
  entering as `stable` 1.0.0 (installed and in daily use). Content unchanged.
- **verification-kit**, **consistency-checker**, **deploy-ops**: migrated from
  gfm-foundry with their agents, entering as `incubator` (never installed).
- **decks**: new plugin merging gfmcloud-skills' deck-build + deck-critique
  (6 skills). Content unchanged.
- **frontend-design**: 4 skills from gfmcloud-skills (YAML frontmatter repaired on
  design-taste-frontend, image-taste-frontend, minimalist-ui — descriptions were
  unparseable), plus `frontend-design` (from sloshball-champions-league-v2, with
  its LICENSE.txt) and `emil-design-eng` (rescued from a frozen Documents archive;
  675-line body split — six technique sections moved verbatim to
  `references/techniques-and-craft.md`).
- **workbench**: 12 workbench skills + graham-voice folded in from the voice
  plugin (YAML repaired on capability-index and handoff). Known gap:
  capability-index describes "installed but disabled" packs, a premise that
  doesn't match this machine — content refresh pending.
- **_incubator**: pipeline-foundry (was unlisted in gfm-foundry's manifest, never
  installable), devshell-init (promoted from mac-setup), new-project (unpacked
  from an orphan .skill zip).
- Not migrated by user ruling: the three SCL skills stay project-local in
  sloshball-champions-league-v2.

## 2026-08-09

- Repo created: marketplace skeleton with `_incubator` plugin, validator
  (`scripts/validate-skills.sh`), CI workflow, authoring standard, and skill
  template. No skills yet — migration follows.
