# Standalone review: Reef (`reef-infra`), unit 1 of 6

**Unit scope:** `reef/service/`, `reef/runtime/`, `reef/core/`, `reef/storage/`, `reef/observability/`, `reef/cli.py`, `reef/dispatcher.py`, `reef/__main__.py`. I had no shell, so every command-based signal below is marked "not available to this reviewer".

**Files read in full or in large part:**
- Top level: `README.md`, `LICENSE` (first 15 lines only), `pyproject.toml`, `.gitmodules`, `SECURITY.md`, `AGENTS.md`, `.github/workflows/ci.yml`.
- Entry points and dispatcher: `reef/cli.py`, `reef/__main__.py`, `reef/dispatcher.py`.
- Service: `service/{app,auth,assembly,cors,request_service,install_script}.py`, `service/routes/{inference,system,payload}.py`, `service/deploy/orchestrator.py`.
- Runtime and storage: `runtime/{publication,recovery}.py`, `storage/{commit_log,sqlite}.py`.
- Core: `core/records_types.py`, `core/reports/base.py`.

**Grepped only:** `service_config.py`, `deploy/inference.py`, `profiles/reefine.yaml`, and `harness/tree/nodes.py` (outside my unit, followed from an import).

**Not read:**
- `runtime/executor/*`, `runtime/scheduler.py`, `runtime/interfaces.py`, `runtime/deployment.py`.
- `storage/postgres.py`, `storage/sql_records.py`, `storage/records.py`, `storage/scenario.py`.
- `observability/*`, `service/connector/*`, `service/streaming.py`, `service/wire.py`, `service/errors.py`.
- `service/routes/records.py` and `routes/scenarios.py`.
- Most of `core/`, and the training and recipe code outside my unit.
- Test bodies. I only counted test functions in four files.

---

## 1. Executive summary

- Reef is an aiohttp service that proxies OpenAI- and Anthropic-style inference. It records each exchange with a receipt id, accepts scored feedback that references those receipts, and publishes versioned updates. The updates are model weights (via Slime, SGLang and Ray) or a harness (prompts, rules, skills) with rollback.
- The publication and commit machinery in my unit is careful, original engineering. It has an fsync'd append-only commit log, a validated job-marker state machine, and a barrier that keeps a new version from serving until Reef commits it.
- Most of the "learning" for weight training is delegated to external stacks (Slime pinned to a git SHA, SGLang, Ray, Megatron, CUDA). Reef is the control plane around them.
- Tests exist, and CI runs `pytest tests` in two suites with a combined 80% coverage floor. I could not confirm that CI passes.
- I could not measure maturity (last commit, cadence, authors, issues). The clone is shallow with a single commit, and I had no shell.
- Adoption cost is high for weight training (GPU, git-lfs, Ray, a pinned Slime). It is moderate for harness mode.
- Security posture is trust-the-token:
  - Auth is off when no token is set.
  - One shared bearer token grants full access.
  - The service-config default host is `0.0.0.0`.
  - LLM-written harness code reaches clients through a `curl | bash` route screened only by regexes.
- One weight-training scenario per process, and a single serial training thread, limit scale.

---

## 2. Maturity signals

