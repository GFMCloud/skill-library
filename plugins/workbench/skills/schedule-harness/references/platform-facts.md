# Platform facts: Desktop scheduled tasks

Fetched from https://code.claude.com/docs/en/desktop-scheduled-tasks on 2026-09-11
(WebFetch succeeded; quoting the pages's own words, not a paraphrase). These are the
primary-source lines this skill's claims rest on, corresponding to research record
rows R-6 and R-7. See also `/Users/gfm/work/ai-workflow-roadmap/research-2026-09-11.md`.

## Permission mode and saved approvals

> "Each task has its own permission mode, which you set when creating or editing the
> task."

> "If a task runs in Manual mode and needs to run a tool it doesn't have permission
> for, the run stalls until you approve it. The session stays open in the sidebar so
> you can answer later."

> "To avoid stalls, click **Run now** after creating a task, watch for permission
> prompts, and select 'always allow' for each one. Future runs of that task
> auto-approve the same tools without prompting. You can review and revoke these
> approvals from the task's detail page."

This is the primary source for the roadmap's `[R]` step: "set the task's own
permission mode explicitly and seed its saved approvals with one attended 'Run now'."

> "Review allowed permissions: see and revoke saved tool approvals for this task from
> the Always allowed panel"

## Overlap skip

> "Hover a skipped entry to see why: your computer was asleep, the previous run was
> still in progress, or other scheduled tasks were already running."

This is the "built-in overlap skip" the roadmap's Steps and Validation lines refer to.
It is observed in run history, not re-implemented by this skill or by the generated
pointer.

## Catch-up (missed runs)

> "When the app starts or your computer wakes, Desktop checks whether each task missed
> any runs in the last seven days. If it did, Desktop starts exactly one catch-up run
> for the most recently missed time and discards anything older. A daily task that
> missed six days runs once on wake. ..."

> "Keep this in mind when writing prompts. A task scheduled for 9am might run at 11pm
> if your computer was asleep all day. If timing matters, add guardrails to the prompt
> itself, for example: "Only review today's commits. If it's after 5pm, skip the
> review and just post a summary of what was missed.""

This is the primary source for the roadmap's "write a time guard into the prompt
because a missed run is caught up once at wake time" step.

## Worktree option

> "By default, scheduled tasks run against whatever state your working directory is
> in, including uncommitted changes. Enable the worktree toggle when creating the task
> to give each run its own isolated Git worktree, the same way parallel sessions
> work."

This is the primary source for the roadmap's "offer the worktree toggle where the
phase does not need to commit to the harness's own tree" step.

## Run history and skip reasons

> "Review history: see every past run, including skipped runs. Hover a skipped entry
> to see why: your computer was asleep, the previous run was still in progress, or
> other scheduled tasks were already running. Click Show more to load older entries."

## `update_scheduled_task` (self-rescheduling)

> "A scheduled task can also modify its own schedule or prompt from within a running
> session using the `update_scheduled_task` MCP tool. This lets a task reschedule
> itself based on what it finds, for example, rescheduling a code review to run
> earlier when it detects a release branch has been created."

## Pointer file location and format

> "To edit a task's prompt on disk, open `~/.claude/scheduled-tasks/<task-name>/SKILL.md`
> (or under `CLAUDE_CONFIG_DIR` if set). The file uses YAML frontmatter for `name` and
> `description`, with the prompt as the body. Changes take effect on the next run.
> Schedule, folder, model, and enabled state are not in this file: change them through
> the Edit form or ask Claude."

This is the primary source for two design decisions in this skill: (1) the pointer's
frontmatter carries only `name` and `description`, every other field (schedule,
folder, model, permission mode) lives in the platform's own task configuration, not in
the file; (2) this skill never writes into `~/.claude/scheduled-tasks/` itself, the
hard boundary in this skill's build brief is also what the platform's own file layout
implies: that path is the platform's, populated when a task is created through the UI,
through natural language in a Desktop session, or through
`mcp__scheduled-tasks__create_scheduled_task`.

## Headless `--permission-prompts none` (R-6)

Not on this page. The desktop-scheduled-tasks doc covers the Desktop app's own task
runner, which has its own per-task permission mode and never needs the headless CLI
flag. The `--permission-prompts none` claim (arrived 2.1.259) is sourced from the CLI
changelog per the research record (R-6, VERIFIED) and applies to the separate case this
skill also covers: a headless `claude -p "/phase ..."` run launched by cron, launchd, or
any scheduler other than the Desktop app's own.

## Scheduled runs can spawn subagents (R-14)

Not documented on this page either way. The research record's R-14 overrides an
earlier secondary claim that scheduled runs cannot spawn subagents: "the maintainer's
first scheduled run on 2026-08-15 spawned ten, per its run log", local evidence beats
doc silence. This skill's pointer and prompt guidance assume subagent fan-out is
available to a scheduled `/phase` run, the same as an interactive one.
