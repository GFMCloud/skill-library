### Steelman Y

`item-b9504c3e` targets a real, specific failure mode: an agent that judges a run by memory or by scattered stdout instead of reading back the actual persisted log. It gives concrete, executable-sounding guidance — specific `orx logs` flags (`--head`, `--bytes`, `--range`), a checklist of what the log must contain (variant/config, final metric, compact summary, recoverable trajectory), and two crisp rules that directly enforce "executed evidence before done": *"Never infer a result from run status or memory"* and *"Truncated output is not evidence of absence."* It also correctly separates stdout (log content) from stderr (truncation status), a detail that shows real familiarity with the failure mode of silently-truncated tool output. For any workflow built around long-running training runs read through `orx`, this is a tightly scoped, on-demand skill that would meaningfully prevent premature or hallucinated success claims.

### Steelman X

X splits the evidence problem into two complementary skills that mirror the bar's own structure: one (`item-7aed43c3`) makes the agent actually run checks and refuses to accept a tool's self-reported success, backed by a script that captures real exit codes per phase, distinguishes "ran/not-run/skipped," and even demonstrates a tamper case where a false "ran" claim is overridden because the exit file is missing; the other (`item-92c76be2`) forces the resulting report into a fixed, machine-checkable shape (CLAIM/CHECK/OUTPUT/VERDICT plus a mandatory NOT VERIFIED section) validated by its own script. Together they cover both "executed evidence" and "say what was and wasn't checked" with actual enforcement rather than prose, they generalize beyond a single log-reading tool to code, documents, deployments, data, and config, and both ship fixture-proofs of their own scripts' correctness — a level of self-verification neither item in Y attempts.

### Scores

| Criterion | Y (item-b9504c3e) | X (item-92c76be2, item-7aed43c3) |
|---|---|---|
| Fit with the bar | 2 — Strongly reinforces "executed evidence" ("Never infer a result from run status or memory") and partially supports "say what was checked," but is silent on "plan then stop" (neutral, not conflicting). | 3 — 7aed43c3 is central to "executed evidence" ("Executed evidence is attached to every claim of completion") and 92c76be2 enforces the not-verified list; neither conflicts with plan-then-stop, it's simply unaddressed, same as Y. |
| Enforcement mechanism | 0 — Report states explicitly: "Prose only — no executable checker, hook, or script is included in this file." | 3 — Both items ship scripts (`check-report.py`, `run-checks.sh`) that parse/validate structure, capture real exit codes, and fail closed on missing fields or missing exit files. |
| Context cost | 2 — Single skill, loads on demand per its trigger description; report gives no length/token count to compare precisely. | 2 — Two skills, each loads on demand per its own trigger, but their triggers ("presenting verification results" / "declaring any artifact complete") plausibly co-fire at the same moment, stacking two items' context where Y stacks one; no length counts given either. |
| Maintenance burden | 1 — Depends on the specific `orx` CLI and defers final formatting to an undefined external "session playbook" not included in the file, a real functional gap. | 2 — 92c76be2 needs only python3; 7aed43c3 lists bash/python3/node/npm/gh, and the report itself flags it could not determine where `gh` is actually used — an unresolved dependency, but scripts are otherwise self-contained with fixture-proofs. |
| Specificity | 3 — Concrete `orx logs` flag usage, explicit stdout/stderr distinction, explicit pre-report checklist, two quotable stop-conditions on truncation/inference. | 3 — Ordered check sequence (build/types/lint/tests/secrets/diff), `step -> verify: check` declaration format, three cited prior cases of tools lying about success, a tamper-detection example, mandatory NOT VERIFIED section. |

No 0 on "Fit with the bar" for either candidate, so neither fails the slot outright.

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-b9504c3e | COMPLEMENT | Fills a gap neither X item covers: a protocol for reading back truncated/long-running logs via `orx logs` byte-range reads, distinct from X's build/lint/test-style checks. |
| item-92c76be2 | COMPLEMENT | Fills a gap in Y: a mandatory, script-validated NOT VERIFIED reporting shape that forces explicit disclosure of what wasn't checked, which Y's item only "partially supports" and never formats. |
| item-7aed43c3 | COMPLEMENT | Fills a gap in Y: real, script-enforced "run the thing" evidence (captured exit codes, tamper detection, cross-artifact-type coverage) versus Y's prose-only, log-reading-only enforcement. |

### Deciding criteria

Enforcement mechanism and Specificity (of domain coverage) settled the rows — each item's content is concrete enough that no pair does strictly the same job, so all three land as complements rather than supersessions.

### What I could not assess from reading alone

Whether `orx logs` (Y) or the two X scripts (`check-report.py`, `run-checks.sh`) are actually invoked automatically at the right moments versus skippable by the agent; whether the "session playbook" Y defers to exists and is adequate; whether X's `gh` dependency is load-bearing or vestigial; and whether the two X skills reliably co-trigger in practice or one gets skipped, leaving only formatting without execution or vice versa. I did not infer either candidate's origin from the reports.
