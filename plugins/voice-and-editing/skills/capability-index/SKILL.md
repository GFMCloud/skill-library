---
name: capability-index
description: >-
  Points at capability that exists on this machine but is not loaded in the current session, so it does not become invisible. Consult whenever the user asks for something no loaded skill covers, specifically: making a video or launch clip (hyperframes, and decks:brag which needs it); deploying a site and checking it live, or moving one to Cloudflare Pages (deploy-ops); GitHub work through an MCP server rather than the gh CLI (github); TypeScript type-safety review (typesafe); anything about the Sloshball Champions League (SCL) keeper rules, session startup, or module deploys. Those packs are installed but disabled since 2026-10-18. Do not attempt those tasks unaided. Say what covers it and where it lives, and offer to enable it.
metadata:
  maturity: incubator
  reviewed: 2026-10-18
---

# Capability index

Not every skill on this machine is loaded in every session. Some packs are not
installed; some skills are project-scoped and only load inside their own repo. This
skill exists so that capability does not become invisible: when a request matches
something unloaded, say so and offer to load it rather than improvising a worse
answer.

## What is not loaded, and where it actually lives

Verified against `~/.claude/settings.json` (`enabledPlugins`) and
`~/.claude/plugins/installed_plugins.json` on 2026-10-18, when a `/skill-doctor` run
showed 106 listed skills, 62 never invoked, and four packs were disabled to shrink the
listing. Every pack below is still installed, so enabling is one command and no download.

| Not loaded | Covers | Where it lives | How to reach it |
|---|---|---|---|
| `hyperframes` pack (21 skills) | videos: launch clips, explainers, slideshows, music videos, PR-to-video, captions, the Hyperframes CLI | `~/.claude/plugins/cache/claude-plugins-official/hyperframes/` | `claude plugin enable hyperframes@claude-plugins-official`, then a new session. `decks:brag` stays enabled but reads five hyperframes skills, so a `/brag` request needs this pack on first |
| `deploy-ops` pack | deploy, check the result as a visitor would, fix, repeat; moving a site to Cloudflare Pages | `~/skill-library/plugins/deploy-ops/` | `claude plugin enable deploy-ops@skill-library` |
| `github` pack | GitHub through an MCP server (issues, PRs, files). The `gh` CLI covers the same ground without it, and the server failed to connect with a 400 on 2026-10-18 | `~/.claude/plugins/cache/claude-plugins-official/github/` | `claude plugin enable github@claude-plugins-official`; try `gh` first |
| `typesafe` pack | TypeScript type-safety review (`typesafe-ai`) | `~/.claude/plugins/cache/typesafe-ai/typesafe/` | `claude plugin enable typesafe@typesafe-ai` |
| SCL project skills | keeper rules, session startup, module deploy checklist | **project-scoped** in `~/work/GitHub/sloshball-champions-league-v2/.claude/skills/`, not a plugin and not installable | open a session in that repo, where they load automatically |

## How to respond

When a request matches, do not silently proceed. Say what covers it and offer. For a
pack row, check `claude plugin list` first, because "not installed" and "installed but
disabled" take different commands:

> That is covered by the `<pack>` pack, which is installed but disabled here.
> Enable it? `claude plugin enable <pack>@<marketplace>`
> (If it is not installed at all: `claude plugin install <pack>@<marketplace>`)

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
jq '.enabledPlugins' ~/.claude/settings.json
ls ~/skill-library/plugins/
```

A pack that appears in `claude plugin list` as enabled does **not** belong in the table
above. The table is only for capability that a current session cannot reach. When a
pack is enabled again, remove its row and its clause in the description in the same
commit; when `/skill-doctor` shows another pack idle for a month, disable it and add a row.
