### Steelman Y

item-b304dc9f is a well-structured decision-support skill for a genuinely hard, recurring judgment call: which model, at what reasoning effort, and whether to keep work inline or fan it to subagents. It backs this with named reference material (a five-axis rubric, a model catalog, an effort-sizing guide, a subagent-routing guide) rather than vague heuristics, and it has two calibrated modes — a fast default and an explicit "Deep Planning" mode for larger work that forces a task breakdown, per-task model/effort assignment, and a "Human Review Checkpoints" output before consequential steps proceed. It has a hard rule against silent guessing on mode ("Never guess silently. Getting the mode wrong wastes more time than asking once."), a fixed, terse output format so it doesn't sprawl into essay-writing, zero runtime dependencies, and it self-scopes out of a decision that belongs elsewhere (leaving the session entirely). For a slot about *deciding* when and how to delegate, this is a serious, fairly complete answer to the "when/how much/which model" half of the question.

### Steelman X

item-fcc7bb6a answers the other half of the delegation question that Y explicitly disclaims: once you've decided to hand work to a helper, how do you do it safely? It gives concrete mechanics — the actual CLI invocation, a real concurrency-limit failure mode with an explicit fallback ("do the work here or wait for a helper to finish"), and a genuinely load-bearing safety model: never hand a helper a branch the current session has checked out, never let either session edit a frozen node, and explicitly state (or explicitly forbid) which compute-consuming calls the helper may launch. It also requires the brief itself to contain "a concrete definition of done," which is a real, checkable artifact rather than a vague instruction to "write good instructions." The scoping rule — delegate only work with a "clean boundary," never delegate a specific named loop-step — is a concrete, falsifiable test rather than generic advice. This is the item that actually protects shared state (branches, compute, frozen nodes) during delegation, which is a distinct and important part of the slot's purpose.

### Scores

| Criterion | Y (item-b304dc9f) | X (item-fcc7bb6a) |
|---|---|---|
| Fit with the bar | 2 — Mostly neutral/reinforcing (forces a stop when mode is ambiguous, produces "Human Review Checkpoints"), but it also directs "do not block on missing information" for its own sizing task, a minor tension with blocking-question behavior that the report itself flags. | 2 — Reinforcing on scope/authorization (requires explicit authorization language before compute-consuming `orx exp run` calls, protects branches/frozen nodes) but silent on pausing for user approval before the spawn itself ("does not... instruct the agent to pause for user confirmation before the spawn itself"). |
| Enforcement mechanism | 0 — Report states plainly: "Prose only; no executable enforcement file... Nothing blocks, warns, or exits non-zero." | 1 — Prose-only for branch/authorization rules, but one real tool-layer limit exists ("the CLI enforces the number of helpers a session may have in flight"), even though the report notes this belongs to the external `orx` CLI, not the item itself. |
| Context cost | 2 — Loads on-demand; the only counted figure given is a 148-word frontmatter trigger description, but the report gives no total size for the rubric/catalog/effort/routing reference files it pulls in. | 2 — Loads on-demand per its description field, but the report gives no word/line counts at all, so length cannot be confirmed short from the counted facts available. |
| Maintenance burden | 3 — Report states it "requires no runtime, CLI, or service to function — it just reads its own reference files and outputs text." | 1 — Depends on the external `orx` CLI existing and being callable; the report doesn't state whether that CLI is present or absent in this environment, only that it "must exist," so presence can't be confirmed from the report. |
| Specificity | 3 — Named rubric axes, a model catalog, effort-sizing and subagent-routing files, two concrete modes with fixed output templates, and a worked AWS-IaC example. | 3 — Concrete CLI syntax and flags, an explicit branch/frozen-node protection rule, a named companion skill it defers to, and a required brief content list ("project, relevant experiment and branch, metric, constraints, allowed compute, expected output, and 'a concrete definition of done'"). |

Neither candidate scores 0 on "Fit with the bar" — both are silent on parts of the three-behavior bar rather than contradicting them, per the reports.

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-b304dc9f | COMPLEMENT | Fills a gap in X's item: X assumes the decision to delegate is already made and gives no guidance on which model/effort to use or whether inline vs. subagent is warranted in the first place. |
| item-fcc7bb6a | COMPLEMENT | Fills a gap in Y's item: Y explicitly disclaims the spawn/execution mechanics and produces no guidance on branch protection, compute authorization, concurrency handling, or brief content once a subagent call is chosen. |

### Deciding criteria

Specificity and Fit with the bar settled the rows: both items are concrete and detailed but cover non-overlapping halves of the delegation problem (routing/sizing vs. safe execution/scoping), so neither supersedes or is redundant with the other.

### What I could not assess from reading alone

Neither report shows the actual reference files in full (rubric text, model catalog, or the `orx-lit-review` companion skill), so I can't verify how well the rubric axes actually discriminate cases, whether the model catalog stays current, or how strict the `orx` CLI's concurrency enforcement is on refusal. A behavioral test would need to show: (1) whether the Y skill actually stops and asks when mode is genuinely ambiguous versus silently defaulting, (2) whether X's brief requirement is enforced by anything other than the writer's diligence, and (3) what happens in practice when the `orx` CLI's concurrency limit is hit — does the agent reliably wait/do-it-locally as instructed, or attempt a workaround. I have no basis to identify either candidate's origin and did not attempt to.
