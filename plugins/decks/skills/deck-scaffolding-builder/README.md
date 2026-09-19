# Planning a deck before you make it

Part of the [decks](../../README.md) pack.

Most of the work in a deck happens before a single slide is designed, and most of it is the same work every time: what each slide says, what type each slide is, how the sections are ordered, which slides carry a visual. This skill does that upstream part and stops there. It reads whatever you already have, notes, a transcript, an old deck, a conversation, and turns it into a slide-by-slide plan with real draft copy in it. Where it does not know something only you know, it does not invent a plausible answer. It writes a marker in the text saying what it needs from you, and lists every one of those markers at the end so you have a short list to work through rather than a document to audit.

## Say this to use it

Any of these will do:

- "plan out a deck on our Q4 results"
- "turn these notes into a deck blueprint"
- "restructure this old deck into a proper outline"

Or, to be certain this skill and no other one runs:

```
/decks:deck-scaffolding-builder
```

It asks what the deck is about, who is watching it, and what they should do or believe afterwards. It asks what reference material to read. It asks which documents you want out of it and where to save them. For a small deck that is the whole intake. It asks more only for a large reusable deck that sections get pulled out of.

## What you'll get

A set of planning documents in your deck folder, and a punch list of what is still missing.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Written to ~/decks/q4-review/:
  q4-review-blueprint_v1.md     14 slides, five fields filled on each
  q4-review-design-spec.md      mode mix and section accents for this deck
  q4-review-layout-map.html     one-screen grid of every slide, color coded
  q4-review-build-plan.md       build order, and which 3 slides carry a chart

Needs your input (4):
  slide 3   the real customer situation: which failure pattern do you see?
  slide 6   the number behind "most teams" - do we have one?
  slide 9   name the two accounts this pattern came from, or cut the claim
  slide 12  the ask. "Talk to us" is not an ask.

Cut proposed: slides 7 and 8 make the same point. One of them should go.
Nothing was overwritten. This is v1.
```

## Good to know

- **It writes planning documents into your deck folder, and asks where if that is unclear.** An outline, a design spec, a layout map, an optional rough wireframe, ready-to-paste build prompts and a build plan. It never guesses the path.
- **It saves new versions rather than overwriting.** Blueprints go through heavy revision, so each pass is saved beside the last one with the change summary kept at the top.
- **It ships no programs.** There is nothing to install and nothing runs. The templates it fills in are plain web pages and documents with no scripts in them, and they load nothing from the internet.
- **It goes online only if you say yes.** When several slides in a row need facts nobody has supplied, it offers to look them up first and waits for your answer. Research fills background, never your own knowledge of your customers.
- **It does not make slides.** It stops at the plan. If you ask for a finished deck it produces the plan and offers to hand it on rather than quietly building slides. The one exception is a rough grey-box wireframe, which it makes if you ask for it, because that is a tweaking aid rather than a deliverable.
- **It starts a second helper on a large deck.** The final check of the plan goes to a separate helper set to a smaller model, for a fresh reading. That costs extra, and it finishes inside the run.
- **It needs another skill to read a PowerPoint file.** If you want an existing `.pptx` used as reference, a separate `pptx` skill has to be installed. PDFs it reads by itself.
- **It has an opinion about length.** A deck that gets presented is usually ten to twenty slides. When a plan grows past what the content supports it says so and proposes the cut.

## What next

- Once the plan is agreed and the deck is designed, [cd-to-pptx](../cd-to-pptx/) turns the design into an editable PowerPoint file.
- For the slides carrying numbers, [chart-discipline](../chart-discipline/) picks the chart before it is drawn.
- For a slide that has to explain a system, [html-diagram](../html-diagram/) builds a diagram you can screenshot into it.
- When the deck exists, [layout-critique](../layout-critique/) then [sales-lens-review](../sales-lens-review/).
- Back to the [decks pack](../../README.md), or to [skill-library](../../../../README.md).
