### Steelman X

`item-57dd6a97` treats "done" as a verifiable claim, not a narrative. Every fact the next session needs to trust is written as a `check` command run at write time, and resume mode re-runs those same commands against the live artifact before the agent is allowed to act — this is the executed-evidence bar made mechanical rather than aspirational. The `check-claims.py` script plus three fixture files (match/mismatch/stale) with asserted exit codes is real enforcement infrastructure, not just an instruction the agent might follow: mismatches fail the check (`exit 1`), and the report states plainly that a mismatch means "stop and ask, never silently correct." The resume flow explicitly separates matched claims, mismatched claims, and `not_checkable` items into a discrepancy table, directly satisfying "say what was and was not checked." It also anticipates its own blind spots (deletions not caught by mtime checks, `written_at` being fragile) rather than glossing over them.

### Steelman Y

The `session-handoff` skill (`item-c238a6db`) and its two command wrappers are lightweight, dependency-free, and address a real failure mode X doesn't: what to do when context runs out *before* a handoff gets written. The KEEP/SUMMARIZE/DROP emergency-fallback procedure is a genuinely distinct, concrete piece of guidance about triage under context pressure. The design also has sensible discipline for keeping resumed sessions cheap — "Read only that file. Do not load the history of old sessions" — and pushes saving to happen at ~50-60% context rather than at the edge, which is a proactive habit X's report doesn't describe as explicitly. Splitting save and resume into separate slash commands (`/handoff`, `/pickup`) gives the user simple, guessable, narrow entry points rather than one large multi-mode skill.

### Scores

| Criterion | X (item-57dd6a97) | Y (item-c238a6db + e0eb292d + item-5fc81ea9) |
|---|---|---|
| Fit with the bar | **3** — Report states resume is "explicitly sequenced to run before summarizing... or doing requested work," requires re-running every check before acting, and separates matched/mismatched/unchecked claims; "no conflicting lines found." | **2** — Individual items give only "partial" support to each behavior (e.g. "SAVE mode has no comparable stop/plan step," "no explicit instruction to state what was not checked"), and `item-e0eb292d` is scored "ignore" on all three bar points in the report; nothing contradicts the bar, but nothing reinforces it strongly either. |
| Enforcement mechanism | **3** — `check-claims.py` is an executable script that "exits 1 on any checkable mismatch," and `fixtures/run-fixtures.sh` asserts expected exit codes/ordering, itself failing non-zero on mismatch. | **0** — All three items are stated as "Prose only. No executable check, script, or hook" (repeated verbatim for each of the three items in the report). |
| Context cost | **2** — Single on-demand skill, but with more surface described (main SKILL.md, `references/claims.md`, fixtures, eval graders); no line/word counts given in the report to size it precisely. | **2** — Also on-demand, split across three files (skill + two slim commands) so a resume-only invocation could load less; report gives no counts either, so this is a tie based on available facts. |
| Maintenance burden | **2** — Report says the enforcement script needs `python3` and `PyYAML`, and "errors with an install instruction if missing" — an extra dependency beyond what's certainly present; `git` needed only for fixtures. | **3** — Report states "None named as runtime dependencies," with `git`/`ls` only optional for a "light" reality check, "neither required to exist." |
| Specificity | **3** — Concrete YAML claim schema, a "Core Test," a "Point, Don't Copy" rule, an explicit line "Zero typed claims are accepted from the document alone," and named failure modes (mtime fragility, deletions not detected). | **2** — Concrete in places (fixed frontmatter fields, ✅/🔄/⛔ markers, "save at ~50-60% context," KEEP/SUMMARIZE/DROP fallback), but the bar-relevant steps (reality check, stop-and-confirm) are repeatedly described in the report as "light," "optional," or "partial." |

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-57dd6a97 | SUPERSEDES item-c238a6db | Same generate/resume scope, but backs "executed evidence" with a real exit-code-checked script and fixtures rather than a prose-only "light look at reality." |
| item-c238a6db | FRAGMENT -> item-57dd6a97 | Weaker overall (prose-only enforcement per report), but its auto-compact emergency-fallback procedure (KEEP/SUMMARIZE/DROP) and "save at ~50-60% context, not 90%" habit are not present in X's report and worth folding in. |
| item-e0eb292d | REDUNDANT item-57dd6a97 | X's skill already triggers save behavior on the phrase/command "/handoff" per its trigger list; the command adds only delegation with no independent enforcement or unique content, and the report scores it "ignore" on all three bar points. |
| item-5fc81ea9 | REDUNDANT item-57dd6a97 | X's resume mode already covers the equivalent trigger (uploaded/referenced handoff file) and does the verification work more rigorously (re-run checks vs. a "light look" reality check); the command adds no content the skill lacks. |

### Deciding criteria

Enforcement mechanism and fit with the bar settled the rows: X's item has an executable, exit-code-checked verifier backing the exact behaviors the bar requires, while Y's three items are explicitly prose-only and only partially support those same behaviors.

### What I could not assess from reading alone

Neither report gives word/line counts, so the context-cost comparison rests on described complexity rather than measured size — a behavioral test loading each candidate and checking actual token cost per invocation (generate vs. resume vs. idle) would settle this. I also could not verify from the reports whether X's `check-claims.py` gracefully handles a `check` command that itself errors versus one that just returns a wrong value, or whether Y's "light look at reality" step is ever actually skipped in practice — both would need a live run to observe. I did not attempt to infer where either candidate came from.
