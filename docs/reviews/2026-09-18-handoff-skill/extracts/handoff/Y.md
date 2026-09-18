### Items

| item id | type | what it does |
|---|---|---|
| item-c238a6db | skill | Defines a "session-handoff" skill with SAVE and RESUME modes: write a curated handoff file to `session-logs/` at end of session, and read the newest such file to resume in a clean window. |
| item-e0eb292d | command | Slash command that invokes the session-handoff skill in SAVE mode to write/update today's handoff file. |
| item-5fc81ea9 | command | Slash command that invokes the session-handoff skill in RESUME mode to find and read the newest handoff file. |

### For each item

**item-c238a6db**
**Trigger:** Loads on-demand. Description says to use it when the user wants to "wrap up the session", "save a handoff", "summarize the session to a file", "start from the last session", "continue from the previous window", or types `/handoff` or `/pickup`, plus a list of trigger words in English and Polish.
**What it makes the agent do:** In SAVE mode: create `session-logs/` if missing, write a file named `YYYY-MM-DD-slug.md` with fixed frontmatter (`kind: handoff`, `date`, `topic`, `status`) and adaptive sections (Summary, Key takeaways/decisions, State with ✅/🔄/⛔ markers, Artifacts, Next step, What NOT to do); "Skip sections that do not fit"; if today's file on the same topic exists, "update it instead of creating a second one"; save "at ~50-60% context usage, not at 90%"; "Do not interrupt a working implementation halfway." In RESUME mode: find the newest `kind: handoff` file, "Read only that file. Do not load the history of old sessions," do a light reality check (`git status`/`git diff --stat` or `ls`), then "Summarize in ~3 lines: where we are → next step → what to avoid. Wait for confirmation before moving on." Also describes an emergency fallback procedure for when auto-compact happens before a handoff is saved (KEEP/SUMMARIZE/DROP lists), ending with "immediately save `/handoff` to persist it on disk."
**Enforcement:** Prose only. No executable check, script, or hook; nothing blocks, warns, or exits non-zero if the agent skips a step (e.g., skips the reality check or writes to the wrong path).
**Dependencies:** None named as runtime dependencies. Assumes a filesystem with a writable project root and, for the reality check, optionally `git` (for code projects) or a plain directory listing (for content projects); neither is required to exist.
**State it writes:** Markdown files under `session-logs/<YYYY-MM-DD-slug>.md` in the project root; distinguishes handoff files from other logs via `kind: handoff` frontmatter. Also may prompt to add durable facts to a separate persistent-memory file (e.g. `MEMORY.md`), described but not created by this item itself.
**Fit with the bar:**
- Plan then stop before consequential work: partial support — RESUME mode ends with "Summarize in ~3 lines... Wait for confirmation before moving on," which is a stop-before-proceeding instruction, but SAVE mode has no comparable stop/plan step before writing.
- Executed evidence before "done": partial — RESUME mode calls for a "light look at reality" (`git status`/`git diff --stat` or `ls`) to verify the file matches reality, but this is optional/light and not required before declaring anything done; SAVE mode has no verification that the saved file is accurate.
- Say what was and was not checked: partial — the ~3-line resume summary ("where we are → next step → what to avoid") implicitly covers state and gaps, and "What NOT to do" records rejected approaches, but there's no explicit instruction to state what was *not* checked or verified.
**What it does not cover:** No guidance on multi-file or multi-topic projects beyond "today's file on the same topic"; no versioning/conflict handling if two sessions write concurrently; no instruction on what to do if `session-logs/` contains malformed or missing frontmatter; no enforcement that the reality check actually happened.

**item-e0eb292d**
**Trigger:** Loads on-demand, on the `/handoff` command (or equivalent slash invocation); not always on.
**What it makes the agent do:** Invoke the session-handoff skill in SAVE mode; "write or update the handoff file for the current session in `session-logs/`," following the skill's format; check whether today's handoff on the same topic exists and "update it instead of creating a second one"; "If a durable fact came up in the session..., offer to add it to persistent memory"; accepts an optional topic/slug argument.
**Enforcement:** Prose only, delegating entirely to the referenced skill's instructions. No executable enforcement piece.
**Dependencies:** Depends on the session-handoff skill (item-c238a6db) for the actual format/rules; no runtimes, CLIs, or services named directly.
**State it writes:** Same as the skill: a file in `session-logs/` following the `YYYY-MM-DD-slug.md` naming and `kind: handoff` frontmatter convention (writing is delegated, not separately specified here).
**Fit with the bar:**
- Plan then stop before consequential work: ignore — the command runs straight to writing the file with no stop/confirmation step.
- Executed evidence before "done": ignore — no verification step is specified in this file; it only restates the write task.
- Say what was and was not checked: ignore — no mention of reporting checked/unchecked status.
**What it does not cover:** No description of the file format itself (delegated to the skill); no fallback if `session-logs/` cannot be created; no handling of concurrent/duplicate topic detection beyond the one-line instruction.

**item-5fc81ea9**
**Trigger:** Loads on-demand, on the `/pickup` command; not always on.
**What it makes the agent do:** Invoke the session-handoff skill in RESUME mode: "Find the newest file with the `kind: handoff` frontmatter in `session-logs/`" (or use a user-supplied topic/path argument); "Read only that file. Do not load the history of old sessions or other files until actually needed"; "Take a light look at the real state (`git status`/`git diff --stat` for code, or `ls` of the working folder for content) to verify the handoff matches reality"; "Summarize in ~3 lines: where we are → next step → what to avoid, and wait for confirmation before moving on."
**Enforcement:** Prose only. No executable check; nothing verifies the agent actually limited itself to one file or performed the reality check.
**Dependencies:** Depends on the session-handoff skill (item-c238a6db) for format/rules; optionally `git` or a directory listing for the reality check, neither required to exist.
**State it writes:** None — this is a read/summarize command; it does not create or modify files.
**Fit with the bar:**
- Plan then stop before consequential work: support — explicitly instructs to summarize and "wait for confirmation before moving on" before further action.
- Executed evidence before "done": partial support — includes a "light look at reality" step (`git status`/`ls`) to cross-check the handoff against actual state, though it is described as light/optional in depth.
- Say what was and was not checked: partial — the 3-line summary format ("where we are → next step → what to avoid") approximates this but does not explicitly require stating what was and was not verified.
**What it does not cover:** No instruction for what to do if no `kind: handoff` file exists; no handling of multiple candidate files with ambiguous topics; no enforcement that only one file was read.

### Agent-directed text

None beyond the items' own operating instructions, which are the items' stated purpose (skill/command definitions) rather than embedded third-party directives. No separate hidden agent-directed text was found.

### Could not determine

- Whether `session-logs/` or any persistent-memory file (e.g. `MEMORY.md`) already exists in a given project, since no such files are included in these items.
- How the "skill" and "command" file types are registered/loaded by the surrounding agent runtime (e.g. how `/handoff` and `/pickup` map to these files) — referenced by convention but not shown in the files themselves.
- Behavior when the optional `$ARGUMENTS` topic/path does not match any existing file.
