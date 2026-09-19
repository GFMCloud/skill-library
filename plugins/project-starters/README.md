# project-starters

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

The first hour of a new project decides how the next three months go. Most projects skip it. A folder appears, code goes in, and the things that were never written down get argued about later: what this is for, what done looks like, what must never happen, where the passwords live. Six weeks in, nobody can say whether a change is in scope, because scope was never written.

This pack covers that first hour. One skill interviews you and then creates the project folder, the ignore rules, the licence and a check that stops a password reaching a commit. Others work backwards from the outcome you want, package a rough idea into something a fresh session can execute, pin the project to one set of development tools, and turn a long reference document into files Claude can look things up in.

## When would I use this?

- You are starting something new and want the folder, the git setup and the first commit done properly before any code.
- You have an idea in your head and cannot yet say what finished looks like.
- You want to hand a project to a fresh Claude Code session that has none of your conversation and still have it work.
- Everyone on a project has slightly different versions of the tools, and the build works on one machine and not another.
- You have loose files or a prototype in a folder and want it turned into a real project.
- You have a long reference document, a handbook or a policy PDF, and you want Claude to answer questions from it accurately.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/project-starters/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [devshell-init](skills/devshell-init/README.md) | Adds a pinned set of development tools to a repo, so the same versions appear on every machine that opens it. | "set this project up with its own toolchain" | Three files in your repo (`flake.nix`, `.envrc`, `CLAUDE.md`), and the output of the check that the right tools are now in use. | Writes those three files into the repo you name, then downloads and switches on a Nix toolchain. The tools switch on again each time you enter that folder. Needs Nix and direnv. |
| [new-project](skills/new-project/README.md) | Interviews you about a new project, then creates the folder, the git setup, a secret scan on every commit, a licence and the four project documents. | "start a new repo for a python pipeline" | A new project folder with a first commit of setup only, four written documents, and, when you run the publish step, a GitHub repository with that commit pushed. | Creates a new folder, by default under your home folder at `~/work/GitHub/<name>`, runs the bundled setup script, and on the publish step creates a real GitHub repository under your account and pushes to it. Needs `git`, `gh`, `gitleaks` and `pre-commit`. |
| [pipeline-foundry](skills/pipeline-foundry/README.md) | Turns a project idea into a brief a fresh Claude Code session can execute from, settling scope, decision authority and what counts as done. | "turn this idea into a handoff a fresh session can run" | A zip of project documents, or a named blocker and the advice to shelve the project if a readiness check fails. | Reads templates from a local copy of the `gfm-foundry` project and writes the documents into a zip for you. It recommends a weekly cloud job that works on the project unattended. |
| [project-kb-builder](skills/project-kb-builder/README.md) | Breaks one long reference document into a set of topic-sized markdown files a Claude Project can look answers up in. | "turn this 100-page PDF into knowledge files for a project" | A numbered set of markdown files, an index file first, with source contradictions flagged rather than smoothed over. | Reads the document you give it and writes markdown files. It was written for the Claude website and writes to `/mnt/user-data/outputs/`, which does not exist in Claude Code, so that step needs a local folder instead. |
| [project-setup-wizard](skills/project-setup-wizard/) | Takes a rough brain dump about something you are starting and turns it into a project description and a set of instructions for Claude. | "/newproject" or "help me set up a project for this" | Three blocks of text to copy: a project description, a setup summary with documents to upload, and a full set of project instructions. | Nothing |
| [systems-design](skills/systems-design/README.md) | Runs a guided conversation that works backwards from the outcome you want, maps what must be true at each stage, and tests it against how it could fail. | "help me work backwards from this goal" | A summary document with the end state, the dependency map, ranked failure modes and sprint-sized blocks, plus a diagram of the system. | Runs a conversation of 20 to 30 minutes, then saves one document and draws one diagram. It was written for the Claude website: the output path, the question tool and the file viewer it names are not present in Claude Code. |
<!-- /generated:whats-inside -->

