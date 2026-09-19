# Review of `reef` (`reef-infra`): repository top level

**Files read:** `README.md`, `LICENSE`, `pyproject.toml`, `CONTRIBUTING.md`, `SECURITY.md`, `.pre-commit-config.yaml`, `AGENTS.md`, `.gitmodules`, `docker/Dockerfile.reef`, `docker/README.md`, `docker/patch/mcore_parse_hybrid_pattern.py`, `.github/MAINTAINER.md`, `.github/CODEOWNERS`, `.github/dependabot.yml`, and `.github/scripts/check_python_design.py` and `check_python_statements.py`. I also read the workflows `ci.yml`, `release.yml`, `docker.yml`, `harness-smoke.yml`, `docs-build.yml`, `dependabot-auto-merge.yml`, `assign-merge-oncall.yml` and `stale.yml`. I skimmed `check_community_files.py` and did not read `check_readme_i18n.py`. I listed the `tests/` tree but did not read individual tests. The `reef/` source is outside my unit. There is no CHANGELOG anywhere in the repo.

## 1. Executive summary

- Reef is a Python 3.12+ framework that proxies OpenAI- and Anthropic-compatible traffic, records interactions, matches feedback to them by receipt, and runs a recipe that produces weight or harness updates, published as versioned artifacts.
- The unit I reviewed is unusually disciplined for a young project. It has Apache-2.0 with a real LICENSE file, action versions pinned by SHA, PyPI publishing through OIDC, an 80% coverage floor combined across suites, and a CI job that builds the wheel and runs `reef serve` against it.
- Tests exist (246 `test_*.py` files by glob) and CI runs them. The GPU and Megatron paths, which are the headline weight-training claim, are not run in CI.
- The Docker image is never built in CI, only linted with `docker build --check`. It sits on an unpinned `slimerl/slime:latest` base, patches a file inside the base image's Megatron tree, and fetches an `opencode` binary with no checksum.
- The docs describe CI that does not exist. CONTRIBUTING and MAINTAINER say a Python 3.10/3.11/3.12 matrix is required, but `pyproject.toml` requires 3.12 and `ci.yml` hard-codes `["3.12"]`. MAINTAINER says dependency PRs "are not merged automatically", but `dependabot-auto-merge.yml` auto-merges patch updates.
- The `LICENSE` appendix says "Copyright 2025 Zhipu AI", while `pyproject.toml` lists the author as "Human-Agent-Society". Ask about that before adopting.
- Bus factor: `CODEOWNERS` names three people plus one docs-only owner, and one person owns the default `*`. I could not measure commit history because there is no shell and the clone is shallow.
- The tests do more than the docs claim, but the docs promise more than the CI runs.

## 2. Maturity signals

I have no shell, so signals that need a command are marked "not available to this reviewer". Where a file gave a partial answer, I say so.

| Signal | Command | Result |
|---|---|---|
| Last commit date | `git log -1 --format=%ci` | Not available to this reviewer. `.git/shallow` lists a single commit (`17d81bd`, "feat(training): distillation training backend & pipeline (#533)"). The only reflog line is the local clone. |
| Commit cadence (last ~50) | `git log --format='%ci %an' \| head -50` | Not available to this reviewer. The clone is depth-1, so this cannot be measured here even with a shell. The `(#533)` suffix says only that PR numbering has reached at least 533. |
| Distinct authors, last 12 months | `git shortlog -sn --since=12.months` | Not available to this reviewer. Indirect evidence: the README lists 27 "team" members, and `CODEOWNERS` routes to 4 accounts (`@BobbyZhouZijian` default, `@Benjamin-eecs`, `@hanfeiyu`, `@simonucl` for GEPA docs and recipe). |
| Dependency count | Read `pyproject.toml` | 8 core: `aiohttp`, `alembic>=1.13,<2`, `huggingface_hub`, `pyyaml`, `reef-client>=0.2.0`, `reef-eval[harbor]>=0.1.1`, `sqlalchemy>=2.0,<3`, `tomli-w`. Extras: `sglang` (5), `tinker` (3, exact pins), `postgres` (1), `wandb` (1), `slime` (16). Dependency group `runtime`: Slime pinned to a git commit. `uv.lock` exists. Most core deps are unbounded above. |
| Dependency freshness | Not checkable offline | Not available to this reviewer. `dependabot.yml` covers actions, pip, npm (`docs/site`) and docker, weekly. |
| License file | Read `LICENSE` | Full Apache-2.0 text. The appendix boilerplate reads "Copyright 2025 Zhipu AI". There is no NOTICE file (glob found none). `pyproject.toml` has `license = "Apache-2.0"`. |
| Tests exist | Glob `tests/**/test_*.py` | 246 files across `tests/reef_service` (about 200 of them), `tests/inference`, `tests/plugin_contracts`, `tests/smoke`, `tests/packaging` and top-level `tests/test_*.py`. |
| CI runs them | Read `ci.yml` | Yes. `test-suites` runs `python -m pytest tests -m "not sandbox" -n 8 --cov` on the `source` leg (with a Postgres 16 service) and `-m sandbox` on the `sandbox` leg. The `test` job requires both legs to succeed, combines coverage, and runs `coverage report` against `fail_under = 80`. The `package` job builds sdist and wheel, runs `twine check`, boots `reef serve` from the wheel, and runs `tests/reef_service` against the installed wheel minus 7 Slime-dependent files. |
| CI does not run | Read `docker.yml`, `ci.yml` | No image build (only `docker build --check`; the comment says the base exceeds hosted-runner disk). The 4 Megatron/CUDA modules are omitted from coverage, and CI installs only the CPU torch wheel. Tests that import Slime are ignored in the wheel job. `harness-smoke.yml` is non-blocking and path-triggered. |
| Open issues | Not available to this reviewer | I cannot see GitHub. `.github/ISSUE_TEMPLATE/` has 8 forms (bug, example, experiment, feature, performance, question, rfc, task). `stale.yml` closes issues after 90+30 days and PRs after 60+21 days. The stale bot means a low open-issue count is weak evidence of health. |

