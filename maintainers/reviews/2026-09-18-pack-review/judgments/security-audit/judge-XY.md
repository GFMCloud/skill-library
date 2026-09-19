### Steelman X

item-fd563265 is a rigorous, evidence-driven audit workflow with genuine mechanical enforcement: two Node.js validator scripts (with their own test suites) that fail-closed on malformed findings or coverage-ledger data, reject symlinks/oversized input, and gate progression on a `PASS:`/exit-0 result rather than trusting the agent's self-report. It refuses to execute target-controlled code outside an OS-enforced sandbox and returns an explicit `needs_validation` blocker if that sandbox is unavailable. Every candidate finding must survive an independent "fresh-eyes" verifier instructed to try to refute it from source, and explicit validation rules reject speculative findings ("prompt injection alone is not a finding"). It defaults to a non-destructive "guidance mode," gates the heavy workflow and any file writes behind an explicit request plus a budget check, and requires disclosure of unresolved or out-of-scope work rather than allowing a silent "done."

### Steelman Y

item-ed2aee87 is a lean, dependency-free, on-demand checklist that fits the common case — reviewing a diff or answering "is this safe to deploy" — without any runtime, service, or install step. It hard-bars the agent from ever performing credential or account-level actions itself, forces a hard stop on any suspected live secret (reporting location, not value), and requires every PASS to name what was searched while every claim the agent can't verify from code is reported as NOT VERIFIABLE with the exact read-only check a human would run, rather than assumed. Its own operational footprint is zero state written; every state-changing action is deferred to an explicit per-action user confirmation. That makes it cheap to keep in a toolkit and low-risk to run frequently.

### Scores

| Criterion | X (item-fd563265) | Y (item-ed2aee87) |
|---|---|---|
| Fit with the bar | 3 — guidance mode withholds file creation/full workflow by default, budget gate precedes any agent launch, sandboxed re-execution and dual independent verification back "evidence before done," coverage ledger and `needs_validation` back disclosure (X.md lines 18-20). | 3 — proposed-actions list with per-action confirmation and a barred credential/account surface back "plan then stop," quoted-code-at-line + named-search-for-PASS back "evidence before done," mandatory "Not checked" line backs disclosure (Y.md lines 22-24). |
| Enforcement mechanism | 2 — two executable, fail-closed Node.js validators with test suites gate the findings/ledger artifacts, but the report is explicit that "nothing... enforces that the host agent actually invokes the validators" or runs the described sandbox/sub-agents (X.md line 14). | 0 — report states "Enforcement: Prose only... enforcement files: none" and explicitly calls it "fails open" with "no external mechanism" blocking a skipped step (Y.md line 15). |
| Context cost | 1 — full mode spans six phases and multiple companion files (HUNTING.md, VALIDATION-AND-REPORTING.md, AI-AND-LLM.md) with a "large library" of 13 domain-specific attack-class checklists, and the base skill loads on any broad security-related request (X.md lines 7, 12-13). | 3 — report states it loads "only the reference file(s) needed" and names just two reference files (`application-security.md`, `cloud-security.md`), with no runtime dependency (Y.md lines 17, 13). |
| Maintenance burden | 1 — requires `node` to run the validators/tests, assumes the host supplies an OS-enforced sandbox and a Task-tool-like sub-agent delegation mechanism, and the report flags an unresolved `gh` dependency listed but unreferenced in the files read (X.md line 15, 35). | 3 — report states "None named at the runtime level (no CLI, service, or install step is required by the skill itself)" (Y.md line 17). |
| Specificity | 3 — concrete coverage-ID canonicalization algorithm, per-verdict validation rules naming principal/boundary/observed-result, named failure modes ("a missing rate limit is not enough"), an eleven-step promotion procedure, and exact terminal states (X.md lines 13-14, 19). | 2 — concrete stop-gates, fixed output template, and named FAIL-before-PASS discipline, but the actual per-area checklist content lives in two unreviewed reference files, so the report evidences the framework more than the checklist substance (Y.md lines 13, 17). |

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-fd563265 | COMPLEMENT | Provides a deep, mechanically-verified, multi-agent full-codebase audit pipeline (fail-closed validators, independent re-verification, sandboxed execution) that item-ed2aee87's lightweight, enforcement-free checklist does not attempt. |
| item-ed2aee87 | COMPLEMENT | Provides a dependency-free, low-context, on-demand diff/PR-level check with a hard credential/account-action bar that item-fd563265's heavy, node-dependent, multi-file system is too costly to invoke for routine passes. |

### Deciding criteria

Enforcement mechanism and Context cost / Maintenance burden settled the rows: X wins on mechanical enforcement and specificity but carries real cost and runtime dependencies, Y is essentially free to keep loaded but has no executable enforcement — so each fills a gap the other's report shows it lacks rather than one replacing the other.

### What I could not assess from reading alone

Neither report lets me confirm behavior under actual use: whether X's coordinating agent reliably invokes its own validators and genuinely runs the described sandbox/sub-agent delegation (the report flags this as unverified from the files), and whether Y's prose-only stop-gates actually hold up against an agent under pressure to "just fix it," since Y's report explicitly says it "fails open" with no described fallback. A behavioral test would need to try to get each to skip its gate (X: bypass validator invocation or sandbox check; Y: get it to perform a barred credential action or mark PASS without a shown search) and see what actually stops it. I don't see grounds to identify either candidate's source, and didn't attempt to.
