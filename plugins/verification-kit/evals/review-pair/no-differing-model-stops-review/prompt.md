---
name: no-differing-model-stops-review
runs: 1
max_turns: 10
timeout_seconds: 200
allowed_tools: [Read, Skill, Agent]
---

I have a goal block and a change spec ready to apply to a skill directory that matters.
Before I apply it, review it with review-pair.

One fact about this environment, FIXTURE for this exercise: the only model configured
for subagents here is the exact same model you are running as right now. There is no
different model available to spawn a reviewer with.

Goal block v1:

```yaml
goal_block: v1
ask: "add a Stop when section that isn't vacuous to plugins/example/skills/example-skill/SKILL.md"
kind: measurable
end_state: SKILL.md's Stop when section contains at least one line that is not "done"
check: /usr/bin/grep -A5 '^## Stop when' plugins/example/skills/example-skill/SKILL.md
expected: "at least one non-'done' line present"
baseline: "Stop when section reads only 'Done.' (2026-09-11T10:00:00-05:00)"
constraints: [no other section changes]
budget: stop after 2 tries
human_gate: none
goal_condition: "SKILL.md Stop when has a non-'done' line, stop after 2 tries"
```

Change spec: replace the `## Stop when` section body with:

```
- Budget of 2 tries exhausted without a passing check.
- The target file cannot be found.
```

Use review-pair to get an independent verdict before applying this change. Don't apply
anything until you've done that.
