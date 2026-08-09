# Wireframe Baseline Rules

How to constrain a Claude Design wireframe so it converts into an editable PPTX cleanly - and what to do when it doesn't.

This is one of four files in the Claude Design to PPTX system:
- wireframe-baseline-rules.md (this file) - the rules
- wireframe-template.html - a ready-to-use boilerplate that follows these rules
- conversion-playbook.md - the build process
- pptx-review-playbook.md - the review-and-touch-up process

---

## Read this part first - what you can and can't control in Claude Design

Here's the honest version, because the rest of this doc is useless if you don't know where it actually applies.

Claude Design doesn't hand you a blank HTML file you fully control. It builds decks inside a custom web component called `deck-stage`. When you export a project, the print HTML looks like this:

```html
<deck-stage width="1920" height="1080">
  <section> ... slide 1 ... </section>
  <section> ... slide 2 ... </section>
</deck-stage>
```

Each slide is a `<section>` sized to fill a 1920x1080 stage. Inside those sections, Claude Design writes flex and grid layouts, sizes type in px (72px titles, 30px body), and uses percentages for some widths. That's its native output. A representative export makes this concrete: a 1920x1080 stage with 26 px-based font declarations, 38 flex blocks, 7 grids, and 20 percentage values - typical of what any Claude Design deck-stage export looks like under the hood.

That matters because your `HTML_to_PPTX_Wireframe_Parameters.md` doc describes the opposite world - a 1333x750 canvas, `position: absolute` on everything, pt-based fonts, zero flex/grid/percentages. That spec is the ideal conversion target. Claude Design does not naturally produce it.

So there are two layers to this, and you need both:

1. **Constrain what you can** - the canvas size, the type scale, the brand tokens, the chrome, and whether content sits in clean rectangular regions. You influence these through your Claude Design project prompt and by handing it the template file. This is the "front of the funnel" effort and it makes conversion dramatically easier.

2. **Harden the conversion for what you can't** - deck-stage will still emit flex, grid, and px. The conversion playbook assumes that reality and gives the builder the math to translate it (px-to-inch for geometry, a separate px-to-point conversion for fonts). This is the "back of the funnel" safety net.

The rules below are split into those two buckets - CONSTRAIN (what to push Claude Design toward) and HARDEN (the conversion math the builder uses regardless of how clean the export is). Don't skip the HARDEN section thinking your wireframe was clean enough. It won't be.

---

## Part A - CONSTRAIN: what to push Claude Design toward

These are the things you can actually influence at design time. The more of these you lock, the less the conversion has to guess.

### A1. Lock the canvas to a known 16:9 size and write the conversion ratio down

Claude Design defaults `deck-stage` to 1920x1080. That's fine - it's a clean 16:9 that maps to a standard PowerPoint widescreen slide (13.333in x 7.5in). Don't fight it. Just confirm and record the exact pixel dimensions from the export before any layout math happens.

The two conversions you'll live by:

```
Geometry:  px / 144 = inches      (1920px / 13.333in = 144 px per inch)
Fonts:     px x 0.5 = points      (144 px/in canvas, 72 pt/in PowerPoint, so 1px = 0.5pt)
```

These are DIFFERENT numbers and getting them confused is the single most common failure (it oversized every font ~50% on the first FinOps pass). A 72px title is 36pt, not 54pt. A 30px body line is 15pt. Geometry and type do not share a multiplier.

If you ever build a wireframe from scratch at 1333x750 instead (the params-doc ideal), the geometry ratio becomes the cleaner `px / 100 = inches` and fonts can be authored directly in pt. But for a Claude Design export, assume 1920x1080 and the 144/0.5 pair.

| Canvas | Geometry ratio | Font ratio | When you'll see it |
|---|---|---|---|
| 1920 x 1080 | px / 144 = in | px x 0.5 = pt | Default Claude Design / deck-stage export |
| 1333 x 750 | px / 100 = in | author in pt directly | Hand-built wireframe following the ideal params doc |

### A2. Keep one type scale across the whole deck and put it in `:root`