## 3. Claimed vs verified

**Claimed (README and docs say):**
- "the first open-source infrastructure for continual self-improving agents."
- It trains weights with Slime and SGLang, or improves an agent harness, and "stays live through updates".
- It exposes OpenAI- and Anthropic-compatible endpoints (`/v1/chat/completions`, `/v1/messages`).
- `pip install reef-infra` works on CPU for the base `recipe` configuration, and the wheel contains no recipes.
- The SAO (arXiv:2607.07508) example deployment, the measured benchmark results, and Reefine harness evolution with no GPUs.
- CONTRIBUTING and MAINTAINER: a 3.10/3.11/3.12 matrix is required before merge.
- MAINTAINER: dependency PRs "are not merged automatically."
- The docker image "bundles the full runtime" and is verified by a GPU integration suite.

**Verified (I saw it in the files):**
- Apache-2.0 LICENSE is present and complete. The copyright line names Zhipu AI, not the project's stated author.
- The core dependency list is exactly the 8 in `pyproject.toml`. `ci.yml` asserts this set, asserts that `megatron`, `ray`, `sglang`, `torch` and `transformers` are not importable after a core install, and asserts `recipes` is not shipped. That directly backs the "CPU-only core, cookbook not in wheel" claim.
- `reef serve` starts from the built wheel and answers `/healthz`. This is enforced in CI.
- CI does run the tests. There are 2 suites, a coverage floor of 80, and a combined-coverage gate.
- Releases go through PyPI trusted publishing (`id-token: write`, `environment: pypi`) from tag pushes. The build job only builds and does not re-run the tests, so the `pypi` job depends on the tag being cut from a green `main`.
- Lint policy is enforced in CI: the `check_python_design.py` AST check, the assert/del ban, mypy, README translation pairing, and actionlint with a SHA-256-checked download.

**Contradicted by the files:**
- The 3.10/3.11/3.12 matrix does not exist. `ci.yml` `select-tests` hard-codes `["3.12"]`, and `requires-python = ">=3.12"`.
- Auto-merge: `dependabot-auto-merge.yml` runs `gh pr merge --auto --squash` for `semver-patch` updates, against MAINTAINER's "not merged automatically".

**Unverified:** "first open-source", the arXiv reference, all benchmark results, the GPU/Megatron training path (nothing in CI touches it), and the `reef-client` and `reef-eval` sources. `third_party/` is empty in this checkout because the submodules are not initialised.

## 4. Rubric

| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Does what it says | **3/5** | The packaging and CPU-core claims are asserted by executable checks. The GPU training and benchmark claims are not exercised anywhere in my unit. The docs also describe CI that has drifted (3.10/3.11, auto-merge). |
| 2 | Quality of the interesting part | **Not scored** | It lives in `reef/`, outside my unit. From the top level, the architecture is sensible: a thin core, recipes outside the wheel, and a protocol client kept separate. |
| 3 | Adoption cost | **2/5** | The base install is light. The real feature set needs `git-lfs`, a Ray/SGLang/Slime/Megatron GPU stack, and the fixed Docker base. You also inherit a process orchestrator that writes PID and log files under `/tmp/reef-stack`. Removal is straightforward for the pip core, and state lives under `.reef/` or `/var/lib/reef`. |
| 4 | Failure modes | **2/5** | See below. |
| 5 | Originality | **4/5** | Receipt-linked feedback, versioned artifacts with rejected candidates leaving the serving release untouched, and harness/skill evolution as first-class updates alongside weights are distinctive. |

