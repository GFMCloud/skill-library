---
name: scroll-entry-without-a-scroll-listener
runs: 1
max_turns: 12
timeout_seconds: 240
allowed_tools: [Read, Write, Skill]
---
Use the minimalist-ui skill. Ledgerlane is a FIXTURE invoicing tool for freelance
translators. Its landing page has four stacked sections and, inside the third
one, a six item feature grid. Do not ask me anything, just build it.

Add the scroll-entry motion. Write `reveal.js` and `reveal.css` in the current
directory:

1. `reveal.css` holds the hidden and revealed states, the transition duration and
   the easing curve, plus the per item cascade delay for the six grid items
2. `reveal.js` holds the mechanism that flips a section from hidden to revealed
   when it comes into view

Then in your reply, paste the transition declaration from `reveal.css` and the
first six lines of `reveal.js`, and say in one sentence which browser API does
the detecting.
