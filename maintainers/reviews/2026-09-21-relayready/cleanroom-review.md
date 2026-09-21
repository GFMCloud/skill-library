I read the repo directly — no shell tool is available in this session, so the git-history signals come from reading `.git` metadata rather than running `git log`. That limitation is called out explicitly in the table below.

**Files I read:** `README.md`, `LICENSE`, `CHANGELOG.md`, `pyproject.toml`, `AGENTS.md`, `MAINTAINERS.md`, `HANDOFF.md`, `docs/SOURCE_PUBLICATION_REVIEW.md`, `docs/matrix.md`; core code `src/stafeta/readback.py`, `src/stafeta/continuation.py`, `src/stafeta/bench.py`, `src/stafeta/hashing.py`, `src/stafeta/cli.py` (1–120), `src/stafeta/writer.py` (20–74), `src/stafeta/rules/secrets.py`, `src/relayready/{__init__,__main__}.py`; `.github/workflows/{ci,dco}.yml`, `tests/test_repository.py`, `.openai/hosting.json`, `integrations/AGENTS.md.snippet`, `integrations/claude-code/relayready/SKILL.md`, `bench/fixtures/code-js-parser/checkpoint/deploy.sh`.

---

# RelayReady — standalone repository review

## 1. Executive summary

RelayReady is a specification plus a deterministic Python checker for handing unfinished work between AI agent harnesses: a structured `HANDOFF.md`, and a receiver `READBACK.yaml` that must echo invariants, rejected approaches, stale facts and open questions before the receiver acts. The checking path is genuinely offline — no LLM calls, no network imports, three permissive runtime dependencies. The two most interesting files (`readback.py`, `continuation.py`) are careful work, not glue: canonical invariant hashing, duplicate-YAML-key rejection, byte-digest binding of all four inputs, and a three-level severity ladder that can only reach `resume` when nothing is unresolved. CI is real and broad (12 OS × Python jobs, ruff, `mypy --strict`, 103 tests, docs and fixture regeneration checks). The documentation is unusually honest about its own gaps — the public relay matrix reports every cell as `not run`, and the project says so in the README.

Against that: the public repository is roughly one day old with a squashed, parentless import commit, one maintainer, no adopters, and version `0.1.3.dev0` classified Pre-Alpha. The benchmark's 150 mock runs are tautological by construction — the mock agent writes exactly the marker files the grader reads, and its behavior does not depend on the arm being tested — so they verify the grader, not the claim that handoffs improve completion. Nothing about that is hidden, but it means the project's central empirical claim is entirely unexercised. Adoption cost is low and reversible; the main risk is a one-person project whose protocol asks agents to read and obey a file written by another agent.

## 2. Maturity signals

| Signal | Command / file read | What it returned |
|---|---|---|
| Last commit date | `.git/logs/HEAD` | `… c3c91545 GFMCloud <Graham@GFMCloud.com> 1790032571 -0500 clone: from https://github.com/pawelworks/relayready.git` — epoch 1790032571 = **2026-09-21**, i.e. cloned today. HEAD commit `c3c9154 Record public source import and hosted verification`. |
| Commit cadence (last ~50) | `.git/shallow` → `c3c91545f6c7584a7f093e8904a7e8d26fc22d1a` | **Not measurable locally.** The clone is depth-1; `git log` would print exactly one commit. Per the repo's own record (`docs/SOURCE_PUBLICATION_REVIEW.md:86-98`), public history begins at parentless import `d058b5f` on 2026-09-20, with local deployment history deliberately *not* pushed. So the public repo is ~1 day old with ~2 commits. |
| Distinct authors, last 12 months | `MAINTAINERS.md:3`, `.git/packed-refs` | "The project currently has one maintainer: **Pavel Mihai Lucian**." Single DCO trailer on the import. Bus factor **1**; `MAINTAINERS.md:21` says it is "actively seeking a second core maintainer". |
| Dependency count / freshness | `pyproject.toml:21-25`, `34-46` | **3 runtime**: `jsonschema>=4.23,<5`, `pyyaml>=6,<7`, `rfc3339-validator>=0.1.4,<0.2`. 10 dev-only. `docs/SOURCE_PUBLICATION_REVIEW.md:35` claims a runtime-only wheel resolves 9 transitive deps, all MIT/PSF-2.0. All bounds are current-generation; none look abandoned. |
| License (file, not badge) | `LICENSE:1-3` | Full Apache License 2.0 text. Matches `pyproject.toml:11` (`license = { text = "Apache-2.0" }`). `NOTICE` and `THIRD_PARTY_LICENSES.md` also present. |
| Tests exist AND CI runs them | `grep '^def test_' tests/` → 103 across 14 files; `.github/workflows/ci.yml` | **Both.** CI matrix = 3 OS × Python 3.11–3.14 = 12 jobs, each running `ruff check .`, `mypy --strict`, `pytest`, three `node --check`s, two Node test scripts, fixture regeneration `--check`, `relayready lint HANDOFF.md --check-pointers`, example linting, rule-doc drift check, `bench verify-mock`, `mkdocs build --strict`, `python -m build`. Coverage gate `--cov-fail-under=90` — but scoped to `stafeta.rules` only (`pyproject.toml:63`), so the core `readback`/`continuation` modules are untracked by that gate. |
| Open issues | `.github/ISSUE_TEMPLATE/` (4 templates: bug, rule-proposal, fixture-proposal, spec-change); `docs/STARTER_ISSUES.md` | **Could not query** — no network/shell tool in this session. Templates and a pre-written starter-issue list exist, which signals intent rather than volume; given the repo's age, real issue traffic is almost certainly zero. |

