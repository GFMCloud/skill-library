---
name: clean-draft-still-reports-scope
runs: 1
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Write, Bash, Skill]
---
Use the output-lint skill on this draft. Save it as `draft.md`, run this skill's
`output_lint.py` on it, and tell me whether it is clear to send.

---
The validator passes on the branch. The two files changed are listed below.

- docs/inventory.md
- CHANGELOG.md
---
