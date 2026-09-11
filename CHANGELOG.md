# Changelog

Behavior changes only — not wording tweaks. Newest first.

## 2026-09-11 - AI workflow toolkit: eight skills across three packs (toolkit-build branch)

Pack bumps: foundry-core 0.3.0, verification-kit 0.1.0 (first version field on a
manifest that never had one), workbench 0.10.0. Source: toolkit-build-harness Phases 3
and 4, executing the AI workflow toolkit roadmap items T1 to T8. Every skill ships as
incubator with a fixture-proven deliberate failure and an authored eval suite; eval
execution is deferred to the weekly maintainer (`claude plugin eval` is early-access
gated on this account). Each passed an independent opus review after a sonnet build.

- **goal-spec (foundry-core, new):** turns an open-ended ask into a Goal block v1 with
  a runnable check or criterion-separated rubric, a recorded baseline, and a named
  human gate; refuses when no check can be named. `goal-block-check.sh` fails a block
  with a missing field.
- **bounded-loop (foundry-core, new):** script-based Stop hook that runs a goal's
  check itself, blocks failing turns with the real output, guards against test-file
  edits, and escalates with a structured report at a fixed attempt budget (default 3).
- **smoke-gate (verification-kit, new):** generates a smoke script from a Smoke
  manifest v1, proves every assertion category by poisoning it to exit 1, refuses a
  manifest missing any category's poison, then runs live for exit 0.
- **review-pair (verification-kit, new):** independent pass/fail verdict on a change
  spec from a read-only reviewer subagent that never sees the builder's context;
  `verdict-check.sh` rejects a verdict missing a field and holds on a repeat fail.
- **site-review (verification-kit, new):** Lighthouse, linkinator, viewport and dark
  screenshots, content checklist; scored before/after table with a fix phase under
  `/goal` re-scored by review-pair.
- **handoff 0.2.0 (workbench):** resume mode with Typed claim v1 blocks; a new session
  verifies each checkable claim against the live tree before continuing, and
  `check-claims.py` fails on a mismatch.
- **schedule-harness (workbench, new):** scaffolds a Scheduled-task pointer v1 plus
  absolute-limits block for running one `/phase` mode on a cadence; never registers
  the task or writes under `~/.claude/`. `check-pointer.py` fails a pointer with a
  relative path or no retry cap.
- **change-watch (workbench, new):** registered check with a seen-index that reports
  only on a state transition; a re-fire in the same state produces no report, and an
  unclassified action is refused.
- **`docs/toolkit-interface-spec.md` (new):** the ratified interface spec every shape
  above is defined in (Goal block v1, Escalation report v1, Verdict v1, Typed claim v1,
  Smoke manifest v1, Scheduled-task pointer v1, Seen-index entry v1, scored table, eval
  suite layout), moved into the library from the build harness so the skills' citations
  resolve for a plugin consumer. Skills cite it by name and section; none restates a
  field list.

## 2026-09-11 - contract sections: standard, template, validator (toolkit-build branch)

No pack bump (repo standard, template, and validator only). Source: toolkit-build-harness
Phase 1, executing the AI workflow toolkit roadmap item T0. Branch `toolkit-build`, one PR.

- **`docs/authoring-standard.md`:** new "Contract sections" rule: every SKILL.md carries
  `## Inputs`, `## Verify`, `## Done when`, `## Stop when`, in that order, with at least one
  stop condition that is not "done". Stable skills fail without them; incubator skills warn.
  Known weakness stated beside the rule: presence is checked, quality is not.
- **`templates/SKILL.template.md`:** the four sections with one-line placeholders.
- **`scripts/validate-skills.sh`:** F14 (missing section), F15 (out of order), F16 (vacuous
  Stop when) for stable skills; W4, W5, W6 for incubator. Headings are matched on their own
  line in the body, never in prose. Proven by a stable fixture missing `## Stop when`
  (exit 1) and the same fixture as incubator (warning, exit 0).

## 2026-09-11 - stable backfill: contract sections on every stable skill (toolkit-build branch)

No behavior change in any skill; the four sections name inputs, checks, and stop
conditions that were already in each body. Pack bumps land in Phase 5 of the same branch.

- **identity-resolution 1.0.1:** contract sections added, no behavior change.
- **evidence-report 1.1.1:** contract sections added, no behavior change.
- **proof-of-work 1.1.1:** contract sections added, no behavior change.
- **capability-preflight 1.1.1:** contract sections added, no behavior change.
- **output-lint 1.0.1:** contract sections added, no behavior change.
- **standing-authorization 1.1.1:** contract sections added, no behavior change.
- **phased-harness 1.2.5:** contract sections added around its existing "Done when", no
  behavior change.

## 2026-09-10 - phased-harness 1.2.4 and sweep-harness: two template lessons and an advisory worker field

workbench 0.9.5. Source: claude-improvements-weekly ratify 2026-09-10, executing the
2026-09-03 rulings Q-2026-09-03-29 and Q-2026-09-03-27 part 2 (blocked a week by a dirty
tree). Local commit only.

