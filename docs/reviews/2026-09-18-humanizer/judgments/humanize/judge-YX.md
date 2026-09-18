### Steelman Y

Item-4555c4d5 is a well-scoped, single-purpose skill: strip AI "tells" from prose without altering its factual content. Its strength is specificity — a taxonomy of 25 named tell patterns, each with a watch-for list, the underlying problem, and a before/after example, plus an explicit rule that no fact, name, number, date, quote, or citation may be added beyond what the source or user supplied. It also defines three distinct output contracts (pasted-text, file, embedded) so its behavior is predictable depending on how it's invoked, and it explicitly protects non-prose content (code, YAML, paths, link targets) from being touched in file mode. It is honest about its own limits, noting that "people who judge by feel do little better than chance." It has zero named dependencies and writes no persistent state of its own outside the one file it's asked to edit.

### Steelman X

Item-ebef553d targets a narrower and arguably more faithful reading of "humanize": not just removing generic AI tells, but making outbound communication sound like a *specific* person, calibrated to channel (email/chat/notes) and recipient relationship, with tone exceptions for situations like escalated customers or leadership. It operationalizes this with a 10-step process, three hard "non-negotiables" (no em dashes, no listed filler phrases, no over-explaining), and channel-specific formatting/sign-off conventions — plus a real end-of-process safety behavior absent from Y: flagging risky content (customer escalation, pricing, compliance) at the end of the draft rather than burying it. It never overwrites a file or takes an send action itself, keeping its footprint low-consequence, and it degrades gracefully if its optional `message_compose_v1` tool isn't available.

### Scores

| Criterion | Y (item-4555c4d5) | X (item-ebef553d) |
|---|---|---|
| Fit with the bar | **1** — Report explicitly flags that file mode "runs straight through to 'write only the final text to the file,' which conflicts with stopping before a consequential (file-overwriting) action," and embedded mode's "return only the final text" gives no disclosure of what was checked, undermining behavior 3 as well. | **2** — Never writes files or sends anything itself (report: "the skill produces draft text as its output; it does not describe writing any file, log, or directory"); no explicit instruction contradicts plan-then-stop, though it also adds no explicit checkpoint. |
| Enforcement mechanism | **1** — Report states plainly "Prose only. There is no script, hook, linter, or other executable artifact bundled with it." | **1** — Report states "Prose only. There is no executable checker... No enforcement files are present." Identical mechanism, same score. |
| Context cost | **1** — Loads on demand ("Loads on demand, triggered by its own frontmatter description"), but report notes "the bulk of the file is the 25-pattern reference table itself" with watch-for lists and before/after pairs for all 25 — a counted, sizeable payload. | **1** — Loads on demand ("Loads on-demand. Per its description, it triggers on any request to write, draft, edit..."), but carries a 10-step process plus "longer blocklists of tell-tale words/phrases and structural patterns" plus per-channel rules — comparably long, though the report gives no exact count for X's lists (unlike Y's stated "25"). |
| Maintenance burden | **3** — Report: "None named... self-contained markdown guidance requiring no runtime, CLI, or external service." | **2** — Report: references "a tool called 'message_compose_v1' to use 'when available'" — an optional but named external dependency not itself supplied; otherwise "no runtime, CLI, or service is otherwise named." |
| Specificity | **3** — 25 named patterns each with watch-for list, stated problem, and before/after example pairs, plus a defined 4-step edit procedure. | **3** — 10-step process, three named non-negotiables, per-channel/per-recipient tone exceptions, sign-off conventions, and a concrete risk-flagging instruction. |

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-4555c4d5 | COMPLEMENT | Fills a gap X's set lacks: general-purpose AI-tell removal across arbitrary prose types, with a 25-pattern taxonomy and distinct file/embedded/pasted-text output contracts that protect non-prose content. |
| item-ebef553d | COMPLEMENT | Fills a gap Y's set lacks: per-channel, per-recipient voice-matching for outbound communication (email/chat/notes), tone exceptions for high-stakes contexts, and end-of-draft risk-flagging. |

### Deciding criteria
"Fit with the bar" and "Maintenance burden" separate the two: Y carries an explicit, report-flagged conflict with the plan-then-stop behavior in its file mode, while X avoids that conflict by never writing files itself but takes on a small external-tool dependency (`message_compose_v1`) that Y doesn't have.

### What I could not assess from reading alone
Neither report can confirm from text alone whether an agent actually honors the internal "mark → draft → check" or 10-step sequences in practice, whether Y's file-mode overwrite would in fact bypass a user's broader plan-then-stop expectations in a live session, or what `message_compose_v1` does or whether it can itself send messages (which would raise X's consequence profile). A behavioral test would need to run each skill against real prose/messages and check whether the promised checklist steps, non-negotiables, and risk flags actually surface in output, and whether Y's file mode pauses for confirmation when embedded in a session governed by an outer plan-then-stop policy. I did not form any belief about where either report's source material came from.
