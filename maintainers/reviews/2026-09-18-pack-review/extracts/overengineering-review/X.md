### Items

| item id | type | one line |
|---|---|---|
| item-4ef8ec23 | skill | Reviews a diff for over-engineering, emitting one tagged line per finding and a net-line-count summary. |
| item-3cb4b1ae | skill | Same review applied to a whole repository instead of a diff, producing a ranked list of cuts. |

### For each item

**item-4ef8ec23**
- **Trigger:** Loads on-demand when the user's phrasing matches the description — e.g. "review for over-engineering", "what can we delete", "is this over-engineered", "simplify review", or an explicit slash invocation. Not always on.
- **What it makes the agent do:** Produce one line per finding in the form `L<line>: <tag> <what>. <replacement>.` using five fixed tags (`delete:`, `stdlib:`, `native:`, `yagni:`, `shrink:`), each with a defined meaning (e.g. `yagni:` = "abstraction with one implementation, config nobody sets, layer with one caller"). End every review with `net: -<N> lines possible.`, or `Lean already. Ship.` if nothing to cut, "and stop." Explicitly told: "Does not apply the fixes, only lists them." A revert phrase ("stop ponytail-review" or "normal mode") switches back to ordinary review style.
- **Enforcement:** Prose only — instructional text with example good/bad outputs, no script or check that validates the agent's output format or blocks non-compliant behavior. Nothing to fail open or closed on.
- **Dependencies:** None named — no runtime, CLI, or external service referenced.
- **State it writes:** None. It produces a text review only; no files, directories, or logs are created.
- **Fit with the bar:** Plan-then-stop-before-consequential-work — supported: the item is a read-only review that never edits code ("Does not apply the fixes, only lists them"), so it never crosses into consequential action. Executed-evidence-before-"done" — ignored: nothing directs the agent to run tests, execute code, or gather evidence before presenting findings; it's a static-reading task. Say-what-was-and-was-not-checked — partially supported: the Boundaries section states scope explicitly ("Scope: over-engineering and complexity only. Correctness bugs, security holes, and performance are explicitly out of scope"), which is a declared limit, though not phrased as a per-run checked/unchecked disclosure.
- **What it does not cover:** Correctness, security, and performance review (explicitly routed elsewhere); it does not apply any of the fixes it lists; it carves out an exception so "a single smoke test or `assert`-based self-check" is never flagged for deletion.

**item-3cb4b1ae**
- **Trigger:** Loads on-demand when phrasing matches its description — "audit this codebase", "audit for over-engineering", "what can I delete from this repo", "find bloat", or its slash invocation. Not always on. Described as a "One-shot report."
- **What it makes the agent do:** Run the same tag scheme as the diff-scoped item ("Same as ponytail-review") but across the whole tree, ranking findings "biggest cut first." Instructed to hunt for specific patterns: "Deps the stdlib or platform already ships, single-implementation interfaces, factories with one product, wrappers that only delegate, files exporting one thing, dead flags and config, hand-rolled stdlib." Output one ranked line per finding: `<tag> <what to cut>. <replacement>. [path]`, ending with `net: -<N> lines, -<M> deps possible.` or `Lean already. Ship.` A revert phrase ("stop ponytail-audit" or "normal mode") restores default behavior.
- **Enforcement:** Prose only — no executable check, script, or gate; nothing enforces the output format or scope beyond instructional wording.
- **Dependencies:** None named.
- **State it writes:** None — output is a report to the conversation; no files or logs are created.
- **Fit with the bar:** Plan-then-stop-before-consequential-work — supported: "Lists findings, applies nothing," so it stops short of making changes. Executed-evidence-before-"done" — ignored: there is no instruction to run or verify anything; it is a static scan producing a report. Say-what-was-and-was-not-checked — partially supported: the Boundaries section states the same explicit scope limit ("Scope: over-engineering and complexity only. Correctness bugs, security holes, and performance are explicitly out of scope. Route them to a normal review pass").
- **What it does not cover:** Correctness, security, performance (explicitly excluded and routed elsewhere); does not apply fixes; framed as a single one-shot pass rather than iterative or continuous auditing.

### Agent-directed text

none

### Could not determine

Both items refer to "a normal review pass" / "correctness-focused review" and a "normal mode" / verbose review style to revert to, but no such review pass or mode is included among the files read, so its behavior cannot be determined.
