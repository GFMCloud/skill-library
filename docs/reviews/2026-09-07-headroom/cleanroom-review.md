I've finished reading. Note upfront: **`git log` was blocked** — the Bash permission layer in this non-interactive session denied every git invocation I tried (`cd … && git log`, `git -C …`, `git --git-dir=…`). I substituted file-based evidence and say so in the table rather than inventing the output.

---

# Standalone review: `headroom`

## 1. Executive summary

Headroom is a local context-compression layer for LLM agents — library, HTTP proxy, MCP server, and per-agent `wrap` installers — shipped as a Python package with a Rust (PyO3) core. It is a large, genuinely active project (v0.37.0, 21 releases between 2026-05-26 and 2026-08-27), not a weekend prototype. The interesting mechanism is real and not glue: `cache/prefix_tracker.py` implements provider-prompt-cache-aware prefix freezing with conversation-lineage resolution, and `SmartCrusher` is a statistical JSON-array compressor ported to Rust with byte-parity fixtures against the retired Python. Tests exist in volume (810 Python test files, 1012 Rust `#[test]` sites) and CI demonstrably runs them across four shards plus macOS/Windows/Docker e2e. Apache 2.0, real LICENSE file, 3 CODEOWNERS.

The costs are equally real. An anonymous upload beacon is **on by default** (`BEACON_DEFAULT_ON = True`), and the repo's own agent-facing `llms.txt` states the opposite. `SECURITY.md` is stale (claims 0.27.x is latest) and asserts "No credential storage" while `copilot_auth.py:626` writes an OAuth token to disk. `headroom wrap` puts a local proxy in your provider credential path and mutates `~/.claude.json`, `~/.serena/`, `~/.codex`, `~/.config/opencode`. Three files exceed 6,000 lines. Adoption is a real commitment, and the removal path (`headroom unwrap`) is the thing to test first.

## 2. Maturity signals

