### Items

| id | type | one line |
|---|---|---|
| item-5f05bf4c | skill | A discovery-stub skill that tells the agent how to pick an orchestration CLI executable and then fetch a version-matched usage guide from that binary at runtime, rather than containing the orchestration instructions itself. |

### For each item

**item-5f05bf4c**
**Trigger:** Loads on-demand (skill, not always-on), triggered by the `description` frontmatter matching requests for coordinating supervised workers, threaded messages, blocking ask/reply, task dispatch, worker_done/escalation waits, task DAGs, decision gates, or coordinator loops — as opposed to a full ownership "handoff" to another agent/worktree, which the description routes to a different named skill instead.
**What it makes the agent do:** Resolve one CLI executable for the session and reuse it: use the `ORCA_CLI_COMMAND` env var if set; else `orca-dev` if `ORCA_DEV_REPO_ROOT` is present; else `orca-ide` on Linux outside a managed terminal (explicitly warning that bare `orca` there can instead launch the unrelated GNOME screen reader); else fall back to `orca`. It instructs the agent to substitute this resolved name everywhere a placeholder is used, and "If the selected executable cannot run, report its exact error and stop. Do not fall through to another executable." It then tells the agent to run a `skills get orchestration` command against that executable to print the real, version-matched guide before doing anything else, optionally scoped to a named reference file for conditional cases ("remote placement, uncertain release recovery, or expanded DAG work"), preferring `--json` output, and to fall back to `--help` or explain that an update is needed if `skills get` is unsupported — with the instruction "do not guess unsupported commands."
**Enforcement:** Prose only. There is no script, hook, or exit-code check in this item itself — the file only instructs the agent verbally to stop on executable failure and not to fall through; nothing in the file itself can block or verify that the agent actually complies. Actual command behavior and any pass/fail logic live outside this file, in the external binary it defers to.
**Dependencies:** An external orchestration CLI binary the file only refers to generically as "the `orca` binary" (or its `-dev`/`-ide` variants) and its `skills get` subcommand; no dependency is bundled in the file itself, matching the stated "runtime deps: none named."
**State it writes:** None. The file describes commands to run and guides to fetch but contains no instruction to write logs, files, or directories.
**Fit with the bar:**
- Plan then stop before consequential work: partial support — it does instruct the agent to stop rather than fall through if the executable can't run ("report its exact error and stop"), and to fetch the authoritative guide before issuing further commands, but this is a setup/discovery gate rather than a plan-then-pause step for the actual coordination work itself.
- Executed evidence before "done": not covered — the file contains no instruction about producing or checking evidence of completed work; it stops at "load the guide before running commands."
- Say what was and was not checked: not covered — no instruction to report what was verified versus skipped.
**What it does not cover:** By its own framing it is explicitly "a discovery stub, not the usage guide" — it defers all actual orchestration mechanics (dispatch, dependency waits, escalation, DAGs, decision gates) to a guide fetched from the external binary at runtime, so none of that substantive behavior is present in the file itself.

### Agent-directed text

- item-5f05bf4c: "This file is a discovery stub, not the usage guide."
- item-5f05bf4c: "Choose the executable once and reuse it for every later command"
- item-5f05bf4c: "Never run bare `orca` there — outside Orca's terminals it normally resolves to the GNOME Orca screen reader (`/usr/bin/orca`) and starts speech on the user's machine."
- item-5f05bf4c: "Below, `ORCA` is a placeholder for the executable you resolved. Substitute it before running anything; do not create a shell variable or run `ORCA` literally."
- item-5f05bf4c: "If the selected executable cannot run, report its exact error and stop. Do not fall through to another executable, which could silently target a different Orca build."
- item-5f05bf4c: "Prefer `--json`. Use the selected executable's `--help` for commands or flags the guide does not cover."
- item-5f05bf4c: "If `skills get` is unknown, explain that updating Orca restores the guide; use `--help` for read-only discovery and do not guess unsupported commands."

### Could not determine

- The actual content of the "version-matched guide" printed by `ORCA skills get orchestration` (task dispatch mechanics, dependency handling, waiting/escalation logic, DAG format, decision gates) is not present in this file — it is fetched at runtime from the external binary and so cannot be assessed here.
- The contents of the referenced `references/<file>.md` bundled files (for "remote placement," "uncertain release recovery," or "expanded DAG work") are not included.
- The behavior/interface of the separate "orca-cli" skill that this item defers full-ownership handoffs to is not included in this item's files.
