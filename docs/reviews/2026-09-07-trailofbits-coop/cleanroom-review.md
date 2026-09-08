# Clean-room review: `coop`

## 1. Executive summary

`coop` is a Rust CLI (Apache-2.0, v0.5.4, Trail of Bits) that runs Claude Code and Codex inside disposable microVMs — Firecracker on Linux, Lima on macOS — behind a compile-time `VmBackend` trait. The README understates the project: the tree also holds a devcontainer.json translator, a fine-grained GitHub PAT wizard with Keychain/secret-tool/1Password backends, image commit/restore, editor and port-forward integration, and a separate `coop-proxy` binary. That proxy is the interesting part and it is good work: default-deny method/path allowlist per provider, constant-time capability-token check, credential injected host-side and never exposed to the guest, pinned webpki roots with a real negative test, and a tiered Landlock jail that fails closed on its filesystem/exec floor. Its self-test has a unit test asserting the probe *fails* when unconfined — the check isn't hollow. Test density is high (1208 test attributes across 47 files) and CI runs fmt, clippy `-D warnings`, `cargo test --workspace`, `cargo-deny`, taplo and zizmor with SHA-pinned actions. Two caveats: the VM integration suite, fuzzing, kani and mutation testing are **not** in CI (manual, both platforms), and `coop update` silently degrades from Sigstore attestation to checksum-only when `gh` is absent. Adoption cost is real — a VM runtime, a guest image, host processes holding live API keys, ~216 crates — but removal is clean (`coop uninstall --purge`, `coop destroy --all`, single binary).

**Blocked:** this session has no Bash tool and the GitHub MCP calls were auto-denied (no approval surface). Commit dates, cadence, author count and issue volume could not be obtained. The checkout is also a shallow clone, so the history isn't local either. Those rows are marked unavailable below rather than guessed.

## 2. Maturity signals

| Signal | Command / evidence | Result |
|---|---|---|
| Last commit date | `git log` — **no Bash tool in this session**; `.git/shallow` present (shallow clone, history not local); GitHub MCP `list_commits` **denied** | **Unavailable.** Only HEAD known: `cbfe027 Merge pull request #450 from trailofbits/up-new-instance` |
| Commit cadence (last ~50) | same as above | **Unavailable.** Indirect proxy: CHANGELOG holds 14 tagged releases (`v0.2.5` → `v0.5.4`) plus a substantial `## Unreleased` section — but the file carries no dates, so this shows shipping, not recency |
| Distinct authors, 12mo | `git log --format='%an'` unavailable; MCP denied | **Unavailable.** Single-org project (`trailofbits`); PR-based flow evidenced by the merge-commit HEAD and `.github/workflows/claude-review.yml` + `codex-review.yml` |
| Dependency count | `Grep '^name = ' Cargo.lock -c` | **218** lock entries → ~216 third-party crates (2 are the workspace members). Direct deps are conservative and mainstream: `clap`, `serde`, `anyhow`, `thiserror`, `toml`, `tracing`, `dirs`, `url`, `semver`, `sha2`; `coop-proxy` adds `tokio`/`hyper`/`rustls`+`aws-lc-rs`/`webpki-roots`/`landlock`. `.github/dependabot.yml` present; `deny.toml` + a CI `cargo deny --workspace check` job gate advisories/licenses/bans/sources |
| License file | `Read LICENSE` | Real **Apache License 2.0** text (not a badge); matches `license = "Apache-2.0"` in `Cargo.toml` |
| Tests exist AND CI runs them | `Grep '#\[test\]\|#\[tokio::test\]\|proptest!' -c` → **1208 across 47 files**; `Read .github/workflows/ci.yml` | **Partially verified.** CI runs `cargo test --workspace`, plus `tests/integration-install.sh`, `integration-update.sh`, `integration-uninstall.sh`. `Grep 'integration\.sh|run-integration|kani|fuzz' .github/` → **no matches**: the VM integration suite, fuzz targets, kani proofs and `cargo-mutants` are documented and configured (`.cargo/mutants.toml`, `fuzz/` excluded workspace) but run **only by hand** |
| Open issues, newest 10-20 | GitHub MCP `list_issues` **denied** | **Unavailable.** Code references live issue numbers (`#411` proxy, `#432` reprovision) in doc comments and CHANGELOG, which implies tracked, referenced work |

