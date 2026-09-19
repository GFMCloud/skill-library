# Gate B: [run name]

Written as the walkthrough, not as a table that needs one (ECC Gate B, 2026-09-17, needed
a second message to explain "incubator"). One section per row. Nothing here is
pre-authorized; the owner names rows or lanes.

Vocabulary: **incubator** is a maturity label in the skill's frontmatter, not a location
and not a gate; an incubator skill installs with its plugin like any other. What keeps a
row out of use is not landing it, or not merging the branch. **Lane** is where a row
lands: `incubator` (a skill or agent file on the landing branch), `hook-gate` (a
`plan-gate` output only; the row touches runtime behavior and is implemented in its own
session), `reference-only` (a note, nothing landed), `out-of-scope`.

Fresh concurrency check, run now, not copied from earlier: `git -C <library> status
--short --branch`, `log --oneline -5`, live sessions on the path, worktrees.

## Row B1: [item id], [source path]

- **What the judges said:** [class per judge, the note, the deciding criterion].
- **Recommendation:** [land as / leave out], lane [lane], target [one library file].
- **Why:** one line.
- **What changes if overruled:** [the side effect and its owner].
- **Where it stays recoverable:** the landing branch until merged; the source at its pin.

## Row B2 ...

## Rows left out

One line each with the reason.

## After landing

The landing session: worktree from `origin/main`, one commit per plugin, validator exit
0, inventory regenerated last, review record from `source-intake`'s template, secret
scan, no push. Then the evidence archive: judgments, extracts, summaries and the budget
file copied into the record directory before any residue is offered for deletion, and
exactly one deletion command offered, the narrow one.
