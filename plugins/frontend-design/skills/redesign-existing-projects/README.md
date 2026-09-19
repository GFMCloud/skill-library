# Upgrading a site that already exists

Part of the [frontend-design](../../README.md) pack.

This skill takes a website or app that is already built and working, and improves how it looks without starting over. It reads your code first to find which framework and styling method you use, goes through a fixed audit of typography, color, spacing, borders, shadows, motion and missing states, lists every generic pattern it finds, then edits your existing files to fix them. It is written not to rewrite anything from scratch, which is the difference between this skill and every other one in the pack.

## Say this to use it

Any of these will do:

- "my site works but looks generic, upgrade it without rewriting it"
- "audit this app's design and fix what you find"
- "make this look less like an AI built it, but don't break anything"

Or, to be certain this skill and no other one runs:

```
/frontend-design:redesign-existing-projects
```

It will ask which part of the project to work on if you have not said. Point it at a folder, a page or a component. It is most useful on one screen at a time, because you can look at the result before letting it move on.

## What you'll get

A list of what it found, then edits applied to the files that are already there.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Stack: Next.js, Tailwind, one global stylesheet.

Found:
  Typography  Inter at three weights, headlines at default tracking
  Color       pure #000000 background; two accent colors, both at full saturation
  Surfaces    Tailwind shadow-lg on every card
  States      buttons have no focus ring and no disabled style
  Text        four headlines end in an orphaned single word

Changed:
  tailwind.config.ts   type scale, one accent, tabular figures for the table
  src/app/globals.css  background #0f0f10, tinted shadows, focus-visible ring
  src/components/Card.tsx  shadow removed, 1px border instead
  four headline strings  text-wrap: balance

Not changed: the layout, the routes, the copy, anything in src/lib.
```

## Good to know

- **It edits your existing files in place.** That is the point of it. Have your work saved or committed before you start, so you can compare or undo.
- **It reads your project's code first.** It needs to see the framework and the styling method before it changes anything.
- **It deletes and moves nothing.** It changes the contents of files it was pointed at.
- **It checks `package.json` before importing a new library,** and does not run an installer itself. `package.json` is the file listing which packages a project uses.
- **Placeholder images come from a public website.** If it adds a picture and you have no real one, it points at `picsum.photos`, which your browser fetches when the page is viewed.
- **It runs no programs, goes online for nothing itself, and asks for no sign-in.**
- **It judges look, not correctness.** It does not check that the site still works after its edits. Load the page yourself afterwards.

## What next

- Building something new rather than fixing something old? Use [design-taste-frontend](../design-taste-frontend/), or [minimalist-ui](../minimalist-ui/) for a quiet style.
- Controls that feel wrong rather than look wrong? Use [emil-design-eng](../emil-design-eng/).
- After the edits, [site-review](../../../verification-kit/skills/site-review/) measures the live site's speed, accessibility and broken links.
- Back to the [frontend-design pack](../../README.md), or to [skill-library](../../../../README.md).
