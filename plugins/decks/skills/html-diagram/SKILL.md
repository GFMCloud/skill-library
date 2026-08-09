---
name: html-diagram
description: Build a self-contained, branded, interactive HTML architecture diagram from a description of a system. Use whenever the user wants to visualize, diagram, map, or explain an architecture, data flow, request path, system, pipeline, or "how X works" as a clickable diagram - especially AWS architectures, integration and automation flows, or anything with components and the paths between them. Trigger on "diagram this", "make an architecture diagram", "visualize this system/flow/pipeline", "show how this works", or "turn this into a diagram", or any time the user describes a system with components and wants to see it laid out. Produces one HTML file with clickable nodes, flow-highlight chips that animate request paths, and a light/dark toggle, themed through neutral CSS variables that can be swapped for the project's own brand kit or design tokens. Use even if the user doesn't say "skill" or "HTML", as long as the goal is an interactive architecture or flow diagram. Not for slide decks (use cd-to-pptx) or static one-pagers. Not for planning a deck's overall structure - if the ask is a full deck plan rather than one diagram, that's deck-scaffolding-builder, which handles blueprint/wireframe/design-spec before a deck exists. Not for numeric or data visualization on a slide - that's chart-discipline, which handles chart type and data-encoding decisions. This skill is specifically for a standalone architecture, system, or flow diagram with no numeric data to encode.
metadata:
  maturity: incubator
---

# HTML Diagram

Turn a description of a system into one self-contained, branded, interactive HTML diagram. The output is a single file: a full-screen SVG stage where components are clickable nodes grouped into zones, the paths between them are labeled arrows, and a row of chips up top isolates named request flows - clicking one dims the whole diagram and lights and animates just the nodes and edges on that path, with a step-by-step caption. Everything is themed through a small set of CSS variables (light + dark), so the look stays consistent and the SVG follows the theme without any hand-coloring. No build step, no dependencies, opens in any browser.

**Brand note:** the template ships with neutral, accessible default colors and a default web font, not a real brand. If the project has its own brand kit or design tokens (a tokens file, a CSS variables file, a style guide), swap the `:root` values and `--diagram-font` for those. If it doesn't, the defaults are fine to use as-is - just say so to the user rather than presenting them as an actual brand.

## The one-paragraph model

You never write the CSS or the JavaScript engine - those are frozen in the template and already correct. Making a diagram is filling four content slots in a copy of the template: the **zones** (groupings, as left-to-right columns), the **nodes** (component boxes inside zones), the **edges** (labeled arrows between nodes), and two small **JS objects** - `DETAIL` (what shows when a node is clicked) and `FLOWS` (what lights up when a chip is clicked). Get the architecture straight in plain text first, lay it out, fill the slots, validate, screenshot. That's the whole job.

> **Non-negotiable: a diagram is not finished until `scripts/validate.py` has been run on it and exits clean.** The build step and the QA step are one task, not two. A file that hasn't been validated is a draft you are not allowed to present - this skill's one field failure was a diagram that looked done, was handed over unvalidated, and turned out to be truncated so nothing clicked. Running the validator takes one command and would have caught it. Do not skip it, do not defer it, do not present output without it.

## What you build from

Three bundled files carry the entire system. Read them at the point each is needed, not all up front:

- `assets/template.html` - the boilerplate. Neutral CSS variables, all styling, the flow/click/theme engine, and empty content slots with inline guidance. **Copy this to start.** Never edit its `<style>` or `<script>` engine.
- `assets/example-cppo-architecture.html` - a fully worked example (a private-offer automation pipeline: SharePoint form -> Power Automate -> API Gateway/Lambda -> Marketplace Catalog API -> Teams). Read it to see what a finished, populated diagram looks like end to end.
- `references/structure-contract.md` - the exact rules for the four slots: coordinate conventions, the node classes and when to use each, edge/label rules, the `DETAIL` and `FLOWS` schemas, and the known gotchas. **Read this before filling slots.**

## When this is the right tool

Use it for architecture, integration and automation flows, data flows, request paths, pipelines, and "how it works" explainers - anything with components and the paths between them. The diagram can be the deliverable itself (a customer-facing system explainer, internal onboarding, an architecture-review visual) or the source you screenshot into a deck later. If it's headed for a deck eventually, still build it here first - it's faster to get a system diagram right interactively, then capture it, than to fight it in PowerPoint.

