---
name: four-fields-per-claim
runs: 1
max_turns: 4
timeout_seconds: 120
allowed_tools: [Read, Skill]
---
Use the evidence-report skill to write up these two checks I already ran. Do not
re-run anything; format what is here.

Claim 1: the validator passes on the library.
Command: bash scripts/validate-skills.sh
Output it returned: "56 skills checked: 0 failures, 41 warnings" and exit code 0.

Claim 2: the inventory is current.
Command: bash scripts/generate-inventory.sh && git diff --stat docs/inventory.md
Output it returned: "wrote docs/inventory.md: 56 skills" and an empty diff.

Not checked: CI on the remote, because the branch is not pushed yet.
