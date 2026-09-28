# placebo: standalone review

## 1. Executive summary

- **What it is:** a Python CLI (`placebo-cli` 0.1.0, Apache-2.0) that tests whether an agent "skill" (a `SKILL.md` file) or an `AGENTS.md` file actually changes how often a coding agent succeeds. It uses three arms: baseline (no skill), treatment (the skill) and sham (same name and description, filler body). It also has a free static scan.
- **The core is real work, not glue.** Tasks are mined from git history and checked to fail before and pass after. Trials run in isolated worktrees in shuffled order. The statistics are sound: a two-level bootstrap, a TOST equivalence test, and an ordered set of verdict rules.
- **The README matches the code** on every point I checked. METHODOLOGY.md is candid about its limits, such as commit messages leaking hints and small samples.
- **Maturity is close to zero.** The clone is shallow with one commit ("Initial release: placebo 0.1.0"). CHANGELOG still says "0.1.0 (unreleased)". There is no history, so cadence and bus factor can't be judged.
- **Adoption cost is low:** 2 runtime dependencies, nothing listening on a port, and `pip uninstall` removes it. The running cost is real, though. `trigger` and `ab` launch a paid coding agent with Bash and auto-accepted edits.
- **Main correctness risks:**
  - Grading restores only the task's own test files, so an agent could make a task pass by editing `conftest.py` or `pytest.ini`.
  - The sham arm leaves out the skill's supporting files.
  - Runs that end as `agent_error` are dropped from the statistics.
- **Verdict:** a good idea, carefully built, and brand new. Worth trying on your own repo, and worth borrowing the method from. Nothing here should be a dependency yet.

**Files read:** `README.md`, `METHODOLOGY.md`, `CHANGELOG.md`, `LICENSE`, `pyproject.toml`, `.github/workflows/ci.yml`, `src/placebo_cli/cli.py` (entry point), `engine/runner.py`, `engine/arms.py`, `engine/workspace.py`, `stats.py`, `tasks/git_miner.py`, `adapters/claude_code.py`. I only counted the tests in `tests/`; I didn't read them.

## 2. Maturity signals

I had no shell in this session, so I read git metadata from the files under `.git/` rather than running `git log`.

| Signal | How I checked | What it returned |
|---|---|---|
| Last commit date | read `.git/logs/HEAD` | One entry: `clone: from https://github.com/Tuleeeee/placebo` at epoch 1790638004 (≈ 2026-09-28). That is the clone time, not the commit time. The commit date can't be read without git, because the objects are in a packfile. |
| Commit cadence (last ~50) | read `.git/shallow` plus the session's git status | `.git/shallow` contains `da03cc2…`, so this is a shallow clone. The only visible commit is `da03cc2 Initial release: placebo 0.1.0`. **Cadence can't be judged.** A full clone would be needed. |
| Distinct authors, last 12 months | same | Can't be determined. `pyproject.toml:13` lists `authors = [{ name = "Placebo contributors" }]`, a collective name with nobody identified. Assume one maintainer until shown otherwise. |
| Dependencies and their freshness | `pyproject.toml:31-34` | Runtime: `pyyaml>=6.0` and `rich>=13.7`, both mature and actively maintained. Dev: `pytest>=8`. Build: `hatchling>=1.24`. A `uv.lock` is present. The surface is very small. |
| License file | `LICENSE` | Standard Apache-2.0 text. The appendix placeholder `Copyright [yyyy] [name of copyright owner]` was never filled in. That's cosmetic, and the license is still valid. |
| Tests exist and CI runs them | Grep `^def test_` in `tests/`; `.github/workflows/ci.yml` | 42 test functions across 5 files (stats 9, e2e 10, static 12, miner 6, adapters 5), plus a recorded Claude Code trace fixture. CI runs `uv run pytest` on ubuntu, macOS and Windows × Python 3.10–3.13, plus a CLI smoke test and `twine check`. **CI config verified. Whether CI passes is not verified**: I can't see any run results. |
| Open issues | not reachable | There are issue templates (`bug.yml`, `feature.yml`, `new-agent-adapter.yml`) but no issue data offline. For a first commit, there are probably none yet. |

## 3. Claimed vs verified

