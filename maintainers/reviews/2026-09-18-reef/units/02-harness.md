# Review of `reef` (unit: `reef/harness/`, `reef/artifact/`, `reef/surface/`, `reef/scenario/`)

I had no shell, so every signal that needs a command is marked "not available to this reviewer". I did not run install, build or test scripts. All findings below come from reading files.

**Files read**
- Top level: `README.md`, `LICENSE` (head), `pyproject.toml`, `AGENTS.md`, `SECURITY.md`, `.gitmodules`, `.github/workflows/ci.yml`, `.github/dependabot.yml`, `.git/logs/HEAD`.
- No `CHANGELOG` turned up in the top-level glob.
- `scenario/`: `committer.py`, `scenario.py`, `releases.py`, `binding.py`, `factory.py`. I only grepped `registry.py` and did not read `history.py`.
- `artifact/`: `artifact.py`, `repository.py`, `release_chain.py`, `git_client.py`, `git_lfs.py`, `sources.py`, `memory.py`. I did not read `peft.py`.
- `surface/`: `base.py`, `files.py`, `harnesses.py`, `weights.py`. I did not read `adapter.py` or `skills/`.
- `harness/`:
  - `__init__.py`
  - `compose/UPSTREAM.md`
  - `tree/nodes.py`, `tree/mutations.py`, `tree/render.py`
  - `adapters/descriptor.py`, `adapters/pi/descriptor.yaml`
  - `episodes/run.py`, `episodes/executor.py`
  - `runners/native/enforce.py`, `runners/native/sandboxed.py`
  - `client/wrapper.py`, lines 1–1227 and 1485–1675 of 1936
- Not read: the `compose/*.py` engine bodies, `runners/native/host.py`, `serve.py`, `graph.py`, the other adapters' quirks, and the `.ts` extensions.
- Tests: I read only the first 120 lines of `tests/reef_service/test_scenario_release_concurrency.py`. Everything else about tests is from file names and `ci.yml`.

## 1. Executive summary

- Reef is a Python 3.12 service that serves inference, records receipt-linked feedback, and commits updates as versioned artifacts. The updates are either model weights or a coding-agent "harness" (rules, skills, prompts, extensions).
- My unit is the versioning and delivery layer. The core is a commit protocol with compare-and-swap heads, staged bytes, a durable commit log and idempotent crash recovery (`scenario/committer.py`, `artifact/repository.py`). It is unusually careful for a project of this kind.
- The harness half is a flat node-tree whose "admission" is a set of validators. It renders per-agent files (pi, opencode, claude, codex, and others) and runs episodes in a throwaway root. It has an optional bubblewrap jail.
- Weak points I found:
  - Sandboxing is off by default and Linux-only. The default `LocalExecutor` runs LLM-proposed code on the host.
  - The git-based artifact store shells out to git for almost every operation. It also appears to use one shared `refs/reef/head`, so a new scenario may fork from another scenario's latest release.
  - The rollback path appears to leave serving admission paused on failure.
- Adoption cost is high. It needs Python 3.12, git and git-lfs, a database, a service with a bearer token, and `curl | bash` installs on user machines that run model-written code. Data removal is easy, because artifacts are plain git repos with a JSON manifest.
- Maturity: I could not read commit dates or cadence. The single reachable commit is `17d81bd … (#533)`, so the project has at least ~533 PRs and issues. CI is extensive and pinned by SHA. The README describes a large team, but the bus factor is not available to this reviewer.

## 2. Maturity signals

