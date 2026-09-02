# Worker runbook: sweep-<NAME>

You are dispatched for **exactly one item id** from `MANIFEST.tsv`. Do not read or
act on any other row.

## 0. Idempotency check (do this first, always)

Read `state/item-<ID>.md` if it exists.

- `status: done` → stop immediately. Report "already done" and return. Do not redo
  the treatment.
- `status: failed` or the file does not exist → proceed.

## 1. Look up your item

Read your row from `MANIFEST.tsv`: `id`, `target`, `poisoned`, `notes`.

## 2. Do the treatment

`<PER-ITEM PROCEDURE: the concrete steps that turn `target` into a finished item.
This is the one section the interview in Step 2 of SKILL.md exists to fill in.>`

## 3. Check done

`<PER-ITEM DONE CHECK: the specific, executed evidence that proves this item is
finished. State the command or inspection, not "looks right".>`

## 4. Write your state file, and only your state file

Write `state/item-<ID>.md` from the [item-state template](item-state.template.md)
with:

- `status: done` if the check in step 3 passed, `status: failed` if it did not.
- The evidence: the command run and its actual output, not a paraphrase.
- Timestamps for started/completed.

Then stop. Do not touch `MANIFEST.tsv`, `failures.md`, or any other state file.
