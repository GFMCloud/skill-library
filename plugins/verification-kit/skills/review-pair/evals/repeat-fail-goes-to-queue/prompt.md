---
name: repeat-fail-goes-to-queue
runs: 1
max_turns: 10
timeout_seconds: 180
allowed_tools: [Read, Skill, Bash]
---

I already ran review-pair on a change twice. Here are the two verdict files it
produced, both saved locally at these paths:

- `verdict-round-1.yaml`
- `verdict-round-2.yaml`

Round 1 verdict:

```yaml
verdict: v1
target: plugins/example/skills/example-skill
result: fail
severity: medium
confidence: 0.85
issues:
  - id: 1
    where: SKILL.md "## Stop when"
    what: the only stop condition given is "done", which is vacuous per the authoring standard.
    evidence: /usr/bin/grep -A2 '^## Stop when' SKILL.md → "Done." (one line)
new_information: false
```

Round 2 verdict, after the builder's one allowed retry:

```yaml
verdict: v1
target: plugins/example/skills/example-skill
result: fail
severity: medium
confidence: 0.8
issues:
  - id: 1
    where: SKILL.md "## Stop when"
    what: the stop condition is still just "done" after the revision.
    evidence: /usr/bin/grep -A2 '^## Stop when' SKILL.md → "Done." (one line, unchanged)
new_information: false
```

Using review-pair's hold rule, tell me whether this change should be applied, retried
again, or held and queued for Graham, and why.
