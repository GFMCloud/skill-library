# Decisions: ai-native-sdlc-playbook

contract: v1
source: https://claude.com/blog/the-ai-native-sdlc-playbook
type: article
pin: fetched 2026-09-02T17:17:39Z, sha256 adfcd44e65105377bc05c3577a0193bb4f8bc1b77e3597e7ff4852b0ce1a213f (article body only, nav chrome stripped; 1123 lines)
reviewed: 2026-09-02
verdict: HARVEST
recheck: 2026-12-01 (row 9 only, WATCH)
evidence: scratchpad/cleanroom-review.md, scratchpad/comparison.md (both copied into the review record's commit as docs/reviews/2026-09-02-ai-native-sdlc-playbook/)

## Verdict reasoning

The article's core ideas (executed evidence, files as the bridge between sessions,
boundaries enforced at the tool layer, no approval prompts mid-run, one source of
truth, intent before execution) are already rules in `~/.claude/CLAUDE.md` or
bodies in this library, and in every case the incumbent carries the originating
failure, which the article never does. What survives is six fragments where a rule
this machine already holds has no procedure or no tool-layer enforcement behind
it. Five are one-paragraph edits; the rest change installed behavior outside the
library and are Graham's call. The verdict would move to SKIP only if the fragment
rows were rejected wholesale; it cannot reach ADOPT because the article is prose,
not an installable unit, and its runnable snippets are defective as written.

## Ancestry

