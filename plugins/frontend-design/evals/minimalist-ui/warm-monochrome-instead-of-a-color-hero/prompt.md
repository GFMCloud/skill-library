---
name: warm-monochrome-instead-of-a-color-hero
runs: 1
max_turns: 12
timeout_seconds: 240
allowed_tools: [Read, Write, Skill]
---
Use the minimalist-ui skill. Ledgerlane is a FIXTURE invoicing tool for freelance
translators. Build the color layer for its changelog page: a full-width hero band
across the top, a bento grid of release cards below it, and a row of small status
badges on each card reading "shipped", "beta" and "deprecated". Do not ask me
anything, just build it.

Write `palette.css` in the current directory. It must define, as CSS custom
properties and applied rules:

1. the page canvas background and the card surface background
2. the border on every card and divider, written out in full
3. the card border-radius and internal padding
4. the hero band background
5. the background color and the text color of each of the three status badges

Then in your reply, list every hex value the file uses, each one labelled with
what it colors.
