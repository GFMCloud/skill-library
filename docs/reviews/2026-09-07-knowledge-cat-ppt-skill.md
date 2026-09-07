---
contract: v1
source: https://github.com/gnipbao/knowledge-cat-ppt-skill
type: skill-collection
pin: 889c3dc00b356607fa9af935eb807056c3394886
reviewed: 2026-09-07
verdict: HARVEST
recheck: n/a
applied: see the commit that adds this file (decks 0.2.2)
evidence: the commit that adds this file; scratch clean-room review and comparison did not survive the session
---

# knowledge-cat-ppt-skill

**Verdict:** HARVEST. One skill (383-line SKILL.md, 15 references, 14 standard-library scripts, three honest evidence packages) whose strongest mechanism, proving PPTX editability by OOXML object inspection and a reversible edit probe, beat cd-to-pptx's eyes-only check; the skill as a whole collides four ways on "make me a deck" and its image-first and chart-auto-build lanes contradict cd-to-pptx's "native shapes, never screenshots" non-negotiable.

**Ancestry:** none. Single upstream commit; its CHANGELOG credits ppt-master, guizang-ppt-skill, gpt-image2-ppt-skills, Anthropic's pptx skill, and academic-pptx-skill. Nothing names the decks plugin in either direction.

## What landed

- Row 1: PPTX editability gate. `check_pptx_editability.py`, `probe_pptx_editability.py`, `extract_pptx_text.py` vendored byte-identical (MIT) into `plugins/decks/skills/cd-to-pptx/scripts/`; new Step 2b in `cd-to-pptx/references/pptx-review-playbook.md`; one pointer sentence in `cd-to-pptx/SKILL.md` Step 5. Proven: both self-tests pass, the vendor's six-slide native deck passes with `--fail-on-image-only-slides --require-native-chart --require-native-table --require-notes` (exit 0), a deliberately built image-only deck fails the checker (exit 1, two errors) and the probe (`passed: false`).
- Row 3: ten named machine-made-slide tells added under checklist item 5 of `plugins/decks/skills/layout-critique/SKILL.md`.
- Row 4: P0/P1/P2 severity tiers added to Step 4 of `cd-to-pptx/references/pptx-review-playbook.md`, with a Step 2b failure as P0.
- decks plugin 0.2.1 to 0.2.2; CHANGELOG entry dated 2026-09-07.

## Row 2: ruled out by Graham, 2026-09-07

- Row 2: the HTML deck production contract (four required `data-*` attributes, 12-name layout registry, `validate_html_deck.py`, starter template) as a new `html-deck-builder` skill, effort M. Ruled out. The gap is real in the decks plugin, but visualize already owns HTML decks on this machine, and a second lane adds to the four-way routing collision. Three upstream defects would need fixing first: the ratio regex rejects the recipe's own `4:5`; `html-production-lock.md` points at a "Strategic Minimal" system that `html-visual-systems.md` names "Architectural Minimal"; sixty lines of "Surpass-Guizang" positioning would need stripping.

## What was declined, and why

- Template replication fidelity levels: no request shape here consumes it; revisit on a clone-this-template ask.
- Alternate narrative spines (academic, teaching, demo): decks serves the sales-deck genre.
- Engine routing, image-first recipes, style-prompt intake, 44-seed style library: image-first PPTX by default contradicts cd-to-pptx's top non-negotiable and no image-generation lane exists here.
- Story architecture and design systems (beyond the tells): redundant; deck-scaffolding-builder's copy-voice.md and design-system.md are checkable where these are generic.
- Deck-plan JSON schema and validator: the plugin has no JSON deck-plan intermediate.
- Native PPTX builder (`build_native_pptx.mjs`): requires `@oai/artifact-tool`, absent here, and auto-builds charts, which cd-to-pptx tried and abandoned.
- Benchmark gates, benchmark synthesis, open-source-product, repo checks, installer: author-facing.

## Flags

No agent-directed text or injection; the clean-room reviewer grepped eight patterns with zero matches. Two notes, neither acted on:
- `README.md:85` and `:99` recommend `install_skill.py --agent claude --force`; `--force` runs `shutil.rmtree` on any existing `~/.claude/skills/knowledge-cat-ppt-skill` (`scripts/install_skill.py:48`). Not run.
- `references/style-template-library.md` carries a "Surpass-Guizang Target" section aimed at a named third party inside a runtime file.

## Re-review trigger

The pin moving past 889c3dc with the three HTML-contract defects fixed, or Graham ruling row 2 in, or a request for an HTML deck lane that visualize does not cover.
