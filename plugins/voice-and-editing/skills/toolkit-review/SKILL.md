---
name: toolkit-review
description: >-
  Review installed Claude Code skills, agents and hooks on their own or against one or
  more candidate repos, slot by slot, with context-clean extraction, two order-swapped
  headless judges, a fixed rubric, a computed ledger and a gated landing. Three sizes:
  spot (1 to 5 skills, one session, no harness), set (a slot map with gates), full (set
  plus a hook bench or review fixture per slot that needs it). Use on "review my skills",
  "audit the toolkit", "compare my skills with this repo", "which of these skills earn
  their place", "toolkit review", "evaluate this skill pack against what I have", or a
  source-intake route L for a skill collection. Not for a single repo's worth-adopting
  question with no incumbent in play (that is source-intake), not a code review. Costs
  headless claude -p runs: about 100k tokens per extraction side and 50k per judge at
  spot size, metered against a ceiling the run sets.
metadata:
  maturity: incubator
---

# toolkit-review

Turn "are my skills any good, and is this repo's version better?" into rows a human can
rule on, with the incumbent bias removed by construction: the readers of candidate
material are headless runs with read-only tools and no settings, the judges see neutral
reports and never the files, and the slot verdict is computed from their per-item rows.
Why it is shaped this way, and what the ECC run paid to learn it:
[references/history.md](references/history.md).

## Fit test: pick the size, do not default to the biggest

| Size | When | Shape |
|---|---|---|
| `spot` | 1 to 5 installed items, with or without a candidate repo | one session, a run directory, no harness; ends in a decisions table and a review record |
| `set` | a slot map of 5 to 15 slots, reading evidence only | `phased-harness` with this skill's runbook as the phases; Gate A after calibration, Gate B before landing |
| `full` | `set` plus a behavioral layer for a slot whose comparison is about enforcement that only runs (hooks, gates) | adds the container hook bench and, behind a discrimination gate, the review fixture |

`spot` unless more than five installed items are in scope. `set` unless at least one
slot fails the reading test: does the slot compare enforcement that has to run, or
prose? Prose slots never need `full`, and `full` is per slot, not per run. The ECC
evaluation would have been `set` with a hook bench on two slots and no fixture.

Modes, any size: `self` (installed items only, judged against the bar), `one-repo`,
`many-repos` (one candidate side per slot, tagged by source id; the ledger carries a
source column), `subset` (named installed skills, each its own slot; candidates found by
a mapping step over the pinned sources, listed for ratification before extraction).

## Pipeline

Every step names its script; run [scripts/prove-scripts.sh](scripts/prove-scripts.sh)
first, no model called, and do not proceed on a FAIL.

1. **Environment gate.** `source-intake` Step 0 as written: laptop, clean library clone,
   `gh auth status`, `claude -p "Say OK" --setting-sources ""`. Concurrency check on the
   library: `status --short`, `log --oneline -5`, live sessions, worktrees.
2. **Run directory.** `scripts/init-run.sh <run-dir> <size> <mode> [name]`. The path holds
   neither the owner's nor the project's name (a judge sees its cwd) and is not inside a
   git repository. It writes `run.json` from [templates/run.json](templates/run.json),
   the marker, `name-list.txt` (always forbidden: owner, org, repo, "installed",
   "incumbent") and `context-names.txt` (plugin names, forbidden unless the source cites
   them). Review both lists. Then `scripts/check-dot-claude.sh` against a fresh
   interactive session start: expect `ok`.
