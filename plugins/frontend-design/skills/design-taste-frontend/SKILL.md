---
name: design-taste-frontend
description: >-
  Senior UI/UX Engineer for premium, greenfield frontend builds. Architects digital interfaces overriding default LLM biases: metric-based variance dials, named vibe and layout archetypes, strict component architecture, CSS hardware acceleration, and balanced design engineering. For net-new builds only. If the project already exists and must not be rewritten, use redesign-existing-projects. If the request specifically asks for a minimal, quiet, editorial or document-style look, or names Notion, Linear or Stripe docs as a reference, use minimalist-ui instead, since this skill's archetypes run louder. If the design should be settled visually before implementation, use image-taste-frontend.
metadata:
  maturity: incubator
---

# High-Agency Frontend Skill

<!-- MERGE NOTE: this file absorbs high-end-visual-design (archived 2026-07 after the skill audit).
     Kept design-taste-frontend's dial/config structure as the base since it's more flexible and
     machine-checkable. Folded in high-end-visual-design's named Vibe/Layout Archetypes (Section 4),
     the Double-Bezel component technique, and the Fluid Island nav pattern, since those were the
     genuinely additive pieces not already covered here. Banned-pattern lists were merged into supersets.
     2026-09: merged upstream Leonxlnx/taste-skill v2 (skills/taste-skill/SKILL.md at commit
     ccbc15639c97057cbfcf32ecebc38ef716e4bb37) through the taste-skill-merge harness
     (~/work/taste-skill-merge/docs/decisions.md holds every ratified row). Long material moved to
     references/; the banned-pattern catalogue lives only in references/ai-tells.md. -->

> Landing pages, portfolios, marketing and about pages. Not dashboards, data tables, or multi-step
> product UI (section 14). Every rule below is contextual: read the brief first, then pull only what
> fits. Where a rule has a named override, use it when the brief earns it, not by default.

## 0. BRIEF INFERENCE (read the room before anything else)

Before touching code or dials, infer what the user actually wants. Most LLM design output is bad
because the model jumps to a default aesthetic instead of reading the room.

**Read these signals first:**
1. **Page kind:** landing (SaaS, consumer, agency, event), portfolio (developer, designer, studio), editorial or blog, or a redesign (section 13).
2. **Vibe words** the user used: "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium consumer", "Apple-y", "playful", "serious B2B", "editorial", "glassy", "dark tech".
3. **Reference signals:** URLs linked, screenshots pasted, products named, competitors.
4. **Audience:** a B2B procurement panel, a design-conscious consumer, a recruiter scanning a portfolio. The audience picks the aesthetic, not your taste.
5. **Existing brand assets:** logo, color, type, photography. For redesigns these are starting material, not optional input.
6. **Quiet constraints:** accessibility-first audiences, public-sector, regulated industries, trust-first commerce, kids' products. These OVERRIDE aesthetic preference, including every archetype and dial below.

**Output a one-line design read before generating:** "Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <design system or aesthetic family>." Example: *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities plus Geist plus restrained motion."*

**If the brief is ambiguous, ask exactly one question**, only when the design read genuinely diverges ("Closer to Linear-clean or Awwwards-experimental?"). If you can infer from context, do not ask; declare the read and proceed.

**Anti-default discipline:** the LLM defaults (AI-purple gradients, a centered hero over a dark mesh, three equal feature cards, glass on everything, infinite loops everywhere, Inter plus slate-900) are catalogued in `references/ai-tells.md`. Reach past them deliberately, based on the design read.

## 1. ACTIVE BASELINE CONFIGURATION (the three dials)
* DESIGN_VARIANCE: 8 (1=Perfect Symmetry, 10=Artsy Chaos)
* MOTION_INTENSITY: 6 (1=Static/No movement, 10=Cinematic/Magic Physics)
* VISUAL_DENSITY: 4 (1=Art Gallery/Airy, 10=Pilot Cockpit/Packed Data)

**AI Instruction:** the baseline is `8 / 6 / 4`. Use it unless the design read or the user overrides it; overrides happen conversationally, never by asking the user to edit this file. These values are global variables that drive sections 4 through 9 and 12. Cross-references use these exact names; never invent aliases like `LAYOUT_VARIANCE` or `ANIM_LEVEL`.

**Dial inference from the design read:**

| Signal or use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style"; editorial or blog | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / agency"; creative studio portfolio | 9-10 | 8-10 | 3 |
| Landing page, mainstream SaaS, marketing site (default) | 7-9 | 6-8 | 3-5 |
| Developer portfolio | 6 | 5 | 4 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| Redesign, preserve | match existing | +1 | match existing |
| Redesign, overhaul | +2 | +2 | match existing |

## 2. BRIEF TO DESIGN SYSTEM MAP
After the design read and the dials, pick the foundation. If the brief reads as a product that has an official design system (Fluent, Material 3, Carbon, Polaris, Atlaskit, Primer, GOV.UK Frontend, USWDS, Radix Themes, shadcn/ui, Bootstrap), install and use the **official** package. Do not recreate its CSS by hand, and do not import its tokens and then override most of them. **One system per project.** When the brief is an aesthetic rather than a system (glass, bento, brutalism, editorial, dark tech, kinetic type), build with native CSS plus Tailwind and say so honestly in comments. The mapping tables, install commands, and canonical sources are in `references/design-system-map.md`.

## 3. DEFAULT ARCHITECTURE & CONVENTIONS
Unless the design read picks a real design system or the user specifies a stack, adhere to these:

