# Decision ledger: spot-2

Sources: src1 at 9862685f575c65a8247f90369951df1b3416e3d6. Created 2026-09-18. Rubric v2; verdicts derived from the per-item rows
by `make-ledger.py`, never read from a judge.

## Limits of this evidence

Standing limits that apply (from `references/limits.md`):

- Context-clean, not blind. Each judge's context held the owner's email block and the run
  path `/private/tmp/tr-runs/spot-2`. Neither ties a report to a side.
- A judge may guess at origin from content. Neither judge did: judge-XY wrote "I have no
  basis to guess either candidate's origin and am not attempting to", judge-YX wrote "I
  did not form any belief about where either report's source material came from".
- Agreement on a verdict is not agreement on the rows. Here both judges classed both
  items `COMPLEMENT`, 2 of 2.
- Item mapping is by id. `AMBIGUOUS-CELLS.md` reads "none".

This run's own limits:

- The one slot, `humanize`, is reading-only. No behavior was run for either side.
- Both judges said they could not tell from the reports whether the installed item's
  blocklists and the candidate's 25-pattern catalog overlap in content.
- The style rules in the owner's global instructions file (no em dashes, no mannered
  prose) do the same kind of job and were not binned as an item. The comparison is
  against one installed skill only.
- One installed item and one candidate item. The candidate's README.md, AGENTS.md,
  packaging and CI files were not evaluated (`notes/unbinned.md`).
- No extraction was rejected; no re-dispatch was used.

## Slots

| Slot | Verdict (per judge) | Judge agreement | Evidence | Deciding criteria (per judge) | Per-item rows | Risk |
|---|---|---|---|---|---|---|
| humanize | merge / merge | 2 of 2 | static | Specificity settled the per-item classification (each item's concrete checklist covers ground — channel/recipient tone logic vs. a named pattern taxonomy with fact-preservation — that the other's report shows no equivalent for); Fit with the bar is what separates the two candidates in the overall scoring, since Y's file-mode write-through is a stated conflict with plan-then-stop while X never triggers that bar at all. / "Fit with the bar" and "Maintenance burden" separate the two: Y carries an explicit, report-flagged conflict with the plan-then-stop behavior in its file mode, while X avoids that conflict by never writing files itself but takes on a small external-tool dependency (`message_compose_v1`) that Y doesn't have. | ledger-items/humanize.tsv | judges agree on the class of 2 of 2 items; 1 candidate items named to take by at least one judge, 1 by both |

## Overrides

None. No bench or fixture ran in this run.

## Orchestrator bias log

Verbatim from `notes/orchestrator-bias.md`:

- 2026-09-18: Before the judges returned, the orchestrator expected "keep" because the installed item is personal voice and the candidate is generic. After reading the judgments it leans toward installing the candidate beside the installed item as its own plugin (no skill-name collision exists) over harvesting fragments into the installed item. This is a lean of the orchestrator, not a judge row.
- 2026-09-18: The orchestrator learned which letter is the installed side from the order the two extraction jobs finished. It did not read private/map.json. No judge prompt was affected.

## Not evaluated

| What | Why | Owner | Destination |
|---|---|---|---|
| Content overlap between the installed blocklists and the candidate's 25 patterns | Judges read reports, not files; both said they could not assess it | Graham | Checked at landing, when the candidate file is read as data |
| Global instructions file style rules as a third item | Not a skill; not binned | Graham | A later `self` run if wanted |
| Candidate README.md, AGENTS.md, packaging, CI | Not toolkit items | none | `notes/unbinned.md` |
| Whether either skill's steps are followed in a live session | Reading-only slot | Graham | Behavioral test, not planned |
