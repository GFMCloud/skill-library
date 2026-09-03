# Changelog

Behavior changes only — not wording tweaks. Newest first.

## 2026-09-03 - repo-handoff: hand a personal-data-bearing repo to another person

Pack bump: workbench 0.9.0. New incubator skill `repo-handoff` (weekly maintainer cycle 5,
F-11), built because the same workflow ran by hand three times between 2026-08-28 and
2026-09-02 for three recipients (a privatized fork before Graham's data went in, a clean
branch cut for Lauren with `git log -S`, a sanitized fantasy-draft toolkit for a friend).

- **`repo-handoff`:** inventory personal, league or client-specific, copyrighted and
  credential-bearing content by identifier grep and file class; cut a clean commit or a
  sanitized subset; prove the delivered tree clean (identifier grep to zero, `gitleaks`,
  credential-file find), a hit being a stop; create the recipient's private repo without
  touching Graham's origin; write a walkthrough and execute every command in it before
  handover. Negative scope: not `folder-to-repo` (fresh folders), not a routine push.

## 2026-09-03 - turn-reduction 1.1.0: the plugin gains the version field it never had

Pack bump: turn-reduction 1.1.0 (weekly maintainer cycle 5, F-2). `plugin.json` had no
`version` since the migration commit that called it "stable 1.0.0", so the two skill bumps
since (standing-authorization 1.1.0 on 2026-08-28, capability-preflight 1.1.0 on
2026-09-02) landed without the plugin bump the authoring rules require. Installed caches
had been tracking it by commit sha. No skill body changed.

## 2026-09-02 - x-read: full X posts, Articles, and threads from the terminal

Pack bump: workbench 0.8.0. New incubator skill `x-read`.

- **`x-read`:** `node scripts/x-read.mjs <post-url>` returns a post, a long-form X Article
  (title plus complete body via the `TweetDetail` GraphQL call with article field toggles,
  falling back to `UserArticlesTweets` plain text), a whole thread, or an X search, as
  Markdown or `--json`. Engine is a vendored read-only subset of `@steipete/bird` 0.8.0
  (MIT; the npm package is deprecated upstream, hence pinned and vendored). Credentials come
  from `AUTH_TOKEN`/`CT0` env or keychain items `x-read-*` (fallback `last30days-*`), stored
  by `scripts/x-read-auth.sh`, which only Graham runs; values never pass through Claude.
  Motivation: last30days' vendored bird subset is search-only and caps post text at 500
  characters, so Articles arrived as previews.

## 2026-09-02 - andrej-karpathy-skills reviewed: one fragment into proof-of-work, two into the global CLAUDE.md

Pack bump: foundry-core 0.2.2. Source: github.com/multica-ai/andrej-karpathy-skills, pinned at
commit `2c60614`. Verdict HARVEST; record and evidence in
`docs/reviews/2026-09-02-andrej-karpathy-skills.md` and its directory. No new skill; the source is a
four-principle CLAUDE.md, two principles redundant against the harness prompt, one contradicting it.

- **`proof-of-work` 1.1.0:** multi-step work declares each step's check before the step runs, so the
  evidence standard is fixed up front rather than chosen after the output exists.
- **Global CLAUDE.md, "Surgical edits" block** (`~/.claude` commit `566c71a`): the orphan-cleanup
  asymmetry, match-existing-style, and code-shape anti-overengineering rules. First proposed as banked
  (a 60-day transcript scan found one qualifying correction; the economy rule needs two); Graham ruled
  to add it anyway, overriding the economy rule with that one correction on record.

## 2026-09-02 - source-intake: chunked clean-room review for large sources

Pack bump: workbench 0.7.3. Learned on the bojieli/ai-agent-book run (190k words), which
could not fit one headless context.

- **`source-intake`:** Step 2 gains a rule for sources over roughly 40k words: split into
  natural units, one clean-room `claude -p` per unit at Sonnet (up to six in parallel, every
  exit code and output checked), then one headless synthesis at the CLI default model that
  reads only the per-unit reviews and emits the consolidated review Step 3 consumes. Model
  split is now the default: Sonnet for per-unit reads and the Step 3 comparison agent,
  frontier for synthesis. Procedure and synthesis prompt in `references/large-sources.md`.

