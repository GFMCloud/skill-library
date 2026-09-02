---
name: devshell-init
description: Add a Nix flake devshell to a repo — flake.nix, .envrc, and a project CLAUDE.md. Use when the user wants a project pinned to a reproducible toolchain, mentions setting up a devshell, or asks why a project's tools aren't isolated.
argument-hint: "[path to repo, defaults to cwd]"
allowed-tools: Bash(nix *), Bash(direnv *), Bash(ls *), Bash(git status*), Bash(which *), Read, Write, Edit, Glob, Grep
metadata:
  maturity: incubator
---

## Instructions

Set up a per-project devshell in `$ARGUMENTS` (or cwd).

### 1. Detect, don't assume

Look at what's actually in the repo before writing anything:

- `pyproject.toml` / `requirements.txt` / `uv.lock` → Python
- `package.json` → Node
- `go.mod` → Go
- `*.tf` / `*.tofu` → OpenTofu
- `Cargo.toml` → Rust

Report what you found. If the repo already has a `flake.nix`, stop — show what's
in it and ask whether to modify rather than overwrite.

### 2. Write the files

Copy from `templates/` and edit `packages` to match what you detected:

- `flake.nix` — keep the multi-system output. The same flake must work on the
  Air *and* on homelab Linux hosts; that's the reason this layer exists.
- `.envrc` — verbatim
- `CLAUDE.md` — fill in the project name, the real commands, and the "out of
  scope" section. Leave the environment and secrets sections alone; they are
  the point.

### 3. Python specifically

Nix supplies the interpreter. `uv` supplies the libraries.

Do **not** put `pandas`, `numpy`, `scipy`, or similar into `flake.nix` from
nixpkgs. That path means version skew against PyPI, long local rebuilds on a
fanless chip, and a lockfile CI can't read. Put `python3XX`, `uv`, and `ruff` in
the flake; everything else goes through `uv add`.

If the user asks you to add a Python library to `flake.nix`, push back once and
explain why `uv add` is the right place.

### 4. Verify it actually works

Do not report success without this:

```bash
cd <repo> && direnv allow
direnv exec . which python      # must resolve under /nix/store, not /opt/homebrew
direnv exec . python --version
```

Show the output. If `which python` points at Homebrew, direnv didn't activate —
say so and diagnose rather than declaring victory.

### 5. Secrets

If the repo has a `.env` with real values in it, that's a finding. Report it,
propose converting to a `.env.template` holding `op://` references, and let the
user move the values into 1Password themselves. Never read the existing values,
never copy them, never write them anywhere.
