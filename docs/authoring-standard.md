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

Say what the skill is not for and what it costs (a subagent spawn, a long read, a
network fetch) alongside what it does; a description with no negative scope routes
neighbouring requests to it. When a skill keeps firing wrongly or not at all, fix the
description before reaching for a stronger model: most misroutes trace back to an
inaccurate description, not to the model.

## Body

- **Under 500 lines** (official guidance). A loaded skill stays in context across
  turns; every line is a recurring token cost.
- Long material — rubrics, examples, schemas, sample outputs — lives in
  `references/` or `templates/` inside the skill directory, linked by relative path.
- Structure the body around what the skill must *do*, not background prose.
- Shape each rule as scope, action, exception, verification (when X, do Y, unless Z,
  proven by W) rather than a growing list of banned words or phrases. A ban list ages
  into an enumeration nobody checks; a rule with a verification step can be tested.
- A skill or check that is a heuristic states its measured ceiling in the file that
  implements it (a backtest table, "catches about a third of cases"), so a reader knows
  what it misses before trusting it (hstack review, 2026-09-03).
- A skill or check that enforces something lists its known weaknesses beside its
  rationale, at the same altitude, never in an appendix or a later section (trailofbits
  coop review, 2026-09-07).

## Contract sections

Every SKILL.md body carries four H2 sections, in this order, after the title and any
introductory paragraph and before `## Output contract`:

1. `## Inputs` - what the skill needs before it can start: the artifacts, values, or
   questions answered. A skill with no inputs says so in one line.
2. `## Verify` - the check the skill runs or surfaces to show its work held: the
   command, the observable, or the fixture, and what output means pass.
3. `## Done when` - the end state, stated so a reader could confirm it without asking
   the skill's author. One measurable line beats three vague ones.
4. `## Stop when` - the conditions under which the skill halts short of done and hands
   back: a budget exhausted, a blocker only the user can clear, a check that cannot be
   named. At least one condition that is not "done". A skill with no stop condition is
   an unbounded loop with a description.

Maturity split, enforced by `scripts/validate-skills.sh`: a **stable** skill fails the
validator (F14, F15, F16) when a section is missing, out of order, or `## Stop when` is
vacuous; an **incubator** skill gets a warning (W4, W5, W6) and passes. Promotion to
stable therefore requires the four sections, like `version` and `reviewed`.

Known weakness, stated beside the rule: the validator checks presence, order, and one
non-trivial line under `## Stop when`. A section can be present and vacuous ("Inputs:
see above") and still pass. Quality of the four sections is a review judgment, made by
the human reviewer at promotion and by the weekly maintainer's audit; the validator
proves only that the author wrote them.

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
- Incubator skills: edit directly on main.
- Any change to a skill's files, stable or incubator, bumps the host plugin's
  `version` in the same commit. A versioned plugin's installed cache refreshes only
  when the manifest version changes; the skill's own `metadata.version` does not
  trigger it. Recorded 2026-09-12: phased-harness 1.2.6 shipped in PR #7 without a
  workbench bump, `claude plugin update` reported workbench "already at the latest
  version (0.10.0)", and every installed cache stayed at 1.2.5 until PR #8 bumped
  the manifest.
- Run `scripts/validate-skills.sh` before committing anything.
- Structural checks parse frontmatter with the YAML loader (`scripts/skill_meta.py`),
  never grep for a key name: a checker that can match its own documentation, or a
  key mentioned in prose, is not checking structure (hstack review, 2026-09-03).
- Behavior testing: for stable skills keep 2–3 eval cases and run them on change
  (the official `skill-creator` plugin provides evals and version comparison).
  Reviewing prompt diffs alone tells you almost nothing about behavior.
- Once a skill has eval cases, they run on any change to that skill, its hooks, or the
  CLAUDE.md it depends on, because that configuration steers the agent and deserves the
  regression testing code gets. A change that drops the pass rate is reviewed before it
  merges, not after. (Recorded 2026-09-02 with zero eval cases in the library, so this
  binds from the first one.)
- A change made to fix a failing case is tested on two sets: the boundary set (the
  case or cases that prompted the change) must improve, and the retention set (every
  case that already passed) must not regress. Showing only the second is how a change
  that fixed nothing gets merged.
