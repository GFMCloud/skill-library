# Contributing

Everything for people who want to write or change a skill lives on this page. None of it is on the main README, which is for people who only want to install something.

This library is maintained by one person. Suggestions and fixes are welcome, and there is no promise about how quickly they are read.

## Before you start

Run `bash scripts/install-hooks.sh` once in your clone. It turns on the hooks in `.githooks/`, which stop a commit or push that carries a denied word, an AWS account id or a secret. This repository is public, and a pushed branch is public the moment it lands, so the check has to run before the push. It needs `gitleaks` installed. Don't bypass it with `--no-verify`.

Open an issue first using the "Suggest a skill" form. A skill that duplicates one already here, or that is really three skills, is better caught in an issue than in a pull request.

## What belongs here and what does not

**A skill belongs here if** it does one job, that job comes up in more than one project, and Claude Code does it noticeably worse without written instructions.

**A skill does not belong here if:**

- Claude Code already does it well without help. Instructions for something the model already knows cost reading space and buy nothing.
- It only makes sense inside one project. Keep it in that project's own `.claude/skills/` folder.
- Its name is already used by another skill in any pack. Names are unique across the whole library.
- It asks the user to paste a password, a key or a token into the conversation, in any wording. A skill that needs a sign-in uses one the user already has on their computer, and its pack page says which.
- You cannot say what it reads, writes, runs and connects to. Every pack page states that, and the statement has to be true.
- It covers three jobs. Split it.

A skill may ship a program. Several here do. The cost is that the pack page and the main README's safety section must both say so in the same change.

## Which rules apply

Two sets, and they do not overlap much.

1. **The skill-repo-standard governs the shape of the repository:** the folder layout, the main README, the pack pages, the skill pages, these community files, the templates and the writing style. Its checker is run by the maintainer before a merge. That standard is not public yet, so you cannot run its checker yourself. This page and the three templates carry what you need from it.
2. **The library adds four contract sections to every `SKILL.md`:** `## Inputs`, `## Verify`, `## Done when`, `## Stop when`, in that order. This add-on, the maturity labels and the change rules are written down in [maintainers/authoring-standard.md](maintainers/authoring-standard.md). That file is their one home. `scripts/validate-skills.sh` enforces the parts a script can check.

Where the two disagree, the standard governs, and the disagreement is a bug in the add-on. Please report it.

## Layout

```
.claude-plugin/marketplace.json     the catalog; adding a pack means editing this
plugins/<pack>/
  .claude-plugin/plugin.json        the pack's name, version and dependencies; nothing else goes in this folder
  README.md                         the pack page, for people
  reader-table.tsv                  the source of the pack page's "What's inside" table
  skills/<skill>/SKILL.md           the skill, written for the model, under 500 lines
  skills/<skill>/README.md          the skill page, for people (see below for which skills need one)
  skills/<skill>/references/        rubrics, schemas, long examples
  skills/<skill>/templates/         files the skill writes out
  skills/<skill>/scripts/           programs the skill runs
  agents/<agent>.md                 agent definitions
  evals/<skill>/<case>/             evaluation cases (see below)
docs/                               pages for readers: glossary, picker, install help
docs/inventory.md                   generated, one line per skill
maintainers/                        working records: the authoring add-on, review records, maintenance scripts
scripts/validate-skills.sh          the validator; CI runs the same script
templates/                          blank templates for a SKILL.md, a pack page and a skill page
```

A pack is a set of skills someone would switch on or off together. Packs are not grouped by topic.

## Writing a SKILL.md

Start from [templates/SKILL-template.md](templates/SKILL-template.md). Its comments carry the rules at the point where each applies. The ones that matter most:

- **The description decides whether the skill ever runs.** Claude Code chooses a skill from its `description` alone. Write it in the third person. Say what the skill produces, when to use it, and the words a person would really say. Say what it is not for and what it costs, such as extra agents or a long read. Test it: ask for the job three different ways in a fresh session and confirm the skill loads each time.
- **`name` equals the folder name.** Lowercase letters, numbers and hyphens.
- **The body stays under 500 lines.** A loaded skill stays in the conversation, so every line is paid for on every turn. Long material goes in `references/`, linked directly from `SKILL.md`, one level deep. A reference file over 100 lines opens with a contents list.
- **Nothing a skill loads links outside its own pack.** A pack is installed on its own. Name a skill in another pack as `pack:skill`, in words.
- **Every file the body names ships with the skill.**
- **New skills start as `maturity: incubator`, inside the pack they belong to.** There is no staging pack. Promotion to `stable` changes the label and adds `version` and `reviewed`. Nothing moves.

## The pages for people

`SKILL.md` is written for the model. The pack page and the skill page are written for a person deciding whether they want this. They are different documents and neither is a copy of the other.

- **Every pack has a page.** Start from [templates/pack-README-template.md](templates/pack-README-template.md).
- **Do not type the "What's inside" table.** Add one row per skill and per agent to the pack's `reader-table.tsv`, then run `bash maintainers/scripts/generate-inventory.sh`. It writes the pack tables, the catalog and the counts on the main README, and `docs/inventory.md`. Edit the source, never the generated block.
- **Do not edit the pack map image.** `docs/images/pack-map.svg` is drawn by `python3 maintainers/scripts/generate-pack-map.py` from `marketplace.json` and each pack's `plugin.json`. Run it after adding a pack or changing a pack's `dependencies`. The validator fails when the image is stale.
- **The last column of that file says what the skill does on the reader's computer,** or the single word `Nothing`. Write it from reading the skill's files.
- **A skill needs its own page** when that cell says anything other than `Nothing`, or when the main README sends a first-time reader to it. Start from [templates/skill-page-README-template.md](templates/skill-page-README-template.md).
- **A worked example is real or it is labelled.** The template carries the exact label for an example written by hand.

