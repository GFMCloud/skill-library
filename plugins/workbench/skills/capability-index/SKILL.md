---
name: capability-index
description: >-
  Points at capability that exists on this machine but is not loaded in the current session, so it does not become invisible. Consult whenever the user asks for something no loaded skill covers, specifically: anything about the Sloshball Champions League (SCL) keeper rules, session startup, or module deploys; or a workflow that one of the unreleased `_incubator` skills covers (session retros, sweep and rulings and experiment harnesses, a Cloudflare Pages migration, the Scrollback SB-01 design system, scaffolding a project handoff for a fresh session, devshell or new-project scaffolding). Do not attempt those tasks unaided. Say what covers it and where it lives, and offer to load it.
metadata:
  maturity: incubator
  reviewed: 2026-08-20
---

# Capability index

Not every skill on this machine is loaded in every session. Some packs are not
installed; some skills are project-scoped and only load inside their own repo. This
skill exists so that capability does not become invisible: when a request matches
something unloaded, say so and offer to load it rather than improvising a worse
answer.

## What is not loaded, and where it actually lives

Verified against `claude plugin list` and `~/.claude/plugins/installed_plugins.json`
on 2026-08-20.

| Not loaded | Covers | Where it lives | How to reach it |
|---|---|---|---|
| `_incubator` pack | cloudflare-pages-migration, devshell-init, experiment-harness, new-project, pipeline-foundry, retro, rulings-harness, scrollback, sweep-harness | `skill-library` repo, published to the marketplace but **not installed** | `claude plugin install _incubator@skill-library` |
| SCL project skills | keeper rules, session startup, module deploy checklist | **project-scoped** in `~/work/GitHub/sloshball-champions-league-v2/.claude/skills/`, not a plugin and not installable | open a session in that repo, where they load automatically |

## How to respond

When a request matches, do not silently proceed. Say what covers it and offer:

> That is covered by the `_incubator` pack, which is published but not installed.
> Install it? `claude plugin install _incubator@skill-library`

If the user agrees, run the command. The change takes effect for subsequent sessions,
so if the skill does not appear immediately, tell the user to restart rather than
proceeding without it.

For the SCL skills there is nothing to install. They are project-scoped, so the only
way to reach them is a session opened in the SCL v2 repo. Say that plainly instead of
offering an install command that does not exist.

## Do not

- Do not guess at SCL keeper rules under any circumstances. `scl-keeper-logic-validator`
  is the single source of truth, and getting it wrong corrupts downstream work. Work in
  the SCL v2 repo, or stop.
- Do not assume a skill named in another project's notes is reachable from the project
  you are in. Project-scoped skills load only inside their own repo.
- Do not install a pack without asking first.

## Keeping this list correct

This list is maintained by hand and drifts whenever packs are added, renamed, merged,
or installed. It has drifted badly before: it once named packs `deck-build` and
`deck-critique` that had been merged into `decks`, and a marketplace `gfmcloud-skills`
that had been superseded by `skill-library`. Check it against reality with:

```bash
claude plugin list
cat ~/.claude/plugins/installed_plugins.json
ls ~/skill-library/plugins/
```

A pack that appears in `claude plugin list` as enabled does **not** belong in the table
above. The table is only for capability that a current session cannot reach.
