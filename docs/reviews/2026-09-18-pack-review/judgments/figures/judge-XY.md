### Steelman X

X gives a tight, dependency-free ruleset for the specific failure mode of "chart shipped to a business/deck audience that misleads or looks sloppy" — hero-color discipline, banned chart types (pie, dual y-axis), a declarative-headline annotation grammar, and PowerPoint-specific translation steps that most generic advice skips (get hex from the brand kit, delete the legend, add end-of-line labels). It ships two pure-stdlib scripts with no install footprint, and it explicitly instructs the agent to disclose when it's falling back to a default color palette rather than a real brand kit — a genuine, if narrow, instance of "say what was and wasn't checked." For a toolkit that needs to work with nothing but python3 already on the machine, this is about as low-friction as enforcement gets.

### Steelman Y

Y treats "trustworthy figure" as a reproducibility and honesty problem, not just a style problem: every plotted number must trace to a logged run, synthetic/demo data may never ship, and the closing checklist requires the script to rerun from scratch and reproduce the same file — that's executed evidence, not a self-administered checklist. Its audit isn't a side script the agent might remember to invoke; it's wired into the actual `save()` call in the shared style module, so every real save produces a printed pass/fail line the agent has to read. Captions are required to state seed counts, smoothing, normalization, exclusions, and truncated axes — exactly the "say what wasn't checked" transparency the bar wants, and applied broadly rather than to one edge case.

### Scores

| Criterion | X (item-4a425f59) | Y (item-95409a14) |
|---|---|---|
| Fit with the bar | 2 — no conflict with the three behaviors, but only narrowly touches #2/#3: disclosure is limited to the brand-color fallback case, and pre-flight checklist is "self-administered by the agent" (X.md L21-26). | 3 — actively reinforces #2 ("Every number comes from a run… never plot a remembered, rounded, or plausible number," checklist item "script reruns from scratch and reproduces the same file") and #3 (captions must state seeds/exclusions/truncated axes) (Y.md L23-24). |
| Enforcement mechanism | 1 — `annotate.py` is a separate, optional script disconnected from any rendering step ("no rendering... pure logic"), never invoked automatically, and silently swallows exceptions (`except Exception: pass`) (X.md L15, 26). | 2 — audit is built into the actual `save()` function used to write every figure and always prints a pass/fail line, but by explicit design "never raises or returns a non-zero exit" so it still doesn't block (Y.md L15). |
| Context cost | 2 — on-demand trigger is described, but the report gives no line/word count for the skill file itself to verify size. | 3 — report states concrete counted facts: "216 lines, 56-word description," entry point directs to reading exactly one of six reference files as needed (Y.md L11). |
| Maintenance burden | 3 — "python3 (standard library only)... no dependencies... no network," optional brand-kit file is the only external input (X.md L17). | 1 — requires matplotlib/numpy installed per-run via `uv run --with`, a LaTeX/TikZ toolchain with shell-escape explicitly disabled (some tools "stated as unavailable"), an external `orx` CLI, `gh` listed as a dependency but "not visibly invoked," and companion modules "not included here" (Y.md L17, 34). |
| Specificity | 3 — five numbered rules, seven-item pre-flight checklist, quantified audit deductions (25/10/4/1 points per severity) (X.md L13, 15). | 3 — numbered non-negotiables with concrete thresholds (5pt text floor, exact column width, panel-letter/shared-axis rules), plus specific audit checks (font embedding, canvas width, text collisions) (Y.md L13, 15). |

No 0s on "Fit with the bar" — neither candidate fails the slot.

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-4a425f59 | COMPLEMENT | Fills a gap in Y's set: deck/slide-specific guidance (PowerPoint hex-from-brand-kit workflow, slide-title-as-headline, legend deletion) that Y, being paper/report-focused with a LaTeX/TikZ path, does not address at all. |
| item-95409a14 | COMPLEMENT | Fills a gap in X's set: run-sourced number provenance, reproducibility checklisting ("script reruns from scratch and reproduces the same file"), and caption-level disclosure of seeds/exclusions/truncated axes, none of which X's rules touch — X's disclosure requirement is limited to the single brand-color-fallback case. |

### Deciding criteria

Maintenance burden and Fit with the bar (specifically the breadth of "say what was and wasn't checked" support) did the differentiating work — X wins on being dependency-free and immediately runnable, Y wins on having broad, mandatory-feeling transparency and reproducibility requirements baked into its actual output path.

### What I could not assess from reading alone

Whether either audit script is actually invoked by the agent in practice, versus sitting unused as both reports note it "fails open" and nothing forces a call to it — this needs a behavioral trace of a real chart/figure task to see if the agent reads and acts on the printed audit line or just proceeds. Also unverifiable from the reports: whether Y's `orx` CLI, `gh` dependency, and referenced companion modules (evidence/reports/paper) are reliably present in the target environment, since the report itself flags `gh` as listed but not visibly invoked and the companion modules as "not included here." I don't believe I can identify the source of either candidate from the content, and I haven't tried.
