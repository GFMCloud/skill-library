# sweep-<NAME>: guardrails

Pointer: general working agreements live in `~/.claude/CLAUDE.md`. This file states
only what is specific to this sweep.

## Ownership

- **The orchestrator (the session running `/sweep`) owns:** git, `MANIFEST.tsv`,
  `failures.md`. Nothing else writes these files, ever.
- **Each worker owns exactly one file:** its own `state/item-<ID>.md`. A worker that
  writes any other file, including another item's state file, has violated its
  contract.

## Do-not-touch (workers)

- `MANIFEST.tsv`: frozen at generation. Never edit a row. Scope changes require a
  new manifest version, decided by the orchestrator, not a silent edit.
- `failures.md`: the orchestrator reads worker state files and writes triage rows
  here. Workers report failure by setting `status: failed` in their own state file
  and stop; they do not write to `failures.md` directly.
- Any other item's `state/item-*.md`.
- `.claude/skills/sweep/SKILL.md`: the dispatch logic; edit it deliberately, not as
  a side effect of running a sweep.

## The poisoned item

`<POISONED-ITEM-ID>` is planted deliberately and must fail. Do not "fix" it, remove
it, or treat its failure as a bug to patch: its failure, recorded with real
evidence in `failures.md`, is the proof that this sweep's done-check actually
detects failure. If it ever comes back `status: done`, treat that as a broken
done-check, not a passing item.

## Commits

`<WHO/WHEN: e.g. orchestrator commits MANIFEST.tsv once at generation, then commits
state/ + failures.md after each batch.>`
