---
name: fills-goal-block
runs: 1
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Bash, Skill]
---
Use the goal-spec skill on this ask: "get the homepage lighthouse scores up
for https://gfmcloud.com/." A check exists: `echo "perf=71 a11y=88 bp=92
seo=100"` stands in for the real Lighthouse command in this eval — run it
once to record the baseline, then produce the Goal block v1.
