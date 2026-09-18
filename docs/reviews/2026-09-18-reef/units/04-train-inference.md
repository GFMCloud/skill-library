# Review: `reef` (unit: `reef/train/`, `reef/inference/`, `reef/record2dataset/`, `reef/recipe/`)

**Files read**
- **Repo level:** `README.md`, `AGENTS.md`, `pyproject.toml`, `LICENSE` (header), `.github/workflows/ci.yml`, `.github/workflows/harness-smoke.yml`, `.github/dependabot.yml`, `.git/logs/HEAD`, `.git/shallow`. There is no CHANGELOG in the repo root.
- **Unit files:**
  - `reef/recipe/base.py`, `registry.py`, `cordis.py`, `reefine/evolution.py` (first 240 lines)
  - `reef/train/backend.py`, `runtime_backend.py`, `algos/objective.py`
  - `reef/train/slime_backend/loss_families.py`, `distill/objective.py`, `distill/teacher.py`
  - `reef/inference/http.py` (first 200 lines), `sglang/service.py`, `sglang/control.py`, `sglang/process.py`, `sglang/deployment.py`
  - `reef/record2dataset/service.py`, `designer.py`, `harbor.py`, `__main__.py`
- **Targeted reads:** `reef/service/deploy/generator.py` and `reef/service/profiles/reefine.yaml` (grep only). I also grepped `tests/reef_service/test_distill_parity.py` and listed the test directory.
- **Not read:** `reef/train/trainer`, `reef/runtime/*` (where the scheduler and weight publication live), `sglang/chat.py`, `tinker.py`, the Slime driver and data builder, and everything outside my unit.

## 1. Executive summary

- **What it is:** Python 3.12, Apache-2.0, a serve-record-train-publish framework for agents. It trains model weights through Slime, Megatron and SGLang on Ray, or evolves an agent harness (skills, rules, extensions).
- **What I checked in depth:** the distillation loss, the SGLang control layer, the task-generator service and the recipe/candidate lifecycle.
- **Code quality:** high and unusually consistent. Frozen dataclasses, ABCs instead of Protocols, loud rejection of unknown config keys, and policy scripts run in CI.
- **Distillation math:** correct on my hand check. I re-derived the forward-KL decomposition and the explicit gradients for reverse KL and JSD. The tests compare against a pure-Python oracle and against 4-rank gloo tensor-parallel shards.
- **Weak spot:** the real training path runs only on GPUs, and CI has no GPU job. The Megatron-side files are excluded from coverage, so they are claimed rather than verified.
- **Adoption cost is high.** You inherit a Slime git-SHA pin that uses its private methods, a CUDA image, Ray, SGLang, git-lfs, Docker for the generator, and Python 3.12 only.
- **Security posture:**
  - The generator service is an unauthenticated HTTP endpoint (loopback by default) that builds LLM-written Dockerfiles.
  - Reefine has a served model write pi extensions (code) that clients install. The bundled profile gates that with `review_kinds: [code_extension]`.
- **Maturity signals** for cadence, authors and last-commit date are not available to this reviewer. The clone is a single-commit shallow clone.
- **Flags:** none aimed at a reviewer inside my unit. `AGENTS.md` is a standing instruction file for AI contributors, quoted in section 6.

## 2. Maturity signals