Claude Design declares a type scale as CSS variables in `:root`. The canonical token names are `--t-*` (confirmed from Section 4 test). `--type-*` names exist as legacy aliases only - do not use them in new decks. A fixed, named scale means the builder maps six values to six point sizes once, instead of reading raw font-size off forty individual elements.

An example deck type scale, in both units so the builder has the answer pre-computed - replace these with the project's own scale if one is defined, otherwise these are reasonable neutral defaults:

| Role | CSS token | Wireframe (1920 canvas) | PPTX points |
|---|---|---|---|
| Slide title | `--t-title` | 72px | 36pt |
| Subtitle | `--t-subtitle` | 46px | 23pt |
| Body | `--t-body` | 30px | 15pt |
| Small / label | `--t-small` | 26px | 13pt |
| Micro / caption | `--t-micro` | 24px | 12pt |
| Eyebrow | `--t-eyebrow` | 24px | 12pt |

If a slide needs a size outside this scale, add a named token to `:root` with a pt comment rather than hardcoding it inline:

```css
--t-hero: 120px;   /* 60pt */
```

Inline `font-size` literals anywhere outside `:root` are not allowed - the conversion builder's type lookup table only covers named tokens. An inline literal either gets missed or triggers a wrong conversion.

### A3. Push content into clean rectangular regions

This is the highest-leverage thing you can do inside flex/grid reality. PowerPoint has no flow model - every shape is an absolute box. The closer your slide is to a small number of rectangular regions (a left column, a right column, a header strip, a card row), the more mechanically it converts.

In your Claude Design prompt, ask for layouts in terms of regions, not prose: "two-column slide, left column for the headline and three bullets, right column for the chart" converts cleanly. "A flowing narrative that wraps around an image" does not. Cards in a grid are great - each card is a box. Free-floating overlapping text on a photo is the hard case.

You can't force `position: absolute`, but you can ask for layouts that are *region-shaped*, which gives the builder obvious boxes to map even when the underlying CSS is flex.

### A4. Use the brand tokens, never literal hex

Claude Design's export should use named CSS custom properties (`var(--primary)` etc.), not literal hex sprinkled slide to slide. When the builder reads the CSS, a named token resolved once is the source of truth for that color everywhere. A literal hex value scattered across slides invites drift (one slide ends up one shade off and nobody notices).

Pull the actual token names and values from the project's own design tokens or brand kit if one exists. If none exists, fall back to a neutral, accessible default set like this one, and say so to the user rather than inventing brand colors:

```
--primary:      #0A3971   (dominant, ~25% of surface)
--primary-dark: #0A2546   (darkest, full-bleed backgrounds)
--accent:       #2287FD   (links, secondary accent, ~15%)
--highlight:    #FEC234   (single warm accent - one per slide max)
--muted-blue:   #48709F   (muted variant)
--soft-teal:    #80CCCD   (sparingly)
--white:        #FFFFFF
--off-white:    #F4F7FB
--border:       #CED8E6
--divider:      #E6ECF3
--fg-muted:     #6B89AE
```

### A5. Define chrome once and keep it identical on every slide

Chrome is the stuff that must not move between slides - footer bar, accent line, logo, slide number. If chrome is defined inline per slide, the conversion reconstructs it independently each time and you get a footer that sits 2px lower on section 4. Define it once as `:root` constants and annotate each with its PPTX inch equivalent in a comment, so the build script can write one `add_chrome()` function that references the spec directly.

The confirmed token names and values (from Section 4 test - these are what Claude Design actually exports):

