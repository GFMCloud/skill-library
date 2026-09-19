# Drawing a system you can click through

Part of the [decks](../../README.md) pack.

This builds one web page that shows how a system works. Components are boxes grouped into columns in the direction the data moves, the connections between them are labelled arrows, and clicking a box opens a short note about why that piece is there. Along the top is a row of buttons, one per named path through the system. Clicking one dims everything else and lights up just the boxes and arrows on that path, with the steps written out underneath. It is one file, it opens in any browser, and it has a light and a dark setting. It is meant for architectures, integrations, request paths and pipelines: things made of components with arrows between them, and no numbers to plot.

## Say this to use it

Any of these will do:

- "make an architecture diagram of this system"
- "show how a request flows through this"
- "turn this pipeline into a diagram I can click"

Or, to be certain this skill and no other one runs:

```
/decks:html-diagram
```

Before drawing anything it will ask you to confirm the parts list: what the components are, which ones group together, what connects to what, and which two to five paths through the system are worth having a button for. If your description is loose it reads the list back to you first, because moving a box after the arrows are placed is slow.

## What you'll get

One HTML file, two screenshots of it, and a note of what was assumed.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
$ python3 scripts/validate.py offer-pipeline.html --shots

structure    pass   file closes, script tags balanced, engine present
flows        pass   14 edges and 11 nodes, all found in the diagram
detail       pass   every node has a click-through entry
labels       pass   every label points at a real arrow
coverage     warn   edge e-audit-log is in no flow. Intentional?
screenshots  pass   offer-pipeline-light.png, offer-pipeline-dark-flow.png

Written to offer-pipeline.html. Calls I made on the architecture, correct
me if any are wrong:
  - the form submission is the ingress, not the scheduler
  - the credential read is a dependency, so it is drawn dashed
  - "Notify" is a separate flow, not the tail of "Create offer"
```

## Good to know

- **It deletes two files beside your diagram, without asking.** Before taking new screenshots it removes `<name>-light.png` and `<name>-dark-flow.png`, where `<name>` is your diagram's file name. That is so a stale image from an earlier run cannot be mistaken for a fresh one. If a file of yours happens to carry one of those names, it goes too.
- **It downloads a browser.** The screenshot step uses Playwright and a hidden Chromium, a few hundred megabytes, installed from the internet if they are not already there.
- **The finished diagram is not offline self-contained.** The skill's own text calls it self-contained with no dependencies. It is one file with no build step, which is what that phrase is about, but it fetches its font from Google every time anyone opens it. That means opening it tells Google it was opened, and on a machine with no internet the font falls back. The font link is a single line near the top of the file if you want it gone.
- **The check will not let a broken file through.** A diagram that got written in one piece can be cut off partway, which produces a file that looks finished but where nothing clicks. The checker looks for that first. If the screenshots cannot be taken, it fails rather than reporting them as skipped.
- **The check does not look at the picture.** It proves the two images were written. Whether the boxes overlap, the arrows cross through other boxes or the labels collide is for you to see. Open the two images.
- **It writes into your working folder and one outputs folder.** The template is copied to your file, the two screenshots are written beside it, and the finished diagram is copied to an outputs folder at the end.
- **The light or dark setting is stored in the viewer's browser.** Whoever opens the diagram gets their own choice remembered. Nothing about them is sent anywhere.
- **The packaging instruction at the end of the skill does not work.** It names a program that is not part of this pack, so that one command fails if you try it. Everything else in the skill runs.
- **It needs Python, and Playwright with Chromium for the screenshots.** Plus a browser to look at the result.

## What next

- Numbers rather than components? [chart-discipline](../chart-discipline/) handles anything with data to plot.
- Heading for a slide? [cd-to-pptx](../cd-to-pptx/) leaves a sized, labelled empty box on each diagram slide for you to drop a screenshot of this into.
- Deciding which slides need a visual at all? [deck-scaffolding-builder](../deck-scaffolding-builder/) does that before the deck is built.
- Back to the [decks pack](../../README.md), or to [skill-library](../../../../README.md).