none. Grep over the library and the global CLAUDE.md finds no reference to the
article, its author, or its artifact names; the library's matching rules predate
the article (consolidated 2026-08-12, article dated 2026-08-21). Convergent, not
inherited.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour, one sitting | `M` an afternoon, one PR | `L`
multi-session, or a merge under the 500-line body cap with more than a handful
of edits; L always goes through `phased-harness`.
Adoption cost is mandatory and never "none": what this adds to the maintenance
surface and how it gets backed out.

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Cap low-severity findings; skip what CI already enforces and generated paths | INGESTIBLE FRAGMENT | One paragraph after "Don't pad" in Phase 2 | article L717, L739, L742 | `plugins/workbench/skills/fable-project-review/SKILL.md` | S | One more rule the plan template must stay consistent with; back out by reverting the paragraph | ratified (default) | this session |
| 2 | Test that a skill triggers before promoting it (three phrasings, fresh session) | INGESTIBLE FRAGMENT | One paragraph at the end of "The description is the router" | article L431 | `docs/authoring-standard.md` | S | A manual promotion step the validator cannot check; back out by reverting | ratified (default) | this session |
| 3 | Evals run on any change to a skill, its hooks, or its CLAUDE.md, and gate the merge | INGESTIBLE FRAGMENT | One bullet in "Change hygiene", phrased to bind from the first eval case | article L645, L646 | `docs/authoring-standard.md` | S | A rule ahead of its mechanism: the library has zero eval cases today, so this is drift unless evals follow; back out by reverting | ratified (default) | this session |
| 4 | Behavioral regression routes to an eval case, not prose | INGESTIBLE FRAGMENT | One row in the §3 routing table | article L647 | `plugins/workbench/skills/retro/SKILL.md` | S | A routing destination no skill has yet; retro only proposes; back out by deleting the row | ratified (default) | this session |
| 5 | Bug fix: reproducing test first, seen to fail, committed, frozen during the fix | INGESTIBLE FRAGMENT | Extend hard rule 6 in the generated CLAUDE.md; matching sentence under SPEC.md §6 | article L577, L580 | `plugins/workbench/skills/new-project/scripts/scaffold.sh` (plus `references/conventions.md`, its doc) | S | Generator and its doc must stay in sync; only new projects receive it; back out by reverting both | ratified (default) | this session |
| 6 | PreToolUse hook that blocks Edit/Write on `tests/**` while a fix task is flagged | INGESTIBLE FRAGMENT | Write fresh for the python archetype; prove by deliberate failure before it ships | article L580 (mechanism named, no script given) | `plugins/workbench/skills/new-project/scripts/scaffold.sh` (python archetype `.claude/settings.json`) | M | A shell script in every new Python repo plus a "fix task" marker convention; false blocks on legitimate test edits; back out by removing it from the archetype | proposed (question 1) | Graham |
| 7 | Deny reads of credential files at the permission layer | INGESTIBLE FRAGMENT | `permissions.deny` for `.env` (not `.env.example`), `./secrets/**`, `~/.ssh/**`, `~/.aws/credentials`; `sandbox.credentials` only after key names are verified current | article L829 to L832, L846 to L851, L873 | `~/.claude/settings.json` (outside the library; `~/.claude` is git-versioned locally) | S | Every session loses the ability to read those paths, so a wrong pattern blocks legitimate reads; back out by removing the entries | ratified by Graham 2026-09-02; applied by paste (classifier blocks permission-content edits from the session) | Graham |
| 8 | Explanatory Bash gate hook on pushes and production writes (exit 2 with reason and route) | INGESTIBLE FRAGMENT | Pattern only, never the article's script; recommend OUT: the permission prompt is already the gate on a solo laptop | article L782, L811 | `~/.claude/settings.json` | M | A hook on every Bash call: latency plus false blocks, and substring matching is the article's own defect; back out by removing the hook | out (Graham 2026-09-02, on recommendation) | |
| 9 | Autonomy tiered by statistical deviation band, deterministic detector, tier bound to a tool allowlist | COMPLEMENT | WATCH; if a project gains a metric with a rolling baseline, land as a second trigger type in pipeline-foundry §8, minus the 3σ pre-approved-runbook route (conflicts with the never-pre-authorizable set) | article L984, L985, L998 to L1003 | `plugins/workbench/skills/pipeline-foundry/SKILL.md` | L | Nothing on this machine consumes it today; the σ-to-tier mapping has no derivation | ratified as WATCH, recheck 2026-12-01 | this session |
| 10 | Two-strike rule for CLAUDE.md corrections | REDUNDANT | Global "CLAUDE.md economy" rule plus `retro` (transcript-grounded, routed by type) | article L370, L720 | none | S | n/a | out | |
| 11 | Advisory skill vs deterministic hook | REDUNDANT | Global "Boundaries are declared and enforced"; `pipeline-foundry` §4 verified instance | article L461 | none | S | n/a | out | |
| 12 | Plan-quality bar and interrogation prompts | REDUNDANT | `fable-project-review` plan template, `phased-harness`, `pipeline-foundry`; `anthropic-skills:plan-gate` | article L285, L286 | none | S | n/a | out | |
| 13 | Rehearse rollback | REDUNDANT | `deploy-verify-fix` ("A rollback first attempted during an incident is not a rollback plan") | article L920 | none | S | n/a | out | |
| 14 | One source of truth per artifact | REDUNDANT | Global duplication rule; article's "linkage, two sources of truth" contradicts it | article L341, L347 | none | S | n/a | out | |
| 15 | Approval prompts out of the build phase | REDUNDANT | `phased-harness` doctrine, `standing-authorization`, global standing defaults | article L485 | none | S | n/a | out | |
| 16 | "Done" means verified, in writing | REDUNDANT | Global evidence-over-assertion, `proof-of-work`, `evidence-report` | article L591, L592 | none | S | n/a | out | |
| 17 | Committed-artifact chain intent/spec/plan | REDUNDANT | `phased-harness`, `new-project` four docs, `pipeline-foundry` scaffold; note `spec.md` vs `SPEC.md` collision | article L95, L115 | none | S | n/a | out | |
| 18 | Verifier subagent, report only | REDUNDANT | `verification-kit:pre-delivery-verifier` enforces report-only at the tool layer | article L520 to L529 | none | S | n/a | out | |
| 19 | Parallel sessions in worktrees plus subagents | REDUNDANT | Global concurrency section, `sweep-harness` doctrine | article L513, L516 | none | S | n/a | out | |
| 20 | The CLAUDE.md play | REDUNDANT | Global economy rule, `conventions.md` hard-rules-with-reasons (stronger form) | article L367 to L371 | none | S | n/a | out | |
| 21 | Plan mode default, commit plan.md | REDUNDANT | `new-project` plan-gate pointer, `fable-project-review` verify mode | article L265, L287 | none | S | n/a | out | |
| 22 | Feedback-loop mechanics | REDUNDANT | `deploy-verify-fix` table, `capability-preflight`, SPEC.md §6 | article L574 to L578 | none | S | n/a | out | |
| 23 | CI/CD adoption order, MCP deploy allowlist | REDUNDANT | `deploy-verify-fix`; no MCP deploy consumer here | article L915 to L919 | none | S | n/a | out | |
| 24 | Auto mode conditions | REDUNDANT | Global standing defaults, `standing-authorization` ceilings | article L329 | none | S | n/a | out | |
| 25 | Intent capture in the originator's words | REDUNDANT | Global "Intent before execution" with its audit | article L141 | none | S | n/a | out | |
| 26 | Measurement definitions from git and PR metadata | DISCARD | No baseline; depend on artifacts no project here produces | article §"How to measure it" | none | S | n/a | out | |
| 27 | Claude Security scheduled scans | DISCARD | Enterprise beta, no entitlement, gitleaks covers secrets | article L1031 to L1051 | none | S | n/a | out | |
| 28 | Claude Tag on-call | DISCARD | Slack-only beta, no channel; the lessons file is `retro` | article L1075 to L1080 | none | S | n/a | out | |
| 29 | Dependency graph, "start with any clay play" | DISCARD | Self-contradicting prerequisites | article L147, L161, L226, L231 | none | S | n/a | out | |

