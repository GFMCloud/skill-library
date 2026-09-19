# Comparison: `coop` (Trail of Bits) vs. installed set

Pin: `cbfe0273ac68585f381bcd9edf22384cac2cefce`. Read in full: the clean-room review, all four incumbent CLAUDE.md sections named, the hooks-and-permissions runbook, the STATE.md pending-queue row, and source-intake Step 2. Read directly from the candidate to verify: `docs/trust-model.md`, `coop-proxy/src/jail.rs`, `coop-proxy/src/proxy.rs` (relevant ranges), `CLAUDE.md`, `AGENTS.md`, `.claude/settings.json`, `.claude/hooks/closeout-review-gate.sh`, `.claude/skills/closeout-review/SKILL.md`, `.claude/commands/my-review.md`, and `src/secret_store.rs` (partial), plus `~/skill-library/docs/inventory.md` in full to check for a consuming skill.

## Spot-checks of the clean-room review

Verified directly against the files (all held):
- `proxy.rs:249-262` — `operation_allowed` matches exactly `POST /v1/responses` and `POST /v1/messages{,/count_tokens}`. Confirmed.
- `proxy.rs:65-88` — `GuardedBody` holds `_permit: OwnedSemaphorePermit` for the life of the body. Confirmed.
- `jail.rs:120-202` — tiered Landlock, hard `bail!` at line 147-154 if the v1 floor isn't `FullyEnforced`. Confirmed.
- `jail.rs:280-286` — `probe_fails_when_unconfined` test exists and asserts `probe(false).is_err()`. Confirmed.
- `closeout-review-gate.sh:17-18` — "Fail-open by design" comment quoted verbatim, text matches. Confirmed.
- `docs/trust-model.md:340-354` — stop-and-confirm checklist has exactly six enumerated triggers. Confirmed.
- `CLAUDE.md:1-5` (review cites it as such) — actually the quoted line is `CLAUDE.md` line 1, "Follow the shared repository instructions in AGENTS.md...". Close enough; trivial mislabel, not a substantive error.

Not independently confirmed: the `secret_store.rs` claim that `cmd:` retrieval goes through `sh -c` with a tested `shell_quote`/`shell_split` round-trip — I only read the first 80 lines (backend enum and detection), which corroborate the indirection but not the `sh -c` call site itself. Treat that one sub-claim as plausible-but-unverified by me.

## Ancestry

No shared history. Grepped the full candidate tree for `skill-library`, `GFMCloud`, `scout-weekly`, `improvements-weekly`, and `graham` — zero matches. `coop` is a Trail of Bits security-engineering repo with no awareness of this machine's maintenance harnesses, and vice versa. Every classification below is a genuine independent-convergence-or-gap comparison, not "who forked whom since when."

One structural convergence worth flagging up front, though: `coop`'s `.claude/skills/closeout-review/SKILL.md` is a five-line pointer file:
> "Read [`.agents/skills/closeout-review/SKILL.md`](../../../.agents/skills/closeout-review/SKILL.md) in full and follow it. The shared skill is the source of truth."

That is exactly the "one editable home, pointer shim" pattern already stated in `~/.claude/CLAUDE.md` under Duplication and reversibility: "Every rule, skill, and document has exactly one editable home. Mirrors, plugin caches, and generated copies are read-only." Independent arrival at the same convention, not something to harvest — it confirms the incumbent rule rather than improving it.

## Classification

Working from the clean-room review's Section 5 ("Ideas worth taking independently of the code"), each against the named incumbents.

### 1. "Test that your sandbox self-test can fail" (`jail.rs:280-286`) — REDUNDANT

Coop:
> "The probe must report failure when the process is *not* confined — otherwise a `=> PASS` from the integration self-test would be hollow."

Incumbent, `~/.claude/CLAUDE.md`, Boundaries are declared and enforced:
> "A gate or validator is trusted only after being proven by deliberate failure; a check that has never failed a fixture is untested."

