---
name: not-verified-list-when-nothing-skipped
runs: 1
max_turns: 4
timeout_seconds: 120
allowed_tools: [Read, Skill]
---
Use the evidence-report skill on this one claim. Everything I care about was
checked; I do not think anything was skipped.

Claim: the plugin cache holds the real skill file, not an empty directory.
Command: wc -c ~/.claude/plugins/cache/gfm-foundry/foundry-core/0.3.0/skills/proof-of-work/SKILL.md
Output: "4211 /Users/gfm/.claude/plugins/cache/gfm-foundry/foundry-core/0.3.0/skills/proof-of-work/SKILL.md", exit 0.

Write the report. Do not run anything.
