# Comparison: Buzzoni "Claude Loop Engineering" vs. the installed skill library

Candidate: `sources/buzzoni-loop-engineering.md` (Mr. Buzzoni / @polydao, X Article, pinned
2026-09-02, sha256 `12d990e5...`). Second opinion: `cleanroom-buzzoni.md`. Incumbents: the
`workbench` harness family, `foundry-core:proof-of-work` / `evidence-report`,
`deploy-ops:deploy-verify-fix`, `turn-reduction:standing-authorization` /
`capability-preflight`, `~/skill-library/docs/authoring-standard.md`, global
`~/.claude/CLAUDE.md`, and the live `~/work/claude-improvements-weekly` loop.

---

## 0. Ancestry: none found

Checked for a merge note, shared filenames, matching section structure, or byte-identical
passages. None exist.

- `/usr/bin/grep -ril "buzzoni\|loop engineering\|polydao"` over `~/skill-library`,
  `~/work/claude-improvements-weekly`, and `~/.claude/CLAUDE.md` returned nothing.
- `git -C ~/skill-library log --all --oneline | grep -i "loop\|goal\|VISION"` returned one
  unrelated hit (`deploy-verify-fix` migration commit, about a "deploy iteration loop," not
  this article).
- The two corpora don't even share vocabulary: the candidate's artifacts are `STATE.md`,
  `VISION.md`, `/goal`, `/loop`, a "verifier subagent"; the incumbent's are `STATE.md`,
  `CONFIG.md`, `docs/end-state.md`, `/phase`, `/sweep`, `/rulings`. Where the names overlap
  (`STATE.md`), the schemas differ completely (see §1, item 6) — convergent naming, not a
  shared source.

`phased-harness/references/doctrine.md` traces the incumbent's `STATE.md` pattern to a
specific internal incident (the 2026-08-09 skill-migration run); `sweep-harness`'s poisoned-item
rule traces to a different internal incident (2026-08-12, generalizing the same migration's
"two agents appending to one tracker only worked by luck" near-miss). The candidate cites
Karpathy, Osmani, Rajasekaran, and Stripe. Two lineages, independently arrived at nearly the
same shape (freeze a resume file, gate before the irreversible step, isolate parallel writers,
verify with fresh eyes) from different failures. This reframes nothing — it is not "what did
each side learn since the fork," because there was no fork. It is a straight comparison
between two systems that happen to have converged.

---

## 1. Cleanroom spot-checks

Per instructions, spot-checked rather than trusted wholesale. Checked:

1. **The "13 techniques" count.** Confirmed: the cleanroom's §3 lists exactly 13 numbered
   items, quoted, sourced to specific lines in the article.
2. **Item 8's quote** ("Give parallel agents `isolation: worktree`... Let the builder run
   fast and cheap, and hand the reviewer the slower, stricter model") — verified verbatim
   against the article, line 455. Exact match.
3. **The 17,022-skill / 520-leak claim** — verified verbatim against line 605: "Auto-installed
   community skills bring along whatever sits in their descriptions, and one audit of 17,022
   skills found 520 leaking credentials." The cleanroom's flag ("a precise, alarming, entirely
   unsourced number... Do not cite this") is correct — no link, no audit name, nothing.
4. **The "cost per accepted change" quote** (item 12) — verified against lines 643–645, exact
   match including the 50%-survival threshold.
5. **The six-step build order** (item 4) — verified against lines 422–432, exact match; the
   cleanroom's ellision is faithful to the original meaning.
6. **Flag section G** (page furniture — Reuters/Al Jazeera/DraftKings trending items) —
   confirmed these appear at the tail of the scraped file (lines 830–895) and are unrelated to
   the article; correctly excluded from analysis in both this document and the cleanroom's.
7. **No prompt injection.** Independently confirmed on a full read: nothing in the article
   addresses a reviewing agent, claims prior authorization, or asks anything to be installed
   without the reader's deliberate action. Agrees with the cleanroom's finding.
8. **Em dashes.** Ran a byte-level check for the em-dash character across the whole source
   file: zero occurrences. The cleanroom didn't check this (it's not in its rubric); worth
   noting for §4 below, since it means the em-dash rule isn't the problem with this source —
   mannered prose is (see §4).

No cleanroom claim was found to be wrong in this spot-check; the cleanroom's rubric and
citations hold up under re-reading.