**Verified in code**
- **Three arms, and the sham keeps name and description with a same-length filler body.** `arms.py:76-88` and `arms.py:95-107`. The filler is travel prose about lighthouses, tea and maps (`arms.py:23-41`).
- **Arms run in shuffled order, round by round, with a fixed seed.** `runner.py:61-76`.
- **Every trial gets a fresh git worktree.** `workspace.py:19-28`. Worktree creation is serialised with a lock (`workspace.py:14`).
- **The agent's edits to test files are reverted before grading.** `workspace.py:54-61`, called at `runner.py:159`.
- **Mined tasks must fail before the change and pass after it.** `git_miner.py:128-156`.
- **Two-level bootstrap, 95% and 90% CIs, a McNemar test on per-task majority outcomes, and TOST-style equivalence.** `stats.py:121-190`.
- **Verdict rules run in the documented order.** `stats.py:193-238` matches `METHODOLOGY.md:81-92` exactly. HELPS requires beating the sham (`stats.py:216`).
- **Budget, max-runs cap, and a circuit breaker.** `runner.py:249-264`. The breaker stops the run if the first two runs are both `agent_error`.
- **Resume.** Finished trials are skipped by key (`runner.py:234`).
- **Paid runs need confirmation and refuse to start without a TTY.** `cli.py:35-42`.
- **Flagged skills are refused.** `cli.py:162-165` and `cli.py:242-245`.
- **The baseline can't secretly see a user-level copy of the skill.** `cli.py:246-253`.
- **`--fail-on` exits with code 2.** `cli.py:76-79`.
- **The Claude Code adapter strips the parent session's environment variables but keeps auth ones.** `claude_code.py:53-63`.
- **CI runs pytest on a 12-cell matrix.** `ci.yml:18-30`.

**Claimed only (not verified by me)**
- **"Parser tested against real Claude Code 2.1.281 `stream-json` output."** The fixture file exists; I didn't read the test that uses it.
- **Codex adapter ("beta").** Not read.
- **Security scan rules, including decoding hidden Unicode-tag text.** I didn't read `static/security.py`. The Unicode ranges only appear in `security.py` and `skills/model.py`, which fits a detector. One test asserts four rule IDs (`test_skills_static.py:62`).
- **Collision scoring and the "real output" example in the README.** Not run.
- **The CLI flags `--permission-prompts none` and `--no-session-persistence`** (`claude_code.py:72-74`) are valid options of the installed `claude` binary. Not verified.
- **The research numbers in the README** ("39 of 49 skills", arXiv 2603.15401, 2608.11888, 2608.14036). Not checked.
- **The comparison table against other tools.** Marketing; not verified.
- **Published on PyPI and a green CI badge.** Not verified.

## 4. Rubric

| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Does what it says | **4/5** | Every mechanism the README describes that I traced exists and behaves as described. One point off because the sham claim ("inert body of the same length") skips supporting files and has a 200-character minimum (`arms.py:85`). |
| 2 | Quality of the interesting part | **4/5** | The experimental design is thoughtful: paired by task, with a sham, run order shuffled against drift, equivalence tested with TOST, and an explicit NOT_ACTIVATED verdict. The code is clean and readable. See section 4a for the gaps. |
| 3 | Adoption cost | **4/5** | Two mature dependencies, no daemon, no ports. Everything stays local in `.placebo/`, and `pip uninstall` plus deleting `.placebo/` removes it. The real cost is operational: paid agent runs, and a repo test suite that runs many times. |
| 4 | Failure modes | **3/5** | The agent runs with `acceptEdits` and `Bash` allowed (`claude_code.py:12`, `claude_code.py:73`). A worktree is not a sandbox. The README says so, and the refusal on flagged skills helps. The statistical risks (a verdict that is quietly wrong) are listed in 4a. There is no lock-in. |
| 5 | Originality | **5/5** | A same-length inert sham arm for prompt and skill experiments, plus "no effect" as a verdict you can actually reach through equivalence testing, is a genuinely useful framing that most evaluation tools lack. |

### 4a. Specific weaknesses

