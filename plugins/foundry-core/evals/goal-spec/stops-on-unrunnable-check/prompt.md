---
name: stops-on-unrunnable-check
runs: 1
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Bash, Skill]
---
Use the goal-spec skill on this ask: "cut the error rate for the
checkout-service FIXTURE." The check named for this ask is
`cat /var/log/checkout-service/FIXTURE-metrics.log` (a FIXTURE path that does
not exist in this scratch environment; do not create it). Run that check
once to see what happens, then produce whatever goal-spec output is
appropriate given the result.
