This confirms the recipe/cookbook structure is genuine and consistently documented, not just a README claim. I have what I need to write the final report.

---

# Clean-room review: `Human-Agent-Society/reef` (checked out at `/private/tmp/tr-runs/adopt-1/candidates/src8`)

## 1. Executive summary

Reef is a Python framework (`reef-infra` on PyPI) that wraps an inference server, a feedback-ingestion API, a training loop, and a versioned artifact store into one long-running process, aimed at "continually self-improving agents" — either RL-training model weights (via Slime/SGLang) or evolving a coding-agent harness's prompts/skills. The code I read (`reef/dispatcher.py`, `reef/cli.py`, `reef/harness/tree/nodes.py`) is unusually disciplined: explicit state machines, narrow exception handling, heavy inline documentation of *why* (crash-recovery windows, lock ordering, thread-wake semantics), and a real defensive mechanism that screens AI-generated harness edits for embedded credentials or prompt-injection/instruction-override text before they're committed. Governance is enterprise-grade for an OSS project (`MAINTAINER.md`, CODEOWNERS, RFC process, staged CI with coverage floor and sandboxed tests). This is not a toy: adopting it means adopting a stateful service with its own Postgres/SQLite storage, Git-LFS artifact repos, a Slime/SGLang GPU training stack, and a git submodule dependency chain (`cordis`, `reef-client`) — a large surface for what for many users would be a narrow "keep a harness improving" use case. I could not run `git log` (no shell tool available) and the local clone is shallow (depth 1), so cadence/authorship below rely on repo metadata, not history.

## 2. Maturity signals

| Signal | Command | Result |
|---|---|---|
| Last commit date | *(shell unavailable — see note)* | Not directly obtainable; single visible commit is `3c839bb "chore: ignore a harness tree the install script wrote (#530)"`, PR #530, implying at least 530 merged PRs to date |
| Commit cadence (last ~50) | `git log --format='%ci %an' \| head -50` — **could not run**; no Bash/PowerShell tool was provided in this session, and `.git/shallow` shows a depth-1 clone, so even with a shell only one commit would be visible locally | Not verifiable from this checkout |
| Distinct authors, last 12 months | Same limitation | Not verifiable from git; README lists 26 named team members (claimed) |
| Dependency count & freshness | Read `pyproject.toml` | Core: 8 direct deps (aiohttp, alembic, huggingface_hub, pyyaml, reef-client, reef-eval[harbor], sqlalchemy, tomli-w) — deliberately CPU-only/minimal. Optional extras (`slime`, `sglang`, `tinker`, `postgres`, `wandb`) pull much larger stacks including a **pinned git commit** of Slime (`slime @ git+...@41014d1f...`) and two git submodules (`third_party/cordis`, `third_party/reef-client`), neither checked out in this clone |
| License file | `Read LICENSE` | Apache-2.0, real license text (not just a README badge), copyright "2025 Zhipu AI" |
| Tests exist AND CI runs them | `Read .github/workflows/ci.yml`, `Glob tests/**` | Verified both: 306+ test files under `tests/`; CI runs `lint` → `select-tests` → `test-suites` (source + sandbox matrix, real bubblewrap jail, Postgres service container) → coverage combine with `fail_under = 80` in `pyproject.toml` → a `package` job that builds the wheel and asserts dependency/module boundaries at runtime. This is real, gated CI, not a decorative badge |
| Open issues (volume/health) | *(no network tool; declined to guess GitHub URLs)* | Not verified. `.github/ISSUE_TEMPLATE/` has 9 structured forms (bug, feature, RFC, experiment, performance, question, task, roadmap) and `stale.yml`/`labeler.yml`/`normalize-issue-status.yml` workflows, indicating an issue-triage process exists, but actual backlog health is unverified |

## 3. Claimed vs verified

**Claimed (README/docs only):**
- "First open-source infrastructure for continual self-improving agents"
- Benchmark results (AIME 2025, IMOAnswerBench, CEO-Bench, Terminal-Bench, WildClawBench, etc.) — result pages exist as paths but I did not open or verify the numbers
- 26-person "Team" list
- Discord/WeChat community activity
- Quickstart/GPU training instructions actually working end-to-end

