# decks

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

Making a deck is several different jobs wearing one name. Deciding what each slide says. Deciding what the slide looks like. Getting a chart to tell the truth. Getting the finished thing into PowerPoint so someone can edit a typo without asking you. Each job has its own way of going wrong, and the wrong ones surface late, usually the evening before the deck is shown.

This pack splits the work into those jobs and gives Claude Code a method for each. Plan the deck before any slide exists. Choose a chart for the question it answers. Draw a system as a diagram you can click. Convert a designed deck into a real PowerPoint file. Then read the result twice: once asking whether it can be read, once asking whether someone could sell with it.

## When would I use this?

- You have notes, a transcript or an old deck, and you need a slide-by-slide plan before anyone starts making slides.
- You have numbers going onto a slide and you want a chart that states its point instead of naming its axes.
- You need to explain how a system works, and a picture people can click through would do it better than a paragraph.
- You have a deck designed as a web page and you need it as an editable PowerPoint file.
- A deck is finished and you want to know whether it is too busy before it goes in front of anyone.
- A deck is going to a sales team and you want to know whether a seller could actually use it.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/decks/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [cd-to-pptx](skills/cd-to-pptx/README.md) | Turns a slide deck exported as a web page into a real PowerPoint file you can edit, leaving charts and diagrams as labelled empty boxes for you to fill in. | "convert this deck to PowerPoint" | A `.pptx` file saved as a new version, a list of the placeholder boxes to fill by hand, and a note of anything that did not come across cleanly. | Reads your deck folder, builds a new PowerPoint file and some check images there, and installs missing conversion tools from the internet if they are not already on the machine. |
| [chart-discipline](skills/chart-discipline/README.md) | Decides which chart fits the question, cuts the colors back to one that matters, and makes the chart say its point in a sentence rather than naming its axes. | "what chart should I use for this?" or "clean up this graph" | Chart rules applied to your slide, and a score out of 100 with a sorted list of what to fix if you run its checker. | It runs two small local programs that read a chart description you point at and print advice; nothing is written, installed or sent anywhere. |
| [deck-scaffolding-builder](skills/deck-scaffolding-builder/README.md) | Plans a deck before any slide is made: a slide-by-slide outline, a design spec, a layout map, an optional rough wireframe, and a build plan. | "plan out a deck on our Q4 results" | A set of planning documents in your deck folder, with clear markers where your own knowledge is still needed. | It writes a set of planning documents for your deck into the folder you name, and searches the web only if you say yes when it offers. |
| [html-diagram](skills/html-diagram/README.md) | Builds one interactive web page that diagrams a system: boxes you can click for detail, and buttons that light up a single path through the diagram. | "make an architecture diagram of this system" | One HTML file you open in a browser, two screenshots of it, and a note of the judgment calls made about the architecture. | It writes an HTML diagram and two screenshot images into your working folder, can download and install a headless browser to take those screenshots, and the diagram it makes calls out to Google for a font whenever someone opens it. |
| [layout-critique](skills/layout-critique/) | Asks whether a slide reads: whether the eye lands in the right place, whether there are too many type sizes, whether the slide is too busy. | "does this slide read, or is it too busy?" | A pass or fail against each layout question, with the fix attached to each failure. | Nothing |
| [sales-lens-review](skills/sales-lens-review/) | Asks whether a sales slide or sheet would really help someone sell: whether it starts a conversation or only answers one. | "would a sales leader actually use this?" | Direct notes on what a seller could and could not do with the asset, and what to change. | Nothing |
<!-- /generated:whats-inside -->

