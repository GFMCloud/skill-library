# skill-library — authoring rules

This repo is the canonical home of every reusable Claude Code skill on this account,
structured as a plugin marketplace. **This repo is the only editable surface** for
these skills — never edit installed plugin caches (`~/.claude/plugins/**`) or any
other copy; changes land here and reach machines via plugin updates.

## Rules for sessions editing this repo

- Follow [docs/authoring-standard.md](docs/authoring-standard.md) for every skill.
  Start new skills from [templates/SKILL.template.md](templates/SKILL.template.md).
- **New skills start in `plugins/_incubator/`** with `maturity: incubator`. Promotion
  to a real plugin is a `git mv` plus a CHANGELOG line — never a copy.
- **Stable-skill changes** bump `metadata.version`, update `metadata.reviewed`, and
  get a CHANGELOG entry describing the behavior change (not the wording change).
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
