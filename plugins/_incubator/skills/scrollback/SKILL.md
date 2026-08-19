---
name: scrollback
description: >-
  Build any surface in Scrollback (SB-01), the monospace terminal-instrument
  design system: seven color tokens, the dashed ASCII frame, and fourteen
  specified components. Load BEFORE writing the first line of markup or CSS for
  a Scrollback page, doc site, dashboard, invoice, slide, OG card or CLI output.
  Use on "Scrollback", "SB-01", "terminal spec", "the dashed frame system",
  "build this in our mono system", "make it look like the brand guide", or any
  request to restyle something into the terminal/monospace house style. Owns
  chart and data marks inside a Scrollback surface (one accent, no legend, no
  second series colour); see references/rulings.md for precedence against
  dataviz and visualize.
metadata:
  maturity: incubator
---

# Scrollback SB-01

A monospace design system for surfaces that report on machines. The thesis:
**the page is a terminal buffer that happens to be typeset well.** Everything is
monospace, everything sits on an 8px grid, the only chrome is drawn from
characters a terminal can print, and one accent colour is spent on three things.

Scrollback is instrumentation, not a website. It reports; it does not persuade.

## Step 0: fit test

Build in Scrollback when the surface **reports state or fact**: docs, specs,
dashboards, invoices, receipts, logs, changelogs, status pages, CLI output,
internal tools, technical marketing.

Do not use it for consumer marketing, editorial storytelling, anything needing
photography or illustration, or a brand that already has its own system. Say so
and route elsewhere (`frontend-design`, `minimalist-ui`) rather than bending
Scrollback into a look it refuses.

## Step 1: start from the stylesheet, never from memory

[references/scrollback.css](references/scrollback.css) is the **normative
source** and the single editable home of the system's CSS. Do not retype tokens
from this document, and do not invent values.

- **Self-contained page** (Artifact, single HTML file, email preview): inline the
  whole file inside `<style>`. It is ~14KB.
- **Project with a build**: copy it in as a real stylesheet and link it.
- Either way the copy is **generated output**. A fix goes in
  `references/scrollback.css` first, then propagates.

Start from [templates/starter.html](templates/starter.html), which already wires
the font link, the stylesheet and one frame.

The Claude Code browser pane serves local files as `data:` URLs, so a relative
`<link rel="stylesheet">` does not resolve there. Inline the CSS before
previewing, or you will verify an unstyled page and think the template is
broken.

## Step 2: the non-negotiables

These are the rules that, broken, stop the page reading as Scrollback. Everything
else is detail.

| | Rule |
|---|---|
| Type | One monospace family, every role. Weight **400 everywhere**. No italics. No proportional face, ever, including logos and headlines. |
| Emphasis | Carried by `--bright`, never by bold and never by size. |
| Radius | **0**, everywhere, no exception. Rounded chrome is the fastest way to make this look like a template. |
| Accent | Three uses, listed below. A fourth turns the page into a website. |
| Grid | Every gap a multiple of 8px. Values off the scale are bugs, not judgement. |
| Frames | One idea per frame. Frames never nest. |
| Numbers | `font-variant-numeric: tabular-nums` globally; columns align on the decimal. |
| Emptiness | Content occupies roughly the middle third. Do not fill the rest. |
| Motion | 120ms linear on colour and border-colour, and nothing else. |

## Step 3: spend the accent budget deliberately

`--accent` (`#2E8EFF`) appears in exactly three places:

1. The bracketed frame title.
2. Data marks: bar fills, sparkline endpoint, spec-diagram corner brackets.
3. The keyboard focus indicator.

It is **never** a link colour, a button fill, a border, a hover state, a
highlight, or syntax highlighting. Links carry brightness instead: `--bright`
text with a dashed `--rule` underline that goes solid on hover.

The interaction model is the brightness ramp. `--rule` → `--muted` → `--text` →
`--bright` is a four-step ladder, and nearly every state change in this system is
a move of one step along it.

## Step 4: build from the component catalog

[references/components.md](references/components.md) carries markup and rules for
all fourteen patterns:

