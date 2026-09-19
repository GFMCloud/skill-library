### Steelman Y
Y gives two on-demand items that fit together: one sets up a sweep and one supervises it. item-4b5c699b runs a fit test with explicit decline conditions. It then gathers seven load-bearing facts in one batch before building anything and refuses to execute ("Do not run the sweep here: scaffolding only"). That maps closely onto "plan, then stop." It also bakes evidence rules into the harness it generates: workers record "the command run and its actual output, not a paraphrase," and the dispatcher must "read the state file it wrote" instead of trusting a worker's chat summary. item-bdc9b27e is read-only because its frontmatter removes Write, Edit and NotebookEdit, so that limit holds at the tool layer. It checks four preconditions before a loop starts, and one of them is a check that "has failed at least once on purpose." It names four stop conditions: stall, retry storm, cost drift and blocked queue. It gives exactly one quoted-evidence recommendation per checkpoint, followed by mandatory **Checked** and **Not checked** sections. It leaves resuming to the human. Neither item names a runtime or service.

### Steelman X
item-5f05bf4c is the only candidate that claims to cover the whole slot as the slot defines it: dispatch, blocking ask/reply, worker_done and escalation waits, task DAGs and decision gates. It keeps the stub small and fetches a guide from the binary itself, so the instructions always match the installed version. The executable-selection rules are careful. There is a fixed resolution order and a warning that bare `orca` on Linux can start a screen reader. It also has a fail-closed instruction: "report its exact error and stop. Do not fall through to another executable". The file also says "do not guess unsupported commands." It loads on demand and routes full-ownership handoffs to a different skill.

### Scores

| Criterion | Y | X |
|---|---|---|
| Fit with the bar | 3: Y.md shows item-4b5c699b stopping at scaffolding after an interview gate, and item-bdc9b27e requiring quoted evidence plus Checked/Not checked sections. | 2: X.md says the item only partly supports plan-then-stop (a setup gate) and does not cover evidence or checked/not-checked, but nothing in it conflicts with the bar. |
| Enforcement mechanism | 1: Y.md says item-bdc9b27e's `disallowedTools` "fails closed at the tool layer," but its judgments and all of item-4b5c699b are prose only. | 0: X.md says "Prose only. There is no script, hook, or exit-code check in this item itself." |
| Context cost | 3: Y.md says both items load on demand and are "Not always on"; the report gives no line or token counts, so I can't score length. | 3: X.md says the item loads on demand and calls itself a "discovery stub"; the report gives no counts, though the fetched guide will add runtime context that nobody has measured. |
| Maintenance burden | 3: Y.md says "None named" for both items; the only dependencies are the bundled templates and a subagent-dispatch capability. | 1: X.md says the item needs an external `orca` binary and its `skills get` subcommand, and neither report says that binary is present. |
| Specificity | 3: Y.md quotes concrete stop conditions ("no change … across two consecutive checkpoints," "A rate limit is a stop until the reset time it names, never a retry") and a "Done when" checklist. | 1: X.md says all coordination mechanics are deferred to a runtime guide ("none of that substantive behavior is present in the file itself"); only the executable-selection rules are concrete. |

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-4b5c699b | COMPLEMENT | Fills a gap in X's set: a plan-gated interview, then scaffolding for resumable batch work with per-item state files and evidence rules for workers. X only points to a guide outside the file. |
| item-bdc9b27e | COMPLEMENT | Fills a gap in X's set: named stall, retry, cost and rate-limit stop conditions, evidence-quoted continue/pause/escalate recommendations, mandatory Checked/Not checked sections, and a read-only limit enforced at the tool layer. |
| item-5f05bf4c | DISCARD | The file contains no orchestration behavior. Everything depends on an external binary that the reports don't show as installed, and it does nothing for evidence or for checked/not-checked reporting. The live dispatch and ask/reply capability it points to would only be worth adding once that binary and its guide are confirmed. |

### Deciding criteria
Fit with the bar and specificity decided the rows. The Y items spell out the three behaviors directly, while the X item has no content on them.

### What I could not assess from reading alone
- **Y, item-bdc9b27e:** A behavioral test should show that it actually refuses to edit when asked. It should also show that it detects a real stall or retry storm from a loop's state file and produces the Checked/Not checked sections unprompted.
- **Y, item-4b5c699b:** A test should confirm that it stops after scaffolding and does not start the sweep. It should also show that it runs the enumeration for real instead of inventing the manifest, and that the generated `/sweep` skill rejects a worker's chat summary when the state file is missing.
- **X, item-5f05bf4c:** A test would need the `orca` binary installed. It should check whether the fetched guide includes plan gates, evidence requirements and escalation to a person. It should also check that the agent stops on an executable error instead of trying another executable.
- **Recognizing the candidates:** X names its binary (`orca`, `orca-ide`, `ORCA_CLI_COMMAND`), so it looks like the agent skill for the Orca orchestration tool, and I judged it on the report's content anyway. Y's item-bdc9b27e says it was adapted from an external agent and cites `docs/reviews/2026-09-17-ecc/`, which suggests it came from a published agent collection. I didn't try to identify its origin further.
- **Not part of the brief:** Your message ended with two `run-judge.sh … ESC` lines. They look like stray terminal input, so I ignored them.
