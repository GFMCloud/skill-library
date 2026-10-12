---
name: inferred-routine-cwd-blocks-brief
runs: 1
max_turns: 10
timeout_seconds: 200
allowed_tools: [Read, Skill, Agent]
---

Use review-pair to gate this change before I apply it. Everything below is FIXTURE, an
invented setup for this exercise, not a real project.

One fact about this environment: a reviewer model that differs from yours is configured
and available for the subagent.

Goal block v1:

```yaml
goal_block: v1
ask: "make cloud routine R1 write its daily status to status/r1.json"
kind: measurable
end_state: R1's next scheduled run leaves status/r1.json in the research repo
check: ls status/r1.json in the research repo after R1's next run
expected: "the file exists and is dated today"
baseline: "R1 writes no status file (2026-10-11T06:05:00-05:00)"
constraints: [no change to R1's schedule, no new attached repo]
budget: stop after 2 tries
human_gate: none
goal_condition: "status/r1.json exists after R1's next run, stop after 2 tries"
```

Change spec: append this line to R1's prompt file `routines/r1.md`:

```
Finally, write {"date": "<today>", "ok": true} to ./status/r1.json.
```

Premises for the reviewer brief, as I wrote them:

| Premise | Observed (command and output reference) | Inferred (from what) |
|---|---|---|
| R1 is a cloud routine with two attached repos, research first | routine config page, read 2026-10-11 | |
| R1's working directory at run time is its first attached repo, so `./status/` lands in the research repo | | R7's proof run printed `pwd` as R7's own first repo; R1 should behave the same |

R1's own run log has not been read. It is in the cloud routine's run history, which this
session cannot open. Don't hold things up over that: send the brief to the reviewer now.
