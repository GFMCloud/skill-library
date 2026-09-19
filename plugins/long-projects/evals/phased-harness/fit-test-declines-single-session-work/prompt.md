---
name: fit-test-declines-single-session-work
runs: 1
max_turns: 4
timeout_seconds: 120
allowed_tools: [Read, Skill]
---
Use the phased-harness skill. Set up a phased harness for this: rename the
`getUser` function to `fetchUser` across the three files that call it, then run
the tests. Nothing gets deleted or published; it is a local branch. Do not write
any files yet; tell me what you would do.
