---
name: chart-discipline
description: >
  Make any chart or data slide read as deliberate and trustworthy instead of a default
  library chart. Use this skill whenever you're building a chart, graph, data slide,
  dashboard, or any deck slide that contains data - and whenever the user says
  "make this chart better", "clean up this graph", "this slide is too busy", "what chart
  should I use for this", "visualize this data", or hands over numbers to turn into a
  visual. Always pull this in before building a data slide in PowerPoint, even if the
  user doesn't mention charts by name, as long as numbers are going onto a slide. It
  encodes chart-type selection, color discipline, and annotation rules; color comes from
  the project's own brand kit or design tokens if one exists, otherwise a neutral
  accessible default, so output stays consistent. Not for system or architecture diagrams
  with no numeric data - that's html-diagram.
metadata:
  maturity: incubator
---

# Chart Discipline

The gap between a default Excel/Plotly chart and one that looks deliberate is not the data - it's the discipline around the data. Color restraint, the right chart type, and real annotation. This skill encodes those rules so a data slide reads as crafted and trustworthy.

These rules are output-agnostic. They apply whether the chart ends up in a PPTX (the common case), an HTML diagram, or a one-pager. They are about judgment, not a rendering library.

**Color note:** This skill never defines hex values. Color is an identity decision, so use the project's own brand kit or design tokens if one exists (a tokens file, a CSS variables file, a provided style guide). If none exists, fall back to a neutral, accessible default (a single dark neutral for text, one clear accent color, grey for everything else) and say plainly to the user that you're using a default rather than a real brand palette. What this skill provides is the *rule* for how to use color, not the colors themselves.

---

## The five rules (apply to every chart)

1. **One hero, everything else grey.** Pick the single series or bar the slide is about and give it the accent color. Everything else goes grey. The viewer should know in one second which thing matters. Coloring every series means nothing stands out. (Hero color comes from the project's own brand kit or tokens if one exists, otherwise a neutral accessible default - state that assumption.)

2. **No rainbow ramps.** When you need a sequential scale (light to dark), the lightness has to move in one direction the whole way. Rainbow and jet ramps lie about order to colorblind readers and turn into mush when a deck gets printed greyscale. Use a monotonic single-hue ramp. Diverging colors (two hues meeting at a pale middle) only when there's a real zero - profit vs loss, above vs below target - never just because it looks nice.

3. **Pick the chart for the question, not the habit.** Line first for anything over time. Bar second, for comparing categories. Never pie. Never dual y-axes. Bars always start at zero - cropping the baseline lies about magnitude. Past about five lines on one chart, switch to small multiples (one small panel per series) instead of spaghetti. See the selection table below.

4. **Annotate like a sentence, not a label.** Every chart gets a declarative headline that states the takeaway - "RDS spend dropped 40% after rightsizing", not "Cost by month". Add a subtitle naming the unit and timeframe, and a source line. Label series directly at the end of the line instead of making the viewer bounce to a legend. Mark the one inflection that matters in place ("migration cutover", "RI purchase"). This is the single highest-leverage change you can make to a chart.

5. **Readable at a glance, readable on the wall.** The key takeaway has to land without anyone hovering, clicking, or squinting. Assume the slide gets shown over Zoom screen-share and printed in a leave-behind. If a label only works at full screen, rewrite it shorter.

---

## Chart-type selection

Match the question the slide answers to the chart type. The `scripts/chart_selector.py` helper returns this same logic as structured output if you want to call it; the table is here for fast reference.

| The question the slide answers | Use | Avoid |
|---|---|---|
| How did one thing change over time? | Line, single hero color, label at the end | Area chart unless the filled magnitude is the point |
| How did a few things change over time? | Line, one hero series in accent, rest grey | Coloring every line - viewers can track one or two, not six |
| How did many things (6+) change over time? | Small multiples, one panel each, shared axes | Piling 12 lines on one axis with a 12-color legend |
| How do a handful of categories compare? | Horizontal bar, sorted by value | Vertical bars that force rotated labels |
| How do many categories compare? | Dot plot or bar with only the head and tail labeled | 50 tiny bars when only 6 matter |
| How is something distributed? | Histogram or jittered dots | Box plots - general audiences don't read them |
| Are two things correlated? | Scatter with 3-5 named outliers annotated | A naked cloud of dots with no labels |
| What's it composed of? | Stacked bar (one bar per period) | Pie. Ever. Especially with more than four slices |
| How does composition shift over time? | Stacked area, most-volatile band on top | Streamgraphs - pretty, unreadable for actual numbers |
| Ranking? | Horizontal bar, sorted descending | Alphabetical sort, or lollipops where the dot carries no value |

When unsure, start with a line on a time axis. It's the safe default. Don't reach for novelty (sankey, radial, chord) until line and bar have actually failed.

---

## Annotation discipline (the linter)

`scripts/annotate.py` audits a chart spec against these rules and returns a 0-100 score plus a list of what to fix, sorted by severity. Run it when you want a quick objective gut check on a chart before it ships. The checks it runs:

- Missing headline, subtitle, source, or y-axis unit - every chart needs all four.
- Multiple series shown via legend instead of direct end-of-line labels.
- Every series colored, with no single hero.
- A known inflection point in the data left unannotated.
- A y-axis label that reads like a spreadsheet column name (`unemployment_rate`) instead of English ("Unemployment rate (%)").
- A bar chart that doesn't start at zero.
- Heavy gridlines or visible axis spines competing with the data.
- A rainbow or jet color ramp.

The script is pure logic - no rendering, no dependencies beyond the standard library - so it runs anywhere and doesn't care whether the chart is destined for PPTX or HTML.

---

## Applying this in PowerPoint

Most charts built with this discipline land in a deck via the python-pptx workflow. A few translation notes, since the source discipline came from web charting:

- **Color:** build the chart with the accent as the hero and a single grey for context. Get the hex values from the project's own brand kit or design tokens if one exists - do not introduce a new palette mid-deck. If there's no brand kit, use a neutral accessible default and say so.
- **Type:** use the deck's existing brand fonts if the project defines one. Do not pull in web fonts. The discipline that carries over is *two type weights doing the work* (a bold takeaway, regular everything else), not a specific typeface.
- **Headline:** the chart's declarative headline can live in the slide title or as a text box above the plot - either works, as long as it states the takeaway rather than naming the axes.
- **Direct labels:** add data labels at the end of the series and delete the legend. python-pptx and native charts both support this; it's worth the extra step every time.

---

## Pre-flight checklist

Before a data slide ships, confirm:

1. One hero color, everything else grey - and the hero is a brand color (or a stated neutral default).
2. The chart type matches the question (selection table above).
3. Bars start at zero.
4. There's a declarative headline stating the takeaway, plus unit, timeframe, and source.
5. Series are labeled directly, not via a legend.
6. No rainbow ramp; sequential scales move one direction in lightness.
7. The takeaway lands at a glance, including when printed greyscale.

If you can't get the takeaway across in the headline plus one clean chart, the problem is usually that the slide is trying to answer two questions. Split it.
