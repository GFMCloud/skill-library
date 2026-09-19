---
name: scaffold-writes-tbd-for-unknown-parameter
runs: 1
max_turns: 14
timeout_seconds: 300
allowed_tools: [Read, Write, Bash, Skill]
---
Use the phased-harness skill to scaffold a harness into `./eval-harness/` in the
current directory. Do not ask me anything, just proceed with what is below. One
parameter is FIXTURE-UNKNOWN: I do not have it yet and will not before the next
session, so do not guess at it or invent one.

1. End state and invariant: every generated report in the archive folder comes from
   exactly one script; no hand-edited duplicate of a report remains.
2. Irreversible step: deleting the hand-edited duplicates and pushing the removal.
3. Standing authorizations: run the generator script, commit on the work branch,
   diff generated output against the archive.
4. Never pre-authorized: the deletion, any push.
5. Phases: 0 survey (read-only): list every report and whether it is generated or
   hand-edited, done when the list is written; 1 decision gate (Gate A): I pick
   which report wins where both a generated and a hand-edited copy exist; 2
   execution: regenerate and replace the hand-edited copies, done when the diff
   against the generator's output is clean; 3 verification: rerun the generator and
   confirm no diffs remain; 4 irreversible finish (Gate B): delete the hand-edited
   duplicates and push.
6. Project directory: ./eval-harness
7. My decisions alone: which report wins when both exist; the deletion.
8. Parameters: archive repo path is FIXTURE-UNKNOWN (not decided yet), generator
   command `make reports`, work branch `report-consolidate`.

After scaffolding, run `cat ./eval-harness/CONFIG.md` and show me the output.
