# Rubric v2

The one editable home for the judging vocabulary. `references/judge-prompt.md` and
`references/self-review-prompt.md` restate it for the judge; `scripts/check-judgment.sh`
enforces the row format; `scripts/make-ledger.py` derives verdicts from it. Change it
here first, then in those four, in one commit.

## Why v2

Rubric v1 (the ECC run, 2026-09-17) asked each judge for a slot verdict token and
per-item classes from `source-intake`'s five. Every one of fourteen verdict tokens came
back `merge`, so the token carried nothing; the information was in the rows. And
`SUPERIOR SUBSTITUTE` was written in both directions (on the better item by some judges,
on the item that has a better counterpart by others), which left 38 cells the assembler
could not read and six rows contradicted by the same judge's prose. v2 fixes the
direction in the class name, drops the verdict token, and computes the verdict.

## Comparison classes (two reports, X and Y)

One row per item id, three columns: Item, Class, Note.

| Class | Meaning, from the row's item's point of view | Requires |
|---|---|---|
| `SUPERSEDES <id>` | this item should replace the named item on the other side | an id from the other report |
| `SUPERSEDED BY <id>` | the named item on the other side should replace this one | an id from the other report |
| `COMPLEMENT` | fills a gap the other side's set has; the note names the gap | |
| `FRAGMENT -> <id>` | not wanted whole; named sections improve the named item | an id from the other report |
| `REDUNDANT <id>` | the named item does the same job at least as well; nothing to take | an id from the other report |
| `DISCARD` | nothing to take, for a reason that is not about the other side | |

Rejected by the checker: a class missing its id; an item naming itself; two items that
`SUPERSEDES` each other. Left for the assembler to print as ambiguous, never resolved:
an id that is not in `items.tsv`; an item classed twice by one judge; a row for an id no
report mentions.

## Derived slot verdict (comparison)

Computed per judge from the rows, then compared across judges:

- `drop-both`: every row on both sides is `DISCARD`.
- `replace`: every installed item is `SUPERSEDED BY` a candidate item (or is the target
  of a candidate `SUPERSEDES`) or `DISCARD`, and at least one is superseded.
- `merge`: any candidate item is `SUPERSEDES`, `COMPLEMENT` or `FRAGMENT`, and not `replace`.
- `keep`: otherwise.

Judge agreement is reported twice: on the derived verdict, and per item on the class
word. A candidate item is "named to take" when a judge classed it `SUPERSEDES`,
`COMPLEMENT` or `FRAGMENT`; the ledger says how many judges named it. When the two
judges' derived verdicts differ, a third judge runs on the escalation model and all three
are kept.

## Self-review classes (one report, R)

One row per item id, four columns: Item, Class, Criterion, Note.

| Class | Meaning |
|---|---|
| `KEEP` | earns its place as written |
| `TIGHTEN <section or field>` | earns its place; the named part is where it falls short |
| `SPLIT` | two jobs that would route or load better as two items |
| `RETIRE` | does not earn its place; the note says what covers the job instead |

Criterion is the one score-table criterion that decided the class. The slot line in the
ledger is the count of each class per judge; there is no verdict token.

## Score criteria (both modes)

Fit with the bar, Enforcement mechanism, Context cost, Maintenance burden, Specificity,
each 0 to 3 with one sentence of evidence citing the report. A 0 on Fit fails the
candidate. "Portability" and "Gap coverage" from the original brief were dropped in the
ECC plan review because they reward the bigger corpus and adapters the owner cannot use.

## Mapping to source-intake contract v1

`decisions.md` is read by a later `source-intake` run and keeps that skill's vocabulary:
`SUPERSEDES` to `SUPERIOR SUBSTITUTE`; `SUPERSEDED BY` and `REDUNDANT` to `REDUNDANT`;
`FRAGMENT` to `INGESTIBLE FRAGMENT`; `COMPLEMENT` and `DISCARD` unchanged. Both columns
are printed. Adopting v2 inside `source-intake`'s comparison prompt is a separate change
at promotion time.
