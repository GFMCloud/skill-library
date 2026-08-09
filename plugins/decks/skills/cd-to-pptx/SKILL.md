---
name: cd-to-pptx
description: Convert Claude Design slide deck exports (deck-stage HTML) into native, editable PowerPoint files. Use whenever the user wants to turn a Claude Design deck, design export, or HTML slide deck into a .pptx, "convert this deck", "export this to PowerPoint", "make this editable", or hands over a folder of print HTML + PDF from Claude Design. Also use for batches - multiple decks in one run. Runs recon, builds native slides, leaves charts/graphs/diagrams as labeled placeholder boxes for the user to finish by hand, self-QAs against the reference PDF, and hands back a review-ready file. Trigger even if the user doesn't say "skill" or name the file type, as long as a Claude Design export is going to PowerPoint.
metadata:
  maturity: incubator
---

# Claude Design to PPTX

Turn a Claude Design export (a `deck-stage` HTML deck) into a native, editable PowerPoint file. Built to run on one deck or several in a single pass, with the user answering a short fixed intake once and then stepping back until there's a file to review.

This SKILL.md is the orchestration layer - the order of operations and the decisions. The detail lives in four reference files; read them at the point each is needed, not all up front:

- `references/run-intake.md` - the five questions the user answers once per run
- `references/wireframe-baseline-rules.md` - the conversion math (geometry vs font ratios) and what holds vs what gets hardened
- `references/conversion-playbook.md` - the full build process and the hardened build prompt
- `references/pptx-review-playbook.md` - the review-and-touch-up pass
- `assets/wireframe-template.html` - the deck-stage-compatible boilerplate

## The one-paragraph model

HTML is a flow layout; PowerPoint is absolute boxes at fixed coordinates. Conversion is translating between the two. Claude Design exports a 1920x1080 deck-stage with flex, grid, and px. The job: read the export, translate each rendered box to inches (`px/144`) and each font to points (`px x 0.5` - a different number, do not mix them), rebuild as native shapes, leave charts/graphs/diagrams as placeholder boxes the user fills by hand, embed the brand fonts, and QA the actual PPTX against the reference PDF. The PDF is ground truth, not the HTML.

## Scope - what this builds and what it doesn't

| Element | What happens |
|---|---|
| Text, headings, bullets | Native text boxes |
| Shapes, dividers, cards, chrome | Native shapes |
| Tables | Native editable PowerPoint tables |
| Backgrounds, gradients, fills | Real slide background fills |
| Logos, icons | Rasterized PNG, embedded |
| **Charts, graphs, diagrams** | **Placeholder box only** - sized, positioned, labeled. User builds the real visual by hand after export. |
| Photos | Labeled placeholder unless the user provides them |
| Animations, transitions | Not built - manual finish if needed |

Charts and diagrams are deliberately out of the automated path. Auto-built charts never matched cleanly and were the biggest source of rework. A correctly-sized empty box that the user finishes by hand is faster and more reliable than a wrong chart.

---

## Step 0 - Preflight (gate the whole run before doing any work)

Do all of this before building anything. It stops avoidable failures at the gate instead of mid-run.

1. **Confirm the folder shape.** Expect the layout in `run-intake.md`: one subfolder per deck, each with a `*-print.html` and a `*.pdf`, fonts shared at the top level or in the design system folder. If the shape is off, say so and ask the user to fix it rather than guessing.

2. **Check every deck has a reference PDF.** This is a hard gate. If any deck is missing its PDF, STOP and list which decks are missing one. Do not start the run until they're provided - the PDF is the only ground truth for QA, and finding it missing on deck 3 of 6 wastes the whole run.

3. **Locate the design system folder.** The user points to it in intake. Confirm it has the TTF fonts and logo PNGs. This is the source for assets and canonical token values (see precedence rule below).

4. **Toolchain check.** Confirm the QA render path is available in the sandbox - `python-pptx`, `poppler` (`pdftoppm`/`pdfinfo`), and a PPTX-to-PDF route (LibreOffice). If anything's missing, install it before building, don't let the first render fail silently:
   ```bash
   pip show python-pptx >/dev/null 2>&1 || pip install python-pptx --break-system-packages
   pdftoppm -v 2>/dev/null || (apt-get install -y poppler-utils 2>/dev/null || brew install poppler)
   which libreoffice soffice 2>/dev/null   # need one for pptx -> pdf
   ```

5. **Validation-gate awareness.** Look for a `.pipeline-validated` marker in the run folder or design system folder. If it's NOT there, this is a first run on this pipeline - tell the user the first finished deck must be opened in real PowerPoint to confirm chrome positions, embedded fonts, and font sizing before trusting a full batch. After they confirm it checks out, write the marker so later runs skip the nag. The skill can't see into PowerPoint, so this is the one thing it relies on the user to verify once.

## Step 1 - Intake (once per run)

Read `references/run-intake.md` and get the five answers: design system folder, fidelity bar, output naming, speaker notes, standalone-vs-section (+ optional master reference). These apply to every deck in the run unless the user flags a deck as different. Don't re-ask per deck.

If the user gave the answers already in the conversation, extract them - don't ask again.

