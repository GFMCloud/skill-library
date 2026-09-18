### Steelman Y

Y's candidate is small, legible, and cleanly decomposed: one skill defines the format, two thin slash commands (`/handoff`, `/pickup`) trigger SAVE and RESUME modes. It has genuinely useful behaviors not mirrored in X: an explicit emergency-fallback procedure (KEEP/SUMMARIZE/DROP) for when auto-compact fires before a handoff is saved, bilingual trigger phrases, a "today's file, same topic → update don't duplicate" rule, and an offer to promote durable facts into a separate `MEMORY.md`. Both modes are cheap: SAVE writes an adaptive, section-skippable file; RESUME explicitly says "Read only that file. Do not load the history of old sessions," and ends with a mandatory "wait for confirmation before moving on" — a genuine stop-point before further work. It asks nothing of the environment beyond a writable directory and optionally `git`/`ls`.

### Steelman X

X's single item does the same job as Y's three but ties "done" to something the agent cannot fake: a Typed Claims block where every `expected` value must be captured from actually running the `check` command at write time ("Zero typed claims are accepted from the document alone"), and a resume flow that mechanically re-runs each check against the live artifact, producing a discrepancy table and treating any mismatch as a hard stop ("never silently correct"). This is the executed-evidence bar behavior built directly into the artifact format, not just described in prose — and it's backed by an actual enforcement script (`check-claims.py`, exit 1 on mismatch) with its own fixture-driven test suite (match/mismatch/stale cases) and evals. It also explicitly separates "unverified by design" claims from verified ones, matching the "say what was and wasn't checked" bar behavior almost verbatim.

### Scores

| Criterion | Y | X |
|---|---|---|
| Fit with the bar | 2 — no item contradicts the three behaviors, but support is partial: SAVE mode has "no stop/plan step before writing" and RESUME's reality check is "optional/light," per Y's own per-item fit notes. | 3 — report states resume is "explicitly sequenced to run before summarizing... or doing requested work," done-ness is tied to re-running checks, and discrepancies are surfaced, not hidden; report finds "no conflicting lines." |
| Enforcement mechanism | 0 — report states plainly "Prose only. No executable check, script, or hook; nothing blocks, warns, or exits non-zero" for all three items. | 3 — `check-claims.py` "exits 1 on any checkable mismatch, 0 if all match" and `fixtures/run-fixtures.sh` "asserts the expected exit codes... itself exiting non-zero if any assertion fails." |
| Context cost | 2 — 3 small on-demand items; RESUME explicitly restricts loading to one file, and output is capped at "~3 lines." | 2 — one on-demand skill, but its own template is denser (work-type detection, typed-claims YAML, discrepancy table, three-sentence status); neither report gives token/line counts, so this is a rough parity call. |
| Maintenance burden | 3 — report says "None named as runtime dependencies," with `git`/`ls` only optional. | 1 — report says `check-claims.py` "imports `yaml` and errors with an install instruction if missing," i.e., a dependency not guaranteed present. |
| Specificity | 2 — concrete file/frontmatter format and a KEEP/SUMMARIZE/DROP emergency checklist, but resume verification is only "light"/"optional." | 3 — concrete claim schema, exit codes, discrepancy-table format, explicit stop condition ("a mismatch means stop and ask, never silently correct"), and three tested fixture scenarios. |

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-c238a6db | FRAGMENT -> item-57dd6a97 | Core save/resume format is outclassed by item-57dd6a97's mechanized verification, but its auto-compact emergency-fallback (KEEP/SUMMARIZE/DROP) and MEMORY.md-promotion prompt are gaps not present in item-57dd6a97. |
| item-e0eb292d | REDUNDANT item-57dd6a97 | Pure trigger wrapper delegating entirely to item-c238a6db's format with no independent stop/verification content; item-57dd6a97 already triggers on phrases like "handoff" without needing a separate command file. |
| item-5fc81ea9 | REDUNDANT item-57dd6a97 | Trigger wrapper for resume with only a "light"/optional reality check; item-57dd6a97 covers the same trigger surface and performs a mandatory, mechanized re-check instead of an optional one. |
| item-57dd6a97 | SUPERSEDES item-c238a6db | Same core purpose (write/resume a handoff) but adds an executable enforcement script, tested fixtures, and a claim schema that ties "done" to re-run evidence rather than prose trust. |

### Deciding criteria

Enforcement mechanism and Fit with the bar (specifically executed-evidence) settled the rows: X's item ties resume to a mechanically re-run, exit-code-gated check, while Y's equivalent item relies on an optional, unenforced "light look at reality."

### What I could not assess from reading alone

Neither report shows the actual `check-claims.py` output or a Y handoff file being written/read in a live session, so I can't confirm the discrepancy-table/exit-code behavior fires correctly on a real mismatch, nor that Y's "light reality check" reliably happens rather than being skipped under context pressure. I also can't confirm whether X's PyYAML dependency is trivial or a real friction point in the target environment, or whether Y's bilingual/emergency-fallback logic actually triggers correctly under an auto-compact event — that would require observing a session hit the compaction boundary. I have no strong indication of either candidate's origin.