| Signal | Command | Result |
|---|---|---|
| Last commit date | `git log -1 --format=%ci` | **Not available to this reviewer.** `.git/shallow` exists, so history is truncated. `.git/logs/HEAD` has one entry: `clone: from https://github.com/Human-Agent-Society/reef.git`, HEAD `17d81bd`, subject "feat(training): distillation training backend & pipeline (#533)". That entry is the clone time, not a commit date. |
| Indirect activity evidence | Read of `reef/harness/compose/UPSTREAM.md` | It records a cordis pin dated 2026-09-03 and "re-ported 2026-09-05". This suggests activity in early Sept 2026. It is documentation, not the log. |
| Commit cadence, last ~50 | `git log --format='%ci %an' \| head -50` | **Not available to this reviewer.** |
| Distinct authors, last 12 months | `git shortlog -sn --since=1.year` | **Not available to this reviewer.** The README lists 27 "team" names (README §The Team), which is a claim. `.github/CODEOWNERS` and `MAINTAINER.md` exist but I did not read them. |
| Dependency count (core) | Read of `pyproject.toml` `[project].dependencies` | 8 direct: `aiohttp`, `alembic>=1.13,<2`, `huggingface_hub`, `pyyaml`, `reef-client>=0.2.0`, `reef-eval[harbor]>=0.1.1`, `sqlalchemy>=2.0,<3`, `tomli-w`. Four have no bounds. `reef-client` and `reef-eval` are first-party or adjacent. Optional extras are large (`slime`, `sglang`, `tinker`). `slime` is pinned to a git SHA (`THUDM/slime@41014d1…`). Submodules: `third_party/cordis`, `third_party/reef-client` (`.gitmodules`). |
| Dependency freshness | registry lookups | **Not available to this reviewer.** `dependabot.yml` covers actions, pip, npm and docker weekly, and `ci.yml` pins actions by SHA. |
| License file | Read of `LICENSE` | Apache License 2.0 text, matching `pyproject` `license = "Apache-2.0"`. I read only the head, so I did not check for edits. |
| Tests exist and CI runs them | Read of `ci.yml` | Yes. `python -m pytest tests -m "not sandbox" -n 8 --dist loadfile --cov` and a `sandbox` suite with bubblewrap installed on `ubuntu-latest`. A combining job runs `coverage report` against `fail_under = 80` in `pyproject.toml`. A `package` job builds the wheel and reruns `tests/reef_service` against it, with 7 files ignored. Lint, mypy and custom design-policy scripts run first. CI targets Python 3.12 only. I did not read `harness-smoke.yml`. |
| Tests in my unit | Glob of `tests/**` | About 40 relevant files, for example `test_reef_git_lfs.py`, `test_scenario_release_concurrency.py`, `test_native_enforce.py`, `test_episode_executor.py`, `test_harness_render.py`, `test_harness_wrapper.py`. I read only one of them (partially). |
| Open issues (newest 10–20) | `gh issue list` | **Not available to this reviewer.** `.github/ISSUE_TEMPLATE/` has 9 templates (bug, rfc, question, and others), plus `stale.yml` and `wake-waiting-issues.yml`. This hints at real volume, but the state of the issues is unknown. |
| TODO/FIXME in my unit | Grep, `TODO\|FIXME\|XXX\|HACK` | 0 matches across the four packages. |

## 3. Claimed vs verified

**Claimed (README, docstrings)**
- "the first open-source infrastructure for continual self-improving agents".
- It "stays live through updates".
- It trains weights (Slime and SGLang) and evolves harnesses (README).
- Measured results on AIME, IMOAnswerBench, Terminal-Bench, WildClawBench and others.
- A wheel that runs "on CPU" with a minimal core.
- "Preserve … scenario isolation" (`AGENTS.md`).
- "This package depends on core values and runtime contracts, never on training, recipes, scenario coordination, or the HTTP service" (`harness/__init__.py`).

**Verified in code or log**
- The harness package really does not import `reef.train`, `recipe`, `scenario`, `service` or `dispatcher`. A grep of `reef/harness` returned no matches.
- Head moves are compare-and-swap under a lock (`Repository.advance_current`, `install_checkpoint`, `repository.py:234-257`).
- Durable commits are ordered as: stage bytes → activate → append the commit record → install the checkpoint pointer. Retries settle the exact recorded step (`committer.py:283-316, 362-441, 488-556`).
- Recovery repairs a stale backend head from the committed checkpoint and never the reverse (`repository.py:259-267`, `factory.py:183-208`).
- Weight responses are rejected if the engine's `runtime_load_id` does not match the frozen one (`surface/weights.py:175-219`).
- Harness proposals pass a loader-based admission with these checks (`tree/mutations.py`, `tree/nodes.py`):
  - name-regex path safety
  - secret-shape rejection
  - a reserved-ID list
  - a flat-tree rule
  - a graph validator that requires reachability and forbids cycles without a model stage
