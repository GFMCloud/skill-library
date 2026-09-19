### Items

| id | type | one line |
|---|---|---|
| item-4a425f59 | skill | A skill that encodes chart-type selection, color discipline, and annotation rules so data slides/charts read as deliberate, plus two Python helper scripts (a chart-type recommender and a chart-spec linter/scorer) |

### For each item

**item-4a425f59**

**Trigger:** Loads on-demand, described as a skill invoked "whenever you're building a chart, graph, data slide, dashboard, or any deck slide that contains data," and also on phrases like "make this chart better," "clean up this graph," "this slide is too busy," "what chart should I use for this," "visualize this data," or whenever numbers are going onto a slide, even if the user doesn't say "chart." It states it is not for system/architecture diagrams with no numeric data.

**What it makes the agent do:** Apply "five rules" to every chart: (1) one hero color, everything else grey; (2) no rainbow/jet ramps, monotonic single-hue sequential scales, diverging only with a real zero; (3) pick chart type by question not habit (line for time, bar for categories, never pie, never dual y-axes, bars start at zero, small multiples past ~5 lines), guided by a selection table; (4) annotate like a sentence — declarative headline stating the takeaway, subtitle with unit/timeframe, source line, direct end-of-line labels instead of a legend, and mark the one inflection point; (5) make the takeaway readable at a glance, assuming Zoom screen-share or a printed leave-behind. For color, it says to use the project's brand kit/design tokens if one exists, otherwise a neutral accessible default, and to "say plainly to the user that you're using a default rather than a real brand palette." It gives PowerPoint-specific translation notes (get hex values from brand kit, use existing deck fonts, put headline in slide title or text box, add end-of-series labels and delete the legend). It ends with a seven-item "Pre-flight checklist" to confirm before a data slide ships, and a note that if the takeaway needs two questions, split the slide.

**Enforcement:** Mostly prose/checklist, not a hard gate. Two executable pieces exist: `scripts/chart_selector.py`, which is pure lookup logic returning a recommended chart type, rationale, and anti-pattern for a given question type and data shape (no dependencies, no rendering); and `scripts/annotate.py`, which audits a chart-spec dict against the rules and returns a severity-sorted issue list and a 0-100 score (deducting 25/10/4/1 points per critical/high/medium/low issue). Neither script blocks, warns, or exits non-zero on its own — they are described as things the agent may "run ... when you want a quick objective gut check," returning data for the agent to act on; nothing forces the agent to call them or to act on their output. Both fail open in the sense that they only report a score/list rather than halting any process, and `audit()` even catches and silently swallows exceptions from individual checks (`except Exception: pass`).

**Dependencies:** python3 (standard library only, per the scripts' own docstrings — "no dependencies," "no rendering, no network"); for the PowerPoint-specific advice, an implied python-pptx workflow is mentioned as "the common case," and an existing project brand kit/design tokens file is an optional dependency for color decisions.

**State it writes:** None. Both scripts are pure functions/CLIs that print JSON to stdout; no files, directories, or logs are created.

**Fit with the bar:**
- Plan then stop before consequential work: not addressed. The skill describes judgment rules and a pre-flight checklist to confirm before a slide "ships," but nothing requires stopping for user approval before producing or finalizing a chart; the checklist is self-administered by the agent.
- Executed evidence before "done": partially supported in spirit — `scripts/annotate.py` can produce an objective score/issue list for a chart spec — but nothing requires the agent to actually run it before declaring a chart finished; the text only says to run it "when you want a quick objective gut check."
- Say what was and was not checked: supported for one narrow case — the color rule explicitly instructs the agent to "say plainly to the user that you're using a default rather than a real brand palette" when no brand kit exists, and to "state that assumption." Beyond that specific disclosure, there's no general instruction to report what was or wasn't verified on a shipped chart.

**What it does not cover:** States it is not for system/architecture diagrams without numeric data. It provides no rendering step itself (explicitly "pure logic ... no rendering") and defers actual chart construction to whatever tool (e.g., python-pptx) is in use. It does not define brand hex values itself. It does not mandate that the linter/checklist actually be run — running it is optional/discretionary language ("if you want"), and there is no verification step confirming the pre-flight checklist was actually completed rather than just read.

### Agent-directed text
none

### Could not determine
The files reference a "python-pptx workflow" and an optional project "brand kit or design tokens" file, but neither is included in this item's contents.