**Failure modes (score 4):**
- The image inherits `slimerl/slime:latest` by default, so a rebuild can silently change CUDA, torch and sglang (the Dockerfile notes two breakages seen on fresh builds, on 2026-07-28 and 2026-08-24). Reef then rewrites the base's Megatron source by appending a backport to `mamba_hybrid_layer_allocation.py` and deletes and re-installs numpy by hand. That is brittle by the Dockerfile's own comments.
- Supply chain in the image: `opencode` is fetched with `curl | tar` from a GitHub release with no checksum, `peft` is unpinned, and it installs an AI coding agent into a training container.
- The README's harness install is `curl ... /reef/harness/install?adapter=pi | bash` against your own server. That is fine on loopback, but it makes the Reef endpoint a code-delivery channel. The README says the reefine profile listens on `127.0.0.1:8901` unauthenticated unless `REEF_TOKEN` is set.
- Core dependencies are mostly unbounded (`aiohttp`, `pyyaml`, `huggingface_hub`, `tomli-w`, `reef-client>=`, `reef-eval>=`). Tinker is pinned exactly. Two of the 8 core packages (`reef-client`, `reef-eval`) are the project's own or a sibling's, so you inherit their release cadence too.
- A coverage floor of 80% is stated "just under the 82 percent baseline", and it excludes the GPU paths. Coverage protects the CPU control flow only.
- Bus factor: `CODEOWNERS` gives `@BobbyZhouZijian` the default owner, `/.github/`, `/docker/` and `pyproject.toml`. The single Merge Oncall is set in `merge-oncall.json`.

## 5. Ideas worth taking independently of the code

- **A packaging boundary asserted in CI.** `ci.yml` builds the wheel, installs it, and asserts the exact core requirement set, that `megatron`, `ray`, `sglang`, `torch` and `transformers` are not importable, and that `recipes` is absent. Quote: `assert core == expected_core, core`. (`.github/workflows/ci.yml`)
- **Test the wheel, not the checkout.** It runs the service suite from `${{ runner.temp }}` with only `recipes/` symlinked, so the source tree cannot shadow the installed package. (`.github/workflows/ci.yml`)
- **Design rules as AST checks with a baseline.** The design-policy script bans `Protocol` and `TYPE_CHECKING` outright ("cannot be baselined") and grandfathers Callable-state patterns. Stale baseline entries also fail the build. Quote: `Stale Python design baseline entries (remove them):`. (`.github/scripts/check_python_design.py`)
- **A translation-pairing check.** `README.md` and `README.zh.md` are pinned by git blob hash in `README.i18n.yaml`, so a one-sided edit fails CI. (`CONTRIBUTING.md`, "Keep the root READMEs synchronized")
- **A single required check that cannot be greened by skipped jobs.** `docs-gate` explicitly tests that a skipped build is allowed only when no docs changed. (`.github/workflows/docs-build.yml`)
- **No-`--no-deps`-by-accident.** Runtime pins are kept in a `[dependency-groups]` entry so GPU images can install Slime with `--no-deps` and keep the CUDA-matched stack. (`pyproject.toml`)
- **Least-privilege workflows.** `persist-credentials: false` on every checkout, and the `pull_request_target` workflow reads config from the base ref and never checks out PR code. (`.github/workflows/assign-merge-oncall.yml`)

## 6. Flags

Nothing in my unit addresses a reviewing agent, asks to be added to agent instructions, or asks for credentials.

Two agent-related items I saw, quoted for completeness and not acted on:

- `AGENTS.md`, line 3: "These instructions apply to AI-assisted work in `Human-Agent-Society/reef`." It addresses agents that contribute to the repository, not a reviewer. It says a `CLAUDE.md` symlink points at it, which I did not confirm (my glob for `CLAUDE.md` returned nothing). It asks for no credentials. Its closing line 8 says "Explicit user instructions take precedence over repository guidance."
- `CONTRIBUTING.md`, "AI-assisted contributions": "Do not submit autonomous or bulk-generated issues, pull requests, reviews, or comments."

The only credential-shaped strings I found are test and CI values: `POSTGRES_PASSWORD: reef_test` in `ci.yml` (a throwaway CI Postgres) and the `REEF_TOKEN=reef-local` example in the README.