* **DEPENDENCY VERIFICATION [MANDATORY]:** Before importing ANY 3rd party library (e.g. `motion`, `@phosphor-icons/react`, `zustand`), check `package.json`. If the package is missing, output the installation command before providing the code. **Never** assume a library exists.
* **Framework & Interactivity:** React or Next.js. Default to Server Components (`RSC`).
    * **RSC SAFETY:** Global state works ONLY in Client Components. In Next.js, wrap providers in a `"use client"` component.
    * **INTERACTIVITY ISOLATION:** Any component using Motion, scroll listeners, or pointer physics MUST be an isolated leaf with `'use client'` at the very top. Server Components render static layouts only.
* **Animation library:** Motion, imported from `motion/react` (`import { motion } from "motion/react"`). The `framer-motion` package still works as a legacy alias; prefer `motion/react` in new code. GSAP and Three.js only for the isolated cases in section 7.
* **State Management:** Local `useState`/`useReducer` for isolated UI. Global state (Zustand, Jotai, context) strictly for deep prop-drilling avoidance. **NEVER** use `useState` for continuous values driven by input (mouse position, scroll progress, magnetic hover): it re-renders the tree on every change and collapses on mobile. Use `useMotionValue`, `useTransform`, `useScroll`.
* **Styling Policy:** Tailwind CSS for 90% of styling. v4 by default; v3 only when the existing project demands it.
    * **TAILWIND VERSION LOCK:** Check `package.json` first. Do not use v4 syntax in v3 projects.
    * **T4 CONFIG GUARD:** For v4, do NOT use the `tailwindcss` plugin in `postcss.config.js`. Use `@tailwindcss/postcss` or the Vite plugin.
* **Fonts:** `next/font` on Next.js, otherwise self-host with `@font-face` and `font-display: swap`. Never link Google Fonts via `<link>` in production.
* **Emoji policy:** Discouraged by default in code, markup, and visible text; replace symbols with icon-library glyphs or clean SVG primitives. **Override:** only when the user explicitly asks for a playful, chat-style, or social-native vibe, and even then sparingly, with intent.
* **Icons:** `@phosphor-icons/react` (Light weight for premium contexts), `hugeicons-react`, `@radix-ui/react-icons`, or `@tabler/icons-react`, in that priority order. `lucide-react` only on explicit request or when the project already depends on it. One family per project; standardize `strokeWidth` globally (`1.5` or `2.0`). Never hand-roll icon paths.
* **Responsiveness & Spacing:**
  * Standardize breakpoints (`sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`). Test at 375, 390, 768, 1024, and 1440 before calling a layout done.
  * Contain page layouts using `max-w-[1400px] mx-auto` or `max-w-7xl`.
  * **Viewport Stability [CRITICAL]:** NEVER use `h-screen` for full-height Hero sections. ALWAYS use `min-h-[100dvh]` to prevent layout jumping on mobile browsers (iOS Safari).
  * **Grid over Flex-Math:** NEVER use complex flexbox percentage math (`w-[calc(33%-1rem)]`). ALWAYS use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`).
  * **Mobile floors:** every interactive element is at least a `44px` tap target; body text is never below `1rem`; headlines scale with `clamp()`; vertical section gaps scale proportionally (`clamp(3rem, 8vw, 6rem)`); desktop nav collapses to a clean mobile menu; inline typography images stack below the headline on mobile.
  * **Horizontal-overflow guard:** wrap the page in `<main className="overflow-x-hidden w-full max-w-full">` so off-screen entry animations never create a horizontal scrollbar. Horizontal overflow on mobile is a critical failure.

## 4. VIBE & LAYOUT ARCHETYPE SELECTION
Before writing code, select ONE Vibe Archetype and ONE Layout Archetype from the design read, so output is tailored but always premium. Do not repeat the same combination for two different projects in one conversation.

### A. Vibe & Texture Archetypes (Pick 1)
1. **Ethereal Glass (SaaS / AI / Tech):** Deepest OLED black (`#050505`), subtle radial tonal gradients in the background (palette-matched, not AI-purple orbs). Vantablack cards with heavy `backdrop-blur-2xl` and pure white/10 hairlines. Wide geometric Grotesk typography.
2. **Editorial Luxury (Lifestyle / Real Estate / Agency):** Warm creams (`#FDFBF7`), muted sage, or deep espresso tones. High-contrast Variable Serif for massive headings, justified by the brief per section 5.1. Subtle CSS noise/film-grain overlay (`opacity-[0.03]`) for a physical paper feel.
3. **Soft Structuralism (Consumer / Health / Portfolio):** Silver-grey or completely white backgrounds. Massive bold Grotesk typography. Airy, floating components with highly diffused ambient shadows.

### B. Layout Archetypes (Pick 1)
1. **The Asymmetrical Bento:** A masonry-like CSS Grid of varying card sizes (e.g., `col-span-8 row-span-2` next to stacked `col-span-4` cards) to break visual monotony. Bento rules in section 5.7 apply.
2. **The Z-Axis Cascade:** Elements stacked like physical cards, slightly overlapping with varying depths of field, some with a subtle `-2deg`/`3deg` rotation to break the digital grid.
3. **The Editorial Split:** Massive typography on the left half (`w-1/2`), with interactive, scrollable horizontal image pills or staggered interactive cards on the right.

**Mobile Collapse (applies to all three):** Falls back to a single-column stack (`grid-cols-1`, `w-full`) with generous vertical gaps (`gap-6`), `px-4 py-8`. Remove all rotations and negative-margin overlaps below `768px`; overlapping elements cause touch-target conflicts on mobile.

