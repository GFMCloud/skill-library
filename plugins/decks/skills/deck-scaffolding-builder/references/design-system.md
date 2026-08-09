# Design System

The visual system is brand-locked and constant across decks. A per-deck design spec records only what varies (mode mix, section accents, layout choices). **Exact brand values - hex codes, type scale, logo files, aspect ratios - come from the project's own brand kit or design tokens skill/file if one exists. Load it for those; don't restate them here or in the spec.** If the project has no brand kit, use the neutral defaults below and say plainly that they're a default, not a real brand. This file covers only how the brand applies specifically to decks.

## Font resolution (settle this once, every deck)

Decks often have a documented conflict between a "deck font" and a "brand/web font." Resolve it the same way every time, using whatever the project's own tokens name for each role:

- **The deck font** is the corporate/deck role - it's what embeds in the PPTX and what Claude Design builds with (e.g. SemiBold headlines, Medium subheads, Regular body).
- **The brand body/web font**, if the project has a separate one, is not the deck font - that's for web and documents. Slides built to convert via cd-to-pptx use the deck font because its real TTFs embed reliably.
- Arial is the MS Office fallback.
- If the project defines no fonts at all, default to a neutral, widely-available sans-serif (system UI font, or Arial) and state that assumption in the design spec.

State this in every design spec so it doesn't get re-litigated mid-build.

## Two slide modes

The deck runs on two interchangeable backgrounds sharing one type system, palette, and component set. Any layout works in either mode - only the color mapping flips.

- **Light mode** - white or very light blue-gray background; primary-color headlines; medium-gray body; accent (or highlight) eyebrows; light cards with a colored left accent bar.
- **Dark mode** - primary or deeper primary-dark background; white headlines; muted body; highlight or accent eyebrows; lighter-navy card panels.

**Rule of thumb:** openers, "why this matters," and statement slides run dark. Detail, framework, and explainer slides run light. Mix freely. The per-deck spec records the actual mode assignment per section.

## Accent discipline (the rule that keeps decks from looking busy)

- One highlight color per slide for the accent word in a headline - the accent or the highlight token, not both in the same headline.
- The highlight token is the scarcity color. Reserve it for the single most important number, word, or callout per slide. Don't spread it.
- The accent token does the workhorse accenting - eyebrows, links, left accent bars, icon chips.

These are role names, not fixed hex values - pull the actual colors from the project's own tokens, or use the neutral default palette in `assets/wireframe-template.html` and say so.

## Chrome (the persistent template layer)

Build it once on the master, never per slide. Raw reference screenshots may show clean edges, but the deck template carries chrome uniformly so the deck holds together across sections.

- Thin primary-color top bar across the top edge
- Wordmark or logo with a small highlight-color dot in a top corner (~1.1-1.4" wide; inverted variant on dark slides)
- Primary-dark footer bar across the bottom edge
- Thin highlight-color accent rule just above the footer
- Chrome adapts to mode but stays consistent in placement and weight

## Spacing and grid

Comfortable outer margins (~0.6-0.8"), nothing crowds the edge. Generous whitespace - the deck reads calm, not dense. Consistent card gutters (~0.2-0.3"). The eyebrow+headline top block gets real breathing room. Vertical rhythm: eyebrow tight to headline, headline loose to body.

(The `assets/wireframe-template.html` encodes these as working CSS primitives - reuse them when building a wireframe rather than re-deriving spacing.)
