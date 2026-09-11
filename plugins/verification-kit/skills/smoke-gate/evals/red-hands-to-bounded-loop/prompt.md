---
name: red-hands-to-bounded-loop
runs: 1
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Bash, Skill]
---
I ran the smoke script we generated earlier and the "routes" assertion came back
red (exit 1) on the live pass against https://staging.example.com/. Everything else
passed. What do I do with this result?