## Evaluation cases

Cases live in one place: `plugins/<pack>/evals/<skill>/`, one folder per case, each with a `prompt.md` and its graders. They never go inside the skill folder. `claude plugin eval` refuses a suite placed under `skills/`, and the validator fails one put there. The layout and the run command are in [maintainers/toolkit-interface-spec.md](maintainers/toolkit-interface-spec.md), section 9.

Write the cases before the skill body:

1. Ask Claude Code to do the job with no skill loaded. Write down exactly what went wrong.
2. Turn each failure into a case. Three cases at minimum.
3. Write the shortest instructions that make those cases pass.
4. Run the cases again and compare with step 1.

Most skills here do not have three cases yet. The main README's "Status and help" section gives the current count, which is generated.

A case that passes just as well with the skill turned off is not testing anything. Two traps found the hard way: a `tool_used` grader on `Skill` passes even when the skill was not found, so it never proves the pack loaded; and `claude plugin eval <pack folder>` does not load a pack that declares `dependencies`, so check the run's first event for the plugin list before believing a result. Test in a fresh session, because a session where you have been editing the skill already knows what you meant.

## Checks

```bash
bash scripts/validate-skills.sh
```

It must exit 0. CI runs the same script on every pull request and every push to `main`. It checks that frontmatter parses, names match folders and are unique, bodies are under 500 lines, relative links resolve, the generated tables and `docs/inventory.md` are current, the contract sections are present, no eval suite sits inside a skill folder, and that a change to a skill or an agent came with a version bump for its pack. It also fails when it finds no skills at all, because a run that checked nothing proves nothing. Set `STRICT=1` to make warnings fail too.

A second workflow, `brand-gate`, runs `scripts/brand-gate.py` and gitleaks on the changed lines, file paths, commit messages and pull request text. It is the backstop for the local hooks, not a replacement for them. The words it refuses are stored as hashes in `maintainers/brand-gate/denylist.sha256`, so the list doesn't publish them. Add one with `python3 scripts/brand-gate.py --hash '<word>' >> maintainers/brand-gate/denylist.sha256`, and keep the word itself out of the commit message.

## Checklist before you open a pull request

Structure:

- [ ] The skill folder name and the frontmatter `name` match.
- [ ] `plugin.json` is inside `.claude-plugin/`. `skills/` is not.
- [ ] The pack's `version` in `plugin.json` has been bumped. Installed copies only update when it changes.
- [ ] `version` is set in `plugin.json` only, never also in `marketplace.json`.
- [ ] The skill has a row in its pack's `reader-table.tsv`, and the generator has been run.
- [ ] If the pack is new, it is in `marketplace.json` with a `category`, in `docs/which-pack.md`, and in the pack list of both issue forms under `.github/ISSUE_TEMPLATE/`.

Content:

- [ ] `description` is third person and says what, when, what not, and the cost.
- [ ] The four contract sections are present and in order.
- [ ] Reference files are one level deep, and any over 100 lines has a contents list.
- [ ] No em dashes in any file, outside a code fence, a blockquote, or a vendored `SKILL.md`.

Safety:

- [ ] The pack page's "What this does on your computer" table is still true after this change.
- [ ] The main README's safety section is still true after this change.
- [ ] No credential, key or password is asked for in the conversation anywhere in the skill.

Machine checks:

- [ ] `bash scripts/validate-skills.sh` exits 0.
- [ ] The hooks are installed (`git config core.hooksPath` prints `.githooks`), and `python3 scripts/brand-gate.py --range origin/main..HEAD` exits 0.
- [ ] `CHANGELOG.md` has an entry that describes the change in behavior, not the change in wording.

## Work taken from someone else

A skill derived from another project names it in `metadata.source` (`owner/repo@commit`). Its pack then needs a `NOTICE.md` with a `## Derived skills` table, one row per derived skill, and the upstream licence texts in `LICENSES/` beside it. The validator checks the two against each other (F20).

Keep the original license file beside the skill and say where it came from. If the text is kept exactly as its author wrote it, put a `SOURCE.md` beside `SKILL.md` naming the project and the commit, and do not edit the files in place. If you rewrote it, say in the skill what you changed. The review records under [maintainers/reviews/](maintainers/reviews/) show how this was done for the skills already here.

## Renaming or removing a pack

Never just delete an entry. Anyone who installed it will break. Add the old name to the `renames` map in `marketplace.json`, pointing at the new name, or at `null` if the pack is gone for good.

A rename does not reach copies of a skill kept outside this repository. If you once uploaded a skill to your claude.ai account and later switched it off there, that copy still holds the text and the pack name from before the rename. Do not switch such a copy back on without comparing it with the skill here first: it would load beside the installed pack under the old content. Delete it instead, and install the pack.

## Style

Plain, short sentences. No marketing. No popularity badges. No em dashes. Define a term the first time it appears, or link to [docs/glossary.md](docs/glossary.md). Write the pages for someone who has never installed a plugin, because that is who reads them.
