# Decision ledger: set-1

Sources: src1 at e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156, src2 at 69768ff1b0537a4656e69f550fc444ac35b945d2, src3 at 71f3bdb700268e1a2d70fa28da84c88081337503, src4 at c1c8a8c1471069fb0e188eeaff69b8e8db6564a8, src5 at 72c750bb070d95171dbb2244e5b62b1b7da69c12. Created 2026-09-18. Rubric v2; verdicts derived from the per-item rows
by `make-ledger.py`, never read from a judge.

## Limits of this evidence

Standing limits that apply to this run (full text: the skill's `references/limits.md`):
context-clean, not blind; a judge may guess at origin from content; agreement on a verdict
is not agreement on the rows; item mapping is by id. The bench and fixture limits do not
apply: no behavioral layer ran.

This run's own limits:

- Every slot is reading-only (static). Nothing was executed from any candidate.
- One judge said it recognized a side: `judgments/orchestration/judge-ESC.md` names the
  product behind item-5f05bf4c from the binary names in its report. It classed that item
  DISCARD on content. `judgments/evidence/judge-ESC.md` states it did not recognize either.
- Almost every candidate row is COMPLEMENT, which derives to `merge` whenever any candidate
  item is a complement. Here `merge` means "does a different job and has a piece worth
  taking", not "is better". The pieces are in each judgment's per-item notes.
- Slot `overengineering-review`: both judges found the two library items paired with the
  slot do a different job. Read the verdict as a gap, not a comparison.
- Several candidate items depend on their own CLI (src2, src3) per the inventory. Judges
  scored that under maintenance burden; no CLI was present to test the dependence.
- The owner's `dataviz` skill and the rules in the owner's global instructions file are
  not library items and were not compared (slots `figures`, `delegation`, and the
  worth-adopting review of src1).
- Ambiguous cells: none. Extractions that failed the check three times: none. One
  extraction (diagram, one side) was rejected once for a forbidden word and passed on
  re-dispatch.
- The worth-adopting reviews are single clean-room readings with no second reviewer, on
  depth-1 clones, so commit cadence and author count are unverified in all seven.

## Slots

| Slot | Verdict (per judge) | Judge agreement | Evidence | Deciding criteria (per judge) | Per-item rows | Risk |
|---|---|---|---|---|---|---|
| delegation | merge / merge | 2 of 2 | static | Maintenance burden (external `orx` CLI + missing companion skill for X vs. no runtime dependency for Y) and Fit with the bar (Y's explicit human-review-checkpoint and stop-and-ask instructions vs. X's silence on pausing before the spawn action itself) most separated the two; specificity and enforcement were essentially tied and neither failed the bar outright. / Specificity and Fit with the bar settled the rows: both items are concrete and detailed but cover non-overlapping halves of the delegation problem (routing/sizing vs. safe execution/scoping), so neither supersedes or is redundant with the other. | ledger-items/delegation.tsv | judges agree on the class of 2 of 2 items; 1 candidate items named to take by at least one judge, 1 by both |
| diagram | merge / merge | 2 of 2 | static | Fit with the bar (specifically the "plan, then stop" behavior) and Enforcement mechanism settled the rows: X wins on the former with a built-in confirm-before-draw step, Y wins on the latter with fail-closed atomic delivery and deeper geometric/visual checks, so neither supersedes the other. / Fit with the bar (behavior 1, plan-then-stop) and Enforcement mechanism (fail-closed visual evidence vs. silent degrade) — X wins the first, Y wins the second, and neither dominates the other, which is why both are marked COMPLEMENT rather than one superseding the other. | ledger-items/diagram.tsv | judges agree on the class of 2 of 2 items; 1 candidate items named to take by at least one judge, 1 by both |
| evidence | merge / keep / merge | 2 of 3 | static | Enforcement mechanism and Fit with the bar decided the rows. X backs executed evidence and the not-checked list with scripts that exit non-zero. Y is prose only and hands the not-checked reporting to a document the report says is absent. / Enforcement mechanism and Specificity settled the rows: X's items back their instructions with executable, fixture-proofed scripts that verify their own claims, while Y's item is prose-only despite comparably concrete checklists. / Enforcement mechanism and Specificity (of domain coverage) settled the rows — each item's content is concrete enough that no pair does strictly the same job, so all three land as complements rather than supersessions. | ledger-items/evidence.tsv | judges agree on the class of 1 of 3 items; 1 candidate items named to take by at least one judge, 0 by both |
| experiment-loop | merge / merge | 2 of 2 | static | Fit with the bar and Specificity settled the rows: each item is strong on different halves of the bar (X on plan-then-stop/checked-vs-not, Y on executed evidence) with equally concrete, non-generic mechanics, so neither supersedes the other — they cover different failure modes of the same slot. / Maintenance burden and Fit with the bar most sharply separated the two items' character (X self-contained and bar-aligned, Y dependent on an unincluded external CLI and only partially bar-aligned), but the classification itself rests on the two items covering non-overlapping mechanisms — execution/orchestration versus predict-before-look discipline — which is why both land as COMPLEMENT rather than one superseding or being redundant with the other. | ledger-items/experiment-loop.tsv | judges agree on the class of 2 of 2 items; 1 candidate items named to take by at least one judge, 1 by both |
| figures | merge / merge | 2 of 2 | static | Maintenance burden and Fit with the bar (specifically the breadth of "say what was and wasn't checked" support) did the differentiating work — X wins on being dependency-free and immediately runnable, Y wins on having broad, mandatory-feeling transparency and reproducibility requirements baked into its actual output path. / Maintenance burden and enforcement mechanism separated the two most: Y's real, file-inspecting audit and tighter evidence discipline outweigh its much heavier dependency chain (LaTeX/TikZ, external `orx` CLI, unverified companion modules), while X's stdlib-only footprint is offset by a weaker, dict-level, exception-swallowing check that nothing compels the agent to run. | ledger-items/figures.tsv | judges agree on the class of 2 of 2 items; 1 candidate items named to take by at least one judge, 1 by both |
| orchestration | keep / keep / merge | 2 of 3 | static | Fit with the bar and specificity decided the rows. The Y items spell out the three behaviors directly, while the X item has no content on them. / Specificity and enforcement mechanism settled the rows: item-5f05bf4c's own report confirms it contains no orchestration substance and no verification mechanism, while Y's two items each carry concrete, non-overlapping checklists/failure modes and (for bdc9b27e) an actual tool-layer restriction. / Specificity and fit with the bar: the three items address non-overlapping sub-problems (scaffolding, in-flight supervision, external-tool discovery) at very different depths of concrete, falsifiable detail, so none does the same job as another and no SUPERSEDES/REDUNDANT pairing applies. | ledger-items/orchestration.tsv | judges agree on the class of 2 of 3 items; 1 candidate items named to take by at least one judge, 0 by both |
| overengineering-review | merge / merge | 2 of 2 | static | Specificity (topic fit for the slot's stated purpose) and context cost/maintenance burden decided the rows: Y's enforcement edge is real but confined to one item and buys rigor for the wrong job, while X hits the slot's actual purpose — over-engineering, not correctness/security — cheaply and with nothing to install or verify externally. / Specificity to the slot's actual task (over-engineering review, not correctness/security review or pre-apply gatekeeping) decided the rows; Context cost and Maintenance burden reinforced the pick of X as the base to fragment into, since Y's items carry more named external references and an install step X's items lack. | ledger-items/overengineering-review.tsv | judges agree on the class of 2 of 4 items; 2 candidate items named to take by at least one judge, 2 by both |
| security-audit | merge / merge | 2 of 2 | static | Enforcement mechanism and Context cost / Maintenance burden settled the rows: X wins on mechanical enforcement and specificity but carries real cost and runtime dependencies, Y is essentially free to keep loaded but has no executable enforcement — so each fills a gap the other's report shows it lacks rather than one replacing the other. / Enforcement mechanism and context cost/maintenance burden pulled in opposite directions — X wins decisively on having a real script-layer check, Y wins decisively on cost and dependency footprint — which is why neither item supersedes the other rather than one dominating outright. | ledger-items/security-audit.tsv | judges agree on the class of 2 of 2 items; 1 candidate items named to take by at least one judge, 1 by both |

## Overrides

None. No bench or fixture ran.

## Orchestrator bias log

# Orchestrator bias log (printed verbatim under the ledger)

- 2026-09-18 01:10. The orchestrator learned which letter is the library side in slot
  `security-audit`: `check-extract.sh` printed "context name 'turn-reduction' allowed, the
  source cites it" for `Y.md`. The orchestrator judges no slot, and the judges never see
  this output. Overnight checks write to files the orchestrator does not need to read.
- 2026-09-18 01:00. The slot map was drawn from a clean headless inventory (one neutral
  sentence per item, `mapping/src*.tsv`), not from reading candidate files. The choice of
  which library items sit opposite each candidate is the orchestrator's and is ratified by
  the owner at Gate A row A0.
- 2026-09-18 01:11. `pgrep` output at launch showed the orchestrator which report file belongs to which side in slots `diagram` and `overengineering-review`. Same handling: the orchestrator judges nothing.
- 2026-09-18 01:45. Forming a view on slot `delegation`: the orchestrator knows the owner's global instructions file already covers brief content, disjoint subtrees and spawn limits, which the judges never saw. That view is why the Gate B recommendation for the row is leave out, and it is the orchestrator's, not the judges'.
- 2026-09-18 01:45. Slot `overengineering-review`: both judges found the two library items paired with this slot do a different job. The pairing was the orchestrator's at Gate A row A0; the computed verdict (merge) stands, read as a gap, not a comparison.

## Not evaluated

| What | Why | Owner | Destination |
|---|---|---|---|
