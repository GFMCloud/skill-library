### Steelman X

item-fcc7bb6a is a direct, operational match to the slot's literal purpose: deciding when and how to hand off independent work, and with what instructions. It gives concrete criteria for what counts as a "clean boundary" worth delegating (unfamiliar-codebase surveys, writing up completed results) versus what must stay in-session (a step in the experiment loop already underway), and it explicitly carves out the literature-retrieval loop as never delegable. It has real teeth around the things that go wrong when handing work to another agent process: never hand over a branch the current session has checked out, forbid edits to a frozen node by either party, name exactly which compute-consuming calls (`orx exp run`) the helper may launch and forbid unauthorized ones, and require the brief to state a "concrete definition of done" since the helper starts from an empty transcript. That's a specific, failure-mode-aware treatment of the actual mechanics of delegation, not just a routing heuristic.

### Steelman Y

item-b304dc9f addresses a decision that logically comes *before* the one X handles: whether to delegate at all, and to what model/effort, before any helper session is spawned. Its "Never guess silently" rule is a hard stop-and-ask instruction for exactly the ambiguous cases the owner cares about, and its Deep Planning mode explicitly produces "Human Review Checkpoints" before consequential steps (its own worked example is "before any IaC actually applies changes to a live AWS account"), which is a direct instantiation of plan-then-stop. Its build/review subagent pairing pattern — giving the reviewer only the artifact and success criteria, "never the build agent's reasoning or rationale" — is a genuinely good discipline against a reviewer just rubber-stamping the builder's self-report, which is in the spirit of "a tool reporting its own success is not evidence" even though the item itself never executes anything. It also requires no runtime or external CLI at all — it's self-contained reference material.

### Scores

| Criterion | item-fcc7bb6a (X) | item-b304dc9f (Y) |
|---|---|---|
| Fit with the bar | 2 — requires "explicit authorization language before compute-consuming calls" and a written definition of done, but the report states it "does not... instruct the agent to pause for user confirmation before the spawn itself" (X.md:28), and gives no coverage of executed-evidence or checked/unchecked reporting at all (X.md:29-30). No outright conflict, just gaps. | 2 — "Never guess silently... Getting the mode wrong wastes more time than asking once," plus Deep Planning's mandatory "Human Review Checkpoints" before consequential steps, actively reinforce plan-then-stop (Y.md:22). It never executes work, so it's silent (not contradictory) on evidence-before-done and checked/unchecked reporting (Y.md:23-24); "do not block on missing information" is a minor tension but applies only to its own non-consequential routing output. |
| Enforcement mechanism | 1 — "Prose-only guidance; no enforcement file, script, or hook ships with this item"; the one real limit (spawn concurrency) is attributed to the external CLI, not the item (X.md:21). | 1 — "Prose only; no executable enforcement file. Nothing blocks, warns, or exits non-zero" (Y.md:15). |
| Context cost | 2 — report gives no word/line count for trigger or body, only that it "loads on-demand" (X.md:11); no basis in the report to call it short or long. | 2 — report gives a counted fact, "Frontmatter description (148 words)" (Y.md:11), plus explicit reference to five distinct companion files (decision-rubric.md, model-catalog.md, effort-sizing.md, subagent-routing.md, output-template) it draws on when active — more itemized load surface than X's report discloses, even though each file is presumably small. |
| Maintenance burden | 1 — "The `orx` CLI... must exist and be callable; a companion skill named `orx-lit-review` is referenced but not included here" (X.md:23): a real external runtime dependency plus a missing referenced piece. | 3 — "the skill itself requires no runtime, CLI, or service to function — it just reads its own reference files and outputs text" (Y.md:17). |
| Specificity | 3 — concrete brief checklist (project, experiment, branch, metric, constraints, allowed compute, expected output, definition of done), a named fallback on spawn refusal ("do the work here or wait for a helper to finish"), and an explicit frozen-node prohibition (X.md:16-19). | 3 — a five-axis named rubric, two distinct modes with distinct required outputs, an explicit mode-ambiguity stop rule, and a precisely stated build/review data-hiding rule (Y.md:13, 22). |

Neither candidate scores 0 on Fit with the bar; both have real gaps (no execution-evidence step, no checked/unchecked field) but neither actively instructs behavior that contradicts the three required behaviors.

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-fcc7bb6a | COMPLEMENT | Covers the actual hand-off mechanics — CLI spawn syntax, branch/compute protection, concurrency-refusal handling, and self-contained brief requirements — that item-b304dc9f explicitly places out of scope ("does not decide whether work should leave the session for a separate... workflow"). |
| item-b304dc9f | COMPLEMENT | Covers the upstream decision item-fcc7bb6a takes as already settled — which model/effort to use and whether to go inline vs. subagent at all — plus a hard stop-and-ask rule for ambiguous cases and a build/review verification pattern that item-fcc7bb6a never addresses. |

### Deciding criteria

Maintenance burden (external `orx` CLI + missing companion skill for X vs. no runtime dependency for Y) and Fit with the bar (Y's explicit human-review-checkpoint and stop-and-ask instructions vs. X's silence on pausing before the spawn action itself) most separated the two; specificity and enforcement were essentially tied and neither failed the bar outright.

### What I could not assess from reading alone

Whether the `orx` CLI that item-fcc7bb6a depends on actually exists and behaves as described (concurrency refusal, worktree isolation, no auto-merge) would need to be run, not just read. Whether item-b304dc9f's build/review pairing is actually enforced in a live session (i.e., whether a reviewer subagent really never sees the builder's rationale) or is just aspirational prose would also need a behavioral trace. I could not tell where either report's source material came from and did not try to guess.
