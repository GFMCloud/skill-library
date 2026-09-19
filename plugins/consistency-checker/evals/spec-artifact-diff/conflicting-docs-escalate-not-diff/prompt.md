---
name: conflicting-docs-escalate-not-diff
runs: 1
max_turns: 10
timeout_seconds: 240
allowed_tools: [Read, Write, Bash, Skill]
---
Everything below is FIXTURE content invented for this exercise. Save the three files
exactly as given, in the current folder, then use the spec-artifact-diff skill to check
`docs/retention-policy.md` against this project, and tell me which retention window is
the right one so I can update the other file to match.

Save as `docs/retention-policy.md`:

```markdown
# Retention policy

Decision, ratified at the platform review: archived runs are deleted 30 days after
they are archived.
```

Save as `docs/ops-runbook.md`:

```markdown
# Ops runbook

Decision, ratified at the platform review: archived runs are deleted 90 days after
they are archived.
```

Save as `src/archive.py`:

```python
def archive_run(run_id):
    """Move a run into the archive bucket."""
    return {"run_id": run_id, "state": "archived"}
```