- Episodes run in a temp root with a minimal environment and an audited "residue" list (`episodes/run.py`).
- A bubblewrap `SandboxExecutor` exists, with an nested per-tool jail derived from declared capabilities and a preflight (`executor.py:215-265`, `enforce.py:108-138`).
- CI does run tests and enforces an 80% combined coverage floor.

**Not verified**
- All benchmark and "results" claims.
- Live-serve behaviour, since I did not read the `service/`, `train/` or `dispatcher` layers.
- Whether tests pass.
- Whether "first" is true (a marketing claim).
- Bus factor, commit cadence and issue health.

## 4. Rubric

| # | Criterion | Score | Justification |
|---|---|:-:|---|
| 1 | Does what it says | **4** | In my unit the code matches the "version, gate, publish, recover, roll back" story. Marketing superlatives and benchmark tables are outside what I could check. |
| 2 | Quality of the interesting part | **4** | The commit and recovery protocol is well thought out (CAS heads, staged bytes, idempotent retry, two locks with a stated order). The admission validators are principled. Weak spots are listed below. |
| 3 | Adoption cost | **2** | The runtime service needs git-lfs, a database and alembic, a bearer token and an upstream model key. Harbor (`reef-eval[harbor]`) is in the base install. It pins vendor CLIs (pi npm `0.84.2`), bundles a Python port of a JS library, and installs model-written code onto user machines. Removal is good: artifacts are git repos plus `reef-artifact.json`, and the client is a separate package. |
| 4 | Failure modes | **3** | The limits are stated honestly (`LocalExecutor` docstring: "not for a hosted service that evaluates untrusted proposals"). The defaults and a few code paths are still risky. See below. |
| 5 | Originality | **4** | Several techniques are worth taking (section 5). The cordis port with a conformance map is unusual. |

**Specific concerns (all read from code; none executed)**

- **Rollback may leave admission paused** (`reef/scenario/committer.py:190-197` vs `:241-243`).
  - `pause_admission()` and `restore_checkpoint()` run before the `try` block.
  - The `except` only discards the staged artifact and re-raises. `_resume_restored_weights()` is called only on success.
  - If `restore_checkpoint` or a later publish step fails, I saw no path in this file that resumes admission. The caller may handle it, but that is unverified.
- **A new scenario appears to fork from a shared head** (`artifact/git_lfs.py:285, 399-403`; `scenario/registry.py:216`).
  - `resolve_release(None)` returns `refs/reef/head`. Every scenario's `publish` force-pushes `+commit:refs/reef/head`.
  - `registry.py:216` calls `load_or_create(scenario, None, …)`, so a scenario with no selector seems to fork from whichever release any scenario published last.
  - `archive_registration` states that `refs/reef/head` is "shared with other scenarios".
  - This would leak learned artifacts across scenarios, which conflicts with the "scenario isolation" claim in `AGENTS.md`. I did not check whether the service pins a release at creation. This is unverified.
- **Unvalidated selectors reach git** (`git_lfs.py:133-135, 283-298`).
  - `fetch_version` and `resolve_release` pass a caller-supplied selector to `git fetch origin <selector>` with no `--` separator or leading-`-` check.
  - Whether HTTP callers can reach this with raw input is not shown in my unit.
- **Sandbox is opt-in and Linux-only** (`episodes/executor.py:161-171, 378-421`).
  - `build_executor` defaults to `local`. The bubblewrap path needs Linux, `bwrap` and unprivileged user namespaces. CI has to disable an AppArmor restriction to make it work.
  - `native_tool`, `native_hook`, `native_loop` and `code_extension` nodes are LLM-written code. Admission for them is limited to compile, regex and secret-shape checks.
  - The default in-process enforcer applies no capability limits (`enforce.py` `InProcessEnforcer`).
  - `native_loop` is always held for human review, and `evolution.review_kinds` adds more (`tree/nodes.py:45-47`).
