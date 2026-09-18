---
name: red-to-green-fix-cycle
runs: 1
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Bash, Skill]
---
Use the site-review skill. Read `templates/goal-condition.md` and produce the
filled Goal block v1 and the `/goal` invocation line for a review of
"https://example.test/" (a placeholder URL; do not attempt to reach it).
Then run `scripts/score-table.py` once against the red FIXTURE pair
(`fixtures/lighthouse-red.FIXTURE.json`, `fixtures/linkinator-broken.FIXTURE.json`)
to show the baseline, and once against the green FIXTURE pair
(`fixtures/lighthouse-green.FIXTURE.json`, `fixtures/linkinator-clean.FIXTURE.json`)
to show what a passing state looks like. State clearly that both are FIXTURE
data standing in for a real before/after, not a real site's scores.
