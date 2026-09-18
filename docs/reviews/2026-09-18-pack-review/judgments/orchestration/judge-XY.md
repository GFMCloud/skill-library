### Steelman X

item-5f05bf4c is a deliberately minimal "discovery stub": it loads only on demand, resolves the correct executable through a documented precedence order (env var → dev repo → IDE-safe fallback → default), and explicitly warns against a real collision hazard (bare `orca` launching the GNOME screen reader on Linux). It refuses to silently fall through on failure ("report its exact error and stop"), and it defers the actual orchestration guidance to a version-matched fetch rather than baking possibly-stale instructions into the skill file — a sensible design for keeping context short and instructions in sync with whatever CLI version is actually installed. For a toolkit that already has a working `orca` binary, this is a lightweight, safe front door.

### Steelman Y

Y supplies two purpose-built items that map directly onto the three-part bar. item-4b5c699b forces a seven-fact interview and explicit fit-test/decline conditions before it will scaffold a batch-sweep project, and refuses to run anything itself ("Do not run the sweep here: scaffolding only"). item-bdc9b27e is a read-only supervisor — enforced not just by prose but by `disallowedTools` blocking Write/Edit/NotebookEdit — that gates loop start on four shown preconditions, watches for four named failure patterns (stall, retry storm, cost drift, blocked queue), and mandates evidence-backed recommendations plus explicit Checked/Not-checked sections every time, with resume authority reserved for a human. This is a small, concrete, mechanically-backed supervision system built specifically for the slot's purpose.

### Scores

| Criterion | X (item-5f05bf4c) | Y (item-4b5c699b, item-bdc9b27e) |
|---|---|---|
| Fit with the bar | **1** — stops on executable failure (partial plan-then-stop) but the report marks "evidence before done" and "checked/not-checked" as "not covered," since all substantive orchestration logic is deferred to an unseen external guide. | **3** — 4b5c699b explicitly refuses to run consequential work before an interview gate ("Do not run the sweep here"); bdc9b27e mandates evidence per recommendation ("quote the before and after") and explicit **Checked**/**Not checked** sections every checkpoint, with resume left to "the human's call." |
| Enforcement mechanism | **0** — report states plainly "There is no script, hook, or exit-code check in this item itself... nothing in the file itself can block or verify that the agent actually complies." | **2** — bdc9b27e's `disallowedTools` frontmatter mechanically blocks Write/Edit/NotebookEdit ("fails closed at the tool layer"); the checkpoint judgments themselves and all of 4b5c699b remain prose-only. |
| Context cost | **3** — loads only on the matching description, and its own content is a short resolution+fetch routine (report quotes only ~7 short directives); it explicitly defers the bulk of content to a runtime fetch rather than carrying it in-context. | **2** — both items are also "not always on," but each carries substantially more inline structure (3-step scaffold process with 5 rules, or 4 preconditions + 4 named failure conditions + mandatory report sections), so a triggered load costs more text than X's stub. |
| Maintenance burden | **1** — depends on an external, unbundled CLI binary (`orca`/`orca-dev`/`orca-ide`) and its `skills get` subcommand actually existing and supporting `--json`; the report notes "no dependency is bundled in the file itself," meaning functionality is contingent on infrastructure the item doesn't confirm is present. | **3** — item-bdc9b27e "names no runtime, CLI, or service of its own," reading only the supervised loop's own artifacts; item-4b5c699b depends only on its own bundled templates, matching "runs with what the reports say is already present." |
| Specificity | **1** — generic executable-resolution and fallback logic; the report is explicit that the file "defers all actual orchestration mechanics (dispatch, dependency waits, escalation, DAGs, decision gates)" elsewhere. | **3** — named failure modes ("Stall," "Retry storm," "Cost drift," "Blocked queue," each with a precise definition), concrete checklists (fit-test decline conditions, seven interview facts, four preconditions), and explicit stop conditions ("A rate limit is a stop until the reset time it names, never a retry"). |

No 0 on "Fit with the bar" for either candidate, so neither is disqualified outright.

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-5f05bf4c | DISCARD | By the report's own framing it is "a discovery stub, not the usage guide" — all dispatch, dependency, waiting, and escalation logic is deferred to an external, unseen guide fetched at runtime, so nothing concrete for this slot's actual coordination job is present in the file to take. |
| item-4b5c699b | COMPLEMENT | Fills a gap neither of the other items cover: pre-execution planning of multi-item work, with a mandatory fact-gathering interview and explicit fit-test/decline conditions before any real dispatch infrastructure is scaffolded. |
| item-bdc9b27e | COMPLEMENT | Fills a gap neither of the other items cover: real-time, read-only supervision of an in-progress agent loop with named stall/retry/cost/blocked-queue detection, mechanically enforced by `disallowedTools`, and mandatory per-checkpoint Checked/Not-checked reporting with escalation/resume reserved for a human. |

### Deciding criteria

Specificity and enforcement mechanism settled the rows: item-5f05bf4c's own report confirms it contains no orchestration substance and no verification mechanism, while Y's two items each carry concrete, non-overlapping checklists/failure modes and (for bdc9b27e) an actual tool-layer restriction.

### What I could not assess from reading alone

For X, the actual orchestration mechanics (dispatch, dependency handling, waiting, escalation, DAG format, decision gates) live in a runtime-fetched guide that isn't included, so its real quality, coverage, and consistency with the bar are unverifiable — a behavioral test would need to actually run `ORCA skills get orchestration` and inspect the fetched guide's content and structure. For Y, both items' "Done when" and Checked/Not-checked claims would need a live run to confirm the agent actually follows the interview gate and stop conditions rather than skipping them, since both mechanisms are prose-enforced except for bdc9b27e's tool restriction. I did not attempt to infer either candidate's source and have no strong guess to report.
