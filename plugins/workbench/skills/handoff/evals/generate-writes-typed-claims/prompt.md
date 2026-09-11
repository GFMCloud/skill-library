---
name: generate-writes-typed-claims
runs: 1
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Bash, Write, Skill]
---
We just finished a short technical session: we created a scratch git repo at
/tmp/eval-handoff-repo, committed one file on a branch called `spike`, and confirmed
`git -C /tmp/eval-handoff-repo branch --show-current` prints `spike`.

Write me a handoff for a fresh session using the handoff skill, including its Typed
Claims block, so the next session can re-check that we're really on the `spike` branch
without re-reading this conversation.
