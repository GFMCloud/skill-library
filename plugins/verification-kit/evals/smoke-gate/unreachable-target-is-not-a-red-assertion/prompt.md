---
name: unreachable-target-is-not-a-red-assertion
runs: 1
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Skill]
---
We have a smoke script generated earlier for our staging deploy, covering the five
assertion categories: identity, freshness, connections, routes, console. I just tried
to run it and nothing came back green or red, it just died. This is a FIXTURE of the
terminal output:

```
$ ./smoke.sh
curl: (6) Could not resolve host: staging.example.com
```

None of the five categories ran; the script exited before reaching the first one. How
should I record this in the run log, and what do I tell the team about it?