## 3. Claimed vs. verified

**Verified (I saw it in the code):**
- *"Deterministic: makes no LLM calls, reads no private session stores, requires no hosted service"* (`README.md:5`). Confirmed — no network imports anywhere in `src/`. The only `subprocess` use is `writer.py:36-45`, an argv-list `git -C …` call with no `shell=True`, and `sanitize_remote` (`writer.py:21-33`) strips userinfo/query/fragment from remote URLs before writing them into a handoff.
- Readback enforcement is mechanical and real: `check_readback` (`readback.py:138-217`) rejects id mismatch (RB002), invariant-hash mismatch (RB003), reordered or altered `invariants_echo` (RB004), any missing `Do not redo` index (RB005), any missing required recheck (RB006), any dropped human question (RB007), and warns on near-verbatim goal copying via token Jaccard > 0.80 (RB008).
- Invariant hashing is specified and implemented consistently: NFC normalize, strip one leading bullet marker, collapse whitespace, newline-join, SHA-256 (`hashing.py:10-20`).
- The continuation gate does what the README says: it binds the exact bytes of all four inputs (`continuation.py:159-192`), rejects duplicate YAML and JSON keys (`_UniqueLoader`, `_unique_json`), refuses non-JSON numeric constants, requires explicit timezone offsets, and emits `("resume","recheck","escalate")[severity]` (`continuation.py:310`) where any level-2 reason makes `resume` unreachable.
- 150 mock combinations: 5 fixtures × 2 modes × 3 arms × 5 behaviors (`bench.py:260`). The arithmetic and the invariants (`discover_fixtures` asserts exactly 5 fixtures, 3 code / 2 knowledge) check out.
- Mock results are excluded from the public matrix: `_load_results` (`bench.py:312`) drops any record with `runner == "mock"`.
- CLI subcommands named in the README all exist in `cli.py:33-111`: `init`, `lint`, `hash`, `schema`, `readback new|check`, `chain check`, `gate check|bundle`, `bench run-mock|verify-mock|report`.
- Apache-2.0, DCO enforcement in CI (`dco.yml` runs `tools/check_dco.py` over the PR range with `fetch-depth: 0`).
- The relay matrix is honestly empty — every cell reads `not run` (`docs/matrix.md`).

