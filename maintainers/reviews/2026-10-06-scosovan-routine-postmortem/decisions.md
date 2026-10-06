# Decisions: scosovan routine postmortem

contract: v1
source: https://runbook.scosovan.com/claude-code-routine-reported-success-did-nothing/
type: article
pin: fetched 2026-10-06 00:58 CDT (page dated 2026-10-05), sha256 8b1cd7956bcdac94ce46ecbd5caa93705520d36b97346ac01de3ab77fc5dd31d (markitdown of the page, 1,575 words)
reviewed: 2026-10-06
verdict: HARVEST
recheck: -
evidence: maintainers/reviews/2026-10-06-scosovan-routine-postmortem/cleanroom-review.md, maintainers/reviews/2026-10-06-scosovan-routine-postmortem/comparison.md

## Verdict reasoning

A vendor post (it funnels to a paid "Routines Runbook"; author slug `manus_admin`, four posts
on the site all dated 2026-10-05, so likely agent-written) that argues one true thing well: a
green cloud Routine run means the session exited without an infrastructure error, not that
the task was done, and a source that could not be read must never render as a source with
nothing in it. The clean room scored evidence 2 of 5 (every platform claim is asserted with
a date, nothing quoted or linked to a section) and actionability 5 of 5. The incumbents
already hold the rule at harness level ("Unreachable is reported as unreachable, never as
empty", two three-way coverage counts, retry-then-escalate) and are stronger wherever they
overlap; the article's lane (cloud Routines) is one `schedule-harness` carves out and nothing
local covers. HARVEST, thin: three fragments sharpen the incumbents' wording, and the
comparison found one incumbent defect in passing. What would change the verdict: nothing
toward ADOPT; the platform claims become citable once the Routines doc is quoted with a
fetch date.

## Ancestry

none. Convergent: both sides reached "unreadable is not empty" independently.

## Rows

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Two-outcome source accounting with the verbatim error text and the explicit window: `read: <count> items for <explicit window>` or `unavailable: <the exact error or refusal text>`, carried into the section the source feeds so a report cannot silently shrink | INGESTIBLE FRAGMENTS | Two additions to the scout harness's own rule, in the library's words ("unreachable", `UNVERIFIED`, never "unavailable"): record the exact error text beside `unreachable`, and the window beside the item count, in `CLAUDE.md` Working conventions and `prompts/phase-0-scan.md` step 6 | `article.md:43` (the Check 5 block) | `claude-scout-weekly/CLAUDE.md` and `prompts/phase-0-scan.md` (harness files, Graham's) | S | two clauses; backed out by deleting | proposed (Tier 3: a harness edit; folded into Q-2026-10-06-6 as item (e)) | Graham |
| 2 | A closed status token per run: OK or PARTIAL on the first line of the run summary, PARTIAL forced whenever a source was unreachable or a verification check failed, so a script can count PARTIAL runs | INGESTIBLE FRAGMENT | One sentence in schedule-harness `## Done when` and the first line of `references/FIXTURE-run-log-excerpt.md`; pair it with an out-of-band check (the model that failed to read a source can also fail to write PARTIAL), which the scout harness already has in one form ("a cycle that ends without republishing the report is not done") | `article.md`, Check 7 | `plugins/voice-and-editing/skills/schedule-harness/SKILL.md` | S | one token to keep honest; backed out by deleting. Would fit the widened Tier 2 (incubator body, S, decisions row); flag off, Tier 3 | proposed | Graham |
| 3 | Late-run disclosure and the intended window: "If it is hours late, say so in the first line of the output" and "report on the window the slot intended, not the last 24 hours from now" | INGESTIBLE FRAGMENTS | Two sentences in schedule-harness "Overlap skip and the time guard", with the stateless-model correction: the prompt hardcodes the intended slot and the run reads the clock (`date`), because a session is never told its slot | `article.md`, Check 8 | `plugins/voice-and-editing/skills/schedule-harness/SKILL.md` | S | two sentences; depends on row 4 being settled first | proposed (Tier 3; after row 4) | Graham |
| 4 | Incumbent defect found while comparing: schedule-harness says "Do write a time guard into the pointer's prompt" (`SKILL.md:149`) while `templates/pointer.md:16` and the interface spec section 7 (`toolkit-interface-spec.md:283`) say the pointer body carries the harness directory, the phase skill, the mode and the absolute-limits block, "nothing else"; the run-log fixture says "Time guard in the prompt held", a guard the template cannot render (verified by grep 2026-10-06) | incumbent defect | Settle where the time guard lives: in the harness's `/phase` skill (the dispatch logic's one editable home, which section 7 names) or as an allowed pointer line (a spec change, section 7 bump); then make the fixture match | `comparison.md` T5 | `plugins/voice-and-editing/skills/schedule-harness/SKILL.md` or `maintainers/toolkit-interface-spec.md` section 7 | S | a spec question; the fixture changes with it | proposed (Tier 3: a stable spec is one of the two targets) | Graham |
| 5 | Platform claims for the Routine lane: on-the-hour runs start minutes late, so schedule at 9:07 not 9:00; every account connector is attached to a new routine by default, including write scopes, and included connector tools run without permission prompts; blocked hosts answer `403` with `x-deny-reason: host_not_allowed`; a 72-hour GitHub expiry switches a routine off | COMPLEMENT (Routine lane), unverified | None of the four is quoted or linked to a doc section; re-fetch the Routines doc, quote the lines with a fetch date, then decide whether `change-watch` (the only skill that registers a Routine) carries a connector-pruning line. Until then a watch row, not skill text | `article.md:100, 118` and Checks 6 and 8 | `state/watch.md` W-64 | S | one watch row | proposed (watch) | scout |
| 6 | A verification step that can fail; an idempotency key (head SHA, not PR number); the eight-row checklist as a whole; the `x-deny-reason` string match | REDUNDANT or DISCARD | evidence-report ("A verdict that does not say what failure mode it eliminates is decoration") and spec section 3's independent reviewer are stronger than a same-session re-read; the seen-index entry v1 already handles re-fire and flapping; the checklist rows are each covered by an incumbent where they overlap; matching an exact header string is brittle | `article.md`, Checks 3, 4, the table | none | - | - | out | - |

## Conflicts for the user to rule on

1. **Self-verification.** Article: "Add a step where the routine re-opens its own output and
   checks it against what it read ... Make that step able to fail the run." Interface spec
   section 3: "The reviewer runs on a model that differs from the builder's, with no parent
   history." Proposal: the article's check is a cheap first filter inside a Routine prompt,
   never the verdict; record it so the article is not cited for more. Alternative: none.
2. **Thin pointer against self-contained prompt.** Article: "Write it as instructions to a
   competent stranger ... name the files, name the windows, name the thresholds." Spec section
   7: the pointer body is the harness directory, the skill, the mode and the limits block,
   "nothing else", because the dispatch logic has one editable home. Both are right for their
   lane (a cloud Routine has no local harness to point at). Proposal: keep the lanes separate;
   `schedule-harness` stays thin, and any future Routine skill says so in its "Not for".
3. **Permissions posture.** `references/platform-facts.md` says to select "always allow" on
   each prompt to seed approvals; the article says to trim the tool list before the first run.
   Different platforms, but a reader following both grants first and trims later. Proposal:
   `schedule-harness` adds a review of the "Always allowed" panel after seeding (S, incubator
   body; rides row 2 or 3). Alternative: leave as is.

## Corrections at ingest

- Em dashes and staged one-line closers throughout the source; anything taken is rewritten.
- A stateless model cannot compare the clock to a slot it was never told: the prompt must
  carry the intended time, and the run needs `date`.
- "Append one line per run to a log file" names no destination; a cloud session's filesystem
  may not persist. Locally the run log already exists.
- PARTIAL cannot be self-enforced; pair it with an out-of-band check.
- The platform facts are asserted with a date stamp, not shown; the date stamp is not
  evidence. Quote the Routines doc with a fetch date before any of the four is used.
- Drop "the one almost every prompt fails" and "the single highest-value edit".
- Use the library's terms; "Routine" capitalized means the cloud product.
- The companion "hardened prompt" article and the product pages were not read and are not
  ingested.

## Flags

- No text addresses an agent; the one paste-in block (Check 5) is addressed to the reader
  for their own routine prompt and only restricts how outputs are reported.
- Commercial: the page funnels to a paid product and a checkout link
  (`/checkout/?add-to-cart=28`) and says it is not affiliated with Anthropic.
- Provenance: author slug `manus_admin`; all four posts on the site dated 2026-10-05.

## Rulings log

- 2026-10-06, scout cycle 7 (unattended): rows 1 to 4 proposed, queued as Q-2026-10-06-11 in
  claude-scout-weekly `STATE.md` (row 1 folded into Q-2026-10-06-6 (e)); row 5 a watch row
  (W-64); row 6 out.