The archetype sets the flavor; the dials in sections 1 and 9 drive how intensely it is expressed.

## 5. DESIGN ENGINEERING DIRECTIVES (Bias Correction)

> The pack-wide banned-pattern list is canonical at `references/ai-tells.md`. It is shared by
> redesign-existing-projects, minimalist-ui and image-taste-frontend. The rules below are this
> skill's engineering directives and are consistent with it. When a banned pattern changes, change
> it in `ai-tells.md`, not here. Each rule below has a context-aware override path.

### 5.1 Typography
* **Display/Headlines:** Default to `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Body/Paragraphs:** Default to `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
* **Sans choice:** Inter is discouraged as the default. Pick `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, `Clash Display`, or `Plus Jakarta Sans` first. Pairings to know: `Geist` + `Geist Mono`, `Satoshi` + `JetBrains Mono`, `Cabinet Grotesk` + `Inter Tight`, `GT America` + `IBM Plex Mono`. **Override:** Inter is fine when the user asks for a neutral, standard, or Linear-style feel, or on public-sector and accessibility-first sites.
* **SERIF DISCIPLINE:** Serif is discouraged as the default font for any project. "It feels creative / premium / editorial" is NOT a reason. Serif is acceptable only when the brand brief literally names a serif, or the aesthetic family is genuinely editorial, luxury, publication, manuscript, heritage, or vintage AND you can articulate why this specific serif fits this specific brand. Everything else (agency, studio, modern brand, premium consumer, portfolio, lifestyle) defaults to a sans display (Geist Display, ABC Diatype, Söhne Breit, Cabinet Grotesk Display, Migra Sans, GT Walsheim, Inter Display, PP Neue Montreal). Sans display fonts are not "boring"; they are the default for the same reason black is the default in fashion. The two LLM-favorite display serifs are banned as defaults; `ai-tells.md` names them. If a serif is justified, pick from: PP Editorial New, GT Sectra Display, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, Domaine Display, Canela, Schnyder, Tobias, ITC Galliard. Serif is never used on dashboard or software UI.
* **EMPHASIS RULE:** To emphasize a word inside a headline, use italic or bold of the SAME family. Never inject a serif word into a sans headline (or the reverse) for visual interest.
* **ITALIC DESCENDER CLEARANCE [MANDATORY]:** Italic display words containing `y g j p q` clip under `leading-none`. Use `leading-[1.1]` minimum plus a `pb-1` or `mb-1` reserve on the wrapper. Audit every italic display word before shipping.
* **CONTAINER-WIDTH FIX:** A wrapped headline is a container problem before it is a type problem. Give the H1 an ultra-wide container (`max-w-5xl`, `max-w-6xl`, or `w-full`) first; only then reduce scale (`clamp(3rem, 5vw, 5.5rem)`). The H1 never exceeds 3 lines; 4 or more is a failure.

### 5.2 Color Calibration
* **Constraint:** Max 1 Accent Color. Saturation < 80% by default. Neutral bases (Zinc, Slate, Stone) with a singular high-contrast accent (Emerald, Electric Blue, Deep Rose, Burnt Orange).
* **THE LILA RULE:** The "AI Purple / Blue glow" aesthetic is discouraged as a default: no automatic purple button glows, no random neon gradients. **Override:** if the brand or brief explicitly asks for purple, violet, or lila, embrace it and execute with intent: consistent palette, harmonised neutrals, restrained gradients.
* **COLOR CONSISTENCY LOCK [MANDATORY]:** One palette per project; do not fluctuate between warm and cool grays. Once an accent is chosen it is used on the WHOLE page: a warm-grey site does not get a blue CTA in section 7, a rose-accented site does not get a teal badge in the footer. Audit every component before shipping.
* **PREMIUM-CONSUMER PALETTE RULE:** For cookware, wellness, artisan, luxury, heritage-craft, and DTC home-goods briefs, the LLM default is warm cream plus brass, clay, oxblood, or ochre plus espresso text; the hex families are listed in `ai-tells.md`. Do not reach for it because "this is a cookware brief". Rotate through these instead: **Cold Luxury** (silver-grey, chrome, smoke), **Forest** (deep green, bone, amber), **Black and Tan** (true off-black, warm tan, no beige), **Cobalt + Cream**, **Terracotta + Slate**, **Olive + Brick + Paper**, **Pure monochrome + one saturated pop**. **Override:** the beige-and-brass family is acceptable only when the brand names those colors, or the identity is genuinely vintage or warm-craft and you can say why it fits this brand.

### 5.3 Layout Diversification
* **ANTI-CENTER BIAS:** Centered Hero/H1 sections are avoided when `DESIGN_VARIANCE > 4`. Use a section 4 Layout Archetype, a 50/50 split, left-aligned content with a right-aligned asset, asymmetric white space, or a scroll-pinned structure. **Override:** a centered hero is right for editorial, manifesto, and launch-announcement briefs where the message itself is the design.

### 5.4 Materiality, Shadows, and Cards
* **Execution:** Use cards ONLY when elevation communicates real hierarchy. Otherwise group with `border-t`, `divide-y`, or negative space. When a card is warranted, the Double-Bezel treatment in section 6 is the default.
* **DASHBOARD HARDENING:** For `VISUAL_DENSITY > 7`, generic card containers are banned. Data metrics breathe in plain layout.
* When a shadow is used, tint it to the background hue. No pure-black drop shadows on light backgrounds.
* **SHAPE CONSISTENCY LOCK [MANDATORY]:** Pick ONE corner-radius scale per page: all-sharp (0), all-soft (12-16px), or all-pill (full radius for interactive). Mixed systems only with a documented rule ("buttons full-pill, cards 16px, inputs 8px") followed everywhere. Round buttons in a square layout, or square cards on a pill-button page, is broken design.

### 5.5 Interactive UI States
* **Mandatory Generation:** Implement full interaction cycles: Loading (skeletal loaders matching layout sizes, not generic spinners), Empty States (composed, showing how to populate), Error States (clear, inline for forms, toasts only for transient), Tactile Feedback (`:active` uses `-translate-y-[1px]` or `scale-[0.98]`).
* **BUTTON CONTRAST CHECK [MANDATORY, a11y]:** Verify button text is readable against the button background. White button with white text, `bg-white` CTA with `text-white`, a transparent button on the page background with no border: all banned. Ghost buttons over photography get a backdrop, scrim, or stroke. Minimum WCAG AA: 4.5:1 for body-size text, 3:1 for large text, where large means 18pt (about 24px) regular or 14pt (about 18.7px) bold. Card titles and subheads below 24px need 4.5:1.
* **CTA BUTTON WRAP BAN [MANDATORY]:** Button text fits on one line at desktop. Shorten the label (3 words max for primary CTAs, ideally 1-2) or widen the button; never constrain `max-width` on a CTA.
* **NO DUPLICATE CTA INTENT [MANDATORY]:** "Get in touch" + "Contact us" + "Let's talk" are one intent; so are "Try free" + "Get started" + "Sign up free", and "View work" + "See selected work". One label per intent, used identically in nav, hero, and footer.
* **FORM CONTRAST CHECK [MANDATORY, a11y]:** Inputs, placeholder text, focus rings, helper text, and error text all pass WCAG AA against the section background.

### 5.6 Data & Form Patterns
* **Forms:** Label ABOVE input. Helper text optional but present in markup. Error text BELOW input. Standard `gap-2` for input blocks. No placeholder-as-label, ever.

### 5.7 Layout Discipline (hard rules; failing any of these is shipping broken work)
* **Hero MUST fit the initial viewport.** Headline max 2 lines on desktop, subtext max 20 words AND max 3-4 lines, CTAs visible without scroll. If you cannot state the value proposition in 20 words, the proposition is unclear, not the rule too tight.
* **Hero font-scale discipline.** Plan font size and image size together. Default `text-4xl md:text-5xl lg:text-6xl`; `text-6xl md:text-7xl` only for a 3-5 word headline. A 4-line hero headline is a font-size error, never a copy-length error.
* **HERO TOP PADDING CAP [MANDATORY]:** max `pt-24` at desktop. If the hero needs more room, increase font scale or asset size, not top padding.
* **HERO STACK DISCIPLINE (max 4 text elements):** one small label (eyebrow OR brand strip OR neither), headline, subtext, CTAs (1 primary + max 1 secondary). Taglines under CTAs, trust micro-strips, pricing teasers, feature bullets, and avatar rows move to dedicated sections directly below the hero. A "Used by / Trusted by" logo wall lives UNDER the hero, never inside it, and uses real SVG logos (section 5.8).
* **Navigation renders on ONE line at desktop**, height 64-72px, 80px max. Condense labels, drop secondary items, or use a hamburger before wrapping.
* **Bento grids MUST have rhythm and an exact cell count.** N items means N cells (3 items: 1+2 or an asymmetric trio; 5 items: 2+3 or hero+4). Apply Tailwind `grid-flow-dense` (`grid-auto-flow: dense`) on every bento grid and verify that `col-span` and `row-span` values interlock; no empty cell in the middle or at the end. 3-5 intentional cards beat 8 messy ones. At least 2-3 cells carry real visual variation (an image, a palette-matched gradient, a pattern, a tinted background), never six white-on-white text cards.
* **SECTION-LAYOUT-REPETITION BAN:** a layout family (3-column cards, full-width quote, split text-image) appears at most ONCE per page. 8 sections need at least 4 families.
* **ZIGZAG ALTERNATION CAP [MANDATORY]:** max 2 consecutive image-plus-text split sections. The third in a row is a Pre-Flight fail; break it with a full-width section, a vertical stack, a bento, or a marquee.
* **EYEBROW RESTRAINT [MANDATORY, the most-violated rule in production tests]:** An eyebrow is the small uppercase wide-tracking label above a section headline (`text-[11px] uppercase tracking-[0.18em]`). **Maximum 1 eyebrow per 3 sections; the hero counts as 1.** If section A has an eyebrow, the next two cannot. The check is mechanical: count `uppercase tracking` labels above headlines; if the count exceeds ceil(sectionCount / 3), the output fails. What to do instead: drop it. The headline alone is enough; the section's position on the page already categorizes it.
* **SPLIT-HEADER BAN [MANDATORY]:** "left big headline + right small explainer paragraph" as a section header is banned as default. Stack them vertically (headline, then body at max-width 65ch). Split only when the right column carries a visual or interactive element.
* **Mobile collapse is explicit per section.** Every multi-column layout declares its `< 768px` fallback in the same component. No "Tailwind handles it".

### 5.8 Image & Visual Asset Strategy
Landing pages and portfolios are visual products. Text-only pages with fake-screenshot divs are slop.

**Priority order for visual assets:**
1. **Image-generation tool first.** If ANY image-gen tool is available (`generate_image`, an MCP image tool, IDE-integrated generation), use it to create section-specific assets at the right aspect ratio: hero photography, product shots, texture backgrounds, mood images. Do not skip it because hand-rolled CSS feels faster.
2. **Real web images second.** `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` (the seed describes the section, e.g. `marrow-cookware-kitchen`); actual stock or brand URLs from the brief; open-license sources if explicitly allowed.
3. **Last resort: tell the user.** Do NOT fill the page with hand-rolled SVG illustrations or div-based fake screenshots. Leave clearly labeled placeholder slots (`<!-- TODO: hero product photo, 1600x1200 -->`) and end the response with: *"This page needs real images at: [list of placements]. Please generate or provide them."* These placeholder comments are instructed output, not truncation.

* **Even minimalist sites need real images.** A pure-text page is incomplete work, not minimalism. An editorial Linear-style site still needs 2-3 real images (hero, one product or lifestyle shot, one supporting image); generate restrained B&W photography if the brief is quiet.
* **Real company logos for social proof.** Never plain text wordmarks in a row. Use Simple Icons (`https://cdn.simpleicons.org/{slug}/ffffff`, or the `simple-icons` package) or devicon; for an invented brand, generate a simple monogram as an inline `<svg>` matching the page style. Logos render in both light and dark mode. **LOGO-ONLY:** a logo wall is logos and nothing else (brand name as alt text is fine).
* **Hand-rolled decorative SVGs** (illustrations, logos, marks) are strongly discouraged as default: only when the brief asks, the mark is a single simple geometric shape, and you are confident in the quality. Library icons are fine (section 3).
* **Div-based fake screenshots are banned.** To show a product: a real screenshot URL, a generated image, a real component preview (a mini-version of the UI inside the page), or editorial photography instead.
* **The hero needs a real visual.** Text plus a gradient blob is a placeholder, not a hero.

