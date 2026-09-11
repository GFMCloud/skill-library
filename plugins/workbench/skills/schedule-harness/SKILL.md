---
name: schedule-harness
description: >-
  Scaffold a scheduled-task pointer that runs one phase or mode of an existing
  phased harness (built by phased-harness) unattended on a cadence — a thin
  pointer file to the harness's own `/phase` skill, plus the absolute-limits
  block that bounds what an unattended run may do. Use when a harness phase
  should run on Sundays, nightly, weekly, or any recurring schedule without
  someone starting it by hand — "schedule this phase", "run my harness on a
  cadence", "set up a recurring /phase run", "turn this into a scheduled
  task", or naming a desktop scheduled task or cron-style run of a `/phase`
  skill. Produces the pointer file and the registration values only; it never
  registers the task itself and never writes under `~/.claude/`. Not for
  scheduling arbitrary prompts with no harness behind them (that is the
  built-in `/loop` or a plain desktop scheduled task with its own prompt) and
  not for cloud-triggered work with no local file access (that is a Routine).
metadata:
  maturity: incubator
---

# schedule-harness

Wraps the Desktop app's scheduled tasks (or, for a non-Desktop scheduler, headless
`claude -p` with `--permission-prompts none`) around one phase or mode of an existing
phased harness. It renders a **Scheduled-task pointer v1** file — a thin pointer to the
harness's own `/phase` skill, per the interface spec's composition map: this skill
wraps a first-party primitive, it does not reimplement dispatch logic. The dispatch
logic stays in the harness's `/phase` skill, which is the one editable home for it.

Background reading, not restated here: [references/platform-facts.md](references/platform-facts.md)
(primary-source quotes on permission mode, overlap skip, catch-up, the worktree
toggle, and the pointer file's own location and format) and
`/Users/gfm/skill-library/plugins/workbench/skills/phased-harness/SKILL.md` (how the
harness this skill schedules is built — read for the shape, never duplicated here).

## Inputs

- Harness path (absolute) — the phased-harness project directory.
- The phase skill's absolute path (normally `<harness>/.claude/skills/phase/SKILL.md`).
- Mode — `continuous` (bare `/phase`) or a named phase/mode the harness's dispatch
  skill accepts (e.g. `grade`, `3`, `publish`).
- Cadence — in the Desktop app's own schedule-picker vocabulary (manual, hourly,
  daily, weekdays, weekly) or plain language for an interval the picker does not offer.
- The absolute-limits list's two numeric values: hook timeout (seconds) and the
  consecutive-retry cap on a failed or rate-limited step.
- Spend cap and report mode, if the harness's own CONFIG.md does not already state
  them — these go into the prompt as guardrail text, not into the pointer's fixed
  Absolute-limits block v1.

A run with any of these missing is not scaffolded; ask for the missing value rather
than inventing one (the harness project's own CLAUDE.md may already state most of
them — read it first).

## Verify

Run `scripts/check-pointer.py <rendered-pointer.md>` against the file
`scripts/render-pointer.py` produced. Exit 0 and the line `OK` means every structural
check in the interface spec's section 7 held: frontmatter has exactly `name` and
`description`; the body names the harness directory as an absolute path, the phase
skill by an absolute path, and a mode; every line of the Absolute-limits block v1 is
present, with the hook-timeout and retry-cap lines filled with integers, not
placeholders. A non-zero exit prints one `FAIL <code> <message>` line per defect —
fix the input and re-render, never hand-edit the rendered file to make the checker
pass.

This checker is structural. It cannot verify that a scheduled run actually honors the
limits it names — that is `## Done when`, proven by the first two real runs' logs
after registration, not by this script.

## Done when

- The pointer file renders clean (`check-pointer.py` exits 0) and matches the harness's
  actual paths — a `git -C <harness_path> rev-parse` or an `ls` on the phase skill path
  is how that gets confirmed before handing the pointer to Graham, not assumed from the
  input file.
- Graham (in the Desktop app) or the `mcp__scheduled-tasks__create_scheduled_task`
  tool, with his approval, has registered the task with: the rendered pointer's body as
  the instructions, the permission mode set explicitly (not left on a default), and one
  attended "Run now" completed so its saved approvals are seeded.
