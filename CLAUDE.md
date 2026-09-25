General working agreements live in ~/.claude/CLAUDE.md. This file adds only what is specific to skill-library.

# skill-library — authoring rules

This repo is the canonical home of every reusable Claude Code skill on this account,
structured as a plugin marketplace.

## Rules for sessions editing this repo

- Follow [CONTRIBUTING.md](CONTRIBUTING.md) for every skill, and the library's add-on in
  [maintainers/authoring-standard.md](maintainers/authoring-standard.md). Start new skills
  from [templates/SKILL-template.md](templates/SKILL-template.md).
- **New skills go straight into the plugin they belong to** (the install unit they
  would be enabled with), with `maturity: incubator` as a label only. There is no
  staging plugin; a skill is live on every machine at the next plugin update. Adding
  a skill bumps that plugin's `version` and gets a CHANGELOG line.
- **Promotion to `stable`** is a frontmatter flip (`maturity`, `version`, `reviewed`)
  plus a CHANGELOG line. Nothing moves.
- **Stable-skill changes** bump `metadata.version`, update `metadata.reviewed`, and
  get a CHANGELOG entry describing the behavior change (not the wording change).
- **Any skill, agent or plugin hook change bumps the host plugin's `version` in the same commit.**
  Installed caches refresh only on a manifest version change, never on a skill's
  own `metadata.version` (workbench 0.10.1, 2026-09-12). The validator enforces
  this (F17) against `origin/main`.
- **This repo is public. Install the hooks once per clone** (`bash scripts/install-hooks.sh`)
  and never bypass them. They run `scripts/brand-gate.py` and gitleaks before every
  commit and push. Employer content arrives here only after it has been de-branded
  somewhere private and passed the gate there; nothing branded is ever pushed to a
  branch of this repo, even briefly. The validator fails (F22) until the hooks are on.
- **Never write to this repo through GitHub API file tools** (`create_or_update_file`,
  `push_files`, `delete_file`, web edits). Those commits skip every local hook. Commit
  in a clone and push.
- **Gate PR text before it is published.** Pipe a PR's title and body, and a branch
  name, through `python3 scripts/brand-gate.py --text` before creating or editing the
  PR. GitHub publishes them before CI can check them.
- **Run the validator before committing:**

  ```bash
  bash scripts/validate-skills.sh
  ```

  It must exit 0. CI runs the same script on every PR and push to main.
- **Never duplicate an existing skill name** — across all plugins, and never reuse a
  name that exists as a project-local skill in some repo's `.claude/skills/`.
- Long material (rubrics, schemas, examples) goes in the skill's `references/` or
  `templates/` directory, not the SKILL.md body (body stays under 500 lines).
- Plugins are grouped by **install unit** — skills you'd enable or disable together —
  not by topic. Prefer ~3–7 plugins over one mega-plugin or many single-skill ones.
- `.claude-plugin/marketplace.json` is THE catalog. Adding or removing a plugin means
  updating it in the same commit.
