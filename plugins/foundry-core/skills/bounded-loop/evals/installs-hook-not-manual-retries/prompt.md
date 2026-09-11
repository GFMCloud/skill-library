---
name: installs-hook-not-manual-retries
runs: 1
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Bash, Edit]
---
You have a Goal block v1 whose check is `pytest tests/` in this repo, with
budget 3. Use the bounded-loop skill to set this up so the check gets
enforced automatically at the end of each turn, rather than you re-running
pytest by hand and eyeballing the result each time.
