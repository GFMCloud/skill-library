# Why toolkit-review is shaped this way

Condensed from the ECC harness evaluation (2026-09-16 to 2026-09-18) and its retro at
`~/work/ecc-harness-eval/.claude/retros/2026-09-17-ecc-harness-eval-project.md`; the
design it implements is `~/work/ecc-harness-eval/docs/toolkit-review-design.md`.

## What the ECC run was

A seven-phase `phased-harness` comparing the installed toolkit with `affaan-m/ECC`
v2.2.1 across six slots and two labeled gatekeeper pairs: neutral extraction per side,
two Sonnet judges per slot with the order swapped, a no-network container bench of hook
scripts, a three-arm review fixture, a generated ledger, two one-batch gates, and a
landing of nine skills and agents plus four fragments on a worktree branch. Spend
12.46M of a 15M token ceiling; about ten session hours over one day.

## What it proved

- Context-clean extraction plus two order-swapped judges produced rows a human could rule
  on, at under a third of the spend. Every landed row came from that layer.
- Deliberate-failure proofs before trust caught real bugs: a 429 check that matched reply
  text, an extractor that polluted the judge's directory, a fixture check masked by a
  redundant one.
- A mechanical rejection loop (structure and name checks, rejection notes, a wave runner
  with a cap and stop-on-429) ran 47 headless calls with no retry storm.
- Gates in one batch: ten rulings over seven hours, most "as proposed, continue".
- `output-lint` on packages, a bounded cross-document check and a fresh-context verifier
  found the assembler's own errors and the judges' self-contradictions.

## What it cost that a second run should not

- 15 of 16 first extractions were rejected (wrong heading levels, plugin names quoted
  from the source), because the template was calibrated on a synthetic slot. Extraction
  cost 2.3 times its projection and one slot lost its verdict to a name rule that forbade
  a name the source itself cites. Fix: the sharpened rejection text is the first prompt;
  calibrate on one real slot; the name rule allows names the source cites.
- The review fixture cost 27 percent of the ceiling to be inconclusive; the bare arm
  already found 8 to 10 of 10 conditions. Fix: a discrimination gate before the arms run.
- All fourteen verdict tokens were `merge` and `SUPERIOR SUBSTITUTE` ran both ways. Fix:
  rubric v2, verdict derived from rows.
- The `~/.claude` invariant stopped the run three times on Claude Code's own writes. Fix:
  the denylist check is the baseline, proven at run start.
- The evidence workspace was the only copy of the judgments and was deleted at close.
  Fix: archive before residue.
- Prose limits on read-only subagents failed three times; `--tools "Read,Glob,Grep"` on
  headless runs held every time. This skill uses headless runs for every read of
  candidate material.

## Sizes, and why `spot` exists

The independent reviewer of the ECC plan predicted "mostly SKIP plus a few harvested
ideas, which one `source-intake` run would find in a day", and the outcome matched. A
skill that turned every candidate repo into a seven-phase run would repeat the cost
without the lesson. `spot` is one session with no harness; `set` adds slots and gates;
`full` adds a behavioral layer only for slots whose comparison is about enforcement that
has to run.

## Relationship to the neighbours

`source-intake` owns intake, pin, the clean-room review and the review record; its
decisions table is the pre-seeded slot map here and its record template is what a run
writes at the end. `phased-harness` owns gates and disk-based resume for `set` and
`full`. `sweep-harness` is the shape of per-slot state. This skill owns the slot model,
the extraction and judging method, rubric v2, the runner tooling, and the landing
runbook. The label-blind judge in `source-intake/references/history.md` is the ancestor
of the method here.
