---
name: design-jury
description: >-
  Score a visual design the way an award jury does and gate it: renders the
  artifact, runs three blind judge subagents that each score every category
  1-10 with cited evidence, takes the medians, and returns APPROVED only when
  every category meets its floor, with concrete per-category fixes and a
  Verdict object v1. The web module scores websites on the Awwwards
  categories (Design 40%, Usability 30%, Creativity 20%, Content 10%),
  calibrated against real jury scores. Use on "judge this design", "would
  this win an Awwwards", "score this site like Awwwards", "design review this
  page", "is this design good enough to ship", or before presenting a
  showcase site as done. Not for Lighthouse, link or accessibility audits
  (site-review), not for chart encoding (dataviz), and not yet for slides,
  PDFs or diagrams (web is the only medium module). Costs three judge
  subagent runs per review, each reading 15 to 30 images, plus a headless
  Chrome capture.
metadata:
  maturity: incubator
---

# design-jury

Renders a design, has three independent judges score it on a medium's jury categories,
and approves it only when every category clears its floor.

The skill is a shared core (this file) plus one module per medium in `references/`. The
core owns the method: render, blind passes, evidence rules, medians, floors, the verdict.
A module owns what is medium-specific: the categories and weights, the score bands, the
render recipe, the floors, and what it defers to. Only the web module exists:
[references/web.md](references/web.md).

## Method

1. **Pick the module and purpose.** Web is the only module. Purpose is `showcase` or
   `product` (definitions in the module). If the user did not say, ask once; a product
   page judged as a showcase fails Creativity by construction.
2. **Render.** Run the module's render recipe into a fresh output directory. For web:

   ```bash
   node scripts/capture.mjs <url-or-file> <out-dir>
   ```

   Exit 1 means a viewport produced no frames: stop and report the manifest's
   `failures`; never judge a partial render as if it were complete. Open one desktop
   tile and one mobile frame yourself to confirm the render shows the design, not a
   cookie wall, an error page or a login screen.
3. **Judge, three blind passes in parallel.** Spawn three non-fork subagents in one
   message, each with the prompt in [references/judge-prompt.md](references/judge-prompt.md)
   filled with the target, the purpose, the module path, the render set and its own
   output file (`judge-1.json` to `judge-3.json`). Rules for the spawn:
   - Never a fork, and never pass the builder's goal, transcript or reasoning. The
     judge sees renders and extracted text only; independence comes from what the
     subagent is given, not from telling it to ignore things.
   - Model: one that differs from the builder's. When Fable built the design, use a
     fresh non-fork Fable (ruled 2026-10-03). For a design no one in this session
     built, use `opus`. State the choice before spawning.
   - The judge does not fetch the live site. What it scores is what the render set
     shows.
4. **Aggregate and gate.**

   ```bash
   python3 scripts/aggregate.py references/floors-web.json <purpose> <out-dir> <out-dir>/judge-1.json <out-dir>/judge-2.json <out-dir>/judge-3.json
   ```

   Median per category is the score; max minus min is the spread. A spread above 2 marks
   the category UNSTABLE. APPROVED needs every median at or above its floor and no
   unstable category. The weighted overall is printed for information and never gates.
   Exit 0 APPROVED, 1 NOT APPROVED, 2 a malformed judge file (fix the file by re-running
   that pass, never by editing its scores).
5. **Report.** Give the user `report.md`: the score table, evidence per category, the
   deduplicated fixes, the not-observed list and the labels. Lead with the verdict and
   the categories below floor. `verdict.yaml` is the machine-readable result.

## Rules

- **Evidence or no score.** When a judge file has a category with no cited evidence,
  `aggregate.py` rejects it (exit 2), unless that pass is re-run, proven by the exit code.
- **8 or above needs a named mark.** A score of 8 or more must cite an observation the
  module lists as a mark of that band; otherwise the judge caps it at 7.
- **Not observed is never scored.** Hover, sound, transitions, frame rate, keyboard
  focus and reduced motion are absent from a headless render; they go in `not_observed`,
  never into a score, unless the module names a probe that observed them.
- **Never edit a judge's scores** to change a verdict. A verdict the user disagrees with
  is re-run with a new pass or argued in the report, not adjusted.