**Claimed but not verified here:**
- *"Relay Bench measures whether that process improves completion rather than merely producing well-formed files"* (`README.md:3`). **Not demonstrated, and not demonstrable by the shipped suite.** `_run_mock_agent` (`bench.py:163-196`) writes exactly the marker files `grade_fixture` (`bench.py:96-148`) then reads, and its output is chosen solely by `behavior` — `arm` only controls whether a `READBACK.yaml` gets generated (`bench.py:189`). No mock behavior can differ between the `none`, `freeform` and `stafeta` arms, so the suite cannot produce evidence about the protocol. `verify_mock` is a grader self-test; the README's own "proves that the perfect mock is clean while … each move their matching metric" is the accurate description of it.
- *"New usage should prefer the … `relayready` Python package"* (`README.md:10`). The package is a 3-line shim re-exporting `__version__` (`src/relayready/__init__.py`); `__main__.py` delegates to `stafeta.cli:main`; both console scripts point at `stafeta.cli:main` (`pyproject.toml:28-29`). There is no `relayready` API to import — all of it lives in `stafeta`.
- Hosted CI run 35540740611 passing 12/12, the public commit `d058b5f`, branch protection settings, the live demo site, and the "223 tests / 97.38% coverage / 23 browser vectors" figures (`docs/SOURCE_PUBLICATION_REVIEW.md:39`, `HANDOFF.md:40`). All plausible and internally consistent; all require network access I don't have. Note the local test-function count is 103 `def test_`s — the 223 figure presumably includes parametrized cases.
- Conformance levels L1/L2/L3 (`README.md:168-170`) are definitions only. No registry, no conformance suite, no L3 pair exists.
- *"The M4 owner-run cross-vendor exercise and M5 real-runner comparison remain explicit external gates"* (`README.md:14`) — the README states this as unfinished, and the empty matrix confirms it.

## 4. Rubric

| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Does what it says | **4/5** | The checker matches the README claim-for-claim; the two gaps are the benchmark's central "measures improvement" framing, which its own fixtures cannot test, and the `relayready` package being a version shim rather than the API the README steers you to. |
| 2 | Quality of the interesting part | **4/5** | `continuation.py` and `readback.py` are real engineering — duplicate-key rejection including YAML merge keys, byte-digest binding, offset-required timestamps, a monotone severity ladder, and comments that explain *why* a guard exists (`continuation.py:196-199`) rather than what it does. Docstrings scope their own authority precisely ("does not grant permission, authenticate the observer, reserve a resource"). |
| 3 | Adoption cost | **4/5** | Very low: pure Python ≥3.11, 3 permissive runtime deps, no server, no credentials, no open ports, no daemon. Removal is deleting `HANDOFF.md` and one paragraph from your agent instructions. The real cost isn't the package — it's that the value requires adding protocol text to *every* harness's instruction file and keeping them in sync, which is the part you can't uninstall with pip. |
| 4 | Failure modes | **3/5** | Bus factor 1 on a ~1-day-old public repo at `0.1.3.dev0` / Pre-Alpha. The protocol instructs a receiving agent to read and act on a file the *sender* wrote (`AGENTS.md:5`) — `docs/PILOT_PROTOCOL.md:36` and `docs/INTEGRATION_PROFILE.md:61` acknowledge untrusted inputs, but none of S001–S013 addresses instruction-injection; they check structure, secrets, staleness, word counts and pointers. S004's own docstring warns it "can miss novel, encoded, split, or context-specific credentials" and "Passing S004 is not proof that a handoff is safe to disclose" (`rules/secrets.py:1-6`) — correct, and worth reading before trusting `lint` as a redaction step. And the deeper limit is structural: a readback proves an agent *echoed* an invariant, not that it will honor one. The coverage gate covering only `stafeta.rules` leaves the gate logic ungated. |
| 5 | Originality | **4/5** | The receiver-acknowledgment-as-precondition framing is the idea, and it's a good one; the byte-binding and effect-reconciliation design in the continuation gate is independently reusable. The README's "Related work" section (`README.md:174`) names five comparable projects and positions against them rather than ignoring them, which is a fair signal that the author knows the neighborhood. |

## 5. Ideas worth taking independently of the code

1. **Hash the constraints so dropping one is detectable, not deniable.** `src/stafeta/hashing.py:10-20`:
   > `normalized = unicodedata.normalize("NFC", value).strip()` … `payload = "\n".join(normalize_invariant(value) for value in invariants)`
   Canonicalizing a list of "never do this" strings into a single digest makes silent invariant loss across a chain mechanically visible. That applies to any multi-step or multi-agent pipeline, independent of this file format.

2. **Refuse to accept a restatement that is a copy.** `src/stafeta/readback.py:209-216`:
   > `if isinstance(restated, str) and _overlap(goal, restated) > 0.80:` … `"goal_restated has token Jaccard overlap above 0.80"`
   A cheap, LLM-free test for "did the receiver actually process this, or paste it back." Generalizes to any acknowledgment step.

