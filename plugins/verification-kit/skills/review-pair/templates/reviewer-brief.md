# Reviewer brief: Premises table

The brief handed to the reviewer is the Goal block v1, the change, and this table. The
rule and its reason are in SKILL.md, "Premises in the brief". `long-projects:orch-review`
carries the same table in its own `templates/reviewer-brief.md`; the two plugins do not
depend on each other, so each keeps a copy of this short file.

## Premises

| Premise | Observed (command and output reference) | Inferred (from what) |
|---|---|---|
| <one-line fact the change relies on> | `<command>` -> <where its output is: file and line, run id, transcript line> | |
| <one-line fact> | | <the source it was inferred from> |

## Filling it

- One row per fact the change relies on that the change itself does not show: a path, a
  working directory, a schedule, a version, the state of a running system.
- Each row fills exactly one of the two evidence columns.
- Another system's proof is not an observation of this one. Evidence from a different
  routine, host or run goes in Inferred.
- An inferred premise about a running system (a scheduled or cloud routine, a deployed
  service, a trigger) is checked against that system's own log before the brief is sent.
  The log command and its output reference then replace the inference in Observed.
- An inferred premise about something not running (a design intent, a plan) may go out
  as Inferred; the reviewer weighs it as unproven.
- The table carries facts and their evidence, not the builder's reasoning.
