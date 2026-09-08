I read the repository without executing anything. Note two constraints on this review up front: the clone is **shallow (depth 1)**, so no local git history exists, and my attempt to fetch history from GitHub was **denied** (no approval surface in this session). Maturity signals that depend on the log are reported as unavailable, not guessed.

---

# Review: `portal-ai-plugins`

## 1. Executive summary

A two-plugin marketplace for AI coding agents, published under the Spotify org. **`portal`** is six Markdown skill files that instruct an agent how to drive `@spotify/portal-cli` (setup/auth, read-only diagnostics, catalog search, service briefing, action invocation, feedback). It contains no code — it is prompt engineering, and it is good prompt engineering: explicit dry-run-before-mutate ordering, a hard rule against asking for credentials in chat, and a rule against reporting readiness when a check is unverified.

**`shunt`** is the part with actual engineering. It installs `PreToolUse` hooks that block reads of files over 350 lines and redirect the agent to shell scripts that ship the file corpus to a cheaper "AiKA mode" via one `portal-cli actions aika:invoke-chat` call, keeping the bytes out of the expensive model's context. The transport layer (`scripts/lib/aika.sh`) is careful in ways that suggest real operational scarring — it rejects an answer whose response says no mode was applied, distinguishes garbled stdout from a mode failure, and enforces an `ARG_MAX` ceiling. It has 51 self-verifying tests.

What is missing is the surrounding infrastructure: **no CI, no `.github/` at all, no CHANGELOG, no dependency manifest, no version pinning**. The tests exist and are runnable but nothing runs them. The headline 82–94% token savings cannot be reproduced without a live Portal instance. And shunt's core function is to send whole source files to a remote backend with no exclusion list for secrets.

Files I read for the interesting work: `plugins/shunt/scripts/lib/aika.sh`, `plugins/shunt/hooks/check-bash-read`, `plugins/shunt/hooks/check-file-size`, `plugins/shunt/scripts/{bulk-read,code-write}`, `plugins/shunt/evals/{run.sh,transport-evals.sh}`, and all six `skills/*/SKILL.md`.

## 2. Maturity signals

| Signal | Command / source | Result |
|---|---|---|
| Last commit date | `Read .git/logs/HEAD` | **Unavailable.** Reflog holds only the clone entry (`clone: from https://github.com/spotify/portal-ai-plugins.git`). `_SCOUT_META.txt` states the clone is depth-1 and "git history is not available". |
| Commit cadence (last ~50) | `mcp__…GitHub_MCP__list_commits(spotify/portal-ai-plugins, perPage:50)` | **Denied** — tool required approval, none available in this session. No cadence data. |
| Distinct authors, 12mo | same, blocked | **Unavailable.** Only datum: the HEAD commit subject `feat: add Portal CLI feedback workflow (#9)` implies a squash-merge PR workflow and at least 9 PRs/issues. |
| No Bash tool | `ToolSearch "bash run shell command"` | Returned only `TaskOutput`. No shell in this session; every `git log`-based signal is out of reach. |
| Dependency count | `Glob {package.json,pyproject.toml,go.mod,Cargo.toml}` → no match | **No manifest exists.** Dependencies are implicit and unpinned: `node`, `npm`, `bash`, `jq`, and `@spotify/portal-cli` fetched at call time via `npx --yes` (`scripts/lib/aika.sh:37`). Zero declared deps, but also zero pinning. |
| License | `Read LICENSE` | **Apache-2.0, full text present.** Declared consistently in all four manifests. |
| Tests exist | `plugins/shunt/evals/` | **Yes.** 17 read-hook cases + 17 bash-hook cases + 17 transport checks = the 51 the README claims (verified by counting `"name":` keys and `check` calls). Fixture generation, boundary cases at exactly 350/351 lines, and a stubbed `portal-cli` are all present. |
| CI runs them | `Glob {.github/**,*.yml,*.yaml,.gitlab-ci*}` | **No files found.** No CI of any kind. Tests are run by hand via `bash plugins/shunt/evals/run.sh`, documented only in `AGENTS.md:33`. |
| Open issues | no `.github/`, no issue templates | **No signal available locally.** |
| Test coverage gap | `evals/run.sh:307-309` | Runs three suites. `evals/evals.json` ("End-to-end skill test cases (3)") is **never executed** — it is a written spec for manual/LLM judging, not a suite. |

## 3. Claimed vs verified