### 5.9 Content Density and Copy
Landing pages live on the first impression, not the full read. Cut ruthlessly.
* **Default content shape per section:** short headline (8 words or fewer), short sub-paragraph (25 words or fewer), one visual asset OR one CTA. More must be justified by the section's job.
* **No data-dump sections.** Top 3-5 highlights plus a "View full list" link; a marquee or carousel for breadth; a different page if the data is the product.
* **Long lists need a different component, not a longer list.** Over 5 items: a 2-column split with grouped items, a card grid with image and label, tabs or an accordion, horizontal scroll-snap pills, a carousel, or a marquee. **Spec sheets** (cookware, hardware, apparel): a 2-column card grid (name, large display value, one-line "why it matters"), scroll-snap pills, 3 grouped clusters with one soft divider each, or 3-4 hero specs as display tiles with the rest under a disclosure. Never a 10-row table with a hairline under every row.
* **COPY SELF-AUDIT [MANDATORY before ship]:** Re-read every visible string (headlines, subheads, eyebrows, buttons, body, captions, alt text, footer, errors). Flag anything grammatically broken ("free on its past"), with unclear referents, that sounds like hallucinated wordplay, or that reads like an LLM trying to sound thoughtful (passive-aggressive humility, fake-craftsman labels, mock-poetic micro-meta). Rewrite every flagged string; when unsure, use a plain functional sentence. Cute AI copy is worse than boring copy.
* **Fake-precise numbers** (`92%`, `4.1×`, `48k`, `5.8 mm`) come from real data, are labeled as mock (`<!-- mock -->`, "sample data"), or do not appear. Do not fake engineering precision the brand does not claim.
* **One copy register per page.** Do not mix technical mono, editorial prose, and marketing punch unless the brand voice calls for it.
* **Em dashes in rendered copy: zero.** Headlines, labels, body, quotes, attribution, captions, buttons, alt text. Restructure with a period, comma, colon, or parentheses. En dashes in date and number ranges are correct typography and stay.

