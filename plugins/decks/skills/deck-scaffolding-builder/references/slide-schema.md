# Slide Schema

Every slide in a blueprint is specified with the same five fields, then its copy blocks. This is the part that drifts when blueprints get rebuilt freehand - enforce it. A slide missing a field is a slide that hasn't been thought through.

## The five fields

For each slide, fill all five:

**One thing it says** - the single point. If you can't write it in one sentence, the slide is doing too much. One idea per slide.

**Act differently** - what this slide changes in the buyer's head. Does it reframe the conversation, build recognition, remove an objection, make the ask? If the answer is "it presents information," the slide is probably filler. Strong slides earn a "yes - because [specific shift]."

**5-second grasp** - can the core land in five seconds? Answer yes / partial / no, and say why. Headline and opener slides should be yes. Depth slides can be partial or no by design - that's appropriate when the slide is built to be read, not presented. The point is to make the call consciously, not to make every slide fast.

**Builds confidence** - does this slide make the buyer trust the seller more? Tone-setter / yes / strongly / not yet (but earns the next slide). Specificity builds confidence; generic capability lists don't.

**Copy density** - headline slide (minimal, presenter carries) or self-service depth slide (more copy, reads without a presenter) or transitional (in between). This field drives the layout choice and must match the slide's position - front of a section runs punchy, back of a section runs deep.

## Copy blocks

Below the five fields, write the actual copy the slide will use. Don't describe the copy - write it. Common blocks:

- **Lead copy** - the headline and/or opening line, written verbatim.
- **Supporting copy** - the recognition layer or sub-head under the headline.
- **Element copy / Row copy / Card copy / Panel copy** - for multi-element slides, the copy for each card, row, or panel, labeled.
- **Scenario copy** - for pattern-recognition slides, the named archetypes with their recognition descriptions.
- **Footer** - the closing line or caveat if the slide has one.

Write copy as it will appear. The whole value of a blueprint is that downstream the builder uses the copy as written and doesn't rewrite it. Copy that's only described gets reinvented - and reinvented copy drifts off-voice.

## Example (abbreviated, from a real practice deck)

```
### Slide 2.8 - FinOps Assessment: the entry point
- One thing it says: One week, read-only access - at the end you know exactly where the waste is, what it costs, and what fixing it looks like.
- Act differently: Strongly yes - converts interest into a concrete next step. Value framing does the work, not price framing.
- 5-second grasp: Partial - three-phase approach plus deliverables plus trust pills takes time. Appropriate for a CTA slide.
- Builds confidence: Closes the section strongly. A sample report mockup with a real savings number makes the output feel real.
- Copy density: Self-service depth slide.

Lead copy: "One week. Read-only. At the end, you know exactly where the waste is and what it would take to get it back. Most environments we assess surface $500K to $2M in savings opportunity in the first pass."
Element copy: [three-phase approach - Inform & Analyze, Optimize & Recommend, Operate & Roadmap]
Footer note: Do not use the word "complimentary" - frame around the output, not the cost.
```

## Section-level header

Each section opens with a one-line purpose note ("*For customers where spend is growing faster than understanding*"). For modular decks, also note whether the section always runs or is pulled.

## Blueprint changelog header

Every blueprint carries a version header at the top: version number, date, and a dated summary of what changed from the prior version. When iterating, append to this - don't erase the history. It's how you track what moved between revisions.
