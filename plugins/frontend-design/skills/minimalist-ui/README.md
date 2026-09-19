# Building a quiet, document-style interface

Part of the [frontend-design](../../README.md) pack.

This skill builds web pages in one specific look: warm off-white background, almost no color, strong editorial typography, thin hairline borders, flat boxes laid out in an uneven grid, and pale washed-out accents used sparingly. It is the look of a well-made document rather than a marketing page, and it is close to what people mean when they name Notion, Linear or Stripe's documentation as a reference. The style is fixed, not negotiated: the skill carries the exact colors, the typefaces, the border widths, the spacing and the animation timings, and it lists the common defaults it refuses to use, including the Inter typeface, heavy drop shadows, gradients, pill-shaped buttons and emoji.

## Say this to use it

Any of these will do:

- "make this look clean and minimal, like Notion"
- "build a quiet, document-style landing page for this"
- "I want something understated and editorial, no gradients"

Or, to be certain this skill and no other one runs:

```
/frontend-design:minimalist-ui
```

It will ask what the page is for and who reads it, because the style needs real words and real names rather than filler. If you have a typeface or an accent color you must keep, say so; otherwise it uses its own.

## What you'll get

A page built to the style, with the colors, type sizes, borders and spacing all taken from the skill's fixed rules rather than chosen fresh.

EXAMPLE-PENDING-REAL-RUN

## Good to know

- **It writes code into the project you are working in.** HTML, CSS, Tailwind or React, depending on what your project already uses. It adds nothing outside that project.
- **Placeholder images come from a public website.** Where you have no real photograph, it points the page at `picsum.photos`, which serves stock pictures. Your browser fetches them when the page is viewed. Replace them before anyone else sees the page.
- **It runs no programs and installs nothing.** The skill is written instructions. It fetches nothing itself and needs no other software.
- **It asks for no sign-in and no key.**
- **The style is not adjustable.** It will not produce a bold, colorful or animated page. If that is what you want, this is the wrong skill.
- **It names typefaces you may not own.** The list includes commercial faces such as Lyon Text and Switzer. Where one is missing, the browser falls back through the list to a face you do have, which will not look the same. Tell it which typefaces you actually have.
- **It writes real words, not filler.** The skill forbids "Lorem Ipsum", "Acme Corp" and stock marketing phrases, so it will invent plausible copy about your actual subject. Read that copy before publishing it.

## What next

- Want a bolder or more colorful page instead? Use [design-taste-frontend](../design-taste-frontend/), which picks a style to fit the brief and runs louder than this one.
- Your site already exists and must not be rewritten? Use [redesign-existing-projects](../redesign-existing-projects/).
- Want to see the design as pictures before any code? Use [image-taste-frontend](../image-taste-frontend/).
- The page looks right but a control feels wrong? Use [emil-design-eng](../emil-design-eng/).
- Once the page is live, [site-review](../../../verification-kit/skills/site-review/) measures its speed, its accessibility and its broken links.
- Back to the [frontend-design pack](../../README.md), or to [skill-library](../../../../README.md).
