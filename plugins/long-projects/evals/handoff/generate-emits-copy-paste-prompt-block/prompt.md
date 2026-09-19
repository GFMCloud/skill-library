---
name: generate-emits-copy-paste-prompt-block
runs: 1
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Write, Bash, Skill]
---
That is the end of this work block. Here is where we got to. All of the detail below
is FIXTURE material invented for this exercise.

- Work type: strategy. We compared three pricing models for the FIXTURE product
  "Northwind Analytics": flat seat pricing, usage tiers, and a hybrid of the two.
- Decided: usage tiers, because the two largest FIXTURE accounts are seat-light and
  query-heavy, so seats undercount what they actually cost us.
- Rejected: flat seat pricing, because it prices out those same two accounts.
- Open: the tier boundaries are not picked, and nobody has checked the FIXTURE
  margin model behind them.
- Nothing was written to disk this session. There is no repo, no deploy and no state
  file behind any of it.

Use the handoff skill and give me the handoff for this. I am picking this up in a
brand new chat tomorrow, on a different machine, so give me everything that session
will need from me.
