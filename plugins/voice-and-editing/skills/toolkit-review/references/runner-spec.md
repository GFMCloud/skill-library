# Runner script spec

Every headless or container call in a run is one simple command through a script in
`scripts/`, with no `cd ... &&`, no inline variable assignment, no loop and no pipe,
which are the shapes the permission classifier blocks (global `CLAUDE.md`, classifier
section). Output goes to files, never through a pipe.

Every script reads the run directory from `TR_RUN` and the run's parameters from
`$TR_RUN/run.json` (`templates/run.json` lists them). `scripts/prove-scripts.sh` proves
each script by deliberate failure with no model call; run it before the first wave of any
run.

`headless.sh <profile> <cwd> <model> <prompt-file> <output-file> <label> [flags]` is the
core every model-calling runner goes through. Profiles: `clean` (the judge flags below),
`bare` (no settings, read-only tools), `current` (default settings, read-only tools),
`open` (default settings and tools, negative controls only). Exit codes: 0 ok, 2 bad
arguments, 3 stalled, 4 rate limited, 5 empty or model-reported error, 6 `claude` failed.
`run-hook-bench.sh` exits 7 when refused. `TR_CLAUDE` names the binary so proofs can
point it at a stub.

Common rules:

- Arguments are positional. The script does its own `cd`. It wraps the call in
  `timeout <timeout_s>`.
- With `--output-format json`, the script saves the raw JSON beside the output as
  `<output>.json`, stderr as `<output>.stderr`, and extracts the reply text with `jq`.
- It appends one tab-separated line to `$TR_RUN/budget/usage.tsv`: timestamp, label,
  profile, model, input tokens (including cache reads), output tokens, status.
- Exit non-zero on: timeout (`stalled`), a non-zero exit from `claude` or `docker`, an
  empty output file, or a 429 in stderr or in an error result (`rate-limited`; the reply
  text is not searched, because a report that discusses rate limits is not a 429).
- No script reads, writes or echoes a credential. Container runs pass no host environment.
- `run-wave.sh` copies `scripts/` into `<log>.bin/` before the first job and every job
  runs from the copy, so an edit to the scripts cannot reach an in-flight run. The copy
  finds `references/` through `TR_SKILL_DIR`, which the wave runner exports; a runner
  called directly falls back to its own skill directory.

The judge flags (extractors, judges, readers):

```text
claude -p "<prompt>" --model <model> \
  --setting-sources "" --restricted --strict-mcp-config \
  --permission-prompts none --tools "Read,Glob,Grep" \
  --no-session-persistence --output-format json
```

| Script | Arguments | cwd | Prompt | Output |
|---|---|---|---|---|
| `run-extractor.sh` | slot, side | `slots/<slot>/<side>/` | `references/extraction-prompt.md` with slot, purpose and that side's facts rows | `extracts/<slot>/<X, Y or R>.md`; letter from `private/map.json`, `R` for a one-sided slot |
| `run-judge.sh` | slot, order (`XY`, `YX`, `ESC`, `S1`, `S2`) | `extracts/<slot>/` | `references/judge-prompt.md` or `references/self-review-prompt.md`; `ESC` uses the escalation model; a `challenge-*` slot gets `references/judge-challenge-note.md` | `judgments/<slot>/judge-<order>.md` |
| `run-reader.sh` | chunk number | `readthrough/input/chunk-<n>/` | `references/reader-checklist.md` | `readthrough/report-<n>.md` |
| `run-fixture-arm.sh` | arm (`bare`, `current`, `current-plus-candidate`), run number | a fresh copy of `<run>/fixtures/review/repo/` | the fixed review task | `<run>/fixtures/review/runs/<arm>-<n>.md` |
| `run-hook-bench.sh` | side (`installed` or a source id) | run | none; each hook script against each event in `bench/events/`, one container each, `--rm --network none`, read-only mounts | `bench/results/<side>/<hook>__<event>.txt` |
| `run-wave.sh` | jobs file, log file | run | none | one log line per job; stops on the first exit 4 |
| `check-extract.sh` | path, optional source dir | any | none | exit 0 if the four sections and seven fields are present and no forbidden name appears |
| `check-judgment.sh` | path, optional `self` | any | none | exit 0 if the sections are in order and every row carries a valid v2 class with its id |
| `check-dot-claude.sh` | optional root and marker | any | none | exit 0 unless a file under `~/.claude` newer than the marker is on the denylist; exit 9 with a VIOLATIONS list otherwise |
| `sum-budget.sh` | optional extra tokens | any | none | totals against the ceiling; exit 8 at the stop percent |

Fixture arms use `--tools "Read,Glob,Grep,Skill,Agent"`: without `Skill` a run sees no
skills, without `Agent` it cannot invoke an agent (ECC run, Gate A row A4). Skill calls
are not visible in `--output-format json` results; that limit stands until the arm runner
captures stream output to a file (not built).

`run-hook-bench.sh <source id>` refuses to run unless `$TR_RUN/gate-a/rulings.md`
contains the line `auth_candidate_hook_bench: yes`. Prove that refusal before Gate A.