**Files I read** (entry points first, not the README's description): `src/main.rs` (6-line shim) → `src/lib.rs` (CLI dispatch, lines 1–1593 of 2530) → `coop-proxy/src/main.rs` → `coop-proxy/src/proxy.rs`, `coop-proxy/src/jail.rs`, `coop-proxy/src/tls.rs`. Plus `README.md`, `LICENSE`, `CHANGELOG.md`, both `Cargo.toml`s, `.github/workflows/ci.yml`, excerpts of `.github/workflows/release.yml`, `src/update.rs`, `src/secret_store.rs`, `docs/trust-model.md`, `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, `.claude/hooks/closeout-review-gate.sh`.

## 3. Claimed vs verified

**Claimed (README/CHANGELOG), not checked in code**
- `coop setup` installs Firecracker and fetches a guest kernel on Linux; requires Lima on macOS (`src/setup.rs`, `src/lima.rs` exist and are `#[cfg]`-gated as described — I did not read their bodies).
- "tested on macOS arm64 and Linux x86_64; Linux arm64 builds available but untested."
- The `curl | bash` installer at `install.sh` (CI has an "installer provenance" integration test; I did not read the script).
- Codex ChatGPT-account auth via GNOME Keyring wrapper; devcontainer feature translation; `restore --reprovision` semantics.

**Verified in code**
- Rust CLI over a compile-time backend trait — `src/lib.rs:30-58` gates `lima`/`vm`/`network`/`setup` by `target_os`; dispatch at `src/lib.rs:928`.
- Credential proxy keeps the API key off the guest — `coop-proxy/src/proxy.rs:364-399`: guest `Authorization`/`x-api-key` stripped, `Host` pinned to the configured upstream, real credential injected and marked `set_sensitive(true)`. Secret arrives via stdin only (`coop-proxy/src/main.rs:80-86`, "never argv, never a file").
- SSRF closed: upstream host/port fixed by host config, only path forwarded — `proxy.rs:45`, `origin_form()` at `proxy.rs:425`.
- Default-deny provider operations — `proxy.rs:249-262` allows exactly `POST /v1/responses` (OpenAI) and `POST /v1/messages{,/count_tokens}` (Anthropic); 6 tests cover admin-API denial, stored-response reads, cross-provider leakage, unknown upstream.
- Constant-time token comparison — `proxy.rs:328-359`.
- Concurrency cap actually bounds streaming requests — `GuardedBody` at `proxy.rs:65-88` holds the semaphore permit until the body drains.
- No path that skips TLS verification; pinned Mozilla roots — `coop-proxy/src/tls.rs:18-35`, with `rejects_untrusted_upstream_cert` standing up a self-signed server and asserting refusal (`tls.rs:63-95`).
- Landlock jail, tiered, fail-closed floor — `jail.rs:120-202`; refuses to start if the fs-write/exec floor isn't `FullyEnforced` (`jail.rs:147`); `--no-jail` exists but is documented as test-only (`main.rs:51-68`).
- Refuses to bind an unspecified address — `proxy.rs:127-132`.
- `coop update` verifies `SHA256SUMS` then `gh attestation verify` — `src/update.rs:728-750`; release workflow publishes SLSA build provenance (`release.yml:106-158`).
- Strict lint policy is real, not aspirational — `Cargo.toml:57-72` denies `unwrap_used`, `panic`, `todo`, `exit`, `print_stdout`/`print_stderr`; every exception in the code carries an `#[expect(..., reason = ...)]`.
- CI supply-chain hygiene: all actions SHA-pinned, `persist-credentials: false` on every checkout, `zizmor` workflow-auditing job.

**Claimed and contradicted / narrower than it sounds**
- Nothing contradicted. One narrowing: `AGENTS.md` and `CLAUDE.md` say `cargo test` and the integration suite are the gates, but only the former runs in CI — the "on **both platforms**" suite is a human step.

## 4. Rubric scores

**1. Does what it says — 5/5.** Every README claim I could reach in code held, and the README materially undersells the tree (proxy, devcontainer translation, PAT wizard, image commit/restore are all absent from it).

**2. Quality of the interesting part — 4/5.** `coop-proxy` is a genuine security component, not glue: default-deny operation policy, fixed upstream, constant-time auth, sensitive-marked headers, permit-bearing response body, pinned roots with a *negative* test, and a jail whose self-test is itself tested for hollowness. The VM layer below it is orchestration over Firecracker/Lima and I did not read it closely enough to score it; the point is deducted for the allowlist at `proxy.rs:249` hardcoding two hosts and three exact paths — correct and fail-closed today, a standing maintenance obligation as the provider APIs move.

**3. Adoption cost — 3/5.** You inherit a hypervisor dependency (KVM+Firecracker, or Lima/Virtualization.framework), a built guest image, one long-lived host process per (VM, provider) holding a live API credential in memory, a loopback listener, writes into `~/.ssh/config`, an optional secret-store integration that shells out, and a self-updating binary. ~216 crates. Against that: removal is genuinely clean — `coop uninstall` with `--keep-data`/`--purge`, `coop destroy --all`, and the artifact is one binary plus `~/.coop`. The uninstall path even tolerates a corrupt config and warns that a custom `data_dir` may be missed (`src/lib.rs:977-989`).

**4. Failure modes — 3/5.** Where it would hurt:
- **Attestation downgrade.** `src/update.rs:565-575`: no `gh` on PATH → cryptographic verification is skipped and the install proceeds on checksum alone, logged at `info`. The message is honest ("the same assurance level as most `curl | bash` installers") but this is a self-replacing binary, and `info` is easy to miss.
- **Jail degrades silently by kernel.** On kernels 5.13–6.6 the Landlock network tier is dropped and proxy TCP egress is unrestricted (`jail.rs:24-28`); a `warn` is emitted. Even when enforced it is port-scoped, not host-scoped, and TCP-only — UDP/DNS ungated. The code says so plainly.
- **Shell strings for secrets.** `src/secret_store.rs` resolves credentials through `cmd:`-prefixed invocations executed via `sh -c`. There is a `shell_quote`/`shell_split` round-trip with tests, but the design puts a secret-fetching command line through a shell by construction.
- **The VM is the only boundary, by design.** Guest has passwordless sudo and agents run in bypass mode (`CLAUDE.md:38-46`). A Firecracker or Lima escape is a total compromise; there is no defense in depth inside the guest, deliberately.
- **Bus factor / concentration.** Single-org project; author count unverifiable here.

**5. Originality — 4/5.** The overall shape (agent-in-a-VM) is not novel. Two things in the execution are: the credential-injecting proxy with a *default-deny operation allowlist* — so even a proxy bug can't reach billing or admin APIs with the host key — and the self-verifying tiered jail. The process artifacts (trust model as a merge gate, closeout-review hook) are transferable independent of any of this code.

## 5. Ideas worth taking independently of the code

**Test that your sandbox self-test can fail.** `coop-proxy/src/jail.rs:280-286`:
> ```
> /// The probe must report failure when the process is *not* confined —
> /// otherwise a `=> PASS` from the integration self-test would be hollow.
> fn probe_fails_when_unconfined() {
> ```

**Tier a sandbox: hard floor plus best-effort above it, and report which tier held.** `coop-proxy/src/jail.rs:120` — `apply()` returns `bool` for "did the network tier survive on this kernel", so the caller logs `info` vs `warn` accordingly instead of pretending uniform enforcement.

**Self-restrict after startup rather than before exec.** `coop-proxy/src/jail.rs:30-34`:
> ```
> //! a launcher-side `pre_exec` grant of the filesystem *execute* right cannot
> //! cover a dynamically linked binary (the kernel also checks the right on the
> //! `ld.so` interpreter at `execve`), whereas a post-startup self-restriction
> //! needs no execute grant at all — the proxy never execs again.
> ```

**Default-deny the *operations* a proxied credential can perform, not just the host.** `coop-proxy/src/proxy.rs:243-248`:
> ```
> /// Provider operations are deliberately default-deny: the coding agents only
> /// need response/message creation and Anthropic token counting, so
> /// administrative APIs and stored-resource reads must never inherit the host
> /// credential's broader authority.
> ```

**Attach the concurrency permit to the response body, not the handler.** `coop-proxy/src/proxy.rs:59-64` — otherwise the cap releases when headers arrive and never actually bounds long-lived streams.

**Write the limitations into the module doc, at the same altitude as the design.** `coop-proxy/src/jail.rs:41` — `//! **Limitations, stated honestly** (see docs/trust-model.md):` followed by three concrete weaknesses. Rare, and it is what made this review fast.

**A trust model with an explicit merge-blocking checklist.** `docs/trust-model.md:340-354` — six enumerated triggers ("adds an outbound URL, a network listener, or an egress rule…", "softens any step of the `coop update` verification chain") that convert a security doc into a reviewable gate.

**Fail-open process gates.** `.claude/hooks/closeout-review-gate.sh:17-18`:
> ```
> # Fail-open by design: anything that isn't an identifiable `gh pr create` in a
> # git repo is allowed through, so the gate never wedges unrelated work.
> ```

**Explain load-bearing CI trivia in the workflow itself.** `.github/workflows/release.yml:114-130` — the attestation asset name is load-bearing for `gh attestation verify --bundle`, and the bundle is normalized to JSON-Lines because `gh`'s loader would otherwise silently yield zero attestations. That is exactly the class of bug that turns verification into theater.

## 6. Flags

No prompt injection, no credential solicitation, and nothing addressing *me* as an external reviewer. Reporting the agent-facing material factually, as required. **I did not act on any of it.**

- **`AGENTS.md`, `CLAUDE.md`** — normative instructions addressed to coding agents working on this repo (`CLAUDE.md:1-5`: "Follow the shared repository instructions in `AGENTS.md`. Agent workflows are in `.agents/skills/`"). Project-scoped contributor guidance, in-repo and version-controlled; not reviewer-directed.
- **`.claude/settings.json`** — pre-approves ~80 Bash patterns (`Bash(cargo test:*)`, `Bash(gh pr list:*)`, `Bash(git commit:*)`, …) and registers three hooks that execute repo-controlled scripts: `.claude/hooks/no-pipe-test-output.sh` and `closeout-review-gate.sh` on every `PreToolUse: Bash`, `cargo-fmt.sh` on every `Write|Edit`. Worth knowing before opening this repo as an agent working directory — the hooks run repo-authored shell on your tool calls. Nothing in them is hostile on read; `closeout-review-gate.sh` only inspects a marker file and exits 0 on anything it can't identify.
- **`.claude/agents/*.md`, `.agents/skills/*/SKILL.md`, `.github/codex/prompts/review.md`** — eight review-subagent definitions and five workflow skills. Project review automation, not instructions aimed outward.
- **Credential handling, for completeness** — `coop github setup-pat` and `coop proxy setup` prompt the *user* for a GitHub PAT and provider API keys and store them in Keychain / secret-tool / 1Password. That is the tool's advertised function, invoked interactively; nothing in the repo asks a reading agent for credentials.