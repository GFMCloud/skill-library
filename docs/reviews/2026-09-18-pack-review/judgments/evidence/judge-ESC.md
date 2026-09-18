### Steelman Y
item-b9504c3e deals with a failure mode that generic verification advice misses: a long run whose log cannot be judged afterward. It works at both ends of the run. Before launch, it tells the agent to make the command print the effective configuration, "periodic one-line metrics", and "final metrics and a compact summary block at the end of the run". After the run, it tells the agent how to read the log back with `orx logs --head/--bytes/--range`. Before any claim from a run is reported, it lists four things to confirm: the log identifies the variant, the final metric and summary are present, the trajectory can be recovered, and the byte window read actually contains the supporting output. Two of its lines go straight at the bar: "Never infer a result from run status or memory" and "Truncated output is not evidence of absence." It is one on-demand skill with no scripts, so it is cheap to carry.

### Steelman X
X covers both halves of the slot, and each half comes with executable enforcement. item-7aed43c3 defines executed evidence for several kinds of artifact. It rejects a tool's own success message as evidence, citing three prior cases where one was wrong. It requires the check to be declared before each step runs. Its `run-checks.sh` records a real exit code for each phase, marks a phase "not-run" rather than passed when no exit code was captured (a tamper case is tested), and is itself tested against green, red and absent-tool fixtures. item-92c76be2 turns results into CLAIM/CHECK/OUTPUT/VERDICT blocks with quoted output and an identifier per claim. It also requires a NOT VERIFIED section even when nothing was skipped, and `check-report.py` exits 1 when that section is missing. X is candid about its own limits: the report checker cannot tell whether a CHECK was actually run, and "A green sequence with no run of the new behavior is not evidence for it."

### Scores

| Criterion | Y | X |
|---|---|---|
| Fit with the bar | 2: It supports executed evidence ("Never infer a result from run status or memory") and ignores plan-then-stop, but it only "partially supports" stating what was checked, because it defers that to an absent "evidence-and-links contract". | 3: Neither item conflicts with plan-then-stop, 7aed43c3 is central to executed evidence, and 92c76be2 makes the NOT VERIFIED list mandatory even when empty. |
| Enforcement mechanism | 0: The report says "Prose only — no executable checker, hook, or script… Nothing blocks, warns, or exits non-zero." | 2: `run-checks.sh` and `check-report.py` both exit non-zero on failure and the runner is fixture-tested, but "nothing in the files shows this script being invoked automatically". |
| Context cost | 2: It is one skill "loaded on-demand by its description. Not always on", but the report gives no counted length, so I could not score size. | 2: Both skills load on demand ("Not always on"), and the report gives no counted length, so I could not score size. |
| Maintenance burden | 1: It depends on the `orx` CLI and on a "session playbook" that "is not included". The report does not say orx is present. | 2: It depends on bash, python3, node, npm and gh. None is reported absent, but the report could not find any use of gh. |
| Specificity | 3: It gives a four-point confirmation list before reporting, exact `orx logs` flags, and a named failure mode: truncated output read as absence. | 3: It gives fixed report fields, an ordered phase sequence (build/types/lint/tests/secrets/diff), stop phases, exit codes 0/1/3, and a named fallback for checks that genuinely cannot be run. |

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-b9504c3e | FRAGMENT -> item-7aed43c3 | Not wanted whole, because it is prose only and relies on orx plus a missing playbook. Three sections would improve item-7aed43c3: the pre-run print design (effective config, periodic one-line metrics, final summary block); the four-point confirmation before reporting a run-derived claim; and the rule "Truncated output is not evidence of absence", with its instruction to keep reading until the relevant portion has been read. |
| item-92c76be2 | COMPLEMENT | Fills Y's gap on stating what was and was not checked. Y defers that to an "evidence-and-links contract" that is absent. This item defines the report format, including a mandatory NOT VERIFIED section, and a checker that exits 1 when the format is broken. |
| item-7aed43c3 | COMPLEMENT | Fills Y's gaps on non-log evidence (diffs, tests, deployments, config), on what to do when evidence cannot be produced, and on enforcement. Y has no script, while this item records a real exit code for every phase it runs. |

### Deciding criteria
Enforcement mechanism and Fit with the bar decided the rows. X backs executed evidence and the not-checked list with scripts that exit non-zero. Y is prose only and hands the not-checked reporting to a document the report says is absent.

### What I could not assess from reading alone
- **Whether the skills fire:** a behavioral test would need to show both X skills loading on "done" claims, and the agent actually running `run-checks.sh` and `check-report.py` rather than skipping them. X's report says nothing forces either invocation.
- **Fabricated output:** it would need to show whether a report with made-up OUTPUT but correct shape gets through, which X admits it cannot catch.
- **Y under truncation:** for Y, it would need to show the agent actually reading more byte ranges when output is truncated, rather than reporting from the tail.
- **Dependencies:** it would need to show whether `orx` and the session playbook exist in the owner's environment, and why X lists `gh`.
- **Size:** neither report gives a counted length, so I could not compare context cost on size.

I don't recognize the origin of either candidate.
