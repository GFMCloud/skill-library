# [Deck Name] - Build Plan

Working doc for building the deck. Pipeline, structure, chart split, and step count. The blueprint is the source of truth for all slide content.

## What we're building

[One [deck format], [N] slides across [M] sections. For modular: which sections always run vs are pulled.] Designed in Claude Design, converted to native editable PowerPoint with the cd-to-pptx skill, then maintained natively in PowerPoint.

| Section | Name | Slides |
|---|---|---|
| [N] | [name] | [count] |

Total: [N] slides.

## Folder structure

```
[Deck Build Folder]/
  00_project_docs/
    [deck]-blueprint-v[N].md      <- canonical content source
    BUILD_PLAN.md                  <- this file
    BUILD_STATUS.md                <- running tracker
    design-spec.md                 <- design pattern reference
    layout-map.html                <- visual section/slide map
  design_system/
    fonts/   <- deck font TTFs (from Claude Design export)
    logos/   <- official logo PNGs
  deck_export/
    [deck]-print.html              <- Claude Design deck export
    [deck].pdf                     <- reference PDF (cd-to-pptx ground truth)
  build_output/
    <YourOrg>_[Deck]_v1.pptx       <- conversion output, versioned
```

## Build sequence

1. **Phase 1 - validate the pipeline on the opener section.** Build the opener section in Claude Design (Prompt A), review, then trial-convert just that section with cd-to-pptx and open it in real PowerPoint. Confirm font embedded, chrome positioned, sizing correct. This de-risks the whole run before more slides are built on the template.
2. **Phase 2 - build remaining sections.** Run Prompt B per section, pulling copy from the blueprint. Approve each against the opener for visual consistency.
3. **Phase 3 - convert once.** After all sections are exported, run the cd-to-pptx batch (Prompt C). Merge section PPTXs into one master with python-pptx (use the opener as the base file; don't use PowerPoint's Reuse Slides - it corrupts the theme).
4. **Phase 4 - finish.** Hand-build the data visuals into their placeholder boxes. Final review.
5. **Phase 5 - maintain.** Edit the PPTX natively. Only frozen PNG diagrams round-trip back to Claude Design.

## Chart handling (the split)

See chart-handling.md for the decision logic. Categorize every visual/diagram slide:

**Native placeholders - build by hand after conversion:**
- [slide] - [what it is]

**Frozen PNG embed - rasterize from HTML:**
- [slide] - [what it is]

**Native auto-build - cd-to-pptx builds as editable elements:**
- [slide] - [what it is]

## Manual step count (honest)

- Pipeline validation: [X] steps
- Final conversion: [X] steps
- Chart finishing: [N] visuals by hand - heaviest is [which]. Budget [time].
- Final review: 1 pass

[Note where the weight is concentrated so there are no surprises.]