And the runbook, `2026-09-03-hooks-and-permissions.md` line 3: "Every hook is proven by deliberate failure before it is trusted: feed it the payload it exists to refuse and a payload it must allow, and record both verdicts." STATE.md's hstack row 1 has already turned this into a standing artifact: `scripts/prove-hooks.sh`, a positive-and-negative-control script wired into the Thursday maintainer's Phase 0. The incumbent is equal in principle and ahead in execution — it already generalizes past one sandbox test to every gate on the machine, and it's already been ruled into a script. Nothing to take.

### 2. Tiered enforcement with reported degradation (`jail.rs:120`, `apply() -> bool`) — COMPLEMENT

No incumbent addresses graduated enforcement. The runbook's destructive-command hook (Step 1) and dash-gate (Step 2) are both binary: a command either matches a bad pattern or it doesn't. Coop's pattern — enforce a hard floor unconditionally, degrade a secondary tier by host capability, and have the caller `log("warn")` vs `log("info")` based on which tier actually held — has no analog here.

The gap is directly relevant to a named open item: STATE.md's `Q-2026-09-03-4` ruling says "An OS sandbox for the scheduled task is a bigger decision; note it as the alternative" — i.e., this machine has already flagged that the two weekly maintainers should eventually run inside a real OS sandbox rather than relying only on tool-stripping (`--restricted`, no-Bash spawns). Coop's tiered-Landlock/Seatbelt design is a working reference implementation of exactly that alternative, including the "report which tier held" idea, which the current tool-layer approach (binary: restricted or not) doesn't have room for.

### 3. Self-restrict after startup rather than before exec (`jail.rs:30-34`) — COMPLEMENT

> "a launcher-side `pre_exec` grant of the filesystem *execute* right cannot cover a dynamically linked binary (the kernel also checks the right on the `ld.so` interpreter at `execve`), whereas a post-startup self-restriction needs no execute grant at all — the proxy never execs again."

This is a specific, non-obvious Landlock mechanism fact, not a policy statement, so it has no CLAUDE.md counterpart. But it is squarely inside the same still-open decision as #2: if `Q-2026-09-03-4`'s OS-sandbox alternative is ever built for the scheduled maintainers (both of which spawn subprocesses via `claude -p`), this exact self-restriction-after-startup-vs-before-exec tradeoff is what an implementer would need to get right. Worth keeping as reference material for whoever picks that decision up, not worth acting on now.

### 4. Default-deny the *operations*, not just the host (`proxy.rs:243-248`) — COMPLEMENT, with a philosophy note

> "Provider operations are deliberately default-deny: the coding agents only need response/message creation and Anthropic token counting, so administrative APIs and stored-resource reads must never inherit the host credential's broader authority."

No incumbent states this as a design principle for anything resembling a gateway or proxy. The closest analog already in practice (not in prose) is `coop`'s own `.claude/settings.json` allow-list — `"Bash(cargo test:*)"`, `"Bash(gh pr view:*)"`, etc. — which is the same default-deny-by-operation shape, and Graham's own settings presumably work the same way. But there is no *named* rule anywhere in the incumbent set generalizing "when you build a thing that relays a credential, allow-list the exact operations, not the host" — it's practiced ad hoc, not written down.