- **phased-harness 1.2.4:** the phase runbook template's supersession step now verifies
  the rename with `find <root> -name '*.superseded'` and forbids `grep` for the suffix
  (ignore-file-aware wrappers drop hits silently); its final-phase block now places any
  generated catalog or inventory regeneration in the final phase after the last content
  edit, with the `--check` as part of Gate B. SKILL.md's evidence discipline names both.
  Both defects were met live by the taste-skill-merge harness and never reached the
  templates.
- **sweep-harness (incubator):** `WORKER.template.md` step 4 and the item-state template
  gain an optional, advisory "what would have made this item cheaper or more reliable"
  line, written into the item's own state file. The orchestrator reads it at triage and
  never acts on it automatically.

## 2026-09-08 - prove-hooks.sh scores WARN-only hooks and indexes fixtures per matcher

No pack bump (repo scripts and fixtures only). Source: claude-scout-weekly hooks runbook Step 5
(evidence-guard, oops-i-did-it-again rows 2, 4, 5), run on Graham's instruction. Local commit only.

- **`scripts/prove-hooks.sh`:** a fourth verdict, `warn` (additionalContext with no
  permissionDecision); a fixture declares `"positive_verdict": "warn"` for a WARN-only hook and
  its positives must warn, never deny. The fixture index now counts hooks per (event, matcher)
  across every settings entry, so two Bash hooks are `PreToolUse__Bash__0.json` and
  `PreToolUse__Bash__1.json` and never share a fixture (the old single-entry index would have
  proved both against the first). Proven by deliberate failure: the evidence-guard command
  replaced by `true` came back RED on all 17 positives, "expected warn".
- **`scripts/prove-hooks.d/`:** `PreToolUse__Bash.json` renamed `PreToolUse__Bash__0.json`;
  new `PreToolUse__Bash__1.json` for `~/.claude/hooks/evidence-guard.py` (17 warn positives,
  17 negatives, `born` 2026-09-08).

## 2026-09-08 - replay-hooks.py: a hook's fire rate on real history is the second proof

No pack bump (a repo script, no plugin body changed). Source: claude-scout-weekly
`docs/runbooks/2026-09-07-replay-hooks.md`, run on Graham's instruction; oops-i-did-it-again
review rows 1 and 6 (ruled Q-2026-09-07-8). Local commit only.

- **`scripts/replay-hooks.py`** (new): runs a registered hook command over every Bash (or
  Read) tool_use in a COPY of Claude Code transcripts and prints counts and rates per rule,
  split at the fixture's `born` date, with a NOISY flag above 5 fires per 100 commands. It
  refuses `~/.claude/projects` as input, refuses a fixture without `born`, and prints no
  command body, path, or session id. Proven by a planted transcript built from the
  deny-destructive fixture (40 commands: 23 denials, 17 silent, per-rule counts exact) and
  by the refusal control.
- **`scripts/prove-hooks.d/*.json`** carry `born` (added 2026-09-07 with the hooks runbook);
  `prove-hooks.sh`'s header names replay-hooks.py as the second proof.

## 2026-09-07 - hooks runbook run: prove-hooks.sh takes control lists, env, and born dates; llama-offload marker protocol

Pack bump: workbench 0.9.4. Source: claude-scout-weekly `docs/runbooks/2026-09-03-hooks-and-permissions.md`
run on Graham's instruction (Steps 1, 2, 4; Step 3 in part; Step 5 gated on replay-hooks.py).
Local commit only.

- **`scripts/prove-hooks.sh`:** a fixture's `positive` and `negative` may be lists (every
  positive must deny, every negative must allow); a fixture-level `env` is exported to the hook;
  a `born` date is documented for `replay-hooks.py`; three more placeholders (`{{TMP_ENDASH}}`,
  `{{TMP_LARGE}}`, `{{TMP_SUPERSEDED}}`). Proven by deliberate failure: a candidate settings
  file with the Bash hook replaced by `true` came back RED on all 23 positives.
- **`scripts/prove-hooks.d/`:** `PreToolUse__Bash.json` (23 positives, 17 negatives for
  `~/.claude/hooks/deny-destructive.py`), `PreToolUse__Read.json` (the llama-offload router,
  `~/.claude/hooks/route-large-read.py`), `PreToolUse__Artifact.json` widened to en dash and
  the `.superseded` exemption for `~/.claude/hooks/dash-gate.sh`. The hook scripts live in
  `~/.claude/hooks/`, outside this repo; the fixtures here are their proof.
- **`llama-offload`:** step 1 writes `~/.claude/state/llama-offload-active` and step 6 removes
  it; while it exists, a plain Read of a file over 200 KB is denied and routed here.

## 2026-09-07 - retro owns recurrence: third occurrence of a failure class is a mechanism failure, not a fourth rule

