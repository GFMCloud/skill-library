---
name: transition-reports-once
runs: 1
max_turns: 6
timeout_seconds: 120
allowed_tools: [Read, Bash]
---
Use the change-watch skill at
plugins/long-projects/skills/change-watch/SKILL.md. A seen-index at
plugins/long-projects/skills/change-watch/fixtures/seen-index-ok.yaml (a FIXTURE)
currently records source cloudwatch:demo-alarm-fixture at state OK. The
source has just moved to state ALARM.

Copy the fixture to a scratch file first (do not edit the fixture in place).
Run the skill's own step script against the scratch copy to determine
whether this cycle should report, and tell me: does this cycle produce a
report, and what does the seen-index's last_reported field say afterward?
