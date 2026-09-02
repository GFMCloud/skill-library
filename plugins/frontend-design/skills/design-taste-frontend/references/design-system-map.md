# Brief to design system map

Derived from upstream `Leonxlnx/taste-skill` v2, `skills/taste-skill/SKILL.md` §2 and Appendices
A and B, at commit `ccbc15639c97057cbfcf32ecebc38ef716e4bb37`. Restyled to the pack's
conventions. The flagship body (`../SKILL.md`, section 2) states the rule; this file holds the
tables, install commands, and canonical sources.

Once the design read and the dials are set, pick the right foundation. Do not invent CSS for
things that have an official package, and do not pretend an aesthetic trend is an official system.

## A. When to reach for a real design system (use the official package)

| Brief reads as | Reach for | Why |
|---|---|---|
| Microsoft, enterprise SaaS, dashboards | `@fluentui/react-components` or `@fluentui/web-components` | Official Fluent UI, Microsoft tokens, accessibility done |
| Google-ish UI, Material-flavored product | `@material/web` plus Material 3 tokens | Official, themeable via Material Theming |
| IBM-style B2B, enterprise analytics | `@carbon/react` plus `@carbon/styles` | Official Carbon, mature data-density patterns |
| Shopify app surfaces | `polaris.js` web components or Polaris React | Required for Shopify admin UI |
| Atlassian, Jira-style product | `@atlaskit/*` plus `@atlaskit/tokens` | Official Atlassian design system |
| GitHub-style devtool or community page | `@primer/css` or `@primer/react-brand` | Official Primer; the Brand variant is for marketing |
| Public-sector UK service | `govuk-frontend` | Legally and regulatorily expected |
| US public-sector, trust-first | `uswds` | Same |
| Fast local-business or agency MVP | Bootstrap 5.3 | Boring, fast, works |
| Modern accessible React foundation | `@radix-ui/themes` | Primitives plus a polished theme |
| Modern SaaS where you own the components | shadcn/ui (`npx shadcn@latest add ...`) | You own the code and customize it easily; never ship the default state |
| Tailwind-based modern SaaS or AI marketing | Tailwind v4 utilities plus the `dark:` variant | Default for indie and small-team builds |

**Honesty rule:** if the brief reads as one of the systems above, install and use the official
package. Do not recreate its CSS by hand. Do not import a system's tokens and then override 90
percent of them.

**One system per project.** Do not mix Fluent React with Carbon in the same tree. Do not import
shadcn/ui components into a Material 3 app.

## B. When the brief is an aesthetic, not a system

There is no single official package for these. Build with native CSS plus Tailwind plus a
maintained component library, and be honest in code comments about what is borrowed inspiration
versus official material.

| Aesthetic | Honest implementation |
|---|---|
| Glassmorphism, "frosted glass" | `backdrop-filter`, layered borders, highlight overlays. Provide a solid-fill fallback for `prefers-reduced-transparency`. |
| Bento (Apple-style tile grids) | CSS Grid with mixed cell sizes. No single library owns this. |
| Brutalism | Native CSS, monospace, raw borders. No library. |
| Editorial, magazine | Serif type, asymmetric grid, generous whitespace. No library. |
| Dark tech, hacker | Mono plus an accent neon, terminal motifs. No library. |
| Aurora, mesh gradients | SVG or layered radial gradients. No library. |
| Kinetic typography | Native CSS animations, scroll-driven animations, GSAP for hijacks. No library. |
| Apple Liquid Glass | Apple documents this for Apple platforms only. There is no official `liquid-glass.css`. Web implementations are approximations; see `liquid-glass.md` and label them as such. |

## Appendix A. Install commands per design system

```bash
# Material Web (Material 3)
npm install @material/web

# Fluent UI React (v9)
npm install @fluentui/react-components

# Fluent UI Web Components (framework-free)
npm install @fluentui/web-components @fluentui/tokens

# IBM Carbon
npm install @carbon/react @carbon/styles

# Radix Themes
npm install @radix-ui/themes

# shadcn/ui (open code, owned components)
npx shadcn@latest init
npx shadcn@latest add button card badge separator input

# Primer CSS (GitHub product and devtool UI)
npm install --save @primer/css

# Primer Brand (GitHub marketing UI)
npm install @primer/react-brand

# GOV.UK Frontend
npm install govuk-frontend

# USWDS (US Web Design System)
npm install uswds

# Atlassian Design System (Atlaskit)
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/badge @atlaskit/section-message @atlaskit/card

# Bootstrap 5.3
npm install bootstrap

# Shopify Polaris Web Components (Shopify apps only)
# Add this to your app HTML head:
#   <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
#   <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```

## Appendix B. Canonical sources (read these before reinventing)

- Material Web: https://github.com/material-components/material-web, https://material-web.dev/theming/material-theming/, https://m3.material.io/develop/web
- Fluent UI: https://fluent2.microsoft.design/get-started/develop, https://fluent2.microsoft.design/components/web/react/, https://github.com/microsoft/fluentui, https://learn.microsoft.com/en-us/fluent-ui/web-components/
- Carbon: https://carbondesignsystem.com/, https://github.com/carbon-design-system/carbon, https://carbondesignsystem.com/developing/react-tutorial/overview/
- Shopify Polaris: https://shopify.dev/docs/api/app-home/web-components, https://github.com/Shopify/polaris-react, https://polaris-react.shopify.com/components
- Atlassian: https://atlassian.design/get-started/develop, https://atlassian.design/components/button/examples, https://atlassian.design/tokens/design-tokens
- Primer: https://primer.style/, https://github.com/primer/css, https://github.com/primer/brand
- GOV.UK: https://design-system.service.gov.uk/components/button/, https://design-system.service.gov.uk/styles/layout/, https://github.com/alphagov/govuk-frontend
- USWDS: https://designsystem.digital.gov/documentation/developers/, https://designsystem.digital.gov/components/button/, https://github.com/uswds/uswds
- Bootstrap: https://getbootstrap.com/docs/5.3/layout/grid/, https://getbootstrap.com/docs/5.3/components/card/
- Tailwind: https://tailwindcss.com/docs/dark-mode, https://tailwindcss.com/blog/tailwindcss-v4
- Radix: https://www.radix-ui.com/themes/docs/components/theme, https://github.com/radix-ui/themes
- shadcn/ui: https://ui.shadcn.com/docs, https://github.com/shadcn-ui/ui
- Native CSS and W3C: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter, https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme, https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion, https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations, https://drafts.csswg.org/scroll-animations-1/
- Apple Liquid Glass (Apple platforms only): https://developer.apple.com/design/human-interface-guidelines/materials, https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass, https://developer.apple.com/documentation/SwiftUI/Material
