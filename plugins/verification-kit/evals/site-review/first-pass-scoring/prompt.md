---
name: first-pass-scoring
runs: 1
max_turns: 6
timeout_seconds: 120
allowed_tools: [Read, Bash, Skill]
---
Use the site-review skill to score a site. Instead of running real Lighthouse
and linkinator commands (no network access in this eval), use the FIXTURE
files already in this skill's `fixtures/` directory:
`fixtures/lighthouse-red.FIXTURE.json` and
`fixtures/linkinator-broken.FIXTURE.json`. Run `scripts/score-table.py`
against that pair and report the scored table, clearly labeling it as coming
from FIXTURE data, not a real site. Include the two mandatory labels about
the performance and accessibility scores in your report.