---

## 2. Classification of every technique

The cleanroom's §3 lists 13 items; one further concrete technique (item 14) was found in the
article that the cleanroom's technique list omitted (it appears in the claims tally as #61–65
but wasn't extracted as an actionable item).

### Item 1 — Put verification in a durable skill file, not the prompt

> ```
> 1. start the dev server, open the edited page
> 2. click the new control, confirm the state change, screenshot before/after
> 3. browser console: zero new errors or warnings
> 4. run a performance trace, audit Core Web Vitals
> if any step fails, fix it and rerun from step 1
> ```
> "The more measurable those steps are, the less room Claude has to talk itself into
> finishing early"

**INGESTIBLE FRAGMENTS.** The general move — write verification down as a persistent,
checkable artifact instead of ephemeral prompting — is already thoroughly covered, and more
rigorously, by `foundry-core/skills/proof-of-work/SKILL.md`:

> "An artifact is not done because it looks done. It is done when there is executed evidence
> attached... Verify at the level the failure lives. A check that structurally cannot see the
> defect is not a check, however green it comes back."

and by `deploy-ops/skills/deploy-verify-fix/SKILL.md`'s verification table ("The deploy tool
printed success | The thing responds at its real address"). Both are general (code, document,
deployment, data, config) and grounded in three named, dated real incidents
(`anthropics/claude-code` issue #53948, a marketplace-update false-success, a plugin-validate
false-green) rather than one hypothetical.

**Fragment worth taking:** deploy-verify-fix's table is generic — it never says what "verify
at the level the failure lives" looks like for a *frontend* change specifically. The
candidate's four concrete steps (start server → click → screenshot → console-check → Core Web
Vitals trace) are a genuinely more specific worked example than anything currently in the
incumbent set for that one case.

**What it improves / target:** `deploy-ops/skills/deploy-verify-fix/SKILL.md`, the
verification table — add one row or a short worked sub-example for "UI/frontend change,"
using the candidate's four steps as the content, rewritten to the library's rule shape (scope,
action, exception, verification) rather than pasted as prose.

---

### Item 2 — Program-checkable goal conditions, paired with "the evaluator sees only what surfaced in conversation"

> "*all tests in test/auth pass and the lint step is clean* holds up across twenty turns.
> *The code looks clean* collapses on the first one." / "it can only judge what Claude
> surfaced in the conversation, because the evaluator runs nothing itself."

**REDUNDANT.** `phased-harness/SKILL.md`'s fit test requires a "nameable invariant... stated
as a state, not a task list" that is "testable by inspection at any moment, by anyone, without
knowing the project's history," and every generated phase runbook's "Done when" section
insists on "an observable state, not 'did the work.'" `sweep-harness`'s `WORKER.template.md`
requires "the specific, executed evidence that proves this item is finished. State the command
or inspection, not 'looks right.'" This is the same principle, applied library-wide, not to
one product feature.

The second half of the quote — "the evaluator runs nothing itself" — is a *limitation* of
Claude Code's `/goal`, not a design choice worth importing. If taken as doctrine for how *our*
verifiers should work, it directly contradicts `verification-kit:pre-delivery-verifier` and
`proof-of-work`, both of which require a verifier to *act* (run the code, hit the endpoint),
not just read a transcript. Flagged under §4 (corrections needed) rather than imported.

---

### Item 3 — Cap the goal explicitly (`/goal ... stop after 5 tries`)

**REDUNDANT — incumbent is measurably better.** A flat retry cap can't distinguish a
genuinely converging 6th cycle from a stuck 2nd cycle. `deploy-ops/skills/deploy-verify-fix`'s
stop condition is information-based, not count-based:

> "Three consecutive cycles fail and the last produced no new information. The information
> test is the real one — ten cycles each revealing something are fine; two identical ones are
> a loop, not iteration."

This is a strictly better stop rule than "stop after 5 tries": it won't kill a loop that's
making progress on cycle 6, and it won't let a loop burn 5 identical, informationless cycles
before stopping.

---

### Item 4 — Build in this order (manual run → skill → state file → gate+cap → schedule → verifier subagent)

