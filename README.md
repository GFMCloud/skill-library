# skill-library

[![validate-skills](https://github.com/GFMCloud/skill-library/actions/workflows/validate.yml/badge.svg)](https://github.com/GFMCloud/skill-library/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A Claude Code plugin marketplace holding 47 reusable skills and 6 subagents, grouped
into 10 installable plugins. Delivery discipline, deck building, frontend design
judgment, project harnesses, and the connective tissue that keeps long-running agent
work honest.

## Why this exists

Skills have a way of multiplying. They start as a folder in one project, get copied
into a second project when they turn out to be useful, get zipped up and emailed to
yourself, and end up in `~/.claude` under a slightly different name. A year in you
have four copies of the same skill, three of them stale, and no idea which one the
agent actually loaded.

This repo is the fix: **one editable home per skill**. Everything reusable lives here
and is consumed everywhere else as an installed plugin. Plugin caches and local copies
are read-only. A skill lives in its plugin from day one; maturity is a label, not a
location, so promotion never moves or copies anything. If an
editable duplicate shows up somewhere else, that's drift to be flagged and removed,
not a convenience to keep.

It was assembled by sweeping every skill scattered across two older marketplaces,
several project repos, a home directory, and one orphaned `.skill` zip, then ruling on
each one individually: move, keep project-local, deprecate, or archive.
[MIGRATION.md](MIGRATION.md) is the permanent record of where each skill came from and
why it landed where it did.

## Install

Add the marketplace, then install the plugins you want:

```bash
/plugin marketplace add GFMCloud/skill-library
```

```bash
/plugin install foundry-core@skill-library
```

Both are interactive Claude Code commands. Plugins are deliberately fine-grained so
you can enable a few without taking the whole library.

## What's inside

| Plugin | Contents | What it's for |
|---|---|---|
| `foundry-core` | evidence-report, proof-of-work, full-output-enforcement | Never present work as done without executed evidence, and never truncate it. The skills most worth having on every project. |
| `turn-reduction` | capability-preflight, output-lint, standing-authorization | Cut wasted round trips: prove access before starting, lint outgoing instructions, read your authorization from a file instead of asking. |
| `verification-kit` | fact-currency-check, `pre-delivery-verifier` agent | Check a claim is still true today, and verify an artifact against its acceptance criteria before handing it over. |
| `consistency-checker` | spec-artifact-diff, `cross-document-checker` agent | Catch docs that have drifted from the thing they describe, and documents that contradict each other. |
| `deploy-ops` | deploy-verify-fix, cloudflare-pages-migration, `deploy-loop-owner` agent | Own the deploy, verify, fix loop end to end instead of handing a half-deployed artifact back to a human. Includes the Cloudflare Pages migration runbook. |
| `data-wrangler` | identity-resolution, `data-pipeline-owner` agent | Move data between shapes and match records across sources whose keys don't line up. |
| `decks` | cd-to-pptx, chart-discipline, deck-scaffolding-builder, html-diagram, layout-critique, sales-lens-review | Plan, build, and critique slide decks. Includes HTML-to-PowerPoint conversion and interactive architecture diagrams. |
| `frontend-design` | design-taste-frontend, image-taste-frontend, mobile-taste-frontend, minimalist-ui, redesign-existing-projects, frontend-design, emil-design-eng, scrollback, `frontend-surface-builder` agent | Visual design judgment for new builds, app screens, and in-place redesigns, split by aesthetic so the right one fires. Includes the Scrollback SB-01 design system. |
| `workbench` | 21 skills including handoff, retro, phased-harness, sweep-harness, rulings-harness, experiment-harness, new-project, devshell-init, source-intake, systems-design, model-effort-advisor, skill-discovery, `transcript-scanner` agent | General-purpose working skills. Session handoffs and retros, project scaffolding, multi-session harnesses, model routing, source intake, mining past sessions for workflows worth codifying. |
| `graham-voice` | graham-voice | One person's writing voice as its own install unit, so it can be enabled alone. |

A few skills are personal (`graham-voice` encodes one person's writing style, `adhd`
shapes output for one reader, `capability-index` points at a private project). They're kept in the open because the shape is more reusable than the
content: fork them and swap in your own.

## Layout

```
.claude-plugin/marketplace.json   the catalog; adding a plugin means editing this
plugins/<plugin>/
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md         the skill body, under 500 lines
  skills/<skill>/references/      rubrics, schemas, worked examples
  skills/<skill>/templates/       files the skill writes out
  agents/<agent>.md               subagent definitions
docs/authoring-standard.md        the contract every skill must meet
docs/inventory.md                 generated, one line per skill; validator fails when stale
scripts/validate-skills.sh        the validator; CI runs the same script
templates/SKILL.template.md       start new skills from this
```

## Authoring standard

The full contract is in [docs/authoring-standard.md](docs/authoring-standard.md). The
parts that matter most:

**The description is the router.** Auto-invocation keys off `description`, so write it
as a router and not a summary: what the skill produces, when to use it, and the
trigger phrases someone would actually say. Vague descriptions are the top cause of
skills that never fire, or fire at the wrong moment.

**Bodies stay under 500 lines.** A loaded skill sits in context across turns, so every
line is a recurring token cost. Rubrics, schemas, and long examples belong in
`references/`.

**Maturity is a label, not a location.** A new skill goes straight into the plugin it
belongs to as `incubator`: no stability promise, edited directly on main, and live on
every machine at the next plugin update. There is no staging plugin. Promotion to
`stable` (after the skill has proven itself in real use) flips the label and adds a
semver `version` and a `reviewed` date; later changes go through PR. `deprecated`
names its replacement via `supersedes`.

**Plugins group by install unit,** meaning skills you'd enable or disable together, not
by topic.

## Validation

```bash
bash scripts/validate-skills.sh
```

Thirteen failure checks and three warnings: frontmatter parses, `name` matches the
directory, descriptions clear 40 characters, no duplicate names across plugins, bodies
under 500 lines, no broken relative links, maturity is valid, stable skills carry
version and review date, deprecated skills name a real replacement. It also fails on
finding zero skills, because a green run that checked nothing is a false green.
Warnings cover stale review dates, unintended slash-only skills, and oversized files;
set `STRICT=1` to make them fail too.

CI runs the same script on every PR and every push to main. Current state: 47 skills
checked, 0 failures, 0 warnings.

## License

[MIT](LICENSE).

Two pieces of third-party content are redistributed here with their original terms
intact: `plugins/frontend-design/skills/frontend-design/` carries its own Apache-2.0
license file, and `workbench/adhd` is adapted from
[ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) (MIT), itself loosely based
on *The Adult ADHD Tool Kit* by Ramsay and Rostain. Keep those notices if you fork.
