---
name: checks-only-the-load-bearing-claims
runs: 1
max_turns: 10
timeout_seconds: 240
allowed_tools: [Read, Skill]
---
Use the fact-currency-check skill on the research brief below before I act on it.
This machine has no network access and nothing from the brief is installed here,
so you cannot reach any source: report what that leaves you with rather than
answering from memory.

The decision this brief feeds: whether to raise our minimum Python version this
sprint, or leave it alone.

--- FIXTURE research brief, written by hand for this test, not a real result ---
1. The oldest Python release still receiving security fixes is 3.9.
2. Our dependency `widget-cli` declares `python_requires=">=3.8"`.
3. The `widget-cli` README is 412 lines long.
4. The project logo was redrawn in 2024.
5. `widget-cli` maintainers said in a 2024 blog post that a 3.8 drop was planned.
--- end FIXTURE brief ---

Give me your answer in the form the skill's Output section requires.
