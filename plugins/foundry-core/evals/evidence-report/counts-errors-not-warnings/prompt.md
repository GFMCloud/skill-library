---
name: counts-errors-not-warnings
runs: 1
max_turns: 4
timeout_seconds: 120
allowed_tools: [Read, Skill]
---
Use the evidence-report skill to write up this one check I already ran on the
FIXTURE plugin cache. Do not re-run anything; format what is here.

Claim: the FIXTURE plugin cache passes validation after the rename.
Command: bash scripts/validate-skills.sh
Output it returned: "Validation passed with warnings: 47 warnings, 0 errors"

Nothing else was checked.

Write the report.
