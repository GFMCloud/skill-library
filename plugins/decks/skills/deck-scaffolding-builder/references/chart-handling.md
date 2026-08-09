# Chart Handling

Every slide with a data visual or a complex diagram needs a build decision made at blueprint time, not build time. Deciding upfront saves rework downstream because it tells Claude Design and cd-to-pptx exactly how to treat each visual. There are three categories.

## 1. Native placeholder - build by hand after conversion

Data-driven visuals that get updated over time. cd-to-pptx leaves a pre-sized, labeled placeholder box; the visual is built by hand in PowerPoint after conversion so it stays editable.

Use when: the numbers will change, or the customer-specific data goes in later.

Examples from the AWS deck: stacked bar chart (cost trend), prioritization matrix (savings vs effort), live dashboard mock, sample report mockup, pricing figures.

## 2. Frozen PNG embed - rasterize from HTML

Complex CSS/SVG diagrams where visual fidelity matters more than editability. cd-to-pptx embeds the rendered visual as a PNG. The image is frozen - changing it means round-tripping back to Claude Design.

Use when: the diagram has intricate SVG nodes/connectors, a load-bearing color progression, or custom path geometry that won't survive being rebuilt as native shapes.

Examples: a five-step framework flow with SVG nodes/connectors, a stacked color-coded levers diagram, a phased wave diagram with gate markers.

## 3. Native auto-build - cd-to-pptx builds as editable elements

Text-based slides that look visual but are really structured text - numbered lists, two-column contrasts, styled cards. cd-to-pptx builds these as regular editable PowerPoint elements. No special handling.

Use when: the slide is text and boxes following one of the standard layouts (B/C/D/F). Most "visual-looking" slides are actually this. Default here unless there's real visual complexity justifying category 1 or 2.

## How to decide

```
Is the visual data that will change or get customer-specific numbers later?
├── YES → Native placeholder (category 1)
└── NO → Is it an intricate CSS/SVG diagram where fidelity > editability?
         ├── YES → Frozen PNG (category 2)
         └── NO  → Native auto-build (category 3)
```

When in doubt, prefer category 3 (editable) - PNGs are expensive to change. Only escalate to PNG when a native rebuild would visibly degrade the diagram. Tables and text columns are always category 3 - they convert automatically.

## Recording the split

In the build plan, list each visual/diagram slide under its category. This list is the instruction set for the cd-to-pptx run and the post-conversion hand-finishing work. Note which placeholder slides are heaviest (e.g. a dashboard mock) so the manual build time is budgeted honestly.
