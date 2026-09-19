# PPTX Review Playbook

How to take the freshly built PPTX and prompt a structured review pass that closes the gap to the wireframe - without chasing ghosts.

## Contents

- The core principle
- Step 1 - Get the right comparison surface
- Step 2 - Structural check (catch the obvious misses first)
- Step 2b - Object inspection (prove "editable" before you look at pixels)
- Step 3 - Visual check against the wireframe
- Step 4 - Build the punch list
- Step 5 - The targeted fix prompt
- Step 6 - Re-review and decide when to stop
- What to finish by hand in PowerPoint
- Quick reference - which tool for what
- The one-line version

Fourth file in the set:
- wireframe-baseline-rules.md - constrain the wireframe
- wireframe-template.html - the boilerplate
- conversion-playbook.md - build the PPTX
- pptx-review-playbook.md (this file) - review and touch up

The build prompt already runs a QA loop. This playbook is the *human-in-the-loop* review that follows it - the pass where you compare the built file against the wireframe, write a punch list, and direct targeted fixes. The build QA catches obvious breaks. This catches the things that are technically correct but wrong against intent.

---

## The core principle

You are reviewing the PPTX against the PDF, using your own eyes plus a fresh-eyes agent - not re-reviewing the HTML. The PDF is ground truth for how it should look. The PPTX is what you actually shipped. The HTML is already behind you. Three sources, and only two of them matter at this stage.

And the hardest discipline in the whole review: **distinguish a real file defect from a renderer artifact.** The QA preview is not PowerPoint. Some things look broken in the preview that are perfectly fine in the actual file, and occasionally the reverse. Chasing a renderer artifact as if it were a real bug cost several iterations on the FinOps build. If you can spot-check the file in real PowerPoint, do - one human "looks right in PowerPoint" beats three rounds of preview guessing.

---

## Step 1 - Get the right comparison surface

Before reviewing anything, make sure you're looking at the PPTX rendered correctly, not the HTML.

The correct QA render path is `pptx -> PDF -> PNG`, one image per slide. (Playwright/browser screenshots render HTML, not a .pptx - wrong target. This trips people up because "screenshot the slides" sounds right.)

**[Cowork]** Ask the builder to export the PPTX to PDF, then rasterize to per-slide PNGs in the sandbox, and lay them next to the reference PDF pages.

**[CLI]** Same - `libreoffice --headless --convert-to pdf`, then `pdftoppm` to PNGs.

Open the reference PDF and the rendered PNGs side by side, in slide order. That's your review surface.

---

## Step 2 - Structural check (catch the obvious misses first)

Fast pass. You're confirming nothing is *missing* before judging whether anything is *wrong*.

- Slide count matches the source exactly
- No missing copy - every block from the PDF made it across
- Logo present on every slide, correct variant (color on light backgrounds, invert/white on dark)
- No leftover placeholder text - search for "TODO", "INSERT", "Lorem", "[", "PLACEHOLDER"
- Speaker notes present/absent per what you asked for

If structure fails, fix that before anything visual - a missing slide changes every numbering and layout judgment that follows.

---

## Step 2b - Object inspection (prove "editable" before you look at pixels)

A rendered PNG cannot tell a native text box from a picture of one. "Native shapes, never screenshots" is the build's top non-negotiable, so check it with code, not eyes, before the visual pass. Three standard-library scripts live in this skill's `scripts/` directory (vendored from gnipbao/knowledge-cat-ppt-skill, MIT, pinned 889c3dc; they read the OOXML directly and need no python-pptx):

```
python3 scripts/check_pptx_editability.py "[PPTX_PATH]" --expected-slides N --fail-on-image-only-slides --require-native-table
python3 scripts/probe_pptx_editability.py "[PPTX_PATH]" --search "[a phrase that appears on one slide]"
python3 scripts/extract_pptx_text.py "[PPTX_PATH]"
```

- The checker counts text shapes, pictures, charts, and tables per slide and exits non-zero on any slide that is image-only or below the text-shape minimum. Add `--require-native-table` only when the source has a table; leave `--require-native-chart` off, since this skill deliberately leaves charts as placeholder boxes.
- The probe copies the file, rewrites one text run, reopens the copy, and confirms the edit landed while the original's checksum is unchanged. Pass a real phrase from the deck; the default search string is the vendor's demo text and will not match. A failing probe means the text is not a native text object, whatever the render looks like.
- The extractor dumps every text run per slide, which is the fastest way to run the placeholder search from Step 2 ("TODO", "INSERT", "Lorem", "[", "PLACEHOLDER") across the whole file at once.

Any error here is a P0 (see Step 4) and goes back to the build before Step 3 starts. Both scripts carry `--self-test`; run it once on a new machine before trusting a green result.

---

## Step 3 - Visual check against the wireframe

Now the real review. Go slide by slide against the PDF. Lean on the complexity flags from the build (the chart-heavy and dense slides are where problems hide). For each slide check:

- **Brand colors** - only palette tokens, no stray generic blues/blacks that aren't in the token table
- **Fonts** - the deck's actual brand font rendering, not a system fallback; both referenced AND embedded (the file should carry its fonts); if Arial appears anywhere it means TTFs weren't found or a Google Fonts link was used instead of local `@font-face`
- **Type sizing** - titles and body match the `--t-*` scale; nothing oversized (the ~50% font-scale bug shows up here as wrapped titles and overlap); flag any text that appears sized differently from the token table - it may have been an inline literal that the conversion missed
- **Text fit** - nothing cut off at a box edge, no overflow, no collision under a wrapped title
- **Alignment** - columns line up, chrome (footer, accent line, logo) sits identically across slides
- **Logos** - correct aspect ratio, not stretched or squished
- **Backgrounds** - gradients/fills are real slide backgrounds, not rectangles sitting on top of content
- **Chart/diagram placeholders** - every chart, graph, and diagram from the PDF has a placeholder box at the right size and position, clearly labeled with what goes there. No chart was accidentally rebuilt as stray shapes; no real content (KPI block, table, card row) was wrongly blanked into a box. This is where a detection miss shows up.
- **Tables** - built natively as editable PowerPoint tables (not boxed, not a picture), cell values intact
- **Images** - embedded (not linked), photo placeholders clearly labeled so you know what to drop in later

