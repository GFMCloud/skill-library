# Decisions: placebo

contract: v1
source: https://github.com/Tuleeeee/placebo
type: code-repo
pin: da03cc2a5f3015eb9eb38d41b39bafa9945c6987 (2026-09-26 02:27 +0700, "Initial release: placebo 0.1.0"; shallow clone; Apache-2.0; 1 star, created 2026-09-25)
reviewed: 2026-09-28
verdict: HARVEST
recheck: -
evidence: maintainers/reviews/2026-09-28-placebo/cleanroom-review.md, maintainers/reviews/2026-09-28-placebo/comparison.md

## Verdict reasoning

A one-commit Python CLI that runs a three-arm A/B (baseline, skill installed, sham with the
same description and an inert body of equal length) on tasks mined from the repo's own
commits, with a two-level bootstrap and a TOST equivalence test so "no effect" is a
positive finding. The mechanism is verified in code by the clean room; the comparison found
it fills three of the four things Q-2026-09-14-1 planned to build (trigger recall, restraint
as false-trigger rate, a with/without ablation arm). Not ADOPT: one commit, one anonymous
author, it runs a paid agent with Bash allowed in a worktree that is not a sandbox, and its
grading can be gamed through files outside the test list. HARVEST: the method and two
fragments, and a pointer to the tool from the eval queue. What would change the verdict: a
second maintainer and a release history, or the placebo scan proving useful on the library.

## Ancestry

none. No shared files, names, or prose with eval-harness, toolkit-review, or
skill-discovery; both cite arXiv 2608.14036 independently.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour, one sitting | `M` an afternoon, one PR | `L`
multi-session, or a merge under the 500-line body cap with more than a handful
of edits; L always goes through `phased-harness`.
Adoption cost is mandatory and never "none": what this adds to the maintenance
surface and how it gets backed out.

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `placebo trigger` (recall, false_trigger_rate) and `placebo ab` (baseline vs treatment) as the reference implementation for the first `claude plugin eval` suite | COMPLEMENT | Name the repo and pin on Q-2026-09-14-1 as the implementation to evaluate before building trigger, restraint, and ablation cases from scratch; the tool runs the agent itself, so it is a candidate to run by hand in a throwaway worktree, never from a scheduled cycle | `src/placebo_cli/engine/trigger.py:91-149`, `engine/arms.py:97-99`, `stats.py:215-222` | `STATE.md` queue entry Q-2026-09-14-1 (this project) | S | one more external tool in a queue note; backed out by deleting the sentence | proposed (Tier 1 here: a queue note) | scout |
| 2 | "No effect" as a positive finding: equivalence testing instead of eyeballing three trials | SUPERIOR SUBSTITUTE (needs code, not prose) | Replace the Metrics clause "Read a before/after difference against noise ... At k=3 one flipped trial moves a case's pass fraction by a third" with an equivalence concept: state the delta you would call "no effect", and report PLACEBO only when the interval sits inside it; a prose model cannot hand-compute a 4,000-resample bootstrap, so either ship a trimmed `stats.py` as a script the skill invokes or name a closed-form interval | `stats.py:9-11`, `stats.py:193-238`; incumbent `eval-harness/SKILL.md:85-88` | `plugins/foundry-core/skills/eval-harness/SKILL.md` (Metrics) | S for the prose, M with a script | a formula the skill must keep right; backed out by restoring the clause | proposed (Tier 3: incubator body) | Graham |
| 3 | Sham-arm control for context effects | COMPLEMENT | One clause in the Graders section: when the change under test adds text, run a third arm with the same length of inert text so a gain over baseline that the sham also shows is attributed to context, not content | `engine/arms.py:1-8`, `METHODOLOGY.md:16-25` | `plugins/foundry-core/skills/eval-harness/SKILL.md` (Graders) | S | one more arm per eval (k more trials); backed out by deleting the clause | proposed (Tier 3: incubator body) | Graham |
| 4 | Whole-library description collision scan (TF-IDF cosine over name plus description, threshold 0.35) | COMPLEMENT | A pre-flight step referenced from toolkit-review before Step 4, or a maintainer note to run a collision scan against `~/skill-library` periodically; the 76-skill inventory sits inside the range where arXiv 2608.14036 measured routing precision collapsing | `static/collisions.py:79-113` | `plugins/voice-and-editing/skills/toolkit-review/SKILL.md` (pipeline, before Step 4) | S (the reference) | running it means `pip install placebo-cli`, an install, so the scan itself is Tier 3; backed out by removing the step | proposed (Tier 3: incubator body plus an install to run it) | Graham |
| 5 | Judgment-primary vs execution-primary grading: eval-harness ranks a model grader "a second opinion, not a measurement"; toolkit-review's slot verdict is computed from two judges' prose rows | philosophy conflict, INGESTIBLE FRAGMENT | One paragraph in toolkit-review's history.md beside "what it cost" naming the disagreement and that placebo sides with eval-harness; no behavior change | `METHODOLOGY.md:22-25`; incumbents `eval-harness/SKILL.md:61-67`, `toolkit-review/SKILL.md:23-24`, `references/limits.md:24-25` | `plugins/voice-and-editing/skills/toolkit-review/references/history.md` | S | one paragraph to keep true; backed out by deleting it | proposed (**fits Tier 2 as written**: effort S, INGESTIBLE FRAGMENT, a references/ file of an incubator skill, from a clean-room decisions row; flag off, so Tier 3) | Graham |
| 6 | Interleave arms against drift (shuffled task-arm pairs per round, seeded) | COMPLEMENT | One sentence in eval-harness's trial procedure: when a run spans hours, interleave arms rather than running all baselines first | `engine/runner.py:61-76` | `plugins/foundry-core/skills/eval-harness/SKILL.md` | S | none beyond the sentence; backed out by deleting it | proposed (Tier 3: incubator body) | Graham |
| 7 | NOT_ACTIVATED: do not score a skill that never triggered (activation rate under 30%) | COMPLEMENT | Note on toolkit-review's limits.md line 17 ("Skill calls are invisible in `--output-format json`") that `stream-json` `tool_use` events name the skill, which is how placebo measures activation | `adapters/claude_code.py:104-108`, `stats.py:204-209` | `plugins/voice-and-editing/skills/toolkit-review/references/limits.md` | S | none beyond the note; backed out by deleting it | proposed (references/ of an incubator skill, from a decisions row: also fits Tier 2 as written; flag off, Tier 3) | Graham |
| 8 | Circuit breaker and `agent_error` exclusion | REDUNDANT | eval-harness's "fails identically twice for an environmental reason: report `not runnable`" is narrower and safer; placebo's version drops immediate failures a skill may have caused (clean room 4a-3) | `engine/runner.py:153-158, 261-264` | - | - | - | out | - |
| 9 | Task mining from commits that changed source and tests, validated fail-before pass-after | COMPLEMENT, outside scope | eval-harness disclaims product-code testing; no consumer here | `tasks/git_miner.py:128-156` | - | - | - | out (noted) | - |
| 10 | Publishing norms for results about someone else's skill | COMPLEMENT | Only if a toolkit-review ledger is ever shared outside this machine | `METHODOLOGY.md:109-113` | - | S | - | out (no consumer) | - |
| 11 | README statistics (39 of 49 skills, +1.2%, 451% tokens, SWE-Skills-Bench, arXiv 2603.15401, 2608.11888) | claim, unverified | Run `verification-kit:fact-currency-check` before any of these numbers is quoted in the library; 2608.14036 is already queued (Q-2026-09-03-11) | `README.md:20-24` | - | S | - | proposed (a check, not a change) | next cycle |

