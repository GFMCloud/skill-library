# Changelog

Behavior changes only — not wording tweaks. Newest first.

## 2026-08-15 - Weekly maintainer cycle 1

First cycle of the `claude-improvements-weekly` maintainer. Pack bump: workbench
0.5.0.

- **phased-harness 1.2.1**: the six scaffolding templates no longer emit em dashes.
  They were copied verbatim into every harness the skill scaffolds, so each new
  project started life violating the global no-em-dash rule and had to be hand
  corrected. 59 occurrences across 54 lines: 58 became ` - `, and one became a full
  stop, which forced a single `this` to `This`. No word was added, removed, or
  reordered, and no placeholder changed. The skill's own `SKILL.md` and
  `references/doctrine.md` prose is
  deliberately left alone, since the global rule exempts pre-existing text from
  retroactive restyling; only the generator was changed.
- **capability-index**: rewritten against live plugin state, because every structural
  claim it made was false. It named packs `deck-build` and `deck-critique`, merged into `decks`
  during the migration to this repo; it pointed at marketplace `gfmcloud-skills`,
  superseded by `skill-library`; it described the deck skills as installed but
  disabled when `claude plugin list` shows `decks@skill-library` installed and
  enabled, which falsified the skill's whole premise; it listed an `scl` pack that is
  not installed at all; and it told the reader to verify with `scripts/list-skills.py`,
  which does not exist. The table now holds only capability a session genuinely cannot
  reach: the uninstalled `_incubator` pack, and the SCL skills, which are
  project-scoped in the SCL v2 repo and therefore have no install command at all.

## 2026-08-14 - Session-review wave: eight skill edits, five new builds

From the 2026-08-13 session-review backlog, executed via the claude-improvements
harness. Pack bumps: workbench 0.4.0, decks 0.2.0, frontend-design 0.2.0,
consistency-checker 0.1.0 (its first version stamp; the manifest had no version key
at all), _incubator 0.2.0.

- **phased-harness 1.2.0** (SL-1, SL-3, SL-6, SL-7): a routing front-door section so
  sessions land in the right mode; the Phase 0 truth-pass fixes as adjusted (derived
  counts, git-init check on unversioned deletion targets, a mandatory Phase 0 write
  preflight with negative controls, and an mtime check for a parallel harness already
  in flight); generated templates now name their subagent types; new doctrine line:
  prefer ending a session at a phase or gate boundary over grinding one session long.
- **handoff** (SL-2): gains the claim protocol and a live-state check that verifies
  deploy state, not just git state, before writing the handoff. Now versioned 0.1.0,
  `reviewed: 2026-08-13`; stays `maturity: incubator` per the Gate A ruling.
- **skill-discovery** (SL-4): its five scanner spawn sites pin `model: sonnet`
  instead of inheriting the parent model, and the inline scanner spec (75 lines) is
  replaced by a pointer to the new `workbench:transcript-scanner` agent.
- **New agent `workbench:transcript-scanner`** (SL-5): reusable session-transcript
  scanning agent; locates sessions by content and metadata, never trusting a
  reported session id as a filename, and reports discrepancies instead of
  reconciling them silently.
- **New agent `frontend-design:frontend-surface-builder`** (WL-2): builds frontend
  surfaces under the pack's design-skill constraints.
- **New incubator skills** (SL-8, WL-1, WL-3): `cloudflare-pages-migration` (with a
  worked example; unverified limits are marked as such and dated rather than
  asserted), `retro` (gated on-demand retrospective, plus template),
  `sweep-harness`, `rulings-harness`, and `experiment-harness` (the three harness
  archetypes; experiment-harness's scaffold is fresh design from recovered intent,
  and its doctrine file marks invented versus recovered elements explicitly).

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