---

## Step 4 - Build the punch list

Write down every issue as `slide number + specific defect`. Specificity is what makes the fix pass work - "redo slide 5" gets a guess; "slide 5 right column is in Arial instead of the brand font" gets a fix.

Good punch-list entries:

```
- Slide 3: headline overflows the text box on the right edge
- Slide 5: logo stretched horizontally - aspect ratio wrong
- Slide 7: body copy in Arial, should be the brand font
- Slide 9: background is a generic dark blue - should be the token value from the design system
- Slide 12: two-column layout uneven, left column much wider than right
- Slide 2: title wrapped to 2 lines and the subtitle below it is overlapping
```

As you write each one, tag it: **real defect** or **suspected renderer artifact**. If you can open it in PowerPoint, confirm. Don't send renderer artifacts to the fix pass - you'll burn cycles chasing something that isn't broken.

Give every real defect a severity too, so the fix pass and the stop decision in Step 6 have an order to work in:

- **P0 - must fix before delivery:** file does not open; a slide is missing or its copy did not make it across; text is cut off, overlapping, or unreadable; placeholder text remains; a slide failed the Step 2b object inspection (image-only, or text that is not a native object); a chart or table from the PDF has no placeholder or was wrongly blanked into one.
- **P1 - fix before a client sees it:** wrong font or fallback font anywhere; off-token colors; chrome (logo, footer, accent line) shifted between slides; a stretched logo; low contrast or uneven spacing that hurts readability.
- **P2 - nudge if time allows:** sub-pixel alignment, a caption to tweak, a margin a couple of pixels off. These are the items Step 6 says to finish by hand.

A punch list with no P0s and a couple of P2s is done. A punch list with one P0 is not, however clean the rest looks.

---

## Step 5 - The targeted fix prompt

Feed the punch list back to the build session (or a fresh one pointed at the same file). The key constraints: fix only what's listed, verify only the affected slides, leave everything else alone.

```
The PPTX needs a targeted cleanup pass. File: "[PPTX_PATH]".

Here's my punch list from reviewing it against the reference PDF:

[paste the punch list, e.g.:]
- Slide 3: headline overflowing the text box on the right edge
- Slide 7: body copy in Arial instead of the brand font
- Slide 9: background should be the design system's dark navy token, not a generic dark blue
- Slide 12: two-column layout uneven - make columns equal width

Fix each of these in the existing file. After fixing:
1. Re-render ONLY the affected slides (pptx -> PDF -> PNG)
2. Use a fresh-eyes subagent to verify just those slides against the reference PDF
3. Confirm the fixes look right before wrapping up

Rules:
- Do NOT touch slides that aren't on the list
- If any listed item is actually a renderer artifact and the underlying file is
  already correct, tell me that instead of "fixing" it
- For font fixes, verify the TTF binaries are still embedded after the change
- Preserve all other content, positions, and colors exactly
```

---

## Step 6 - Re-review and decide when to stop

Open the updated file. Spot-check only the slides that were on the punch list.

Decision rule:
- **2-3 small issues left** -> one more targeted pass with the same prompt structure.
- **Mostly clean, only nits remain** (a margin 2px off, one caption to tweak) -> stop iterating. Those are faster to fix by hand in PowerPoint than to round-trip with the builder.
- **Same issue keeps coming back** -> it's probably a renderer artifact, or the instruction is ambiguous. Stop, open it in real PowerPoint, and confirm whether it's real before another cycle.

Know when "good" is good. A customer-facing deck earns the extra passes; an internal draft doesn't. Match the effort to the fidelity bar you set at intake.

---

## What to finish by hand in PowerPoint

Some things are just faster to do yourself than to prompt for. Don't iterate the agent on these:

- **Building the charts, graphs, and diagrams** into the placeholder boxes the build left - this is the main finishing work now, and it's deliberate. The boxes are already sized and positioned; you build the real visual inside each one, slide by slide.
- **Dropping in real photos** where the build left labeled placeholders - drag and drop
- **Speaker notes** the agent couldn't know (weren't in the source)
- **Animations and transitions** - the build is static slides; add motion manually if needed
- **Sub-pixel alignment** - if something is 2px off, nudge it
- **Copy accuracy** - the agent uses the source text faithfully, so source errors carry through; you proofread

---

## Quick reference - which tool for what

| Task | Tool |
|---|---|
| Render the PPTX for review | builder -> pptx to PDF to PNG (sandbox / LibreOffice) |
| Prove native editability | `scripts/check_pptx_editability.py` and `scripts/probe_pptx_editability.py` (Step 2b) |
| Structural + visual review | the rendered PNGs next to the reference PDF, your eyes |
| Confirm a suspected artifact is/isn't real | real PowerPoint, if available |
| Targeted fixes | build session + punch list |
| Final polish (photos, notes, nudges) | PowerPoint, by hand |

---

## The one-line version

Render the PPTX (not the HTML) to images, compare to the PDF with fresh eyes, write a specific punch list tagging each item as real-or-artifact, fix only what's listed and verify only what changed, and stop iterating the moment the leftovers are faster to nudge by hand than to round-trip.
