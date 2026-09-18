# Decision ledger: verification-self-review

Sources: none (self-review). Created 2026-09-18. Rubric v2; verdicts derived from the per-item rows
by `make-ledger.py`, never read from a judge.

## Limits of this evidence

Copy the standing limits from the skill's `references/limits.md` that apply to this run,
then add the run's own: which slots are reading-only, which judge said it recognized a
side, which rows the assembler printed as ambiguous (`AMBIGUOUS-CELLS.md`), and any
extraction that failed the check three times and has no verdict.

## Slots

| Slot | Verdict (per judge) | Judge agreement | Evidence | Deciding criteria (per judge) | Per-item rows | Risk |
|---|---|---|---|---|---|---|
| verification | TIGHTEN 5 / TIGHTEN 5 | 5 of 5 items same class | self-review, reading only | Enforcement mechanism decided four of the five rows (all named a real prose-vs-script gap the report itself disclosed); Fit with the bar decided the fifth (e739493a's evidence-quality allowance). / Enforcement mechanism decided four of the five rows; item-e739493a's row turned on Fit with the bar because its enforcement script is real but validates the wrong thing (verdict shape, not evidence substance). | ledger-items/verification.tsv |  |

## Overrides

Every slot where bench or fixture evidence contradicted the reading verdict, and whether
the result was consistent across all runs of the arm. "None" if none.

## Orchestrator bias log

Verbatim from `notes/orchestrator-bias.md`. "Empty" if empty.

## Not evaluated

| What | Why | Owner | Destination |
|---|---|---|---|
