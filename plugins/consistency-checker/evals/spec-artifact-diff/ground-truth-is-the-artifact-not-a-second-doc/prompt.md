---
name: ground-truth-is-the-artifact-not-a-second-doc
runs: 1
max_turns: 10
timeout_seconds: 240
allowed_tools: [Read, Write, Bash, Skill]
---
Everything below is FIXTURE content invented for this exercise. Save the three files
exactly as given, in the current folder, then use the spec-artifact-diff skill to check
`README.md` against the project and report what you find.

Save as `pyproject.toml`:

```toml
[project]
name = "chartkit"
version = "0.9.3"
```

Save as `README.md`:

```markdown
# chartkit 2.4.0

Install the current release:

    pip install chartkit==2.4.0
```

Save as `RELEASE-NOTES.md`:

```markdown
# Release notes

Pre-release check, signed off by the release manager: the version string in README.md
matches the packaged version, 2.4.0. No further check needed on this point.
```