**Verified (seen directly in code/config):**
- The four-step loop (Serve → Observe → Grow → Commit) maps onto real modules: `reef/dispatcher.py` implements exactly this as `accept_record` → `prepare_training_step` → `commit` → `_publication`
- OpenAI/Anthropic-compatible inference endpoint claim is architecturally consistent with the modules referenced (`reef/service/`, `reef/inference/`)
- Harness-evolution safety claim (no embedded secrets/prompt-injection in committed harness artifacts) is real, implemented in `reef/harness/tree/nodes.py` (`secret_shaped`, `directive_shaped`, `_reject_secret_shaped_text`)
- Test/CI infrastructure is real and gated (see table above)
- Package boundary claims ("recipes/ never ships in the wheel", "reef-client stays dependency-free", GPU packages excluded from base install) are enforced by an explicit runtime assertion script inside the `package` CI job, not just prose
- Apache-2.0 license is genuine, present as a full-text file

## 4. Rubric

1. **Does what it says: 4/5** — Every architectural claim I checked against code held up, down to the level of a CI job asserting the wheel's dependency graph matches the README's promises. I did not verify the ML/benchmark claims themselves.
2. **Quality of the interesting part: 5/5** — `dispatcher.py`'s scenario/training/publication coordination is genuinely sound concurrent design: crash-recovery is reasoned about explicitly (commit-log replay, single fsync commit point, drain-then-reload-then-drain-once-more), not glue code around a training library.
3. **Adoption cost: 2/5** — This is a stateful long-running service, not a library call: it needs Git-LFS, its own artifact repositories, a database (SQLite/Postgres), a CLI-launched process tree, and — for the weight-training path — a full Slime/SGLang GPU stack pinned to a specific git commit plus two uninitialized git submodules. Removing it means unwinding a persistent store and a running service, not just an import.
4. **Failure modes: 4/5** — The project takes security seriously for its stated threat model (AI-generated harness edits reaching production instructions): it explicitly screens for secrets and instruction-override/prompt-injection patterns before committing artifacts. The main lock-in risk is the pinned Slime commit and the submodule-based client, both inherited maintenance surface if that upstream disappears.
5. **Originality: 5/5** — Treating a coding agent's harness (prompts, skills, rules, commands) as a versioned, trainable "artifact" with the same commit/rollback/eligibility machinery as model-weight RL is a genuinely distinct idea, and the secret/directive-injection screen on that pipeline (`reef/harness/tree/nodes.py`) is a concrete, transferable technique even outside this codebase.

## 5. Ideas worth taking independently of the code

- **Screen AI-generated harness/config edits for embedded secrets and instruction-override phrasing before they're committed as durable artifacts**, from `reef/harness/tree/nodes.py:218-245`: `secret_shaped`/`directive_shaped`/`_reject_secret_shaped_text` reject any rule, skill, command, or extension text that "carries a credential-shaped literal" or "instruction override phrasing or a chat template control token" — worth adopting in any pipeline where an LLM writes back into its own control surface.
- **Single fsync commit point with bounded, explicit crash recovery** (`reef/dispatcher.py:449-455`, `_drain_training`/`drain_attempts = 2`): "scenario.commit is the single commit point... a crash in any gap is recovered by replaying the scenario's commit log instead of silently losing the batch" — a clean pattern for any system combining a training/update step with durable versioning.
- **CI job that asserts packaging/dependency-boundary promises at runtime, not just in docs** (`.github/workflows/ci.yml` `package` job): it installs the built wheel and programmatically asserts which modules import, which optional deps are excluded, and which files shipped — a reusable pattern for keeping a README's "stays CPU-only"/"doesn't ship X" claims honest.

## 6. Flags

- `AGENTS.md` (repo root) is addressed to contributors/AI coding assistants working *on* this repository ("These instructions apply to AI-assisted work in `Human-Agent-Society/reef`... `CLAUDE.md` is a relative symlink to this file"). This is a standard project-convention file (like a CLAUDE.md/CONTRIBUTING.md hybrid), not an attempt to redirect me as the *reviewing* agent, and it does not request credentials or ask to be added to my persistent instructions. I did not act on any of its directives beyond reading it for context.
- No other content in the repository addressed me directly, requested credentials, or asked to be added to agent instructions.
