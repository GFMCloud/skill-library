# Holdout: experiment-<NAME>

The fixed data, scenario set, or check that predictions are scored against. Frozen
once; not fit, tuned, or adjusted against afterward.

## What is frozen

`<Describe the holdout precisely enough that "did this change" is checkable: a file,
a query, a fixed date range, a set of held-out cases.>`

## Frozen since

`<YYYY-MM-DD>`

## How to verify it has not changed

`<The command or check that proves the holdout is still what it was when frozen: a
checksum, a row count, a diff against a committed snapshot.>`

## History

`<If the holdout was ever re-frozen, list each version here with its date and why:
never silently overwrite this file.>`