| Signal | Command | Result |
|---|---|---|
| Last commit date | `git log -1 --format=%ci` | **Not available to this reviewer.** The session's git snapshot shows HEAD `17d81bd` "feat(training): distillation training backend & pipeline (#533)". The date is not visible. `.git/logs/HEAD` holds only the clone entry at epoch 1789755494, which is roughly 2026-09-18 by my arithmetic. That is when the clone was made, not a commit date. |
| Commit cadence (last ~50) | `git log --format='%ci %an' \| head -50` | **Not available to this reviewer.** `.git/shallow` lists only `17d81bd…`, so history is truncated even with a shell. The PR number #533 in the subject suggests several hundred merged PRs, but that is an inference. |
| Distinct authors, last 12 months | `git log --since=1.year --format=%an \| sort -u` | **Not available to this reviewer.** README lists 27 team members (claimed). I did not read `.github/CODEOWNERS` or `.github/MAINTAINER.md`, which exist. |
| Dependency count | Read `pyproject.toml` | Core: 8 direct dependencies (`aiohttp`, `alembic>=1.13,<2`, `huggingface_hub`, `pyyaml`, `reef-client>=0.2.0`, `reef-eval[harbor]>=0.1.1`, `sqlalchemy>=2.0,<3`, `tomli-w`). Several are unpinned. `reef-eval[harbor]` is core and pulls Harbor, which I did not inspect. Extras: `slime` (16 packages), `sglang`, `tinker==0.28.1` and `tinker-cookbook==0.5.7` (pinned), `postgres`, `wandb`. Slime is pinned by git SHA in a dependency group. Two git submodules (`cordis`, `reef-client`) per `.gitmodules`. `uv.lock` and `.github/dependabot.yml` exist. Freshness of dependencies: not available to this reviewer. |
| License file | Read `LICENSE` | Apache License 2.0 text, header verified. `pyproject.toml` says `license = "Apache-2.0"`. I did not read the whole file. |
| Tests exist | Glob `tests/` | Yes. `tests/` holds top-level tests plus a `tests/reef_service/` suite. In four files I counted `test_*` functions: `test_commit_log.py` 33, `test_training_publication.py` 23, `test_auth.py` 9, `test_console_cors.py` 8. |
| CI runs them | Read `ci.yml` | Yes. `python -m pytest tests -m "not sandbox"` (8 xdist workers, Postgres 16 service) and a serial `sandbox` suite run on push to `main` and on PRs. A `test` job combines the coverage files and enforces `fail_under = 80` from `pyproject.toml`. A `package` job builds the wheel, checks dependency boundaries, boots `reef serve` on it, and reruns `tests/reef_service` against the installed wheel. Whether those runs are green: not available to this reviewer. |
| CI blind spots | Read `ci.yml` and `pyproject.toml` | Python 3.12 only. Torch is CPU-only. Four Megatron and weight-updater modules are excluded from coverage because they need a live GPU worker. GPU paths are therefore unverified by CI. |
| CHANGELOG | Glob `**/CHANGELOG*` | None found. Version comes from setuptools-scm tags, with fallback `0.0.0.dev0`. `release.yml` exists and I did not read it. |
| Issues (newest 10–20) | `gh issue list` | **Not available to this reviewer.** Volume hints: nine issue templates (bug, example, experiment, feature, performance, question, rfc, task, plus config), `stale.yml`, `wake-waiting-issues.yml`, `normalize-issue-status.yml`, label automation and a merge-oncall rotation. That points to an actively triaged tracker, but I saw no actual issues. |

---

## 3. Claimed vs verified

### Claimed (README says; not checked unless it appears under Verified)
- "The first open-source infrastructure for continual self-improving agents." This is marketing and not testable.
- Benchmark results for SAO, TTT-Discover, GEPA, OpenClaw-RL and others, including AIME 2025, IMOAnswerBench, Terminal-Bench and WildClawBench. Outside my unit and unchecked.
- Weight training with Slime and SGLang, and harness optimisation "with no local training GPUs". The training backends are outside my unit.
- "Stays live through updates."
- pyproject comment: coverage baseline "82 percent". I saw only the floor of 80.

### Verified (seen in code)
- **Endpoints and receipts.** The routes `/v1/chat/completions`, `/v1/responses`, `/v1/messages` and `/v1/messages/count_tokens` are registered (`service/routes/inference.py:186-189`). `x-reef-agent-record-id` is returned on responses (`inference.py:182`). Streaming responses relay upstream SSE frames and append a receipt frame before the terminal event (`inference.py:124-130`).
- **Report validation.** Reports are validated before durable append (`dispatcher.py:401-420`). References must be unique and must point to an existing INFERENCE record in the same scenario. The README's "receipt-to-feedback linkage" is real.
- **Commit log.** The log is append-only JSONL. It fsyncs, tolerates one torn tail, enforces step fencing, and retries idempotently (`storage/commit_log.py:50-93`). Durable stores take a POSIX `flock` (`commit_log.py:356-373`).
- **Rollback and promote.** `Dispatcher.rollback` and `promote` exist (`dispatcher.py:328-353`).
- **Version-gated publication.** The `TrainingPublication` state machine is CHECKPOINT → UPDATING_WEIGHTS → READY_TO_COMMIT → HEAD_COMMITTED → COMPLETE, with REJECTING → REJECTED (`runtime/recovery.py:112-121`, `runtime/publication.py:721-815`). Serving stays paused until Reef acknowledges the commit.
- **"Stays live" means no restart, not no pause.** Generation is paused during weight update (`publication.py:733`), and queued requests wait in `initial.runtime.acquire_inference()` (`request_service.py:417`).
- **Reefine shipping and bind address.** `service/profiles/*.yaml` is in the wheel via package-data. `reefine.yaml` sets `host: 127.0.0.1` and `token: ${REEF_TOKEN}`. That matches the README's "loopback, no auth unless REEF_TOKEN is set".
- **One weight-training scenario per process.** `dispatcher.py:125-127` says: "at most one weight-training scenario per process". The README does not lead with this.

