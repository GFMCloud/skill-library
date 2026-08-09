# Design Spec - [Deck Name]

This spec records only what varies for this deck. The visual system itself is brand-locked and constant - see the deck-scaffolding-builder design-system.md reference and the project's own brand kit or design tokens skill/file, if one exists, for the standard. If no such source exists, use neutral accessible defaults and say so. Do not redefine palette, type, or chrome here; point at the standard and record the per-deck choices.

## Fonts (locked)

- Deck font: **[Deck Font]** (SemiBold headlines, Medium subheads, Regular body) - embeds in the PPTX. Pull the actual name from the project's design system; if none exists, a neutral default sans-serif is fine - say so.
- If the project has a separate brand body/web font, that is not the deck font. Arial is the MS Office fallback.

## Mode assignment

Default: openers and statement slides run dark; detail and framework slides run light.

| Section | Slide | Mode | Notes |
|---|---|---|---|
| [N] | [N.N] | [light/dark] | [why] |

## Section accent assignments

One highlight color per slide. The highlight token is reserved for the single most important element per slide. The accent token does workhorse accenting.

| Section | Accent treatment |
|---|---|
| [N] | [e.g. accent-color eyebrows, highlight-color on the section's one key stat] |

## Layout usage per section

Map each section's slides to the eight standard layouts (A-H). This tells the Claude Design build exactly what to construct.

| Section | Slides → layouts |
|---|---|
| [N] | [e.g. N.1 → A (statement), N.2 → B (4 cards), N.3 → D (numbered list)] |

## Chrome

Standard chrome on every slide (primary-color top bar, logo top corner, primary-dark footer, highlight-color accent line). No per-deck variation unless noted here: [none / exceptions].

## Anything non-standard for this deck

[Record any deliberate deviation from the standard system and the reason. Default: none.]