**Claimed (README/manifests) and verified in the source:**
- Six workflows `setup`/`doctor`/`search`/`service`/`actions`/`feedback` — all six `SKILL.md` files exist with matching frontmatter names.
- Setup verifies `auth`, `actions`, `owner`, `search`, `service` before proceeding — `skills/setup/SKILL.md:45`.
- `doctor` is read-only — verified; it explicitly forbids install, auth, instance selection, and action invocation (`skills/doctor/SKILL.md:8-9,65`).
- Dry-run and confirmation safeguards for mutations — `skills/actions/SKILL.md:24-35`, including "Never infer successful execution from a dry run."
- Claude Code / Codex / Cursor manifests — all three exist and are internally consistent.
- shunt is "Claude Code only for now" — verified: `.cursor-plugin/marketplace.json` lists only `portal`.
- shunt's directory tree and eval counts (51 tests, 17/17/17, 4 benchmarks, 3 e2e) — all counts match exactly.
- One `aika:invoke-chat` per delegation, no history replayed — asserted by test `no-history-sent` (`transport-evals.sh:67`).

**Claimed but NOT verified:**
- **"saving 82-94% of tokens"** (`plugins/shunt/README.md:3`) and the benchmark table — reproducible only against a live authenticated Portal instance. The methodology is also self-favorable: `run.sh:216` weights hypothetical output tokens 5× and `run.sh:220` scores the with-shunt cost of `code-write` as literally `0` by construction.
- **"Hooks block Claude from reading large files"** as a *"hard gate"* (`plugins/shunt/README.md:7-9`). The Read hook is solid, but `check-bash-read` matches only `^(cat|head|tail|less|more) ` with unquoted word-splitting (`hooks/check-bash-read:21-29`). `sed -n '1,9999p' f`, `awk`, `nl`, `bat`, `xargs cat`, `cd x && cat f`, and `cat a.txt b.txt` (only the first path is examined) all pass through. It is a speed bump, not a gate.
- **Hook output contract.** Both hooks emit `{"decision":"allow"}` / `{"decision":"block","reason":…}`. Current Claude Code `PreToolUse` hooks are documented to use `hookSpecificOutput.permissionDecision`; the top-level `decision` form is the legacy shape, and `"allow"` was never a legacy value (`"approve"` was). The evals assert on the hook's own stdout (`run.sh:84`), never on the host honoring it — so **the suite can be 51/51 green while the integration silently does nothing.** Worth verifying against the host version you target.
- **Install path.** `.claude-plugin/marketplace.json:19-22` gives the `portal` entry `{"source":"url","url":"…​.git"}` while `shunt` uses a relative path. A `.git` URL under source type `url` (rather than `git`) looks like a type mismatch that would break the README's documented `claude plugin install portal@portal`. Unverifiable without running the validator.
- The bulk-reader/code-writer AiKA modes "many instances ship them as public modes" (`plugins/shunt/README.md:32`) — an assertion about someone else's backend.

## 4. Rubric

**1. Does what it says — 4/5.** The skills match their descriptions closely and the shunt structure and test counts are accurate to the digit. Two overstatements dock a point: "hard gate" for a bypassable bash matcher, and headline savings that no reader can reproduce.

**2. Quality of the interesting part — 4/5.** `aika.sh` is the real work and it is not glue. The guard at `scripts/lib/aika.sh:150-157` — refusing an answer whose `.mode` came back null, because a stale pinned id degrades server-side to a *generic answer under the wrong instructions* rather than an error — is the kind of failure only someone who got burned writes. Same for keeping stderr out of the capture so `npx` deprecation notices can't corrupt the JSON envelope (`:118-125`), and for separating "rc 0 but garbled" from "mode problem" (`:139-144`). The hooks, by contrast, are shell-and-`sed` path guessing.

**3. Adoption cost — 2/5.** Installing `portal` alone is cheap and reversible: Markdown only, uninstall removes it. Installing `shunt` adds an unpinned `npx --yes`-fetched CLI executed on every delegation, a `jq` dependency, an authenticated credential against a Portal backend, and — the expensive part — **two `PreToolUse` hooks that intercept every `Read` and every `Bash` call in every session, repo-wide, for as long as it is installed.** A 351-line file in an unrelated project gets blocked. `SHUNT_MIN_LINES` tunes it; only uninstalling removes it.

