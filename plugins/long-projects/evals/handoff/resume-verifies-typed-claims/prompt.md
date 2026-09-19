---
name: resume-verifies-typed-claims
runs: 1
max_turns: 14
timeout_seconds: 180
allowed_tools: [Read, Bash, Skill]
---
A teammate just uploaded a handoff file from a previous session. It is
`fixtures/FIXTURE-mismatch-handoff.md` inside the handoff skill's own folder (the base
directory the skill reports when it loads), not in the current folder.

Read it, then follow the handoff skill's Resume Mode before doing anything else. Do not
start any of the work the handoff describes.