## 2026-09-02 - "AI Agents in Depth" (bojieli/ai-agent-book) harvested: six fragments on main, two by PR

Pack bump: workbench 0.7.2. Source: github.com/bojieli/ai-agent-book, English text, pinned at
commit `8b45707`. Verdict HARVEST; record and evidence in `docs/reviews/2026-09-02-ai-agent-book.md`
and its directory. No new skill; the book builds agent harnesses, this library drives Claude Code.

- **`model-effort-advisor`:** `decision-rubric.md` gains a diagnostic for a skill or prompt that
  already underperforms: hold it fixed, swap the model tier, and let the direction of the change
  say whether to rewrite the skill or change the model. `subagent-routing.md` build/review pairing
  now hands the reviewer the artifact and criteria only, never the builder's rationale.
- **`experiment-harness`:** the run template's Verdict field asks for paired per-item wins and a
  stated sample size or interval when two configurations are compared.
- **`docs/authoring-standard.md`:** descriptions state negative scope and cost, and a misrouting
  skill gets its description fixed before a stronger model is tried; rules are shaped as scope,
  action, exception, verification; a fix is tested on the boundary set and the retention set.
- **`evidence-report` 1.1.0** (foundry-core 0.2.1): a rule against adding separately measured
  improvements together; a combined claim is measured with everything applied or reported as
  separate claims.
- **`capability-preflight` 1.1.0:** `excerpt()` keeps the head and the tail of probe output with
  an explicit "chars omitted" marker instead of head-only truncation, so a failure printed after
  a long preamble is no longer hidden from the report. Proven by a fixture whose only error line
  sat past the old 400-char window.

## 2026-09-02 - No-mannered-prose rule added to the three copy-producing skills

Pack bumps: graham-voice 1.0.1, decks 0.2.1, frontend-design 0.4.1. Source: Anthropic's
"Prompting Claude Fable 5.1" guide (Writing density section), which names metaphor-for-statement
as the model's main prose tic and supplies the defining instruction. Same rule added to the
global CLAUDE.md the same day.

- **`graham-voice`:** drafts drop metaphor and flourish that stand in for a direct statement
  ("a dial worth turning", "earns its keep"); each figure of speech is swapped for the literal
  phrase unless it carries something the literal version cannot.
- **`deck-scaffolding-builder`:** `references/copy-voice.md` worst-tells list gains mannered prose.
- **`design-taste-frontend`:** `references/ai-tells.md` gains a mannered-copy tell for headlines,
  eyebrows, and body text alongside the em-dash tells.

## 2026-09-02 - AI-native SDLC playbook harvested: five fragments, three questions open

Pack bump: workbench 0.7.1. Source: claude.com/blog/the-ai-native-sdlc-playbook, pinned by
sha256 `adfcd44e…a213f` (fetched 2026-09-02). Verdict HARVEST; record and evidence in
`docs/reviews/2026-09-02-ai-native-sdlc-playbook.md` and its directory.

- **`fable-project-review`:** Low findings are capped at five per review with the rest
  summarized as a count; anything a formatter, linter, or CI already enforces, and anything
  under a generated path, is not reported.
- **`retro`:** the §3 routing table gains a row: a behavioral regression no script can catch
  routes to an eval case in the owning skill, not to prose.
- **`new-project`:** generated hard rule 6 and `conventions.md` SPEC.md §6 add the bug-fix
  procedure: reproducing test first, seen to fail for the expected reason, committed before
  the fix, untouched by the fix commit.
- **Authoring standard (rule change):** promotion requires a trigger test (three phrasings,
  fresh session); once a skill has eval cases they run on any change to that skill, its
  hooks, or its CLAUDE.md, and a pass-rate drop is reviewed before merge. The library had
  zero eval cases when this was written, so the second rule binds from the first one.