`data table` · `flow` · `spec diagram` · `document` · `chart` · `status pill` ·
`log stream` · `command block` · `spec sheet` · `meter` · `sparkline` · `note` ·
`tree` · `field and button`

Use a listed pattern before inventing one. If nothing fits, the new pattern must
answer three questions before it ships: which brightness step carries its
emphasis, what it does at 375px, and what a screen reader gets. Record it in
[references/rulings.md](references/rulings.md).

## Step 5: verify with executed evidence

A Scrollback page is not done because it looks done. Run both checks and paste
the output.

**Palette.** Any new or altered colour:

```bash
python3 templates/verify.py
```

It computes WCAG ratios for the whole palette against both grounds, asserts the
floors, and fails on a token that was eyeballed rather than measured.

**Render.** Open the page and confirm, in this order:

- [ ] No horizontal page scroll at **1280px and 375px**. Wide content scrolls
      inside its own `overflow-x:auto` container, never the body.
- [ ] Every component renders. The three bugs this system produces most often:
      a `%` width on an inline `span` (silently 0), a multi-line block without
      `white-space:pre` (newlines collapse), and a `nowrap` value overflowing the
      viewport on mobile.
- [ ] Token names and other unbreakable strings do not wrap mid-name (`.nw`).
- [ ] Focus is visible on every interactive element and clears the dashed chrome.
- [ ] Charts and marks carry `role="img"` and an `aria-label` stating shape,
      range and endpoint.

Below-fold screenshots in the Claude Code browser pane come back black. Verify
below the fold with DOM geometry and text reads, or hoist the section to the top
of the viewport, and say which parts had visual proof.

## Voice

The system reports. If a sentence exists to make the reader feel something, cut
it.

- Sentence case everywhere; uppercase only for frame titles, eyebrows and pills.
- Labels are plain nouns: `Tokens`, `Tool calls`, `Due`.
- Units live with the number: `16m`, `€21.04`, `112 seats`.
- Approximation is marked, not hidden: `~50m`.
- Errors state what happened and what to do. No apology, no exclamation mark.
- A control says what happens, then the confirmation says it happened: "Issue",
  then "Issued".

## Do not

Gradients, shadows, glows, blurs, glass. A second accent. Rounded anything.
Icons or emoji (the glyph set is `+ - | [ ] ▸ ◂ · ├ │ └ ─` and nothing else).
Pure `#FFFFFF` or `#000000`. Bold standing in for `--bright`. Full-bleed content.

And the genre clichés, refused by name because a contributor will otherwise add
them as a helpful improvement: phosphor green, CRT scanlines, text glow, blinking
cursors, typewriter reveals, ASCII-art wordmarks, inverse-video emphasis in
running text.

## Precedence

- The **user's own words** win over this skill.
- A **project's existing system** wins over this skill unless the project *is*
  Scrollback.
- Inside a Scrollback surface, **this skill owns chart and data-mark styling**
  (one accent, no legend, no second series colour). That is a deliberate
  exception to the global "dataviz owns every chart" rule, and the reasoning plus
  the parts of `dataviz` that still apply are in
  [references/rulings.md](references/rulings.md). Read it before styling a chart.
- `artifact-design` fundamentals still apply: real content, no page-level
  horizontal scroll, visible focus, `prefers-reduced-motion` honoured. Its
  advice to design both themes does **not**: Scrollback is a deliberate
  single-theme system with a print-only paper inversion.

## Output contract

The token names are an API. Downstream pages, CLI themes and generated documents
bind to them.

**v1.0** exports: `--canvas --surface --rule --muted --text --bright --accent`
(core), `--rule-dim --signal-warn --signal-fail` (extensions), `--mono --u
--measure` (layout).

Renaming or removing an exported token is a breaking change: bump the major,
amend [references/rulings.md](references/rulings.md), and sweep every consumer.
Adding a token requires a declared scope; core stays at seven.

## Files

- [references/scrollback.css](references/scrollback.css): normative stylesheet
- [references/components.md](references/components.md): the fourteen patterns
- [references/rulings.md](references/rulings.md): palette table, amendments,
  errata, precedence reasoning
- [templates/starter.html](templates/starter.html): minimal page scaffold
- [templates/verify.py](templates/verify.py): runnable palette check
