# Comparison: PostHog "Your AGENTS.md is holding you back" vs. installed set

**Candidate:** `sources/posthog-agents-md.md` — PostHog / Jina Yoon, X article, pinned
2026-09-02, sha256 `476068f76c43349c57f768c90f8f9804e1c90e7b9f79dce60e9ecc9c809a971f`.
**Clean-room review:** `cleanroom-posthog.md`.
**Incumbents read in full:** `~/skill-library/docs/authoring-standard.md`; `workbench/skills/retro/SKILL.md`;
`workbench/skills/rulings-harness/SKILL.md` + `references/doctrine.md` + all four
templates; `workbench/skills/sweep-harness/SKILL.md` + `references/doctrine.md` + all
six templates; `workbench/skills/skill-discovery/SKILL.md`;
`workbench/skills/fable-project-review/SKILL.md`; `workbench/skills/source-intake/SKILL.md`
+ all four `references/` + both `templates/`; `workbench/skills/handoff/SKILL.md`;
`verification-kit/skills/fact-currency-check/SKILL.md`; `~/.claude/CLAUDE.md`; plus the
top-level docs of `~/work/claude-md-consolidation/` and `~/work/claude-improvements-weekly/`
as context.

## Ancestry

None. `grep -ril` across `~/skill-library` for "posthog", "jina yoon", "wizard-ci",
"context-mill", "commandments.yaml", "pr-evaluator" returned zero hits, and no
CHANGELOG entry names PostHog, Jina Yoon, or "AGENTS.md". The two artifacts are
independent: no merge note, no shared passages, no matching section structure. This
machine's context-maintenance apparatus (`rulings-harness`, `sweep-harness`, `retro`,
the two running harnesses) was designed and shipped in August–September 2026 with no
visibility into this article, and the article shows no sign of familiarity with any of
it. Every classification below is convergent-evolution comparison, not fork comparison.

## Spot-check of the clean-room review

Checked seven of the review's verbatim quotes and two of its paraphrased claims
against the article text directly:

- Deletion heuristic (review §3.1) — exact match, article line 161.
- `failures.md` box (review §3.2) — exact match, article line 227.
- End-of-run prompt (review §3.3) — exact match, article line 243.
- Wizard-ci three-step loop (review §3.4) — faithful paraphrase of lines 190–198.
- "cluster and verify" / subagent-verify (review §3.6) — exact match, lines 263 and 273.
- PR-template attribution (review §3.7) — faithful paraphrase, lines 281–285.
- Cherny six-months (review §3.8) — exact match, lines 91–93.
- Claim #14 (`/doctor` output block, `Est. resident tokens: ~1,780`, `Verdict: trim ~350`) — exact match, lines 131–139.
- Claim #17 (21-hour merge-queue incident) — matches lines 149–157, and the review correctly flags that the specific durations (10 hours, 45 minutes) are not independently sourced beyond the prose.

No errors found. One judgment call worth surfacing rather than treating as fact: the
review's executive summary says the merge-queue incident is "filed under 'subtract
more'." That's a reasonable reading — the incident sits in the same section as, and
directly precedes, the deletion Try-this box — but the incident itself is presented in
the article as evidence that `/doctor` "doesn't check for correctness," which is a
narrower framing than "subtract more." I'm treating the review's broader reading as
correct because the Try-this box is what a reader actually walks away with, but it's
an interpretive claim, not a quoted one. Everything else checked was a direct,
accurate transcription.

---

## Classification of the eight listed techniques, plus one more found

### 1. The deletion heuristic — SUPERIOR SUBSTITUTE (incumbent wins after correction)

> "Run claude doctor after each upgrade and follow up with a manual pass on your
> AGENTS.md. For each line, if you can't name the failure it prevents, delete it."

`rulings-harness` does the same job — deciding what stays in a context file — with a
three-way test instead of a binary one, and it is measurably better at the exact
failure mode the clean-room review flags. Compare:

> Article: "if you can't name the failure it prevents, delete it."

