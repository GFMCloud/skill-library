---
name: fixture-gate-fails
runs: 1
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Bash, Skill]
---
Use the design-jury skill. There is no network in this eval, so do not run the capture
script and do not spawn judge subagents. Three judge passes for one page already exist
in the skill's `fixtures/` directory: `generic-template.judge-1.FIXTURE.json`,
`generic-template.judge-2.FIXTURE.json` and `generic-template.judge-3.FIXTURE.json`.
Run `scripts/aggregate.py` on them with `references/floors-web.json` and purpose
`showcase`, writing to a temporary directory, and report the verdict and the categories
below floor. Label the result as coming from FIXTURE data, not a real site.
