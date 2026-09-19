# Choosing a visual direction for a page

Part of the [frontend-design](../../README.md) pack.

This skill decides what a page should look like before it builds it, and makes the decision out loud so you can argue with it. It produces a compact plan: four to six named colors, a display typeface and a body typeface chosen for this subject rather than reached for by habit, a layout idea sketched in rough outline, and one signature element the page will be remembered by. It then reviews its own plan against the brief and revises anything that reads like the answer it would have given to any similar request, before writing a line of code. It knows the three looks that machine-made design currently clusters around, and avoids spending a free choice on one of them.

## Say this to use it

Any of these will do:

- "help me pick a palette and typography for this page"
- "what should this page actually look like? give me a direction first"
- "build this, but make the type treatment memorable rather than neutral"

Or, to be certain this skill and no other one runs:

```
/frontend-design:frontend-design
```

It will pin down what the subject is, who it is for, and what the page's single job is, and it will tell you what it decided rather than asking you for all three. If the brief leaves the visual direction open, it chooses and says why.

## What you'll get

A short written plan, revised once against the brief, then the page built to that plan exactly.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Subject: a two-person bookbindery. Audience: people commissioning one book.
The page's job: make someone write the first email.

Color     Board #C9BBA8  Ink #1B1815  Thread #7A2E2A  Paper #F2EDE4  Foil #B08D57
Type      Display: Canela, used only for the three section openers
          Body: Söhne, 17px, measure of 62 characters
          Utility: Söhne Mono for the price and lead-time table
Layout    One column, wide margins, each section opening on a full-bleed
          photograph of one stage of the work. No cards anywhere.
Signature A spine that builds down the left edge as you scroll, one band
          per section, in Foil.

Revised after self-review: first plan used a cream background with a serif
headline and a terracotta accent, which is one of the three defaults. Kept
the serif because the subject earns it; changed the ground to Board, which
is the color of the material this shop actually works in.
```

## Good to know

- **It writes the page or component into the project you are working in,** and nothing outside it.
- **It runs no programs, installs nothing and goes online for nothing.**
- **It asks for no sign-in and no key.**
- **It does most of the deciding before showing you anything.** The skill tells Claude Code to work through the options privately and only bring you ideas it has confidence in, so expect a plan rather than a menu.
- **It may use what it remembers about you.** The skill says to draw on anything already known about your preferences and past designs, if your Claude Code has such notes. If you want a clean slate, say so.
- **It takes one deliberate risk per page.** That is written into the skill. Everything around the risky element is meant to stay quiet, so if the page feels too plain in places, that is the design, not an omission.
- **It suggests keeping notes on what has been tried,** without naming a file. If you want that kept, tell it where to write it.
- **It can check its own work only if your Claude Code can take screenshots.** Without that, the self-critique happens in its head rather than against a picture.

## What next

- Ready to build a whole page from the direction? Use [design-taste-frontend](../design-taste-frontend/).
- Want that direction expressed in pictures instead of words? Use [image-taste-frontend](../image-taste-frontend/).
- Want a quiet, document-like style decided for you? Use [minimalist-ui](../minimalist-ui/).
- The page exists and needs fixing, not designing? Use [redesign-existing-projects](../redesign-existing-projects/).
- Back to the [frontend-design pack](../../README.md), or to [skill-library](../../../../README.md).
