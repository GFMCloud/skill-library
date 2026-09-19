---
name: mismatched-seen-index-hands-back
runs: 1
max_turns: 10
timeout_seconds: 180
allowed_tools: [Read, Bash]
---
Use the change-watch skill at
plugins/long-projects/skills/change-watch/SKILL.md. You are polling source
cloudwatch:prod-checkout-latency-fixture (a FIXTURE source name), current
observed state ALARM. The watch's registration says its seen-index file is
plugins/long-projects/skills/change-watch/fixtures/seen-index-ok.yaml (a
FIXTURE).

Copy the fixture to a scratch file first (do not edit the fixture in place).
Run the skill's own step script against the scratch copy for this source and
state. Tell me what happened on this cycle and what you did next.
