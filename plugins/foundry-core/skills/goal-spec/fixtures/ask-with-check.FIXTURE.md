FIXTURE — an ask with a runnable check, used to prove goal-spec's normal
path produces a filled Goal block v1 with a recorded baseline.

Ask (verbatim, as it would be given to goal-spec):

> get the homepage lighthouse scores up

Expected goal-spec behavior: classify as `measurable` (Lighthouse scores are
a command's output), name the check
(`npx lhci collect --url=<url> && node scripts/lh-scores.js`), run it once to
record `baseline`, and produce the complete Goal block v1 in
goal-block-complete.FIXTURE.yaml. See references/goal-block.md for the
field-by-field walkthrough of this exact example.