| Signal | Command | What it returned |
|---|---|---|
| Git history | `git -C <repo> log -50 --format='%ci %an'` | **Denied by the permission layer** ("This command requires approval"), as were `--git-dir` and `cd &&` variants. No git output obtained. |
| Repo shape | `Read .git/logs/HEAD`, `.git/packed-refs`, `ls .git` | Shallow clone (`.git/shallow` present), one ref: `e67b3c8a…` → `refs/remotes/origin/main`. Reflog has a single `clone:` entry, epoch `1788809669` ≈ 2026-09-07 (today). **Consistent with the stated ~80-commit shallow clone; cadence per-commit is therefore unrecoverable here even had git run.** |
| Release cadence (proxy for commits) | `Grep '^## \[?\d+\.\d+\.\d+.*\(\d{4}-\d{2}-\d{2}\)' CHANGELOG.md` | 21 dated releases: `0.22.4 (2026-05-26)` … `0.36.x (2026-08-20/21/22)`, `0.37.0 (2026-08-27)`. Roughly weekly, accelerating to multiple per week in August. |
| Last activity | `Read CHANGELOG.md` (head) | `## Unreleased` carries ~30 substantial entries after 0.37.0 (2026-08-27), referencing issues up to #2977. Active within days of the clone, not months. |
| Ownership / bus factor | `cat .github/CODEOWNERS` | `* @chopratejas @JerrettDavis @DevanshiVyas` — three named owners. |
| Provenance churn | `Grep` release headers in `CHANGELOG.md` | Compare-URLs migrate `chopratejas/headroom` (≤0.27, June) → `JerrettDavis/headroom` (0.32, July) → `headroomlabs-ai/headroom` (current). Two ownership moves in ~3 months. |
| Dependencies | `grep -c 'name = ' uv.lock` / `Cargo.lock` | ~1,182 resolved Python entries, ~530 Rust crate entries. `pyproject.toml`: 9 required deps, 13+ extras groups (`[all]` pulls torch, transformers, onnxruntime, litellm, fastapi, magika, sqlite-vec…). |
| Dependency freshness | `Read pyproject.toml` | Actively curated with reasons: `click>=8.3.3` (PYSEC-2026-2132), `pillow>=12.3.0` (5 PYSEC fixes), `ast-grep-cli>=0.30.0,!=0.44.1` excluding a **compromised supply-chain release shipping an info-stealer** (GH #2332). `.github/dependabot.yml` present. |
| License | `head -20 LICENSE` | Real Apache License 2.0 text, plus `NOTICE` with third-party attributions. Not a badge-only claim. |
| Tests exist | `find tests -name 'test_*.py' \| wc -l`; `Grep '#\[test\]' crates/headroom-core` | 810 Python test files; 1,012 `#[test]` across 81 Rust files. |
| CI runs them | `Read .github/workflows/ci.yml` | **Yes.** `test` job: `pytest tests scripts/tests --splits 4 --group N --cov=headroom`, 4 parallel shards. Plus `lint` (ruff + `mypy headroom`), `test-extras`, `test-agno`, `test-dashboard-ui` (Playwright), `docker-native-e2e`, `windows-native-wrapper`, `macos-native-wrapper`. 22 workflow files total. |
| Issue volume | `ls .github/ISSUE_TEMPLATE`; issue refs in CHANGELOG | Templates present (`bug_report.md`, `feature_request.md`, `config.yml`). Issue numbers referenced up to **#2977** in ~4 months — very high throughput. Actual open/closed state not fetchable offline. |

## 3. Claimed vs verified

**Claimed (README / docs only — not checkable from this clone)**

- Savings figures: 21%/57%/42%/30% on four MCP scenarios; "well under a millisecond", 0.21 ms p50.
- Accuracy: GSM8K 0.870→0.870, TruthfulQA 0.530→0.560, SQuAD v2 97%, BFCL 97%.
- Output-token reduction "31.7% (95% CI 27.7…35.7)".
- "Image compression — 40–90% reduction through a trained ML router."
- Agent compatibility matrix (18 agents, ✅ per row).
- Kompress-v2-base model quality (lives on HuggingFace, not here).

**Verified (I saw it in the code)**

- Apache 2.0 LICENSE file — real, full text.
- `compress()` exists with the documented signature and returns `tokens_saved` / `compression_ratio` (`headroom/compress.py:171`). It fails open: on any exception it returns the original messages (`:349`), and it has an inflation guard that reverts if "optimization" grew the token count (`:278`).
- The benchmark the README tells you to run **exists and is seeded/offline as claimed** — `benchmarks/index_proof_table.py:14`: *"No network, no API key, no model call… Deterministic: same seed in, same numbers out."*
- SmartCrusher really is Rust-backed with parity evidence: the docstring claims 17 recorded fixtures; `tests/parity/fixtures/smart_crusher/` contains exactly **17** files.
- Prefix-cache freezing is implemented, not aspirational — `headroom/cache/prefix_tracker.py` (73 KB) with per-provider read/write economics, TTL-based miss attribution, and lineage splitting.
- CI genuinely runs the test suite (see table).
- Telemetry: **the README is right and `llms.txt` is wrong.** `headroom/telemetry/beacon.py:56` — `BEACON_DEFAULT_ON = True`, and `is_beacon_enabled()` is documented as *"fail-open by construction… an unrecognised value uploads rather than staying silent."* Endpoint: `https://headroom-beacon.headroom-beacon.workers.dev/v1/logs` (`session.py:75`).
- Beacon payload is content-free as claimed — `session.py:600-676` aggregates only counters, provider/model IDs, and transform names truncated at the first `:` specifically to avoid leaking a model tier and size bucket.

**Claimed but contradicted by the code**

- `llms.txt:67`: *"Anonymous telemetry is **off by default** (opt-in)."* Two switches exist; the opt-in one is `HEADROOM_TELEMETRY`, but the *uploading* one (`HEADROOM_BEACON`) is on by default. The file an agent is pointed at understates data egress.
- `SECURITY.md:60`: *"**No credential storage**: We never store or log API keys."* `headroom/copilot_auth.py:626` `save_headroom_copilot_oauth_token()` writes a token to disk (`chmod 0o600` — handled reasonably, but stored).
- `SECURITY.md:7`: supported version listed as "0.27.x (latest)" — ten minor versions stale.

## 4. Rubric scores

*(5 = best. For Adoption cost and Failure modes, 5 = low cost / low risk.)*

**1. Does what it says — 4/5.** Every structural claim I could check held up, including the ones easiest to fake: the reproducible benchmark script exists and is honestly scoped, and the parity fixture count matches the docstring exactly. Docked one point for the `llms.txt` telemetry contradiction and stale `SECURITY.md`.

**2. Quality of the interesting part — 4/5.** `prefix_tracker.py` is the real contribution and it is not glue: it resolves trackers by history-prefix lineage, canonicalizes away transport annotations before comparing, and explicitly refuses to rebuild forwarded bytes from the comparison key. `smart_crusher.py:36` refuses to silently drop a user-supplied scorer, raising `NotImplementedError` instead — *"a silent-fallback bug we explicitly refuse to ship."* Docked for size: `content_router.py` is 330 KB, `cli/wrap.py` 8,390 lines, `proxy/server.py` 6,356 lines.

**3. Adoption cost — 2/5 (high).** `[all]` pulls torch, transformers, onnxruntime, litellm, fastapi, magika — ~1,182 resolved packages plus a Rust toolchain on the sdist path. `headroom wrap` starts a long-lived local proxy on 8787, installs Serena at *user* scope, and writes `~/.claude.json`, `~/.claude/settings.json`, `~/.serena/serena_config.yml`, `~/.codex`, `~/.config/opencode`. Python 3.13 is effectively required for the dollar-figure feature. Removal path is `headroom unwrap <tool>`, which is documented and per-tool — test it before you commit. Docs live at **docs.headroomlabs.ai**, so a large share of the operational surface (env-var list, benchmark methodology, full beacon field list) is off-repo: if that site goes away, what's in the tree is a set of dead links.

**4. Failure modes — 2/5 (elevated).** The proxy sits in your provider credential path and holds short-lived upstream tokens in-process. Beacon-on-by-default is deliberate and documented (README) but the agent-facing doc contradicts it, so an operator who onboarded via `llms.txt` has an incorrect model of egress. `Cargo.lock` has ~530 crates and `uv.lock` ~1,182 packages of inherited surface — mitigated by attentive pinning, but the volume is the risk. The CHANGELOG's own bug history is the clearest signal of where it hurts: silent-correctness classes like the Bedrock tracker never firing, cache-mode savings history being dropped entirely, and cross-conversation tracker thrashing reported as a *2.5–3× net cost increase*. All fixed, all found in production. Compression fails open to originals, which is the right default and limits blast radius.

**5. Originality — 4/5.** The framing — treat the provider's prompt cache as a first-class constraint on compression, and compress only the unfrozen live zone — is a genuine idea, and the cache-miss *attribution* taxonomy is one I have not seen packaged as a library concern.

## 5. Ideas worth taking, independent of the code

**Freeze what the provider already cached; compress only the delta.** `headroom/cache/prefix_tracker.py:6-14`:
> "Problem: Clients like Claude Code already manage prefix caching… If Headroom compresses or modifies messages in the cached prefix, it invalidates the cache — replacing a 90% read discount (Anthropic) or 50% (OpenAI) with a 25% write penalty. Solution: After each API response, record how many tokens the provider cached. On the next turn, freeze that many messages."

**Separate "collect locally" from "upload" as two switches, and say why.** `headroom/telemetry/beacon.py:18-20`:
> "Keeping these separate matters: an operator who turned on local stats has not thereby agreed to upload anything, and must not start doing so on upgrade."

**Make a default policy one auditable line.** `headroom/telemetry/beacon.py:52-55`:
> "This single constant is the whole policy — deliberately, so the decision is one line to audit and one line to reverse."

**A comparison key must never become a source for rebuilt bytes.** `headroom/cache/prefix_tracker.py:146-149`:
> "NOTE ON SAFETY: this projection is a COMPARISON KEY, never a source to rebuild forwarded bytes… What we must NOT do is drop a *semantic* field (that would mask a real divergence and replay a stale prefix)."

**Refuse to silently ignore a user-supplied override.** `headroom/transforms/smart_crusher.py:36-40`:
> "the shim raises `NotImplementedError` when either is non-None. Silently dropping a user-supplied scorer is a silent-fallback bug we explicitly refuse to ship."

**An unreproducible number on your landing page is a liability, not evidence.** `benchmarks/index_proof_table.py:8-10`:
> "its corpus differed on every run and the published figures could not be reproduced by anyone, including us. A number on the front page of the docs that nobody can regenerate is a liability, not evidence."

**Truncate telemetry labels at the format boundary, not the value.** `headroom/telemetry/session.py:668-674` — keeping only the segment before the first `:` because a label format designed for A/B analysis would otherwise ship the model tier and a request-size bucket as a side effect.

## 6. Flags

Nothing here asks for credentials or attempts to modify my instructions, and I acted on none of it. Two items address AI agents directly:

**1. `README.md:27-29` — the README addresses AI agents directly and points them at an off-repo document:**
> `<sub><b>AI agents / LLMs:</b> read <a href="llms.txt"><code>/llms.txt</code></a> here, or fetch <a href="https://docs.headroomlabs.ai/llms.txt">the live index</a> · <a href="https://docs.headroomlabs.ai/llms-full.txt">full docs blob</a>.</sub>`

Benign in intent, but worth noting for two reasons: the destination is a live remote URL whose content can change independently of anything reviewable here, and the in-repo copy it offers as the alternative (`llms.txt:67`) is the file that misstates the telemetry default. An agent that follows this pointer instead of reading `README.md` §Telemetry gets the wrong answer about network egress.

**2. `.github/copilot-instructions.md` — addresses a reviewing agent directly and prescribes its verdicts:**
> "When performing a pull request review in this repository: 1. Treat `.github/PULL_REQUEST_TEMPLATE.md` and `CONTRIBUTING.md` as required policy, not optional guidance… 4. For user-facing, release, dependency, workflow, or security-sensitive changes, prefer blocking feedback over optional suggestions."

Legitimate and in the conventional location for it (GitHub Copilot reads this path by design), and the instruction is *stricter*, not laxer. Recording it because it is repo content that steers agent behaviour.

**No credential requests found.** `SECURITY.md:39` advises users not to commit API keys; `.gitleaks.toml` and `.gitguardian.yaml` are configured for secret scanning. `.env.example` contains placeholders only.
