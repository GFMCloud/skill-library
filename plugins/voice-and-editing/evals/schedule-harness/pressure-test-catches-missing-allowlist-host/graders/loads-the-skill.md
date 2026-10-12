---
type: tool_used
tool: Skill
min: 1
---

Tests `references/unattended-run-pressure-test.md`, item 1: "Every host a routine fetches
from is on that routine's network allowlist". The FIXTURE design holds every other item
and fetches from `feeds.example.net`, which its allowlist does not name. The case only
tests schedule-harness's own checklist if the skill fired.