> `rulings-harness/references/doctrine.md`: "'Don't auto-run `open <file>.html`' has
> no evidence that could overturn it; it is a standing choice about behavior, not a
> measurement. It stays a preference, in CLAUDE.md, forever."

The incumbent explicitly protects the class of line the article's heuristic would
delete: a preventive rule with no attached incident, because its value is that the
incident never happened. `rulings-harness/SKILL.md` states the boundary test
("**It cost something to determine, and a future session would otherwise re-derive or
violate it.**") and sorts everything into `Preference` (kept forever, no evidence
needed), `Ruling` (falsifiable, expires), or `Burn-derived` (incident-backed, no
falsifier) — a strict superset of the article's binary keep/delete that avoids
inverting the burden of proof the way the article's version does. What would have to
change for the article's version to be adoptable as-is: replace the single yes/no
test with the three-way classification and add the `Preference` escape hatch; as
written, it is not safe to run.

### 2. "Test your context like it's code" (evals / `failures.md`) — REDUNDANT

> "Every time you update your context to address an agent's mistake, capture what
> caused it in the first place as an eval... The next time your agent makes a mistake,
> paste the prompt that caused it into a failures.md. Re-run those prompts the next
> time you edit or delete parts of your AGENTS.md as a quick test suite."

`authoring-standard.md` already mandates this, more rigorously:

> "Once a skill has eval cases, they run on any change to that skill, its hooks, or the
> CLAUDE.md it depends on, because that configuration steers the agent and deserves the
> regression testing code gets. A change that drops the pass rate is reviewed before it
> merges, not after."
>
> "A change made to fix a failing case is tested on two sets: the boundary set (the
> case or cases that prompted the change) must improve, and the retention set (every
> case that already passed) must not regress. Showing only the second is how a change
> that fixed nothing gets merged."

The article's version is one set (failing prompts, re-run); the incumbent requires
two (boundary AND retention), which is exactly the discipline that prevents a
context-file fix from silently breaking something that used to work — a failure mode
the article never names. Caveat worth recording, not a reclassification: the
incumbent rule is currently unexercised — `authoring-standard.md` itself notes "zero
eval cases in the library" as of 2026-09-02 — while PostHog's `failures.md` is
described as a running practice. Design superiority, not yet field-proven superiority.

### 3. The end-of-run feedback prompt — COMPLEMENT

> "What information or guidance would have been useful to have in the integration
> prompt or documentation for this task? Specifically anything that would have
> prevented tool failures, erroneous edits, or other wasted turns."

Nothing on this machine asks an agent this question, proactively, as a standing final
step of a task. `retro` is the closest thing and it deliberately does the opposite:

> `retro/SKILL.md`: "By the time a retro gets written, your context may already be
> compacted. You are not a reliable narrator of your own session, you will report the
> tidy version, not what actually happened. Ground every claim in the record... **Do
> not read the transcript yourself.**"

`retro` refuses self-report and requires transcript-grounded evidence instead; the
article leans into self-report and compensates downstream (see item 6) rather than at
the source. That is a genuinely different, complementary layer, not a competing one:
`retro` is post-hoc and single-session; the article's prompt is inline and per-task,
producing a stream of signal `retro` never generates because `retro` only fires when
its gate (commit / failure / decision) is met. The gap: no mechanism here captures
"what would have helped" at the moment a task ends, only after the fact and only when
a session crosses `retro`'s bar. Nothing currently consumes this signal, but
`sweep-harness`'s per-item `WORKER.md` cycle is a natural consumer — it already runs
one task per item, has a "write state file" step, and nothing in that step today asks
this question.

### 4. The full wizard-ci → pr-evaluator loop — INGESTIBLE FRAGMENTS

> "1. wizard-ci runs the PostHog Wizard on all ~40 sample apps and creates one PR for
> each. 2. Those PRs don't get merged. Instead, a second agent called the pr-evaluator
> grades each of them based on the diffs and session logs. 3. The pr-evaluator leaves
> metrics and reports on the trigger PR and the wizard-ci PR."

