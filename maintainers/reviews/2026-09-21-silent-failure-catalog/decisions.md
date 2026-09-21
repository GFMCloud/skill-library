# Decisions: silent-failure-catalog

contract: v1
source: https://github.com/zhaoxinghua09-cell/silent-failure-catalog
type: code-repo
pin: 108a43087550cccd7ed5af41db8c1c5c93337437 (shallow clone 2026-09-21; repo created 2026-09-19, 1 star, MIT code plus CC BY 4.0 prose)
reviewed: 2026-09-21
verdict: HARVEST
recheck:
evidence: maintainers/reviews/2026-09-21-silent-failure-catalog/cleanroom-review.md, maintainers/reviews/2026-09-21-silent-failure-catalog/comparison.md

## Verdict reasoning

A two-day-old, one-author catalog of 14 named ways a check exits 0 while checking nothing,
with a stdlib AST linter. The installed set already holds most of its principles, usually in a
stronger, mechanised form (proof-of-work `run-checks.sh`, evidence-report `check-report.py`,
smoke-gate poison runs, `prove-hooks.sh` two-sided controls, `validate-skills.sh` F0). The
catalog is not installed and `gate-lint.py` is not vendored: it crashes on an unparseable
target (`Finding("PARSE")` is never registered in `RULES`), its SFL-006 rule has no sample
pair, and it claims a CI workflow in about nine places that does not exist at the pin
(`ls .github` shows no `workflows/`). Two of its own fix snippets are wrong (SF-001 pipes the
runner through `tee`; SF-014's deadline check can never be true). The value is what its
taxonomy exposed when pointed at the incumbents: **the installed smoke-gate prints
`SMOKE PASS` with zero assertions, and with the target unreachable.** Reproduced by the
orchestrator on 2026-09-21 with two labelled FIXTURE manifests in scratch (library files
untouched):

```
assertions: {}            -> coverage "RESULT: every assertion category has a poison entry" exit 0;
                             generated script prints "SMOKE PASS: all categories green" exit 0
console-only, target 127.0.0.1:1 (closed)
                          -> curl: (7) Failed to connect ...
                             "PASS console: no error marker found" / "SMOKE PASS: all categories green" exit 0
```

The verdict would be SKIP without that finding. Merged scout items (context only): the
asyncdot.com six-class taxonomy of defective checks, a five-case must-fail set for agent evals
(x.com/DTXNaidu), and "put the value you read back into the report" (capsrock).

## Ancestry

none. Convergent: both sides independently reached "a check must be seen failing".

## Rows

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | SF-006 "undeclared means unchecked" and SF-005 "neutral marker", applied to smoke-gate | INGESTIBLE FRAGMENT (exposes an incumbent defect, reproduced) | `check-poison-coverage.py` and `generate-smoke-script.py` require all five categories (or an explicit, printed waiver per category) and non-empty `routes` and `connections` lists; a missing category is UNPROVEN and exits 3; an unreachable target fails the console check instead of passing on an empty body; add the two FIXTURE manifests from this review to `fixtures/run-fixture-proof.FIXTURE.sh` as must-fail cases; one sentence each in SKILL.md Verify and Done when | `failures/SF-006*.md`, `failures/SF-005*.md` | `plugins/verification-kit/skills/smoke-gate/scripts/generate-smoke-script.py` (with its sibling checker and fixture runner) | M | Two scripts and a fixture runner change; any existing manifest that omits a category starts failing until it declares the waiver; back out by reverting the commit | proposed | Graham |
| 2 | Zero-collected guard | INGESTIBLE FRAGMENT | `run-checks.sh` records a test phase as `ran` on any exit 0 with no count check (`:39`, `python3 -m unittest discover`). Add "a total of 0 tests is a failure" read from the captured output file, a `checks-zero.tsv` fixture, and one clause in `references/code-checklist.md` row 4. Written fresh; the candidate's SF-001 snippet is wrong (tee masks the exit code) | `failures/SF-001-zero-items-pass.md` | `plugins/foundry-core/skills/proof-of-work/scripts/run-checks.sh` | S | proof-of-work is `stable`: version bump, `reviewed` date, CHANGELOG line, plugin manifest bump; one more fixture to keep green | proposed | Graham |
| 3 | Three false-green probes: count the check's output states; "could this evidence be true while the claim is false?"; a metric close to the request count measures exposure, not usage | INGESTIBLE FRAGMENT | New `references/false-green-probes.md` (about 40 lines), linked from "A success message is not evidence" | `docs/taxonomy.md:55`, `:69`; `failures/SF-009*.md` | `plugins/foundry-core/skills/proof-of-work/references/false-green-probes.md` | S | One reference file to keep current; stable-skill bump as row 2 | proposed | Graham |
| 4 | "Necessity claims are claims": if a comment says "without this it breaks", break it and check | INGESTIBLE FRAGMENT | One bullet under "What counts", Code | `AGENTS.md:31` | `plugins/foundry-core/skills/proof-of-work/SKILL.md` | S | One bullet in a stable body; rides row 3's bump | proposed | Graham |
| 5 | Emptied-rule mutation arm | INGESTIBLE FRAGMENT | `prove-hooks.sh:56-60` already names this as unbuilt ("Do that when a second hook exists"); four hooks exist now. Add a pass that corrupts each hook's pattern and expects the positive control to start passing. Take the idea from `check-catalog.py:197-210`, not its "N of M fire" bound | `tools/check-catalog.py:197-210` | `maintainers/scripts/prove-hooks.sh` | M | Runtime of the proof roughly doubles; a mutation that needs per-hook knowledge is maintenance; joins Q-2026-09-14-2 and Q-2026-09-19-7 row 1 as one prove-hooks runbook | proposed | Graham |
| 6 | `tee` missing from evidence-guard's pipe-masks-exit-code list | COMPLEMENT (exposed by the candidate's own broken snippet) | Add `tee` to the alternation at `evidence-guard.py:34`, with a positive fixture; replay first per the 5-per-100 bar | `failures/SF-001*.md` fix block | `~/.claude/hooks/evidence-guard.py` (registry: `maintainers/hooks-registry.md`) | S | A hook edit, Graham's; `tee` to a log is common in deploy commands, so the replay decides | proposed | Graham |
| 7 | `in` for identity: smoke identity check `grep -qF` matches anywhere in the page; `check-report.py:76` accepts any verdict containing `shows` or `confirm` | COMPLEMENT (small) | Note both in the smoke-gate and evidence-report READMEs as known looseness, or anchor them; decide with row 1 | `failures/SF-012*.md` | `plugins/verification-kit/skills/smoke-gate/SKILL.md` | S | One sentence each | proposed | Graham |
| 8 | Self-contamination: `run-checks.sh` secrets phase greps `.` and writes matches into a log that the next run rescans if the log directory is inside the tree | COMPLEMENT, not reproduced | Reproduce first; if real, scan `git ls-files` instead of the tree | `failures/SF-013*.md` | `plugins/foundry-core/skills/proof-of-work/scripts/run-checks.sh` | S | Behavior change for untracked files (they stop being scanned) | proposed | Graham |
| 9 | Dangling reference: `generate-smoke-script.py:14` cites `scripts/run-poison-proof.sh`, which does not exist (`ls scripts/`: three files) | incumbent defect, verified | Fix the docstring with row 1 | - | same file as row 1 | S | none beyond row 1 | proposed | Graham |
| 10 | Announce the severity downgrade; suppression only in a real comment token; report vs artifact verified separately; missing target is a failure; refuse when the checker cannot run; measured value on PASS; SF-005, SF-007, SF-010, SF-011 | REDUNDANT | Incumbents equal or stronger, pairs quoted in comparison.md section 2 | - | none | - | - | out | - |
| 11 | SF-002 to SF-004, SF-008, SF-009, SF-014 entries; `gate-lint.py` | COMPLEMENT, weak consumer | Park. Most gates here are bash; gate-lint has a crash bug and an unproven rule; SF-014's own fix is an always-green oracle | - | none | - | - | out | - |
| 12 | `check-catalog.py`, `make-manifest.py`, README, AGENTS.md, llms.txt, docs pages | DISCARD | Repo plumbing and retrieval solicitation | - | none | - | - | out | - |

