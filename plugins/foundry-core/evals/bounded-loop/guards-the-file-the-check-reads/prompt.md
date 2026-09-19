---
name: guards-the-file-the-check-reads
runs: 1
max_turns: 8
timeout_seconds: 200
allowed_tools: [Read, Bash, Edit, Skill]
---
FIXTURE: an invented repo and check, not a real project.

You have a Goal block v1 whose check is:

  pytest tests/test_login.py::test_reset_flow

with budget 3. This check reads only tests/test_login.py to decide pass or fail; nothing
else in the repo affects its verdict. Use the bounded-loop skill to set this up so the
check is enforced automatically at the end of each turn, the way the skill's Verify
section describes. Do not ask me anything, just set it up.
