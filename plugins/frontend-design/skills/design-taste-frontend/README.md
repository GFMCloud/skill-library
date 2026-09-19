# Building a new page that does not look templated

Part of the [frontend-design](../../README.md) pack.

This skill builds a new web page from nothing and tries to give it a character of its own. Before writing any code it reads your brief for what kind of page it is, who reads it, and what look you hinted at, then says out loud what it decided. It carries a long list of the patterns that make a page look machine-made, such as the purple gradient behind a centered headline, three equal feature cards and the Inter typeface everywhere, and it reaches past them deliberately. It is for landing pages, portfolios, marketing pages and about pages. It is not for dashboards, data tables or multi-step forms.

## Say this to use it

Any of these will do:

- "build me a landing page for this that doesn't look like every other AI site"
- "design and build a portfolio home page with a real point of view"
- "make a marketing page for this product, Awwwards-style, not a template"

Or, to be certain this skill and no other one runs:

```
/frontend-design:design-taste-frontend
```

It will state the design it read from your brief in one line, for example that it is reading this as a business landing page for technical buyers in a restrained style. It asks you at most one question, and only when the brief genuinely points two ways. Otherwise it declares what it decided and carries on, so read that line and correct it if it is wrong.

## What you'll get

The design read first, then the page's code written into your project.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Reading this as: a landing page for a small accounting practice, for owners of
one-person businesses, in a warm and plain-spoken style, leaning toward a
serif headline with a narrow measure and very little motion.

Not doing: the centered hero over a dark gradient, the three equal cards, Inter.

Written:
  src/app/page.tsx          the page
  src/app/globals.css       the color and type scale
  src/components/Ledger.tsx the signature element, a running figure that
                            settles as you scroll

One package is missing. Run this yourself if you want the serif:
  npm install @fontsource/newsreader
```

## Good to know

- **It writes code into the project you are working in.** React, Next.js, CSS or Tailwind, matching what the project already uses. It writes nothing outside that project.
- **It reads your project's `package.json`.** That is the file listing which packages a project uses. It checks there before using a package or naming a Tailwind version.
- **It does not install anything.** When a package is missing it prints the `npm install` or `npx` command and leaves you to run it.
- **It uses an image-generation tool first, if you have one.** If such a tool is connected to Claude Code, the skill uses it to make each section's pictures, which may cost you whatever that tool charges. Without one it falls back to placeholder images.
- **The code it writes can point at public websites.** Placeholder photographs come from `picsum.photos` and company logos from `cdn.simpleicons.org`. For a Shopify app it includes a script from `cdn.shopify.com` as standard starting code. Your browser or your build loads those; the skill fetches nothing itself.
- **It asks for no sign-in and no key, and runs no programs.**
- **It is for pages, not products.** Dashboards, data tables and multi-step forms are outside what it covers, by its own statement.
- **Accessibility and regulated work override its taste.** The skill is written so that a public-sector, accessibility-first or trust-first brief beats every style choice it would otherwise make.

## What next

- Want a quiet, document-like page instead? Use [minimalist-ui](../minimalist-ui/), which holds one fixed restrained style.
- The site already exists and must not be rewritten? Use [redesign-existing-projects](../redesign-existing-projects/).
- Want the look settled in pictures before code? Use [image-taste-frontend](../image-taste-frontend/) first.
- Want the palette and typefaces argued out before building? Use [frontend-design](../frontend-design/).
- Phone app screens rather than a web page? Use [mobile-taste-frontend](../mobile-taste-frontend/).
- Back to the [frontend-design pack](../../README.md), or to [skill-library](../../../../README.md).
