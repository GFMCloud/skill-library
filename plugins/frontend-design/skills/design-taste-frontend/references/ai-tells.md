# AI Tells: the shared banned-pattern list

Canonical list for the frontend-design pack. `design-taste-frontend`, `redesign-existing-projects`,
`minimalist-ui` and `image-taste-frontend` all defer to this file rather than restating it.

If a pattern below needs to change, change it here. Do not copy it back into a SKILL.md.

The production-test sections (hero, section numbering, separators, fake previews, marketing copy,
pills, decoration strips, lists, locale strips) came out of real LLM-generated landing-page tests
in upstream `Leonxlnx/taste-skill` v2 §9.F (commit `ccbc15639c97057cbfcf32ecebc38ef716e4bb37`).
They are the signatures the model defaults to when it tries to "look designed". Treat every entry
as a hard ban unless the brief explicitly calls for it.

## Typography tells

- Reaching for Inter or Roboto on premium or creative work. Prefer Geist, Outfit, Cabinet Grotesk,
  Satoshi, Clash Display, PP Editorial New, or Plus Jakarta Sans. Inter is acceptable only when the
  user asks for a neutral, standard, or Linear-style feel, or on public-sector and
  accessibility-first sites.
- "Creative brief, therefore serif." Fraunces and Instrument Serif are the two LLM-favorite display
  serifs and are banned as defaults. A serif needs the brand brief to name one, or a genuinely
  editorial, luxury, publication, or heritage aesthetic with an articulated reason.
- A random serif word injected into a sans headline (or the reverse) for visual interest.
  Emphasis is italic or bold of the same family.
- Serif fonts on dashboard and software UI. Technical UI uses high-end sans pairings such as Geist
  plus Geist Mono, or Satoshi plus JetBrains Mono.
- No giant heading paired with weak tiny subcopy; oversized H1s that scream. Hierarchy comes from
  weight and color, not raw scale.
- No more than two font moods in one design.
- No lazy all-caps everywhere.
- No gradient headline tricks; no gradient text as a shortcut for "premium".
- Body copy caps at roughly 65 characters per line.
- Headlines broken with `<br>` and italicized halves ("for thirty<br>*years.*") as a default move.
- Vertically rotated text ("INDEX OF WORK, 2018 - 2026" at 90 degrees). Agency-portfolio cliché.

## Color and gradient tells

- The AI purple and blue aesthetic as a default: purple button glows, neon gradients, random
  mesh orbs. When the brand or brief explicitly asks for purple, embrace it with a consistent
  palette and restrained gradients.
- More than one accent color, or saturation over 80 percent, without a reason.
- Mixing warm and cool grays inside one project.
- Replacing a designed palette with generic default web colors.
- The premium-consumer default palette (warm cream backgrounds such as `#f5f1ea`, brass, clay,
  oxblood, or ochre accents such as `#b08947`, espresso text such as `#1a1714`) reached for because
  the brief is cookware, wellness, artisan, or luxury. Acceptable only when the brand names those
  colors or is genuinely vintage or warm-craft with an articulated reason.
- Pure `#000000` and pure `#ffffff` surfaces. Off-black and off-white keep depth.
- Oversaturated accents that do not blend with the neutrals.
- Neon or outer glows by default. Use inner borders or subtle tinted shadows.
- Gradient slop: rainbow or mesh-blob gradients, purple-to-blue "AI" defaults, pink-to-orange
  "creator" defaults, neon edges and glow halos with no purpose, gradients that compete with
  imagery instead of supporting it.
- The gradient allow-list, so gradients are not banned outright: low-chroma palette-matched tonal
  gradients (ink to graphite, cream to sand, ivory to warm grey), single-hue atmospheric grades
  behind hero photography, soft vignettes and radial depth that direct the eye, noise-textured
  gradients that add tactile depth without color noise, editorial color washes that match the
  brand mood. Use these confidently.

## Layout and spacing tells

- Centered hero over a dark mesh gradient as the default opening.
- Cards inside cards inside cards; a giant rounded wrapper section containing more bordered panels.
- Dashboard-style compartment stacking without a reason; generic card containers at visual density
  above 7. Group with `border-t`, `divide-y`, or negative space instead.
- Three equal feature cards in a row, repeated section after section. Use a two-column zig-zag, an
  asymmetric grid, a scroll-pinned section, or a horizontal-scroll alternative.
- Cloned left-text / right-image blocks down the whole page.
- The split header: a giant left-aligned headline with a small explainer paragraph floating in the
  top-right corner of the same section header, aligned to nothing. Put the sub-text under the
  headline or build a real two-column header.
