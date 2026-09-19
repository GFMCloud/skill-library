### Items

| id | type | one line |
|---|---|---|
| item-b9504c3e | skill | Guides preparing run logs as evidence and reading/validating them with `orx logs` before trusting or reporting a run's result. |

### For each item

**item-b9504c3e**
**Trigger:** A skill loaded on-demand by its description, which says to use it "before launching a run whose output must be judged, after a run finishes, or before analyzing or reporting run results." Not always on.
**What it makes the agent do:** Treat run logs as the evidence channel: make the run command print everything needed to judge the result, then read it back with `orx logs`. Specific instructions include printing "final metrics and a compact summary block at the end of the run, not just scattered during training," echoing "the configuration the run actually used so the log identifies the variant," and printing "periodic one-line metrics" for long runs so trajectory stays visible through byte-range reads. It gives concrete `orx logs` invocations (tail, `--head`, `--bytes`, `--range`) and notes where output goes (stdout for log content, stderr for a `[source] bytes a–b of N` status line noting truncation). Before accepting or reporting a run-derived claim, it requires confirming: the log identifies the variant/effective configuration; final metric and compact summary are present; the relevant trajectory is recoverable for a long run; and the returned byte window actually contains the supporting output. It states "Never infer a result from run status or memory" and "Truncated output is not evidence of absence," instructing further reads via `--head`/`--bytes`/`--range` until the relevant portion has been read. It also directs formatting the final chat response "using the evidence-and-links contract in the session playbook."
**Enforcement:** Prose only — no executable checker, hook, or script is included in this file. Nothing blocks, warns, or exits non-zero; compliance depends on the agent following the written guidance.
**Dependencies:** The `orx` CLI (specifically `orx logs` and `orx runs <projectId>` commands) and a "session playbook" referenced for response formatting, which is not included in this item.
**State it writes:** None. The file only describes reading persisted logs; it does not itself write files, directories, or logs.
**Fit with the bar:**
- Plan then stop before consequential work: ignores. The item is about post-hoc log inspection and pre-run print design; it contains no instruction to pause for approval before taking consequential action.
- Executed evidence before "done": supports. Its core content is explicitly about this — requiring the log to contain final metrics, a compact summary, and effective configuration, and requiring validation of that evidence before "accepting or reporting a run-derived claim," e.g. "Never infer a result from run status or memory."
- Say what was and was not checked: partially supports. It requires confirming specific things are present (variant/config, final metric, summary, recoverable trajectory, non-truncated window) before reporting, which implies awareness of what was checked, but it does not explicitly instruct the agent to state in its output what was or was not checked — it only instructs formatting per an external "evidence-and-links contract."
**What it does not cover:** It does not address what to do if the required evidence is missing or unrecoverable (no stated fallback or escalation), does not cover non-log evidence (e.g., file diffs, test results outside a run's stdout), and does not itself define the "evidence-and-links contract" it defers to.

### Agent-directed text

item-b9504c3e: "Use before launching a run whose output must be judged, after a run finishes, or before analyzing or reporting run results." (from the frontmatter description); "Never infer a result from run status or memory."; "Truncated output is not evidence of absence."; "Format the resulting chat response using the evidence-and-links contract in the session playbook."

### Could not determine

The content and rules of the "session playbook" and its "evidence-and-links contract" referenced in item-b9504c3e are not present in the given files. The behavior of the `orx` CLI itself (beyond the flags documented) is not shown.