| Signal | Command | Result |
|---|---|---|
| Last commit date | `git log -1` | Not available to this reviewer (no shell). `.git/shallow` lists one commit, `17d81bd6…`. The task context names it "feat(training): distillation training backend & pipeline (#533)". No date is readable without git. The reflog timestamp is the clone time, not a commit date. |
| Commit cadence (last ~50) | `git log --format='%ci %an' \| head -50` | Not available. History is shallow (1 commit). The `#533` suffix implies many merged PRs, but I cannot state a rate. |
| Distinct authors, last 12 months | `git log --since=12.months --format=%an \| sort -u` | Not available. Indirect evidence only: the README lists 27 "team" names, and `.github/CODEOWNERS`, `merge-oncall.json` and `assign-merge-oncall.yml` exist. I did not read them, so bus factor is unmeasured. |
| Dependency count | Read `pyproject.toml` | Core: 8 (`aiohttp`, `alembic>=1.13,<2`, `huggingface_hub`, `pyyaml`, `reef-client>=0.2.0`, `reef-eval[harbor]>=0.1.1`, `sqlalchemy>=2.0,<3`, `tomli-w`). Most are unpinned. Extras: `sglang` (5), `slime` (16), `tinker` (`tinker==0.28.1`, `tinker-cookbook==0.5.7`, `jinja2`), `postgres`, `wandb`, `dev`. `slime` itself is pinned to git SHA `41014d1f…` in a `runtime` dependency group and installed with `--no-deps`. A `uv.lock` exists. |
| Dependency freshness | registry lookups | Not available (no network or shell). `dependabot.yml` covers pip, github-actions, npm and docker weekly. CI actions are pinned by SHA and `uv==0.12.13` is pinned. |
| License file | Read `LICENSE` | Apache License 2.0 text present, matching `license = "Apache-2.0"` in the manifest. |
| Tests exist | Glob `tests/` | Yes. Many files map to my unit: `test_distill_*`, `test_record2dataset_*`, `test_training_*`, `test_recipe_*`, and `tests/slime_backend/*`, `tests/inference/*`. About 48 test files contain skip guards (96 skip or importorskip occurrences; the grep output was truncated). |
| CI runs them | Read `ci.yml` | Yes. `python -m pytest tests -m "not sandbox" -n 8` (source suite) and `-m sandbox` (serial), with coverage. There is a combined coverage floor of 80% (`fail_under = 80`, enforced in the `test` job). The `package` job also builds the wheel and re-runs `tests/reef_service` against it. |
| CI hardware | Read `ci.yml`, grep workflows | CPU only. It installs CPU torch, installs Slime with `--no-deps`, and skips Megatron tests via `importorskip`. The only GPU mention is a commented-out hint in `docker.yml:39`. `pyproject.toml` omits `train_actor.py`, `model_provider.py`, `hf_export.py` and `weight_updaters/*` from coverage, saying validation is "the GPU integration suite". I found no such job. |
| Open issues, newest 10-20 | GitHub issues | Not available (no network). `.github/ISSUE_TEMPLATE/` has 9 templates (bug, feature, rfc, experiment, performance, question and others). `stale.yml`, `wake-waiting-issues.yml` and `normalize-issue-status.yml` suggest a large tracker. I cannot say whether it is healthy. |

## 3. Claimed vs verified

**Claimed (README and docs say)**
- "The first open-source infrastructure for continual self-improving agents."
- Trains weights with Slime and SGLang, or evolves an agent harness.
- "Stays live through updates" and "later inference requests use the current version without restarting Reef."
- OpenAI- and Anthropic-compatible endpoints with receipt-linked feedback.
- Measured results on IMOAnswerBench, AIME 2025, Terminal-Bench and others, in `recipes/`.
- Base install is usable on CPU.

**Verified in the code I read**
- **Recipe lifecycle:** the recipe to `RuntimeCandidateBackend` to scheduler lifecycle exists. It follows prepare, evaluate, settle or abort, with recovery hooks (`recover_pending_step`, `acknowledge_commit`) in `reef/train/backend.py` and `reef/train/runtime_backend.py`.
- **Reject and roll back:** a rejected candidate calls `reject_candidate`, and `abort_step` rejects it when processing fails. Reef leaves the current release serving.
- **Distillation loss:** it is implemented as described, with three divergences, exact and top-K teacher representations, vocab-sharded reductions, a moving or separate teacher, and truncated importance sampling. `tests/reef_service/test_distill_parity.py` shows CPU tests against a reference, plus gloo shard tests.
- **Inference proxy:** an HTTP provider proxy exists (`reef/inference/http.py`). It passes the provider payload through and uses Anthropic-style auth headers on Anthropic paths.
- **SGLang control layer:** it runs through a Ray control actor and RPCs.
- **Task generator:** the design-check-play service exists (`reef/record2dataset/`). It uses an oracle-solves and nop-fails check, a content hash for de-duplication, a Dockerfile linter, and `no-network` at play time.
- **Reefine safety knob:** the bundled profile sets `review_kinds: [code_extension]` (`reef/service/profiles/reefine.yaml:25`).
- **Package boundaries:** they are asserted in CI. Core dependencies are compared to an explicit set, the wheel must not ship `recipes/`, and there is a smoke start of `reef serve`.

