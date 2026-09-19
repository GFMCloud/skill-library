# Decision ledger: handoff-vs-handoff-skill

Sources: src1 at 8990d64805fe340c9e79f59db5a93da273559dc6. Created 2026-09-18. Rubric v2; verdicts derived from the per-item rows
by `make-ledger.py`, never read from a judge.

## Limits of this evidence

Copy the standing limits from the skill's `references/limits.md` that apply to this run,
then add the run's own: which slots are reading-only, which judge said it recognized a
side, which rows the assembler printed as ambiguous (`AMBIGUOUS-CELLS.md`), and any
extraction that failed the check three times and has no verdict.

## Slots

| Slot | Verdict (per judge) | Judge agreement | Evidence | Deciding criteria (per judge) | Per-item rows | Risk |
|---|---|---|---|---|---|---|
| handoff | merge / merge | 2 of 2 | static | Enforcement mechanism and fit with the bar settled the rows: X's item has an executable, exit-code-checked verifier backing the exact behaviors the bar requires, while Y's three items are explicitly prose-only and only partially support those same behaviors. / Enforcement mechanism and Fit with the bar (specifically executed-evidence) settled the rows: X's item ties resume to a mechanically re-run, exit-code-gated check, while Y's equivalent item relies on an optional, unenforced "light look at reality." | ledger-items/handoff.tsv | judges agree on the class of 4 of 4 items; 1 candidate items named to take by at least one judge, 1 by both |

## Overrides

Every slot where bench or fixture evidence contradicted the reading verdict, and whether
the result was consistent across all runs of the arm. "None" if none.

## Orchestrator bias log

Verbatim from `notes/orchestrator-bias.md`. "Empty" if empty.

## Not evaluated

| What | Why | Owner | Destination |
|---|---|---|---|