3. **Intake and pin** each source with `source-intake` Step 1 (shallow clone into
   `<run>/candidates/<id>`, `rev-parse HEAD` into `run.json`, prior-review check in the
   library's `maintainers/reviews/`). Untrusted-content rule as written there.
4. **Slot map and items.** Fill `slot-map.tsv` (slot, purpose, evidence) and `items.tsv`
   (id `-`, side `installed` or a source id, source, slot, type, path). Then
   `scripts/bin-slots.py` (copies, ids as `item-<hash8>`, X/Y letters into
   `private/map.json`, never printed) and `scripts/make-facts.py` (counted facts per
   item). Items that fit no slot go in `notes/unbinned.md`.
5. **Calibrate on one real slot, both sides.** `scripts/run-extractor.sh <slot> <side>`
   for each side, `scripts/check-extract.sh <report> <side dir>` on each, then
   `scripts/run-judge.sh <slot> XY` and `YX` (or `S1` and `S2` for `self`) and
   `scripts/check-judgment.sh` on each. Record cost per call from `budget/usage.tsv`,
   project the run with real item counts, and set `budget_ceiling_tokens` in `run.json`
   before any wave. The extraction prompt already carries the exact headings and the
   forbidden-word rule; a rejected report gets the checker's note appended on re-dispatch,
   up to `redispatch_budget`, then the slot is recorded `extraction failed` with an owner.
6. **Waves.** One line per job in a jobs file, `scripts/run-wave.sh <jobs> <log>`:
   extractions, then checks, then judges, then checks. The wave runs from a copy of the
   scripts, so nothing in flight is changed by an edit. A 429 stops the wave; nothing
   relaunches until the reset time. A judge pair whose derived verdicts differ gets
   `run-judge.sh <slot> ESC` on the escalation model; all three are kept.
7. **Behavioral layer, `full` only, per slot.** Hook bench: stage the side's scripts under
   `<run>/bench/code/<side>`, events under `<run>/bench/events`, hooks list per side,
   then `scripts/run-hook-bench.sh installed`; a candidate side runs only after Gate A
   writes `auth_candidate_hook_bench: yes`. Fixture: build the repo and `planted.tsv`,
   run the bare arm, then `scripts/score-fixture.py --gate <min_bare_misses>`; a FAIL
   drops the fixture and returns its budget. Arms through `scripts/run-fixture-arm.sh`.
8. **Ledger.** `scripts/make-ledger.py` writes `ledger-items/<slot>.tsv`, `LEDGER.md`
   from [templates/ledger.md](templates/ledger.md), `decisions.md` in `source-intake`'s
   contract v1 vocabulary, and `AMBIGUOUS-CELLS.md`. `scripts/make-patches.py` writes the
   file lists. Then `turn-reduction:output-lint` on the ledger and the gate package,
   `consistency-checker:cross-document-checker` under a bounded loop of three, and
   `verification-kit:pre-delivery-verifier` in a fresh context.
9. **Gates.** `set` and `full` present Gate A from [templates/gate-a.md](templates/gate-a.md)
   after calibration and Gate B from
   [templates/gate-b-walkthrough.md](templates/gate-b-walkthrough.md) before landing,
   each in one batch, each defining its own vocabulary inline. `spot` presents the
   decisions table once, as `source-intake` Step 4 does.
10. **Landing.** Worktree from `origin/main`, one commit per plugin (validator F17),
    `maintainers/scripts/generate-inventory.sh` last, review record from
    `<source-intake>/templates/review-record.template.md`, secret scan, `scripts/validate-skills.sh`
    exit 0, no push. A row that touches runtime behavior (hooks, settings) lands as a
    `plan-gate` output whose every proof step names its trigger and says whether it is
    headless; one with no headless path is marked "the owner runs it, the agent watches"
    in the plan. Implementation sessions for such rows on one repo get disjoint file
    lists or run in sequence.
11. **Evidence archive before residue.** Copy `judgments/`, `extracts/`, `ledger-items/`,
    `LEDGER.md`, `decisions.md`, `AMBIGUOUS-CELLS.md` and `budget/usage.tsv` into the
    review record's directory, then offer exactly one deletion command for the run
    directory's `candidates/`, never the run directory itself.

Rubric, classes, derived verdict and the mapping to contract v1:
[references/rubric-v2.md](references/rubric-v2.md). Prompts:
[references/extraction-prompt.md](references/extraction-prompt.md),
[references/judge-prompt.md](references/judge-prompt.md),
[references/self-review-prompt.md](references/self-review-prompt.md),
[references/reader-checklist.md](references/reader-checklist.md), and for a
`challenge-*` slot [references/judge-challenge-note.md](references/judge-challenge-note.md)
(spliced into the judge prompt by `run-judge.sh`). Scripts and exit codes:
[references/runner-spec.md](references/runner-spec.md). Standing limits to print in every
ledger: [references/limits.md](references/limits.md). Fixtures the proofs use:
`templates/fixtures/`.

## Guardrails that bind every size

- Every read of candidate material is a headless run with `--tools "Read,Glob,Grep"`
  through `scripts/headless.sh`, never a subagent (a subagent inherits this session's
  hooks, skills and `CLAUDE.md`, and a prose "read-only" limit did not hold three times
  in the ECC run). The orchestrating session never reads a candidate source file except
  at landing, as data, to check it against the judge's description before rewriting.
- The orchestrator never judges a slot. A verdict it notices itself forming goes to
  `notes/orchestrator-bias.md` and is printed verbatim under the ledger.
- Candidate code runs only in the no-network container, only after the Gate A line, and
  never through an installer. No session opens with its cwd inside a clone.
- Nothing is written under `~/.claude`, and nothing to the library before landing.
- One budget covers everything: headless runs from the budget file, subagents from their
  completion notices, the orchestrator from the session usage tool, passed to
  `scripts/sum-budget.sh <extra>` at each phase boundary. Stop at
  `budget_stop_percent`.
- Fixture results are labelled fixture-derived wherever they appear; an inconclusive
  fixture is recorded as inconclusive, never as a tie.
- Boundary overrides given in chat are written to the run's `authorization.json` or
  `DONE.md`, dated and quoted, before the agent acts (ruled 2026-09-18).

## Inputs

The size and mode from the fit test; the installed items in scope (paths) and their
slots; zero or more sources with a pin; the models and ceiling in `run.json` (the
ceiling is set after calibration, not before); for `full`, the bench events and hook
lists, or the fixture repo with `planted.tsv`.

## Verify

`scripts/prove-scripts.sh` prints `all proofs PASS` before the first wave. Every
extraction passes `scripts/check-extract.sh` and every judgment `scripts/check-judgment.sh`
before the ledger is built; a rejected one is re-dispatched, never repaired. The ledger's
`AMBIGUOUS-CELLS.md` is read, not skipped. `scripts/check-dot-claude.sh` exits 0 at the
end of the run. For `spot`: the decisions table and review record exist and
`output_lint` passes on both.

## Done when

Every slot in `slot-map.tsv` has one row in `LEDGER.md` backed on disk by its extraction
reports and judgments (or is recorded `extraction failed` with an owner); ratified rows
are on a landing branch with the validator green and a review record; the evidence
archive exists; `~/.claude` and the library's main checkout are unchanged by the run.

## Stop when

Any proof in `scripts/prove-scripts.sh` fails. A 429 arrives (stop the wave until the
reset time it names). The budget stop is reached. A secret scan hits and the hit is not
in the reviewed-exceptions file. `check-dot-claude.sh` exits 9. A slot exhausts its
redispatch budget (record it, continue the others). The environment gate fails (no
degraded mode: the run does not happen from a phone, a cloud session or a connector).

## Output contract: v1

`LEDGER.md` and `ledger-items/<slot>.tsv` use rubric v2 (`references/rubric-v2.md`).
`decisions.md` uses `source-intake`'s contract v1 vocabulary by the fixed mapping in
that file, so a later `source-intake` run reads it unchanged. `budget/usage.tsv` columns:
timestamp, label, profile, model, input tokens, output tokens, status. Renaming a class,
a column or a section is a breaking change: bump this line and say so in the CHANGELOG.
