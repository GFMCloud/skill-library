# AI Tells: the shared banned-pattern list

Canonical list for the frontend-design pack. `design-taste-frontend`, `redesign-existing-projects`,
`minimalist-ui` and `image-taste-frontend` all defer to this file rather than restating it.

If a pattern below needs to change, change it here. Do not copy it back into a SKILL.md.

## Typography

- Do not reach for Inter or Roboto on premium or creative work. Prefer Geist, Outfit, Cabinet Grotesk,
  Satoshi, Clash Display, PP Editorial New, or Plus Jakarta Sans.
- Serif fonts are banned for dashboard and software UI. Serif belongs to editorial and creative
  contexts only. Technical UI uses high-end sans pairings such as Geist plus Geist Mono, or Satoshi
  plus JetBrains Mono.
- No giant heading paired with weak tiny subcopy.
- No more than two font moods in one design.
- No lazy all-caps everywhere.
- No gradient headline tricks.
- Body copy caps at roughly 65 characters per line.

## Color

- The AI purple and blue aesthetic is banned. No purple button glows, no neon gradients.
- One accent color maximum, saturation under 80 percent. Neutral bases (Zinc, Slate) with a single
  high-contrast accent such as emerald, electric blue, or deep rose.
- Do not mix warm and cool grays inside one project.
- Do not replace a designed palette with generic default web colors.

## Layout

- No cards inside cards inside cards.
- No giant rounded wrapper section containing more bordered panels.
- No dashboard-style compartment stacking without a reason.
- Centered hero and H1 sections are banned when design variance is above 4.
- No three-card rows repeated section after section.
- No cloned left-text / right-image blocks down the whole page.
- Never use `h-screen` for full-height sections. Use `min-h-[100dvh]`, which avoids layout jump on
  iOS Safari.
- Use CSS Grid rather than flexbox percentage math such as `w-[calc(33%-1rem)]`.
- Contain page layouts with `max-w-[1400px] mx-auto` or `max-w-7xl`.
- Generic card containers are banned at visual density above 7. Group with `border-t`, `divide-y`, or
  negative space instead.

## Motion

- Animate transform and opacity only. Anything else risks jank.
- No decorative motion that does not serve hierarchy or feedback.

## Icons and symbols

- Never use emojis in code, markup, text content, or alt text.
- Use `@phosphor-icons/react` or `@radix-ui/react-icons`. Standardize stroke width globally, typically
  1.5 or 2.0.

## Content and copy

- No filler verbs: unleash, elevate, revolutionize, next-gen, seamless, transformative platform.
- No placeholder brand names: Acme, Nexus, Flowbit, Quantumly, NovaCore.
- No placeholder people: John Doe, Jane Doe.
- No invented statistics or fake logos presented as real.
- No pseudo-enterprise jargon used as decoration: fake control labels, decorative system markers,
  filler status microcopy, invented runtime or orchestration terminology, strings like
  "00 orchestration layer".

## Density

- No over-packed sections or card overload.
- No tiny spacing between major sections.
- No visually exhausting walls of content.
- Decorative empty space with no purpose is also a failure, not restraint.

## Visual effects

- No floating blobs, no stacked glassmorphism without reason, no glowing edges everywhere.
- No over-rendered noise that hides the layout.
- Random futuristic detail with no underlying structure is slop.

## Interaction completeness

Any interface that loads or submits data implements the full cycle: loading state with skeletal
loaders matching final layout size, empty state that shows how to populate it, inline error state,
and tactile active feedback such as `-translate-y-[1px]` or `scale-[0.98]`.