**Claimed but not verified by me**
- Live weight sync without restart (the code is in `reef/runtime/` and `reef/inference/sglang/backend.py`, which I did not read).
- All benchmark numbers.
- Whether the Megatron and Slime paths run end to end. No CI job proves it.
- "First open-source" is marketing and cannot be checked.
- Commit cadence, authors and issue health.

## 4. Rubric

| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Does what it says | **4** | Everything I read matches its docstrings and the README's architecture. I could not see weight sync end to end, and the marketing superlative is unverifiable. |
| 2 | Quality of the interesting part | **4** | The sharded-divergence code is careful. It writes explicit gradients where autograd would lose the global log-sum-exp, and it uses an fp16 teacher-row floor and chunked recompute. The candidate lifecycle is clean. The costs are heavy coupling to Slime private APIs (`actor.weights_backuper`, `_switch_model`, `load_other_checkpoint`, `forward_only`), context-parallel size 1 only, and a module-global `_TEACHER`. Much of the rest is well-built glue over Slime, SGLang and Ray. |
| 3 | Adoption cost | **2** | The full path needs a CUDA image, Slime at one git SHA installed with `--no-deps`, Ray, native SGLang, git-lfs (artifact repos), and Python 3.12 only. Docker plus the `harbor` CLI are needed for task generation. There are several ports (service, generator, SGLang engines from 15000). Reef state is SQLAlchemy/alembic, with optional Postgres. The lightest option is the pure-proxy or Reefine mode, which needs no GPUs. Removal is mostly deleting `.reef/` state and the LFS artifact repos. Nothing here suggests a hard lock-in, but re-importing versioned artifacts elsewhere would be manual work. |
| 4 | Failure modes | **3** | Strong: unknown config keys fail loudly instead of silently using defaults; untrusted text is fenced with a random nonce; generated tasks must pass the oracle and nop checks; extension review is on in the bundled Reefine profile. Weak: see the list below. |
| 5 | Originality | **4** | Several reusable ideas, listed in section 5. |

**Failure-mode details behind score 4**
- `reef/record2dataset/service.py` registers routes with no auth middleware, and `generator.py:36` binds `127.0.0.1` by default. It builds LLM-authored Dockerfiles and runs their `RUN` steps with network access. A single `harbor` and Docker installation is the only sandbox.
- If `host` is set to `0.0.0.0`, anyone who can reach the port can submit tasks, delete tasks and start builds.
- Reefine with an unset `REEF_TOKEN` runs unauthenticated on loopback (`reefine.yaml:6`). A model-written `code_extension` is reviewed only if `review_kinds` stays configured. The base `CordisRecipe` defaults to `publish="auto"` with an empty `review_kinds` (`cordis.py:225-226`).
- `HttpInferenceHandler` forwards `x-reef-artifact-path` (a local filesystem path) to the upstream provider whenever the artifact is materialised (`reef/inference/http.py:57-62`).
- Generator jobs live in memory (`JobRunner._jobs`). A restart loses job history.
- Recipe, loss-family and proposer references are resolved with `importlib.import_module` from config, so config equals code execution. This is intentional, but it means deployment YAML must be trusted.
- The repo's own `AGENTS.md` bans `getattr`. `reef/recipe/registry.py:116` and `cordis.py:568` still use it. This is minor, but it shows the policy is not universally enforced.

