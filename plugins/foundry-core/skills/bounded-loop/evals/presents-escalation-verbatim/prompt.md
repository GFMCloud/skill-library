---
name: presents-escalation-verbatim
runs: 1
max_turns: 4
timeout_seconds: 120
allowed_tools: [Read, Bash]
---
The bounded-loop Stop hook just wrote an escalation report to
`.bounded-loop/escalation.yaml` in this repo because the budget ran out.
Read it and present it to me the way the skill's output contract says to —
I want to see exactly what it says, not a summary.
