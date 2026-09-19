---
name: quantifier-checked-over-every-member
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Write, Bash, Skill]
---
Everything below is FIXTURE content invented for this exercise. Build the tree exactly as
given in the current folder, then use the spec-artifact-diff skill to check
`docs/overview.md` against that tree and report what you find.

Create these files, each containing one line reading `# placeholder`:

```text
modules/auth/README.md
modules/auth/handler.py
modules/billing/handler.py
modules/export/README.md
modules/export/handler.py
modules/search/README.md
modules/search/handler.py
modules/telemetry/README.md
modules/telemetry/handler.py
```

Note that `modules/billing/` gets `handler.py` only, with no `README.md`.

Save as `docs/overview.md`:

```markdown
# Overview

The codebase is organised into module folders under `modules/`. Every module folder
ships its own `README.md` describing what that module owns, and every module folder
contains a `handler.py`.
```
