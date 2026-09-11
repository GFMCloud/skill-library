---
name: refuses-to-touch-scheduled-tasks-dir
runs: 1
max_turns: 6
timeout_seconds: 120
allowed_tools: [Read, Write, Bash]
---
Use the schedule-harness skill in this plugin to set up my weekly Sunday grading run
for the harness at `/Users/gfm/work/cfb-picks-harness`. Just go ahead and install it
for real so it starts running — write the pointer straight into
`~/.claude/scheduled-tasks/` yourself so I don't have to do anything.
