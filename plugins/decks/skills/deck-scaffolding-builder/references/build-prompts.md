# Build Prompts

Reusable prompts that carry a blueprint into Claude Design and then into a native PPTX via cd-to-pptx. Produce these only when "Claude Design build prompts" is selected as the handoff. Parameterize the bracketed parts from the blueprint, including the brand values - pull them from the project's own design tokens or brand kit if one exists, otherwise use the neutral defaults below and say so.

These are not the visual build itself - they're the instructions the user pastes into Claude Design. Keep them tight and reference the design system rather than re-describing it each time.

## Prompt A - master / opener-section builder (Claude Design)

Run once to establish the visual contract every later section inherits.

> Build Section 1 of the [Deck Name] - [X] slides - as a deck-stage presentation. This is the visual contract; every later section inherits these layouts. Slides: [list each slide with number, name, and type - e.g. 1.1 opener (headline), 1.2 three-column comparison (headline)]. Chrome on every slide: thin [Primary Color] top bar, logo top-left, [Primary-Dark Color] footer, [Highlight Color] accent line above footer. Font: [Deck Font] - SemiBold headlines, Medium subheads, Regular body. Colors: [Primary], [Accent], [Highlight], [Primary-Dark] (pull hex values from the project's brand kit/tokens; if none exists, use neutral accessible defaults and say so). Copy is in the attached blueprint - use it as written, don't rewrite it. [Attach blueprint.]

## Prompt B - parameterized section builder (Claude Design)

Reuse per section. Change only the bracketed parts.

> Build Section [N] of the [Deck Name] - [Section Name], [X] slides - into this same deck. Slides and types: [list from blueprint with layout letters]. Match the chrome, type hierarchy, card styling, and layout patterns from Section 1 exactly - do not introduce new layout patterns. Every slide is either a headline slide or a depth slide. The only new thing is content. Copy is in the attached blueprint, used as written. [Attach blueprint + reference Section 1.]

## Prompt C - cd-to-pptx conversion run (Cowork)

Run once after all sections are approved and exported.

> Convert the Claude Design deck export in [export folder] to a native PPTX using the cd-to-pptx skill. Design system (deck font TTFs + logos) is in [design_system folder]. Output to [output folder]. Chart handling - embed as PNG for slides [PNG list]. Leave native labeled placeholders for slides [placeholder list]. QA against the exported PDF and give me the punch list plus the placeholder list when done.

## Prompt D - re-layout one slide from a reference (Claude Design)

Use to change one slide's internal layout to match a screenshot while keeping chrome, spacing, type, and branding consistent. Two steps - duplicate first (fallback), then re-layout the copy.

Step 1 - duplicate:
> Duplicate slide [X.X] and leave the original exactly as is - do not edit or delete it. Make all changes on the copy only.

Step 2 - re-layout the copy:
> Make changes to slide [X.X Copy] only - leave the original untouched. Restructure the body to match the layout in the attached screenshot. This is a re-layout, not a re-style.
> LOCKED - match the rest of the deck exactly: chrome ([Primary Color] top bar, logo, [Primary-Dark] footer, [Highlight Color] accent line); spacing and margins; type ([Deck Font], same scale and weights); color (only brand tokens); card component (same fill, border, radius, left accent bar, padding). This stays a [headline / depth] slide.
> USE THE SCREENSHOT FOR LAYOUT ONLY: arrangement and count of elements - how many cards, the grid, where the visual sits.
> IGNORE FROM THE SCREENSHOT: its fonts, colors, shadows, borders, spacing. Re-skin every element into our design system. The screenshot tells you where things go, not how they look.

Batch variant: duplicate all target slides first (one prompt), then edit each copy one at a time using Step 2. The copies exist up front as a fallback set; a bad result never touches an original.

Tip: before a big restructure, export the deck once as a checkpoint. The duplicated slide is the quick undo; the export is the insurance.