```css
:root {
  /* ACCENT LINE - PPTX: top=Inches(6.90), height=Inches(0.03) */
  --ch-accent-top:  994px;   /* 994 / 144 = 6.90in */
  --ch-accent-h:      4px;   /* 4 / 144 = 0.03in */

  /* FOOTER BAR  - PPTX: top=Inches(6.93), height=Inches(0.57) */
  --ch-footer-top:  998px;   /* 998 / 144 = 6.93in */
  --ch-footer-h:     82px;   /* 82 / 144 = 0.57in */

  /* LOGO        - PPTX: left=Inches(0.69), top=Inches(0.25), width=Inches(1.39) */
  --ch-logo-left:   100px;   /* 100 / 144 = 0.69in */
  --ch-logo-top:     36px;   /* 36 / 144 = 0.25in */
  --ch-logo-w:      200px;   /* 200 / 144 = 1.39in */
  --ch-logo-h:       44px;   /* 44 / 144 = 0.31in */

  /* SLIDE NUMBER - bottom-right corner */
  --ch-num-right:   100px;   /* 100 / 144 = 0.69in from right */
  --ch-num-bottom:   24px;   /* 24 / 144 = 0.17in from bottom */
  --ch-num-size:     24px;   /* 24 x 0.5 = 12pt */
}
```

These constants are consumed by the `.slide-chrome` component - a `position: absolute; inset: 0; pointer-events: none` div appended as the **last child** of every `<section>`. It renders the accent line (`::before`), footer bar (`::after`), logo (`.ch-logo`), and slide number (`.ch-num`) from the token values. Two variants: `.slide-chrome` for light slides (primary-to-accent gradient line, light footer, color logo), `.slide-chrome--dark` for dark slides (highlight-color accent, dark footer, inverted logo).

The Section 4 test confirmed these constants held correctly in the Claude Design export HTML. PPTX inch-position verification is still pending.

### A6. Define a content safe zone and stay inside it

Content lives inside a box that clears the chrome on all four sides. Define the four edges once so every slide starts content from the same place. Without it, one slide starts content at the equivalent of 0.35in from the top and the next at 0.50in, and the deck looks subtly unsettled at the transitions.

```css
:root {
  /* SAFE ZONE @ 1920x1080 - PPTX inch equivalents in comments */
  --content-top: 144px;     /* Inches(1.0) - below logo/header */
  --content-left: 100px;    /* Inches(0.69) - matches --pad-x */
  --content-right: 1820px;  /* Inches(12.64) - right margin */
  --content-bottom: 980px;  /* Inches(6.81) - above accent line */

  /* Two-column helpers */
  --col-gap: 64px;          /* Inches(0.44) */
}
```

### A7. Fonts: require local TTFs and confirm the font variable resolves correctly

**The deck font comes from the project's own design system, not an assumption.** Read whatever the design system's `--font` token resolves to for deck exports, and use that. If the project has no design system or brand kit to point at, fall back to a neutral, widely-available default (a standard sans-serif such as Arial or the system UI font) and tell the user you're assuming a default rather than inventing a brand font. Still grep the CSS to confirm `--font` resolves to what you expect before building - don't assume.

**Local TTFs only - no Google Fonts CDN.** This is a hard rule learned from real testing, independent of which font is in play. Deck HTML must load the deck font via `@font-face` with local TTF paths, never via a `<link href="https://fonts.googleapis.com/...">`. A CDN link will fail in sandboxed build environments and leaves the font unembeddable in the PPTX. The correct pattern (shown here with a placeholder font name - substitute the actual deck font):

```css
@font-face { font-family: '[Deck Font]'; font-style: normal; font-weight: 400;
  src: url('fonts/[Deck-Font]-Regular.ttf') format('truetype'); }
```

During Step 1 inspection, grep for the Google Fonts link and treat its presence as a blocker - correct it before building:

```bash
grep -i "fonts.googleapis.com" *-print.html   # should return nothing
grep -i "@font-face" *-print.html              # should return local declarations
```

If TTFs are present and `@font-face` is local: single pass, embed directly. If TTFs are missing or the Google Fonts link is there: two-pass approach - build with Arial, then swap fonts once the TTFs are in place. (Detail in the conversion playbook.)

### A8. Logos and icons: expect to rasterize

Brand kits ship logos and icons as SVG. PowerPoint's SVG support is unreliable across versions. Decide up front that logos and icons get rasterized to high-resolution PNG at the colors used in the design, rather than relying on SVG dropping in as editable vectors. Note which logo variant each slide uses (color on light, invert/white on dark) so the builder picks the right file.

---

## Part B - HARDEN: the conversion math the builder uses no matter what