Don't use it for full slide decks (that's `cd-to-pptx`), static branded one-pagers or PDFs, numeric/data visualization on a slide (that's `chart-discipline`), planning a deck's overall structure before slides exist (that's `deck-scaffolding-builder`), or simple non-technical flowcharts where the interactivity is wasted.

## Build workflow

### Step 0 - Get the architecture straight (gate before drawing)

Before any HTML, pin down in plain text:

- **Components** - what each one is, one line. These become nodes.
- **Groupings** - which components belong together (e.g. "Microsoft 365", "AWS Integration", "AWS Marketplace"). These become zones, laid left-to-right in the direction data flows.
- **Connections** - what talks to what, and a short label for each hop. These become edges. Note which are dependencies / credential reads rather than the main flow (those get dashed).
- **Named flows** - the 2-5 distinct paths worth isolating (e.g. "Create offer", "Notify", "Login"). Each is an ordered subset of nodes + edges plus a short step list.

If the user's description is loose, reflect back the component / zone / flow list and confirm before drawing. Fixing this on paper is free; fixing it after you've placed SVG coordinates is tedious.

### Step 1 - Copy the template on disk, then edit slots in place

This is a hard rule, not a style note. **Copy `assets/template.html` to your working file with a file operation (`cp`), then fill the four slots with in-place edits (str_replace) into that copy.** Never regenerate the whole file - never paste the entire diagram into one `create_file`/write call.

Why this matters: the frozen `<style>` block and `<script>` engine are ~250 lines. If you re-emit the whole file in one shot you can run out of output budget partway through and truncate the engine, which produces a file that looks complete but where nothing clicks (the script never closes, so `setFlow`/`DETAIL`/`FLOWS` are never defined). Copying on disk and editing only the slots means the engine is written by `cp`, never by you, so it cannot be truncated. Set the title and subtitle in the top bar. Leave `<style>` and the `<script>` engine byte-for-byte untouched.

### Step 2 - Read the contract, then lay out zones

Read `references/structure-contract.md`. Place each zone as a column on the 1560x980 canvas in flow order, with gutters between columns for edges and labels.

### Step 3 - Place nodes

One node per component, inside its zone. Pick the node class by role (default / `hero` / `store` / `entity` / `ext` - see contract). Unique `data-k` on each. Title plus 2-4 short lines max.

### Step 4 - Draw edges and labels

One `<path class="edge" id="e-...">` per connection with a matching `<text class="elbl" data-e="e-...">`. Dashed for dependencies. Route around boxes, not through them. Nudge labels off the line and away from node text.

### Step 5 - Write `DETAIL`

One entry per node `data-k`: title, meta line, and a 1-3 sentence body (inline `<b>` / `<code>` ok). This is the click-through detail - the "why it matters," not a spec dump.

### Step 6 - Define `FLOWS` and chips

One `FLOWS` entry per named flow (name, ordered `edges`, `nodes`, and `steps`), plus a matching chip button in the bar. "Everything" is built in - don't redefine `all`.

### Step 7 - QA gate (MANDATORY - the build is not done without it)

Run this on every diagram, every time, before Step 8. No exceptions, including "it's a small change" or "it obviously works."

```bash
python3 scripts/validate.py <working-file.html> --shots
```

You may only proceed to Step 8 when this command exits clean (`pass` on cross-references and no structural FAILs). If it reports any FAIL, you are not done - fix it and re-run until clean.

The validator runs a structural-integrity check first (file ends with `</html>`, script tags balanced, engine sentinels present) - this catches a truncated file, the one failure that looks fine until you click and nothing happens. If it FAILs there, the file got regenerated and cut off: go back to Step 1, copy the template fresh, and edit slots in place. After that it checks every `FLOWS` edge and node exists in the SVG, every node has a `DETAIL` entry, every label points at a real edge, and flags edges no flow lights. Fix every FAIL. The `--shots` flag writes light, dark, and active-flow PNGs (needs playwright - install with `pip install playwright --break-system-packages && playwright install chromium` if missing). Open the PNGs and actually look: nodes not overlapping, edges not crossing boxes, labels not colliding with node text, the hero node readable. Fix layout and re-shoot until clean. Eyeballing the screenshot is part of the gate, not optional polish.

### Step 8 - Present

Only reachable once Step 7 exits clean. Copy the finished file to `/mnt/user-data/outputs/` and present it. State plainly that the validator passed, and tell the user which calls you made on the architecture (ingress, async handling, what's a dependency vs a main hop) so they can correct anything you inferred. If you find yourself about to present without a clean validator run in this session, stop and go run Step 7 first.

## Gotchas

Carried from real builds - the full list is in `references/structure-contract.md`. The big three: use the `hero` class once and only once; never let an edge label sit on a node's text line; leave the theme pre-paint script and `diagram-theme` localStorage key alone.

## Packaging

This skill ships as a folder. To hand the user an installable file, package it with the skill-creator script:

```bash
python3 -m scripts.package_skill <path-to-html-diagram>
```

That produces a `.skill` file they can install the same way as their other skills.
