# Claude Design to PPTX - Conversion Playbook

The repeatable process for turning a Claude Design export into a native, editable PowerPoint file.

This is the main file in a set of four:
- wireframe-baseline-rules.md - how to constrain the wireframe before it gets here
- wireframe-template.html - the boilerplate that follows those rules
- conversion-playbook.md (this file) - intake, prompt, build
- pptx-review-playbook.md - the review-and-touch-up pass after the build

Primary environment is Cowork (where you are now). Claude Code CLI deltas are flagged inline with **[CLI]**. The process is the same shape in both; only a few tool names and a setup step differ.

---

## The mental model in one paragraph

HTML is a flow layout - things stack and wrap and respond to each other. PowerPoint is absolute positioning - every shape is a fixed box at a fixed coordinate with no awareness of its neighbors. Conversion is translating between those two models. Claude Design exports flow-model HTML (a 1920x1080 deck-stage with flex, grid, and px). Your job is to feed the builder a clean enough wireframe that the translation is mostly mechanical, point it at the right files, hand it the two conversion ratios, name the failure modes before they happen, and QA the actual PPTX (not the HTML) against the reference PDF. That's the whole playbook. The rest is detail.

---

## What you need before starting

Gather these into one folder before you open a build session. Everything in one place keeps the builder from hunting.

1. **The Claude Design project export (unzipped)** containing:
   - A `*-print.html` file - this is the source, not the interactive version
   - `assets/` and `uploads/` (logos, photos, fonts, source markdown)
   - `deck-stage.js` - ignore this, it's a browser runtime file, not content