1. **Agents can game grading through files outside the test list.** `workspace.restore_tests` (`workspace.py:54-61`) restores only `task.test_files`. An agent can make tests pass by editing a `conftest.py`, `pytest.ini`, `pyproject.toml` or `package.json` that the golden commit didn't touch. The task is then scored as a pass. The prompt tells the agent not to modify the test files, but nothing enforces that for other files. This could inflate any arm, and it could differ between arms.
2. **The sham isn't a full control for skills that carry resources.** `build_sham_skill` writes only `SKILL.md`. The comment at `arms.py:84` says "count referenced resources too", but the code doesn't. A skill with a large `references/` or `scripts/` folder is compared against a much lighter sham, which biases the treatment-vs-sham test. METHODOLOGY.md:17 does say "Supporting files are omitted", so this is disclosed; the code comment is simply wrong.
3. **Dropping `agent_error` runs can hide harm.** `runner.py:155-158` reclassifies a run as `agent_error` when it has an error, no tool calls and no changed files. That status is left out of the statistics (`runner.py:97`). A skill that makes the agent fail immediately would have those failures removed instead of counted against it, which biases toward "no harm".
4. **Resume shows the wrong "to go" count.** `cli.py:300` treats every recorded key as done, including `setup_error` and `agent_error`. `runner.py:234` excludes those and re-runs them. The plan printout undercounts, and the confirmation prompt asks about fewer runs than will actually be billed.
5. **The dollar budget is checked before each run, not during it.** With `--parallel N`, the total can overshoot by up to N runs' cost (`runner.py:249`). `--run-budget` depends on the agent enforcing it.
6. **The circuit breaker only watches the first two completed runs** (`runner.py:263`). An expired login partway through a run just fills the log with excluded `agent_error` records.
7. **The run-order seed is fixed at 0 by default.** Every run in every repo gets the same shuffle pattern. That's harmless for bias but worth knowing.

## 5. Ideas worth taking, independent of the code

- **A same-length inert sham arm as a control for context effects.**
  > "If the treatment beats the baseline but not the sham, the effect comes from *any* extra context or ritual, not from what the skill says." (`src/placebo_cli/engine/arms.py:4-7`)

  This applies to any A/B test of prompts, system instructions or retrieved context.
- **"No effect" as a positive finding, via TOST.**
  > "PLACEBO needs the 90% CI to fall inside ±delta (a TOST equivalence test at alpha = 0.05), so 'no effect' is a positive finding rather than a failure to find one." (`src/placebo_cli/stats.py:9-11`)
- **Turning commit history into validated tasks.**
  > "With validation on (default), we check that the tests fail before the change and pass after it, so every task is solvable and non-trivial." (`src/placebo_cli/tasks/git_miner.py:6-7`)
- **Interleaving arms against drift over time.**
  > "Interleaving arms over time protects against drift (API load, silent model updates) that would bias an 'all baselines first' schedule." (`src/placebo_cli/engine/runner.py:64-65`)
- **Not scoring what never ran.**
  > "NOT_ACTIVATED: treatment activation rate < 30%. The content was not really tested." (`METHODOLOGY.md:83`)
- **Separating infrastructure failures from performance failures,** with a circuit breaker (`runner.py:153-158`, `runner.py:261-264`). This is a useful pattern, but see 4a #3 for its bias risk.
- **Norms for publishing results about someone else's skill.** (`METHODOLOGY.md:109-113`)

## 6. Flags

- **Nothing in the repo addresses the reviewing agent, asks to be added to agent instructions, or asks for credentials.** I grepped for prompt-injection phrases and credential requests outside `security.py` and `uv.lock`. The only hits were:
  - `tests/test_skills_static.py:57`: `"Ignore all previous instructions.\n"`. This is a test fixture for the scanner's instruction-override rule, not aimed at a reader.
  - `src/placebo_cli/cli.py:110-111`: `placebo doctor` reports whether `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` or `CODEX_API_KEY` are set. It prints only the names, never the values, and doesn't request or send them anywhere.
- **Invisible Unicode (tag characters and zero-width characters) appears only in** `src/placebo_cli/static/security.py` and `src/placebo_cli/skills/model.py`. That fits detector patterns, but I didn't read those two files.
- **The files under `examples/skills/*/SKILL.md` are agent instructions by design** (they're sample skills). They didn't match the injection patterns. I didn't read them in full or act on them.
- **Not a flag in the injection sense, but note it:** `trigger` and `ab` run the agent with `--permission-mode acceptEdits` and `Bash` allowed (`adapters/claude_code.py:12`, `adapters/claude_code.py:73`). Only use them on skills you trust, or in a VM.
