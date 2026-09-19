### Steelman X

`item-ebef553d` is built for the actual moment most "humanize" requests happen: someone has a real email or Slack message to send and wants it to sound like them, not like a bot. It doesn't just ban AI-sounding phrases — it routes on channel and relationship first ("identify the recipient and relationship... apply tone exceptions"), which is the variable that actually determines whether a message reads as human (a note to a direct report reads differently from a customer escalation). Its three "non-negotiables" plus explicit blocklists give the agent a hard bar to clear rather than vague taste. It also draws its own scope boundary correctly: it produces a draft and defers sending, and it explicitly separates risk-flagging from the draft body ("Flag anything risky... at the end of the draft, not woven into it") so a human reviewer can see the risk without having to parse it out of the prose. It stays out of file-system side effects entirely, which limits how much damage a bad application of the skill could do.

### Steelman Y

`item-4555c4d5` treats "sounds like AI" as a diagnosable, taxonomized problem rather than a vibe. Twenty-five named patterns, each with a watch-for list, a stated failure mode, and before/after pairs, is a genuinely falsifiable checklist — an agent (or a reviewer) can point at a specific pattern name and a specific before/after example rather than relying on "does this sound right." Its content-preservation rule is the most important discipline in this slot: it explicitly forbids adding "a fact, name, number, date, quote, or citation" during a humanizing pass and treats an unsupported addition as an error — this directly guards against the most dangerous failure mode of style-editing (silently changing meaning while polishing prose). It's also honest about its own limits, explicitly stating that "people who judge by feel do little better than chance," which is a rare and useful admission of the task's inherent uncertainty, and it adapts its output contract by mode (paste vs. file vs. embedded) rather than assuming one context.

### Scores

| Criterion | item-ebef553d (X) | item-4555c4d5 (Y) |
|---|---|---|
| Fit with the bar | 2 — never instructs sending or any consequential action itself; drafting a message isn't itself irreversible, so it's silent on the bar rather than actively conflicting with it (report: "sending itself is outside its stated scope"). | 1 — in file mode it "runs straight through to 'write only the final text to the file,' which conflicts with stopping before a consequential (file-overwriting) action," a direct, not merely silent, conflict with behavior 1. |
| Enforcement mechanism | 0 — "Prose only... no enforcement files are present." | 0 — "Prose only. There is no script, hook, linter, or other executable artifact bundled with it." |
| Context cost | 2 — loads on demand per its trigger description; content is a 10-step process plus blocklists, no reference table described. | 1 — also loads on demand, but the report states "the bulk of the file is the 25-pattern reference table itself, each with a watch-for list, a stated problem, and before/after example pairs," a materially longer payload by the report's own description. |
| Maintenance burden | 3 — "No other items are referenced as dependencies"; the one named tool (message_compose_v1) is used "when available," i.e. optional. | 3 — "None named... self-contained markdown guidance requiring no runtime, CLI, or external service." |
| Specificity | 2 — concrete non-negotiables and blocklists, but the report describes them as lists of words/phrases rather than named failure-mode categories with worked examples. | 3 — 25 named categories each with a watch-for list, a stated problem, and before/after example pairs, per the report the most concrete artifact of either candidate. |

Neither candidate scores 0 on "Fit with the bar," so neither is disqualified outright, though Y's file-mode behavior is a real, stated conflict with the plan-then-stop behavior rather than a mere omission.

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-ebef553d | COMPLEMENT | Covers channel identification, recipient/relationship tone exceptions, sign-off conventions, and "lead with the ask" structure — none of which item-4555c4d5 addresses, since Y only edits existing prose for AI-tell patterns and does not reason about audience or channel. |
| item-4555c4d5 | COMPLEMENT | Covers a named, example-backed taxonomy of AI-sounding patterns and an explicit no-invented-facts discipline during rewriting — X's report only describes "blocklists" and "non-negotiables" without worked examples or a content-preservation rule. |

### Deciding criteria

Specificity settled the per-item classification (each item's concrete checklist covers ground — channel/recipient tone logic vs. a named pattern taxonomy with fact-preservation — that the other's report shows no equivalent for); Fit with the bar is what separates the two candidates in the overall scoring, since Y's file-mode write-through is a stated conflict with plan-then-stop while X never triggers that bar at all.

### What I could not assess from reading alone

Whether X's blocklists and Y's 25-pattern catalog actually overlap in content (i.e., whether merging them would be mostly redundant or mostly additive) can't be determined without seeing the full text of both blocklists side by side — the reports summarize rather than reproduce them. I also can't tell from the reports how often Y's file mode is actually invoked in practice versus paste/embedded modes, which matters for how serious the plan-then-stop conflict is in real use. I have no basis to guess either candidate's origin and am not attempting to.