## Step 2 - Per-deck recon (report before building)

For each deck, inspect the print HTML and report findings before building. Read `references/conversion-playbook.md` Step 1 for the exact commands. Confirm and record:

- Canvas dimensions from `<deck-stage width height>`. If it's NOT 1920x1080, recompute both ratios - do not reuse 144/0.5 blindly (formula in baseline-rules gap #2).
- Slide count (`<section>` count) and that it matches the PDF page count.
- The font variable and what it resolves to (whatever the deck's own design system names as its font - confirm, don't assume). Check for a Google Fonts CDN link - that's a blocker, fonts must be local `@font-face` + TTF.
- TTF presence in the design system folder. Present -> single pass. Missing -> two-pass with Arial then a font swap (conversion-playbook Step 2 and the Pass 2 prompt).
- Both token naming styles: `--t-*` is canonical, `--type-*` is legacy - map either.

State both conversions explicitly and sanity-check one known title (a 72px title must be 36pt, not 54pt) against the PDF before building all slides.

## Step 3 - Chart / diagram detection (the one human checkpoint)

Detect chart, graph, and diagram regions in the source - they appear as SVG, canvas, div-styled bars, or flat images. Tables are not charts; build those natively.

Before finalizing the build, report every placeholder: "Placeholdering N regions on slides X, Y, Z - [type] each." This catches the two ways detection misfires: a missed chart that would otherwise get rebuilt as stray shapes, or a non-chart (KPI stat block, card row, table) wrongly blanked into a box. If a region is ambiguous, flag it rather than guessing. This is the single most important review point in the whole flow - surface it clearly.

Placeholder spec (full version in conversion-playbook): a light rectangle with thin border at the exact measured box, labeled with what goes there pulled from the source (e.g. "CHART: cost by service (bar) - 7.6in x 4.2in"). Keep any title/caption sitting outside the plot area as live text.

## Step 4 - Build

Read `references/conversion-playbook.md` Step 5 (the hardened build prompt) and follow it. The non-negotiables: native shapes never screenshots, both conversions applied correctly, backgrounds as real slide fills not stacked rectangles, brand colors from tokens, fonts both referenced AND binary-embedded (verify the streams exist), headroom under variable-length titles, charts/diagrams as placeholders, tables native.

For section-of-master decks, keep slide masters and layouts consistent with the master reference (or with sibling sections built in the same run).

## Step 5 - Self-QA (per deck)

Render the built PPTX through `pptx -> PDF -> PNG` and compare slide-by-slide against the reference PDF - QA the PPTX, never the HTML. Use a fresh-eyes subagent for the visual comparison. Distinguish real file defects from QA-renderer artifacts (the preview is not PowerPoint). Read `references/pptx-review-playbook.md` for the structural + visual checklist.

## Step 6 - Hand off

Save each finished file per the naming pattern (new version, never overwrite). For each deck, hand back a short punch list of anything unresolved, tagged real-defect vs suspected-renderer-artifact, plus the list of chart/diagram placeholders the user needs to fill by hand. Then the user reviews, fine-tunes, and builds the real charts into the pre-sized boxes.

---

## Precedence rule - export vs design system

The export and the design system folder can disagree (deck built on an older token version, a color since changed). Resolve it this way, every time:

- **The export HTML is the truth for what's on the slide and where** - positions, layout, which tokens are used, slide content. That's what rendered into the PDF you're matching.
- **The design system folder is the truth for assets** - the actual TTF binaries and logo PNGs - and the canonical value when the export references a token it doesn't define locally.
- **If the export's token value and the design system's value actually conflict, flag it.** Don't silently pick one.

Color and typography come from the deck's own design system folder or an equivalent brand kit or tokens file the user provides. If the deck's folder is missing a value the export needs, fall back to neutral, accessible defaults (a dark neutral text color, a single accent, system-standard fonts) and say plainly to the user that you're assuming a default rather than inventing a brand value.

## No-stall defaults (so unattended runs don't block)

Every interactive fork has a default so a multi-deck run never halts waiting on input. Apply these unless intake said otherwise:

| Fork | Default |
|---|---|
| Found images - embed or placeholder? | Embed icons/logos; labeled placeholder for photos |
| Font not found at system path? | Arial fallback, flag the slide for a font-swap pass |
| Title wraps an extra line vs PDF | Let it reflow from the measured bottom (headroom rule) |
| Ambiguous chart vs native element | Flag in the placeholder report, lean toward placeholder for drawn visuals |
| A deck in the batch fails to build | Skip it, keep going, report it at the end - don't kill the run |
| Output file already exists | Save a new version (`_v2`), never overwrite |

The two things that DO stop the run: a missing reference PDF (Step 0), and an unvalidated pipeline on a first batch run (Step 0).

## Why this works (the short version)

Recon-first so no work is wasted on wrong assumptions. PDF is ground truth, not HTML. Native shapes, never screenshots. Two conversions, not one - geometry `px/144=in`, fonts `px x 0.5=pt`, different numbers. Backgrounds are slide backgrounds. Fonts embedded as binaries, verified. Charts and diagrams are placeholders, finished by hand. QA the PPTX, not the HTML. The user answers five things once and reviews at the end.
