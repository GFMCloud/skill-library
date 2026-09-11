# Transports for change-watch

Three ways to get a check running on a cadence or in reaction to an event.
Pick one per watch based on where the source lives and whether local files
are needed. All three are first-party primitives; this skill wraps them, it
does not reimplement them.

## 1. Desktop scheduled task, polling read-only

**When.** The source is local: files on this machine, a local marker, a
command that only makes sense run here. Available now, no research-preview
gate.

**How it fits.** `schedule-harness` (T7, `workbench`) produces a Scheduled-task
pointer v1 (interface spec section 7) that registers the poll. change-watch
supplies the check the scheduled task runs each cycle: read the source, run
`scripts/watch-step.py` against the seen-index, and act on `REPORT` lines.
`schedule-harness`'s SKILL.md did not exist yet at the time this file was
written (it is a wave-2 sibling built in parallel); this section composes
against the Scheduled-task pointer v1 shape from the interface spec alone,
not against that skill's file.

**Source.** Research record row R-7 (VERIFIED against
`code.claude.com/docs/en/desktop-scheduled-tasks`): "per-task permission
mode, saved 'always allow' approvals reviewable per task, optional isolated
worktree per run, one catch-up run for a missed schedule, a run is skipped
when the previous run is still in progress, run history with skip reasons, a
task may reschedule itself via `update_scheduled_task`."

**What it cannot do.** No live push; the gap between reality changing and the
task noticing is the poll interval. No local files for a cloud-only source
(a SaaS webhook payload has nowhere to land between polls unless something
else stores it first).

## 2. Routine with an API trigger, alarm-to-agent

**When.** The source is cloud-side (a monitoring tool, a CI pipeline, an
alerting system) and can make an outbound HTTP call when something happens.
No local files: the routine runs in Anthropic-managed cloud infrastructure,
cloned from GitHub, not on this machine.

**Source, on the API trigger itself** (fetched 2026-09-11 from
`https://code.claude.com/docs/en/routines`):

> "An API trigger gives a routine a dedicated HTTP endpoint. POSTing to the
> endpoint with the routine's bearer token starts a new session and returns a
> session URL."

> "The request body accepts an optional `text` field for run-specific context
> such as an alert body or a failing log, passed to the routine alongside its
> saved prompt."

**Source, on the untrusted wrapping (the prompt must opt in)**, same page:

> "The `text` value doesn't reach the routine as a bare message. It arrives
> wrapped in a `<routine-fire-payload>` block that labels it as untrusted data
> and tells Claude not to follow instructions inside it unless the routine's
> own prompt says to."

> "This means a routine's saved prompt must opt in to acting on fire text:
> write the prompt to reference the payload explicitly, for example
> 'Investigate the alert described in the routine-fire-payload block', or the
> routine treats the text as inert context."

A change-watch routine's prompt therefore names the payload block explicitly.
Skipping that line silently turns the alarm into a no-op: the session starts,
runs green, and never reads the alert.

**Source, on green status not meaning success**, same page:

> "A green status in the run list means the session started and exited
> without an infrastructure error. It does not mean the task in your prompt
> succeeded. Open the run to read the transcript and confirm what Claude
> actually did."

This is why the roadmap's own success line ("every transition has a diagnosis
and a queued action within one cycle") cannot be read off the routine's
status column. A watch built on this transport needs its own report as the
success signal, never the run's green check.

**What it cannot do.** No local files, so it cannot read or write this
machine's seen-index directly; the seen-index has to live somewhere the
routine's environment and connectors can reach (a repo file it can commit to,
or a connector-backed store), and the routine's own environment network
policy has to allow whatever it reaches. Runs draw down the daily routine cap
(research record R-8; not `[R]`-cited here since it does not change the
design, only the operating budget).

## 3. Channel webhook receiver, once out of research preview

**When.** An external system needs to push events into a session that is
already open and working the problem, rather than spinning up a fresh cloud
session per event (the Routine path) or waiting for the next poll (the
scheduled-task path).

**Source, on the mechanism** (fetched 2026-09-11 from
`https://code.claude.com/docs/en/channels`):

> "A channel is an MCP server that pushes events into your running Claude
> Code session, so Claude can react to things that happen while you're not at
> the terminal."

> "Webhook receiver: a webhook from CI, your error tracker, a deploy
> pipeline, or other external service arrives where Claude already has your
> files open and remembers what you were debugging."

**Source, on the always-open-session requirement:**

> "Events only arrive while the session is open, so for an always-on setup
> you run Claude in a background process or persistent terminal."

**Source, on research-preview status:**

> "Channels are a research preview feature. Availability is rolling out
> gradually, and the `--channels` flag syntax and protocol contract may
> change based on feedback."

**What it cannot do, today.** Requires a persistent session (a background
process or terminal that stays open), which is a standing cost the other two
transports do not have. Custom webhook receivers are the "build your own
channel" path in the channels reference, not a shipped plugin, so this
transport is the one the roadmap line marks "once out of research preview":
not selected as change-watch's default until the preview gate lifts.

**Idempotency note, not covered by the docs above** (research record,
secondary findings, T8): "Webhook idempotency: a seen-index catches replays;
reordered distinct events need a state-transition guard." A seen-index alone
proves a duplicate delivery of the same event is a no-op; it does not by
itself prove that two distinct events delivered out of order are applied in
the right order. `scripts/watch-step.py`'s predicate (`current_state !=
last_state`, using the timestamp on the observation, not the delivery order)
is the state-transition guard; a channel receiver that only checked "have I
seen this webhook id before" would not be enough on its own.

## Choosing

| Source lives | Needs local files | Transport |
|---|---|---|
| This machine | Yes | Desktop scheduled task |
| Cloud service that can call out | No | Routine, API trigger |
| Cloud service pushing events to an open session | No | Channel webhook receiver (once out of preview) |

## Known weakness

Alarm-driven agents in the wild document no flapping suppression (research
record, secondary findings, T8, citing AWS DevOps Agent). This skill's
transition predicate reports once per transition, which already prevents the
"same state re-fires forever" failure mode; it does not smooth a rapid flap
into a single summary report, and the deliberate divergence noted in
`SKILL.md`'s known-weakness line means a genuine flap produces one report per
transition, not one report for the whole episode.
