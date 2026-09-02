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
     machine-checkable. Folded in high-end-visual-design's named Vibe/Layout Archetypes (Section 3),
     the Double-Bezel component technique, and the Fluid Island nav pattern, since those were the
     genuinely additive pieces not already covered here. Banned-pattern lists were merged into supersets. -->

## 1. ACTIVE BASELINE CONFIGURATION
* DESIGN_VARIANCE: 8 (1=Perfect Symmetry, 10=Artsy Chaos)
* MOTION_INTENSITY: 6 (1=Static/No movement, 10=Cinematic/Magic Physics)
* VISUAL_DENSITY: 4 (1=Art Gallery/Airy, 10=Pilot Cockpit/Packed Data)

**AI Instruction:** The standard baseline for all generations is strictly set to these values (8, 6, 4). Do not ask the user to edit this file. Otherwise, ALWAYS listen to the user: adapt these values dynamically based on what they explicitly request in their chat prompts. Use these baseline (or user-overridden) values as your global variables to drive the specific logic in Sections 3 through 8.

## 2. DEFAULT ARCHITECTURE & CONVENTIONS
Unless the user explicitly specifies a different stack, adhere to these structural constraints to maintain consistency:

* **DEPENDENCY VERIFICATION [MANDATORY]:** Before importing ANY 3rd party library (e.g. `framer-motion`, `lucide-react`, `zustand`), you MUST check `package.json`. If the package is missing, you MUST output the installation command (e.g. `npm install package-name`) before providing the code. **Never** assume a library exists.
* **Framework & Interactivity:** React or Next.js. Default to Server Components (`RSC`).
    * **RSC SAFETY:** Global state works ONLY in Client Components. In Next.js, wrap providers in a `"use client"` component.
    * **INTERACTIVITY ISOLATION:** If Sections 4 or 8 (Motion/Liquid Glass) are active, the specific interactive UI component MUST be extracted as an isolated leaf component with `'use client'` at the very top. Server Components must exclusively render static layouts.
* **State Management:** Use local `useState`/`useReducer` for isolated UI. Use global state strictly for deep prop-drilling avoidance.
* **Styling Policy:** Use Tailwind CSS (v3/v4) for 90% of styling.
    * **TAILWIND VERSION LOCK:** Check `package.json` first. Do not use v4 syntax in v3 projects.
    * **T4 CONFIG GUARD:** For v4, do NOT use `tailwindcss` plugin in `postcss.config.js`. Use `@tailwindcss/postcss` or the Vite plugin.
* **ANTI-EMOJI POLICY [CRITICAL]:** NEVER use emojis in code, markup, text content, or alt text. Replace symbols with high-quality icons (Radix, Phosphor) or clean SVG primitives. Emojis are BANNED.
* **Responsiveness & Spacing:**
  * Standardize breakpoints (`sm`, `md`, `lg`, `xl`).
  * Contain page layouts using `max-w-[1400px] mx-auto` or `max-w-7xl`.
  * **Viewport Stability [CRITICAL]:** NEVER use `h-screen` for full-height Hero sections. ALWAYS use `min-h-[100dvh]` to prevent catastrophic layout jumping on mobile browsers (iOS Safari).
  * **Grid over Flex-Math:** NEVER use complex flexbox percentage math (`w-[calc(33%-1rem)]`). ALWAYS use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) for reliable structures.
* **Icons:** You MUST use exactly `@phosphor-icons/react` or `@radix-ui/react-icons` as the import paths (check installed version). Standardize `strokeWidth` globally (e.g., exclusively use `1.5` or `2.0`).

## 3. VIBE & LAYOUT ARCHETYPE SELECTION
Before writing code, silently "roll the dice" and select ONE Vibe Archetype and ONE Layout Archetype based on the prompt's context, so output is uniquely tailored but always premium. Never generate the exact same combination twice in a row for different projects.