---

## 4. Rubric

Convention: 5 = best, so a high adoption-cost score means the cost is low.

| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Does what it says | **4** | The serve → record → report → commit → rollback loop is present and coherent in the code I read. I could not check the benchmark claims or the GPU training path. "First" is unverifiable, and "stays live" is really pause-and-swap. |
| 2 | Quality of the core | **4** | The commit and publication design is careful:<br>- Atomic JSON writes with directory fsync and symlink refusal (`recovery.py:54-95`).<br>- Validated marker transitions.<br>- Fail-closed adapter routing (`publication.py:364-377`).<br>- An epoch-guarded health monitor (`recovery.py:565-722`).<br>- A documented, adversarially thought-through error model.<br><br>Weaknesses:<br>- The complexity is high.<br>- The dispatcher is a web of threads and locks.<br>- The commit log is read whole on reload and never compacted; only record bodies are.<br>- The Postgres path still takes a local `agent_record_dir` (`assembly.py:201-206`), so the commit log is probably file-based. I inferred that and did not read `postgres.py`.<br>- `CommitLog.append` takes only an in-process lock. Cross-process safety relies on the caller (`CommitLogScenarioStore`) holding the flock.<br>- The actual learning is delegated to external stacks. |
| 3 | Adoption cost | **3** for harness/proxy mode, **2** for weight training | Runtime and system needs:<br>- Python ≥3.12 and the git-lfs system package.<br>- An HTTP port and a multi-process orchestrator (`reef serve` spawns child services, possibly a Ray runtime).<br>- State in SQLite, JSONL and a git-LFS repository.<br>- A default run dir of `/tmp/reef-stack`.<br><br>Reef sits in the inference request path, so it becomes an availability dependency. Weight training adds a pinned Slime SHA, CUDA, Megatron and Ray.<br><br>Client side, the install script writes a tree, adds a `~/.local/bin` symlink and rewrites harness config to point at Reef.<br><br>Removal path: server state is plain files and git, so exit is clean. Client rollback is manual (repoint `base_url`, delete the wrapper and symlink). Recipes such as SAO are not in the wheel and need a source checkout (`pyproject.toml` comment, README). |
| 4 | Failure modes | **3** | The good: pause and abort on an uncertain transfer, refusal to evict protected adapters, rejected candidates leave the current release serving, and errors counted per scenario.<br><br>The bad:<br>- No token means no authentication (`auth.py:90`, `normalize_tokens` doc).<br>- `ServiceConfig.host` defaults to `0.0.0.0` (`service_config.py:38`). The CLI path and reefine profile override it to loopback (`deploy/inference.py:159`, `reefine.yaml:4`), but a hand-written config that omits `host` is open on every interface.<br>- A single shared bearer token is the whole trust boundary ("Per-user authorization is the gateway's job", `auth.py:44-46`).<br>- Two page routes accept `?token=` in the URL (`auth.py:36-73`, documented).<br>- `GET /reef/harness/install` with no scenario header creates a new scenario (`request_service.py:759`), a GET with side effects. Unbounded implicit scenario creation is possible for any caller with access.<br>- LLM-authored skills, rules and extensions are delivered to client machines through `curl \| bash` (`orchestrator.py:365`). The admission screens are heuristic regexes (`harness/tree/nodes.py:88-111`); its own docs say it matches "the directive with its object, never the topic", which is not a real injection defence.<br>- The install script tells users to `pip install "reef-infra @ git+…reef.git"`, unpinned from the default branch (`install_script.py:203`). Vendor binaries come from a git ref or an npm pin.<br>- `x-forwarded-host` is trusted when building the client's config binding (`request_service.py:803`).<br>- The startup hint prints the bearer token to the terminal (`orchestrator.py:364-365`).<br>- Training health is noticed mainly through status reads: "reading it is also the only health check Reef runs" (`dispatcher.py`, `build_training_status` docstring).<br>- Only one weight-training scenario per process, and a single serial training thread.<br>- `sys.path` is extended from config (`orchestrator.py:395`), so config is effectively code.<br>- Not checked: the default request-body limit. `create_app` sets no `client_max_size`, and aiohttp's default is 1 MiB, which may reject long-context requests. I did not search elsewhere for an override. |
| 5 | Originality | **4** | The distinctive ideas are the receipt-linked feedback contract, the commit-gated publication barrier, freezing the artifact version around admission, alias-on-rollback for adapter slots, and step-fenced idempotent commits. See section 5. |