Pack bump: workbench 0.9.3. Source: claude-scout-weekly `/phase ratify` Q-2026-09-07-9 (Graham:
`retro` owns the "a mistake just happened" trigger), oops-i-did-it-again row 7. Local commit only.

- **`retro`:** section 3 gains a recurrence check before routing: read earlier retros for the
  same failure class; on the third occurrence the destination is a statement that the mechanism
  holding the existing rules is failing, with those rules named, never another rule on top.
  The global CLAUDE.md is untouched; no new always-loaded line.

## 2026-09-07 - scout ratify: clean room hides MCP tools; llama-offload gains four batch-hygiene rules

Pack bump: workbench 0.9.2. Source: rulings from claude-scout-weekly `/phase ratify` 2026-09-07
(Q-2026-09-07-5; spotify-shunt rows 2 to 5; trailofbits-coop row 5; oops-i-did-it-again row 8),
applied the same evening on Graham's instruction. Local commit only; rides the Thursday push manifest.

- **`source-intake`:** the clean-room command adds `--disallowedTools "mcp__*"`; `--restricted`
  leaves MCP servers visible, and three reviewers on 2026-09-07 could see the GitHub MCP.
  Proven by a reviewer asked to list its tools naming no `mcp__` tool.
- **`llama-offload`:** validate inputs before the batch (empty record fails loudly); check each
  response's `model` field against the request (silent fallback is a failure); temperature 0.1
  to 0.2 in the request body; per-item text that looks like a secret is shown before it is
  forwarded, never silently redacted or forwarded (Spotify shunt review).
- **`docs/authoring-standard.md`:** an enforcing skill or check lists its known weaknesses
  beside its rationale, at the same altitude (coop review).
- **`docs/reviews/2026-09-03-hstack/decisions.md`** row 7 carries a pointer to the
  oops-i-did-it-again Stop-hook loop brake for whoever builds the first Stop hook.

## 2026-09-07 - scout cycle 2: clean room gets a tool-layer boundary; model-effort-advisor learns Fable 5.1 and cache economics; prove-hooks.sh

Pack bump: workbench 0.9.1. Source: rulings from claude-scout-weekly `/phase ratify` 2026-09-03
(Q-5, Q-7, Q-8, Q-10; hstack rows 1, 4, 6; commerce-agents row 1), applied by the scout cycle
of 2026-09-07. Local commit only; rides the Thursday push manifest.

- **`source-intake`:** the clean-room command runs from the pinned source with
  `--restricted --permission-prompts none` (Claude Code 2.1.248 and 2.1.259), so the reviewer
  has no command tools and cannot prompt; proven by a reviewer answering `NO-BASH` while Read
  worked. Untrusted-content paragraph: an archive arriving with `.git` inside is cloned fresh
  or has `.git/config` read before any git command (core.fsmonitor hijack).
- **`model-effort-advisor`:** `model-catalog.md` gains a `claude-fable-5-1` section (routing
  advice, the three API constraints, the documented behavior differences from Fable 5);
  new `references/cache-economics.md` (1-hour Claude Code cache window, 0.025x reads on
  Fable 5.1, /compact before leaving, cacheTtl for long scanners, the /cost miss-cause
  field); `effort-sizing.md` measures cost per completed task, not per call.
- **`scripts/prove-hooks.sh`** (new) with `scripts/prove-hooks.d/` fixtures: runs a positive and
  a negative control against every command hook in a Claude Code settings file; a hook with
  no fixture, a missing hooks block, or an unexpected verdict is RED. Proven by deliberate
  failure on 2026-09-07 (corrupted pattern RED, unproven hook RED, no hooks block RED, live
  settings GREEN). The Thursday maintainer's Phase 0 calls it (H7).
- **`docs/authoring-standard.md`** and the validator header: structural checks parse
  frontmatter, never grep prose; a heuristic states its measured ceiling where it is
  implemented.

## 2026-09-07 - decks 0.2.2: cd-to-pptx proves editability with code; layout-critique names the tells

Pack bump: decks 0.2.2. Source: `source-intake` HARVEST of gnipbao/knowledge-cat-ppt-skill
(pinned 889c3dc, MIT); review record in `docs/reviews/2026-09-07-knowledge-cat-ppt-skill.md`.

- **`cd-to-pptx`:** the review playbook gains Step 2b, an object-inspection gate that runs
  before the visual pass. Three vendored standard-library scripts count native text shapes,
  pictures, charts and tables per slide, fail on image-only slides, and prove a text object
  can be edited with a reversible mutation probe against an unchanged original checksum.
  Punch-list items now carry a P0/P1/P2 severity next to the real-defect/artifact tag, and
  an object-inspection failure is a P0. Proven this session by the scripts' self-tests, a
  pass on the vendor's six-slide native deck, and a deliberate image-only deck failing both.
- **`layout-critique`:** checklist item 5 lists ten named machine-made-slide tells
  (gradient blobs, over-rounded floating cards, fake laptop frames) instead of the generic
  "decorative chartjunk" line alone.

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
