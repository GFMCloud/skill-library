# Deciding the look in pictures before writing code

Part of the [frontend-design](../../README.md) pack.

This skill settles what a page will look like before any code exists. If your Claude Code has an image-generation tool connected, it makes one reference picture per section of the page, labels each one as it arrives, then reads those pictures back as a specification: the headline text, the type sizes, the spacing between things, the button shapes, the colors, the grid. Only then does it write code to match. If you have no image tool, it says so and falls back to a reference picture you supply, or to a short written visual direction it agrees with you first. It is for pages whose whole point is how they look.

## Say this to use it

Any of these will do:

- "design this landing page visually first, then build it"
- "show me what the hero will look like before you code it"
- "here's a screenshot of a site I like, build mine to match"

Or, to be certain this skill and no other one runs:

```
/frontend-design:image-taste-frontend
```

It will say how many sections it is committing to before it generates anything, for example six images for a landing page, so you can correct the count while it is still cheap. It will also tell you plainly if it has no image tool and which fallback it is taking.

## What you'll get

The pictures first, then a written reading of each one, then the code built from it.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
No cropping, no boards: 6 horizontal images, one per section.
  hero, how it works, proof, pricing, questions, footer

[Section 1 of 6: hero]  (image)

Reading it as a specification:
  Text        "Ship the invoice, not the chase." / one line of sub / one button
  Typography  display serif about 4x the body, tight tracking, body at 1.6
  Spacing     headline to sub 24px, sub to button 40px, section padding 160px
  Components  one button, filled, 6px radius, no shadow, no outline secondary
  Color       bone background, ink text, a single clay accent on the button
  Structure   text left at a narrow measure, image bleeding off the right edge

[Section 2 of 6: how it works]  (image)
...

Built to it: src/app/page.tsx, src/app/globals.css
```

## Good to know

- **It calls an image-generation tool many times.** One picture per section, often six to twelve for a whole site, and more when a section needs a closer view. Each call costs whatever that tool costs you.
- **It will not reduce the count to save time.** By its own rule it generates the whole set rather than one board for the site, and it regenerates rather than crops.
- **It works without an image tool,** from a picture you supply or from a written direction. It is written never to stall waiting for a tool it does not have.
- **The image tool is yours, not the skill's.** If one is connected, you connected it, and its sign-in and its cost are yours. This skill sets nothing up and handles no key.
- **It writes code into the project you are working in,** and nothing outside it.
- **Placeholder photographs come from `picsum.photos`** when no generated or supplied picture is available. Your browser fetches those when the page is viewed.
- **It runs no programs and fetches nothing itself.**

## What next

- Happy to decide the look in words instead of pictures? Use [design-taste-frontend](../design-taste-frontend/), or [minimalist-ui](../minimalist-ui/) for a quiet style.
- Phone app screens rather than a web page? Use [mobile-taste-frontend](../mobile-taste-frontend/), which works the same way for screen sets.
- The site already exists? Use [redesign-existing-projects](../redesign-existing-projects/).
- Back to the [frontend-design pack](../../README.md), or to [skill-library](../../../../README.md).