- Using `h-screen` for full-height sections. Use `min-h-[100dvh]`, which avoids layout jump on
  iOS Safari.
- Flexbox percentage math such as `w-[calc(33%-1rem)]` where CSS Grid belongs.
- Page layouts that are not contained (`max-w-[1400px] mx-auto` or `max-w-7xl`).
- Mathematically inconsistent padding and margins; floating elements with awkward gaps.
- Crosshair or hairline grid lines drawn only to make the page "feel designed". Lines organize
  real content or they do not exist.

## Responsive tells

- Touch targets under 44px, body text under 1rem, horizontal overflow on mobile, and section gaps
  that do not scale down (use `clamp()`). Any of these is a critical failure, not a polish item.

## Motion tells

- Animating anything other than transform and opacity.
- Decorative motion that does not serve hierarchy, storytelling, feedback, or a state transition.
- An infinite loop on every card because the dial is high.
- Two or more marquees on one page.
- Custom mouse cursors. Outdated, accessibility-hostile, perf-hostile.

## Icon and symbol tells

- Emojis in code, markup, text content, or alt text, unless the user explicitly asked for a
  playful, chat-style, or social-native vibe (and then sparingly, with intent).
- Hand-rolled SVG icon paths. Use `@phosphor-icons/react`, `hugeicons-react`,
  `@radix-ui/react-icons`, or `@tabler/icons-react`; Lucide only on explicit request or when the
  project already depends on it. One family per project, stroke width standardized at 1.5 or 2.0.

## Hero and top-of-page tells

- Version labels as hero eyebrows: `V0.6`, `v2.0`, `BETA`, `INVITE-ONLY PREVIEW`, `EARLY ACCESS`,
  `ALPHA`. Acceptable only when the brief is explicitly about a launch or preview status.
- "Brand · No. 01"-style sub-eyebrows ("Marrow · No. 01 · The 6-quart" micro-meta lines).
- Trust logo walls, tagline micro-strips, pricing teasers, feature bullet lists, or social-proof
  avatar rows stuffed into the hero. All of those belong in dedicated sections directly below it.
- A decoration text strip across the bottom of the hero: `BRAND. MOTION. SPATIAL.`,
  `TYPE / FORM / MOTION`, `DESIGN · BUILD · SHIP`, `ESTD. 2018 · LISBON`. Acceptable only when the
  strip carries real navigable links or real status information.
- Text plus a gradient blob presented as a hero. That is a placeholder, not a hero.

## Section numbering and micro-label tells

- Section-number eyebrows: `00 / INDEX`, `001 · Capabilities`, `002 · Featured commission`,
  `06 · how it works`, `05 · The honest table`, `SECTION 01`, `ABOUT US`. Eyebrows name the topic in
  plain language, or do not exist.
- `01 / 4`-style pagination on images or bento tiles. If the user can count, they do not need it.
- `Scroll · 001 Capabilities`-style scroll cues with a section-number prefix.
- "Index of Work, 2018 - 2026"-style range labels as eyebrows.
- Generic step labels: "Stage 1 / Stage 2 / Stage 3", "Step 1 / Step 2", "Phase 01 / Phase 02",
  "Pass One / Pass Two". The step content is the label: "Install", "Configure", "Ship".
