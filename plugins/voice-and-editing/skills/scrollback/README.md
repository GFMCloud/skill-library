# Build a page in the Scrollback look

Part of the [voice-and-editing](../../README.md) pack.

Scrollback is one fixed visual style for pages that report facts: dashboards, invoices, changelogs, status pages, specifications, command-line output written up as a document. Everything is in a typewriter-style typeface, the only decoration is drawn with characters a terminal can print, corners are square, and one blue is allowed in three named places. This skill carries the stylesheet, a starter page, a catalogue of fourteen ready-made pieces such as tables, meters and log streams, and a small program that measures whether the colours are readable. It exists so a page built today looks like the one built last month, instead of whatever the style of the moment happens to be.

## Say this to use it

Any of these will do:

- "build this status page in Scrollback"
- "restyle this dashboard into our terminal look"
- "make an invoice using the SB-01 system"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:scrollback
```

It will first ask what the page is for, because the style is refused for some jobs. It is meant for pages that report state or fact. For consumer advertising, storytelling, or anything built around photographs, it says so and points you elsewhere rather than bending the style.

## What you'll get

A finished page or stylesheet, plus the output of the colour check if you asked for it.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```text
Wrote: ~/sites/status/index.html   (stylesheet inlined, one page, no build step)
Used:  frame, data table, status pill, meter, note

Colour check (python3 templates/verify.py):
  token      on canvas   on surface   floor   result
  --text       11.8:1       10.4:1     4.5:1   pass
  --muted       5.2:1        4.7:1     4.5:1   pass
  --rule        2.1:1        1.9:1     1.5:1   pass
  --accent      5.9:1        5.3:1     4.5:1   pass
  all floors held

Checked by eye at 1280px and 375px: no sideways scrolling, every
piece renders, focus outline visible on each link and button.
```

## Good to know

- **It writes the page or stylesheet you asked for, and nothing else.** It deletes and moves nothing.
- **It reads its own stylesheet and catalogue every time, and the page you point it at.** It is told not to retype colour values from memory, because the stylesheet is the one place they are allowed to live.
- **The pages it produces fetch a typeface from Google when someone opens them.** The skill itself makes no internet connection while building. If the page has to work offline, or you would rather not have readers' browsers contact Google, host the typeface yourself and change that one line.
- **The colour check is a small Python program you can run, and it needs Python 3.** It measures the contrast of every colour against both backgrounds and fails on a value that was guessed rather than measured. It only reads; it writes no file.
- **It asks for no accounts, keys or passwords.**
- **Inside a Scrollback page, this skill decides how charts look**, not the general chart guidance you may have installed. That is deliberate: one accent colour, no legend, no second series colour. The reasoning is recorded in the skill's own rulings file.
- **The colour names are treated as a published list that other things depend on.** Renaming or removing one is handled as a breaking change, with every page that uses it updated.
- **It is a single style, in one theme.** There is no light and dark pair, only a version for printing on paper. If your project already has its own visual system, that system wins and this skill says so.

## What next

- For a page that has to persuade or tell a story, this style is the wrong one. Use [frontend-design](../../../frontend-design/skills/frontend-design/) instead.
- For a quiet, document-like look that is not terminal styled: [minimalist-ui](../../../frontend-design/skills/minimalist-ui/).
- Before calling a finished page done, check it against what a visitor actually sees: [proof-of-work](../../../foundry-core/skills/proof-of-work/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
