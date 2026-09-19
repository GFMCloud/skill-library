---
name: resume-verifies-typed-claims
runs: 1
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Bash, Skill]
---
A teammate just uploaded a handoff file from a previous session:
`plugins/long-projects/skills/handoff/fixtures/FIXTURE-mismatch-handoff.md`.

Read it, then follow the handoff skill's Resume Mode before doing anything else. Do not
start any of the work the handoff describes.
