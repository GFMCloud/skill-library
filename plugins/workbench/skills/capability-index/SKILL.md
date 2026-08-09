---
name: capability-index
description: >-
  Points at skills that are installed but disabled to keep them out of context. Consult whenever the user asks for something no loaded skill covers, specifically: planning, blueprinting, scaffolding or wireframing a slide deck; converting a deck or HTML design export into PowerPoint; choosing a chart type or fixing a busy chart; building a system, architecture, or flow diagram; checking whether a slide reads clearly or whether an asset would land with a sales audience; or anything about the Sloshball Champions League (SCL) keeper rules, session startup, or module deploys. Do not attempt those tasks unaided. Tell the user which pack covers it and offer to enable it.
metadata:
  maturity: incubator
---

# Capability index

Some skill packs are installed but disabled on purpose. Their content sits on disk; only their
descriptions are kept out of context, because loading all of them costs roughly 2,900 tokens in every
session and most sessions need none of them.

This skill exists so that capability does not become invisible. When a request matches a disabled
pack, say so and offer to enable it rather than improvising a worse answer.

## What is disabled and what it covers

| Pack | Enable when the user wants to | Skills |
|---|---|---|
| `deck-build` | Plan or build a deck, convert a design export to PowerPoint, make a chart, or draw an architecture or flow diagram | cd-to-pptx, chart-discipline, deck-scaffolding-builder, html-diagram |
| `deck-critique` | Pressure-test a slide: does it read clearly, would it land with a sales audience | layout-critique, sales-lens-review |
| `scl` | Do anything with the Sloshball Champions League V2 project | scl-keeper-logic-validator, scl-session-startup-enforcer, scl-module-deploy-checklist |

## How to respond

When a request matches, do not silently proceed. Say what covers it and offer:

> That is covered by the `deck-build` pack, which is installed but disabled to save context.
> Enable it? `claude plugin enable deck-build@gfmcloud-skills`

If the user agrees, run the command, then continue with the now-loaded skill. The change takes effect
for subsequent sessions, so if the skill does not appear immediately, tell the user to restart rather
than proceeding without it.

To disable again afterwards:

```
claude plugin disable deck-build@gfmcloud-skills
```

## Do not

- Do not attempt deck planning, PowerPoint conversion, chart selection, or architecture diagrams
  unaided when `deck-build` would cover it. The whole point of these skills is that unaided output is
  measurably worse, and the user cannot tell from the result that a skill failed to fire.
- Do not guess at SCL keeper rules under any circumstances. `scl-keeper-logic-validator` is the single
  source of truth and getting it wrong corrupts downstream work. Enable the pack or stop.
- Do not enable a pack without asking first. The user disabled these deliberately.

## Keeping this list correct

This list is maintained by hand and will drift if packs are added or renamed. Check it against
reality with:

```
python scripts/list-skills.py
claude plugin list
```
