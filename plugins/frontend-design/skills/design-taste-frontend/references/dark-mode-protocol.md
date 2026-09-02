# Dark mode protocol

Derived from upstream `Leonxlnx/taste-skill` v2, `skills/taste-skill/SKILL.md` §6.C and §8, at
commit `ccbc15639c97057cbfcf32ecebc38ef716e4bb37`. Restyled to the pack's conventions. The flagship
body (`../SKILL.md`, section 8) states that dark mode is mandatory for consumer-facing pages; this
file is the procedure.

Dual-mode by default. Never assume light-only unless the brief is print-emulating editorial, and
never ship light-only or dark-only without explicit user instruction. Design for both modes from
the start; retrofitting one is where hierarchy breaks.

## A. Token strategy (pick one, stick to it)

- **Tailwind `dark:` variant** (default for utility-first projects): every color utility is paired
  with its dark variant (`bg-white dark:bg-zinc-950`, `text-gray-900 dark:text-gray-100`).
- **CSS variables** (for shadcn/ui, Radix Themes, or component libraries with theming): define
  semantic tokens (`--surface`, `--surface-elevated`, `--text-primary`, `--accent`) and swap the
  values under `[data-theme="dark"]` or `@media (prefers-color-scheme: dark)`.

One strategy per project. Mixing the two produces surfaces that flip in one mode and not the other.

## B. Do not prescribe specific colors here

The brief and the brand decide the colors. This protocol enforces only:

- **Contrast.** WCAG AA minimum for all text in both modes; AAA is the target for body and hero
  copy. (Upstream stated this two different ways in two sections; this is the reconciled rule.)
- **Hierarchy parity.** Visual hierarchy that works in light must work in dark. If a CTA pops in
  light, it pops in dark.
- **Brand fidelity.** The primary brand color stays recognizable. Do not desaturate the brand into
  a dark mode.
- **No pure `#000000` and no pure `#ffffff`.** Use off-black (zinc-950, a near-black warm gray) and
  off-white. Pure values kill depth.

## C. Default mode

Respect `prefers-color-scheme` unless the brand insists on one mode. Add a manual toggle if either
mode would lose key brand expression.

When a design system with built-in theming is in use (Radix Themes, shadcn/ui with `<Theme>`), set
the theme once in `layout.tsx` or the page root. Individual sections do not override it; the page
theme lock in the flagship body applies.

## D. Test in both modes before finishing

Open the page in both modes during development. Do not ship a page you have only seen in one mode.
Logos, hairlines, and image overlays are the usual casualties: a `1px solid #EAEAEA` hairline is
invisible on a dark surface, and a black-on-transparent logo disappears.