**REDUNDANT — and the incumbent has lived evidence, not an anecdote.** Every harness in the
`workbench` family opens with exactly this shape (fit test → interview → scaffold → generation
rules → done-when), and `~/work/claude-improvements-weekly` is a running instance built in
almost this literal order over four real cycles. Its `STATE.md` records the payoff of step 6
(the verifier subagent) directly, with dates and commit-level detail the candidate's anecdotes
never carry:

> "Three of four Tier 2 changes were built, failed independent verification, and were reverted
> rather than repaired... The most useful thing that happened: nothing this harness measures
> mechanically would have caught any of them, which is recorded as S-30 and is the single
> strongest argument for the fresh-context verifier being non-optional." (`STATE.md`, cycle 3
> entry)

That is the candidate's claim, proven against a real system with real commits, rather than
asserted about Karpathy's unlinked repo.

---

### Item 5 — Fire a named skill from the schedule, never pasted instructions

> "Have the schedule fire a named skill rather than a wall of pasted instructions, because
> instructions inside a cron job never get updated by anyone, ever."

**REDUNDANT in principle — and the incumbent states it more strongly.** Global
`~/.claude/CLAUDE.md`, Duplication and reversibility: "Every rule, skill, and document has
exactly one editable home. Mirrors, plugin caches, and generated copies are read-only; an
editable duplicate is drift, so flag it rather than silently keeping both." `phased-harness`'s
"Compose, don't duplicate" section says the same for generated harnesses: "Reference them by
name; do not copy their content into the harness."

**But direct inspection found the live system currently violates its own rule, in exactly the
shape the article warns about.** `~/.claude/scheduled-tasks/claude-improvements-weekly/SKILL.md`
is a hand-restated copy of the dispatch logic — not a one-line pointer to the project's own
`/phase` skill. Diffing it against the canonical dispatch skill,
`~/work/claude-improvements-weekly/.claude/skills/phase/SKILL.md` (version 1.1.0, reviewed
2026-08-28):

- The canonical skill documents four modes: no-argument (full cycle, with a **same-day rule**
  ruled 2026-08-28), `N` (single phase), `publish` (the push gate), and `ratify` (the Tier-3
  queue walk).