The overall shape (enumerate N items, dispatch treatment, collect results, report) is
already `sweep-harness`'s job, and the "cannot claim done at scale" problem the loop
solves is already solved there via the mandatory poisoned item — a stronger guarantee
than PostHog's approach, which has no analogous deliberate-failure proof that
`pr-evaluator` actually catches a bad diff. The article's shape as a whole is
REDUNDANT with `sweep-harness` + `verification-kit:pre-delivery-verifier` composed
together (the composition is already documented: `claude-improvements-weekly/CLAUDE.md`
uses "a `verification-kit:pre-delivery-verifier` agent for Tier 2" for exactly this
role today). One fragment is sharper than the current template, though:

> Article: "a second agent called the pr-evaluator grades each of them based on the
> diffs and session logs" — grading is structurally separated from doing.

> `sweep-harness/templates/WORKER.template.md`: "## 3. Check done \`<PER-ITEM DONE
> CHECK: the specific, executed evidence that proves this item is finished... \`"

`WORKER.template.md`'s own done-check is self-graded — the same agent that did the
treatment also decides whether it passed. That is a real gap: nothing in the generic
sweep template requires or even suggests a second, independently-instructed grading
pass, even though this machine already has the tool for it
(`verification-kit:pre-delivery-verifier`) and already uses it elsewhere. This
fragment — pairing an independent grader with the worker's self-check, for sweeps
where the stakes justify it — improves `WORKER.template.md` §3 and
`dispatch-SKILL.template.md` §5–6 specifically. It replaces nothing (self-check stays
as the cheap default) and adds an optional second gate.

### 5. The scaled-down eval technique ("test your context by saving prompts...") — REDUNDANT

> "test your context by saving prompts that check if your agents are doing what you
> want them to do."

This is the portable restatement of item 2. Same incumbent, same verdict: covered
as-or-better by `authoring-standard.md`'s eval-case rule (see item 2's quotes). Not a
separate finding.

### 6. Verification before action ("cluster and verify") — REDUNDANT

> "since we can't trust agents at face value, we cluster and verify the underlying
> issues first... Once the loop identifies a meaningful cluster, it deploys subagents
> to verify the issue before attempting a fix."

`claude-improvements-weekly` already runs this pattern, machine-wide, weekly, with a
tighter guarantee than "deploys subagents to verify":

> `claude-improvements-weekly/CLAUDE.md`: "Every auto-applied change is self-verified
> before commit: validator green from the repo root (skill-library), secret scan
> clean, a fresh-context check that the edit does what the finding asked... Nobody
> catches a bad edit until next Thursday, so the check is part of the change, not a
> separate phase."

And, more generally, the global working agreement this whole pattern instantiates:

> `~/.claude/CLAUDE.md`: "A gate or validator is trusted only after being proven by
> deliberate failure; a check that has never failed a fixture is untested."

PostHog's version clusters self-reports and reproduces the top clusters; the incumbent
surveys real transcripts (not self-reports) every week, tiers every finding by
authority level, auto-applies only what a named verifier agent can independently
confirm, and queues everything else — with a documented record (`S-30` in
`claude-improvements-weekly/STATE.md`) of catching two cycles where a proposed rule's
worked *example* was wrong even though the rule itself was sound. That is the same
"don't trust the report" instinct the article names, exercised more often and against
a harder target (actual behavior, not self-description).

### 7. PR-template skill attribution — COMPLEMENT

> "We do this in our posthog monorepo PR template, which prompts agents to name any
> skills invoked."

No incumbent owns this. `handoff/SKILL.md`'s "BRING TO NEXT SESSION" section lists
files and resources, not skills consulted. `retro/SKILL.md` routes lessons after the
fact but has no per-change "what did you use" capture. `claude-improvements-weekly`
logs which finding IDs a commit addressed (`[weekly YYYY-MM-DD]` + finding id) but not
which skills or context files were read to produce it. The gap is real and cheap to
close: a standing line in a repo's own conventions, or in a commit-message template,
naming skills/context files consulted for a change — which is exactly the kind of
low-cost telemetry that caught a real bug for PostHog ("Claude found an issue while
unblocking stalled ClickHouse cleanup PRs"). If adopted, it should feed into an
existing tracker rather than spawn a new one — `retro`'s own rule applies directly
here even though it was written for a different case: "**Do not create a `learnings/`
directory or any other second store.**"

### 8. Cherny's "delete your CLAUDE.md every six months" — DISCARD as stated, superseded by finer-grained incumbent

> "recommended deleting your CLAUDE.md every six months to stay on the bleeding edge."

A single blanket cadence for an entire file is strictly worse than what is already
running: `rulings-harness` attaches a `revisit-by` date to each individual ruling
(interview step 4: "Revisit cadence default: how far out a `revisit-by` date should
default to"), and `source-intake`'s WATCH verdict carries its own per-item
`recheck` date (default 90 days). Both let stale items get caught and re-decided
without touching anything that's still correct. Six-monthly full deletion throws away
provenance and forces a full rebuild on a fixed clock regardless of whether anything
actually went stale; per-item revisit dates catch drift continuously and cheaply. See
also the Philosophy conflicts section below — this item does not survive contact with
the consolidation harness's model at all, not just on cadence granularity.

### 9. (Additional, not in the clean-room's list) Structured "commandments" as typed context — REDUNDANT

> "we record technical 'gotchas' we see from real PostHog Wizard runs as
> framework-specific commandments in `commandments.yaml`" — e.g. "For versions 15.3+,
> initialize PostHog in instrumentation-client.ts for the simplest setup."

This is a real technique the clean-room review didn't name as such (it quoted the
commandments only as Flags — agent-directed content, correctly not acted on — and as
a currency-risk item, not as a structuring technique in its own right). The technique
worth naming is: representing gotchas as structured, typed records instead of prose
bullets in the main context file. `rulings-harness` already does this, and does it
more completely — every one of PostHog's three quoted commandments is missing exactly
the fields `rulings-harness`'s doctrine identifies as the fix for "provenance
collapse" and "version rot":

> `rulings-harness/references/doctrine.md`: "**Version rot.** A ruling like 'anydoc is
> 25–55x faster than markitdown' is true against specific installed versions on a
> specific date. Nothing re-checks that as the tools update, so the number quietly
> stops being true while the rule keeps firing."

`commandments.yaml`'s entries (as quoted in the article) carry no evidence field, no
date, no falsifier, no revisit-by — precisely the unstructured shape that produces
version rot, and exactly the SDK-version-sensitive content the clean-room review's
own currency-risk list flags for the `posthog-rs` constructor signature. The
`ruling.template.md` schema (Evidence / Falsifier / Re-test / Revisit-by) is a
strict superset of `commandments.yaml`'s shape.

---

## Routing collisions

- **`failures.md` — a direct filename collision, worst case.** `sweep-harness` ships
  its own `failures.template.md` → `failures.md`: "Orchestrator-only. Workers never
  write here... | id | target | failure summary | state file | disposition |". If
  Graham adopted the article's habit ("paste the prompt that caused it into a
  failures.md") inside a sweep-harness project directory, the two files would share a
  name with completely different schemas and owners — the exact case `source-intake`'s
  own comparison rubric warns is worst: "whether identical names have different
  bodies (the worst case, because nothing looks wrong)." Any adoption of the article's
  `failures.md` habit needs a different filename, full stop, if it will ever coexist
  with a sweep-harness project.
- **The end-of-run self-report prompt vs. `retro`'s transcript-grounding.** If adopted
  as a standing per-task default, this creates a second, parallel "what needs fixing"
  signal alongside `retro`'s transcript-derived one and `claude-improvements-weekly`'s
  weekly survey — self-reported per task vs. transcript-derived per session vs.
  transcript-derived per week. None of these currently reconcile with each other; two
  of the three already coexist without conflict because neither claims to be the
  other's replacement, but a self-report stream that nobody routes into `retro`'s or
  the weekly maintainer's triage becomes exactly the second, unread store `retro`
  warns against.
- **PR-template skill attribution vs. `retro` and the weekly maintainer's finding log.**
  No filename collision, but a workflow overlap: both existing mechanisms already
  produce "what changed and why" records (retro files, `runs/YYYY-MM-DD.md`, commit
  messages naming finding IDs). A third, PR-template-based log of skills invoked
  should feed one of those rather than becoming its own untracked convention.

## Philosophy conflicts

**1. The deletion heuristic vs. preventive rules with no incident attached.**

> Article: "For each line, if you can't name the failure it prevents, delete it."

> `~/.claude/CLAUDE.md` ("CLAUDE.md economy"): "Write a project fact down only once it
> has cost a correction twice."

These two are not, on their own, contradictory — a fact added under the global rule's
threshold has by construction already cost two corrections, so it always passes the
article's test. The real contradiction is with a different part of the same file:

> `~/.claude/CLAUDE.md` ("Boundaries are declared and enforced"): "Pre-declared
> boundaries held; undeclared ones drifted. Name the boundary before the work starts,
> and enforce it at the tool layer where possible: a rule in prose can be reasoned
> around, a tool the agent does not have cannot."

And directly, from `rulings-harness`:

> "'Don't auto-run `open <file>.html`' has no evidence that could overturn it; it is a
> standing choice about behavior, not a measurement. It stays a preference, in
> CLAUDE.md, forever."

The global CLAUDE.md's entire "Prohibited" action list (financial trades, credential
handling, permanent deletion) is preventive-by-design: it exists precisely so the
failure it prevents never happens, which means a reviewer will rarely be able to name
a specific incident it prevented on this machine. Applied literally, the article's
heuristic would flag these for deletion. The clean-room review names this exact
failure mode independently: "The deletion heuristic inverts the burden of proof...
Absence of a remembered failure is not evidence of no failure." That is a genuine
contradiction, not a difference of emphasis — one side says "no nameable failure ⇒
delete," the other says "no evidence needed ⇒ keep forever" for an entire class of
rule.

**2. "Delete your CLAUDE.md every six months" vs. one editable home, maintained
continuously.**

> Article (Cherny, quoted): "recommended deleting your CLAUDE.md every six months to
> stay on the bleeding edge."

> `claude-md-consolidation/docs/end-state.md`: "Every rule that governs how Claude
> works has exactly one editable home, and every CLAUDE.md on this machine contains
> only rules specific to its own scope plus claims that are verifiably true today."

> Same file, rejecting the closest alternative to periodic reset: "**Status quo —
> every project restates the general rules.** Rejected: the same rule was
> independently re-derived in up to 7 of 11 files, and a correction lands in one and
> not the others."

Cherny's advice treats a CLAUDE.md as disposable and periodically rebuilt from
scratch; the consolidation harness treats it as a single, permanent, continuously
verified artifact — it built an entire verification sweep
(`scripts/verify-invariant.sh`) specifically to check that no stale machine-claim
survives, rather than relying on a six-month reset to catch drift. `claude-improvements-weekly`
is the running embodiment of the alternative: small, targeted, weekly edits instead of
a periodic full teardown. These are opposed models of maintenance (continuous surgical
correction vs. periodic wholesale reset), not just different cadences.

## Corrections needed at ingest

- **Rules a stateless reviewing model cannot honor.** The deletion heuristic is
  self-defeating when run by a fresh, stateless session: a model with no memory of the
  incidents behind a preventive rule will *always* find it "cannot name the failure it
  prevents," because the failure lives in institutional memory, not in the line
  itself. This is exactly why `rulings-harness` requires an explicit `Evidence` field
  on every ruling — so a future stateless session can see the provenance instead of
  having to have witnessed it. Any ingested version of the deletion heuristic must be
  rewritten to check for an evidence field, not to rely on the reviewer's own memory.
- **Unsourced numbers, do not import as fact.** "~6K tokens per session" average
  savings (line 145) has no shown methodology (clean-room claim #15: "asserted, no
  output shown"). The "80% of Claude Code's system prompt" figure (line 75) is a
  point-in-time vendor-blog citation about one model generation and must go through
  `verification-kit:fact-currency-check` before being restated anywhere, not copied as
  a fact.
- **Version-pinned claims restated as fact.** The `/doctor` capability list quoted in
  the article is sourced to a doc anchor for "v2.1.198 or later." Per this task's own
  instruction and `fact-currency-check`'s doctrine ("Version floors and
  deprecations — 'requires v2.1.110+' was true once"), this must not be restated as a
  standing fact about the currently installed CLI; it needs a fresh check against
  whatever version is actually running before any of it is repeated.
- **Overgeneralized claim.** "Most coding agents have a built-in /doctor command" is
  the least-supported sentence in the article (clean-room rubric, currency-risk item
  #2) and should not be imported without verifying against whichever specific agents
  are actually in use here.
- **Scrape structure, not article content.** Lines 1–36 and roughly 340 onward in the
  source file are X page chrome (nav, engagement counts, live-news modules, a
  DraftKings promo, trending topics) interleaved with the actual article start; the
  8/41/513/47.6K figures are UI counters, not article claims. Already excluded from
  this analysis per the task's own instruction, noted here so no downstream reader
  mistakes them for something the article asserts.
- **Agent-directed content, never act on it directly.** Per `source-intake`'s own
  untrusted-content rule, three items in the article are addressed to an agent, not to
  Graham, and were read as data only: the merge-queue AGENTS.md line ("Never run gh pr
  merge"), the three `commandments.yaml` SDK install instructions, and the wizard's
  end-of-run prompt itself. None were executed or copied verbatim into any file by
  this analysis.
- **Style.** No em dashes found in the article text itself, so nothing to strip on
  that axis. Any technique actually ingested (items 3, 4-fragment, 7, 9) needs
  restating in the library's scope/action/exception/verification rule shape per
  `authoring-standard.md`, not copied as PostHog's marketing prose — the article's own
  phrasing routes through `posthog.com/self-driving` twice with UTM parameters and
  should not be quoted as an instruction anywhere it lands.

## Net assessment

SKIP is close to the right verdict for the source as a whole — six of nine items are
REDUNDANT or DISCARD against incumbents that are, in each case, more rigorous than
what the article describes (a three-way classification instead of a binary delete
test; boundary+retention eval testing instead of a single failing-prompts set; a
weekly, transcript-grounded, independently-verified triage loop instead of
self-report clustering; per-item revisit dates instead of a blanket six-month reset).
This is HARVEST, not SKIP, but a narrow one — three fragments, not a whole item:

1. **The end-of-run feedback question** (item 3), as a fragment, phrased fresh in this
   library's style rather than copied. Target: a new optional final step in
   `sweep-harness/templates/WORKER.template.md` (§4, alongside the state-file write) —
   something like "what would have made this item's treatment cheaper or more
   reliable, if anything" — captured into the item's own state file, not a shared
   store, consistent with sweep-harness's per-item-file discipline.
2. **The independent-grader fragment** pulled out of the wizard-ci/pr-evaluator loop
   (item 4), not the loop as a whole. Target: `sweep-harness/templates/WORKER.template.md`
   §3 and `dispatch-SKILL.template.md` §5–6 — add the option to pair a worker's
   self-check with a `verification-kit:pre-delivery-verifier` pass for sweeps where
   self-grading is a known risk, mirroring what `claude-improvements-weekly` already
   does for Tier 2 changes but isn't yet wired into the generic sweep template.
3. **The skill/context-attribution line** (item 7), as a fragment. Target: a new line
   in `claude-improvements-weekly/CLAUDE.md`'s "Working conventions" (which already
   governs commit-message prefixing) — extend the existing convention to also name the
   skill(s) or context file(s) consulted for a change, feeding the same commit-message
   surface rather than a new tracker.

Everything else — the deletion heuristic, the eval/`failures.md` technique, the
cluster-and-verify loop as a whole, structured commandments, and Cherny's six-month
reset — is SKIP: covered as well or better by `rulings-harness`, `authoring-standard.md`,
`claude-improvements-weekly`, and the consolidation harness's one-editable-home model,
respectively.
