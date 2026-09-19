# Turning a designed deck into PowerPoint

Part of the [decks](../../README.md) pack.

A deck designed as a web page looks right and cannot be edited by anyone who does not write code. This skill rebuilds it as a real PowerPoint file: every heading, bullet, box, table and background becomes a native PowerPoint object that someone can click and change. It does not try to rebuild your charts and diagrams. Those come out as empty boxes at exactly the right size and position, each labelled with what belongs there, because an automatically rebuilt chart was never right and always cost more to correct than to redo. It then checks its own work by turning the new file back into images and comparing them against the PDF you started from.

## Say this to use it

Any of these will do:

- "convert this deck to PowerPoint"
- "turn this design export into an editable pptx"
- "I have six decks in this folder, make them all editable"

Or, to be certain this skill and no other one runs:

```
/decks:cd-to-pptx
```

It asks five things once, at the start, and then works through every deck in the run without asking again: where your design folder is, how close to the original you want it, how to name the output, whether to carry over speaker notes, and whether each deck stands alone or is a section of a larger one. Two things stop it. A deck with no reference PDF beside it, because the PDF is the only thing it can check against. And a first run on a new set-up, where it asks you to open the first finished file in real PowerPoint and confirm the fonts and positions before it trusts the rest of the batch.

## What you'll get

A PowerPoint file, plus a short list of what is unfinished and what looks wrong.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Built: Q4-Review_v1.pptx (14 slides, 1920x1080 -> 13.33in x 7.5in)
Fonts embedded: 2 of 2 found in the design folder, binary streams verified.

Placeholders you need to fill by hand (3):
  slide 4   CHART: cost by service (bar)        7.6in x 4.2in
  slide 7   CHART: headcount over time (line)   7.6in x 3.1in
  slide 11  DIAGRAM: request path               9.0in x 4.8in
  The title and caption around each one are live text, already in place.

Punch list:
  slide 2   real defect       subtitle wraps to 3 lines, PDF shows 2. Shorten or widen.
  slide 9   renderer artifact table gridlines look heavy in the check image only.
                              Object inspection shows the real borders are correct.

Nothing was overwritten. The previous file is still there.
```

## Good to know

- **It reads your deck folder and writes into it.** The new PowerPoint file, the PDF and images it makes while checking, and an optional report go where you say. It also leaves a small marker file called `.pipeline-validated` so later runs skip asking you to check the set-up again.
- **It never overwrites.** When a file of that name already exists it saves a new version instead, so the earlier one stays.
- **It installs software without stopping to ask.** If LibreOffice, poppler or the `python-pptx` library is missing, it fetches it. Its own instructions encourage this, so a first run on a clean computer can pull down several packages. If you would rather approve each one, install them yourself first.
- **It needs a reference PDF for every deck.** Without one it stops before doing any work, because the PDF is the only thing it can check the result against. The web page is not treated as the truth.
- **Three of its programs are other people's code.** They come from `gnipbao/knowledge-cat-ppt-skill` under the MIT license, fixed at one version, and they only open your PowerPoint file as a zip and read the structure inside. They make no network calls and run no commands.
- **The editability check does not touch your file.** It copies your file to a temporary folder, changes one line in the copy to prove the text is really editable, then confirms your original is unchanged before finishing.
- **It starts a second helper to compare slides.** During the check it hands the visual comparison to a separate helper set to a smaller model. That costs extra, and it finishes inside the run.
- **It cannot see inside PowerPoint.** The images it checks against come from LibreOffice, not from PowerPoint, so some differences are the check's own rendering rather than a fault in the file. It labels which it thinks each one is. The first file of any new set-up is yours to open and confirm.
- **It needs another skill.** It reads a separate `pptx` skill before building. Without one installed, it has no way to write the file.

## What next

- No slides yet? [deck-scaffolding-builder](../deck-scaffolding-builder/) plans the deck first, before anything is designed.
- The empty boxes this leaves behind are charts. [chart-discipline](../chart-discipline/) decides what each one should be before you draw it.
- For the diagram placeholders, [html-diagram](../html-diagram/) builds a system diagram you can screenshot into the box.
- Before the deck goes out, [layout-critique](../layout-critique/) and [sales-lens-review](../sales-lens-review/) read it back to you.
- Back to the [decks pack](../../README.md), or to [skill-library](../../../../README.md).