## Conflicts for the user to rule on

1. Row 5. "Code grader ... Model grader ... it is a second opinion, not a measurement"
   (eval-harness) against "the judges see neutral reports and never the files ... the slot
   verdict is computed from their per-item rows" (toolkit-review). Proposal: record the
   disagreement in history.md and leave both skills as they are (toolkit-review's fixture arm
   is the execution layer it has). Alternative: add an executed arm to toolkit-review's
   `full` slot type using placebo's trigger and ab commands, effort M, with an install.

2. Row 4 versus the install rule. The collision scan is free and offline but needs
   `pip install placebo-cli`. Proposal: reference the idea now; install only by ratify.
   Alternative: write a 40-line TF-IDF collision script of our own under
   `maintainers/scripts/` (no install; effort S) and skip the tool.

## Corrections at ingest

- `engine/arms.py:84` comment "count referenced resources too" documents behavior the code
  does not have (the sham writes only SKILL.md; `METHODOLOGY.md:17` discloses it). Do not
  copy the comment.
- The TOST idea cannot be adopted as prose alone (row 2).
- Strip the README register (emoji title, comparison table, "SkillBench" branding) from any
  fragment.
- `trigger` and `ab` run a real agent with `--permission-mode acceptEdits` and Bash allowed
  (`adapters/claude_code.py:12, 73`); a worktree is not a sandbox. Never run from a cycle.

## Flags

- `tests/test_skills_static.py:57` "Ignore all previous instructions.\n": a scanner fixture,
  not aimed at a reader.
- `cli.py:110-111` `placebo doctor` reports whether `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`,
  `CODEX_API_KEY` are set; names only, never values.
- `examples/skills/*/SKILL.md` are sample agent instructions by design; not read in full.
- Nothing addresses the reviewing agent.

## Rulings log

- 2026-09-28, scout cycle 6: all rows proposed; nothing applied. Row 1 is a Tier 1 queue
  note in this project's STATE.md (done this cycle). Rows 5 and 7 fit Tier 2 as written
  (flag off): the second and third such rows in six cycles.