This is worth flagging against the runbook's destructive-command hook (Step 1), which is the opposite polarity: a **denylist** of known-bad patterns ("`rm -rf` outside the scratchpad, `git push --force`, ..."), explicitly justified as "A wrong pattern blocks real work until edited; that is the accepted cost." That's a reasonable choice for arbitrary Bash (you can't enumerate all safe commands), but it is a different security posture than coop's allow-list, and the runbook doesn't discuss the tradeoff — it just picks denylist without comparing. Not a strict substitute (the domains differ: fixed HTTP API surface vs. arbitrary shell), but worth a sentence in the runbook acknowledging the choice was made, and why an allow-list wasn't viable there.

### 5. Concurrency permit attached to the response body, not the handler (`proxy.rs:59-64`) — DISCARD

Sound Rust/async correctness technique (a semaphore permit must outlive the streaming body or the cap is fictional), but nothing on this machine builds a streaming HTTP proxy — no incumbent, no consumer, no gap this fills. Good code, no home here.

### 6. Limitations documented at the same altitude as the design (`jail.rs:41` style) — INGESTIBLE FRAGMENT

> "**Limitations, stated honestly** (see docs/trust-model.md): ..." followed by three concrete weaknesses, inline in the module doc next to the design rationale, not in a separate "known issues" appendix.

None of the four incumbent CLAUDE.md files or the runbook state this as an authoring convention, though STATE.md's `Q-2026-09-03-16` (hstack review) references "the authoring standard" getting "one sentence each" for two other findings — meaning the library has a place for exactly this kind of rule and is actively adding to it this cycle. This fragment is a good candidate for that same authoring-standard document (not read directly here, so I can't confirm it isn't already covered — flag as a candidate row, not a confirmed gap).

### 7. Trust model with an explicit stop-and-confirm checklist (`trust-model.md:340-354`) — SUPERIOR SUBSTITUTE (as a pattern, not a direct swap)

Coop:
> Stop and get explicit human confirmation before merging a change that: "adds an outbound URL, a network listener, or an egress/`FORWARD`/NAT rule — name the boundary it crosses and what authenticates it；" "runs a host subprocess on tainted (guest- or fetch-derived) bytes — no shell strings; use `Cmd::arg`/`RemoteCommand::arg`;" ... (six total, each tied to an exact code pattern).

Incumbent, `~/.claude/CLAUDE.md`, Boundaries are declared and enforced:
> "Standing escalation triggers in any project: irreversible actions or state changes of a different authority class than the work in flight; audited facts, which are never adjusted to make a narrative fit; touching credentials or production; anything that changes project intent."

Both are the same genre — an enumerated, project-facing escalation list — but coop's is concrete and mechanically checkable (each trigger names the actual function/pattern that would trip it: `Cmd::arg` vs. shell strings, `0.0.0.0` vs. loopback binds), while the global rule is deliberately abstract because it has to cover every project on the machine. The global list is right to stay abstract (per CLAUDE.md economy: "every line loads into every session"), but it is missing the pattern coop demonstrates: a *project-specific* trust-model doc that instantiates the global escalation categories into exact, greppable code idioms for that codebase. Nothing here is a wholesale replacement — the edit needed is to lift the *pattern* (a per-project stop-and-confirm doc anchored to real function names) into guidance for when a project is security-sensitive enough to warrant one, likely a candidate row for `phased-harness` or the source-intake authoring guidance rather than a change to the global file itself.

### 8. Fail-open process gates (`closeout-review-gate.sh:17-18`) — INGESTIBLE FRAGMENT

> "Fail-open by design: anything that isn't an identifiable `gh pr create` in a git repo is allowed through, so the gate never wedges unrelated work."

The destructive-command hook design in the runbook implicitly follows the same shape (it matches only known-bad patterns and lets everything else through, so it never blocks unrelated work by construction) but the runbook never states the principle explicitly — it only shows the mechanism. Coop's one-sentence articulation is crisper and worth quoting into the hooks-and-permissions runbook or a future hook-authoring note, as the named justification for why a hook that can't positively identify its target case should default to allow, not deny.

## Routing collisions

None found, and the framing mostly doesn't apply here: `coop` is a target codebase being reviewed, not a plugin being installed side-by-side into `~/skill-library`. Its skill-shaped artifacts (`.claude/skills/closeout-review`, `.claude/skills/mutation-check`, `.agents/skills/{babysit-my-prs,babysit-pr,closeout-review,integration,mutation-check,review}`) are project-local — they load only when Claude Code's working directory is inside this repo, and none of their names (`closeout-review`, `mutation-check`, `integration`, `review`, `babysit-pr`, `babysit-my-prs`) collide with anything in `~/skill-library/docs/inventory.md` (checked the full inventory — no match). If Graham ever works in this repo, his global `~/.claude/CLAUDE.md` and coop's project `CLAUDE.md`/`AGENTS.md` apply simultaneously (Claude Code merges project + global), and I found no contradiction between them worth flagging as a collision — coop's rules are a strict specialization (VM/taint boundaries, Rust style) layered on top, not a conflicting restatement of anything global.

The one soft risk: coop's skill named `review` is generic enough that a future skill-library addition with the same name (there isn't one today) would collide, and the session's own system prompt already carries a distinct `/code-review` / `ultrareview` concept — worth remembering that "review" as a bare skill name is contested territory if this repo and skill-library skills are ever loaded in the same session (they currently can't be, since coop's are project-scoped).