- Micro-meta sentences under eyebrows ("Each of these is a feature we ship today, not a roadmap
  promise. The list will stay short on purpose."). Eyebrow, headline, body is enough.

## Separator and dot tells

- The middle dot (`·`) as the default separator for everything ("foo · bar · baz · qux"). Maximum
  one per line in metadata strips; otherwise prefer line breaks, hairlines, or columns.
- Decorative colored status dots before nav items, list rows, badges, or status labels. Zero by
  default. Acceptable only when the dot conveys real semantic state (a live server status, an
  availability flag), limited to one per page section.

## Em dash and typographic flourish tells

- The em dash (U+2014) anywhere in rendered copy: headlines, eyebrows, pills, body, quotes,
  attribution, captions, button text, alt text. Zero. It is the LLM's signature stylistic crutch
  and the most-violated tell in production tests. Restructure with a period, a comma, a colon, or
  parentheses; in attribution use a line break or a spaced hyphen. "Use sparingly" has never
  worked; the rule is binary.
- The en dash stays legitimate for date and number ranges (`2018–2026`, `€40–80k`); that is correct
  typography, not a tell. Do not use it as a sentence separator either.
- Kinetic em-dash flourishes, em-dash bullets, and long-pause dashes inside quote text.

## Fake product preview tells

- Div-based fake product UI in the hero: a fake task list, a fake terminal, a fake dashboard built
  from styled rectangles. The number one LLM design tell. Use a real screenshot, a generated image,
  a real component preview, or nothing.
- Fake version footers inside fake screenshots ("v0.6.2-rc.1", "last sync 4s ago · main").
- Hand-rolled decorative SVG illustrations, logos, or marks as a default. Acceptable only when the
  brief asks for one, the mark is a single simple geometric shape, and the output quality is
  certain.
- Broken Unsplash links. Use `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`, generated
  photo placeholders, or actual assets.

## Marketing copy tells

- Filler verbs: unleash, elevate, revolutionize, next-gen, seamless, transformative platform.
- Placeholder brand names: Acme, Nexus, Flowbit, Quantumly, NovaCore, SmartFlow, Cloudly. Invent
  contextual names that sound real.
- Placeholder people: John Doe, Jane Doe, Sarah Chan, Jack Su. Use creative, realistic,
  locale-appropriate names. Generic SVG "egg" avatars and Lucide user icons in place of believable
  photo placeholders.
- Fake-perfect numbers (`99.99%`, `50%`, `1234567`) and invented statistics or fake logos presented
  as real. Use organic data (`47.2%`, `+1 (312) 847-1928`) and label mock data as mock.
- "Quietly in use at" and "Quietly trusted by" social-proof headers. Use "Trusted by", "Used at",
  "Customers include", or let the logos speak.
- Poetic section labels: "From the field", "Field notes", "Currently on the bench", "On our desks",
  "Loose plates". Performative-craftsman. Use "Testimonials", "Latest writing", "Now working on", or
  no label.
- Mock-humble industry references in body copy ("We respect the French ones").
- Pseudo-enterprise jargon as decoration: fake control labels, decorative system markers, filler
  status microcopy, invented runtime or orchestration terminology, strings like
  "00 orchestration layer".
- Quote attribution by first name only ("- Sarah") and straight ASCII quote marks where typographic
  quotes or none belong.

## Pill, label, and version stamp tells

- Pills, labels, or tags overlaid on images (`Brand · 02`, `PLATE · BRAND`, `Field notes - journal`).
  Let the image speak or caption it directly below, outside the frame.
- Photo-credit captions as decoration under stock or picsum images (`Field study no. 12 · Ines
  Caetano`, `Plate 03 · House archive`, `Frame XII · 35mm`). A credit is allowed only for a real
  photographer on a real photo. Otherwise a one-line functional caption or none.
- Version footers on marketing pages (`v1.4.2`, `Build 0048`, `last sync 4s ago · main`). Those are
  CLI and devtool fixtures.
- "Reservation 412 of 800"-style live-stock counters as decoration. Only for a real limited-run
  waitlist with real data.
- Industry or category labels printed below logos in a logo wall (`Vercel` plus `hosting`). The
  logo is the credibility; the label adds nothing.
- Arbitrary floating stamp or badge icons on hero text.

## List, divider, and scoring tells

- `border-t` plus `border-b` on every row of a long list or spec table; a ten-row spec sheet with a
  hairline under every row. Pick one border direction, use it sparsely, or move to a card-per-item,
  grouped-chunk, or scroll-snap layout.
- Scoring or progress bars with filled background tracks as comparison visuals on a landing page.
  Prefer a number plus a small icon, or a tiny inline bar with no track.
- A default `<ul>` with `divide-y` rows for more than five items.

## Locale, time, and scroll cue tells

- Locale, city-name, time, or weather strips ("Lisbon, working with founders", "LIS 14:23 · 18°C",
  "1200-690 Lisbon, Portugal" in the footer). Allowed only for a genuinely distributed studio, a
  travel brand, or a real physical venue. One contact address in the footer is fine; an atmospheric
  locale strip is not.
- Scroll cues: `Scroll`, `↓ scroll`, `Scroll to explore`, animated mouse-wheel icons. The user is
  looking at the hero; they know what scrolling is.

## Density tells

- Over-packed sections or card overload; walls of content; tiny spacing between major sections.
- Data-dump sections on a marketing page: a 20-row publication table, a 30-row award list, a giant
  pricing matrix.
- Decorative empty space with no purpose is also a failure, not restraint.

## Visual effect tells

- Floating blobs, stacked glassmorphism without reason, glowing edges everywhere.
- Over-rendered noise that hides the layout.
- Random futuristic detail with no underlying structure.
- shadcn/ui shipped in its generic default state. Customize radii, colors, shadows, and typography.

## Interaction completeness

Any interface that loads or submits data implements the full cycle: loading state with skeletal
loaders matching final layout size, empty state that shows how to populate it, inline error state,
and tactile active feedback such as `-translate-y-[1px]` or `scale-[0.98]`.