### 5.10 Quotes & Testimonials
* Max 3 lines of quote body; a landing-page quote is a snippet, not the full review (footer-size testimonials may stretch slightly). Attribution is name plus role, optionally company; never name only. Real typographic quote marks or none; no straight ASCII quotes; no dash flourishes inside the quote.

### 5.11 Page Theme Lock
The page has ONE theme. If it is dark, ALL sections are dark; no warm-paper section sandwiched between dark ones. Pick light, dark, or auto (`prefers-color-scheme`) at the page level and lock it; tints within one family (`bg-zinc-950` next to `bg-zinc-900`) are fine, flipping to `bg-amber-50` mid-page is broken. **Override:** a deliberate "Color Block Story" or theme switch on scroll, once per page, with a strong transition, when the brief asks for it. With a themed design system, set the theme once at the root. Dual-mode design is mandatory for consumer-facing pages; the procedure is `references/dark-mode-protocol.md`.

## 6. HAPTIC MICRO-AESTHETICS (COMPONENT MASTERY)

### A. The "Double-Bezel" (Doppelrand / Nested Architecture)
When a card, image frame, or container is warranted (section 5.4), this is the default treatment. It should look like physical, machined hardware (a glass plate sitting in an aluminum tray) using nested enclosures.
- **Outer Shell:** A wrapper `div` with a subtle background (`bg-black/5` or `bg-white/5`), a hairline outer border (`ring-1 ring-black/5` or `border border-white/10`), specific padding (e.g., `p-1.5` or `p-2`), and a large outer radius (`rounded-[2rem]`).
- **Inner Core:** The content container inside the shell, with its own distinct background, its own inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), and a mathematically smaller radius (`rounded-[calc(2rem-0.375rem)]`) for concentric curves.

### B. Nested CTA & "Island" Button Architecture
- **Structure:** Primary interactive buttons are fully rounded pills (`rounded-full`) with generous padding (`px-6 py-3`), when the page's shape lock (section 5.4) is pill or documents pill buttons.
- **The "Button-in-Button" Trailing Icon:** If a button has an arrow (`↗`), nest it inside its own circular wrapper (`w-8 h-8 rounded-full bg-black/5 dark:bg-white/10 flex items-center justify-center`), flush with the main button's right inner padding.

