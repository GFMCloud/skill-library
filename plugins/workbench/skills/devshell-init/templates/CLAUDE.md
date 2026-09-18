General working agreements live in ~/.claude/CLAUDE.md. This file adds only what is specific to <project>.

# <project name>

<!--
Per-project CLAUDE.md template. Lives at the repo root.

Keep this file within the "CLAUDE.md economy" rule in ~/.claude/CLAUDE.md.
-->

## What this is

<One or two sentences. What the project does and who uses it.>

## Environment — read this before running anything

This project uses a Nix devshell. The toolchain is pinned in `flake.nix`.

**Run every command through the devshell:**

```bash
nix develop -c <command>
# or, equivalently:
direnv exec . <command>
```

**Why this matters:** `direnv` hooks into *interactive* shells. Agent tool calls
run non-interactive shells, so the hook does not fire and you will get the
system PATH instead of the project one. Prefixing is the fix. Symptoms of
forgetting: "command not found" for a tool that plainly exists, or the wrong
language version.

If a tool is missing, add it to the `packages` list in `flake.nix` and re-enter
the shell. Python dependencies are the one exception: those go through `uv add`
and land in `pyproject.toml` / `uv.lock`, which is the intended path.

## Commands

```bash
nix develop -c uv sync          # install deps
nix develop -c uv run pytest    # tests
nix develop -c ruff check .     # lint
```

## Secrets

Config that needs a secret reads it at runtime:

```bash
op run --env-file=.env.template -- <command>
```

`.env.template` contains `op://` references, not values.

## Conventions

- <Anything you've had to correct twice.>
- <Layout quirks, deploy ritual, naming rules.>

## Out of scope

- <Things Claude should not touch: generated files, vendored code, migrations.>