- **Not taken:** the article's `production-gate.sh` (substring match, Bash-only matcher,
  spoofable env var) and `agent-evals.yml` (no timeout, `result.json` overwritten per loop);
  fifteen practices already stated here with their originating failure attached. WATCH on
  σ-banded autonomy tiers (recheck 2026-12-01). Open for Graham: a test-file freeze hook, a
  credential-file `permissions.deny`, a Bash gate hook (recommended out).

## 2026-09-02 - _incubator retired; maturity is a label, not a location

Pack bumps: workbench 0.7.0, frontend-design 0.4.0, deploy-ops 0.2.0, foundry-core 0.2.0.
The `_incubator` plugin is removed from the marketplace. It was never installed on the
authoring machine (enabled in settings, absent from the install list), so its twelve
skills loaded in no session, and promotion out of it happened once in four weeks.

- **Twelve skills moved by `git mv`, content unchanged, still `maturity: incubator`:**
  `retro`, `experiment-harness`, `rulings-harness`, `sweep-harness`, `new-project`,
  `devshell-init`, `pipeline-foundry`, `source-intake` to **workbench**;
  `mobile-taste-frontend`, `scrollback` to **frontend-design**;
  `cloudflare-pages-migration` to **deploy-ops**; `full-output-enforcement` to
  **foundry-core**. Each now loads with its host plugin.
- **Rule change.** New skills go straight into the plugin they belong to, with
  `maturity: incubator` as a label. Promotion flips the label and adds `version` and
  `reviewed`; nothing moves. Adding a skill bumps the host plugin's version so daily
  plugin updates pick it up. CLAUDE.md, README, the authoring standard and the SKILL
  template say so.
- **Validator:** check F12 (`_incubator` skill marked stable) removed; there is no
  such plugin to check.
- **capability-index:** the `_incubator` row and its install instructions are gone.
  The only skill-library capability a session cannot reach is the disabled `decks`
  pack, which the table now lists instead.

## 2026-09-01 - Upstream taste-skill v2 merged into frontend-design; two incubator skills

Pack bumps: frontend-design 0.3.0, _incubator 0.3.0. Source: `Leonxlnx/taste-skill` at
`ccbc15639c97057cbfcf32ecebc38ef716e4bb37`, merged by hand through the `taste-skill-merge`
harness (36 ruled decision rows; nothing installed side by side, no upstream text copied).

- **`design-taste-frontend` behaves differently on five points.** Eyebrows are rationed
  (max 1 per 3 sections, hero counts as 1, mechanically counted at pre-flight) instead of
  mandated before every H1/H2. Infinite-loop card states are optional and must be
  motivated; the pack no longer says every card loops. `prefers-reduced-motion` is
  mandatory above `MOTION_INTENSITY 3`. Real images come first (generation tool, then
  seeded placeholders, then labeled `<!-- TODO -->` slots); div-based fake screenshots
  are banned. Hard bans became contextual with named overrides (purple when the brand
  asks, emoji for playful briefs, centered hero for manifesto and launch briefs), and a
  quiet-constraints rule lets accessibility-first and public-sector briefs override
  aesthetics. Also new: a brief-inference design read, a design-system map, a copy
  self-audit, and zero em dashes in rendered copy (en dashes in ranges stay).
- **Two corrections at ingest.** Upstream's WCAG large-text threshold ("18px+") is
  corrected to 18pt (about 24px) regular or 14pt bold, so subheads under 24px need 4.5:1.
  Upstream's two conflicting dark-mode contrast lines are reconciled as AA minimum for all
  text, AAA target for body and hero copy.
- **Not ingested, on purpose.** The dead Block Library contract, the 62-box pre-flight
  (now 15 countable items), the two cross-project-memory rules a stateless model cannot
  honor, and the redesign audit (routed to `redesign-existing-projects` instead).
- **`references/ai-tells.md` is now the whole catalogue.** Upstream's production-tested
  tells (hero version labels, section-number eyebrows, decorative dots, poetic section
  labels, photo-credit captions, locale strips, scroll cues) live there under distinctive
  "... tells" headings; the flagship body points at it and restates none. Long material
  moved out of the body into `references/` (GSAP skeletons, design-system map with install
  commands, dark-mode protocol, Liquid Glass approximation). Body 332 lines.
