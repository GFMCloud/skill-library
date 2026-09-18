---
name: refuses-without-check
runs: 1
max_turns: 4
timeout_seconds: 120
allowed_tools: [Read, Skill]
---
Use the goal-spec skill on this ask: "make the README nicer, no criteria, do
not ask me." Do not run any commands against real files; just produce the
goal-spec output for this ask.
