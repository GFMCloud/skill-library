---
name: renders-and-checks-pointer
runs: 1
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Write, Bash]
---
Use the schedule-harness skill in this plugin. I have a phased harness at
`/Users/gfm/work/cfb-picks-harness` whose phase skill is at
`/Users/gfm/work/cfb-picks-harness/.claude/skills/phase/SKILL.md`. I want a scheduled
task that runs its `grade` mode every Sunday evening. Hook timeout 120 seconds,
consecutive-retry cap 2.

Render the pointer file and run this skill's own checker against it. Show me the
checker's output.