### A. Vibe & Texture Archetypes (Pick 1)
1. **Ethereal Glass (SaaS / AI / Tech):** Deepest OLED black (`#050505`), radial mesh gradients (subtle glowing purple/emerald orbs) in the background. Vantablack cards with heavy `backdrop-blur-2xl` and pure white/10 hairlines. Wide geometric Grotesk typography.
2. **Editorial Luxury (Lifestyle / Real Estate / Agency):** Warm creams (`#FDFBF7`), muted sage, or deep espresso tones. High-contrast Variable Serif fonts for massive headings. Subtle CSS noise/film-grain overlay (`opacity-[0.03]`) for a physical paper feel.
3. **Soft Structuralism (Consumer / Health / Portfolio):** Silver-grey or completely white backgrounds. Massive bold Grotesk typography. Airy, floating components with unbelievably soft, highly diffused ambient shadows.

### B. Layout Archetypes (Pick 1)
1. **The Asymmetrical Bento:** A masonry-like CSS Grid of varying card sizes (e.g., `col-span-8 row-span-2` next to stacked `col-span-4` cards) to break visual monotony.
2. **The Z-Axis Cascade:** Elements stacked like physical cards, slightly overlapping each other with varying depths of field, some with a subtle `-2deg`/`3deg` rotation to break the digital grid.
3. **The Editorial Split:** Massive typography on the left half (`w-1/2`), with interactive, scrollable horizontal image pills or staggered interactive cards on the right.

**Mobile Collapse (applies to all three):** Falls back to a single-column stack (`grid-cols-1`, `w-full`) with generous vertical gaps (`gap-6`), `px-4 py-8`. Remove all rotations and negative-margin overlaps below `768px` - overlapping elements cause touch-target conflicts on mobile. Never use `h-screen` for full-height sections - always `min-h-[100dvh]`.

The archetype picked here sets the flavor; the numeric dials in Section 1 and Section 6 still drive how intensely that flavor gets expressed.

## 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)

> The pack-wide banned-pattern list is canonical at `references/ai-tells.md`. It is shared by
> redesign-existing-projects, minimalist-ui and image-taste-frontend. The rules below are this
> skill's engineering directives and are consistent with it. When a banned pattern changes, change
> it in `ai-tells.md`, not here.

LLMs have statistical biases toward specific UI cliché patterns. Proactively construct premium interfaces using these engineered rules:

**Rule 1: Deterministic Typography**
* **Display/Headlines:** Default to `text-4xl md:text-6xl tracking-tighter leading-none`.
    * **ANTI-SLOP:** Discourage `Inter` for "Premium" or "Creative" vibes. Force unique character using `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, `Clash Display`, `PP Editorial New`, or `Plus Jakarta Sans`.
    * **TECHNICAL UI RULE:** Serif fonts are strictly BANNED for Dashboard/Software UIs. Use Serif only for the Editorial Luxury vibe archetype or other creative/editorial contexts. For technical UIs, use exclusively high-end Sans-Serif pairings (`Geist` + `Geist Mono` or `Satoshi` + `JetBrains Mono`).
* **Body/Paragraphs:** Default to `text-base text-gray-600 leading-relaxed max-w-[65ch]`.

**Rule 2: Color Calibration**
* **Constraint:** Max 1 Accent Color. Saturation < 80%.
* **THE LILA BAN:** The "AI Purple/Blue" aesthetic is strictly BANNED. No purple button glows, no neon gradients. Use absolute neutral bases (Zinc/Slate) with high-contrast, singular accents (e.g. Emerald, Electric Blue, or Deep Rose).
* **COLOR CONSISTENCY:** Stick to one palette for the entire output. Do not fluctuate between warm and cool grays within the same project.

**Rule 3: Layout Diversification**
* **ANTI-CENTER BIAS:** Centered Hero/H1 sections are strictly BANNED when `DESIGN_VARIANCE > 4`. Use one of the Section 3 Layout Archetypes instead.

**Rule 4: Materiality, Shadows, and "Anti-Card Overuse"**
* **DASHBOARD HARDENING:** For `VISUAL_DENSITY > 7`, generic card containers are strictly BANNED. Use logic-grouping via `border-t`, `divide-y`, or purely negative space.
* **Execution:** Use cards ONLY when elevation communicates hierarchy. When a shadow is used, tint it to the background hue - see the Double-Bezel technique in Section 5 for the default card treatment when elevation is warranted.

**Rule 5: Interactive UI States**
* **Mandatory Generation:** You MUST implement full interaction cycles: Loading (skeletal loaders matching layout sizes), Empty States (composed, indicate how to populate data), Error States (clear, inline reporting), Tactile Feedback (`:active` uses `-translate-y-[1px]` or `scale-[0.98]`).

**Rule 6: Data & Form Patterns**
* **Forms:** Label MUST sit above input. Helper text optional but present in markup. Error text below input. Use a standard `gap-2` for input blocks.

## 5. HAPTIC MICRO-AESTHETICS (COMPONENT MASTERY)

### A. The "Double-Bezel" (Doppelrand / Nested Architecture)
This is the default treatment for any premium card, image, or container - never place one flatly on the background. They should look like physical, machined hardware (a glass plate sitting in an aluminum tray) using nested enclosures.
- **Outer Shell:** A wrapper `div` with a subtle background (`bg-black/5` or `bg-white/5`), a hairline outer border (`ring-1 ring-black/5` or `border border-white/10`), specific padding (e.g., `p-1.5` or `p-2`), and a large outer radius (`rounded-[2rem]`).
- **Inner Core:** The actual content container inside the shell, with its own distinct background color, its own inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), and a mathematically calculated smaller radius (e.g., `rounded-[calc(2rem-0.375rem)]`) for concentric curves.

### B. Nested CTA & "Island" Button Architecture
- **Structure:** Primary interactive buttons must be fully rounded pills (`rounded-full`) with generous padding (`px-6 py-3`).
- **The "Button-in-Button" Trailing Icon:** If a button has an arrow (`↗`), nest it inside its own distinct circular wrapper (e.g., `w-8 h-8 rounded-full bg-black/5 dark:bg-white/10 flex items-center justify-center`), flush with the main button's right inner padding.

### C. "Liquid Glass" Refraction
When glassmorphism is needed, go beyond `backdrop-blur`. Add a 1px inner border (`border-white/10`) and a subtle inner shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) to simulate physical edge refraction.

### D. Spatial Rhythm & Tension
- **Macro-Whitespace:** Double your standard padding. Use `py-24` to `py-40` for sections (up to `py-40` on Ethereal Glass / Editorial Luxury vibes). Allow the design to breathe heavily.
- **Eyebrow Tags:** Precede major H1/H2s with a microscopic, pill-shaped badge (`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em] font-medium`).

## 6. MOTION CHOREOGRAPHY

**Magnetic Micro-physics (If MOTION_INTENSITY > 5):** Buttons pull slightly toward the mouse cursor. **CRITICAL:** NEVER use React `useState` for magnetic hover or continuous animations. Use EXCLUSIVELY Framer Motion's `useMotionValue`/`useTransform` outside the React render cycle. On hover, scale the button down slightly (`active:scale-[0.98]`), translate the inner icon circle diagonally (`group-hover:translate-x-1 group-hover:-translate-y-[1px]`) and scale it up (`scale-105`) for internal kinetic tension.

**Perpetual Micro-Interactions:** When `MOTION_INTENSITY > 5`, embed continuous, infinite micro-animations (Pulse, Typewriter, Float, Shimmer, Carousel) in standard components. Apply premium Spring Physics (`type: "spring", stiffness: 100, damping: 20`) - no linear easing. Never use default `linear`/`ease-in-out` transitions for anything the user is meant to notice; use custom cubic-beziers (e.g. `cubic-bezier(0.32,0.72,0,1)`) where spring physics isn't the mechanism.

**Layout Transitions:** Always use Framer Motion's `layout`/`layoutId` props for smooth re-ordering, resizing, and shared element transitions.

**Staggered Orchestration:** Don't mount lists/grids instantly. Use `staggerChildren` (Framer) or CSS cascade (`animation-delay: calc(var(--index) * 100ms)`) for sequential waterfall reveals. **CRITICAL:** Parent (`variants`) and Children must reside in the identical Client Component tree; if data is async, pass it as props into a centralized Parent Motion wrapper.

**The "Fluid Island" Nav & Hamburger Reveal (default nav pattern):**
- **Closed State:** Navbar is a floating glass pill detached from the top (`mt-6`, `mx-auto`, `w-max`, `rounded-full`).
- **The Hamburger Morph:** On click, the hamburger lines fluidly rotate/translate to form a perfect 'X', not just disappear.
- **The Modal Expansion:** Menu opens as a massive, screen-filling overlay with heavy glass effect (`backdrop-blur-3xl bg-black/80` or `bg-white/80`).
- **Staggered Mask Reveal:** Nav links inside fade in and slide up from an invisible box (`translate-y-12 opacity-0` to `translate-y-0 opacity-100`) with staggered delay per item.

**Scroll Interpolation:** Elements never appear statically on load - gentle, heavy fade-up (`translate-y-16 blur-md opacity-0` resolving to `translate-y-0 blur-0 opacity-100` over 800ms+) as they enter viewport. Use `IntersectionObserver` or Framer Motion's `whileInView`. Never `window.addEventListener('scroll')` for entry animations - causes reflows and kills mobile perf. For complex scrolltelling or 3D/Canvas, GSAP (ScrollTrigger/Parallax) or ThreeJS/WebGL are acceptable, but **CRITICAL:** never mix GSAP/ThreeJS with Framer Motion in the same component tree - default to Framer Motion for UI/Bento interactions, reserve GSAP/ThreeJS exclusively for isolated full-page scrolltelling or canvas backgrounds, wrapped in strict `useEffect` cleanup blocks.

## 7. PERFORMANCE GUARDRAILS
* **DOM Cost:** Apply grain/noise filters exclusively to fixed, `pointer-events-none` pseudo-elements (e.g., `fixed inset-0 z-50 pointer-events-none`) and NEVER to scrolling containers.
* **Hardware Acceleration:** Never animate `top`, `left`, `width`, or `height`. Animate exclusively via `transform` and `opacity`.
* **Blur Constraints:** Apply `backdrop-blur` only to fixed/sticky elements (navbars, overlays). Never to scrolling containers or large content areas.
* **Z-Index Restraint:** NEVER spam arbitrary `z-50`/`z-10`/`z-[9999]`. Reserve z-indexes strictly for systemic layer contexts (Sticky Navbars, Modals, Overlays, Tooltips).

## 8. TECHNICAL REFERENCE (Dial Definitions)

### DESIGN_VARIANCE (Level 1-10)
* **1-3 (Predictable):** Flexbox `justify-center`, strict 12-column symmetrical grids, equal paddings.
* **4-7 (Offset):** `margin-top: -2rem` overlapping, varied image aspect ratios (4:3 next to 16:9), left-aligned headers over center-aligned data.
* **8-10 (Asymmetric):** Masonry layouts, CSS Grid with fractional units (`grid-template-columns: 2fr 1fr 1fr`), massive empty zones (`padding-left: 20vw`). Pull the specific structure from the Layout Archetype chosen in Section 3.
* **MOBILE OVERRIDE:** For levels 4-10, any asymmetric layout above `md:` MUST fall back to a strict single-column layout below `768px`.

### MOTION_INTENSITY (Level 1-10)
* **1-3 (Static):** No automatic animations. CSS `:hover`/`:active` only.
* **4-7 (Fluid CSS):** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. `animation-delay` cascades for load-ins. `transform`/`opacity` only. `will-change: transform` sparingly.
* **8-10 (Advanced Choreography):** Complex scroll-triggered reveals or parallax via Framer Motion hooks. NEVER `window.addEventListener('scroll')`.

### VISUAL_DENSITY (Level 1-10)
* **1-3 (Art Gallery Mode):** Lots of white space, huge section gaps, expensive and clean.
* **4-7 (Daily App Mode):** Normal spacing for standard web apps.
* **8-10 (Cockpit Mode):** Tiny paddings, no card boxes, 1px lines to separate data, everything packed. **Mandatory:** Monospace (`font-mono`) for all numbers.

## 9. AI TELLS (Forbidden Patterns)
To guarantee a premium, non-generic output, strictly avoid these unless explicitly requested:

### Visual & CSS
* **NO Neon/Outer Glows:** No default `box-shadow` glows. Use inner borders or subtle tinted shadows.
* **NO Pure Black:** Never `#000000`. Use Off-Black, Zinc-950, Charcoal, or the Ethereal Glass archetype's `#050505`.
* **NO Oversaturated Accents.**
* **NO Excessive Gradient Text** for large headers.
* **NO Custom Mouse Cursors.**

