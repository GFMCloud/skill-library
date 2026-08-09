# Layout Patterns

Every slide is either a **headline slide** (punchy, presenter carries, front of section) or a **depth slide** (self-service, reads without a presenter, back of section). Both draw from the same eight body layouts. Don't invent new layout patterns per deck - map every slide to one of these so the deck stays coherent and converts cleanly.

## The universal top block (every slide)

Every slide opens with: small-caps eyebrow → big headline → 1-3 short intro lines. This anchors the upper-left or full width. Logo sits opposite the eyebrow in the top corner. Keep this consistent across the whole deck.

## The eight body layouts

**A. Eyebrow + headline + intro only** - the top block is the whole slide. Openers and statement slides. Usually dark mode.

**B. Card grid (3 or 4 columns)** - equal-width cards across the slide. Each card = eyebrow label + sub-head + short body + optional small bullets. Cards may carry a numbered chip (01-06) or icon tile. Colored left accent bar on light-mode cards. Used for: control domains, outcomes, pillars, "what it covers."

**C. Two-panel split** - left panel explains, right panel is a contrasting callout (usually a dark navy box with a highlight-color or white header and an example/stat). Used for pricing, commitment spectrum, before/after comparisons.

**D. Numbered list (01-05)** - vertical stack of rows, each led by a large colored numeral and a left accent bar, headline + one explanatory line per row. One row can be emphasized (filled/inverted). Used for layered lists, sequences, frameworks.

**E. Stat callout** - one or two oversized numerals with a tiny label underneath, against a contrasting block. Often inside a split or comparison.

**F. Comparison table / matrix** - simple 2-3 column table, header row in accent fill. Light separators, no heavy gridlines. Used for positioning and before/after.

**G. Light data visual** - minimal on-brand mini-charts: a single horizontal bar pair, a heatmap grid, a left-to-right flow diagram with labeled boxes and arrows. Flat, no 3D, no drop shadows beyond the card's own.

**H. Full-width statement** - big headline dominates, minimal support. The thesis slide. Often dark mode, two-line headline with the second line in a lighter or accent tone.

## Card anatomy (the workhorse component)

- Rounded rectangle, ~8-12px corner radius
- Fill: light mode a very light off-white/blue-gray tint; dark mode a lighter-navy panel
- 1px subtle border, slightly darker than fill
- 3-4px colored left accent bar (accent or highlight token) on light-mode cards
- Generous internal padding - content never touches edges
- Optional top marker: numbered chip or icon tile (~28-36px)
- Internal stack: eyebrow (caps, accent) → sub-head (semibold) → body → optional bullets
- Equal heights across a row even when content length varies

## Mapping slides to layouts

When blueprinting, tag each slide with its layout letter. This makes the design spec and the Claude Design build prompt concrete: "2.4 is a card grid (B), six cards." If a slide's content doesn't map cleanly to one of the eight, that's a signal to simplify the content, not to invent a ninth layout.
