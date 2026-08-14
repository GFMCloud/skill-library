# End state — what "done" means

This document is the contract the project works toward. **When any instruction in
`CLAUDE.md` or a phase runbook is ambiguous, this doc is the tiebreaker.**

## The invariant

> `<INVARIANT — one sentence, stated as a STATE, not as a task. e.g. "Every X has
> exactly one editable home." Testable by inspection at any moment, by anyone,
> without knowing the project's history.>`

Everything below explains or enforces that sentence. If a rule below ever conflicts
with it, the invariant wins.

## The model in one paragraph

`<GOAL — what the world looks like when this is finished: the structure, where things
live, how they are consumed or used, what no longer exists.>`

## Why this shape and not the alternatives

`<The alternatives that were considered and why they fail — the structural reason,
not a preference. This section is what stops a later session from "helpfully"
regressing to a rejected design.>`

- `<Alternative A>` — rejected because `<structural failure mode>`.
- `<Alternative B>` — rejected because `<structural failure mode>`.

## Target layout / shape

```text
<the concrete target structure — tree, schema, environment, or checklist>
```

## Rules that follow from the invariant

| Situation | Correct home / handling |
|---|---|
| `<case 1>` | `<where it goes, how it is consumed>` |
| `<case 2>` | |

`<Any "never both" rules, naming rules, or collision rules go here.>`

## Enforcement

`<What checks the invariant mechanically — a validator script, a CI job, a query, a
sweep — and what is left to discipline because it cannot be checked mechanically.
Anything checkable should be checked; anything not checkable lives in CLAUDE.md.>`

## Definition of done (final-phase gate)

Route these checks to the installed agents rather than hand-authoring a prompt: a
fresh-context verification pass goes to `verification-kit:pre-delivery-verifier`, and
any check that compares documents against each other or against the artifacts they
describe goes to `consistency-checker:cross-document-checker`. Hand-authoring the
prompt each time is how three separate sessions ended up with three different
verifiers.

The final phase re-verifies each of these **from scratch**, in a fresh context — not
by re-reading earlier notes:

1. `<check 1 — restates the invariant as an executable sweep>`
2. `<check 2>`
3. `<check 3>`
4. `<check 4 — the enforcement gate proven by deliberate failure>`
5. `<check 5>`
6. `<IRREVERSIBLE-STEP> completed — the only irreversible step in the project.`
