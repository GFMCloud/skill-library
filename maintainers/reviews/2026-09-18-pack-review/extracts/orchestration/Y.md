### Items

| item id | type | one-line description |
|---|---|---|
| item-4b5c699b | skill | Interviews the user and scaffolds a resumable batch-sweep project (manifest, per-item state files, worker runbook, dispatch skill) for running an identical treatment over many items; it does not run the sweep itself. |
| item-bdc9b27e | agent | Read-only supervisor for an already-running or about-to-start agent loop/sweep/harness: checks preconditions, watches checkpoints for stalls/retries/cost drift, and recommends continue, pause-and-shrink, or escalate. |

### For each item

**item-4b5c699b**
**Trigger:** Loads on demand as a skill, matched by its description against requests like "validate every skill in the library", "run this across all our repos", "sweep harness", or "batch job with more items than fit in a context window." Not always on.
**What it makes the agent do:** Runs a "Step 1: Fit test" (three required conditions: one treatment for N items, more work than fits one context, a checkable per-item done state) with explicit decline conditions ("Decline, and say why, when..."). Then a "Step 2: Interview" that must gather seven load-bearing facts (enumeration method, per-item treatment, per-item done check, a poisoned item, batch size, project directory, who commits) "in one batch" before scaffolding. Then "Step 3: Scaffold" builds a fixed tree (`MANIFEST.tsv`, `CLAUDE.md`, `WORKER.md`, `state/item-*.md`, `failures.md`, a generated `/sweep` dispatch skill) from bundled templates, under five rules including "Generate the manifest by actually running the enumeration... then commit it before any worker runs" and "The poisoned item is mandatory." It states explicitly: "Do not run the sweep here: scaffolding only." Closes with a verification pass (grep for stray `<PLACEHOLDER>`, check tree/links) and a "Done when" checklist.
**Enforcement:** Prose only. There is no executable check bundled in this item; correctness relies on the agent following the checklist and self-verifying (e.g., grepping for leftover placeholders). No named enforcement file, so it fails open if the checklist is skipped.
**Dependencies:** None named in the item itself. It depends on its own bundled templates (`references/doctrine.md`, six files under `templates/`) and, once instantiated, the generated harness depends on a subagent-dispatch capability to run workers in parallel.
**State it writes:** The skill itself writes no persistent state; running it generates a new project tree (`MANIFEST.tsv`, `CLAUDE.md`, `WORKER.md`, `state/` directory, `failures.md`, `.claude/skills/sweep/SKILL.md`) that the *generated* harness later populates with one state file per item.
**Fit with the bar:**
- Plan then stop before consequential work: supports. It forces an interview gate before scaffolding and explicitly refuses to run the sweep: "Do not run the sweep here: scaffolding only."
- Executed evidence before "done": supports, but only for the harness it generates, not for itself — the generated `WORKER.md` template requires "the command run and its actual output, not a paraphrase," and the generated dispatch skill says "Do not proceed on a worker's chat summary alone: read the state file it wrote."
- Say what was and was not checked: mostly ignored. The generated `item-state` template has an optional advisory `## Notes` field but no required "checked / not checked" statement; the item's own "Done when" list is a completion checklist, not a per-run checked/not-checked report.
**What it does not cover:** Does not run or monitor a sweep once scaffolded (later sessions do that via the generated `/sweep` skill); explicitly routes heterogeneous, multi-phase work elsewhere ("route to `phased-harness`"); does not itself define escalation to a person beyond a `needs-human` disposition value in the generated `failures.md` template.

**item-bdc9b27e**
**Trigger:** Loads on demand as an agent, invoked "when a fix loop, batch sweep or scheduled harness runs for more than a few iterations, and when a loop looks stuck." Not always on. Its frontmatter disallows the `Write`, `Edit`, and `NotebookEdit` tools, making it read-only by construction.
**What it makes the agent do:** Before a loop starts, confirm four preconditions by reading a file or running a read-only command — a pass/fail check that "has failed at least once on purpose," a written attempt/cost budget, a rollback path (branch/worktree/snapshot), and isolation from shared state — and report any precondition that "cannot be shown" as missing rather than assumed. While the loop runs, read its own record at each checkpoint and watch for four named conditions: Stall ("no change in the check's result, or in the files touched, across two consecutive checkpoints"), Retry storm ("the same failure text on consecutive attempts"), Cost drift, and Blocked queue ("A rate limit is a stop until the reset time it names, never a retry"). It must then give "Exactly one recommendation per checkpoint, with the evidence that produced it": `continue`, `pause and shrink` (naming a smaller resume scope), or `escalate`, followed by explicit **Checked** and **Not checked** sections. It states "Resuming after a pause is the human's call."
**Enforcement:** Mixed. The `disallowedTools` frontmatter field is an actual mechanical restriction (blocks the agent from invoking Write/Edit/NotebookEdit), so the no-editing rule fails closed at the tool layer. The checkpoint judgments and recommendations themselves are prose-only guidance with no separate executable gate, so they fail open if the reader ignores them.
**Dependencies:** None named in the item. It depends entirely on the supervised loop producing its own readable artifacts (state file, run log, budget file); it names no runtime, CLI, or service of its own.
**State it writes:** None — it is read-only and produces only a report (recommendation plus Checked/Not checked), no files or logs.
**Fit with the bar:**
- Plan then stop before consequential work: supports. It gates the loop's start on four shown preconditions and defers any resume decision to a human: "Resuming after a pause is the human's call, and only after the check passes on the smaller scope."
- Executed evidence before "done": supports. Every recommendation must carry "the evidence that produced it," e.g. "`continue`: the check moved, quote the before and after" and "escalate: ... Quote the two checkpoints or the repeated failure text."
- Say what was and was not checked: supports directly and explicitly — it mandates a **Checked** and **Not checked** section after every recommendation.
**What it does not cover:** Cannot dispatch, restart, or repair the loop it watches ("it recommends, it does not restart or edit the loop"); cannot supervise a loop that keeps no record: "A loop with no state file or log cannot be supervised, and the report says so instead of guessing."

### Agent-directed text

none

### Could not determine

- item-4b5c699b: the actual answers a user would give during "Step 2: Interview," and therefore what a fully instantiated sweep (and its generated `/sweep` dispatch skill) looks like in practice — only the placeholder templates are present.
- item-bdc9b27e: the source material it was "adapted from" (an external agent of the same name, described only by name, license, and version in the file) and the contents of the review record it cites at `docs/reviews/2026-09-17-ecc/` are referenced but not included among the files read.
