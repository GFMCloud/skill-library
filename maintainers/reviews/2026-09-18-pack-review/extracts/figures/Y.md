### Items

| id | type | one line |
| --- | --- | --- |
| item-95409a14 | skill | Guidance and code for building publication-quality matplotlib/TikZ figures (learning curves, scaling laws, benchmark/ablation comparisons, Pareto fronts, heatmaps/confusion matrices, method diagrams), backed by a shared style module and a TikZ preamble. |

### For each item

**item-95409a14**

**Trigger:** Loads on-demand — its frontmatter description says to use it "whenever you plot, chart, or visualize results, add a figure to a paper or report, or one looks unpolished; then read one reference." It is not always-on; the top-level `SKILL.md` (216 lines, 56-word description) is the entry point, and it directs the agent to read exactly one of six per-figure-type reference files depending on the question the figure answers.

**What it makes the agent do:** A numbered list of "non-negotiables" — build at the exact final printed column/text/wide width and never rescale after the fact; export vector PDF+SVG, never a rasterized plot; source every plotted number from a logged run ("Every number comes from a run… never plot a remembered, rounded, or plausible number"); no `ax.set_title` (the caption is the title); show a seeds-uncertainty band or explicitly write "single seed"; label axes with units; use the module's colorblind/greyscale-safe palette, never `jet`/`rainbow`/`hsv`; use a fixed sans-serif font stack. It also prescribes where the output file goes and how it must be cited (`figs/` for a paper vs. an artifacts-directory folder for a report, with matching citation tag), a specific caption structure and word-count target, multi-panel composition rules (panel letters, shared axes, one legend), and a pre-handoff checklist ending in "Read the audit line `save()` prints… `clean` is the bar; anything else is a defect to fix, not a warning to note and move past."

**Enforcement:** Executable piece is `assets/orx_figstyle.py`. Its `save()` function runs an `_audit()` (and `_text_collisions()`) that checks font embedding type, whether a real publication font resolved, whether the canvas width matches a known column width, stray axes titles, missing axis labels, text below a 5pt floor, and overlapping/off-canvas text. On finding problems it prints them to stderr with a "FIGURE AUDIT … problem(s) — fix before using" line; on none, it prints "clean." It never raises or returns a non-zero exit — the code comment states the reasoning explicitly: "Printed, not raised: a hard failure mid-analysis loses the figure, but a silent pass is how an unpublishable figure reaches the paper." So it fails open: the figure is always written and saved regardless of audit result: enforcement is advisory text plus a printed report, not a hard gate.

**Dependencies:** python3; matplotlib and numpy (via `uv run --no-project --with matplotlib --with numpy`); gh (per the given facts, though not visibly invoked in the file text itself); a TikZ/LaTeX toolchain for the diagram path, compiled with `-no-shell-escape` (so `\tikzexternalize`, pgfplots externalization, and `minted` are stated as unavailable); an external CLI invoked as `orx` for vendoring assets (`orx skill …`) and for pulling metrics (`orx logs`); references to companion modules not included here (evidence/logging module, a reports module, and a paper/table-formatting module).

**State it writes:** `figs/<name>.pdf` and `figs/<name>.svg` (or an artifacts-directory equivalent for reports), a vendored copy of the style module (`figs/orx_figstyle.py`), a vendored `.tex` copy of the TikZ preamble for diagrams (`figs/method.tex` → `figs/method.pdf`), and audit findings printed to stderr only (not persisted to a file).

**Fit with the bar:**
- *Plan then stop before consequential work:* partial support in one narrow case — it tells the agent not to change the environment unilaterally: "say so when you hand the figure over rather than installing fonts, which is a change to the environment you should ask about first." It does not otherwise instruct pausing for approval before generating figures or writing files.
- *Executed evidence before "done":* strong support — "Every number comes from a run… never plot a remembered, rounded, or plausible number, and never leave synthetic demo data in a script that ships," plus a closing checklist item "The script reruns from scratch and reproduces the same file."
- *Say what was and was not checked:* strong support — repeated instructions to state seed counts, smoothing, normalization, excluded points, and truncated/zoomed axes in the caption, and to flag machine-level audit findings (e.g. missing font) rather than silently fixing or hiding them.

**What it does not cover:** No instruction to pause for user confirmation before generating or overwriting figures generally (only for the font-install edge case). No mechanism that blocks a "dirty" audit result from being handed over — it relies on the agent choosing to read and act on the printed warnings. Does not cover statistical validity of the underlying experiment (only how to display uncertainty once computed), non-figure content, or what happens if the external `orx` CLI or LaTeX/TikZ toolchain is unavailable beyond one line about reading a reference directly if it "cannot be read."

### Agent-directed text

none

### Could not determine

What the external `orx` CLI is or does beyond the invocations quoted in the files (`orx skill …`, `orx logs`); the contents of the referenced companion modules ("evidence" module for `orx logs`, "reports" module for artifacts-directory conventions, "paper" module for table/compilation handling); the "session playbook's Python policy" the skill tells the agent to follow; where or how `gh` is actually used by this item (listed as a runtime dependency but not referenced in any file's visible text); the definition/location of the "artifacts directory" mentioned as one of the two valid figure destinations.