## Conflicts for the user to rule on

1. **Row 6, test-file freeze hook.** Article: "an agent fixing code must not be able to weaken the check on that code. A hook that blocks edits to test files during a fix task does this." Incumbent: rule 6 says "Do not relax an assertion to make a change pass" as prose only. Proposal: build the hook into the python archetype, M effort, gated runbook. Alternative: leave row 5's prose as the control. Reasoning: this is the one row that turns a prose rule into a tool-layer one, which the global file prefers, but it costs a marker convention and will false-block sometimes.
2. **Row 7, credential-file denies.** Article: "`permissions.deny` keeps secrets out of the agent's context". Incumbent: "Never handle raw credentials: not reading them" with no deny list in `settings.json` (checked live: `permissions` holds only `defaultMode`). Proposal: add the deny entries. Alternative: keep prose only. Reasoning: closes a gap between a rule loaded into every session and zero enforcement, but it lives outside the library and any wrong pattern blocks legitimate reads.
3. **Row 8, Bash gate hook.** Article: "A block should explain itself". Incumbent: the permission prompt on `git push` is already the gate. Proposal: out. Alternative: a hook limited to `--force`, deletes of tracked paths, and `terraform apply`. Reasoning: on a solo laptop the prompt already stops the never-pre-authorizable set; the hook adds latency to every Bash call for little.

## Corrections at ingest

- No em dashes in any ingested text; the article has 18. All landed text was written fresh, not pasted.
- Every landed rule carries its reason inline, per `conventions.md`; the article attaches none.
- Row 3 is phrased to bind from the first eval case, because a gate that does not exist cannot be "trusted after deliberate failure".
- Row 5 must not say "all sessions read CLAUDE.md": `pipeline-foundry` §3 verified that Explore and Plan subagents do not.
- Row 7 must not use `Read(.env*)`: it also denies `.env.example`, which `scaffold.sh` writes. Key names for `sandbox.credentials` are unverified until the currency check returns.
- Never copy `production-gate.sh` (substring match, Bash-only matcher, spoofable env var) or `agent-evals.yml` (no timeout, no concurrency cap, `result.json` overwritten per loop).

## Flags

Untrusted-content findings, quoted with path, none acted on:

- `source/ai-native-sdlc-playbook.md` L446 to L456 (skill body): "When you create or change an API endpoint: 1. Authentication: every endpoint requires the gateway JWT ... Run scripts/check-endpoints.sh and include its output in your summary."
- L527 to L529 (subagent body): "Start the app with make run. Exercise the changed behavior and the two nearest neighboring flows ... Do not fix anything; report only."
- L591 to L592 (CLAUDE.md block): "Run all three before reporting any task complete, and paste the output. If a test fails, fix the code, not the test."
- L729 to L742 (REVIEW.md): "Run three passes and tag each finding with its pass ..."
- L407: "Put the skill in the repo at `.claude/skills/<name>/` so it ships with the code, or distribute it organization-wide through a plugin."
- L777: "Team hooks go in `.claude/settings.json` in git, and non-negotiable hooks go in managed settings owned by the platform or IT admin, where individual engineers cannot switch them off."
- L822: "Deployed by the platform team via MDM or the admin console; engineers cannot edit or override any of it." followed by a full managed-settings JSON block.
- L657: "npm install -g @anthropic-ai/claude-code" inside the CI workflow example.

All are inside fenced examples presented to the reader as templates. Commercial note: every outbound link resolves to an Anthropic property; outcome claims are uncited.

## Rulings log

- 2026-09-02, this session: rows 1 to 5 ratified by default and applied; row 9 ratified as WATCH; rows 10 to 29 out. Rows 6, 7, 8 proposed to Graham as questions 1 to 3; no side effects transfer until ruled.
- 2026-09-02, Graham ("run with the ones you feel strongly about"): row 7 ratified, `permissions.deny` only, sandbox block deferred to its own decision; the session's config-skill call was classifier-blocked, so the edit is routed as a paste and proven by deliberate failure after it lands. Row 8 out. Row 6 still open.