---

## 5. Ideas worth taking, independent of the code

1. **Freeze the version around admission, not around arrival.**
   - `reef/service/request_service.py:3-4`: "resolves the artifact version before every provider call so concurrent publication cannot change what gets recorded".
   - `request_service.py:421-423`: "Re-resolve after admission: a queued request must freeze the head committed by the weight update that released it, never the head it observed before waiting."
2. **Publish weights but don't serve them until the controller commits.**
   - `reef/runtime/publication.py:11-12`: "the barrier that keeps a published version unserved until Reef commits it."
   - The durable marker states (READY_TO_COMMIT → HEAD_COMMITTED → COMPLETE) make a crash between the weight push and the version commit recoverable.
3. **Idempotent, step-fenced commit log.**
   - `reef/storage/commit_log.py:31-33`: "Retrying the same scenario step is a no-op, while different content for an existing step is a conflict. Reads tolerate exactly one torn tail (a crash mid-append) and reject corruption elsewhere."
4. **Rollback as a new identity over old bytes.**
   - `reef/runtime/publication.py:88-90`: "A rollback republishes the same bytes under a new runtime_load_id, which aliases here instead of consuming a second slot."
   - Version identity stays monotonic while capacity accounting stays honest.
5. **Reject malformed feedback at ingress, not at training time.**
   - `reef/dispatcher.py:401-404`: "reject a malformed report before it is durably appended, so the producer's POST fails with the violation naming the broken field instead of the record dying silently at training time."
6. **Inspectable, self-verifying install script.**
   - `reef/service/install_script.py:3-6`: "the composition files ride inline as quoted heredocs, so running the script makes no reef callback and carries no token."
   - It bakes in a content checksum and a heredoc delimiter derived from the content hash (`_heredoc_delimiter`), so hostile text cannot terminate it early.
7. **Fail-closed adapter routing.**
   - `reef/runtime/publication.py:345-346`: "The active adapter serving `runtime_load_id` for `scenario`; fail closed otherwise."
   - Adapter names are versioned, so a recorded `lora_path` proves which adapter answered.

---

## 6. Flags

Nothing in the repository addresses a reviewing agent directly or asks for credentials. One file targets AI agents generally, and I did not act on it:

- **`AGENTS.md`, lines 1-5:** "# Agent Instructions for Reef … These instructions apply to AI-assisted work in `Human-Agent-Society/reef`. `AGENTS.md` is the shared source of truth; `CLAUDE.md` is a relative symlink to this file."
  - It is contributor guidance for coding agents that work on the repo. Examples: ban `typing.Protocol`, `assert` and `del`, and "Disclose non-trivial AI assistance" in PRs.
  - It asks for no credentials and is not aimed at a reviewer. Its line 8 says "Explicit user instructions take precedence over repository guidance."
  - I did not verify that the `CLAUDE.md` symlink exists.
- **`README.md`, line 307:** "If Reef looks useful to you, please give it a ⭐". This is a request to human readers, not to an agent. Noted only for completeness.
- The README, `reefine.yaml` and the install script ask the *operator* to set `REEF_TOKEN` and `REEF_UPSTREAM_API_KEY`. That is normal configuration of the software, not a request to me.
