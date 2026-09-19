# Gate A: [run name]

One batch. Every row carries a recommendation and one line of reasoning. Rows the owner
does not object to are ratified as proposed. Any ruling that overrides a proposal names
who owns that proposal's side effects. Run `turn-reduction:output-lint` on this file
before sending it.

Vocabulary used below, so no row needs a second message to explain it: **slot** is one
capability being compared; **side** is `installed` or a source id; **static** evidence is
reading only; **bench** is hook scripts fed synthetic events in a container; **fixture**
is a review task on a synthetic repo, always reported as fixture-derived.

## A0. Slot map

| Slot | Purpose | Installed items | Candidate items | Evidence |
|---|---|---|---|---|

Recommendation: as built. Items that fit no slot: `notes/unbinned.md`.

## A1. Calibration result and budget

Calibration slot: [slot]. Extraction cost per side, judge cost, first-attempt pass or
fail. Projected total with real item counts: [n]. Recommendation: ceiling [n], stop at 80
percent for phases that launch runs, 90 for assembly and landing.

## A2. Behavioral layers (full size only)

| Slot | Layer | Why reading is not enough | Authorization needed |
|---|---|---|---|

Recommendation per row. A candidate hook bench needs `auth_candidate_hook_bench: yes` in
`gate-a/rulings.md`; nothing runs candidate code before that line exists.

## A3. Deferred slots and need questions

| Slot | Why deferred | Question for the owner | Default |
|---|---|---|---|

## A4. Name lists

`name-list.txt` (always forbidden) and `context-names.txt` (forbidden unless the source
cites them) as generated, plus any additions. Recommendation: as generated.

## A5. Anomalies so far

One line each, with the recommendation, from the run's state file.

## Ratified by default

The models in `run.json`, the wave size, the redispatch budget, the timeout.