- The scheduled-task copy documents **one** mode only ("Do exactly this, in order: 1... 2...
  3... 4. Execute the runbooks in order") and has no mention of `publish`, `ratify`, the
  same-day rule, or any argument handling at all.

This is not a hypothetical drift risk — it is a *found* instance, live on this machine, of
the candidate's own warning ("instructions inside a cron job never get updated by anyone,
ever"). See §4 for the correction and §5 for the recommended fix.

---

### Item 6 — Copyable state-file shape

**REDUNDANT — incumbent is richer and already proven at scale.**
`phased-harness/templates/STATE.template.md` covers everything the candidate's example does
(a "Last run" analog via the phase tracker, "in progress" via the tracker, "escalated to
humans" via Anomalies/Open items) plus three things the candidate's template lacks entirely:
a **Decision log** (with the explicit rule that overridden proposals' side effects must be
reassigned, never silently dropped), an **Evidence** section requiring "the command run and
its actual output," and an **Open items** section requiring every closing gap to name an
owner before the harness may close ("'Nobody owns this' is a legitimate destination only when
it is written down as one"). The live `claude-improvements-weekly/STATE.md` — 300+ lines,
four cycles of real history, a rulings log, a settled-ground table — is a materially more
mature instance of the same idea than the candidate's four-line example.

---

### Item 7 — Split position (`STATE.md`) from destination (`VISION.md`)

> "pair the state file with a standing VISION.md. STATE.md holds the position, VISION.md
> holds the destination, and the second one is what stops goal drift around turn 47"

**REDUNDANT — and mandatory, not optional.** `phased-harness/templates/end-state.template.md`
is exactly this artifact, required on every project, not just "long runs":

> "This document is the contract the project works toward. When any instruction in `CLAUDE.md`
> or a phase runbook is ambiguous, this doc is the tiebreaker."

It's also considerably more developed than a one-line VISION.md: it includes the invariant
statement, a "why this shape and not the alternatives" section explicitly designed to stop a
later session from "'helpfully' regressing to a rejected design," a target layout, a rules
table, and an enforcement section. "Turn 47" in the candidate is a rhetorical number with no
mechanism behind it; the incumbent's "Constitution conflict is a stop, not a tiebreak" rule
(`phased-harness/SKILL.md`) is a mechanism: any phase whose plan collides with the invariant
must stop and log it, full stop, regardless of what turn it happens on.

---

### Item 8 — Isolate parallel agents; asymmetric models

> "Give parallel agents `isolation: worktree` so two of them can never write the same file...
> Let the builder run fast and cheap, and hand the reviewer the slower, stricter model"

**REDUNDANT — and the incumbent's reasoning is sharper.** The collision-prevention half is
generalized past git worktrees specifically: `sweep-harness/SKILL.md` gives every worker "a
target only it will ever write," proven against a real near-miss, not a hypothetical:

> "Two agents writing the same file concurrently produce a file that is neither agent's
> version. This is not a hypothetical, it happened during the skill-migration run this harness
> generalizes from... two agents appending to one tracker only worked by luck."

The asymmetric-model half is covered by `model-effort-advisor/references/subagent-routing.md`'s
Build/Review Pairing section, which goes further than "give the reviewer a stricter model" —
it identifies *why* same-context review fails and prescribes the fix:

> "Hand the review agent the artifact and the success criteria only, never the build agent's
> reasoning or rationale. A persuasive explanation of why a choice was made is exactly the
> channel through which a bad choice gets waved through; the reviewer judges what was
> produced, not why."

The candidate never makes this point (context contamination, not just model tier) even though
its own §4 on Rajasekaran's evaluator gestures at the same failure mode without naming the
mechanism this precisely.

---

### Item 9 — Four-part go/no-go filter before automating anything

**REDUNDANT — instantiated four times, with routing, not just refusal.** Every harness in the
family opens with a mandatory "Step 1: Fit test" of this exact shape (all-conditions-must-hold,
then "Decline, and say why, when:"). `phased-harness`'s is the clearest example:

> "Build a harness only when all four hold... State the failing criterion plainly, then route
> in the same breath rather than leaving the user at a dead end: Multi-session and reversible,
> no irreversible finish: hand to `workbench:handoff`... Neither: build it directly, and say
> so."

The candidate's filter stops at "don't automate this" with no next step. The incumbent's
version always names where the declined work should go instead.

---

### Item 10 — Make the evaluator act, not read

> "The verdict moves from 'the JSX looks fine' to 'I clicked login, it navigated, here is the
> screenshot.'"

**REDUNDANT — and better evidenced.** `proof-of-work/SKILL.md`'s entire second half is this
exact point, backed by three named, dated, real incidents rather than one anecdote about one
engineer:

> "Where a tool reports its own outcome, confirm the outcome independently by inspecting what
> it claims to have produced... Instance 3 is the one worth internalising. The check passed
> *because* it was run at the wrong level, and a passing check at the wrong level is more
> dangerous than no check at all — it converts an unknown into a false known."

By this report's own evidence standard (and the global CLAUDE.md's "Evidence over assertion"
rule), the incumbent's version is simply better sourced: three logged, reproducible incidents
with issue numbers versus one named-but-unlinked engineer's account.

---

### Item 11 — Put security scanning inside the gate

**REDUNDANT — already practiced live, not just stated.** Global CLAUDE.md: "`.gitignore` is a
floor, not the check: secret-scan before every commit, and a hit is a hard stop, not a
warning." `claude-improvements-weekly/CLAUDE.md`: "Every auto-applied change is self-verified
before commit: validator green from the repo root (skill-library), secret scan clean..." — and
`STATE.md`'s settled ground shows this actually firing (S-32, a cleartext token found and
ruled on, not silently ignored). Minor gap noted, not promoted: the candidate names SAST and
dependency-audit explicitly; the incumbent's secret-scan discipline doesn't extend to those by
name anywhere read. Too generic and too far from this machine's current CI shape to be worth a
harvest row on its own.

---

### Item 12 — Measure one thing: cost per accepted change

> "Cost per accepted change... If fewer than half the changes your loop produces survive
> review, you are doing the review work the loop was meant to remove."

**COMPLEMENT.** No incumbent file — not `model-effort-advisor`, not any harness, not
`claude-improvements-weekly`'s own `CONFIG.md`/`STATE.md` — states a single north-star
efficiency metric for judging whether a recurring/gated automation is worth its overhead. The
raw material to compute one already exists: `claude-improvements-weekly/STATE.md` tracks
"Applied (Tier 1/Tier 2)" and "Reverted" counts every cycle (e.g., cycle 3: "3 Tier 1 applied,
1 of 4 Tier 2 applied... [3 of 4] passed the validator, the secret scan, and the em-dash check
first" before being reverted on independent verification) — an implicit acceptance rate is
already being generated and never named as a metric.

**Consumer on this machine:** `claude-improvements-weekly/prompts/phase-3-report.md`'s report
could add one line per cycle (applied ÷ (applied + reverted), or a token/subagent-call proxy
for cost) as a standing metric rather than counts alone; `model-effort-advisor/references/
decision-rubric.md`'s existing ablation-diagnosis section ("Diagnosing a skill or prompt that
underperforms") is the natural place to trigger on a metric like this dropping, rather than
someone noticing by eye.

---

### Item 13 — Choose the runtime from the task's physics (local `/loop` vs. cloud routine)

**REDUNDANT.** The underlying judgment — prove what a capability actually requires and
provides before assuming a deployment shape will work — is `capability-preflight`'s whole
purpose, and it is stated more skeptically than the candidate's version:

> "One session recorded its relays as 'structural under current tooling.' They were not: the
> device bridge existed and no folder had been connected... a capability may be declared
> unreachable only with a probe attached."

The live system already made the concrete call the candidate's heuristic would produce:
`claude-improvements-weekly` runs as a **local** scheduled task (`~/.claude/scheduled-tasks/`)
specifically because it needs to see local files (the skill library, the global config) — the
exact reasoning the article gives for choosing `/loop`-style local execution over a cloud
routine. But this was never written up as reusable doctrine anywhere in the incumbent set; it
exists only as one project's implicit correct choice.

The specific product-surface content this item leans on (cloud routine 1-hour minimum, desktop
scheduled task vs. `/loop` distinctions) is exactly what the cleanroom flags as highest
currency risk (§5, items 6–12 in its list) — unversioned command facts, not technique. Not
worth importing at that level of specificity; the durable kernel is already covered by
`capability-preflight`.

---

### Item 14 (found independently, not in the cleanroom's 13) — Deterministic context assembly before generation; a hard-coded gate the agent cannot bypass

> "A deterministic orchestrator assembles the context first - it scans the links in the
> message, pulls Jira, finds the docs, searches the relevant code through Sourcegraph and MCP.
> Only then does the agent start writing, with everything laid out. After it finishes, a
> hard-coded pipeline runs the linter and the agent cannot step around it." / "Anything a rule
> can decide never goes to a probabilistic model. Finding the materials is deterministic work,
> so deterministic code does it."

**COMPLEMENT (narrow).** The gate half — a check that cannot be talked around — is already
redundant against `capability-preflight`'s design (probes must be able to report failure;
`||`, `; true`, `set +e` are rejected at manifest-validation time specifically so a check
cannot be softened). But the *context-assembly* half is a genuinely different, unstated
principle: the article's claim isn't "gate the output," it's "don't even hand the model the
task of finding its own inputs when a rule can decide how to find them." No incumbent skill
states this. `model-effort-advisor/references/decision-rubric.md` frames every task as a
choice of *which* model tier to use — it never asks whether a step needs a model at all.

**Consumer on this machine:** `model-effort-advisor/references/decision-rubric.md` could gain
a zeroth question before the five-axis rubric: "could this step be plain deterministic code —
a lookup, a search, a fixed transform — rather than any model call?" This is a sharper,
more radical framing than the existing rubric's "match tier to task," and it's the one piece
of the Stripe Minions case study that isn't already redundant elsewhere.

---

## 3. Routing collisions

If the article's proposed artifacts were installed alongside the incumbents as-is:

- **A generic `STATE.md`/`VISION.md` pair**, scaffolded ad hoc rather than through
  `phased-harness`, collides directly with `phased-harness`'s own `STATE.md`/
  `docs/end-state.md` convention (different schema, same filename intent) and with
  `claude-improvements-weekly`'s already-proven `STATE.md` variant. Two schemas for the
  resume-point file in one ecosystem is exactly the "second editable copy" failure the
  Duplication rule in global CLAUDE.md exists to catch.
- **A verifier subagent** added under `.claude/agents/` with a generic name (e.g.
  "reviewer," "verifier") overlaps in purpose with `verification-kit:pre-delivery-verifier`,
  which `phased-harness`'s "Compose, don't duplicate" section already names as the harness
  family's verification pass. A second, independently-designed verifier installed without
  deference to the existing one reintroduces the exact ambiguity `subagent-routing.md`'s
  Build/Review pairing section is written to prevent.
- **A "verify-frontend-change"-style skill** would misroute against at least two existing
  descriptions under the authoring standard's own router-quality bar ("A description with no
  negative scope routes neighbouring requests to it"): `deploy-ops:deploy-verify-fix`
  ("Use for every deploy, staging or production") and `foundry-core:proof-of-work` ("Use
  before declaring any artifact complete, and whenever a tool reports its own success"). All
  three would plausibly fire on "verify this UI change is done." A new skill in this space
  needs explicit negative scope ("not for deploys, not the general evidence standard, only
  for pre-deploy local UI checks") to avoid three-way misrouting.
- **A `/goal`-shaped artifact** (a persistent "goal.md" or similar) doesn't collide by name
  with anything installed, but functionally duplicates `docs/end-state.md`'s "what does done
  mean, and is it the tiebreaker" role — installing both invites the same ambiguity a second
  `STATE.md` would.

---

## 4. Philosophy conflicts

The task named two specific comparisons to check. Both come back **no genuine contradiction**
— one is an omission the incumbent fills more strictly, the other is a live violation of a
rule both sides actually agree on.

**1. "A gate or validator is trusted only after being proven by deliberate failure" (global
CLAUDE.md) vs. the article's gate advice.** The article never states this. Its own gate
definition ("The gate - something with no taste that can reject the output... A test suite, a
build, a type check, a linter exit code") never requires proving that gate can actually fail.
The cleanroom independently flagged exactly this as the article's biggest failure mode: "A
gate that cannot fail... nothing instructs the reader to verify their check ever returns
non-zero." Confirmed on a direct re-read — no line in the article does this. This is an
omission, not a contradiction, and the incumbent's version is strictly more rigorous:
`sweep-harness`'s mandatory poisoned item ("The sweep is not proven correct until that row
lands in `failures.md` with a real failure recorded against it. If it lands as `done`, the
worker or the done-check is broken") and `phased-harness`'s deliberate-failure rule both
mechanize what the article only gestures at.

**2. "Instructions in a cron job never get updated by anyone, ever" vs. how the live weekly
loop is built.** Also not a contradiction in principle — the incumbent's own global rule (one
editable home; "Edit the generator, never the output") says the same thing, more strongly.
But direct inspection (§2, item 5) found the live loop currently **violates its own rule** in
exactly this shape: the scheduled task's `SKILL.md` is a hand-pasted, already-stale restatement
of the dispatch logic, missing the same-day rule and the `publish`/`ratify` modes that the
canonical `.claude/skills/phase/SKILL.md` has carried since 2026-08-28. The article is right
about the risk; this machine is a live example of it, found by testing rather than reading, in
keeping with the "Evidence over assertion" rule this very report is written under.

**No other real contradiction found.** Both sides push toward the same posture on the deeper
question of who keeps judgment: candidate — "You do not have to override it often. You do
have to stay capable of saying this is wrong"; incumbent (global CLAUDE.md) — "Never hand over
an artifact and then ask whether it worked; run the check yourself, and route to a human only
after establishing you genuinely cannot." They differ mainly in rigor and evidentiary grounding
(see §2 throughout), not in direction.

---

## 5. Corrections needed at ingest

- **Unsourced numbers are never imported**, per the global rule. This blocks essentially every
  empirical claim in the article from being cited even in passing in a doctrine.md-style
  grounding section: Karpathy's 700 experiments / 20 improvements, Shopify's 19%, Steinberger's
  8M views, the 17,022-skill / 520-leak audit, Stripe's 1,300 PRs/week, and the entire §11
  pricing section ($3k–8k, $500–1,500/mo, "$95k developer / $300k AI architect"). Per the
  cleanroom's own tally, roughly 6–8% of the article's ~86 claims are evidenced; the rest
  cannot be repeated as fact on this machine.
- **A rule a stateless model cannot honor if imported literally:** "the evaluator runs nothing
  itself, it can only judge what Claude surfaced in the conversation" (item 2). If mistaken for
  a design principle rather than a product limitation, it would silently downgrade this
  library's verification standard, which requires a verifier to act (`proof-of-work`,
  `verification-kit:pre-delivery-verifier`), not just read.
- **Mannered prose, in violation of the global no-mannered-prose rule.** Two clear instances:
  "The system plays no favorites. It is a multiplication sign, and you are the number"
  (metaphor substituting for a direct statement) and "Every few months another 'X engineering'
  shows up and everyone rolls their eyes. This one earns its place" — the phrase "earns its
  place" is a near-verbatim match for the CLAUDE.md's own banned example ("this point earns its
  keep"). Any imported fragment must be rewritten plain, not pasted.
- **Rule shape.** None of the article's advice is shaped as scope/action/exception/verification,
  the authoring standard's required rule shape (`~/skill-library/docs/authoring-standard.md`).
  It's aphoristic prose throughout. Every fragment taken in §6 below needs reshaping, not
  quoting, when it lands in a SKILL.md.
- **Em dashes: not an issue.** A byte-level scan found zero em dashes in the source file — the
  author already writes in the library's preferred style on this axis. Noted so nobody wastes a
  pass stripping em dashes that aren't there.
- **The article's own worked example violates its own stated principle.** Its "everything
  stacked" demo (§3, Proactive) — `/schedule every hour: ... /goal: don't stop until every
  report found this run is triaged, actioned, and responded to...` — has no cap, contradicting
  the article's own five-part definition of a loop two sections earlier ("The stop - the
  condition that ends the run, plus a hard cap for when the condition never arrives"). The
  incumbent's `standing-authorization` tooling would catch this class of defect mechanically:
  its `validate` step treats "a ceiling named in prose must be bound" as an error — "An action
  whose text says 'limit', 'cap', 'budget' or 'ceiling' without a `ceiling` key is an error."
  The candidate's own flagship example would fail that check.

---

## 6. Net assessment

Fourteen items assessed: **10 REDUNDANT** (the incumbent already covers the ground, usually
more rigorously and with real evidence rather than an anecdote), **2 COMPLEMENT** (items 12,
14), **1 INGESTIBLE FRAGMENTS** (item 1), **0 SUPERIOR SUBSTITUTE**, **0 outright DISCARD** as
a standalone top-level call (item 13's specific command surface is discard-level but folds
into a REDUNDANT verdict). This is expected, not a surprising result: the installed library was
built by people running exactly this kind of unattended, gated, multi-session work for months,
and it shows — its rules are grounded in named incidents with commit SHAs, not named engineers
with no links.

**If only three things could be taken:**

1. **Fragment — the concrete frontend-verification checklist (item 1).** Target:
   `~/skill-library/plugins/deploy-ops/skills/deploy-verify-fix/SKILL.md`, added as a worked
   sub-example under the existing verification table, rewritten into the library's rule shape
   rather than pasted. Why: it's the one piece of concrete, specific content in the whole
   article that fills an actual gap (deploy-verify-fix is currently generic about what
   "verify at the level the failure lives" means for a UI change specifically).
2. **Fragment — "could this be plain code, not a model at all" as a zeroth rubric question
   (item 14).** Target: `~/skill-library/plugins/workbench/skills/model-effort-advisor/
   references/decision-rubric.md`. Why: the existing rubric only ever asks *which* model tier;
   this is a genuinely sharper frame (no model at all, for the parts a rule can decide) that
   nothing else in the library states.
3. **Fragment — "cost per accepted change" as a named, tracked metric (item 12).** Target:
   `~/work/claude-improvements-weekly`'s Phase 3 report and `STATE.md` schema, and
   `model-effort-advisor/references/decision-rubric.md`'s ablation-diagnosis section as the
   trigger. Why: the raw data (applied vs. reverted counts) is already being generated every
   cycle and never named as a metric — this is the cheapest possible addition, pure
   bookkeeping on data that already exists.

Everything else in the article's technique list is legitimately **SKIP**: either already
covered, or covered better, by a library that has the evidentiary rigor this article's own
cleanroom review found largely missing from it (6–8% evidenced claims). The one thing worth
acting on immediately isn't from the candidate at all — it's the live drift found while
testing the candidate's own claim in §2/§4 (item 5): the scheduled task's `SKILL.md` at
`~/.claude/scheduled-tasks/claude-improvements-weekly/SKILL.md` needs to become a thin pointer
to the canonical `~/work/claude-improvements-weekly/.claude/skills/phase/SKILL.md` rather than
a hand-restated, already-stale copy of it.
