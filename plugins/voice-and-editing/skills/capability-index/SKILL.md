---
name: capability-index
description: >-
  Points at capability that exists on this machine but is not loaded in the current session, so it does not become invisible. Consult whenever the user asks for something no loaded skill covers, specifically: anything about the Sloshball Champions League (SCL) keeper rules, session startup, or module deploys; or a skill in a skill-library plugin that is not installed here (none as of 2026-09-19, all twelve packs are installed and enabled). Do not attempt those tasks unaided. Say what covers it and where it lives, and offer to load it.
metadata:
  maturity: incubator
  reviewed: 2026-09-19
---

# Capability index

Not every skill on this machine is loaded in every session. Some packs are not
installed; some skills are project-scoped and only load inside their own repo. This
skill exists so that capability does not become invisible: when a request matches
something unloaded, say so and offer to load it rather than improvising a worse
answer.

## What is not loaded, and where it actually lives

Verified against `claude plugin list` and `~/.claude/plugins/installed_plugins.json`
on 2026-09-19, after the regroup into twelve packs (`workbench` split into
`long-projects`, `project-starters` and `agent-tooling`; `graham-voice` became
`voice-and-editing`). The former `_incubator` pack is gone: its skills live inside the
packs they belong to and load with them. All twelve `skill-library` packs are installed
and enabled at user scope, so no pack has a row. The `decks` pack had one until
2026-09-18: the row called it "installed but disabled" when it was not installed at all,
and it was then installed and enabled.

| Not loaded | Covers | Where it lives | How to reach it |
|---|---|---|---|
| SCL project skills | keeper rules, session startup, module deploy checklist | **project-scoped** in `~/work/GitHub/sloshball-champions-league-v2/.claude/skills/`, not a plugin and not installable | open a session in that repo, where they load automatically |

## How to respond

When a request matches, do not silently proceed. Say what covers it and offer. For a
pack row, check `claude plugin list` first, because "not installed" and "installed but
disabled" take different commands:

> That is covered by the `<pack>` pack, which is not installed here.
> Install it? `claude plugin install <pack>@skill-library`
> (If it is listed as disabled instead: `claude plugin enable <pack>@skill-library`)

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
- Do not install or enable a pack without asking first.

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