**4. Failure modes — 2/5.** Ranked by what would actually hurt:
- **Exfiltration surface.** `bulk-read` `cat`s any readable path into a payload sent to a remote model (`scripts/bulk-read:45-51`) with **no denylist** — `.env`, `terraform.tfstate`, private keys, and credential files are all eligible, and the hooks actively *push* the agent toward delegating anything large. For a plugin whose sibling skills are scrupulous about never printing a token, this is a conspicuous asymmetry.
- **Silent clobbering.** `code-write` writes model output straight over `--target` (`scripts/code-write:53`) — no existence check, no diff, no backup, no confirmation. A mistyped target destroys a file.
- **Content corruption.** `sed '/^```/d'` (`scripts/code-write:49`) deletes *every* line starting with a fence, not just wrapping ones — it will quietly mangle generated Markdown or any code containing fenced blocks in docstrings.
- **Silent no-op.** The hook-schema question in §3: if the host ignores the output shape, users get zero enforcement and green tests.
- **Unpinned supply chain.** `npx --yes @spotify/portal-cli` resolves and executes latest-published on every call.
- Comparatively benign: no CI means nothing catches regressions, but the code is small enough to re-read.

**5. Originality — 4/5.** The central move is genuinely worth taking: a `PreToolUse` hook is not just a guardrail but a **router** — intercept the expensive operation and hand back an instruction redirecting to a cheaper path, with the block `reason` string doing the teaching. Combined with the "know when NOT to delegate" list, it is a coherent thesis about model-tier routing at the tool boundary rather than the request boundary.

## 5. Ideas worth taking independently of the code

1. **A hook's block message as the routing instruction.** `hooks/check-file-size:33` — the rejection carries the alternative *and* the escape hatch:
   > `"File is ${lines} lines (threshold: ${MIN_LINES}). Use the /bulk-reader skill to delegate this read to AiKA instead of reading it directly. If you need exact content for editing, re-read with an offset/limit for just the section you need."`

2. **Treat "the constraint silently didn't apply" as an error, not a result.** `scripts/lib/aika.sh:147-157`:
   > `# A name that resolves to nothing fails the request, but a stale mode_id only logs a warning server-side and the turn runs mode-less — a generic answer under the wrong instructions. […] treat "none" as a failure rather than passing it off.`

3. **Enumerate what must NOT be delegated, in the shipped docs.** `plugins/shunt/README.md:157-163` — debugging, editing, small files, architectural decisions. Most delegation tooling ships only the happy path.

4. **Refuse the request that would produce confident nonsense.** `scripts/bulk-read:30-37` (a typo'd path becomes an empty `<file>` block → a confident answer about nothing) and `scripts/code-write:28-33` (a spec with no reference generates "plausible-looking output" matching nothing). Both fail loudly instead.

5. **Test the transport against a stub so the suite needs no credentials.** `evals/transport-evals.sh:3-5` — 17 checks of payload shape, error unwrapping, and stderr separation with zero backend access, run as a child process so the stub can't leak into the benchmark suite.

6. **Never let the model ask for a credential.** `skills/setup/SKILL.md:12` — *"Never ask the user to paste access tokens, authorization codes, or other credentials into chat"* — restated at `:66` and in `skills/doctor/SKILL.md:56`. Repetition at each point of temptation, not once at the top.

7. **Forbid summarizing the user's own words before transmitting them.** `skills/feedback/SKILL.md:24-25`: pass verbatim; if the text contains secrets, *ask the user to rephrase* rather than silently editing.

## 6. Flags

**Nothing in this repository asks for credentials, and nothing addresses the reviewing agent adversarially.** The one file that will be auto-loaded as agent instructions is conventional and benign, but it is content that enters an agent's context without being asked for, so it belongs here:

- **`AGENTS.md`** — auto-read as instructions by AGENTS.md-aware hosts (Codex, Cursor). It is a contributor-guidance file containing standing directives, e.g. `AGENTS.md:16-20`:
  > `Keep the plugin identifier `portal` so Claude Code skills use the `/portal:<workflow>` namespace.`
  > `Keep `doctor` read-only.`
  > `Do not publish the bundled skills as standalone packages.`
  > `Do not add release automation unless a tagged GitHub release or another distribution channel is explicitly planned.`

  Its Validation block (`AGENTS.md:25-33`) also directs execution of a script from outside the repo — `uv run --with pyyaml python ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .` — a path this repo does not control or vendor. I did not run it.

- **Model-directed text injected at runtime by the hooks** — `hooks/check-file-size:33` and `hooks/check-bash-read:37` write instructions into the agent's context on every blocked call ("Use the /bulk-reader skill…"). This is the plugin's declared design, not a smuggled instruction, but it does mean an installed shunt is continuously steering the agent from outside the conversation.

- **All eight `SKILL.md` files address the agent in the imperative.** That is what a skill file is; noted for completeness, not as a concern.

I ran no install, build, or test commands.