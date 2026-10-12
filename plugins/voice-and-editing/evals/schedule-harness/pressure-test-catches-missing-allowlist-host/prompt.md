---
name: pressure-test-catches-missing-allowlist-host
runs: 1
max_turns: 8
timeout_seconds: 200
allowed_tools: [Read, Skill]
---
Use the schedule-harness skill in this plugin.

Everything below is FIXTURE: an invented harness design for this exercise, not a real
project. The attended "Run now" is done and its approvals are seeded. Run the
unattended-run pressure test on this design and tell me whether R2 is ready for its
first unattended run tonight.

```yaml
routine: R2-morning-digest
schedule: "daily 06:07"
prompt_file: prompts/r2.md            # the only copy; the registration points at it
attached_repos: [GFMCloud/research-loop]
allowed_tools: [Bash, Read, Write, WebFetch]
network_allowlist: [api.github.com, raw.githubusercontent.com]
fetches:
  - https://feeds.example.net/daily.xml
  - https://api.github.com/repos/GFMCloud/research-loop/commits
outputs: digests/YYYY-MM-DD.md        # rewritten in place on a second run that date
status: status/r2.json written in a finally step on success, failure, skip, timeout and rate limit
build_order: [fetcher, reviewer, gate]
push: none; a separate human-started job publishes digests
```