- **`image-taste-frontend`** gains the count-commitment protocol (commit to N sections out
  loud, label "Section X of N"), the brief-to-direction table, and the hero-scale pick.
- **New in `_incubator`:** `mobile-taste-frontend` (app screens as a distinct medium:
  platform commitment, safe areas, tab bars, onboarding flows, screen-set consistency;
  trimmed from 6,552 to 1,999 words and 19 dials to 3) and `full-output-enforcement`
  (anti-truncation discipline, with the TODO ban scoped to "user asked for a full
  implementation" so it does not collide with instructed image placeholders).
- **Inventory** regenerated (46 skills), absorbing the uncommitted 2026-08-30 regeneration.

## 2026-08-30 - Source intake pipeline retired

Graham closed the project. `source-review` and `source-harvest` are removed from
`_incubator`; the inventory drops from 46 skills to 44. The notes repo
`GFMCloud/personal-source-reviews` is archived read-only with all three notes
preserved, and the reason for closure is recorded in its README.

- **Both skills removed.** Neither was ever promoted out of incubator, and
  `source-harvest` never ran once: all three notes are permanently
  `status: reviewed`, so no harvest item was ever applied. The pipeline produced
  three documents and zero changes to the environment in four days.
- **What actually failed was transport, not judgment.** The notes are
  contract-compliant, the blind incumbent comparison (3b) ran and disclosed its
  own prep error, and untrusted-content flagging behaved correctly on both
  reviews that hit directive-shaped text. But the skill declared its environment
  as "web fetch plus the GitHub connector" while the runtime actually used was a
  cloud Claude Code session holding a token scoped to `claude/*` branches. It
  cannot write `main`. Two of three reviews stranded on unmerged branches, and
  `INDEX.md`, the file whose whole job is preventing duplicate reviews, was blind
  to both.
- **The generalizable lesson, worth keeping when something replaces this.** A
  skill that names its runtime in prose and never verifies it will be debugged at
  the wrong layer indefinitely. Three separate diagnoses this session all
  proposed fixing the write instruction; the environment was never checked until
  a commit trailer settled it. Two proposed fixes were unsatisfiable in the real
  runtime, and one of them (an auto-merge workflow) was a standing
  pre-authorized push to `main`, against the never-pre-authorizable rule.
  `INDEX.md` also proved to be a denormalized cache that both drifted and was
  the sole merge-conflict surface between concurrent runs.

## 2026-08-28 - Ratify execution (same-day, interactive)

Graham ruled the full pending queue and asked for immediate execution. Pack bumps:
workbench 0.6.0, graham-voice 1.0.0 (new), standing-authorization 1.1.0.

- **graham-voice split out of workbench** (ruled Q-2026-08-28-5): the skill moved
  unchanged to its own single-skill plugin `graham-voice`, so it can be installed
  from the marketplace alone; workbench drops "personal voice" from its
  description. This is a move, not a copy. Anyone with workbench installed loses
  `workbench:graham-voice` on their next plugin update and enables
  `graham-voice@skill-library` instead.
- **standing-authorization 1.1.0, `authz.py init`** (ruled Q-2026-08-20-2, rebuilt
  per Q-2026-08-28-7 after the first build was reverted): generates a starter
  `authorization.json` by parameterizing `authorization.example.json` (project
  name plus the three ceiling values; the granted and stop lists come through
  verbatim, keeping the example as the single editable home). Refuses to
  overwrite. Never invents a grant, and deliberately has no generic
  keep-going/proceed/continue entry: under the substring matcher those bare verbs
  auto-granted 10 of 10 dangerous probe asks in the reverted version. The rebuilt
  version's generated file scores 0 of 10 on the same probe suite (9 STOP-LISTED,
  1 NOT-COVERED), verified by execution before commit.

## 2026-08-28 - Weekly maintainer cycle 3

Third cycle of the `claude-improvements-weekly` maintainer. Pack bump: workbench 0.5.2.

