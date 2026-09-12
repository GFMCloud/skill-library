---
name: runs-the-thing-before-done
runs: 1
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Bash, Skill]
---
Use the proof-of-work skill. I am about to tell a colleague that this one-liner
prints the answer 42:

python3 -c 'print(6 * 7)'

Produce the executed evidence that it does, in the form the skill requires, then
say whether the claim is done. Reading the line and reasoning about it does not
count.