## Philosophy conflicts

One real disagreement, not just emphasis: **allow-list vs. deny-list for guarding an action surface.** Coop's credential proxy is default-deny by operation (Section 4 above). The runbook's destructive-command hook is default-allow, deny by known-bad pattern, explicitly trading completeness for usability ("A wrong pattern blocks real work until edited; that is the accepted cost"). Both are defensible for their respective domains (fixed API surface vs. arbitrary shell), but they are opposite security postures and the runbook doesn't acknowledge the alternative was considered. Not a contradiction to resolve — a gap to note in the runbook per the source-intake contract ("Contradictions are reported, not resolved").

No other genuine contradictions found — the rest of the overlap (deliberate-failure testing, fail-open gates, one-editable-home) is agreement, not conflict.

## Corrections needed at ingest

- None of the eight Section-5 ideas or the trust-model/gate fragments carry factual errors as written — they're accurate to the code (per the spot-checks above).
- Style: coop's prose uses standard hyphens/dashes in code comments (`—` appears in the trust-model doc and module docs, e.g. `jail.rs:1`: "coop-proxy holds the real upstream credential and terminates connections originated by the untrusted guest, so it is the feature's new attack surface." — that em dash would need stripping per the no-em-dash rule before any of this text is quoted verbatim into a CLAUDE.md, runbook, or authoring-standard file).
- Anything landed from here needs the "rewriting a load-bearing claim triggers a sweep" treatment if it touches the global escalation-trigger list (Section 7) — that list is quoted/restated in project files per the consolidation note at the top of the global CLAUDE.md, so touching it isn't a one-file edit.
- Nothing here is stateless-model-unenforceable — every fragment worth taking is either a documentation convention (fine) or tied to a concrete future decision (the OS-sandbox alternative) rather than an ambient behavioral rule a model would have to remember unaided.

## Net assessment

If only three things could be taken:

1. **The tiered-enforcement-with-reported-degradation pattern** (`jail.rs:120-202`, `apply() -> bool`), as reference material attached to `STATE.md`'s `Q-2026-09-03-4` row — not a file edit today, but the row's "OS sandbox... later decision" note should point at this pin as a worked example when that decision gets picked up. Form: a pointer/citation in STATE.md, not ingested prose.
2. **The fail-open-by-design one-liner** (`closeout-review-gate.sh:17-18`), as a fragment added to `docs/runbooks/2026-09-03-hooks-and-permissions.md` — the runbook's hooks already behave this way; this sentence is the missing explicit justification, worth one line in Step 1 or Step 2's rationale.
3. **The allow-list-vs-denylist philosophy note** (Section 4/Philosophy conflicts above), as a sentence appended to the same runbook's Step 1, acknowledging that the destructive-command hook deliberately chose denylist over coop's default-deny-by-operation posture, and why (arbitrary shell can't be enumerated; a fixed API surface can).

Everything else — the self-test-that-can-fail idea, the concurrency-permit pattern, the module-doc style convention — is either already covered as well or better (item 1: REDUNDANT), has no consumer on this machine today (item 5: DISCARD), or is a plausible but unconfirmed candidate for a document I wasn't given (item 6, the authoring standard). `coop` itself is SKIP as an adoption target (it's a VM/proxy tool, not a skill or an article), consistent with source-intake's own framing: the code isn't wanted, three or four sentences from it are.