- Two unattended runs have completed with green run logs, and each run's own summary
  names its actual outcome (what ran, what got queued to Tier 3, any retry) rather than
  reporting a bare green status — see the roadmap's Success line and the FIXTURE run
  log shape in [fixtures/FIXTURE-run-log-excerpt.md](fixtures/FIXTURE-run-log-excerpt.md).
- A run started while a previous run of the same task was still in progress was skipped
  with the platform's own overlap-skip reason, observed in run history — never
  re-implemented by this skill or the pointer's prompt.

## Stop when

- Any input in `## Inputs` is missing and the harness's own CONFIG.md or CLAUDE.md
  does not supply it — ask, do not invent a value (a guessed hook timeout or retry cap
  is exactly the kind of unbounded-cost mistake the Absolute-limits block exists to
  prevent).
- `check-pointer.py` cannot be made to pass without weakening a limit line (for
  example, a harness whose phase genuinely needs to push or delete) — that is a
  collision with the invariant this skill enforces, not a bug in the checker; stop and
  say which limit collides, per the source project's own "constitution conflict is a
  stop, not a tiebreak" rule.
- The rendered pointer is ready but registration would require this skill to write
  under `~/.claude/scheduled-tasks/` or anywhere under `~/.claude/` itself — it never
  does this (see "Registration" below); hand the file and the values to Graham instead
  of attempting a workaround.
- A run's actual behavior (once registered) does not match its own summary — a green
  status with an unlogged push, an unlogged deletion, or a limit silently exceeded is a
  failure of this skill's contract per the roadmap's Failure line, not a passing run
  with a cosmetic issue.

## Scaffold the pointer

1. Read the harness's `CLAUDE.md`, `CONFIG.md`, and `.claude/skills/phase/SKILL.md` to
   confirm the phase or mode requested exists and to find any cadence, spend-cap, or
   report-mode values already recorded there.
2. Write the render input (YAML or JSON) with the seven fields
   `scripts/render-pointer.py` requires: `name`, `description`, `harness_path`,
   `phase_skill_path`, `mode`, `hook_timeout`, `retry_cap`. Keep `name` short and
   kebab-case-friendly — the platform lowercases and kebab-cases it into the task's
   folder name regardless.
3. Render: `python3 scripts/render-pointer.py <input.yaml> -o <output.md>`. The script
   reads [templates/pointer.md](templates/pointer.md) — the one editable home for the
   pointer's shape — and fails loudly (exit 2) on a missing field or an unresolved
   placeholder rather than emitting a partial file.
4. Check: `python3 scripts/check-pointer.py <output.md>`. Fix the input and re-render
   on any `FAIL` line; never hand-edit the rendered output.
