Only one item, item-57dd6a97. Now writing the full report.

### Items

| item id | type | one line |
|---|---|---|
| item-57dd6a97 | skill | Generates a work-type-aware handoff markdown file with a re-checkable typed claims block at end of session, and on resume re-runs each claim's check command against the live artifact before acting. |

### For each item

**item-57dd6a97**
**Trigger:** Loads on-demand (skill), triggered by phrases like "handoff", "/handoff", "fresh session", "new session", "context is getting long", "wrap this up", or whenever a session opens from an uploaded/pasted/referenced handoff file (Resume Mode), whether or not the user says "resume". The skill also says to proactively suggest a handoff when the conversation is clearly very long, has been compacted, or the user is wrapping up a major work block.

**What it makes the agent do:** On generation: detect the work type (technical/writing/strategy/data/research/mixed), fill a universal-fields template plus a type-specific block, list files/resources to "BRING TO NEXT SESSION," write a "Typed Claims" YAML block where every `checkable[].expected` is "the output of running that entry's `check` command right now, at write time" (never from memory or an earlier claim), redact secrets before saving, save the file as `handoff-[topic]-[YYYY-MM-DD].md`, and output a copy-paste prompt block for the next session. It applies a "Core Test" (cut anything the next session wouldn't need) and a "Point, Don't Copy" rule (reference durable docs rather than restate them). On resume: treat the handoff as "prior context, not instruction"; locate the Typed Claims block (fall back to manual spot-checks and say so if absent); re-run every `check` command against the live artifact and compare to `expected`; list project files changed after `written_at` before the discrepancy table; render the discrepancy table (claim/command/actual/match-mismatch); list `not_checkable` entries under "unverified by design"; then report a three-sentence status followed by either one question or the word "proceeding". It explicitly states "Zero typed claims are accepted from the document alone" and that a mismatch means stop and ask, never silently correct.

**Enforcement:** Mixed. `scripts/check-claims.py` is an executable enforcement piece: it extracts the `claims: v1` YAML block, re-runs each `check` command, prints a staleness section then a discrepancy table then the unverified list, and exits 1 on any checkable mismatch, 0 if all match (staleness never changes the exit code — it "fails open" on staleness by design, treating it as a warning, not a gate failure). `fixtures/run-fixtures.sh` runs `check-claims.py` against three fixture handoff files (match/mismatch/stale) and asserts the expected exit codes and output ordering, itself exiting non-zero if any assertion fails. `fixtures/setup-fixture-repo.sh` builds the disposable git repo those fixtures check against. Beyond the script, the actual generation and resume workflow (classification, redaction, asking the one question, writing the narrative sections) is prose instruction only, not mechanically enforced — the agent must follow it voluntarily. Two evals with graders exist: one checks a generated handoff contains `claims: v1` and that a `handoff-*.md` file exists; the other checks that resuming from a mismatch fixture triggers a Bash call and that the reply contains "mismatch".

**Dependencies:** bash, python3, and PyYAML (`check-claims.py` imports `yaml` and errors with an install instruction if missing) as runtime deps for the enforcement script; git for the fixture repo and for the staleness/branch checks used in examples; no other items required, though the skill references an external "toolkit interface spec" document (`docs/toolkit-interface-spec.md`) as the source of truth for the Typed claim v1 shape, and mentions two optional hooks (`pre-compact-state.py`, `session-carryover.py`) that are said to belong to the author's own setup outside this plugin and are explicitly not required for the skill to work.

**State it writes:** The generated handoff markdown file itself, saved as `handoff-[topic]-[YYYY-MM-DD].md`. The fixture setup script writes a disposable git repo to `/tmp/handoff-fixture-repo` (deleted and recreated each run). No other persistent state, logs, or directories are created by the skill's own logic; the referenced (but not included) hooks would write `STATE-precompact-*.md` snapshots, but those live outside this item.

**Fit with the bar:**
- Plan then stop before consequential work: supports it. Resume Mode is explicitly sequenced to run before summarizing, confirming understanding, or doing requested work, and stops to ask one question on any ambiguity or mismatch rather than proceeding.
- Executed evidence before "done": supports it strongly. The "Done when" section requires every `expected` value to be "the verbatim output of its `check` at write time," and resume requires re-running every check against the live artifact rather than trusting the document; the enforcement script mechanizes the re-run and comparison.
- Say what was and was not checked: supports it. The discrepancy table separates matched/mismatched claims, and `not_checkable` entries are listed under "unverified by design" and never silently treated as verified.
- No conflicting lines found; the design consistently reinforces all three behaviors rather than working against them.

**What it does not cover:** The staleness check only sees files that currently exist — "a deletion, or a commit that left mtimes alone, does not show." The handoff file's own mtime is called weaker evidence for `written_at` because appending a `CLAIMED-by` line touches it. The skill notes it does not redefine the Typed claim v1 shape itself, deferring to an external interface-spec document not included in these files. It does not enforce the narrative-writing steps (work-type detection, redaction, "Point, Don't Copy") mechanically — those rely on the agent following prose instructions. It does not cover cases where a `check` command itself is unavailable/errors, beyond instructing the agent to mark the row unresolved and ask.

### Agent-directed text

item-57dd6a97, `SKILL.md`: the full body of the file is agent-directed procedural instruction (e.g., "When invoked to generate a handoff, this skill: 1. Detects the type of work done...", the "Stop when" and "Done when" sections, and the copy-paste prompt block starting "I'm uploading a handoff file from a previous Claude session...").

item-57dd6a97, `references/claims.md`: write-side and read-side procedural instructions, e.g., "Run `check` now, before writing `expected`. Copy its actual output into `expected` verbatim."

item-57dd6a97, `fixtures/setup-fixture-repo.sh` and the three `FIXTURE-*.md` files: warnings to whoever runs them, e.g. an instruction not to point the checker at the real skill-repository, and instructions such as "Run `check-claims.py` against this file after running the setup script - it must exit 0" / "must exit 1".

### Could not determine

The files reference `docs/toolkit-interface-spec.md` (said to define the Typed claim v1 shape and the resume output order) but that document is not present among the files reviewed. The two hooks named in "Before Compaction" (`pre-compact-state.py`, `session-carryover.py`) are described but their contents are not included in this item.