2. **A PDF export from Claude Design** - the visual ground truth for comparison
3. **TTF font files** for the brand fonts used (ideally already in the project's `fonts/` or a design-system folder)

If any of the three is missing, the process still runs but degrades: no PDF means you're QAing against the HTML render (worse); no TTFs means a two-pass font swap (slower). Get all three if you can.

---

## Step 1 - Inspect the folder before asking anything

Inspect what's actually there before running intake questions. The inspection answers most questions for you; only ask the user what the files can't tell you.

Check, and write down the answers:

- Is there a `*-print.html` file? If there are multiple, flag them - you'll ask which is the source. (Decks ship multiple HTML variants; the FinOps export had two with identical line counts.)
- Is there a PDF? What's the exact filename, including extension?
- Are TTF font files present? Where?
- What does the print HTML actually use - confirm the canvas dimensions from `<deck-stage width="..." height="...">`, count the `<section>` slides, and grep the CSS for the font variable and what it resolves to.

**[Cowork]** Run these in the sandbox:

```bash
# from inside the project folder
ls -1                                   # spot the print html, pdf, deck-stage.js
grep -oE '<deck-stage[^>]*>' *-print.html        # canvas dimensions
grep -c '<section' *-print.html                  # slide count
grep -iE "font-family|--font" *-print.html | head # font variable + resolution
ls fonts/ assets/ uploads/ 2>/dev/null           # asset + font inventory
```

**[CLI]** Same commands, plus confirm the toolchain is installed (see the CLI setup box at the end).

---

## Step 2 - The font decision (this sets one pass or two)

The font situation is the single biggest fork in the whole process.

**TTFs are present for the brand fonts** -> single pass. Embed the actual fonts directly. No substitution. This is the good case - say so and move on.

**TTFs are NOT present** -> two passes:
- Pass 1: build with Arial as a stand-in. Flag every slide where the swap causes layout trouble (Arial's character metrics differ from most brand display/body fonts, so text overflows, lines re-wrap, spacing drifts).
- Pass 2: once Pass 1 is reviewed, get the TTFs and run a targeted font swap (template prompt at the end of this file).

**Resolve the font variable either way.** Claude Design references fonts by `--font`. Read whatever the project's design system names as its deck font and treat that as the confirmed answer - don't assume a specific typeface. Still grep to confirm what it actually resolves to; if it resolves to nothing (no design system provided), fall back to a neutral default font and say so.

**Also check for Google Fonts CDN links - these are a blocker regardless of which font is in play.** Any design system that requires local `@font-face` declarations pointing at TTF files should be honored. A `<link href="https://fonts.googleapis.com/...">` in the deck HTML means the font won't survive a sandboxed build and can't be embedded in the PPTX. Correct it before proceeding.

```bash
grep -i "fonts.googleapis.com" *-print.html   # should return nothing
grep -i "@font-face" *-print.html              # should show local TTF paths
```

---

## Step 3 - Minimal intake questions

Only ask what Step 1 couldn't answer. Don't ask for things the files already told you.

1. If multiple print HTML files exist: which one is the source?
2. Speaker notes in the output? (yes/no)
3. Standalone deck, or one section of a larger deck to be merged later? (Affects whether slide masters/layouts must stay consistent across sections so they merge cleanly. The AWS Practice deck builds section by section into a master - see the build guide - so this is usually "section to be merged.")
4. **Fidelity bar** - exact visual reproduction, or faithful-and-on-brand rebuilt natively (where editable wins over pixel-matching)? These imply different tradeoffs. Pick one.
5. **Charts and diagrams are NOT built** - they become labeled placeholder boxes (see "Charts and diagrams" below). No data-accuracy question - you build the real visuals by hand after export. Confirm which slides have them so the placeholders get sized right.
6. Confirm output filename. Customer-facing follows `<YourOrg>_<Customer>_<Doctype>.pptx` (the org name the user actually uses); internal is descriptive. Default to a new version (`_v2`) rather than overwriting.

---

## Step 4 - Confirm the paths out loud

Before generating the build prompt, lock and read back:

1. Source directory (the unzipped project folder)
2. Primary HTML filename (the `*-print.html`)
3. PDF reference filename (exact, with extension)
4. Output directory (where the finished .pptx lands)
5. Font directory (if embedding TTFs)

Repeat these back so typos get caught before the build, not during it.

---

## Step 5 - The hardened build prompt

Fill every `[PLACEHOLDER]`, delete the lines that don't apply, and drop the whole block into a fresh build session. This folds in every lesson from the prior builds - the two conversions, title-wrap headroom, real backgrounds, font binary embedding, SVG rasterization, the correct QA path, and renderer-vs-real-defect triage.

```
Convert an HTML slide deck into a native, editable PowerPoint file.

FIRST: read the pptx skill before doing anything else.
  [Cowork] Read the pptx SKILL.md and follow it.
  [CLI]    Read /mnt/skills/public/pptx/SKILL.md before anything else.

SOURCE FILES
- Source directory:    "[SOURCE_DIRECTORY]"
- Primary HTML source: "[PRINT_HTML_FILENAME]" - use THIS file, not any other HTML variant
- Visual ground truth: "[PDF_FILENAME]" - the authority for how each slide should look
- Brand tokens:        the :root block in the print HTML (colors, fonts, scale) - treat as source of truth
- Font files:          "[FONT_DIRECTORY]"   <- delete this line if no TTFs
- Assets:              "[ASSETS_DIRECTORY]" (logos, photos, icons)
- Output:              save as "[OUTPUT_FILENAME].pptx" to "[OUTPUT_DIRECTORY]"
- Ignore deck-stage.js entirely - it is a browser runtime file, not content

RECON FIRST - report back before building anything:
- Confirm the canvas pixel dimensions from <deck-stage> (expected 1920x1080)
- State BOTH conversions explicitly, they are different numbers:
    GEOMETRY: pixels / 144 = inches   (at 1920px wide canvas)
    FONTS:    pixels x 0.5 = points   (144 px/in canvas / 72 pt/in PowerPoint)
- Sanity-check ONE known title: a 72px title must convert to 36pt. Verify against
  the PDF before building all slides. If it lands ~50% oversized, the wrong ratio
  is in play - stop and fix it.
- Count the <section> slides and confirm it matches the PDF page count
- Inspect the CSS: confirm which actual typeface the font variable resolves to
  (do not assume the brand headline font)
- Inventory assets and fonts; confirm the PDF reference is readable
- Decide and state up front: SVG logos/icons get rasterized to high-res PNG at
  the design colors (preferred - PPTX SVG support is unreliable), not dropped as SVG

FIDELITY BAR
- [Pick one: "Exact visual reproduction" / "Faithful, on-brand native rebuild -
   editable always wins over pixel-matching"]

CHARTS AND DIAGRAMS - DO NOT BUILD THESE
- Charts, graphs, and diagrams (flowcharts, architecture, anything that is a custom
  drawn visual) are NOT rebuilt. They become empty placeholder boxes, sized and
  positioned exactly where the visual sits in the source, so the human drops the real
  one in by hand after export. See the "Charts and diagrams" rules below.
- Tables ARE built natively (real editable PowerPoint tables) - a table is structured
  text you want to edit, not a drawn visual.

BUILD REQUIREMENTS
- Native text boxes, shapes, and native tables only - NO screenshot/image-based slides
- Charts/graphs/diagrams = placeholder boxes only (rules below), never auto-rebuilt
- Embed all images and assets in the file - no external references
- Convert CSS gradients/overlays/fills on a section into the slide's real background
  fill - do NOT fake them with rectangles stacked on top of content
- Preserve brand colors exactly as defined by the tokens
- Fonts: this means BOTH referencing the typeface in every run AND injecting the TTF
  binaries into the .pptx package so fonts travel with the file. Verify the embedded
  font streams exist in the final file - do not assume.
- Prefer solid pre-computed colors over alpha/transparency on text (transparency can
  trigger QA-renderer artifacts)
- Do NOT hard-code vertical positions for content below variable-length titles. Assume
  a title may wrap one extra line vs the PDF - leave headroom, or flow the next element
  from the measured bottom of the element above it.
- Percentages resolve against the 1920x1080 stage (e.g. 57% width = 1094px = 7.6in)

CHART / DIAGRAM PLACEHOLDER SPEC
- Detect chart, graph, and diagram regions in the source. They show up as SVG, canvas
  elements, div-styled bars, or flat images. Tables are NOT charts - build those natively.
- For each one, drop a placeholder: a light rectangle with a thin border at the exact
  measured box (top/left/width/height converted via px/144) where the visual sits.
- Label each placeholder with what goes there, pulled from the source: e.g.
  "CHART: cost by service (bar) - 7.6in x 4.2in". Keep any real title/caption text that
  sits OUTSIDE the plot area as live text - only the drawn visual becomes the box.
- Report every placeholder before finalizing: "Placeholdering N regions on slides X, Y,
  Z - [type] each". This is the one human checkpoint that catches a missed chart or a
  false positive (a KPI stat block wrongly blanked). Surface it, don't bury it.
- If unsure whether a region is a chart or a native element (table, card row), flag it
  in the report rather than guessing - a wrong call either loses content or leaves a box.

FONT BLOCK - use ONE:
  -- A: TTFs available (single pass) --
  - Embed the actual brand fonts ([FONT_NAMES]) from the font directory - do not
    substitute system fonts. Confirm the CSS font variable mapping first.
  -- B: no TTFs (two-pass) --
  - Replace all [ORIGINAL_FONT] with Arial - intentional and temporary, a font-swap
    pass follows. Flag every slide where the Arial swap causes overflow/re-wrap/drift.

SPEAKER NOTES: [No speaker notes / Include speaker notes]

MULTI-SECTION (add only if applicable):
- This is one section of a larger deck - use consistent slide masters and layouts so
  sections merge cleanly later.

QA BEFORE SAVING
- Render the generated PPTX to images (pptx -> PDF -> PNG) and compare slide-by-slide
  against the reference PDF. Do NOT screenshot the HTML - the thing being QA'd is the
  PPTX, not the source.
- Use a fresh-eyes subagent for the visual comparison.
- The QA renderer is NOT PowerPoint. Distinguish real file defects from renderer-only
  artifacts; if the file is correct but the preview looks off, say so rather than
  chasing it.
- Fix overflow, overlap, missing assets, and layout breaks. One clean fix-and-verify
  cycle per real defect - don't chase sub-pixel nits.
- Flag any slide where native shapes could not faithfully replicate the original -
  better to know now than to find it in PowerPoint.

ENVIRONMENT NOTE
- Final viewing environment is [PowerPoint on Mac/Windows]. The sandbox preview
  renderer is an approximation. I [can / cannot] spot-check in real PowerPoint between
  iterations.
- Polish for first delivery: [customer-facing, fully clean / internal draft, 90% then
  show me].
```

---

## Step 6 - What to watch during the build

The builder runs recon, then build, then QA. You don't intervene unless it asks. Predictable questions and your answers:

- "I found N images - embed or placeholder?" -> embed icons/logos; placeholder for photos you'll drop in later.
- "Placeholdering N chart/diagram regions on slides X, Y, Z" -> confirm the list is right - flag any missed chart or any non-chart wrongly boxed.
- "Brand font not found at system path - continue with fallback?" -> yes, Arial fallback, and note it for a font-swap pass.
- "A title wraps to two lines and collides with the content below." -> that's the headroom rule doing its job; let it reflow from the measured bottom.

Let the full QA loop finish before you open the file. Don't grab it mid-build.

---

## Skills and tools - what to call on

**[Cowork] - primary**
- **pptx skill** - the core builder. Read its SKILL.md first; it handles native shapes, text, and font embedding.
- **The project's own brand kit or design tokens skill/file, if one exists** - auto-load it for any branded deliverable to confirm tokens, logo variants, and type rules. If none exists, use neutral accessible defaults and say so.
- Sandbox shell for recon (grep/ls), PDF rasterization, and the pptx->PDF->PNG QA render.
- A fresh-eyes subagent (Task tool) for the slide-by-slide visual comparison - a second set of eyes catches what the builder's own context misses.

**[CLI] - deltas**
- Same pptx skill at `/mnt/skills/public/pptx/SKILL.md`.
- One-time toolchain setup (check before the first run):
  ```
  pip show python-pptx pdfplumber pypdf     # PPTX build + PDF parse
  npm list -g pptxgenjs                      # alt PPTX builder
  pdftoppm -v ; pdfinfo --version            # poppler: PDF<->image
  fc-list | grep -i poppins                  # brand font installed?
  ```
  Install the missing ones: `pip install python-pptx pdfplumber pypdf`,
  `npm install -g pptxgenjs`, `brew install poppler` (Mac) / `sudo apt install poppler-utils` (Linux),
  fonts from Google Fonts if absent.

The build approach is identical across both - the only real difference is that [CLI] needs the local toolchain present, and [Cowork] has it in the sandbox already.

---

## Pass 2 - font swap (only if you built with Arial)

After Pass 1 is reviewed and the layout looks right, swap Arial for the real brand font:

```
The Pass 1 deck is at: "[PASS_1_PPTX_PATH]"
TTF files for [BRAND_FONT] are at: "[FONT_DIRECTORY]"

Targeted font swap:
- Replace every Arial run with [BRAND_FONT] using the provided TTFs
- Inject the TTF binaries into the .pptx package (verify the font streams exist)
- Re-render only the slides flagged for layout issues in Pass 1
- Fix any new overflow/spacing caused by the font metric change
- Save as "[OUTPUT_FILENAME]_v2.pptx"
```

---

## The non-negotiables (why this works)

- **Recon-first gate.** Confirm dimensions, both conversions, slide count, and the font variable before building anything. Zero wasted work on wrong assumptions.
- **PDF is ground truth, not the HTML.** The HTML carries interactive states (hover, active flow steps) that don't all show at once. The PDF is the rendered truth. If they conflict, match the PDF.
- **deck-stage.js is always ignored.** Browser runtime, no content. Saying so stops the builder parsing JS as slides.
- **Native shapes, never screenshots.** Screenshot slides look identical and are useless to edit. This is the single most important instruction for a usable file.
- **Two conversions, not one.** Geometry `px/144=in` and fonts `px x 0.5=pt` are different numbers. Confusing them oversized every font ~50% on the first FinOps pass.
- **Backgrounds are slide backgrounds, not stacked rectangles.** Rectangles cover content and break editing.
- **Embedding fonts is two steps.** Reference the typeface AND inject the binaries. Verify the streams exist.
- **QA the PPTX, not the HTML.** Render pptx->PDF->PNG and compare to the reference PDF with fresh eyes. Playwright screenshots HTML - wrong target.

---

## Worked example - FinOps deck (May 2026)

How this played out in practice, as a reference case.

- **Files present:** `Cloud FinOps and Cost Optimization-print.html`, `...Visual.pdf`, full TTF libraries for both the display and body fonts in the design-system fonts folder.
- **Canvas:** 1920x1080, 8 slides, confirmed up front.
- **Font situation:** deck used a `--font-display` token that resolved to a secondary brand font, not the primary corporate font the team expected - caught by grepping the variable instead of assuming. TTFs present -> single pass.
- **Duplicate HTML flag:** two print HTML files with identical line counts; asked which was source. Answer: the Cloud FinOps one.
- **What broke and got fixed:** first-pass fonts oversized ~50% (wrong ratio), title wraps collided with fixed-offset content, a translucent right-aligned run truncated in the QA renderer only (not in the real file), font binaries initially not embedded. All now pre-empted by the build prompt above.
- **Iteration count:** ~9 render-and-fix cycles for a customer-facing bar. An internal draft would stop at "90% then show me."
- **Output:** `<YourOrg>_FinOps_CloudCostOptimization_Deck.pptx`.

---

## Known gaps and open questions

Honest list of where this playbook is still soft or unproven. Read before betting a customer deadline on it.

1. **Can Claude Design actually be constrained? - Partially confirmed.** An earlier structural test confirmed that chrome `--ch-*` constants, the `.slide-chrome` component structure, dark/light variant switching, logo selection, `--t-*` type tokens, and the `--font` token all held correctly in the Claude Design HTML export. The constraint approach works at the HTML level. What remains untested: whether those chrome constants land at the correct PPTX inch positions after conversion (the deck-stage export was reviewed as HTML only - a PPTX export and inch-position check hasn't been run yet). If chrome drifts in the actual PPTX, fall back to the HARDEN math in the baseline rules as the safety net.

2. **The 144 / 0.5 ratios are canvas-specific.** They're correct for a 1920-wide stage. If Claude Design ever exports a different width (some templates differ), recompute: geometry = px / (width / 13.333); font = px x (72 / (width / 13.333)). The recon step catches the dimension, but the builder must recompute rather than reuse 144/0.5 blindly.

3. **Charts and diagrams are out of the automated path on purpose.** They are not rebuilt - they become labeled placeholder boxes you fill by hand after export. This removes the old weakest link (auto-built charts never matched cleanly). The remaining risk moved to detection: a missed chart gets rebuilt as stray shapes, or a non-chart (KPI block, card row) gets wrongly boxed. The pre-finalize placeholder report is the control - review it every run.

4. **No defined "good enough" threshold.** The playbook says "one clean fix per real defect" but doesn't quantify acceptable residual drift. For now that's a judgment call per deck and per fidelity bar. If this becomes a team process, a checklist with a pass/fail bar (covered in pptx-review-playbook.md) should harden into an explicit acceptance standard.

5. **Section merge consistency isn't fully specified.** The AWS deck builds section by section into a master. Keeping slide masters identical across separately-built sections is called out but not proven - sections built in different sessions can drift. The assembly/QA block in the build guide is the current control; watch the section transitions closely.

6. **Cowork vs CLI parity is assumed, not tested.** The build approach should be identical, but the QA render path and font-embedding verification may behave differently between the sandbox and a local toolchain. First time you run each environment, verify the font streams and the QA render explicitly rather than trusting parity.