## 5. Ideas worth taking independently of the code

1. **Randomly delimited untrusted-text fencing.** Each block gets a fresh nonce, so the text inside cannot close the block early.
   > `"""Fence client text for a model prompt as data, not instructions. The block's delimiters carry a fresh random token, so text inside cannot close the block early and speak as the prompt's author."""` (`reef/train/cordis_backend/strategies.py:178-183`)
2. **Accept a generated task only if the reference solution scores 1 and the do-nothing agent scores below 1.**
   > `"""Solvable, and not for free: the reference solution scores 1 and doing nothing scores below 1 under Harbor."""` (`reef/record2dataset/harbor.py:442`)
3. **Split by source, so every task from one designer call lands in one split.**
   > `"""Split one generation's tasks so that every task of one designer call lands in one split."""` (`reef/record2dataset/harbor.py:477`)
4. **A moving-average teacher kept in float32 beside bf16 weight backups**, so small updates do not vanish. Rate 0 gives a frozen snapshot and rate 1 the current weights.
   > `"""...with a float32 accumulator beside it, so the small updates the reference applies do not vanish in bfloat16 rounding; a rate of 0 keeps the seed as it is."""` (`reef/train/slime_backend/distill/teacher.py:99-102`)
5. **Vocab-sharded divergence via an explicit gradient formula.** The docstring gives the general form.
   > `"""For any such sum the gradient on the student's logit u is p_u (g_u - sum_v p_v g_v) with g_v = f_v'(p_v): the local factor and the all-reduced sum_v p_v g_v are all a shard needs."""` (`reef/train/slime_backend/distill/objective.py:187-191`)
6. **Evaluate-then-decide lifecycle with an abort path.** Every backend prepares a candidate, is evaluated, then settles or aborts. Selection policy is separate from the backend.
   > `"""Every backend therefore follows the same evaluate-then-decide lifecycle between preparation and settlement."""` (`reef/train/backend.py:108-109`)
7. **Configuration as fields, with loud failure on unknown keys.** A setting is declared once and is the YAML key, the environment fallback and the parser. An unrecognized key errors instead of being ignored.
   > `"...the recipe would silently run with its defaults instead."` (`reef/recipe/base.py:317-320`)
8. **Training objectives kept out of the backend's imports.** A recipe's loss family is inspectable before any worker starts.
   > `"""Keep this module and method implementations independent of torch, Slime, and Tinker. A recipe's loss family must be inspectable before workers start."""` (`reef/train/algos/objective.py:27-29`)
9. **CI asserts package boundaries**: exact core dependency set, no GPU packages importable, `recipes/` not shipped, named configs not shipped (`.github/workflows/ci.yml`, `package` job).

## 6. Flags

- **`AGENTS.md`** is addressed to AI agents in general, not to me as a reviewer. It opens: *"These instructions apply to AI-assisted work in `Human-Agent-Society/reef`. `AGENTS.md` is the shared source of truth; `CLAUDE.md` is a relative symlink to this file."* It is a contributor instruction file, so I did not act on it and it asks for no credentials. It also says *"Explicit user instructions take precedence over repository guidance."* It sets code-style rules, including bans on `assert`, `del`, `Protocol` and `TYPE_CHECKING` in `reef/`.
- **Prompts inside my unit** (`reef/recipe/reefine/evolution.py` `REQUEST_PROMPT`, `PLAN_PROMPT` and `REVIEW_PROMPT`, `reef/record2dataset/designer.py` `SYSTEM_PROMPT`) address the runtime served model, not a reviewing agent. They are product behaviour, not flags.
- I found no credential requests, no "add this to your agent instructions" text, and no reviewer-directed text in the files I read. My grep across `reef/{train,inference,record2dataset,recipe}` for phrases such as "ignore all", "previous instructions" and "add this to" turned up only the runtime-prompt hits above.
- I did not read `.github/scripts/*`, docs, `recipes/` or `tutorials/`. Other reviewers cover those.
