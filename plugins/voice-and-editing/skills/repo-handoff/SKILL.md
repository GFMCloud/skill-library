---
name: repo-handoff
description: >-
  Hand a repo that carries Graham's personal, league, client, or copyrighted material
  to another person without leaking any of it: inventory what must not ship, cut a
  proven-clean tree (a clean commit found with git log -S, or a sanitized subset),
  prove it clean by identifier grep and a secret scan, create a private repo for the
  recipient, and deliver a walkthrough that was executed before handover. Use when
  Graham says "hand this repo to", "share this project with", "make a copy of this
  for", "spin off a version for", "sanitize this repo", "set this up for Lauren", or
  wants a friend to run his tooling. Not for a fresh folder with no history (that is
  folder-to-repo), not for a routine push, and not a way to move credentials. Costs:
  one full-tree grep pass per identifier and one gitleaks run per candidate tree.
metadata:
  maturity: incubator
---

# Repo handoff

Give another person a working copy of a repo that was built around Graham's own
data, without shipping that data.

Three sessions in one week (2026-08-28 to 2026-09-02) did this by hand for three
different recipients: a public fork was privatized before Graham's CV went in, a
clean branch was cut for Lauren from a repo already carrying his data, and a fantasy
draft toolkit was sanitized for a friend. Each re-derived the same checks, and one
handoff doc stated a figure that was wrong until the commands in it were actually run.
This skill is those checks in one place, with the proof steps that caught the misses.

## Scope

- In: a repo (or a folder with git history) that Graham wants someone else to run,
  where the tree, the history, or both contain things that must not travel.
- Out: a fresh folder with no history (use `folder-to-repo`); pushing Graham's own
  repo to his own remote; anything where the recipient needs Graham's credentials
  (they get their own, or nothing).

## What you need before starting

- The repo path, the recipient, and where their copy should live (their GitHub
  account, or a private repo under Graham's account with them as collaborator).
  Ask Graham which; do not guess.
- The identifier list: the strings that identify Graham or his context. Start from
  full name, employer, phone, email, league and team names, account ids, and any
  file class he names (transcripts, audio, exports). Show the list and let him add
  to it before you grep.
- `gitleaks` on PATH (`command -v gitleaks`); if missing, say so and stop at step 4.

## The flow

Work in order. Steps 4 and 6 are gates: a hit in 4 or a failed command in 6 stops
the handoff until fixed.

### 1. Inventory what must not ship

For every identifier, grep the working tree and the history:

```bash
cd <repo> && /usr/bin/grep -rIl --exclude-dir=.git -e '<identifier>' .
git log --all --oneline -S'<identifier>'
```

Then classify every file into one of three buckets and show the table:

| Bucket | Meaning | Handling |
|---|---|---|
| shareable | code, docs, generators, configs with no personal specifics | ships as is |
| sanitize | keeps its purpose but hardcodes Graham's specifics | parameterize (a config file, a `--league` flag), never a hand-edited fork of the output |
| exclude | personal data files, copyrighted media or transcripts, credentials, `.env`, private exports | never ships; name each one in the report |

Copyright counts as exclude even when the file is "just data": podcast audio,
transcripts, scraped articles.

### 2. Choose the cut

Two shapes; pick the one with less to prove.

- **Clean commit.** If `git log -S` shows every identifier first appearing after
  some commit, the commit before the earliest hit is the candidate. Extract it,
  never check it out in place:
  ```bash
  mkdir -p <scratch>/clean && git archive <sha> | tar -x -C <scratch>/clean
  ```
  Use this when the pre-data history is recent enough to be useful.
- **Sanitized subset.** Copy the shareable files plus the sanitized versions of the
  second bucket into a fresh directory. Use this when the data went in at commit one
  or the clean commit is too old.

Either way the delivered tree starts a new history. Graham's history never travels.

### 3. Sanitize, through the generator

Where a file hardcodes his specifics, move them to a config the recipient fills in
(`config/<recipient>.json`, a league file, a `.env.example` with names and no
values). Edit the script that reads the config, not the outputs it produces. Leave a
`TODO` with the recipient's name where a value must come from them.

### 4. Prove the tree clean (gate)

Run all three on the delivered tree and record the commands with their output:

```bash
cd <scratch>/clean
for id in '<identifier 1>' '<identifier 2>'; do printf '%s: ' "$id"; /usr/bin/grep -rIl -e "$id" . | wc -l; done
gitleaks detect --source . --no-git --redact; echo "gitleaks exit: $?"
find . -name '.env' -o -name '*.pem' -o -name 'credentials*' -o -name '*.tfvars'
```

Expected: every identifier count `0`, gitleaks exit `0`, the find empty. Any hit is
a stop: fix the tree, rerun all three, record the clean run. Do not gitignore your
way past an embedded secret; remove it, and tell Graham if it was ever real so he
can rotate it.

### 5. Create the recipient's repo

```bash
cd <scratch>/clean && git init && git add -A && git status
git commit -m "initial handoff from <source repo name>"
gh repo create <name> --private --source=. --push
```

Rules: private by default; the recipient's account or Graham's, as he ruled in the
preflight; Graham's original `origin` is never touched; if the source was a fork of
a public framework, add that framework as `upstream` in the new repo so the recipient
can pull updates. Confirm visibility with `gh repo view <name> --json visibility`.

### 6. Write the walkthrough, then run it (gate)

Write `AGENT-WALKTHROUGH.md` in the delivered tree: what the repo does, setup,
the commands to run, where the config lives, what the recipient must supply. Then
execute every command in it against the delivered tree, in order, and paste each
output under its command in the run log. A command that fails or prints a different
figure than the doc claims means the doc is wrong: fix the doc, rerun, then deliver.

Add three copy-paste prompts for the recipient's own agent, in this order: run it
(setup and first successful run), extend it (add their own league, client, or
dataset), debug it (what to check when a step fails). Each prompt names the files
it depends on.

### 7. Report

Give Graham, in this order: the repo URL and its visibility; the exclude bucket with
one reason each; the clean-proof commands and outputs from step 4; the walkthrough
run from step 6; and the list of things the recipient must supply themselves.

See [references/checklist.md](references/checklist.md) for the gate checklist and the
grep patterns that caught the misses in the three source sessions.