### C. "Liquid Glass" Refraction
Glass is for premium consumer, Apple-adjacent, luxury, and media-overlay briefs, not dashboards or public-sector. When used, go beyond `backdrop-blur`: add a 1px inner border (`border-white/10`) and a subtle inner shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) for physical edge refraction, and a solid-fill fallback under `prefers-reduced-transparency`. The honest full skeleton is `references/liquid-glass.md`.

### D. Spatial Rhythm & Hairlines
- **Macro-Whitespace:** Double your standard padding. `py-24` to `py-40` for sections (up to `py-40` on Ethereal Glass and Editorial Luxury). Let the design breathe.
- **Section labels:** governed by the eyebrow ration in section 5.7. When one is earned, it is a microscopic label (`text-[10px] uppercase tracking-[0.2em] font-medium`) naming the topic in plain words.
- **Hairline dividers:** `display: grid; gap: 1px` with contrasting parent and child backgrounds yields mathematically perfect razor-thin dividers without border declarations. Use it for dense data groups and spec clusters instead of `border-b` on every row.

## 7. MOTION CHOREOGRAPHY
These are tools, not defaults. **Motion must be motivated:** before adding any animation, name what it communicates: hierarchy, storytelling, feedback, or a state transition. "It looked cool" is not an answer; GSAP everywhere because GSAP is available is amateur. If you cannot state the reason in one sentence, drop the animation. Everything above `MOTION_INTENSITY 3` honors reduced motion (section 8).

**Motion claimed, motion shown:** at `MOTION_INTENSITY > 4` the page actually moves: entry transitions on the hero, scroll reveals on key sections, hover physics on CTAs, at minimum. If you cannot ship working motion in scope, drop the dial to 3 and ship a clean static page. Never half-build motion (cut-off ScrollTriggers, jumpy enters, missing cleanups).

**Magnetic Micro-physics (`MOTION_INTENSITY > 5` AND a premium, playful, or agency read):** Buttons pull slightly toward the cursor. Implement EXCLUSIVELY with `useMotionValue`/`useTransform` outside the React render cycle, never `useState`. On hover, scale the button down slightly (`active:scale-[0.98]`), translate the inner icon circle diagonally (`group-hover:translate-x-1 group-hover:-translate-y-[1px]`) and scale it up (`scale-105`) for internal kinetic tension.

**Perpetual Micro-Interactions (`MOTION_INTENSITY > 5` AND the section benefits):** Pulse, Typewriter, Float, Shimmer, Carousel for status indicators, live feeds, and AI-feel surfaces. **Not every card needs an infinite loop.** If a section is informational, leave it still. Spring physics (`type: "spring", stiffness: 100, damping: 20`), no linear easing; where spring is not the mechanism, custom cubic-beziers (`cubic-bezier(0.32,0.72,0,1)`), never default `linear`/`ease-in-out` for anything the user is meant to notice.

**Marquee max one per page.** Two horizontal marquees on one page reads as filler; pick the one section where it serves the content.

**Layout Transitions:** `layout`/`layoutId` for visible state changes (re-ordering, expanding modals, shared elements). Do not wrap static content in `layout` "for safety"; it costs measurement work.

**Staggered Orchestration:** `staggerChildren` (Motion) or a CSS cascade (`animation-delay: calc(var(--index) * 100ms)`) for reveals where sequence matters. Parent `variants` and children MUST live in the same Client Component tree; if data is async, pass it as props into one parent motion wrapper.

**The "Fluid Island" Nav & Hamburger Reveal (default nav pattern):**
- **Closed State:** Navbar is a floating glass pill detached from the top (`mt-6`, `mx-auto`, `w-max`, `rounded-full`), one line, under 80px.
- **The Hamburger Morph:** On click, the hamburger lines fluidly rotate/translate to form a perfect 'X', not just disappear.
- **The Modal Expansion:** Menu opens as a screen-filling overlay with heavy glass (`backdrop-blur-3xl bg-black/80` or `bg-white/80`).
- **Staggered Mask Reveal:** Nav links fade in and slide up (`translate-y-12 opacity-0` to `translate-y-0 opacity-100`) with a staggered delay per item.

**Scroll work:** Entry reveals (`translate-y-16 blur-md opacity-0` resolving over 800ms+) use `whileInView` or `IntersectionObserver`. Pin and scrub work (sticky-stack, horizontal pan) uses GSAP ScrollTrigger with `start: "top top"` and `pin: true`; the canonical skeletons, the failure diagnoses, and the forbidden-pattern list (no `window.addEventListener('scroll')`, no `scrollY` in React state, no `requestAnimationFrame` loops touching state) are in `references/gsap-skeletons.md`. **Never mix GSAP or Three.js with Motion in one component tree:** Motion for UI and bento, GSAP or Three.js only for isolated full-page scrolltelling or canvas backgrounds, wrapped in strict `useEffect` cleanup.

