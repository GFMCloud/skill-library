# Pinning a project's development tools

Part of the [project-starters](../../README.md) pack.

Most projects rely on whatever versions of the tools happen to be installed on the machine you are sitting at. That is why a build works on one computer and fails on another. This skill looks at a project you already have, works out which language it is written in, and writes three files that pin it to one named set of tools. After that, entering the project folder switches those tools on, and leaving it switches them off again. The same files give the same versions on a laptop and on a Linux server.

## Say this to use it

Any of these will do:

- "set this project up with its own toolchain"
- "why aren't this project's tools isolated?"
- "add a devshell to ~/work/billing-export"

Or, to be certain this skill and no other one runs:

```
/project-starters:devshell-init
```

It will tell you which language it detected before writing anything, and it will ask what to do if the project already has a `flake.nix`, rather than overwriting it. For a Python project it will push back once if you ask it to put a library such as pandas into the toolchain file, because libraries belong with the project's own package tool instead.

## What you'll get

Three files, then the output of a check that the right tools are now in use.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Detected: Python (pyproject.toml, uv.lock)

Wrote:
  flake.nix    python3.12, uv, ruff
  .envrc       switches the toolchain on when you enter this folder
  CLAUDE.md    the project's commands and its out-of-scope list

Checking it actually works:

  $ direnv exec . which python
  /nix/store/9j4k...-python3-3.12.7/bin/python
  $ direnv exec . python --version
  Python 3.12.7

The path is under /nix/store, not /opt/homebrew, so the pinned
interpreter is the one in use.
```

## Good to know

- **It writes three files into the project you name.** `flake.nix`, `.envrc` and a project `CLAUDE.md`. It deletes nothing and moves nothing.
- **It stops rather than overwriting.** If the project already has a `flake.nix` it shows you what is in it and asks whether to change it.
- **It downloads software the first time.** The toolchain definitions come from GitHub, and switching the tools on fetches the packages they name. That first run needs a network connection and can take a while.
- **The tools stay switched on for that folder.** The `.envrc` file it leaves behind re-activates the toolchain every time you enter the folder, for as long as the file is there. Deleting the file stops it.
- **It will not touch the values in your `.env` file.** If it finds a file of real secrets it reports that as a finding, proposes replacing the values with 1Password references, and leaves you to move them. It never reads, copies or writes the values. The environment file line in the template it ships is switched off, so as delivered it reads no environment file at all.
- **It needs Nix and direnv installed first.** Plus the `nix-direnv` helper. Nix is a package manager and direnv is the tool that switches an environment on per folder. Without them the files are written but nothing activates.
- **It checks its own work and says when the check fails.** It runs the tools and shows you where they resolved to. If the path points at Homebrew rather than the pinned toolchain, it says direnv did not activate and diagnoses that instead of reporting success.
- **For Python it splits the job deliberately.** The toolchain supplies the interpreter and `uv` supplies the libraries. Putting libraries in the toolchain file causes long local rebuilds and version mismatches against the public package index.

## What next

- Creating the project from scratch? [new-project](../new-project/) makes the folder, the git setup and the four project documents first, and this skill pins the tools afterwards.
- Back to the [project-starters pack](../../README.md), or to [skill-library](../../../../README.md).
