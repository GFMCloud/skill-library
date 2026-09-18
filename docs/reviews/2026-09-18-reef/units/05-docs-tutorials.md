# Review: Reef, unit `docs/` and `tutorials/`

## 1. Executive summary

- **What it is:** Reef is a proxy that sits between an agent and its model. It records requests, joins later feedback to them by a "receipt" header, and then trains weights (GPU) or evolves the agent's harness files (no GPU). Accepted updates go into a versioned release chain.
- **Docs quality:** Unusually detailed, and candid about limits. The tutorials publish n=1 runs, including rejected and skipped ones. Where I could check, the docs match the code: CLI flags, the packaged Reefine profile, the `/v1/responses` route, and the `reef-client>=0.2.0` pin all exist.
- **Docs drift:** The project looks very young and fast-moving (dated items run from 2026-08-17 to 2026-09-12). The drift shows in at least four places:
  - The Reefine tutorial README says the built-in profile "uses token `reef-local`", but the profile is unauthenticated unless `REEF_TOKEN` is set.
  - `write-a-harness-method.rst:140` uses `max-score`, which the code no longer has.
  - `troubleshooting.rst:80` says there is no `/v1/responses` route, but the code has one.
  - The tutorial README contradicts itself on whether rejected proposals are persisted.
- **Evidence of improvement is thin:** The tutorials show the loop *runs*, not that it *improves* anything. The tasks are 3 arithmetic prompts, many gates end in ties, and one Reefine demo publishes under `selection: always`. Its `floor` mode only checks that "the tree still works".
- **Adoption cost is high for the "no GPU" path:** It needs Python 3.12+, `git-lfs`, Node/npm (a pinned `pi` binary is installed at startup), a long-running service, and a `curl … | bash` client install. Weight training needs a CUDA Docker image.
- **Security posture:** Reasonable guardrails are documented: credential and instruction-override screens, human promotion of code changes, and a bubblewrap sandbox. The docs also say plainly what they don't cover: the default `local` executor "enforces none of this".
- **Scope:** I reviewed `docs/` and `tutorials/` only. I had no shell, so git-history and issue signals are unavailable.

## 2. Maturity signals

I had no shell, so no command was run. "Read" means I read the file directly.

