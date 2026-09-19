---
name: sweep
description: >-
  Run the next batch of the `<SWEEP-NAME>` sweep (or check status). Use when the
  user opens this sweep directory and wants to start, continue, resume, or check
  progress on the batch.
metadata:
  maturity: stable
  version: 1.0.0
  reviewed: <YYYY-MM-DD>
---

# Run a `<SWEEP-NAME>` batch

`<GOAL, one sentence: what this sweep is processing and why.>`

## Dispatch

1. Read `MANIFEST.tsv` (frozen list) and `state/` (per-item results).
2. Compute `pending = { ids in MANIFEST.tsv } - { ids with a state file whose
   status is done or failed }`. This is the entire resume mechanism: no other
   bookkeeping exists.
3. If `pending` is empty: report the count of done vs. failed, confirm the poisoned
   item (`<POISONED-ITEM-ID>`) is present in `failures.md`, and stop. The sweep is
   finished.
4. Otherwise, claim a batch of up to `<BATCH-SIZE>` pending ids.
5. Dispatch one subagent per claimed item, each given: its single item id, the full
   text of `WORKER.md`, and this file's do-not-touch list restated. Run them in
   parallel where the runtime supports it.
6. Wait for every dispatched worker to write its state file. Do not proceed on a
   worker's chat summary alone: read the state file it wrote.
7. For any item whose state file says `status: failed`, add or update its row in
   `failures.md` (orchestrator writes this, not the worker).
8. Commit `state/` and `failures.md` changes for this batch.
9. Repeat from step 2 until `pending` is empty.

## Guardrails

`CLAUDE.md` in this directory is binding: it names who owns `MANIFEST.tsv` and
`failures.md`, and the worker do-not-touch list. Every subagent prompt in step 5
restates it: delegation never weakens a guardrail.

## Interruption policy

None, between batches. This sweep does not ask "shall I continue?" It runs batches
until `pending` is zero, logging failures to `failures.md` as it goes rather than
stopping on the first one. The only stop is the finished report in step 3, or a
genuine blocker `WORKER.md` did not anticipate.

Prefer ending a session at a batch boundary over grinding one session long. Resume is
free: the next `/sweep` recomputes `pending` from disk.
