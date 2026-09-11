---
name: change-watch
description: >-
  Turn a source that changes on its own timeline (a CloudWatch alarm, a PR's
  state, a metric, a marker file another process writes) into a registered
  check with a seen-index, so a state transition gets diagnosed and queued
  for action within one cycle and a re-fire in the same state produces zero
  reports. Use when something should be checked on a cadence or reacted to
  when it changes: "watch this alarm", "tell me when this PR is ready",
  "poll for X and only bug me on a change", "re-enable the estate map as
  exception-only", "wait for this marker file". Not for one-shot checks with
  no ongoing cadence (that is a normal command), and not for a transport
  choice you have not yet made — this skill picks the transport as its first
  step. Costs: a scheduled task or Routine gets registered, and a seen-index
  file gets created and updated on every cycle.
metadata:
  maturity: incubator
---

# change-watch

Watches one source for a state transition and reports only on the
transition, never on presence in a fixed state. Composes with
`schedule-harness` (T7, `workbench`) for the polling transport, and with
`smoke-gate` (`verification-kit`) for the staging check a safe action can run
after a transition. See [references/transports.md](references/transports.md)
for the three transports and when each applies, and
[templates/seen-index.md](templates/seen-index.md) for the state file this
skill reads and writes.

## Inputs

- Source and how to read it: a name (`cloudwatch:<alarm>`, a PR number, a
  metric name, a marker file path) and the command or API call that returns
  its current state.
- Seen-index location: one file per source, Seen-index entry v1 (see
  [templates/seen-index.md](templates/seen-index.md)).
- The meaningful-change predicate: by default `current_state != last_state`
  (a transition), never "is this state already in the index." A watch that
  needs a coarser predicate (ignore a specific sub-state change) says so
  explicitly; the default is the one `scripts/watch-step.py` implements.
- Safe actions: what may run without asking (diagnose, draft a fix on a
  branch, run `smoke-gate` against staging).
- Approval-only actions: what gets queued instead of run (deploy, page
  someone, rotate a credential).
- Report mode: where an exception report goes (a file, a channel, a PR
  comment).
- **[R]** Transport: which of the three in
  [references/transports.md](references/transports.md) fits this source.
  This is a decision, not a default; picking wrong means either no local
  file access (chose scheduled task for a cloud-only source) or a standing
  open session nobody asked for (chose channels when a poll would do).

## Verify

Run `scripts/watch-step.py <seen-index> <source> <current-state>` for the
current cycle's observed state. It prints `REPORT <source> <old> -> <new>` on
a transition or `NO-REPORT` otherwise, and updates the seen-index in place:
`last_seen` advances on every call, `last_state` and `last_reported` only on
a transition. On any `REPORT` line, run
`scripts/classify-action.py <rules-file> <action-name>` for each candidate
action before the diagnostic call: it prints `safe` or `approval-only`, or
exits 1 with `unclassified` on stderr for an action the rules file does not
name. An unclassified action is never treated as safe by default.

Replay proof (FIXTURE-labelled, captured in
`/Users/gfm/work/toolkit-build-harness/runs/phase-3/change-watch.md`): a known
transition OK to ALARM produces exactly one `REPORT`; the same ALARM state
replayed three times produces three `NO-REPORT` lines with `last_seen`
advancing and `last_reported` unchanged; a flapping sequence OK, ALARM, OK,
ALARM produces three `REPORT` lines, one per transition. An action absent
from the rules file exits 1 as `unclassified` rather than defaulting to safe.

## Done when

Every transition since the watch was registered has a diagnosis and a queued
or run action within one cycle, the seen-index reflects the current state
with a non-`never` `last_reported` on every source that has ever transitioned,
and zero duplicate reports exist for a source that has not changed state
since its last report.

## Stop when

- The source cannot be read (the command errors, the API call fails, the
  marker file's parent directory does not exist): report the read failure
  itself as an exception, do not silently skip the cycle.
- An action after a transition is not in the classification rules file:
  stop before the diagnostic call and report it as unclassified, per
  `scripts/classify-action.py`'s exit-1 behavior. Do not guess safe.
- The chosen transport hits its own limit (Routine daily run cap, channel
  session not open, scheduled task skipped because the prior run is still in
  progress): report the skip, do not retry in a loop that could compound
  into a rate-limit storm.
- The seen-index file is corrupt or claims a different source than the one
  being polled (`scripts/watch-step.py` refuses this case and exits 1):
  hand back to a human rather than overwriting a possibly-wrong index.

## Known weaknesses

- **Deliberate divergence from the roadmap wording.** The roadmap's
  Validation line says "a flapping sequence triggers one" report. The
  interface spec (section 6, ratified 2026-09-11) rules that a flapping
  sequence A to B to A produces one report per transition, so two for that
  three-state sequence, never one report for the whole episode. This skill
  implements the spec's rule, not the roadmap's literal wording. A watch
  that floods on a genuinely flapping source is a known cost of this choice,
  not a bug; smoothing a flap into one summary report is future work, not
  built here.
- No flapping suppression beyond "one report per transition": alarm-driven
  agents in the wild document none either (research record, secondary
  findings, T8), so this is a shared gap, not a regression.
- `schedule-harness` and `smoke-gate` were both incomplete wave-2 siblings at
  build time (`smoke-gate/SKILL.md` did not exist; `schedule-harness` had no
  skill directory at all). This skill composes against the Scheduled-task
  pointer v1 and Smoke manifest v1 shapes from the interface spec directly,
  not against either sibling's file. Re-verify the composition once both
  land.
- The seen-index parser in `scripts/watch-step.py` is a narrow hand-rolled
  reader for the fixed five-field shape, not a general YAML parser. A
  seen-index file with fields beyond the spec's five, or YAML syntax beyond
  `key: value` lines, is silently ignored rather than rejected.

## Output contract

Consumes and updates a Seen-index entry v1 (harness interface spec, section
6) per source. On a transition classified safe, may hand a Smoke manifest v1
(interface spec, section 5) to `smoke-gate` for a staging check; this skill
never redefines that shape, only names it. Reports exceptions in the report
mode named in Inputs. When the polling transport is a scheduled task, that
task is registered as a Scheduled-task pointer v1 (interface spec, section
7), produced by `schedule-harness`, not by this skill.