| Signal | Command / source | Result |
|---|---|---|
| Last commit date | `git log -1` | **Not available to this reviewer.** Reading `.git/logs/HEAD` shows only a clone entry (`clone: from https://github.com/Human-Agent-Society/reef.git`), and that timestamp is the clone time, not a commit date. |
| Commit cadence (last ~50) | `git log --format='%ci %an' \| head -50` | **Not available to this reviewer.** `.git/shallow` lists a single commit, `17d81bd…`, so this checkout has no history to read. |
| Cadence, from the docs (not the log) | Dates inside docs | The docs give these dates:<br>- Open-sourced under Apache-2.0: 2026-08-31 (`docs/site/lib/news.ts`)<br>- Newest news item: 2026-09-12<br>- RFC created: 2026-08-25 (`docs/rfcs/reef-router.rst`)<br>- Tutorial runs: 2026-08-17 (PR #58) through 2026-09-08 (PR #315)<br>- Checked-out HEAD: PR #533<br>Read as: about 5 weeks of visible history and hundreds of PRs. This is inferred from doc text and is not verified against the log. |
| Distinct authors, last 12 months | `git log --since=… \| sort -u` | **Not available to this reviewer.** The README lists 27 people as "non-exhaustive" team members (claimed, not verified). |
| Dependencies | Read `pyproject.toml` | Core has 8 runtime deps: `aiohttp`, `alembic>=1.13,<2`, `huggingface_hub`, `pyyaml`, `reef-client>=0.2.0`, `reef-eval[harbor]>=0.1.1`, `sqlalchemy>=2.0,<3`, `tomli-w`. Most are unpinned.<br>Extras: `tinker==0.28.1` and `tinker-cookbook==0.5.7` (pinned); `slime` (about 15 unpinned); `postgres`; `wandb`. The `runtime` group pins `slime` to a git SHA.<br>The docs site (`docs/site/package.json`) has 10 prod and 10 dev npm deps (Next 16, React 19, mermaid, and others).<br>Freshness of each dependency: **not available to this reviewer**. |
| Pinned external binaries | Read `harness-smoke.yml` | `pi` 0.84.2 (npm `@earendil-works/pi-coding-agent`), `@openai/codex` 0.152.1, `@deepseek-ai/dsh` 0.1.2-alpha.5, and Hermes `v2026.8.31` cloned from git. |
| License | Read `LICENSE` (first 15 lines) | Apache License 2.0 header. `pyproject.toml` has `license = "Apache-2.0"`. I did not read the full text. |
| CHANGELOG | Glob `CHANGELOG*` | None found. |
| Tests exist and CI runs them | Read `.github/workflows/ci.yml`, `docs-build.yml`, `harness-smoke.yml`, and the two tutorial tests | **Tests are run in CI.** `ci.yml` calls `python -m pytest tests` (line 209) and `pytest …/tests/reef_service` (line 472).<br>**Docs are checked in CI.** `docs-build.yml` runs `npm run check:docs` (link check plus doc-contract check), lint and build.<br>**Tutorials are only partly covered.** `tests/reef_service/test_reefine_tutorial.py` and `test_harness_example.py` are described in their own docstrings as "hermetic": model stubbed, "episodes never run". The live `run.sh` demos are not in CI, and their published rows are manual, single runs.<br>**Real-binary smoke tests don't gate merges.** `harness-smoke.yml` says "Non-blocking: not in the required check set until stable", and it only triggers on `reef/harness/*`, `tests/smoke/*`, and similar paths. |
| Open issues, newest 10–20 | Issue tracker | **Not available to this reviewer.** Volume hints only: 8 issue templates (bug, example, experiment, feature, performance, question, rfc, task), plus `stale.yml`, `wake-waiting-issues.yml` and `normalize-issue-status.yml` under `.github/workflows/`. |

## 3. Claimed vs verified

I read the docs in depth. Where I say "verified", I confirmed it against code or config. I did not run anything.

**Verified (seen in code, config or CI)**
- `reef serve --inference.upstream-url … --inference.upstream-model …` exists (`reef/service/deploy/cli.py:51`, `reef/service/deploy/inference.py:197-199`). The `--model` shorthand exists too (`cli.py:261`).
- `reef serve --recipe reefine` has a real, packaged profile. It listens on 127.0.0.1:8901, runs unauthenticated unless `REEF_TOKEN` is set, and keeps state under `.reef/reefine/` (`reef/service/profiles/reefine.yaml`; `pyproject.toml` package-data includes `service/profiles/*.yaml`).
- Every stated tutorial default matches `tutorials/evolve-your-harness/configs/serve.yaml`: upstream `http://127.0.0.1:8000`, model `qwen3-8b`, token `reef-local`, port 8900.
- The `/v1/responses` route exists (`reef/service/routes/inference.py:187`), as do the other routes the docs table lists. `docs/site/scripts/check-doc-contracts.mjs` compares the routes table against the route source, and CI runs it.
- `reef-client>=0.2.0` is a declared dependency (`pyproject.toml:29`), which matches the troubleshooting note.
- A `NODE_KINDS` registry exists in `reef/harness/tree/nodes.py:638`. I did not count that it has exactly ten kinds.
- `max_score` is gone from `reef/` (no matches), which agrees with `docs/developer-guide/processors.rst:259`.
- The tutorial READMEs report unflattering results: "skipped: no proposal", "rejected", ties, and "No run here has produced an extension yet". This is visible in the tables.

**Claimed only (README or docs say it; I did not verify it)**
- "Reef is the first open-source infrastructure for continual self-improving agents" (`README.md`).
- Weights hot-swapped into a live engine with no restart, and the Slime, SGLang and Ray stack working (needs a GPU).
- The benchmark results for SAO, TTT-Discover, OpenClaw-RL, SkillClaw and GEPA (those pages are outside my unit).
- The restart and recovery guarantees table (`docs/user-guide/operate.rst`).
- The bubblewrap sandbox properties (fresh non-root namespace, read-only base, no network), and the nested per-tool jail on the native adapter.
- The "63 s reference run" on Qwen3-8B, and the committed notebook outputs.
- `reef-client` being "stdlib-only". It lives in a separate repo and submodule that I did not read.
- The `reef-infra` PyPI package and `reefinfra.ai` URLs.
- The logo wall: `docs/site/components/home/logo-wall.tsx` calls it "institutions contributors come from". That is affiliation of individuals, not endorsement or adoption by the organisations.

**Inconsistencies inside the docs**
- `tutorials/reefine/README.md`, section "Built-in recipe": "the profile listens on `127.0.0.1:8901`, uses token `reef-local`". The actual profile has `token: ${REEF_TOKEN}` and comments "Unset REEF_TOKEN leaves the loopback service without authentication". `docs/user-guide/recipes/reefine.rst:21`, `docs/reference/cli.rst` and the root README say the same as the profile. The tutorial's own `configs/deployment.yaml` does hard-code `reef-local`, and that is likely the source of the mix-up.
- `docs/developer-guide/write-a-harness-method.rst:140` shows `max-score: 0.0` in a recipe config, but the code no longer has the key. `troubleshooting.rst` says an unknown `reef.*` key stops boot. I did not run it, so that is an inference.
- `docs/user-guide/troubleshooting.rst:80` says "Reef serves no `/v1/responses` route yet". The route exists in code and in `http-api.rst`.
- `docs/user-guide/evolve-your-harness.rst` says "Reef ships no proposer and no episode scorer" in the "Write a method" section. The same page says the Reefine proposer and evaluator "ship in the wheel", and `tutorials/evolve-your-harness/harness/evolution.py` is now a thin shim onto them.
- `tutorials/evolve-your-harness/README.md`: "Known limitations" says "A rejected proposal's content is not persisted". Note [5] in the same file says the content is now kept.

## 4. Rubric

| # | Criterion | Score | Justification |
|---|---|---|---|
| 1 | Does what it says | **4/5** | Every flag, file and default I cross-checked exists and behaves as described. Deductions: the four contradictions above, and the "no GPU" harness path also needs Node, npm and a pinned third-party binary. |
| 2 | Quality of the interesting part | **3/5** | The documented design is coherent:<br>- Paired-episode gate with snapshot and revert.<br>- Compare-and-swap head updates, and a stated single-writer rule.<br>- Frozen release per request.<br>- Human promotion of code changes.<br>I did not read the implementation, and the unit's own evidence is weak: 3 arithmetic tasks, one sample per row, and many 0/0/3 ties published under `selection: always`. It shows the loop runs, not that it improves anything. |
| 3 | Adoption cost | **2/5** | Adopting Reef adds:<br>- Python 3.12+ and system `git-lfs`.<br>- Node/npm, with a pinned `pi` installed at service start under `~/.local/share/reef-harness`.<br>- A long-running service on 8900/8901.<br>- A `curl … \| bash` client install that writes `~/.local/bin/reef-pi`, bakes the interpreter path into a wrapper, and writes the model ID and token into local harness config.<br>- For weights, a CUDA Docker image with `--network host`.<br>Rollback and scenario archival are documented. I found no uninstall path for the client footprint in the files I read. Switching the record backend "does not migrate existing records or commit history". |
| 4 | Failure modes | **3/5** | Good guardrails are documented (credential tripwires, override screening, review gates, restart table). Risks the docs themselves state:<br>- Weights between checkpoints "are not recoverable".<br>- Rollback "currently applies to harness artifacts" only.<br>- The local executor "enforces none of" the sandbox.<br>- `egress_hosts` "does not enforce a hostname firewall".<br>- With no tokens configured, "a deployment with no tokens at all accepts every request".<br>- A typo'd scenario name silently creates a second scenario when implicit creation is on.<br>- Under `--follow head`, "whoever can publish to the scenario runs code on the machine the process serves on".<br>Several failure states look the same as "nothing yet", such as `/reef/harness` returning 404 and steps recorded as `skipped: no proposal`. |
| 5 | Originality | **4/5** | Several ideas are worth taking (next section). The docs are more accurate about the design's limits than most. |

## 5. Ideas worth taking independently of the code

- **Gate on a paired comparison with a noise floor.** `docs/user-guide/evolve-your-harness.rst`, "What decides": "The candidate is published only when it wins more tasks than it loses, by more than a margin you set." The same page adds `evolution.min_win_margin`: "so on a stochastic episode a single lucky flip does not publish."
- **Grow the eval suite from real failures, with screening and a per-sender cap.** Same file: "the seed tasks are the floor of a suite that grows from real failures and no later candidate can win while bringing one back". It also has `evolution.recheck_every` to catch a publish that a grown suite later exposes.
- **Feedback joins by receipt on a provider-native proxy.** `docs/getting-started/quickstart.rst`: "The response header `x-reef-agent-record-id` carries the **receipt**, which names the stored exchange. Tests, a verifier, a rubric, a thumbs-down, or any other grader you already have can report feedback against it."
- **The model proposes, a person serves what runs as code.** `docs/user-guide/evolve-your-harness.rst`: "the model proposes a loop, a person serves it."
- **Declared setup requirements, checked only on human confirmation.** `docs/user-guide/operate.rst`: "`reef-<adapter> setup` is the only thing that runs a check, after the person read it and confirmed". The install script refuses a release with unmet items.
- **Freeze the release at request time and reject spans that cross an update.** `docs/reference/http-api.rst`: "Reef reads the scenario's current artifact ref and builds the request against that release", and "Missing or inconsistent spans are a backend contract error and return HTTP 409."
- **Doc-contract check in CI.** `docs/site/scripts/check-doc-contracts.mjs` derives routes from the route source and fails the build with "docs/reference/http-api.rst Routes table is missing the … route". It also bans absolute claims: "the copy says 'continues throughout' / 'keeps serving', never a 'never'".
- **Publish the failed runs.** `tutorials/reefine/README.md`: "The demos here script that path end to end on this machine and record what the model did, working or not".

## 6. Flags

Text in my unit that addresses a coding agent directly, quoted and not acted on:

- **`docs/site/AGENTS.md`** (lines 1–9). The file says it is auto-written by `next dev`. It opens with "# This is NOT the Next.js you know" and continues "Read the relevant guide in `node_modules/next/dist/docs/` … before writing any code. Heed deprecation notices." It ends with: "Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean." This is agent-targeted instruction text, and it tells agents to commit the file.
- **`docs/site/CLAUDE.md`** (line 1) contains only `@AGENTS.md`, an include directive that makes Claude Code load the file above.

Nothing in `docs/` or `tutorials/` asks a reviewing agent for credentials. Two things I saw that are not flags:

- Docs tell *users* to supply `REEF_UPSTREAM_API_KEY`, `WANDB_API_KEY` and `TINKER_API_KEY` through the environment. `tutorials/tinker/README.md` says "never in serve.yaml".
- `evolve-your-harness.rst:198` and `write-a-harness-method.rst:271` mention "`ignore the previous instructions`". They describe a pattern the service screens for, and are not addressed to a reader.

**Files read.**
- **Read in full or nearly so:**
  - `README.md`
  - `LICENSE` (header only)
  - `pyproject.toml`
  - `docs/getting-started/*.rst` (3)
  - `docs/user-guide/{operate,troubleshooting,evolve-your-harness,evolve-your-model,recipes}.rst`
  - `docs/user-guide/recipes/reefine.rst` (first 80 lines)
  - `docs/advanced_topics/state-model.rst`
  - `docs/reference/http-api.rst` (first 400 lines)
  - `docs/contributing/testing.rst`
  - `docs/developer-guide/write-a-harness-method.rst` (first 150 lines)
  - `docs/rfcs/README.rst`, `docs/rfcs/reef-router.rst` (first 60 lines)
  - `docs/community/wechat.md`
  - `tutorials/README.md` and the three tutorial READMEs
  - `tutorials/evolve-your-harness/{run.sh,configs/serve.yaml,harness/evolution.py}`
  - `tutorials/reefine/configs/deployment.yaml`
  - `tutorials/tinker/smoke.py` (first 60 lines)
  - `docs/site/AGENTS.md`, `CLAUDE.md`, `package.json`, the three `scripts/*.mjs` (`check-doc-contracts.mjs` first 200 lines, `fetch-repo-stats.mjs` first 80)
  - `docs/site/components/home/logo-wall.tsx`, `docs/site/lib/news.ts`
- **Outside my unit, read only to confirm claims:** `SECURITY.md`, `.gitmodules`, the four `.github/workflows` files named in the table, `reef/service/profiles/reefine.yaml`, `reef/service/routes/inference.py`, and `tests/reef_service/test_{reefine_tutorial,harness_example}.py` (headers).
- **Not read:** the other `docs/reference/` and `docs/developer-guide/` pages, the per-recipe pages under `docs/user-guide/recipes/` (except `reefine.rst`), most RFCs, the notebook, the Reefine `run.py` and `run.sh`, and the remaining site components.
- **Note on `docs/site/scripts/fetch-repo-stats.mjs`:** it makes GitHub API calls at build time. On a developer machine it falls back to `gh auth token`, which is the developer's own GitHub token, and it never fails the build.