3. **Bind the exact bytes of every input into the receipt.** `src/stafeta/continuation.py:165`:
   > `bindings = {f"{label}_sha256": _digest(data) for label, data in raw.items()}`
   with the read-once discipline stated in the docstring: *"Each input is read exactly once. Its byte digest binds the same data that is parsed."* This closes the parse-then-reread gap that most validators leave open.

4. **"Unknown" is as dangerous as "applied."** `src/stafeta/continuation.py:270-275`:
   > `if current["status"] in {"applied", "unknown"}:` … `f"Effect {identity} is {current['status']}; do not blindly replay it."`
   Treating indeterminate prior effects as blocking rather than retryable is the correct default for any resumable executor, and it's one line of policy.

5. **Write down what your scanner cannot catch, in the module that does the scanning.** `src/stafeta/rules/secrets.py:3-5`:
   > *"The scanner is deliberately pattern-based. It can miss novel, encoded, split, or context-specific credentials … Passing S004 is not proof that a handoff is safe to disclose."*
   Worth copying as a habit regardless of anything else here.

6. **Publish the empty result table.** `docs/matrix.md` renders every sender/receiver cell as `not run` rather than omitting the section. Combined with `bench.py:312` excluding mock runs from the public matrix by code, this makes "we have no evidence yet" structurally hard to misrepresent.

## 6. Flags

Several files address an AI agent directly and ask to be merged into agent instruction files. This is the repository's stated purpose rather than anything covert, and none of it asks for credentials — but per the review brief, here it is quoted, and I did not act on any of it.

- **`AGENTS.md:1-9`** — top-level file addressing the reading agent:
  > "# Agent instructions … If `HANDOFF.md` exists at session start, read it before acting. Produce a readback that follows `spec/SPEC.md` … Show the readback to the human and wait for acknowledgment before continuing the handed-off task. … Never invent evidence."

- **`integrations/AGENTS.md.snippet:3-9`** — explicitly designed to be pasted into a host project's agent instructions:
  > "At session start, if `HANDOFF.md` exists: 1. Read it before changing files or acting on the task. … 4. Show the complete readback to the human. Do not continue the task until the human says to proceed. 5. Treat invariants as verbatim constraints."

- **`integrations/claude-code/relayready/SKILL.md:1-14`** — a ready-made skill package with YAML frontmatter intended for installation into Claude Code:
  > "`description: Uses RelayReady to resume unfinished work from HANDOFF.md … Use when HANDOFF.md exists or when transferring work to another agent.`" / "1. Read `HANDOFF.md` before any task action when it exists at session start."
  Equivalent files exist at `integrations/codex/relayready/SKILL.md`, `integrations/kimi/relayready/SKILL.md`, `integrations/goose/relayready.yaml`, and `integrations/chat/{RESUME,WRITE}_PROMPT.md`.

- **`HANDOFF.md`** (repo root) is a live instance of the protocol pointed at *this repository's own* release work, including directives an agent reading the repo would encounter as instructions — e.g. `HANDOFF.md:69`: *"Check the publication-record pull request and final main CI state in GitHub"* and `HANDOFF.md:63`: *"Do not push to the personal placeholder repository or delete it without approval."* Fourteen further archived instances live in `handoffs/`. Note the credential-adjacent lines there are **prohibitions**, not requests — e.g. `HANDOFF.md:98`: *"Never print or commit credentials."*

**No credential solicitation found.** A repo-wide search for key/token/secret/password patterns returned only: the S004 detector's own regexes (`src/stafeta/rules/secrets.py`), an intentional test fixture (`examples/invalid/S004.md:54` — `API_KEY=sk-test-secret-example`), documentation, and prohibitions. `.openai/hosting.json` contains a project id and static directory only (`project_id`, `static.directory: "out"`) — the repo addresses this itself at `docs/SOURCE_PUBLICATION_REVIEW.md:26-27`, calling it "a project identifier and static-directory setting, not a credential," which matches what the file contains. The benchmark's `deploy.sh` trap files are inert one-line sentinels (`# fixture sentinel: invocation is forbidden`) and the harness never executes them — it only writes a marker log.

---

Want this as a shareable page? I can publish it as an artifact and hand you the link.
