# Standing limits of the evidence

Print these in every ledger's limits section. Each was measured, not assumed; re-measure
the CLI ones with `verification-kit:fact-currency-check` on a new CLI version.

- **Context-clean, not blind.** Judges read neutral extraction reports and never the
  source files, but a judge's context still holds the owner's email address (the
  `userEmail` block survives `--setting-sources ""`, `--restricted` and `--safe-mode`; CLI
  2.1.274, 2026-09-17) and the run directory path. Neither ties a report to a side. Keep
  the run path free of the owner's and the project's names.
- **A judge may guess at origin from content.** One of fourteen ECC judges did, from
  references to a model name and a phase number inside a report, and said it judged on
  content anyway. The ledger quotes any such statement.
- **Agreement on a verdict is not agreement on the rows.** Two judges can derive the same
  slot verdict and name different items; the ledger prints per-item agreement and "named
  to take" counts beside every verdict.
- **Skill calls are invisible in `--output-format json`.** "Did the current setup trigger
  a review skill" cannot be answered from a fixture run's JSON result.
- **The bare arm is not skill-free.** With `Skill` in the tool list a `--setting-sources
  ""` run still sees Claude Code's bundled skills.
- **A hook bench with one container per event sees only first use.** A hook with
  first-use state (a gate that denies until initialized) denies every event, benign ones
  included. The stateful bench (one container per hook, events in sequence) is not built.
- **Fixture results are fixture-derived** and say nothing about real repositories. A
  fixture whose bare arm misses nothing cannot show an arm difference; the discrimination
  gate in `scripts/score-fixture.py` drops it before the arms run.
- **Item mapping is by id**, not position; an id a judge writes that is not in
  `items.tsv` is printed as ambiguous, never guessed.
- **Reads outside a judge's cwd are refused by two layers** (`--restricted`, and the
  permission layer under `--permission-prompts none`), so a "cannot reach the side map"
  proof has a passing control only for the map, not for an arbitrary outside file.
- **Claude Code writes under `~/.claude` on its own** at every interactive session start
  (plugin lock markers), on `~/.claude.json` changes (backups), and on plugin auto-update
  (the whole cache). `scripts/check-dot-claude.sh` exempts bookkeeping by denylist; a run
  that spans a plugin update expects the cache to change and re-baselines the marker with
  a ruling.