### Typography
* **NO Inter, Roboto, Arial, Open Sans, or Helvetica.** Use `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, `Clash Display`, `PP Editorial New`, or `Plus Jakarta Sans`.
* **NO Oversized H1s** that scream - control hierarchy with weight and color.
* **Serif Constraints:** Serif ONLY for Editorial Luxury / creative-editorial contexts. NEVER on clean dashboards.

### Icons
* **NO standard thick-stroked Lucide, FontAwesome, or Material Icons.** Use `@phosphor-icons/react` (Light weight preferred for premium contexts) or `@radix-ui/react-icons`.

### Layout & Spacing
* **Align & Space Perfectly:** Padding/margins mathematically consistent.
* **NO generic edge-to-edge sticky navbars** - use the Fluid Island pattern (Section 6) instead.
* **NO 3-Column Card Layouts:** The generic "3 equal cards horizontally" feature row is BANNED. Use a 2-column Zig-Zag, asymmetric grid, or horizontal scroll instead.

### Content & Data (The "Jane Doe" Effect)
* **NO Generic Names** ("John Doe", "Sarah Chan," "Jack Su") - use creative, realistic-sounding names.
* **NO Generic Avatars** (standard SVG "egg" or Lucide user icons) - use creative, believable photo placeholders.
* **NO Fake Numbers** (`99.99%`, `50%`, `1234567`) - use organic, messy data (`47.2%`, `+1 (312) 847-1928`).
* **NO Startup Slop Names** ("Acme", "Nexus", "SmartFlow") - invent premium, contextual brand names.
* **NO Filler Words** ("Elevate", "Seamless", "Unleash", "Next-Gen") - use concrete verbs.

### External Resources & Components
* **NO Broken Unsplash Links** - use `https://picsum.photos/seed/{random_string}/800/600` or SVG UI Avatars.
* **shadcn/ui:** May be used, but NEVER in its generic default state - customize radii, colors, and shadows.
* **Production-Ready Cleanliness:** Code must be extremely clean, visually striking, memorable, and meticulously refined.