Even with a perfectly constrained wireframe, the export is still flex/grid/px. This is the translation layer the conversion relies on. It belongs in the build prompt verbatim (the conversion playbook includes it), but it lives here as the reference.

### B1. The two conversions, stated once, sanity-checked once

```
GEOMETRY:  pixels / 144 = inches      (at a 1920px-wide canvas)
FONTS:     pixels x 0.5 = points      (144 px/in canvas / 72 pt/in PowerPoint)
```

Before building all slides, the builder converts ONE known title and checks its rendered point size against the reference PDF. A 72px title must land at 36pt. If it lands at 54pt, the wrong ratio is in play - stop and fix it before propagating the error across forty slides.

### B2. Flex/grid becomes absolute boxes - measure, don't guess

The builder cannot read a left coordinate off a flex-centered element directly. It has to take the *rendered* position (render the HTML, read the computed box) and translate that box's top/left/width/height into inches via the geometry ratio. Region-shaped slides (Part A3) make this clean; free-flowing layouts make it lossy. The PDF is the tie-breaker for where things actually landed.

### B3. Don't hard-code vertical positions under variable-length text

Titles and rich text render at slightly different widths in the conversion tool than in the browser, so a title that's one line in the PDF may wrap to two in the build. If everything below it uses a fixed y-offset, it collides. Rule: leave headroom under titles, or flow the next element from the *measured bottom* of the element above it. Assume any title may wrap one extra line.

### B4. Percentages resolve against the 1920x1080 stage

A `width: 57%` is `0.57 x 1920 = 1094px = 7.6in`. Resolve every percentage against the known stage dimensions, not against whatever parent the flexbox implies. When in doubt, render and measure the computed pixel width and convert that.

### B5. CSS backgrounds become real slide backgrounds

Gradients, overlays, and color fills set on a section become the PPTX slide's actual background fill - not a rectangle stacked on top of the content. Stacked rectangles cover content and break editing. This is a frequent silent failure; call it out explicitly in the build prompt.

### B6. Prefer solid pre-computed colors over alpha on text

The sample export uses `rgba(255,255,255,0.06)` card fills and translucent text. Alpha on text can trigger renderer-only artifacts in the QA preview (a right-aligned run silently truncated on the FinOps build, cost several iterations to isolate). Pre-compute the effective color over its known background and use a solid value. Reserve alpha for large fills where it reads cleanly.

### B7. Font embedding is two steps, not one

"Embed the fonts" reads as one instruction but is two: reference the typeface in each text run, AND inject the TTF binaries into the .pptx package so they travel with the file. The pptx tooling does the first automatically and silently skips the second. The builder must verify the embedded font streams exist in the final file - don't assume.

---

## Quick reference card

| Thing | Constrain it to | Converts to |
|---|---|---|
| Canvas | 1920 x 1080 (accept deck-stage default) | 13.333in x 7.5in |
| Geometry | px values in clean regions | px / 144 = inches |
| Font size | `--t-*` tokens in :root, no inline literals | px x 0.5 = points |
| Title 72px (`--t-title`) | -> | 36pt |
| Body 30px (`--t-body`) | -> | 15pt |
| Colors | brand tokens, never literal hex | exact hex from token table |
| Chrome | `--ch-*` constants in :root, `.slide-chrome` as last child | one add_chrome() function |
| Safe zone | :root edges, all content inside | template region boundaries |
| Fonts | project's own deck font (or neutral default), local @font-face + TTFs, no Google Fonts CDN | embed binaries + reference typeface |
| Logos/icons | rasterize to high-res PNG | embedded PNG |
| Charts/graphs/diagrams | leave as-is in the wireframe | placeholder box (built by hand post-export) |
| Tables | clean rows/columns | native PowerPoint table |
| Backgrounds | gradient/fill on the section | real slide background |

---

## The one-line version

Constrain the canvas, the type scale, the tokens, the chrome, and the safe zone - and ask Claude Design for region-shaped layouts. Everything else the export still throws at you (flex, grid, px) gets translated by the two conversions: `px/144=inches` for geometry, `px x 0.5=points` for fonts. They are different numbers. That's the whole game.
