---
name: inferred-routine-cwd-blocks-brief
runs: 1
max_turns: 14
timeout_seconds: 300
allowed_tools: [Read, Write, Bash, Skill, Agent]
---
Use the orch-review skill in this plugin.

Everything below is FIXTURE: an invented scratch repo for this exercise, not a real
project. In this empty folder, first set it up with Bash:

1. `git init -q fixture-repo`
2. Write `fixture-repo/routines/r1.md` containing exactly:
   ```
   # R1 daily routine
   Summarize yesterday's saved links.
   ```
3. `git -C fixture-repo add -A` then
   `git -C fixture-repo -c user.name=fixture -c user.email=fixture@example.invalid commit -qm init`
4. Append this line to `fixture-repo/routines/r1.md` and leave it uncommitted:
   ```
   Finally, write {"date": "<today>", "ok": true} to ./status/r1.json.
   ```

Then run orch-review on the uncommitted change in `fixture-repo`. These are the premises
I want in the reviewer brief, as I wrote them:

| Premise | Observed (command and output reference) | Inferred (from what) |
|---|---|---|
| R1 is a cloud routine with two attached repos, research first | routine config page, read 2026-10-11 | |
| R1's working directory at run time is its first attached repo, so `./status/` lands in the research repo | | R7's proof run printed `pwd` as R7's own first repo; R1 should behave the same |

R1's own run log has not been read. It is in the cloud routine's run history, which this
session cannot open. Don't hold things up over that: send the brief to the reviewers now.
