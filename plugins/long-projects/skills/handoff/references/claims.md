# Typed Claims: write and check

This is the how-to for the Typed claim v1 shape this skill produces and consumes
(writer: handoff generation; reader: handoff resume mode). The shape itself is defined
once, in the toolkit interface spec:
`maintainers/toolkit-interface-spec.md`, section 4. This file
explains how to fill it in and how to check it; it does not redefine any field.

## Write side

1. For each fact worth including that a command could re-derive, write one `checkable`
   entry: `type`, `claim` (the sentence a reader would read), `check` (the exact
   command that re-fetches the live value), and `expected`.
2. Run `check` now, before writing `expected`. Copy its actual output into `expected`
   verbatim. Never fill `expected` from memory, from the plan, or from an earlier
   message in the conversation. The postmortem this skill was built to avoid is a
   handoff that passed seven internal checks while naming the wrong branch, because the
   writer trusted what it remembered rather than what it had just run.
3. Anything that cannot be reduced to a command and an expected value - rationale for a
   decision, a warning about something fragile, an open judgment call - goes in
   `not_checkable` instead, with a `kind` of `rationale`, `warning`, or `decision`. Do
   not force a soft claim into `checkable` by inventing a command that technically runs
   but does not test the claim (a `check` that always matches is a claim wearing a
   checkmark, not a check).
4. Put the whole block in the handoff file under its own `## Typed Claims` heading, as
   a fenced ` ```yaml ` code block starting with `claims: v1`.

## Read side (resume)

1. Find the `## Typed Claims` block. If it is missing, treat the handoff as pre-T5
   format: there is nothing typed to check, so fall back to manual spot-checks and say
   so explicitly. Do not report an empty discrepancy table as if it proved anything.
2. For each `checkable` entry, run `check` again, right now, against whatever it names
   (a repo, a URL, a CLI, a state file). Compare the fresh output to `expected`. Do this
   even for claims that sound obviously true - obviousness is not verification, and is
   exactly the failure mode the roadmap's design note names.
3. Report a status in three sentences, per the toolkit interface spec's resume output
   order (section 4).
4. Render the discrepancy table: `claim | command | actual | match/mismatch`.
5. Render the `not_checkable` list verbatim under the heading "unverified by design".
   Never attempt to verify these; they are not checkable by construction.
6. If every row matches and nothing is ambiguous, report "proceeding". If any row
   mismatches, or a claim's wording is ambiguous enough that two different checks could
   satisfy it, stop and ask exactly one question naming the row. Zero typed claims are
   accepted from the document alone.

Staleness: `written_at` dates the claims. Before the table, list the files in the
project's git repo whose mtime is after `written_at`, and name them in the step 3
status. Matching claims prove the claimed values only; they say nothing about work done
after the handoff was written. A stale project is not a mismatch. It becomes the one
question in step 6 only when a changed file is one the first move or a claim depends on.
Limits: the list covers files that exist now, so a deletion, or a commit that left
mtimes alone, does not show.

`scripts/check-claims.py` in this skill directory implements steps 2, 4, and 5 and the
staleness list mechanically for a single handoff file: `python3 scripts/check-claims.py
<path-to-handoff.md> --project <repo dir>` (`--project` defaults to the current
directory). It exits 1 on any checkable mismatch and 0 when every checkable claim
matches; staleness never changes the exit code. It is the same procedure described
above, ordered so it can be run standalone; it is what the fixtures in `fixtures/` are
checked against (`bash fixtures/run-fixtures.sh` asserts all three cases), and it
does not replace the status in step 3 or the "ask one question" judgment call in
step 6, both of which stay with the session.

## Example (FIXTURE, from the interface spec, reproduced for reference - the spec is
## still the source of truth for the shape; these values are the spec's worked
## example and match no real tree state)

```yaml
claims: v1
written_at: 2026-09-11T16:20:00-05:00
checkable:
  - type: branch
    claim: work is on the toolkit-build branch of the skill library
    check: git -C /Users/gfm/skill-library branch --show-current
    expected: toolkit-build
  - type: count
    claim: the validator sees 49 skills
    check: bash /Users/gfm/skill-library/scripts/validate-skills.sh | tail -1
    expected: "49 skills checked: 7 failures, 42 warnings"
not_checkable:
  - kind: decision
    text: the stable backfill was deferred to Gate A rather than done in Phase 1.
```