## 8. PERFORMANCE & ACCESSIBILITY GUARDRAILS
* **REDUCED MOTION [MANDATORY]:** Any motion above `MOTION_INTENSITY > 3` honors `prefers-reduced-motion`. In Motion, `useReducedMotion()` and degrade to static; in CSS, gate under `@media (prefers-reduced-motion: no-preference)` or disable under `@media (prefers-reduced-motion: reduce)`. Infinite loops, parallax, scroll hijack, and magnetic physics collapse to static under reduced motion. Non-negotiable.
* **Dark mode:** mandatory for consumer-facing pages, designed for both modes from the start, tokens by one strategy, tested in both before finishing. Procedure: `references/dark-mode-protocol.md`.
* **Hardware Acceleration:** Never animate `top`, `left`, `width`, or `height`. Animate exclusively via `transform` and `opacity`; `will-change: transform` only on elements that actually animate.
* **Core Web Vitals:** LCP < 2.5s (hero image `next/image priority` or preloaded), INP < 200ms (heavy work off the main thread), CLS < 0.1 (reserve space for images, fonts, embeds). Run Lighthouse before declaring a page done. Lazy-load anything not above the fold; Motion is not tiny and Three.js is large.
* **DOM Cost:** Apply grain/noise filters exclusively to fixed, `pointer-events-none` pseudo-elements (`fixed inset-0 z-[60] pointer-events-none`) and NEVER to scrolling containers; continuous GPU repaints destroy mobile FPS.
* **Blur Constraints:** `backdrop-blur` only on fixed/sticky elements (navbars, overlays). Never on scrolling containers or large content areas.
* **Z-Index Restraint:** NEVER spam arbitrary `z-50`/`z-10`/`z-[9999]`. Reserve z-indexes for systemic layer contexts (sticky navbars, modals, overlays, tooltips, grain) and document the scale in a project constants file.

## 9. TECHNICAL REFERENCE (Dial Definitions)

### DESIGN_VARIANCE (Level 1-10)
* **1-3 (Predictable):** Symmetrical 12-column CSS Grid with equal fr-units, equal paddings, centered alignment.
* **4-7 (Offset):** `margin-top: -2rem` overlaps, varied image aspect ratios (4:3 next to 16:9), left-aligned headers over center-aligned data.
* **8-10 (Asymmetric):** Masonry layouts, CSS Grid with fractional units (`grid-template-columns: 2fr 1fr 1fr`), massive empty zones (`padding-left: 20vw`). Pull the structure from the section 4 Layout Archetype.
* **MOBILE OVERRIDE:** For levels 4-10, any asymmetric layout above `md:` MUST collapse to strict single-column (`w-full`, `px-4`, `py-8`) below `768px`.

### MOTION_INTENSITY (Level 1-10)
* **1-3 (Static):** No automatic animations. CSS `:hover`/`:active` only; this is also the reduced-motion mode.
* **4-7 (Fluid CSS):** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. `animation-delay` cascades for load-ins. `transform`/`opacity` only.
* **8-10 (Advanced Choreography):** Scroll-triggered reveals, parallax, scroll-driven animation (CSS `animation-timeline` or GSAP ScrollTrigger) via Motion hooks. `window.addEventListener('scroll')` is a hard ban.

### VISUAL_DENSITY (Level 1-10)
* **1-3 (Art Gallery Mode):** Lots of white space, huge section gaps (`py-32` to `py-48`), expensive and clean.
* **4-7 (Daily App Mode):** Standard web app spacing (`py-16` to `py-24`).
* **8-10 (Cockpit Mode):** Tight paddings, no card boxes, 1px lines separate data, everything packed. **Mandatory:** `font-mono` for all numbers. Dashboards themselves are out of scope (section 14); this band exists for dense marketing surfaces such as spec and pricing sections.

## 10. AI TELLS (Forbidden Patterns)
The catalogue of banned patterns, including the production-test tells (hero version labels, section-number eyebrows, decorative dots, fake product previews, poetic section labels, photo-credit captions, locale strips, scroll cues, and the rest), lives only in `references/ai-tells.md`. Read it before generating and again at pre-flight. This file does not restate it.

## 11. THE CREATIVE ARSENAL (Reference Vocabulary)
A vocabulary, not a library: know these names to design with them and reach for them when the design read calls for it.

**Hero Paradigms:** Asymmetric Split Hero, Editorial Manifesto Hero (large type, no asset, almost a poster), Video / Media Mask Hero, Kinetic-Type Hero, Curtain-Reveal Hero, Scroll-Pinned Hero.

**Navigation & Menus:** Mac OS Dock Magnification, Magnetic Button, Gooey Menu, Dynamic Island, Contextual Radial Menu, Floating Speed Dial, Mega Menu Reveal, and the Fluid Island Nav (section 7, the default).

**Layout & Grids:** Bento Grid, Masonry Layout, Chroma Grid, Split-Screen Scroll, Sticky-Stack Sections, Curtain Reveal, or one of the section 4 Layout Archetypes.

**Cards & Containers:** Parallax Tilt Card, Spotlight Border Card, Glassmorphism Panel (Double-Bezel is the treatment, section 6), Holographic Foil Card, Tinder Swipe Stack, Morphing Modal.

**Scroll-Animations:** Sticky Scroll Stack, Horizontal Scroll Hijack, Locomotive / Sequence Scroll, Zoom Parallax, Scroll Progress Path, Liquid Swipe Transition.

**Galleries & Media:** Dome Gallery, Coverflow Carousel, Drag-to-Pan Grid, Accordion Image Slider, Hover Image Trail, Glitch Effect Image.

**Typography & Text:** Kinetic Marquee (one per page), Text Mask Reveal, Text Scramble Effect, Circular Text Path, Gradient Stroke Animation, Kinetic Typography Grid.

**Micro-Interactions & Effects:** Particle Explosion Button, Liquid Pull-to-Refresh, Skeleton Shimmer, Directional Hover-Aware Button, Ripple Click Effect, Animated SVG Line Drawing, Mesh Gradient Background (palette-matched, section 5.2), Lens Blur Depth.