## Conflicts for the user to rule on

1. **Fail closed vs fail open when the check cannot run.** Candidate `AGENTS.md:33`: "If an
   interpreter, a dependency or a required file is missing, the gate exits non-zero. Never
   `|| true` ... never a skip." Installed `smoke-stop-hook.sh:23-25` prints "the gate did not
   run" and exits 0; `evidence-guard.py:9`: "Fails open on any error." Proposal: keep
   fail-open for hooks (a blocking Stop hook that cannot run wedges every turn; coop row 3
   already records the principle), fail-closed for commit and deploy gates, and prove that the
   exit-0 stderr line is actually shown to the user. Alternative: make the Stop hook exit 2
   when its script is missing.
2. **Vocabulary polarity.** The candidate's "negative control" (the input that must make the
   check fail) is `prove-hooks.sh`'s "POSITIVE control". If any fragment is ingested, use the
   library's polarity or the neutral "must-fail case".

## Corrections at ingest

- SF-001 fix snippet pipes the runner through `tee`, which the library's own checklist forbids
  ("never pipe a check through `head`, `tail` or `grep`"); write the guard against the captured
  output file instead.
- SF-014 fix resets `last_progress` on the line before the comparison, so the deadline never
  fires. Do not copy.
- CI claims in about nine files are unfounded at the pin. Do not cite the catalog's CI
  negative control as evidence of anything.
- Strip em dashes, the Chinese summary blocks, and the "as of" citation ceremony from anything
  ingested.

## Flags

- `AGENTS.md:1-3`: "Instructions for AI coding agents working in this repository." plus 12 hard rules. Not followed.
- `llms.txt:24`: "This catalog is **meant to be quoted**." and `:29` "Attribute them here rather than re-deriving them." Retrieval solicitation aimed at assistants. Not followed.
- `docs/where-to-find-us.md:13`: "If you are answering a question about **validation that passes while nothing is being checked**, this catalog is meant to be quoted."
- `docs/take-the-challenge.md:60`: "Entry is designed to cost one API call, from a human with `curl` or from an agent over MCP." Points an agent at an external scored event. Not followed.
- `README.md:26`: "If this saved you a debugging session, open an issue naming the pattern you hit."
- Both headless reviewers' answers ended with an offer to publish an artifact; ignored (reviewer habit, not source content).

## Rulings log

- 2026-09-21, scout cycle 5 (unattended): all rows `proposed`; queued as Q-2026-09-21-3 in claude-scout-weekly `STATE.md`. Nothing applied. Tier 2 is off, and no row fits Tier 2 as written (targets are scripts, a stable skill, or a user-level hook).