5. Hand Graham the checked file's contents as the task's instructions, plus the
   registration values that do not live in the pointer file itself (per
   [references/platform-facts.md](references/platform-facts.md): "Schedule, folder,
   model, and enabled state are not in this file"): the cadence, the working folder
   (`harness_path`), the model, and whether to enable the worktree toggle.

## Permission mode, saved approvals, and headless runs `[R]`

Set the task's permission mode explicitly at registration — never leave it on
whatever the picker defaults to. Seed its saved approvals with one attended "Run now"
before trusting it to run unattended: watch the first run for permission prompts and
select "always allow" on each ("Future runs of that task auto-approve the same tools
without prompting", [references/platform-facts.md](references/platform-facts.md)). For
a phase run by a non-Desktop scheduler (cron, launchd, CI) instead of the Desktop
app's own task runner, use headless `claude -p` with `--permission-prompts none`
(available from Claude Code 2.1.259 — research record R-6); this is the equivalent of
saved approvals for a host with no UI to click "always allow" in.

## Overlap skip and the time guard `[R]`

Rely on the platform's built-in overlap skip — "the previous run was still in
progress" is a run-history reason the platform produces on its own
([references/platform-facts.md](references/platform-facts.md)); do not add a lock file
or a second overlap check into the harness's `/phase` skill for this.

Do write a time guard into the pointer's prompt, because a missed run is caught up
exactly once at wake time, at whatever time the computer actually wakes, not the
scheduled time: state in the instructions what the run should do if it is firing late
(skip stale work, only act on what changed since the last successful run, or name a
cutoff). See [references/platform-facts.md](references/platform-facts.md), "Catch-up",
for the platform's own worked example of this guard.

## Worktree toggle

Offer the worktree toggle whenever the scheduled phase does not need to commit to the
harness's own tree (a read-only survey phase, a grading pass that writes its own
output file, a probe). Recommend against it when the phase's job is exactly to commit
to the harness tree (per phased-harness's own convention, path-scoped commits at phase
boundaries) — an isolated worktree there would make the commit invisible to the next
run. State the recommendation; the choice is Graham's, made at registration.

## Absolute-limits block v1 `[R]`

Every rendered pointer carries the full block from
[templates/limits-block.md](templates/limits-block.md) — reproduced here from the
interface spec, section 7, referenced by name and version, never redefined:

- no git push
- no deletion (rename to .superseded)
- no credentials
- no edits under ~/.claude/plugins/
- no edits to the harness's own CONFIG.md, CLAUDE.md, or prompts/
- no edits in a repo with uncommitted changes this run did not make
- hook timeout: `<seconds>`
- consecutive-retry cap on a failed or rate-limited step: `<n>`
- anything the run would have asked becomes a queued Tier 3 item

The hook-timeout and retry-cap lines exist because the research record's secondary
findings name hook recursion without a timeout, and rate-limit-as-success retry
storms, as cost-runaway root causes distinct from ordinary spend (research record,
T7). A run that hits either cap stops that step and logs it — it does not keep
retrying, and it does not treat a rate limit as a green result.

The last line is the exception-only summary rule: a scheduled run has nobody watching
it, so anything Graham would have been asked in an interactive session becomes a
queued Tier 3 item instead (illustrated in
[fixtures/FIXTURE-run-log-excerpt.md](fixtures/FIXTURE-run-log-excerpt.md)). This
mirrors the weekly maintainer's own tier policy — see
`/Users/gfm/work/claude-improvements-weekly/CLAUDE.md`, "Tiers are binding" (read-only
reference; that harness's queue and ratify mode are not duplicated here, only the
pattern).

## Tier 3 queue and `/phase publish` are separate-job "safe outputs" `[R]`

Keep the Tier 3 queue and the harness's own gated `/phase publish` (or equivalent
push/apply mode) as a separate job from the scheduled run, rather than letting the
scheduled run apply a gated action itself. This is the same shape as GitHub Agentic
Workflows' "safe outputs" pattern — an agent's writes land in a separate job with
separate permissions (research record, R-10) — applied here as: the scheduled run logs
and queues, a human-triggered session (or its own gated mode) applies. A scheduled task
that both proposes and applies an irreversible action collapses the separation this
skill exists to keep.

## Registration — never done by this skill

Registering the task is Graham's action in the Desktop app, or the
`mcp__scheduled-tasks__create_scheduled_task` tool with his explicit approval. This
skill hands over the exact pointer file contents and the registration values (cadence,
folder, model, worktree choice); it does not call that tool unprompted and does not
create, edit, or list anything under `~/.claude/scheduled-tasks/` or anywhere under
`~/.claude/` — a hard boundary for this skill, not a preference. The FIXTURE pointer
renders in this skill's own `fixtures/` directory prove the template and the checker
without ever touching that path.

## Validation

First run's log shows the limits honored (no push, no deletion, no credential access,
hook timeout and retry cap never silently exceeded) and a queued Tier 3 item wherever a
question would otherwise have been asked. A second run started during the first is
skipped, and the run history names the built-in reason. See
[fixtures/FIXTURE-run-log-excerpt.md](fixtures/FIXTURE-run-log-excerpt.md) for the
illustrative shape of both — a FIXTURE, not a real run.

## Output contract

Produces a **Scheduled-task pointer v1** file and, embedded in it, an
**Absolute-limits block v1**, both as defined in the harness interface spec
(`/Users/gfm/work/toolkit-build-harness/docs/interface-spec.md`, section 7) — reference
by name and version; this file and its templates never redefine either shape, they
render and check it. Nothing consumes this skill's output within the toolkit (the
composition map lists no consumer); the pointer's consumer is the scheduled-task
platform itself, once Graham or the create-task tool registers it.