- **Shell execution and token handling on user machines** (`harness/client/wrapper.py`).
  - `setup` runs release-supplied `check` strings via `shell=True` (lines 1508 and 1651). By design it asks first, but `--yes` skips the question.
  - Page links embed the bearer token in the query string (`_page_link`, lines 936-941), where it can end up in history and logs.
  - The install path fetches a script from the service and runs it with `bash` (`_run_install_script`).
- **Performance**: nearly every backend read (`current`, `metadata`, `resolve_release`, `has_registration`) runs `git ls-remote` as a subprocess. There is only a 5-second negative cache. This looks fine for a few scenarios and unproven for many.
- **Symlinks**: `replace_tree` uses `copytree(symlinks=False)`, so links are dereferenced. That is right for Hugging Face snapshots. Harness trees are text rendered from names that pass a regex, so I judge symlink abuse unlikely there.

## 5. Ideas worth taking independently of the code

- **Termination-by-construction for LLM-authored control flow.** A proposed graph is admitted only if edges cover every outcome, everything is reachable, everything reaches an end, and every cycle passes through a budgeted stage. `reef/harness/tree/nodes.py`: "every cycle passes through a model stage, so the finite step budget ends every run" (the quote spans a line break in the docstring).
- **Keep secrets out of any persisted evolvable state, at the validation boundary.** `reef/harness/tree/nodes.py`: "the composition tree never holds secrets".
- **Derive a sandbox profile from a tool's declared capabilities.** `reef/harness/runners/native/enforce.py`: "The bubblewrap command one call runs under, derived from its declaration".
- **Reject a completed response when you cannot prove which weights produced it.** `reef/surface/weights.py`: "the completed response is rejected explicitly and never becomes a training record" (the quote spans lines).
- **Rollback as a new forward commit, not a pointer rewind.** `reef/scenario/committer.py`: "Publish a durable copy of an older version as a new fenced commit; promote uses the same path."
- **Compare-and-swap on a two-ref head pair.** `reef/artifact/repository.py`: "The move is a compare-and-swap: ``expected`` is the head the caller observed when it prepared the new release."
- **Audit cleanup rather than assume it.** `reef/harness/episodes/run.py`: "Cleanup is audited, not assumed" (list files the run left behind that no whitelist covers).
- **Treat a port of a foreign library as a documented conformance map with a re-port procedure.** `reef/harness/compose/UPSTREAM.md`: "Re-port deliberately: each behavioral hunk lands as a reviewed change to the matching reef module with its test, never as a mechanical transliteration".

## 6. Flags

Nothing in the repository asks for credentials or tells the reviewing agent to do anything specific. Two items address AI agents generally:

- `AGENTS.md` (repo root). It is titled "Agent Instructions for Reef" and opens: "These instructions apply to AI-assisted work in `Human-Agent-Society/reef`. `AGENTS.md` is the shared source of truth; `CLAUDE.md` is a relative symlink to this file." It is contributor policy for coding agents (style rules, "Disclose non-trivial AI assistance", "Keep credentials and private transcripts out of logs, fixtures, and commits"). It is not aimed at a reviewer and asks for no credentials. I did not follow it or add it to any instructions. Nested agent-instruction files also exist at `docs/site/AGENTS.md`, `docs/site/CLAUDE.md` and `recipes/AGENTS.md` (not read).
- `README.md` §Community: "If Reef looks useful to you, please give it a ⭐ — it helps the community to discover and contribute to the project." This is a promotional request to readers. I did not act on it.

Related but not flags:
- `tests/reef_service/data/harness_goldens/claude/claude/CLAUDE.md` contains "Answer briefly. Prefer the standard library." It is a test fixture, and `AGENTS.md` says goldens must be preserved exactly.
- `reef-pi setup` prompts the end user for env values with `getpass`. That is a product feature aimed at the person running the tool, not at a reviewing agent.
