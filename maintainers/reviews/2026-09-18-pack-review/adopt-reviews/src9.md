# Clean-Room Review: `deeplethe/utopia` (candidate `src9`)

## 1. Executive Summary

Utopia is a Rust monorepo (8 workspace crates + a React/TS frontend) implementing a "bitemporal knowledge graph" system: document ingest → LLM-driven entity/fact extraction → ontology-governed forward-chaining reasoning → conflict detection → a chat/agent layer over the graph, backed by a single Postgres instance. The code I read (rule engine, main.rs bootstrap, reasoning/materialization) is unusually careful: every non-obvious decision is commented with its rationale and cross-referenced to one of 45 numbered ADRs in `docs/decisions/`. Tests are extensive (111+ files in `utopia-store/tests` alone) and CI is structured specifically to prevent "tests exist but never ran" rot (a documented past incident, #248). License is a clean, unmodified Apache-2.0. The core reasoning/rule mechanism is genuinely sophisticated (interval-based validity, asserted-beats-derived semantics, capped combinatorics reported rather than silently dropped) — not glue code. **Caveat: this environment gave me no shell tool and the local `.git` is a depth-1 shallow clone containing only one commit**, so I could not run `git log` at all; cadence, author count, and bus-factor are therefore *unverifiable* here, not merely unfavorable. Adoption cost is real (Postgres + a Rust binary + LLM API dependency) but the security posture and failure-mode documentation (SECURITY.md, migration/role separation) are more thorough than most projects at this maturity level.

## 2. Maturity Signals

| Signal | Command | Result |
|---|---|---|
| Last commit date | `git log -1 --format=%ci` | **Could not run** — no shell tool available in this session; `.git/logs/HEAD` shows a single reflog entry: a shallow `clone` of `d993006281d81be8fe239890089a55f9d3026228` at Unix time `1789711184` (≈ 2026-09, consistent with "today"), authored `GFMCloud <Graham@GFMCloud.com>` — but that's the *clone* action, not a commit timestamp. |
| Commit cadence (last ~50) | `git log --format='%ci %an' \| head -50` | **Not verifiable**: `.git/shallow` lists exactly one commit hash, so the local repo has depth 1. No history to inspect. |
| Distinct authors, last 12 months | (same) | **Not verifiable**, same reason. LICENSE attributes copyright to "DeepLethe Contributors" (plural), and CONTRIBUTING.md describes a DCO-based external-contributor workflow with branch protection on both `main` and `dev`, implying more than one committer, but I cannot confirm headcount. |
| Dependency count / freshness | `Cargo.lock` grep for `^name =` | 611 crate entries. Notable deps: axum 0.8, sqlx 0.8, tantivy 0.26, oxrdf/oxttl (RDF), pgvector 0.4, jsonwebtoken 10, argon2 0.5, aes-gcm 0.10 — all current-generation major versions, not stale forks. Frontend (`web/package.json`): ~22 runtime + 10 dev deps (React 19, TanStack Query/Router, sigma.js for graph viz) — modest, not sprawling. |
| License file | `LICENSE` (read directly) | Apache-2.0, unmodified boilerplate, `Copyright 2026 DeepLethe Contributors`. Matches the badge in README. |
| Tests exist AND CI runs them | `.github/workflows/ci.yml`, `CONTRIBUTING.md` | **Verified, not just claimed.** Three CI jobs: `backend` (fmt/clippy -D warnings/test/build), `migrations` (spins up real Postgres, runs migrations twice for idempotency, then runs the DB-gated `utopia-store` test suite with `UTOPIA_TEST_REQUIRE_DB=1` so a missing DB *fails* rather than silently skips), and `web` (vitest + tsc build). CONTRIBUTING.md explicitly documents a prior incident (#248) where DB-tests silently skipped and showed false-green, and the CI/test-guard convention (`utopia_store::test_db::url()`) exists specifically to prevent recurrence. |
| Open issues (volume/health) | — | **Not checked** — no `.github/ISSUE_TEMPLATE`, and per instructions I did not fetch external URLs (GitHub issues page) since this is a read-only, no-network review. |

## 3. Claimed vs. Verified

**Claimed (README only, not independently checked by me):**
- "Full-text on Tantivy, vectors on pgvector, fused with RRF" — Tantivy and pgvector are real deps; I did not read the fusion code.
- "Ontology2SQL... state of the art on BIRD Mini-Dev" — external benchmark claim, unverifiable from this repo.
- MCP server, multi-source connectors (Jira/Notion/WebDAV/S3/GitHub), OIDC SSO — modules exist (`jira_issues.rs`, `github_issues.rs`, `notion.rs`, `webdav.rs`, `object_storage.rs`) per `main.rs`'s module list; I did not read their internals.
- Adoption/decision-ledger UX claims — plausible given `audit::record` calls I saw in `main.rs`, not fully traced end-to-end.

**Verified (I read the code/log directly):**
- Rule/reasoning engine implements interval-based (bitemporal) validity, asserted-fact-beats-derived-fact conflict resolution, fixpoint iteration with a documented convergence strategy, and capped-combinatorics reporting rather than silent truncation (`utopia-reason/src/rules.rs`, `utopia-store/src/reasoning.rs`).
- Secrets are AES-256-GCM sealed at rest with the key kept out of the database (`utopia-core/src/secrets.rs`, exercised in `main.rs`).
- CI actually runs DB-backed tests and fails (not skips) without a database.
- Migration/runtime DB-role separation is implemented, not just described (`main.rs` lines ~100–116).
- Release pipeline does an actual container smoke test (boot, migrate, register a user, check `/api/v1/health`) before pushing to `ghcr.io`, not just a build.
- License is genuine, unmodified Apache-2.0.

## 4. Rubric

1. **Does what it says: 4/5** — Every piece of the "interesting" code I read (reasoning engine, main.rs bootstrap, CI) matched or exceeded what the README described; I couldn't verify the long tail of connector/SSO/Ontology2SQL claims.
2. **Quality of the interesting part: 5/5** — The rule/derivation engine is a real forward-chaining reasoner with correct interval-intersection semantics, deliberate premise tracking, and 15+ targeted unit tests per edge case (missing-reading ≠ zero, OR-groups, combinatorial capping reported not dropped). This is not glue around an LLM call.
3. **Adoption cost: 3/5** — Requires Docker + Postgres+pgvector + an OpenAI-compatible LLM endpoint; single-binary deployment is a plus. Removal path is clean (it's your data in Postgres + files), but the schema "only rolls forward, no rollback" (README, "Status" section) means downgrading is not supported — a real, honestly-disclosed lock-in point.
4. **Failure modes: 4/5** — Unusually candid: SECURITY.md lists known unresolved limits rather than hiding them; default DB password and its exposure risk are called out explicitly; migration role separation limits blast radius of app-level bugs/SQLi. Main risk is v0.1 status generally (schema churn) and heavy reliance on an external LLM endpoint for extraction quality.
5. **Originality: 4/5** — Treating an ontology as a first-class, editable governance object with reified edges, bitemporal validity, and human-in-the-loop conflict resolution (rather than bolting reasoning onto a generic property graph) is a genuinely distinct architectural choice worth studying even independent of this codebase.

## 5. Ideas Worth Taking (independent of the code)

- **"A derived fact is second-class to an asserted one, but never silently invisible"** — the conflict-resolution rule that an asserted fact always wins over a derived one, while still recording *why* the derivation was blocked, from `crates/utopia-store/src/reasoning.rs:1701-1717` (comment: `asserted > derived 是硬性的（0002）...认可与否只影响报不报（0017）`).
- **Capacity limits that report, don't silently truncate** — `MAX_COMBOS`/`report.capped` pattern in `crates/utopia-reason/src/rules.rs:240-250,341-346`, with the accompanying test `too_many_combinations_are_reported`, encoding the principle "少推几条与「这个实体不满足」在结果里长得一模一样" (under-deriving must be distinguishable from correctly not-matching).
- **CI job specifically designed to catch "tests exist but never ran"** — `.github/workflows/ci.yml:71-76`, comment explaining that DB-gated tests skip green in the `backend` job and only truly execute in `migrations`, with `UTOPIA_TEST_REQUIRE_DB=1` turning "no database" into a hard failure rather than a skip.
- **Explaining a specific, previously-reported user error directly in application logs** — `crates/utopia-server/src/main.rs:75-87` (`explain_db_error`), which detects a password-auth failure and prints the exact remediation command, motivated by comment `#456`.

## 6. Flags

None. I searched for text addressing the reviewing agent, requesting instruction changes, or requesting credentials (`grep -i` over the whole tree for prompt-injection-style phrasing). All hits were legitimate code/data — e.g. `system prompt` in `crates/utopia-server/src/api/chat.rs` is the application's own LLM system-prompt construction, and `ai-timeline*.json` are benchmark fixture files (AI-history dataset used for entity-resolution testing), not addressed to me. No secrets, tokens, or credential requests found in `.env.example` (placeholders only) or elsewhere.
