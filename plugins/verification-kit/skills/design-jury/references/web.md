# Medium module: web (Awwwards jury)

The web module scores a website or web page on the four Awwwards jury categories. It is
the only module so far; slides is next. A judge reads this whole file before scoring.

## Contents

- [The scale is compressed: read this first](#the-scale-is-compressed-read-this-first)
- [Categories and weights](#categories-and-weights)
- [Design (40%)](#design-40)
- [Usability (30%)](#usability-30)
- [Creativity (20%)](#creativity-20)
- [Content (10%)](#content-10)
- [Caps that cross categories](#caps-that-cross-categories)
- [Render recipe](#render-recipe)
- [Purposes and floors](#purposes-and-floors)
- [Defers to](#defers-to)
- [Sources](#sources)

## The scale is compressed: read this first

These are Awwwards numbers, not school grades. Across 288 juror category scores on four
recent Sites of the Day, 7 was given 53% of the time, 8 36%, 9 5%, and 10 never. Site of
the Day winners average 7.1 to 8.0 per category. The Honorable Mention line is 6.5
overall. So:

| Score | Awwwards voting label | Means on this scale |
|---|---|---|
| 10 | "Perfect" | Almost never given by real jurors. Do not give it. |
| 9 | "Excellent" | Rare. Among the best on the web this year in this category; you can name the specific feature a peer would single out. |
| 8 | "Great" | Among the best of an award batch. Distinctive, controlled, nothing obviously weak. |
| 7 | "Very Good" | Award-grade craft. Site of the Day sites live here. |
| 6 | "Good" | Professional and clean, below the award line: a good agency or product site. |
| 5 | "It's ok" | Competent but templated; could be any brand. |
| 3-4 | "Not good enough" | Visible defects a visitor notices: broken layout, unreadable text, placeholder content. |
| 1-2 | "Not good enough" | Broken or empty in this category. |

Measured on all 93 Sites of the Day from 2026-07-03 to 2026-10-03: every published
overall falls between 7.17 and 7.73, and per-category jury means between 6.81 and 8.16.

A typical well-made business site is a 5 or 6 here, and that is a correct score, not a harsh
one. A judge that gives 8s by default is miscalibrated.

## Categories and weights

Design 40%, Usability 30%, Creativity 20%, Content 10% (Awwwards evaluation page). The
weighted overall is reported for information only; the gate is a floor per category.
Category keys in the judge output: `design`, `usability`, `creativity`, `content`.

The question Awwwards' voting widget asks for each category, paraphrased: Design, does it
engage the user through its use of colour, typography and imagery; Usability, can users
do tasks safely, effectively and efficiently while enjoying it; Creativity, does it solve
problems and communicate ideas in an innovative way; Content, is the content useful and
of high quality, and does it let the site serve its purpose.

Score each category on its own evidence. Usability is the least discriminating category
on the real jury (most scores are 7), so a wide Usability spread across your passes is a
sign of guessing.

## Design (40%)

Type system, layout and grid, color, hierarchy, consistency, art direction.

**Marks of 5:** one pleasant typeface with no visible scale, sizes and spacing that drift
between sections or breakpoints; stacked sections or a card grid that could hold any
brand's content; a default or trend palette with no evident role per colour; effects
everywhere with no hierarchy; with motion removed, the static frame is a polished
template. Template defaults from
`plugins/frontend-design/skills/design-taste-frontend/references/ai-tells.md` (centered
hero on a purple-blue gradient, three equal icon cards repeated, gradient headline text)
are evidence for this band.

**Marks of 7:** a visible type scale held across sections and both viewports, with
distinct display, body and label roles; a deliberate pairing of at most two families;
a consistent grid broken on purpose, with real negative space; one visual idea carried
through (a single accent over photography, a flat-shape palette); the first static frame
has a point of view with motion off.

**Marks of 8-9:** every type, colour and spacing choice reads as the only right one;
the system holds at every breakpoint; a brand-specific visual language that could not be
re-skinned onto another client; an element a peer would name (Typography honors, a
signature grid). Name it in the evidence or do not score above 7.

## Usability (30%)

Orientation, navigation, readability, responsiveness, feedback, accessibility floor,
perceived performance.

**Marks of 3-4:** text that cannot be read (contrast far too low, body under about 12 px);
horizontal overflow or a desktop layout squeezed onto the phone; no visible way in or
forward at all (no navigation, no instruction, no call to action, only unlabelled icons).

**Marks of 5:** a visitor cannot tell what to do next on the first screen (no visible
instruction, call to action or way in); tap targets too small on mobile; a custom cursor
or effects that hide the only control; mobile that is a shrunk desktop.

**Marks of 7:** the visitor always knows the next action, whether that is a labelled
menu, a single clear instruction ("click to start", "scroll", "draw a zero") or a
persistent contact; mobile is its own composition; readable text at both viewports;
some accessibility floor (alt text present) even if incomplete.

**Showcase versus product.** The real jury does not mark a showcase site down for an
entry gate, a loader, a single-screen experience or navigation tucked behind a menu:
Sites of the Day built exactly that way score Usability 7.2 to 7.5 (calibration,
2026-10-03). For `showcase`, judge those as a visitor who came for the experience
would: is the way in obvious, is the text that exists readable, does mobile work. Put
the friction (a 4-second loader, hidden navigation, no visible contact) in
`improvements`, not in the score. For `product`, the visitor came to do a task, so the
5-band marks above apply in full: a gate, a long loader or hidden navigation in front of
the task is a 5.

**Marks of 8-9:** clear orientation on the first view; mobile is first-class; motion aids
navigation (states, feedback, what happens next); content readable with motion off. The
real jury almost never gives 9 here (1 of 72 scores): require observed evidence for each
claim, and put what a headless capture cannot show (frame rate, keyboard focus, reduced
motion) in `not_observed` rather than crediting it.

## Creativity (20%)

Originality of the concept, of interaction, and of execution.

**Marks of 5:** this year's trend kit (horizontal-scroll gallery, cursor blob, boilerplate
WebGL plane, default smooth scroll) with no concept behind it; effects piled up so nothing
matters; the idea could be swapped onto another brand unchanged. Generic AI defaults
(see Design) score 3-4 here: there is no idea at all.

**Marks of 7:** one concept that shows up in copy, layout and motion together; a signature
moment (a considered transition, a pinned scroll sequence, a distinctive hover or menu);
consistent microinteractions.

**Marks of 8-9:** the concept is native to the subject (a type animator's site built from
moving type) rather than a technique applied on top; motion and interaction share one
authored language; the novelty never costs readability.

Motion is a large part of this category and a capture shows little of it. Use the
manifest's `ambient_motion`, `motion.libraries`, `custom_cursor`, `canvases` and `videos`
as evidence that motion exists, not as evidence that it is good. With no scroll frames
showing a motion idea, cap Creativity confidence at `low`.

## Content (10%)

Quality of copy, imagery and video, and how well they integrate with the design.

**Marks of 3-4:** lorem ipsum, placeholder testimonials, emoji standing in for imagery,
empty image plates.

**Marks of 5:** generic copy ("we create experiences", "unlock your potential") carrying
the page; stock-grade imagery; thumbnails with no problem, role or outcome.

**Marks of 7:** the material is real and made for this site: bespoke photography, 3D,
illustration or video, or named clients and projects, or copy with specifics (numbers,
places, roles). Some marketing filler is normal at this level.

**Marks of 8-9:** the content is the experience: art-directed imagery, 3D or video that
carries the story on its own, or projects that show problem, role, craft and outcome;
copy voice (where there is copy) matches the type and motion; words, images and motion
pull in the same direction.

**Showcase versus product.** Awwwards Content is imagery and video as much as words, and
the real jury rewards experience-led sites with almost no copy: a Site of the Day with 25
words on the page scored Content 7.75. For `showcase`, judge the craft and specificity of
whatever carries the content, visual or written; little text is not a defect on its own.
For `product`, the copy has to do the job (what this is, what to do, what happens next),
so a page that relies on imagery while the task needs words scores 5 or below.

Read `text.md` for this category; it holds the outline, navigation labels and body text.

## Caps that cross categories

Apply these after the band scores. Each is one juror's account (Hon Tran) and stated as a
cap, not a deduction.

- Mobile that is broken or a shrunk desktop: Usability at most 5, and the overall reads
  as below the Honorable Mention line.
- Original but hard to use loses to less original and flawless: when Creativity and
  Usability conflict, do not let a high Creativity score pull Usability up.
- Missing any one of art direction, directed motion or performance keeps a site in the
  low 7s at best; do not give 8 in Design or Creativity to a site missing one.

## Render recipe

```bash
node scripts/capture.mjs <url-or-file> <out-dir> [max-frames]
```

Produces desktop (1440 x 900) and mobile (390 x 844) render sets. Each has layout tiles
(the page from the top cut into viewport-height tiles before any scrolling, up to
max-frames tiles, so a very long page is cut off) and scroll frames
(real wheel scrolling, one frame per step), plus `text.md` and `manifest.json`. It presses
a lone entry-gate control ("Start", "Enter") once, as a visitor would, and records it.

What the capture cannot show is listed in every manifest's `not_observed`. Known capture
behaviour, from runs on 2026-10-03:

- Scroll-driven sites can render later scroll frames blank in headless Chrome while the
  layout tiles show the content. Tiles are then the evidence; blank frames are not
  scored.
- Tiles show sections in their pre-reveal state (dimmed text, unrevealed images).
- A site that themes only by a stored toggle is captured in its default theme.

## Purposes and floors

Floors live in [floors-web.json](floors-web.json), the one editable home for the numbers.
`scripts/aggregate.py` reads them; a report printed while `status` is `PROPOSED` says so.

- `showcase`: portfolios, launches, brand and campaign sites, anything that would be
  entered for an award.
- `product`: tools, dashboards, docs and app pages whose job is a task. Creativity has a
  lower floor here because a product page that chases novelty is worse, not better.

## Defers to

- **Developer Award track** (semantics and SEO, animations, accessibility, performance,
  responsive, markup; pass line 7): run `verification-kit:site-review`. Not scored here.
- **Charts or data visualisations on the page:** their encoding is the `dataviz` skill's
  job. Judge them here only as part of the page's design.
- **Generic AI defaults:** `plugins/frontend-design/skills/design-taste-frontend/references/ai-tells.md`
  is cited as evidence of template-ness only. Its bans (custom cursors, for example) are a
  builder's taste rules; Awwwards jurors reward some of them, so a ban is not a deduction
  here.

## Sources

Checked 2026-10-03 by the design-jury build. Research notes and raw records live in the
build workspace, `~/work/design-jury/research/`.

- Weights, scale and Honorable Mention rule: https://www.awwwards.com/about-evaluation/ and
  the Awwwards FAQ.
- Score distribution: per-juror tables on the Site of the Day pages for 'kin, Uncommon,
  Mat Voyce and Iventions (https://www.awwwards.com/sites/<slug>), plus the calibration set
  in [calibration-web.md](calibration-web.md).
- Qualitative band descriptors: Hon Tran, "Awwwards judging criteria" and "Best award
  winning websites 2026" (https://www.hontran.dev/blog/), one juror's account. Where the
  posts disagree with Awwwards' own numbers (they put Site of the Day at "mid-to-high
  8s"), the numbers win.