## 10. THE CREATIVE ARSENAL (High-End Inspiration)
Do not default to generic UI. Pull from this library of advanced concepts:

**Navigation & Menus:** Mac OS Dock Magnification, Magnetic Button, Gooey Menu, Dynamic Island, Contextual Radial Menu, Floating Speed Dial, Mega Menu Reveal, and the Fluid Island Nav (Section 6, the default).

**Layout & Grids:** Bento Grid, Masonry Layout, Chroma Grid, Split Screen Scroll, Curtain Reveal - or reach directly for one of the Section 3 Layout Archetypes.

**Cards & Containers:** Parallax Tilt Card, Spotlight Border Card, Glassmorphism Panel (Double-Bezel is the default treatment - Section 5), Holographic Foil Card, Tinder Swipe Stack, Morphing Modal.

**Scroll-Animations:** Sticky Scroll Stack, Horizontal Scroll Hijack, Locomotive Scroll Sequence, Zoom Parallax, Scroll Progress Path, Liquid Swipe Transition.

**Galleries & Media:** Dome Gallery, Coverflow Carousel, Drag-to-Pan Grid, Accordion Image Slider, Hover Image Trail, Glitch Effect Image.

**Typography & Text:** Kinetic Marquee, Text Mask Reveal, Text Scramble Effect, Circular Text Path, Gradient Stroke Animation, Kinetic Typography Grid.