The order above is not the order you use them. If slides do not exist yet, start with `deck-scaffolding-builder`. If they exist and you want them in PowerPoint, that is `cd-to-pptx`. `chart-discipline` and `html-diagram` each handle one kind of visual: numbers on a slide, and a system with no numbers in it. The last two are reviews of a deck that is already made.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | The deck folder you point at. `cd-to-pptx` reads the exported web page, the reference PDF, and the fonts and logos in your design folder.<br>`deck-scaffolding-builder` reads the reference material you name: notes, documents, prior plans, existing decks including PowerPoint and PDF files, brand documents, transcripts and screenshots.<br>`html-diagram` reads its own bundled template and rules, plus the diagram file you are working on.<br>`chart-discipline` reads one chart description file you name.<br>`layout-critique` and `sales-lens-review` read only the slide or deck you hand them. |
| Files written | `cd-to-pptx` writes the finished PowerPoint file, plus PDF and image renders it makes while checking the result, an optional report file wherever you name, and a small marker file called `.pipeline-validated` in your run folder or design folder.<br>`deck-scaffolding-builder` writes planning documents and web pages into your deck folder, asking where if that is unclear.<br>`html-diagram` copies its template to your working file and edits it, writes two screenshot images beside that file, and copies the finished diagram to an outputs folder. The diagram also remembers a light or dark setting in the browser of whoever views it.<br>`chart-discipline`, `layout-critique` and `sales-lens-review` write nothing. Both of the chart programs only print to the screen. |
| Files deleted or moved | One place. Before taking its screenshots, `html-diagram` deletes two files sitting next to your diagram, without asking. It works out their names from your diagram's name: `<name>-light.png` and `<name>-dark-flow.png`. If an unrelated file of yours happens to have one of those names, it goes too.<br>Nothing else here deletes or moves anything. `cd-to-pptx` and `deck-scaffolding-builder` are both told to save a new version rather than overwrite what is there. |
| Programs and scripts | `cd-to-pptx` runs three bundled Python programs that inspect a PowerPoint file. They are other people's code, included unchanged, from `gnipbao/knowledge-cat-ppt-skill` under the MIT license and fixed at one version. It also runs commands already on your computer: listing files, searching text, LibreOffice to turn PowerPoint into PDF, poppler to turn PDF pages into images, and the installers `pip`, `brew`, `apt-get` and `npm` when one of those tools is missing.<br>`chart-discipline` runs two small Python programs, one that scores a chart description and one that suggests a chart type. Both use only what comes with Python.<br>`html-diagram` runs a file copy, its own Python checker, and a hidden Chromium browser through Playwright to take the screenshots.<br>`deck-scaffolding-builder`, `layout-critique` and `sales-lens-review` ship no code at all. |
| Internet access | `cd-to-pptx` goes online on any run where a tool is missing: it installs that software from the internet, and its instructions also suggest downloading fonts from Google Fonts. Its three bundled programs never go online themselves.<br>`html-diagram` goes online twice over. It installs Playwright and downloads a Chromium browser if they are not there, a few hundred megabytes. Separately, the diagram it produces fetches its font from Google every time anyone opens it.<br>`deck-scaffolding-builder` searches the web only when you say yes to an offer it makes.<br>`chart-discipline`, `layout-critique` and `sales-lens-review` go online not at all. |
| Accounts, keys or passwords | None. Nothing in this pack asks you to sign in or hand over a key. |

Two limits. First, the diagram `html-diagram` makes is described in its own instructions as self-contained with no dependencies. It is one file with no build step, but it is not self-contained in the offline sense: it asks Google for its font each time it is opened, so opening it tells Google that it was opened. If that matters for your diagram, the font link is one line near the top of the file and can be removed. Second, the chart checker in `chart-discipline` is weaker than a score out of 100 sounds. It checks that a source line is present, not that the source exists or that the numbers match it, which the skill says itself. It also passes over any of its own rules that fails on a badly shaped description file, so a malformed description can score higher than a well-formed one.

## How the skills work together

In the order a deck is actually made:

1. **Before any slide exists:** `deck-scaffolding-builder` turns your notes and reference material into a slide-by-slide plan, a design spec and a build plan.
2. **While the visuals are being made:** `chart-discipline` for any slide with numbers on it. `html-diagram` for a system or flow with no numbers, which you can then screenshot into a slide.
3. **When the designed deck needs to be editable:** `cd-to-pptx` converts it to PowerPoint, leaving each chart and diagram as a labelled empty box at the right size for you to fill.
4. **Before it goes to anyone:** `layout-critique` asks whether each slide reads, then `sales-lens-review` asks whether a seller could use it. Run them in that order. A slide nobody can read rarely sells.

You do not need all of them. Each of the first three works on its own, and the last two work on any deck, however it was made.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install decks@skill-library
```

The first line is only needed once, however many packs you install.

Two skills here need other software. `cd-to-pptx` needs Python, LibreOffice, poppler and the `python-pptx` library, and it will try to install the missing ones itself rather than stopping to ask. It also needs a separate `pptx` skill, which it reads before building, and an export that includes a reference PDF. `html-diagram` needs Python, and Playwright plus its Chromium download for the screenshot step. `chart-discipline` needs Python. The rest need nothing installed.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
