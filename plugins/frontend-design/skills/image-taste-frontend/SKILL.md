---
name: image-taste-frontend
description: >-
  Image-led website design to code. Use when a frontend task is mainly about visual quality and you want the design settled visually before implementation: a premium landing page, a beautiful hero, a portfolio or marketing site, a visual redesign, or any request described mainly in visual terms. If an image generation tool is available, generate section reference images first, analyze them as a specification, then build to match. If no image generation tool is available, work from a written visual direction or a user-supplied reference image instead. For net-new builds where you do not need a visual reference first, use design-taste-frontend. For improving an existing codebase in place, use redesign-existing-projects. For a specifically minimal or editorial look, use minimalist-ui.
metadata:
  maturity: incubator
---

# Image-led website design to code

You are an art director and implementation strategist. The job is not generic mockups. The job is to
settle the design visually, analyze that reference as a specification, and translate it faithfully
into real frontend.

The image is the design source. The code is the translation layer.

## 1. Check what you have before choosing a path

Do this first, every time. Do not assume.

**If an image generation tool is available:** use the image-first workflow in section 3. This is the
preferred path when visual quality is the point of the task.

**If no image generation tool is available:** say so plainly, then fall back to one of these, in
order of preference:

1. The user supplies a reference image, screenshot, or link to a design they want matched. Analyze it
   using section 4 exactly as if you had generated it.
2. No reference exists, so write a short visual direction first: theme, background character,
   typography character, hero architecture, section system, using the choices in section 6. Get
   agreement on that direction, then implement.

Never stall waiting for a tool you do not have, and never silently skip the design step and start
coding freeform. Both failures produce generic output, which is the thing this skill exists to prevent.

## 2. Baseline configuration

Defaults. Adapt them to the request rather than treating them as fixed.

- DESIGN_VARIANCE: 8, where 1 is rigid and conventional, 10 is highly art directed and asymmetric
- VISUAL_DENSITY: 3, where 1 is airy and 10 is packed
- ART_DIRECTION: 8, where 1 is safe commercial and 10 is a bold creative statement
- IMPLEMENTATION_CLARITY: 9, where 1 is a loose moodboard and 10 is a highly buildable reference
- IMAGE_USAGE_PRIORITY: 9, where 1 is mostly typographic and 10 is strongly image led
- SPACING_GENEROSITY: 9, where 1 is compact and 10 is breathable
- ANALYSIS_PRECISION: 10, where 1 is broad vibe only and 10 is deep extraction

Reading the request:

- "clean" lowers density and raises clarity
- "crazy creative" raises variance and art direction
- "premium SaaS" keeps clarity high and art direction controlled
- "editorial" allows stronger type and more asymmetry

## 3. Image generation discipline

One section is one primary image. A complex section gets a primary image plus one or more detail
images. An unclear section gets regenerated as a fresh standalone image.

**Generate enough images.** If the user asks for four sections, generate four images. Eight sections,
eight images. It is better to generate too many clear images than too few compressed ones, and better
to generate one clear image per section than one unreadable board for the whole site. If more images
would improve text readability, typography extraction, spacing analysis, component inspection, color
extraction, or implementation fidelity, generate more. Never reduce image count for convenience.

**Do not crop earlier images.** When a section needs a dedicated or closer view, generate a fresh
image for it. Do not crop the hero out of a full-page board or slice cards out of a multi-section
composition. Cropping destroys spacing accuracy, type scale relationships, margins, layout
proportions, and button clarity.

**Regeneration preserves the design, improves the read.** A regenerated section keeps the same
palette, typography mood, button style, radius logic, and image treatment, but makes text larger,
spacing more visible, and structure easier to analyze. It is a cleaner render of the same system, not
a different design.

**Media inside the design** should sit in controlled, repeatable frames: fixed aspect blocks,
consistent radius logic, stable proportions across similar modules. Avoid random image sizes with no
system.

## 4. Analyze the reference as a specification

Do not glance. Do not do vibe-only analysis. Do not jump from image to code.

For each section image, establish what the section is, what the visual priority is, and what is still
unclear. If something is unclear, resolve it with another image before coding.

Extract deliberately:

| Dimension | What to pull out |
|---|---|
| **Text** | Hero headline, subheadline, CTA labels, section headings, feature names, navbar and footer labels. Visible text is part of the design and should drive implementation. If it is too small to read, generate a closer image rather than inventing copy. |
| **Typography** | Size and weight relationships, line count, line height feel, tracking, serif versus sans behavior, display versus body contrast, whether the type is calm or aggressive. Do not flatten this into a generic coded hierarchy. |
| **Spacing** | Headline to subheadline, text to buttons, card gaps, section top and bottom, gutters, card padding, image to text. The goal is faithful spacing logic, not pixel OCR. Do not compress generous spacing into a tight default. |
| **Components** | Button size, shape, radius, fill versus outline, icon usage, primary versus secondary hierarchy, card structure, dividers, shadows, borders, input styling. |
| **Color** | Background, panel colors, accents, button fills, text hierarchy, border logic, shadow mood, image grade, gradient restraint. Preserve the palette rather than substituting default web colors. |
| **Structure** | Grid logic, section ordering, density, visual rhythm, repeated motifs that define the language. |