**Micro-Interactions & Effects:** Particle Explosion Button, Liquid Pull-to-Refresh, Skeleton Shimmer, Directional Hover Aware Button, Ripple Click Effect, Animated SVG Line Drawing, Mesh Gradient Background, Lens Blur Depth.

## 11. THE "MOTION-ENGINE" BENTO PARADIGM
When generating modern SaaS dashboards or feature sections, use this "Bento 2.0" architecture - a "Vercel-core meets Dribbble-clean" aesthetic reliant on perpetual physics.

### A. Core Design Philosophy
* **Palette:** Background `#f9fafb`. Cards pure white (`#ffffff`) with a 1px `border-slate-200/50`.
* **Surfaces:** `rounded-[2.5rem]` for major containers. "Diffusion shadow" (`shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`) for depth without clutter.
* **Typography:** Strict `Geist`, `Satoshi`, or `Cabinet Grotesk`. `tracking-tight` for headers.
* **Labels:** Titles/descriptions placed outside and below cards - clean, gallery-style presentation.
* **Padding:** Generous `p-8` or `p-10` inside cards.

### B. Animation Engine Specs
* **Spring Physics:** `type: "spring", stiffness: 100, damping: 20` - no linear easing.
* **Layout Transitions:** `layout`/`layoutId` for smooth re-ordering and shared element transitions.
* **Infinite Loops:** Every card has an "Active State" that loops infinitely (Pulse, Typewriter, Float, or Carousel).
* **Performance:** Wrap dynamic lists in `<AnimatePresence>`. **CRITICAL:** memoize (`React.memo`) any perpetual motion/infinite loop and isolate it in its own microscopic Client Component - never trigger re-renders in the parent layout.

### C. The 5-Card Archetypes
1. **The Intelligent List:** vertical stack with an infinite auto-sorting loop, items swap positions via `layoutId`.
2. **The Command Input:** search/AI bar with multi-step Typewriter Effect, blinking cursor, shimmering "processing" state.
3. **The Live Status:** scheduling interface with "breathing" status indicators, pop-up badge with "Overshoot" spring effect.
4. **The Wide Data Stream:** horizontal "Infinite Carousel" of metrics, seamless loop (`x: ["0%", "-100%"]`).
5. **The Contextual UI (Focus Mode):** document view animating a staggered highlight, followed by a "Float-in" floating action toolbar.

## 12. FINAL PRE-FLIGHT CHECK
Evaluate your code against this matrix before outputting - this is the last filter:
- [ ] Vibe Archetype and Layout Archetype (Section 3) were consciously selected and applied
- [ ] Global state used appropriately, not arbitrarily
- [ ] Mobile layout collapse guaranteed for high-variance designs
- [ ] Full-height sections use `min-h-[100dvh]`, never `h-screen`
- [ ] `useEffect` animations contain strict cleanup functions
- [ ] Empty, loading, and error states provided
- [ ] Cards use the Double-Bezel nested architecture where elevation is warranted; omitted in favor of spacing elsewhere
- [ ] CTA buttons use the Button-in-Button trailing icon pattern where applicable
- [ ] Section padding at minimum `py-24`
- [ ] All transitions use custom cubic-bezier or spring physics - no `linear`/`ease-in-out`
- [ ] Scroll entry animations present - no element appears statically
- [ ] All animations use only `transform`/`opacity`
- [ ] CPU-heavy perpetual animations strictly isolated in their own Client Components
- [ ] No banned fonts, icons, borders, shadows, layouts, or motion patterns from Section 9 are present
- [ ] The overall impression reads as a premium agency build, not a template with nice fonts
