### Items

| id | type | one-line description |
|---|---|---|
| item-fcc7bb6a | skill | Instructs an agent on when to spawn a helper session via a `orx agent spawn` CLI command, how to scope the task, protect branches/compute, and write a self-contained brief. |

### For each item

**item-fcc7bb6a**

**Trigger:** Loads on-demand as a skill, invoked per its description field: "Use before spawning a helper or interpreting its result; do not delegate the literature retrieval loop." Not always-on; it is pulled in only around delegation decisions.

**What it makes the agent do:**
- Use the `orx agent spawn` command, with variants for title/stdin, harness/model selection, and `--no-wake` when no follow-up is needed.
- Recognize that "a spawned session cannot spawn another helper" and that the CLI enforces a concurrency limit; if a spawn is refused, "do the work here or wait for a helper to finish."
- Choose tasks with a "clean boundary": delegate work "genuinely independent from the node this session owns" (e.g., surveying an unfamiliar codebase, writing up completed results); keep work in-session if it is "a step in the experiment loop already underway."
- Never delegate the retrieval loop covered by a separate skill (`orx-lit-review`); ranking of literature candidates must stay with the main agent.
- Protect branches and compute: never hand a helper a branch checked out by the current session; if code must change, tell the helper to create its own node/branch; a frozen experiment node may not be edited by either session; state exactly which `orx exp run` calls the helper may launch, and explicitly forbid launches when none are authorized; note helper edits stay in its own worktree and nothing auto-merges.
- Write a standalone brief, since the helper starts with an empty transcript: include project, relevant experiment and branch, metric, constraints, allowed compute, expected output, and "a concrete definition of done"; use `--stdin` for multi-paragraph briefs.

**Enforcement:** Prose-only guidance; no enforcement file, script, or hook ships with this item. The one enforcement mechanism referenced ("the CLI enforces the number of helpers a session may have in flight") is attributed to the external `orx` CLI, not to anything contained in this item, and the file gives no detail on fail-open/fail-closed behavior for that external check.

**Dependencies:** The `orx` CLI (`orx agent spawn`, and by reference `orx exp run`) must exist and be callable; a companion skill named `orx-lit-review` is referenced but not included here. No other runtimes, services, or install steps are named.

**State it writes:** None. The item creates no files, directories, or logs itself (spawning creates a worktree/transcript, but that is attributed to the external CLI, not written by this item).

**Fit with the bar:**
- Plan then stop before consequential work: partially supports — it requires a written brief with "a concrete definition of done," explicit branch protection, and explicit authorization language before compute-consuming calls ("Explicitly forbid launches when none are authorized"). It does not, however, instruct the agent to pause for user confirmation before the spawn itself; the spawn is presented as the action to take once the boundary is chosen.
- Executed evidence before "done": not covered — nothing in the file asks the agent to verify the helper's output, run checks, or produce evidence before treating delegated work as complete. It stops at "this chat resumes with the helper's closing reply."
- Say what was and was not checked: not covered — no instruction to report what was or wasn't verified about the helper's results.

**What it does not cover:** How to validate or integrate a helper's output after it returns; what happens to a rejected/failed spawn beyond retry-or-wait; any state or evidence review once the closing reply is received; onboarding or installation of the `orx` CLI itself.

### Agent-directed text

none

### Could not determine

The exact behavior and error semantics of the external `orx` CLI (e.g., what "enforces the number of helpers" does on refusal beyond "do the work here or wait"); the contents/behavior of the referenced `orx-lit-review` skill; any harness/model options accepted by `--harness`/`--model`.
