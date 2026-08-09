# Changelog

Behavior changes only — not wording tweaks. Newest first.

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