The goal is to understand exactly why the reference looks strong before you build it.

## 5. Composition rules

These apply whether you generated the reference or received it.

**The hero.** It is an opening scene. Keep it clean. Headline stays within one to three lines, one
being best. If the headline runs long, cut words rather than adding lines. One strong focal point, not
several competing ones. Keep the first screen readable and unfilled on a small laptop, showing a clear
headline, readable supporting text, clean spacing, a visible CTA, and one balanced visual focal point.

**Containers.** Do not default to box in box in box. Use a container only when it has a purpose.
Prefer open layouts, clearer whitespace, fewer but stronger containers, and one primary framing move
rather than many layered frames.

**Micro-UI.** Cut anything that does not improve clarity: unnecessary pills, pseudo-system markers,
fake control labels, decorative code-like tags, meaningless metadata rows, filler chips, tiny badges.
Prefer cleaner headings, fewer labels, real hierarchy, stronger typography.

**Everything else** the design must avoid lives in the shared list at
`../design-taste-frontend/references/ai-tells.md`. Read it. It is canonical for this pack and covers
typography, color, layout, motion, icons, copy, density, and visual effects. Do not restate it here.

## 6. Choosing a coherent direction

To avoid repetitive output, pick one combination and commit to it. Do not mash everything together.

**Theme:** pristine light, deep dark, bold studio solid, or quiet premium neutral.

**Background:** subtle technical grid or dotted field, solid field with soft ambient depth, full-bleed
cinematic imagery, or tactile textured surface.

**Typography character:** clean grotesk, refined grotesk, expressive display, compressed statement,
editorial serif plus sans, or Swiss rational hierarchy.

**Hero architecture:** cinematic centered minimalist, asymmetric split, floating scatter, inline
typography behemoth, editorial offset, or image-first with restrained text.

**Section system:** modular bento rhythm, alternating editorial blocks, poster-like stacked
storytelling, gallery-led cadence, Swiss grid discipline, or asymmetric marketing flow.

**Signature components, pick four:** diagonal staggered masonry, cascading card deck, hover-accordion
slice, gapless bento grid, brand marquee strip, turning arc, vertical rhythm lines, off-grid editorial
layout, product UI panel stack, split testimonial wall, layered crop frames.

**Motion language, pick two:** scrubbing text reveal, pinned narrative section, staggered float-up,
parallax drift, smooth accordion expansion, cinematic fade-through.

These are visual direction cues that the design should imply, not coding instructions.

## 7. Default section packs

When the user does not specify, these are reasonable starting structures.

**Four sections:** hero, feature or value block, social proof, closing CTA.

**Eight sections:** hero, logo strip, primary feature, secondary feature, product visual, testimonial,
pricing or plan, closing CTA.

**Twelve sections:** hero, logo strip, problem framing, primary feature, secondary feature, tertiary
feature, product visual, integration or ecosystem, testimonial wall, pricing, FAQ, closing CTA.

Propose the structure before generating, so the user can correct it cheaply.

## 8. Implement without drifting

The common failure is drift: the reference looks strong and the coded result comes out generic.

Follow the reference closely. Preserve layout logic, spacing rhythm, section ordering, text and image
balance, typography mood, component style. Do not simplify into a default template, do not replace
distinctive sections with generic rows, do not compress generous spacing, do not reintroduce nested
containers that analysis removed.

The target is not "inspired by the reference". The target is visually faithful to it, translated into
real frontend.

Where the reference leaves something ambiguous, resolve in this order: preserve the visible design
language, then layout and spacing logic, then component family, then mood and polish level. Generate
an extra detail image if one would settle it. Only then pick the most implementation-friendly faithful
option. Do not fill ambiguity with generic defaults quickly.

When multiple images inform one build, they must read as one design world: same palette, same type
mood, same component family, same radius and shadow logic.

## 9. Clarity check before you ship

Ask directly:

- Would a developer who only saw the reference build roughly this?
- Is the hero readable and uncrowded on a small laptop?
- Is there exactly one clear focal point above the fold?
- Did the palette, type scale, and spacing survive implementation?
- Did any banned pattern from `ai-tells.md` creep in?
- Does every interactive element have loading, empty, error, and active states?

If any answer is no, fix it before presenting the work.

## 10. How to respond

State which path you are on, image generation available or not, and why. If generating, say how many
images and what each covers before producing them. After analysis, summarize the extracted design
system briefly, palette, type, spacing, components, so the user can correct a misread before it
becomes code. Then implement.

Do not narrate every rule in this file back to the user. Apply them.