Start with what you have. If you know what you are building, `new-project` creates the folder and the git setup, and `devshell-init` pins the tools of a project that already exists. If the idea is still rough, `systems-design`, `project-setup-wizard` and `pipeline-foundry` produce plans, descriptions and briefs rather than files on disk. `project-kb-builder` is unrelated to the rest and is for turning one long document into files Claude can look answers up in. `project-kb-builder` and `systems-design` were written for the Claude website rather than for Claude Code, and say so on their own pages.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | `devshell-init` looks through the repo you point it at for the files that say which language it is: `pyproject.toml`, `package.json`, `go.mod`, Terraform files and `Cargo.toml`.<br>`new-project` reads its own reference notes, and at publish time reads the four project documents in the new folder.<br>`pipeline-foundry` reads templates from a local copy of the separate `gfm-foundry` project, and stops and asks you to fetch that project if it is not there.<br>`project-kb-builder` reads, in full, the one source document you give it.<br>`project-setup-wizard` and `systems-design` read no files. They work from what you type. |
| Files written | `new-project` creates a whole new project folder, by default under `~/work/GitHub/<name>` (`~` means your home folder): directories, a `.gitignore`, a commit-check config, a licence, an automated build job, starter code and four document stubs that Claude then rewrites with real content.<br>`devshell-init` writes three files into the repo you name: `flake.nix`, `.envrc` and a project `CLAUDE.md`.<br>`pipeline-foundry` writes a set of project documents (`CLAUDE.md`, `HANDOFF.md`, `PROGRESS.md`, `CONTINUATION.md`, `OPEN-ITEMS.md`, a `.gitignore` and `.claude/skills/project-constants/SKILL.md`) and hands them to you as a zip.<br>`project-kb-builder` writes a folder of markdown files to `/mnt/user-data/outputs/<kb-name>/` and `systems-design` writes one summary document to `/mnt/user-data/outputs/`. Those are Claude website locations, not Claude Code ones.<br>`project-setup-wizard` writes nothing. Its three outputs are blocks of text in the reply for you to copy. |
| Files deleted or moved | None. `devshell-init` stops and asks if the repo already has a `flake.nix`. `new-project` refuses to start if the folder it would create is already there. |
| Programs and scripts | One program ships with this pack: `new-project`'s `scripts/scaffold.sh`. It runs `git init`, installs a commit check, runs the secret scanner `gitleaks`, makes the first commit, checks your `gh` sign-in and creates the GitHub repository.<br>`devshell-init` ships no program. It has Claude run `nix` and `direnv` commands in your repo, which build a set of development tools and switch them on. The `.envrc` file it leaves behind switches them on again every time you enter that folder, for as long as the file is there.<br>`pipeline-foundry` has Claude run `claude plugin marketplace list` and `claude plugin list` to see what is installed.<br>`systems-design` calls the `visualize` pack's drawing tool for its diagram. `project-kb-builder` and `project-setup-wizard` run nothing. |
| Internet access | `new-project` creates a repository on GitHub and pushes the first commit to it, and installing its commit check downloads that check from github.com.<br>`devshell-init` pulls its toolchain definitions from GitHub, so switching the tools on the first time downloads packages.<br>A diagram drawn by `systems-design` may load drawing libraries from the internet when you open it.<br>`pipeline-foundry`, `project-kb-builder` and `project-setup-wizard` go online for nothing of their own. |
| Accounts, keys or passwords | `new-project` acts through the GitHub sign-in you already have in the `gh` command line tool, and prints the account name it is signed in as. It never asks for or stores a password or key.<br>`devshell-init` will not read or copy the values in an existing `.env` file. If it finds real values there it says so and proposes that you move them into 1Password yourself.<br>`pipeline-foundry` states that it never handles credentials and deliberately leaves creating the GitHub repository to you.<br>The other three use no account. |

Three limits. First, `project-kb-builder` and `systems-design` were written for the Claude website, not for Claude Code. The output folder `/mnt/user-data/outputs/`, the `present_files` tool both use, and the question tool `ask_user_input_v0` that `systems-design` calls are all website features. On your own computer that folder does not exist and those tools are not there, so the last step of each needs pointing at a normal local folder instead. Second, `pipeline-foundry` recommends setting up a scheduled cloud job, weekly by default, that reopens the project and works through a queue of pre-approved tasks with nobody present and no permission prompts. It also defines a list of things that must never go in that queue. Read both parts before you set one up. Third, `new-project`'s own text says the `--no-scan` option overrides the secret scan. In the code it only takes effect when `gitleaks` is missing: if `gitleaks` is installed the scan still runs and can still stop the publish. The code is stricter than the text, not looser.

## How the skills work together

They cover the stages of starting something, in this order:

1. **Before there is a project.** `systems-design` works backwards from the outcome you want and produces a plan with failure modes and sprint-sized blocks. `project-setup-wizard` takes a rough brain dump and turns it into a Claude Project description and instructions.
2. **Turning the idea into a brief.** `pipeline-foundry` pressure-tests the idea, settles who decides what, and packages the result so a fresh session can execute it without asking you every ten minutes. It refuses to hand over a brief while a readiness check is failing, and recommending that you shelve the project is one of its answers.
3. **Making the repository.** `new-project` interviews you, creates the folder and the git setup, writes the four project documents, and publishes to GitHub as a separate step you trigger.
4. **Pinning the tools.** `devshell-init` adds a reproducible set of development tools to a project that exists, so the same versions appear on every machine.
5. **Any time after that.** `project-kb-builder` turns a long reference document into knowledge files for a Claude Project.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install project-starters@skill-library
```

The first line is only needed once, however many packs you install.

Some skills need other software. `new-project` needs `git` and the GitHub command line tool `gh`, already signed in, plus `gitleaks` and `pre-commit`. `devshell-init` needs Nix and direnv, and the `nix-direnv` helper. `pipeline-foundry` needs a local copy of `github.com/GFMCloud/gfm-foundry` for its templates. `systems-design` needs the `visualize` pack for its diagram step.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
