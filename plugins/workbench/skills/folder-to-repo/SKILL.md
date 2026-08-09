---
name: folder-to-repo
description: >-
  Turn an existing project folder into a brand-new private GitHub repo, following
  Graham's personal repo standard (prefix naming, private-by-default, required
  README + .gitignore, and a mandatory secret scan before the first commit). Use
  this whenever Graham wants to "make this folder a repo", "put this on GitHub",
  "turn this into a git repo", "version control this project", "push this folder
  to GitHub", or hands over a local folder that should become a repository. Trigger
  even if Graham doesn't say the word "skill" or name the standard - any time a
  loose folder needs to become a new GitHub repo, this is the skill. Do NOT use it
  for folders that already have git history or for pushing to an already-existing
  repo - this skill is specifically for a fresh folder becoming a brand-new repo.
metadata:
  maturity: incubator
---

# Folder to Repo

Turn a plain project folder into a brand-new, private GitHub repo that follows
Graham's repo standard - without ever committing a secret.

The git commands here are trivial. The value of this skill is the judgment around
them: naming the repo right, getting the required files in, and above all catching
secrets *before* the first commit. Git history is permanent, so a secret that lands
in a commit stays recoverable even after the file is deleted. The only safe place to
stop a leak is before commit one. That's why the secret scan is a gate, not a
suggestion.

## Scope

This skill is for one specific job: **an existing folder with no git history becoming
a brand-new GitHub repo.** If the folder already has a `.git` directory, or Graham
wants to push to a repo that already exists on GitHub, stop and tell him - that's a
different workflow this skill deliberately doesn't cover.

## What you need before starting

- The path to the folder being turned into a repo.
- A connected GitHub MCP / GitHub connector (look for tools like `create_repository`
  and `push_files`). If none is connected, do the local steps, then hand Graham the
  exact `gh`/`git` commands to create and push - don't pretend you pushed.

## The flow

Work through these in order. Don't skip the scan, and don't commit before it passes.

### 1. Confirm the folder and check it's really a fresh start

Confirm the path. Then check for an existing repo:

```bash
test -d "<folder>/.git" && echo "HAS GIT" || echo "no git - good"
```

If it prints `HAS GIT`, stop - this folder already has history and is out of scope.
Tell Graham and ask how he wants to handle it.

### 2. Propose a name with the right prefix

Graham's naming convention (kebab-case, category prefix first):

| Prefix | Use for |
| --- | --- |
| `awsp-` | AWS Practice work assets |
| `lab-` | Sandboxes, experiments, throwaway tests |
| `personal-` | Personal projects worth keeping |

Look at what's in the folder and propose a name like `awsp-finops-dashboard`. Rules:
name describes what it *is*, not its stage - no `-v2`, no `-final`, no dates, no
`-new`/`-old`. Git tracks history for you. If it's genuinely unclear whether
something is `lab-` or `awsp-`, default to `lab-` (it's easy to rename and promote
later). Always confirm the proposed name with Graham before creating anything.

### 3. Drop in the required files

Every repo needs exactly two files at minimum, both bundled in this skill under
`assets/repo-template/`:

- `README.md` - the four-question stub (what / who owns / how to run / status)
- `.gitignore` - already excludes `.env`, AWS creds, keys, Terraform state, and the
  usual Node/Python/OS junk

Copy them in only if the folder doesn't already have its own. If the folder has a
README already, leave it - just check it covers the four questions and offer to fill
gaps. Do NOT copy `START_HERE.md` into the repo; that file is template scaffolding,
not repo content.

Then fill in the README's four sections from what you can infer about the project,
and confirm with Graham:

1. **What is this?** One or two sentences.
2. **Owner.** Graham, plus category (personal / project / sandbox). Name the wider
   initiative it belongs to, if any.
3. **How to run / use.** Setup, dependencies, the start command.
4. **Status.** One word: active / paused / archived / experiment.

### 4. Run the secret scan - this is the gate

Run the bundled scanner over the whole folder:

```bash
python3 scripts/scan_secrets.py "<folder>" --json
```

It splits findings into two buckets, and they're handled differently:

**Whole-file secrets** (a `.env`, `credentials`, `*.pem`, `*.tfvars`, `id_rsa`,
etc.) - the entire file is a secret container that was never meant to be tracked.
Per Graham's call: **add it to `.gitignore` and continue, but warn him clearly.**
Tell him exactly which files you excluded so nothing silent happens. The bundled
`.gitignore` already covers the common ones, so usually they're handled - just
confirm and surface anything extra you added.

**Embedded secrets** (a key/token sitting *inside* a file you'd want to keep - an
AWS key pasted into `app.py`, a token in a config you need tracked) - you can't
gitignore the whole file without losing real code. **This is a HARD STOP.** Do not
commit, do not push. Show Graham the file, line number, and what was found. The fix
is his to make: pull the secret out (move it to `.env` or AWS Secrets Manager) and,
if it was ever real, rotate it first - assume it's burned. Only continue once the
embedded secret is gone and you've re-run the scan clean.

The scanner exits `2` when there's an embedded secret and `0` otherwise, so you can
gate on the exit code. Never proceed to commit while exit code is `2`.

### 5. Initialize and make the first commit

Once the scan is clean (or only whole-file secrets, now gitignored):

```bash
cd "<folder>"
git init
git add -A
git status            # eyeball what's staged - last chance to catch something
git commit -m "initial commit"
```

Before committing, actually look at `git status` output. If anything secret-looking
is still staged, stop. The scan is the main net but this is the cheap backstop.

Keep the first commit message simple and present-tense. Graham's style: "add finops
cost export", not "stuff" or "asdf".

### 6. Create the GitHub repo and push

Use the GitHub connector. Create the repo **private** (Graham's default is always
private - flip to public only if he explicitly says so):

- Create the repository with the confirmed name, private visibility.
- Push the local commit to it.

With the GitHub MCP, the usual path is `create_repository` (set `private: true`),
then push the committed files (`push_files`) or wire up the remote and `git push`:

```bash
git remote add origin <repo-url-from-create-step>
git branch -M main
git push -u origin main
```

If no GitHub connector is available, stop here and give Graham the exact commands to
run himself, including the `gh repo create <name> --private --source=. --push` one-liner
if he has the GitHub CLI.

### 7. Clean up and confirm

- Delete `START_HERE.md` if it ended up in the folder (`rm -f START_HERE.md`) - it's
  template scaffolding, never repo content.
- Give Graham the repo URL, confirm it's private, and note anything you gitignored
  during the scan so he has the full picture.

## The ownership footnote (mention once, when relevant)

Work-related assets sometimes get kept in a *personal* GitHub by choice, which means
they stay with the person rather than the employer. That is a legitimate call, but it
has a limit: once a repo becomes something an employer or team actually depends on, it
belongs in an org account, not a personal one. Personal-account hosting also means
work credentials, account IDs, and internal detail end up on a personal identity.
Worth a one-line flag when a work-flavored repo starts looking load-bearing. Do not
belabor it.

## Quick checklist (mirror of Graham's standard)

- [ ] Folder has no existing `.git` (in scope)
- [ ] Named with correct prefix, kebab-case
- [ ] README answers: what / who owns / how to run / status
- [ ] `.gitignore` covers the stack and excludes `.env`
- [ ] Secret scan run; embedded secrets resolved; whole-file secrets gitignored + flagged
- [ ] `git status` eyeballed before first commit
- [ ] Repo created **private** and pushed
- [ ] `START_HERE.md` removed