- **Fixtures are labelled.** Results on `fixtures/*.FIXTURE.html` are proofs that the
  gate fails, never findings about a real design.

## Known weaknesses

Stated beside the rule they qualify, per the library's authoring standard.

- **Screenshot blindness.** Motion, interaction and sound carry much of Creativity and
  part of Usability on award sites. The capture shows motion exists (ambient-motion
  check, motion libraries, canvases), not whether it is good. Creativity on a
  motion-led site is the least reliable score this skill gives.
- **Headless rendering.** Scroll-driven sites can render later scroll frames blank; the
  layout tiles cover the content but show it before scroll reveals run.
- **The judge is a model.** It can be gamed by a builder that writes to the rubric's
  words. The bands are written as observables, the judge never sees the builder's
  reasoning, and five calibration sites are held out from rubric tuning; none of that
  makes gaming impossible.
- **The calibration covers the top of the scale only.** Awwwards publishes jury scores
  for award winners (6.5 and up); nominee pages hide them. Below 6.5 the judge is proven
  only to fail labelled fixtures, not calibrated against human scores.
- **Fixes overlap.** `report.md` merges the three passes' fixes by exact text only, so
  the same fix can appear two or three times in different words. Read them as votes:
  a fix all three passes name is the strongest.
- **Measured ceiling (web, 2026-10-03, 26 live sites):** both labelled fixtures fail on
  every category; real Sites of the Day pass the showcase gate 10 times in 15, Honorable
  Mentions 2 in 5, unawarded nominees 3 in 6. Cross-tier ordering is 59% correct (chance
  50%). Within Sites of the Day the judge does no better than always answering 7, and on
  held-out sites it runs 0.63 low on Usability, which causes most false fails. It catches
  weak work; it does not rank good work. Full numbers:
  [references/calibration-web.md](references/calibration-web.md).

## Inputs

- The artifact: for web, a URL (including `http://localhost`) or a local HTML file.
- The purpose: `showcase` or `product`.
- Nothing about the builder's intent. If the user offers a brief, keep it out of the
  judge prompt; it may inform the report's framing, never the scores.

## Verify

Proof the gate works, re-runnable from the skill directory:

```bash
node scripts/capture.mjs fixtures/generic-template.FIXTURE.html <out>/generic
node scripts/capture.mjs fixtures/unusable-polish.FIXTURE.html <out>/unusable
```

then three judge passes on each and `aggregate.py` with purpose `showcase`. Pass means
exit 1 (NOT APPROVED) on both fixtures, with Design, Creativity and Content below floor
on the generic page and Usability below floor on the unusable one. The recorded runs are
in [references/calibration-web.md](references/calibration-web.md), including two real
Sites of the Day that pass.

## Done when

`report.md` and `verdict.yaml` exist in the output directory, every category has a median
from three passes with cited evidence, and the user has the verdict with the categories
below floor and their fixes.

## Stop when

- **The render fails.** `capture.mjs` exits 1 or 2, or the frames show a cookie wall,
  login, error page or bot check instead of the design: report what the render shows
  and stop; never judge it.
- **A pass cannot be made valid.** The same pass is rejected by `aggregate.py` twice:
  stop and report the rejection rather than aggregate two passes.
- **Still unstable after one re-run.** A category stays UNSTABLE after re-running the
  outlying pass once: report NOT APPROVED with the instability named; do not keep
  sampling until the numbers agree.
- **No module fits the medium.** A slide deck, PDF or diagram: say web is the only
  module and stop, rather than judging it with web bands.

## Output contract

- Produces a Verdict object v1 as defined in the toolkit interface spec
  (`maintainers/toolkit-interface-spec.md`, section 3) in `verdict.yaml`: `result: pass`
  only when APPROVED, one issue per category below floor or unstable. review-pair,
  bounded-loop and site-review consume it unchanged.
- Each judge pass writes `design-jury-judge/v1`, defined in
  [references/judge-prompt.md](references/judge-prompt.md). A field change is a breaking
  change and bumps the suffix.
- The capture writes `design-jury-capture/v1` (`manifest.json`), defined by
  `scripts/capture.mjs`.