## 12. THE "MOTION-ENGINE" BENTO PARADIGM
When generating SaaS feature sections, use this "Bento 2.0" architecture, a "Vercel-core meets Dribbble-clean" aesthetic with physics where physics serves the content.

### A. Core Design Philosophy
* **Palette:** Background `#f9fafb`. Cards off-white with a 1px `border-slate-200/50`; the dark-mode pairing is defined by the page's token strategy.
* **Surfaces:** `rounded-[2.5rem]` for major containers. "Diffusion shadow" (`shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`) for depth without clutter.
* **Typography:** Strict `Geist`, `Satoshi`, or `Cabinet Grotesk`. `tracking-tight` for headers.
* **Labels:** Titles/descriptions placed outside and below cards, gallery-style.
* **Padding:** Generous `p-8` or `p-10` inside cards. Cell count and background diversity per section 5.7.

### B. Animation Engine Specs
* **Spring Physics:** `type: "spring", stiffness: 100, damping: 20`, no linear easing.
* **Layout Transitions:** `layout`/`layoutId` for smooth re-ordering and shared element transitions.
* **Active states are optional:** a card gets a looping "Active State" (Pulse, Typewriter, Float, Carousel) only when the loop communicates something (live status, a stream, an AI process). Informational cards stay still. Every loop collapses under reduced motion.
* **Performance:** Wrap dynamic lists in `<AnimatePresence>`. **CRITICAL:** memoize (`React.memo`) any perpetual motion and isolate it in its own microscopic Client Component; never trigger re-renders in the parent layout.

### C. The 5-Card Archetypes (options, not a quota)
1. **The Intelligent List:** vertical stack with an auto-sorting loop, items swap positions via `layoutId`.
2. **The Command Input:** search/AI bar with a multi-step Typewriter effect, blinking cursor, shimmering "processing" state.
3. **The Live Status:** scheduling interface with "breathing" status indicators, pop-up badge with an "Overshoot" spring.
4. **The Wide Data Stream:** horizontal carousel of metrics, seamless loop (`x: ["0%", "-100%"]`); counts as the page's one marquee.
5. **The Contextual UI (Focus Mode):** document view animating a staggered highlight, then a "Float-in" floating action toolbar.

## 13. REDESIGN MODE (detect, then hand off)
Misclassifying the mode is the biggest source of bad redesign output. Detect it as the first action:
* **Greenfield:** no existing site, or a full overhaul approved. This skill, dial baseline from section 1.
* **Redesign, preserve:** modernise without breaking the brand. **Redesign, overhaul:** new visual language on existing content and IA.
If ambiguous, ask once: *"Should this redesign preserve the existing brand, or are we starting visually from scratch?"*

For either redesign mode, the audit (brand tokens, information architecture, content blocks, patterns to preserve and retire, dial reading of the existing site, SEO baseline) and the modernisation levers belong to `redesign-existing-projects`; route there and apply only this skill's directives to the surfaces it names. Whatever the mode, **never change silently:** URL structure and route slugs, primary nav labels, form field names or order (analytics and autofill), the brand logo or wordmark, existing legal, consent, or cookie copy. A brand that is already purple stays purple (the section 5.2 override).

## 14. OUT OF SCOPE
Not for: dashboards, dense product UI, or admin panels (use Fluent, Carbon, Atlassian, or Polaris via section 2); data tables (TanStack Table, AG Grid); multi-step forms and wizards; code editors (Monaco, CodeMirror with their official skinning); native mobile (Apple HIG or Material directly, or the pack's mobile skill if installed); realtime collaboration UI. If the brief is one of these, say so explicitly, point to the right tool, and apply only this skill's marketing-page parts to the surfaces where they apply.

## 15. FINAL PRE-FLIGHT CHECK (countable items only)
Run before outputting. Each line is a count or a grep, not an opinion; if one fails, the page is not done.
- [ ] Design read stated in one line; dial values explicit, not silently baseline (section 0, 1)
- [ ] Em dash count in rendered copy: 0 (section 5.9)
- [ ] Eyebrow count at or below ceil(sections / 3), hero counted as 1 (section 5.7)
- [ ] No 3 consecutive image-plus-text split sections; no layout family used twice (section 5.7)
- [ ] Every bento grid: cells equal items, `grid-flow-dense` present, 2-3 cells visually varied (section 5.7)
- [ ] Hero: headline 2 lines or fewer, subtext 20 words or fewer, at most 4 text elements, top padding at most `pt-24`, CTA visible without scroll (section 5.7)
- [ ] No CTA label wraps at desktop; no two CTAs share an intent (section 5.5)
- [ ] Every button and form element passes WCAG AA against its background (section 5.5)
- [ ] `prefers-reduced-motion` handled for everything above `MOTION_INTENSITY 3`; no `window.addEventListener('scroll')` (section 8, 7)
- [ ] Both color modes rendered and checked; one theme per page (section 5.11, 8)
- [ ] `min-h-[100dvh]` not `h-screen`; every multi-column section declares its mobile collapse; `<main>` has the overflow guard (section 3)
- [ ] Marquee count at most 1; every animation has a one-sentence reason (section 7)
- [ ] Real images present (tool, picsum seed, or labeled `<!-- TODO -->` slots); zero div-based fake screenshots (section 5.8)
- [ ] Loading, empty, and error states present for anything that loads or submits (section 5.5)
- [ ] Copy self-audit done; no entry from `references/ai-tells.md` present (section 5.9, 10)