- **phased-harness 1.2.3**: two rules added to the set every generated harness bakes in,
  both from the spec-kit comparison you asked about on 2026-08-15 and ruled on 2026-08-20.
  First, a constitution conflict is a **stop**, not a tiebreak: when a phase's plan
  collides with an invariant in `docs/end-state.md`, the harness's own `CLAUDE.md`, or
  the never-pre-authorizable list in `CONFIG.md`, the phase
  bends and the invariant does not, and amending an invariant becomes its own gated act
  rather than a side effect of the phase that hit it. Previously the skill said nothing
  about this case, so a harness meeting one had only the reading that let it continue.
  Second, a **residue rule**: the final phase must name where its leftovers go (an owned
  open item in `STATE.md`, a named successor, or explicitly dropped with the reason
  written next to it) before the harness may
  close, because a harness that closes silently converts its own open gaps into "done".
  Both rules are carried by template slots, not by the SKILL.md body alone: the
  constitution rule lands in `project-CLAUDE.template.md` and `STATE.template.md`, the
  residue rule in `end-state.template.md`'s definition-of-done, in
  `phase-runbook.template.md`, and as a new `## Open items` section in
  `STATE.template.md` so the destination the rule names actually exists in a generated
  harness. Every other generation rule already had template hooks;
  a rule that reaches a harness only through the generating model's discretion is the
  same silent-prose failure these two rules exist to prevent.

## 2026-08-26 - Source intake pipeline and inventory gate

- **validator**: new check F13. `docs/inventory.md` (one line per skill, emitted
  by the new `scripts/generate-inventory.sh`) must match the tree on every full
  run; a stale or missing inventory fails locally and in CI. The frontmatter
  parser moved from the validator's inline heredoc into `scripts/skill_meta.py`,
  shared by both scripts, so it has one editable home. Gate proven by deliberate
  failure: missing file failed, poisoned file failed, regenerated file passed,
  single-plugin runs skip it.
- **New incubator skills**: `source-review` (read-only review of incoming
  articles/repos/papers; emits a committed verdict note under a versioned v1
  contract) and `source-harvest` (parses a note's harvest block, gates through
  plan-gate, applies skill and context changes). Notes live in the private
  `GFMCloud/personal-source-reviews` repo.

## 2026-08-20 - Weekly maintainer cycle 2

Second cycle of the `claude-improvements-weekly` maintainer. Pack bump: workbench
0.5.1.

- **transcript-scanner**: the agent may no longer fan its assignment out to nested
  sub-agents, and may no longer report its own work as running in the background. Both
  failure modes are observed, not hypothetical. On 2026-08-15 a scanner split a six
  file batch across nested agents and the caller received results for two of the six,
  noticing only by counting. On 2026-08-20 a scanner replied that its work was running
  in the background, produced no output file at all, and a nested child of that same
  call surfaced minutes later and wrote over the redo's output. Two writers, one path.
  Enforced twice over: a hard-rule section in the body, and `disallowedTools:
  ["Agent"]` in the frontmatter, because a rule in prose can be reasoned around and a
  tool the agent does not have cannot. An assignment too large to finish is now
  reported as named partial coverage instead.
- **phased-harness 1.2.2**: the skill no longer tells every harness it scaffolds to
  read its standing-authorizations markdown table with `turn-reduction:standing-authorization`.
  That skill's `authz.py` calls `json.load` and rejects the table with "authorization
  file is not valid JSON", so the instruction could not be carried out by any harness
  the skill has ever produced. Both sites that made the claim, `SKILL.md` and
  `templates/CONFIG.template.md`, now say that the table is the human-readable
  authority `/phase` reads directly, and that a project wanting the `check`/`validate`
  tooling also keeps `authorization.json` at its root, copied from that skill's
  example. The table is declared the winner if the two ever disagree.
- **capability-index**: the `_incubator` row listed eight skills against nine on disk.
  `scrollback` was added 2026-08-18 and was missing from both the table and the
  description, and `pipeline-foundry` was missing from the description. The row now
  matches `ls plugins/_incubator/skills` exactly, checked as a sorted set rather than
  by eye.

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
