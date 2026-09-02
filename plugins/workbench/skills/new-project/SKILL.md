---
name: new-project
description: Stand up a brand-new repo end to end — directory structure, .gitignore, secret-scanning hooks, licence, the four project docs (README/CLAUDE.md/SPEC.md/KICKOFF.md), the first commit, and the GitHub repo — before any implementation work begins. Use this whenever the user is starting something new and says anything like "new project", "new repo", "start a repo for", "set up a project", "scaffold", "bootstrap", "kick off a new thing", "I want to build X" where X does not exist yet, or asks to get a project "structured properly" / "set up the way I like it". Also use it when they have loose files or a prototype sitting in a folder and want it turned into a real repo. Supports four archetypes — AWS/Terraform infra, homelab service, Python pipeline/CLI, static site. Do NOT use it for adding structure to an existing repo that already has git history and docs.
metadata:
  maturity: incubator
---

# New project

Stand up the repo before any code gets written, so the first commit is a clean
scaffolding-only baseline and every later diff is readable against it.

The work splits in two, and the split is the point:

- `scripts/scaffold.sh` does everything deterministic — directories, ignore rules,
  hooks, licence, CI, and **stubs** for the four docs. It is a script so it produces
  byte-identical bones every time and can be tested.
- **You** do the part that needs judgment: interview the user, then write the four
  docs with real content.

`scaffold.sh publish` refuses to push while any doc still contains its
`<!-- SCAFFOLD-TODO -->` markers. That gate exists because a repo whose `CLAUDE.md` is
an unfilled template is worse than one with no `CLAUDE.md` — people learn to ignore it,
and then the one time it does say something important, nobody reads it.

## Workflow

### 1. Interview first — do not run the script yet

You cannot write a useful `CLAUDE.md` or `SPEC.md` from a project name. Ask these,
batched into one round (use `AskUserQuestion` if you have it), with your best guess
pre-filled as the default so answering is cheap:

1. **What is this and who uses it?** One paragraph. Push for the non-obvious context —
   the thing a competent stranger would not infer from the name.
2. **Archetype** — `infra` (AWS/Terraform), `homelab` (compose service), `python`
   (pipeline/CLI/analysis), `site` (static/generated site). Infer it from the answer to
   #1 and just confirm; only ask openly if it is genuinely ambiguous.
3. **Where does it run?** Laptop, an AWS account, a homelab host, GitHub Pages, CI.
   This decides half of `SPEC.md` and most of the CI workflow.
4. **What must never happen?** The rules a newcomer would break on day one. This is the
   highest-value question in the interview and it is the one people skip.
5. **What is deliberately out of scope for v1?** Recording this stops it being
   relitigated every session.
6. **Name** (lowercase slug) and **private or public** (default private).

If the user is unreachable or clearly wants you to just go, pick sensible answers, write
them into `SPEC.md` §2 as assumptions rather than facts, and say plainly at the top of
your reply which ones you invented.

### 2. Lay the bones

```bash
scripts/scaffold.sh doctor          # once per machine: git, gh auth, gitleaks, pre-commit
scripts/scaffold.sh init --name <slug> --type <infra|homelab|python|site> --desc "<one line>"
```

Defaults to `$GFM_PROJECT_ROOT` or `~/work/GitHub/<slug>`, licence MIT, branch `main`.
It prints the created path on the last line. `--dir` overrides the parent.

### 3. Write the four docs

Read `references/conventions.md` before writing — it defines what belongs in each file
and, more usefully, what does *not*. The short version:

| File | Audience | Holds |
|---|---|---|
| `README.md` | a human landing on the repo | what it is, how to run it, what state it is in. Short. |
| `CLAUDE.md` | auto-loaded agent context | what/state/hard rules. Points at SPEC.md as source of truth. |
| `SPEC.md` | both, as the arbiter | decisions + why, scope, design, dependencies, **verification**, open questions. |
| `KICKOFF.md` | the user, to paste | the prompt that starts the first real Claude Code session. |

Rules for filling them:

- **Delete every `<!-- SCAFFOLD-TODO -->` line as you replace it.** They are the publish gate.
- **Do not invent facts to fill a section.** Write `TBD (<what would settle it>)`. An
  explicit unknown is information; a confident guess is a landmine six weeks out.
- **Keep the pre-written hard rules in `CLAUDE.md`.** Rules 1–7 are the user's standing
  preferences and rules 8–9 are archetype-specific; they are already correct. Add
  project-specific rules below them, and only edit an existing rule if this project
  genuinely contradicts it.
- **`SPEC.md` §6 (Verification) is not optional.** Write the actual commands and what
  their output should look like. It is the section a future agent runs before claiming
  done, and a spec without it produces confident false "complete" claims.
- **Every count, version and size is a dated snapshot.** Say so where you write one.

### 4. Publish

```bash
scripts/scaffold.sh publish --path <repo>            # private (default)
scripts/scaffold.sh publish --path <repo> --public
```

It checks, in order: no unfilled stubs → `.env` is ignored if present → `gitleaks` finds
nothing → `gh` is authenticated → no `origin` yet. Then one commit
(`chore: scaffold <name> (<type>)`) and `gh repo create --source=. --push`.

Add `--dry-run` to rehearse. If `gitleaks` is missing it refuses rather than skipping —
that is deliberate, since purging a leaked credential later means a history rewrite, a
force-push, and rotating the secret anyway. `--no-scan` overrides and records why in the
commit trailer.

### 5. Stop

Report the repo URL and hand over `KICKOFF.md`. **Do not start implementing.** The user
asked for a scaffold; the clean baseline commit is the deliverable, and the first real
session starts fresh with `CLAUDE.md` auto-loaded. If they explicitly say to keep going,
that is a different request and the scaffold is already safely committed.

## Archetype notes

Read the matching file in `references/` when writing the docs — each lists what usually
belongs in that archetype's `SPEC.md` and the traps worth a hard rule.

- `references/archetype-infra.md` — Terraform/AWS: state, envs, plan-before-apply.
- `references/archetype-homelab.md` — compose services: host registry, backups, restore.
- `references/archetype-python.md` — pipelines/CLIs: pinning, `--check` modes, data hygiene.
- `references/archetype-site.md` — generated sites: templates vs output, Pages settings.

For infra specifically: if the project will touch IAM, networking, state, or anything
that spends money, the `plan-gate` skill applies to the *first real session*, not to this
one. Note that in `KICKOFF.md` rather than trying to do it here.

## Things that go wrong

- **Running `init` before the interview.** You end up writing docs to fit a directory
  layout instead of choosing the layout to fit the project. Interview first.
- **Filling `SPEC.md` with plausible-sounding architecture.** If the user has not decided
  how something works, the spec must say so. Half the value of the file is that it is
  trustworthy.
- **A `CLAUDE.md` State section written as aspiration.** It describes what exists *now*.
  On a fresh scaffold that is "nothing is built yet" — say that.
- **Adding directories the project will not use.** Twelve empty folders teach people the
  structure is decorative. The archetypes are already close to minimal; do not pad them.
- **Being clever with the repo name.** Lowercase slug, matches the directory, matches
  the GitHub repo. `scaffold.sh` enforces this.
