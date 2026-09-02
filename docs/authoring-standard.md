# Skill authoring standard

The contract every skill in the library must meet. Copied into the library repo's
`docs/` in Phase 0; the validator enforces the checkable parts.

## Frontmatter

```yaml
---
name: handoff-builder            # must equal the directory name
description: >-
  Produce a versioned execution handoff from a project brief. Use before
  multi-agent delivery work, when the user says "handoff", "execution package",
  or asks to package work for another agent.
metadata:
  maturity: stable               # incubator | stable | deprecated
  version: 1.2.0                 # semver; required once stable
  reviewed: 2026-08-09           # last human review; required once stable
  supersedes: old-handoff-skill  # required when maturity: deprecated
---
```

Rules:

- `name` and `description` are required for every skill regardless of maturity.
- `name` must match the skill's directory name (the directory name is the slash
  command).
- The `metadata:` block is officially supported and ignored by the Claude Code
  runtime — it exists to carry governance and costs nothing.
- Optional runtime fields (`allowed-tools`, `model`, `disable-model-invocation`) are
  allowed. Note the tension: `disable-model-invocation: true` makes a skill
  slash-command-only and disables the `description`-driven auto-invocation. Set it
  deliberately, not by template default.

## The description is the router

Auto-invocation is driven by the `description`. Write it like a router, not a
summary: what the skill produces, when to use it, and the trigger phrases a user
would actually say. Vague descriptions are the #1 cause of skills that never fire or
fire wrongly. Spend review effort here first.

Before promoting a skill, test that it triggers: ask for its task three different ways
in a fresh session and confirm the skill loads each time. A skill that fires on one
phrasing is not routed, it is lucky.

## Body

- **Under 500 lines** (official guidance). A loaded skill stays in context across
  turns; every line is a recurring token cost.
- Long material — rubrics, examples, schemas, sample outputs — lives in
  `references/` or `templates/` inside the skill directory, linked by relative path.
- Structure the body around what the skill must *do*, not background prose.

## Output contracts

If a skill's output is consumed by other agents, skills, or pipelines (handoff
packages, structured reports), that output format is an **API**:

- Version it explicitly in the skill body or a referenced schema file.
- Section renames, field changes, and vocabulary changes are breaking changes: bump
  the major version and note the migration in CHANGELOG.md.

## Lifecycle

Three states, not four:

- **incubator** — a label, not a location. The skill lives in the plugin it belongs
  to from day one and is installed alongside that plugin's stable skills. No
  stability promise. Edit freely on main, no PR ceremony. Promote after the skill
  has proven itself in real use (guideline: 2 or more successful real sessions).
  Promotion flips `maturity` to `stable` and adds `version` and `reviewed`, plus a
  CHANGELOG line. Nothing moves and nothing is copied.
- **stable** — owned by the contract: has `version` + `reviewed`, changes go through
  PR, behavior changes get a CHANGELOG line and a version bump.
- **deprecated** — still installed, but `supersedes` names the replacement and the
  CHANGELOG names a removal target. Remove after one clean interval.

## Change hygiene

- Stable skills: change by PR; bump `metadata.version`; update `metadata.reviewed`;
  CHANGELOG describes the behavior change, not the wording change.
- Incubator skills: edit directly on main. Adding one still bumps the host plugin's
  `version` so installed caches pick it up.
- Run `scripts/validate-skills.sh` before committing anything.
- Behavior testing: for stable skills keep 2–3 eval cases and run them on change
  (the official `skill-creator` plugin provides evals and version comparison).
  Reviewing prompt diffs alone tells you almost nothing about behavior.
- Once a skill has eval cases, they run on any change to that skill, its hooks, or the
  CLAUDE.md it depends on, because that configuration steers the agent and deserves the
  regression testing code gets. A change that drops the pass rate is reviewed before it
  merges, not after. (Recorded 2026-09-02 with zero eval cases in the library, so this
  binds from the first one.)
