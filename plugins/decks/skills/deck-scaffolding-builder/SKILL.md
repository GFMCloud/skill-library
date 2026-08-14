---
name: deck-scaffolding-builder
description: Build the upstream planning scaffolding for a slide deck - the slide-by-slide content blueprint, design spec, layout map, low-fi wireframe, reusable Claude Design build prompts, and build plan. Use whenever the user wants to plan, blueprint, outline, structure, scaffold, or wireframe a deck before it gets built; create or update a "deck blueprint," "slide framework," "design spec," or "layout map"; restructure an existing deck into the standard template; or turn source material (notes, transcript, an old deck, a conversation) into a structured deck plan. Trigger on "blueprint this deck," "plan out a deck on," "scaffold a deck," or "wireframe a deck." This is the PLANNING layer only - it stops before the visual build and hands to Claude Design plus cd-to-pptx. It does NOT build finished slides; if the user wants the deck made now, defer to the build skills (pptx, Claude Design). If the ask is a single standalone architecture or flow diagram rather than a full deck plan, that's html-diagram, not this skill. Use it even when the user doesn't say "skill," as long as the goal is planning a deck before slides exist.
metadata:
  maturity: incubator
---

# Deck Blueprint Builder

## What this is for

Most deck work repeats the same upstream steps before anything gets built: write a slide-by-slide content blueprint, define the layout, iterate, then hand a structured spec to whoever builds the slides. This skill standardizes that scaffolding so every deck starts from the same template, visual system, and copy voice - and so the user's time goes to the content that's actually different (the customer's real situation, the copy that makes a buyer self-identify), not to re-deriving structure.

It produces planning artifacts, not finished slides. The pipeline:

```
[this skill] → spec docs (+ optional wireframe) → Claude Design (visual build) → cd-to-pptx (native PPTX) → maintain in PowerPoint
```

This skill owns the first box only. It builds visual output (a wireframe, or a chart mockup) ONLY when the user explicitly asks. Conversion is the `cd-to-pptx` skill's job - don't duplicate it.

## Scope line (important)

This is planning, not building. Fire for "blueprint / plan / scaffold / outline / wireframe a deck." Do NOT take over when the user wants the finished deck made now - that's `pptx` or Claude Design (or whatever asset-building skill the marketplace provides for a finished deliverable). When a request is ambiguous ("make me a deck on X"), produce the plan and offer to hand it to a build skill rather than silently building slides. The one exception: a low-fi wireframe or a chart mockup, when explicitly requested, because those are tweaking aids that feed the real build.

---

## Phase 1 - Intake (adaptive: light by default)

Pull answers from the conversation first - if we've been discussing the deck, most of this is already known; don't re-ask it. Ask only what's genuinely missing, as clickable options where possible (most users prefer picking over typing), always with a free-text path.

**Default (light) intake** - for a small or linear deck, you only need:
- Topic, audience, and what the audience should do or believe after seeing it
- Any reference material to ingest (see below)
- Which artifacts to produce and where to hand off

**Expand to full intake** only for a modular master deck (a reusable library) or when the user asks for the works. The extra questions: section list, which sections always run vs are pulled, mode mix per section, slide targets per section.

**Always ask about reference material:** any context files, markdown docs, prior blueprints, existing decks, brand docs, transcripts, or screenshots to use as reference? Read them before building - they anchor the content and may override defaults. A `.pptx` reference: read with the `pptx` skill. A PDF: read natively. If the user flags any content as carry-forward-verbatim (e.g. "keep Section 5 as-is"), record it in the blueprint's Locked Content list so the QA pass can verify it survived untouched.

**Artifacts to produce** (multi-select):
- Content blueprint - the slide-by-slide framework (the core; almost always yes)
- Design spec - per-deck visual treatment (mode mix, section accents, layout choices)
- Visual layout map - HTML section/slide overview for at-a-glance review
- Low-fi wireframe - HTML gray-box mockup for rough structural tweaking before Claude Design (only if asked)
- Build prompts - the reusable Claude Design prompts A/B/C/D, parameterized
- Build plan + status tracker - folder structure, build sequence, chart split, step count

**Handoff target:**
- Spec docs only - produce the docs and stop
- Claude Design build prompts - docs plus ready-to-paste prompts (the default pipeline)
- Wireframe - produce the low-fi HTML wireframe for tweaking, then hand to Claude Design

After intake, restate the config in one or two lines and confirm. Flag assumptions.

---

## Phase 2 - Build

Build only what was selected. Templates live in `assets/`; fill them, don't freeform. Read the matching reference file before each artifact.

**Content fill - how to handle copy** (this is the point of the skill): draft real copy from everything we've discussed and from the reference material. Where the input is thin - especially the customer-archetype / pattern-recognition slides that carry the deck - do NOT invent generic archetypes and pass them off as done. Instead drop a clearly-tagged marker:

```
[NEEDS YOUR INPUT: the real customer situation here - which specific failure pattern do you see in these accounts?]
```

This way the user edits real drafts and sees exactly where their input is required, instead of hunting for fabricated copy. When several markers cluster in one area (e.g. all three archetypes for a section are unknown), offer to run research first: "Want me to pull some general context on [topic] to fill these in before you take a pass?" Use `WebSearch` / `mcp__workspace__web_fetch`, or the `deep-research` skill for a deeper pull. Research informs the scaffolding; it doesn't replace the user's specific customer knowledge.

**Length discipline:** have a point of view. A presented deck that lands is usually ~10-20 slides; a modular pull-from library is longer by design because no one sees all of it at once. If a blueprint is bloating - multiple slides making the same point, a section that could be three slides running eight - say so and propose the cut. More slides feels more thorough and usually isn't.

**Order of operations** (dependencies flow downward):

1. **Content blueprint** first - the spine. Use `assets/blueprint-template.md`. Every slide gets the five-field schema from `references/slide-schema.md`. Copy follows `references/copy-voice.md`. For customer-facing copy, load a voice/tone skill if the project has one.
2. **Design spec** - use `assets/design-spec-template.md`. Read `references/design-system.md` and `references/layout-patterns.md`. Record only what varies per deck; point at the standard for palette/type/chrome.
3. **Visual layout map** - use `assets/layout-map-template.html`. Scannable section/slide grid, color-coded by slide type.
4. **Low-fi wireframe** (if asked) - use `assets/wireframe-template.html`. Gray-box 16:9 frames showing structure and real headlines where known, so the user can tweak arrangement before Claude Design builds the real thing. Keep it low fidelity on purpose - it's disposable.
5. **Build prompts** - from `references/build-prompts.md`, parameterized to this deck.
6. **Build plan + status tracker** - `assets/build-plan-template.md`, `assets/status-tracker-template.md`. Includes the chart split (`references/chart-handling.md`).

**Iteration:** expect heavy iteration on blueprints - that's the normal mode. When updating, preserve the changelog header (version + dated summary of what changed). Save as a new version, don't overwrite, unless told.

---

## Phase 3 - QA reconciliation (always run before handing back)

Report as a short punch list, not prose. Verify:

- **Slide count reconciles** - section map total matches actual count and any stated target.
- **Every slide schema-complete** - all five fields present. A missing field is a slide that isn't thought through.
- **Copy density matches slide type** - headline slides minimal, depth slides read without a presenter. A headline slide with paragraph copy is miscategorized.
- **Accent discipline** - one highlight color per slide, the highlight/scarcity token on the single most important element only.
- **No AI tells** - scan copy against the banned list (see `references/copy-voice.md`).
- **Input markers surfaced** - list every `[NEEDS YOUR INPUT]` marker so the user has a punch list of where to focus.
- **Locked content honored** - anything flagged carry-forward-verbatim is actually unchanged.
- **Length sane** - flag bloat against the right-sizing POV.
- **Chart split complete** - every visual/diagram slide categorized, if the build plan was produced.

For a large or high-stakes deck, run this pass as a subagent pinned to `model: sonnet` against the files for a fresh-eyes check.

---

## Output location and naming

Save to the deck's working folder (ask if unclear - never guess the path). Customer-facing: `<YourOrg>_<Customer>_<Doctype>.<ext>` (swap in the org name the user actually uses). Internal: descriptive kebab/snake_case. Version blueprints (`_v2`, `_v3`, or date); don't overwrite prior versions unless told.

---

## Reference files

- `references/slide-schema.md` - the five-field per-slide template and copy blocks. Read before any blueprint.
- `references/design-system.md` - two-mode system, font resolution, chrome, accent discipline. Points at the project's own brand kit or design tokens for exact palette/type/logos, if one exists.
- `references/copy-voice.md` - claim-style headlines, pattern-recognition framing. Points at a voice/tone skill for the universal voice rules and banned-word list, if the project has one.
- `references/layout-patterns.md` - the eight reusable body layouts (A-H), card anatomy, headline-vs-depth rules.
- `references/chart-handling.md` - the three-way visual split decision guide.
- `references/build-prompts.md` - the A/B/C/D Claude Design + cd-to-pptx prompt templates.

## Boundaries

- Plans decks; does not convert to PPTX (that's `cd-to-pptx`).
- Does not redefine the brand - use the project's own brand kit or design tokens if one exists; otherwise fall back to neutral, accessible defaults and say so.
- Does not own outbound voice rules - defer to whatever voice/tone skill the project has, if any; otherwise write in a plain, direct default voice.
- Builds visual output (wireframe, chart mockup) only when explicitly asked; never takes over a "build the finished deck" request.
