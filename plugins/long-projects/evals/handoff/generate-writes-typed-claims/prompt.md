---
name: generate-writes-typed-claims
runs: 1
max_turns: 12
timeout_seconds: 240
allowed_tools: [Read, Bash, Write, Skill]
---
FIXTURE setup, do this first and do not ask about it: in the current folder create
`spike/notes.txt` containing the single line `branch: spike`, and confirm
`cat spike/notes.txt` prints `branch: spike`. Do not use git; the run's sandbox does not
allow it. Treat that as the short technical session we just finished.

Write me a handoff for a fresh session using the handoff skill, including its Typed
Claims block, so the next session can re-check what is in `spike/notes.txt` without
re-reading this conversation.
Save the handoff in the current folder as exactly `handoff-eval.md`.
