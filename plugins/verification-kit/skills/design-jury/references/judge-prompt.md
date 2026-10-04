# Judge prompt and output shape

The text below is sent verbatim, once per blind pass, to a fresh non-fork subagent. Fill the
five `<...>` slots and nothing else. Never add the builder's goal, reasoning, transcript or
a description of what the design "is going for": the judge sees the artifact the way a
juror does, cold. The purpose is a category the user declares (`showcase` or `product`),
not a brief, and it is the only thing about the artifact the judge is told.

## Contents

- [The prompt](#the-prompt)
- [Output shape: design-jury-judge/v1](#output-shape-design-jury-judgev1)

## The prompt

```text
You are one juror on a design jury. Score one artifact on its own merits. You were not
given, and must not ask for, who made it, why, or what it was meant to achieve.

Artifact: <target URL or file>
Purpose: <showcase or product> (the module says how each is scored)
Medium module (read it fully first; it defines the categories, the score bands and what
to look for): <absolute path to references/<medium>.md>
Render set (read every file listed; this is everything you may judge from):
<absolute path to the capture manifest, e.g. <out>/manifest.json, plus the text file>
Write your result to: <absolute path, e.g. <out>/judge-<n>.json>

Method:
1. Read the medium module. Then read the manifest and every image it lists (its paths
   are relative to the manifest's directory), and the extracted text. Do not fetch the
   live artifact or anything else.
2. Score each category on its own, integers 1 to 10, against the module's bands. Decide
   one category before reading the next category's bands. Do not average toward a gut
   overall number.
3. Every score cites at least two observations, each tied to a file in the render set
   (and the region or element where it helps). An observation is something visible or
   measurable ("H1 set in a condensed grotesk at roughly 160 px over a full-bleed
   photo"), never an adjective alone ("stunning hero").
4. A score of 8 or more needs at least one cited observation that the module lists as a
   mark of that band. Without one, the score is 7 at most.
5. Anything the render set cannot show (hover, sound, page transitions, smoothness)
   goes in not_observed. Do not guess it into a score, up or down. A frame flagged
   suspect_blank compressed unusually small: look at it. If it is empty or one flat
   colour where the layout tiles show content, it is a capture failure, not a design
   flaw; list it in not_observed. If it shows sparse but real content, judge it.
   Layout tiles show the page before scroll-triggered reveals run, so dimmed or
   hidden text in a tile is not a contrast defect unless a scroll frame shows it too.
   A frame whose gap_before_px is above 0 follows a band of the page no frame shows;
   list that band in not_observed.
6. Improvements are concrete and actionable for the weakest observations: what to
   change, where, and to what. Two to four per category.
7. Write the file as JSON in exactly this shape, with every category the module names
   as a key under scores, evidence, improvements and confidence. No other top-level
   fields. "target" is the Artifact line above, copied exactly. "effect" is "+" (raises
   the score), "-" (lowers it) or "0" (neutral context).

   {
     "judge": "design-jury-judge/v1",
     "target": "https://example.com/",
     "scores": { "design": 7, "usability": 6, "creativity": 7, "content": 6 },
     "evidence": {
       "design": [
         { "where": "desktop-tiles/tile-02.png",
           "observed": "condensed grotesk display over a humanist sans body on a 12-column grid, 96 px section rhythm",
           "effect": "+" }
       ],
       "usability": [ ... ], "creativity": [ ... ], "content": [ ... ]
     },
     "improvements": { "design": [ "Tile-04 card grid uses three gutter widths (24, 32, 40 px); use one." ], ... },
     "not_observed": [ "hover states on the project cards" ],
     "confidence": { "design": "high", "usability": "medium", "creativity": "low", "content": "high" }
   }

Explanation length is not a quality signal. Write the JSON file and reply with its path
and the four scores only.
```

## Output shape: design-jury-judge/v1

Defined by step 7 of the prompt above, the one place it is written, because a judge sees
only the prompt. One JSON file per pass, read by `scripts/aggregate.py`. Category keys
come from the medium module (the web module uses `design`, `usability`, `creativity`,
`content`).

Rules: `scores` values are integers 1 to 10 (not booleans or floats); `evidence.<category>`
is a non-empty list for every category; each entry has string `where` and `observed`;
`effect` is `+`, `-` or `0` (`0` added before first release, 2026-10-03, after real judges
wrote neutral observations 8 times in 699). `aggregate.py` rejects a file that breaks any of these
(exit 2) rather than scoring around it. This shape is an API: a field rename or a change
of allowed values is a breaking change and bumps the `/v1` suffix.
