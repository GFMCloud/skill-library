### Steelman X

item-979f7ecc directly operationalizes "plan, then stop" and "say what was/was not checked" as *file-level mechanics*, not just prose ideals. The fit test is a real stop-and-decide gate before any scaffolding happens, and the generated `/hypothesis` → `/run` split makes the predict-before-execute discipline structural: a run cannot proceed unless a `created` timestamp on the Prediction predates the run, and an empty Prediction is a hard refusal ("Do not fill in a prediction now and then immediately run"). The `dead-ideas.md` check prevents re-litigating refuted hypotheses, the holdout is frozen before any run, `REGISTER.md` is append-only, and the Result section explicitly demands raw output rather than interpretation. It has zero external runtime dependencies — it only needs the agent and its own templates — so it is trivially portable and low-maintenance.

### Steelman Y

item-5d659876 gives a genuinely concrete shape for managing *many* runs at once, which X's single-run-file model doesn't attempt: a baseline-rooted tree, "stacked bushes" branching so co-equal hypotheses fan as siblings rather than sprawling off the root, and a four-move vocabulary (Repair/Refill/Promote/Stop) with numeric stop conditions (repair cap of two dead-end runs on one node, ~3 consecutive failed/regressed runs overall). Its evidence discipline is explicit and strong — "actually read its results with `orx logs <runId>`... Don't infer from status alone" — which directly satisfies "executed evidence before done" with a named anti-pattern it forbids. The `orx exp wait` pattern is documented correctly as a "sleep-until-change signal, not the source of truth," showing awareness that a wait command finishing isn't itself evidence.

### Scores

| Criterion | item-979f7ecc (X) | item-5d659876 (Y) |
|---|---|---|
| Fit with the bar | **3** — explicit predict/execute separation ("the gate is exactly this separation"), raw-output Result requirement, and a Verdict that must state confirmed/refuted/inconclusive with sample size. | **2** — evidence handling is strong ("Don't infer from status alone"), but plan-then-stop is only partial: the report states the loop "launch[es] rounds, wait[s], and refill/promote autonomously without a stated checkpoint before each new launch," and the turn-end summary covers what was tested but "does not itself instruct stating what was not checked." |
| Enforcement mechanism | **0** — report states explicitly "no executable script, hook, or CI check in the files... nothing outside the agent's own compliance enforces this (no linter, no hook)," and the doctrine itself calls the gate "a file-existence check, not a promise." | **0** — report states "Prose only. There is no script, hook, or exit-code check inside the file," and the external `orx` subcommands are "not shown to fail closed or open here." |
| Context cost | **2** — no explicit token/line counts are given in the report to score precisely; structurally it declines to load for out-of-scope work (on-demand trigger, explicit fit-test refusal), but scaffolds six persistent files plus two generated sub-skills that a later session would re-read. | **2** — same caveat, no counted figures given; it is on-demand per frontmatter and keeps sibling-skill content (git, evidence, compute, reports, session playbook) out of this file by deferring to them by name rather than inlining them. |
| Maintenance burden | **3** — report states "None named — no runtimes, CLIs, or services are referenced," only the agent and its own templates. | **1** — report states it "assumes and references an external `orx` command-line tool and its subcommands, a private Git worktree," and several sibling skills/documents "none of these referenced items are included in this file set," so presence in the target environment is unconfirmed rather than affirmatively absent. |
| Specificity | **3** — concrete fit-test conditions, freeze-before-run rule, append-only register, placeholder-grep verification step, dead-ideas match-and-confirm rule, timestamp gate. | **3** — concrete repair cap (two dead-end runs), stop condition (~3 consecutive failed/regressed runs), stacked-bushes shape rule, four-move taxonomy, "read logs, don't infer from status" rule. |

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-979f7ecc | COMPLEMENT | Fills a gap in item-5d659876: an explicit, structurally-gated predict-before-execute separation (timestamp check, empty-Prediction refusal) and a holdout-freeze/dead-ideas-dedup discipline that the Y report never describes. |
| item-5d659876 | COMPLEMENT | Fills a gap in item-979f7ecc: multi-run tree/branching structure with numeric stop and repair-cap conditions, and an explicit "read the logs, don't infer from status" evidence rule for handling many concurrent runs, which X's single-run-file scaffold doesn't address. |

### Deciding criteria

Fit with the bar and Specificity settled the rows: each item is strong on different halves of the bar (X on plan-then-stop/checked-vs-not, Y on executed evidence) with equally concrete, non-generic mechanics, so neither supersedes the other — they cover different failure modes of the same slot.

### What I could not assess from reading alone

Neither report shows the prose-only "gate" actually being followed or violated in a live session — a behavioral test would need to try to make each agent skip the predict-before-run separation (X) or launch an unreviewed round without a checkpoint (Y) and see whether it actually refuses. For Y, it's also unconfirmed whether the `orx` CLI and the five deferred sibling skills/documents are actually present and working in the target environment, which the maintenance-burden score above flags as unconfirmed rather than proven absent. For X, it's unconfirmed whether the two generated sub-skills (`/hypothesis`, `/run`) reliably load and enforce their gates once handed off to a separate later session, since the scaffolding skill itself never executes them. I did not form a view on where either candidate came from.
