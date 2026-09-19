# Starting a new project properly

Part of the [project-starters](../../README.md) pack.

This skill sets up a new project before any code is written. It asks you six questions about what the thing is, where it runs and what must never happen, then creates the folder, the git setup, an ignore list, a licence, an automated build job and four documents that say what the project is for. The first commit holds the setup and nothing else, so every later change is readable against a clean starting point. Publishing to GitHub is a separate step you ask for, and it refuses to publish while any document still contains its unfilled placeholder text.

## Say this to use it

Any of these will do:

- "start a new repo for a python pipeline that pulls our billing data"
- "I want to build a homelab service, set the project up properly"
- "turn this folder of loose files into a real project"

Or, to be certain this skill and no other one runs:

```
/project-starters:new-project
```

It will ask what the project is and who uses it, which of four shapes it takes (AWS infrastructure, a homelab service, a Python pipeline or command line tool, or a static website), where it runs, what must never happen, what is deliberately out of scope for the first version, and the name. It fills in its best guess for each, so agreeing is quick.

## What you'll get

A new folder with the setup committed, four written documents, and a printed path.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Created ~/work/GitHub/billing-export

  .gitignore, LICENSE, .pre-commit-config.yaml, .github/workflows/ci.yml
  src/, tests/
  README.md  CLAUDE.md  SPEC.md  KICKOFF.md

Four documents written from your answers:
  README.md    what it is, how to run it, what state it is in
  CLAUDE.md    the standing rules, including "never write to the live billing account"
  SPEC.md      decisions and why, scope, and the commands that prove it works
  KICKOFF.md   the prompt to paste into the first real session

Ready to publish. When you say so I will run the publish step, which
creates a private GitHub repository and pushes the first commit.
```

## Good to know

- **Publishing is a real change to your GitHub account.** The publish step creates a repository and pushes the first commit. It is the point of no return, and it happens when Claude runs that command. There is a `--dry-run` option that rehearses everything and pushes nothing.
- **New repositories are private unless you ask for public.** Public is a separate flag.
- **It scans for leaked passwords before the first commit.** The scanner is `gitleaks`, and the publish step refuses to run if `gitleaks` is not installed. The skill's own text says a `--no-scan` option overrides the scan. In the code that option only takes effect when `gitleaks` is missing. With `gitleaks` installed the scan runs and can still stop the publish. The code is stricter than the text.
- **It installs a check that runs on every future commit in that project.** From then on, each commit you make there is scanned for secrets first. A website project also gets an automated job that rebuilds the site weekly.
- **It uses the GitHub sign-in you already have.** It acts through the `gh` command line tool and prints the account it is signed in as, so you can see which one before anything is created. It never asks you for a password or a key.
- **It refuses to start if the folder is already there.** It creates the new folder, by default under `~/work/GitHub/<name>`, where `~` means your home folder. It deletes and moves nothing.
- **It stops when the setup is committed.** It does not begin building the project. The clean starting point is the deliverable, and the first real session starts fresh from `KICKOFF.md`.
- **It needs four other programs.** `git`, the GitHub command line tool `gh` already signed in, `gitleaks` and `pre-commit`. A built-in check reports which of these are missing before you start.
- **The default location is one person's habit.** The folder goes under `~/work/GitHub/` unless you say otherwise. You can pass a different parent folder, or set the `GFM_PROJECT_ROOT` setting once, if that layout is not yours.

## What next

- Want the project's development tools pinned to fixed versions too? Run [devshell-init](../devshell-init/) in the new folder afterwards.
- Not sure yet what you are building? [systems-design](../systems-design/) works backwards from the outcome first, and [pipeline-foundry](../pipeline-foundry/) turns the idea into a brief a fresh session can execute.
- If the project will touch cloud settings, network or anything that spends money, [plan-gate](../../../turn-reduction/skills/plan-gate/) applies to the first real working session, not to this one.
- Back to the [project-starters pack](../../README.md), or to [skill-library](../../../../README.md).
