# Making a chart say something

Part of the [decks](../../README.md) pack.

A chart made by default settings names its axes and leaves the reader to work out the point. This skill applies a small set of rules that make a chart say the point instead: pick the chart type from the question the slide answers, give the accent color to the one series that matters and grey to everything else, write a headline that states the finding rather than the subject, and label the lines where they end instead of in a legend. It also has rules about the numbers themselves, which come before any of the styling: every plotted value has to trace back to something on disk that you can read again, and anything the picture leaves out has to be said on the slide.

## Say this to use it

Any of these will do:

- "what chart should I use for this?"
- "clean up this graph, it is too busy"
- "here are the numbers, put them on a slide"

Or, to be certain this skill and no other one runs:

```
/decks:chart-discipline
```

It will ask what question the slide is answering, which one series or bar the slide is about, and where the numbers came from. If your project has its own brand colors or design tokens it uses those. If it does not, it uses a plain accessible default and tells you it is doing so rather than inventing a brand.

## What you'll get

The rules applied to your chart, and if you run its checker, a score with a sorted list of what to fix.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Score: 62 / 100

HIGH    No headline. "Cost by month" names the axes. State the finding:
        "RDS spend dropped 40% after rightsizing".
HIGH    Bar chart baseline starts at 1200, not zero. A cropped baseline
        overstates the difference. Bars always start at zero.
MEDIUM  All five series colored. Give the accent to one, grey to the rest.
MEDIUM  Series identified by a legend. Label each line at its right end
        instead, so the eye does not bounce.
LOW     y-axis reads "unemployment_rate". Write "Unemployment rate (%)".

Chart type: line is right for this one. It is a single measure over time.
```

## Good to know

- **It writes nothing and installs nothing.** Both of its programs only print to the screen. Neither one goes online, and neither one touches a file except the chart description you point at.
- **The score is weaker than it sounds.** The checker confirms a source line is present. It does not confirm the source exists, or that your plotted numbers match it. The skill says this about itself.
- **A malformed description can score too well.** Any of the checker's own rules that fails on a badly shaped description file is skipped over quietly, and the score comes back without it. A high score on a file you are unsure of is not evidence.
- **It never defines a color.** It gives the rule for using color, not the colors. It takes those from your project's brand kit or design tokens, and falls back to a plain accessible default when there is none, saying so.
- **It refuses some charts outright.** No pie charts, no two vertical axes on one chart, no rainbow color ramps, no bars that start above zero. These are stated as rules, not preferences.
- **It needs Python.** That is all. Nothing else is installed and nothing else is needed.

## What next

- Building the chart into a slide that came from a design export? [cd-to-pptx](../cd-to-pptx/) leaves a correctly sized empty box for each chart to go in.
- Planning the deck before the charts exist? [deck-scaffolding-builder](../deck-scaffolding-builder/) decides which slides carry a visual at all.
- No numbers in it, just components and arrows? That is [html-diagram](../html-diagram/), not this.
- Once the slide is made, [layout-critique](../layout-critique/) checks whether it reads at a glance.
- Back to the [decks pack](../../README.md), or to [skill-library](../../../../README.md).
