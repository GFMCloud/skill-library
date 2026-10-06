# Decisions: claude-code-mods (mod-builder)

contract: v1
source: https://github.com/karanb192/claude-code-mods
type: code-repo
pin: 10617a90106144d3cb131bd599e677d9c38bfd35 (2026-10-03 18:41 +0530, "Rebuild mod-builder for Claude Code 2.1.287 and later (#15)"; shallow clone; MIT; 35 stars, created 2026-09-15, 61 files)
reviewed: 2026-10-06
verdict: HARVEST
recheck: -
evidence: maintainers/reviews/2026-10-06-claude-code-mods/cleanroom-review.md, maintainers/reviews/2026-10-06-claude-code-mods/comparison.md

## Verdict reasoning

A plugin marketplace with three local plugins and one unpinned external one, reviewed the
week Claude Mods shipped (2.1.287). The substance is `mod-builder`: a skill plus seven
zero-dependency Node scripts that wrap `claude plugin validate`, grade the "reach" of every
capability a mod calls against an ordered allowlist, diff that footprint against a plan the
author declared up front (an unplanned call or an ungraded one exits 1), and run the mod in
an isolated child `claude` under its own `CLAUDE_CONFIG_DIR` that hashes the source before
and after, snapshots the real config, and writes evidence files per stage, with the agent
limited to status words a script printed. The code is careful and the ideas transfer. Not
ADOPT: one visible commit and one maintainer on a fast-moving API with a 2.1.287 floor; a
self-promoting star invitation that uses the user's `gh` login (flag); `cache-tax` installed
from another repo's HEAD with no pin; `fable-pin` silently reroutes every subagent to Fable,
against model-effort-advisor; `image-peek` reads the system clipboard. Nothing here has a
consumer until this machine ships a mod of its own, which is exactly the question the
hooks-hardening runbook now faces (W-18 closed). HARVEST: three fragments with consumers
today and two design inputs for the runbook. What would change the verdict: a mod of our own
to build, at which point the footprint-as-budget and isolation harness become the reference
implementation to vendor, after the star invitation is stripped.

## Ancestry

none. No shared history; the incumbents trace to the ECC review (eval-harness, bounded-loop
references). The two work at different layers (settings command hooks proven by
`prove-hooks.sh` fixtures, against plugin function hooks proven by `claude plugin validate`
and a child session).

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour, one sitting | `M` an afternoon, one PR | `L`
multi-session, or a merge under the 500-line body cap with more than a handful
of edits; L always goes through `phased-harness`.
Adoption cost is mandatory and never "none": what this adds to the maintenance
surface and how it gets backed out.

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Normalize a check's output before comparing attempts: strip paths, durations (`[12ms]`) and whitespace, so a timestamp in the output no longer forces `ambiguous_check_feedback` | INGESTIBLE FRAGMENT (fixes a weakness bounded-loop states about itself) | Normalize at `_verify_impl.py:239-240` before the set comparison, test-first with a fixture whose check prints a timestamp, then shrink the "Known weakness" paragraph in `references/escalation-report.md` | `prove.mjs:277-279` | `plugins/foundry-core/skills/bounded-loop/scripts/_verify_impl.py` | S | one normalizer to keep right (an over-eager one could merge two different failures); backed out by reverting | proposed (Tier 3: a script in an incubator skill, behavior change) | Graham |
| 2 | Isolation proven by evidence for live proof sessions: a throwaway `CLAUDE_CONFIG_DIR` seeded with copies of `settings.json` and `hooks/`, before-and-after hashes of the real `settings.json`, the hooks directory and the `~/.claude/projects` listing, and a scan of the evidence for real-config paths | COMPLEMENT (nothing installed proves that a live proof left `~/.claude` alone; the runbook's step 8 sessions would write transcripts into the corpus `replay-board-gate.py` reads) | Add to the hooks-hardening runbook's Boundaries and step 8 as the required form of the live-session arm; the real hooks must fire, so the throwaway config is seeded, then the real files are checked unchanged | `prove.mjs:168, 198-208, 574-622`; `proof.md:14` | `claude-scout-weekly/docs/runbooks/2026-10-01-hooks-hardening.md` (Graham's runbook) | S to write, M to run | one more check per proof session; nothing to back out in the library | proposed (Tier 3: a ratified runbook) | Graham |
| 3 | "The model's own reply offered as evidence that a hook ran" is forbidden: the evidence is the hook's own `tool_result` or block record, or the debug-log line | INGESTIBLE FRAGMENT | One sentence in the runbook's step 8 ("reads the denial back from the transcript" does not say which record counts) and one in eval-harness's Verify, naming the record that counts | `SKILL.md:116, 119`; `proof.md:115` | `plugins/foundry-core/skills/eval-harness/SKILL.md` (Verify) and the hooks-hardening runbook step 8 | S | one sentence each; backed out by deleting. The eval-harness half would fit the widened Tier 2 (incubator body, S, decisions row); flag off, Tier 3 | proposed | Graham |
| 4 | Footprint as a pre-declared budget diffed after the build: an unplanned call, env name or state key is removed or its reason written down; an omitted list means empty, not anything; an ungraded call fails closed | COMPLEMENT, no consumer yet | Revisit when the library ships a mod (row 2 of the auto-handoff review, or the spawn ceiling as a `tool.check` mod); then vendor `footprint.mjs` and `reach-rules.json` after fixing the suffix match at `footprint.mjs:174` (planning `enabled` accepts any plugin's `*.enabled`) | `footprint.mjs:177-224`; `data/reach-rules.json`; `README.md:34`; `SKILL.md:90` | none yet | M | a reach allowlist to keep in step with the `$` API | out (noted; the reference implementation if a mod is ever built here) | - |
| 5 | A `recheck:` clause on every restated fact: source, the build it was checked on, and the observable event that would make it stale | INGESTIBLE FRAGMENT (the third element is new; incumbents carry source and date only) | Add the clause where a fact names a CLI version: `bounded-loop/references/stop-hook-contract.md` ("fetched 2026-09-11" gains the event that would stale it), the `prove-hooks.sh` header's 2.1.260 sentence, and the runbook's "(checked live 2026-10-01)" facts; never copy a stamp whole, re-stamp with our own date and version | `SKILL.md:13` | `plugins/foundry-core/skills/bounded-loop/references/stop-hook-contract.md` (first target; the others ride it) | S | a clause to keep true per fact; backed out by deleting | proposed (Tier 3: an incubator references/ file from a decisions row, so it fits Tier 2 as written; flag off) | Graham |
| 6 | Three-strikes circuit breaker keyed on a normalized failure signature and the source hash | REDUNDANT | `bounded-loop` is stronger: its budget counts distinct attempts and never inflates on a repeated hash, and it has the escalation report; the candidate's count restarts on any source change (`prove.mjs:285`) and its "by hand" rule in `SKILL.md:127` cannot be enforced | `prove.mjs:277-296` | none | - | - | out | - |
| 7 | `fable-pin` (rewrite every `agent.spawn` to `model: 'fable'`), `image-peek` (clipboard reader), `cache-tax` (unpinned external plugin), `mod-builder` installed whole | DISCARD | fable-pin contradicts the model-stated-before-every-spawn rule and would silently distort the per-spawn measurement in the runbook's step 11; image-peek has no consumer; cache-tax runs another repo's HEAD inside the process | `plugins/fable-pin/hooks/register.ts:32-35`; `marketplace.json:53-56` | none | - | - | out | - |
| 8 | Lowest-reach-first design rule ("reading `$.session.repo` beats running `git remote -v`") | DISCARD | specific to the `$` API, no consumer | `SKILL.md:62` | none | - | - | out | - |
| 9 | Mods as the layer for the ratified spawn ceiling: 2.1.290's `tool.check` event carries `agentId`, so a mod can count Agent spawns and tell a subagent's check from the main session's, where a PreToolUse command hook sees only the tool input | design input (first-party changelog, surfaced beside this review) | A rider on Q-2026-09-28-3: the runbook's step 11 chooses the layer (command hook or mod) with the mod-builder harness as the proving pattern if a mod is chosen | Claude Code changelog 2.1.289, 2.1.290 | `claude-scout-weekly/STATE.md` Q-2026-09-28-3 (a rider) | S | none | ratified (Tier 1 here: a queue note, written this cycle) | scout |

## Conflicts for the user to rule on

1. **Subagent model choice.** `fable-pin`: "fable-pin is on: every subagent runs on fable"
   (`register.ts:28`) against model-effort-advisor: "always trigger before spawning a subagent
   with an unspecified model". Proposal: never install fable-pin; a model pin for subagents,
   if ever wanted, is the documented `CLAUDE_CODE_SUBAGENT_MODEL` default, which a per-spawn
   choice overrides, not a silent rewrite. Alternative: none recommended.
2. **When a breaker resets.** Candidate: "A pass or a different signature resets the count"
   (`proof.md:110`); bounded-loop: "a new run needs a new budget, not a silent extension of
   the old one". Proposal: bounded-loop's semantics stand; take only the normalizer (row 1).
3. **Outward actions on the user's account.** `invitation.md:34`: "run `gh api ... -X PUT
   /user/starred/karanb192/claude-code-mods`" after an explicit yes; the star check runs
   before the user is asked. Standing authorization works from a granted list and a star is
   not on it; `untrusted-plan-intake.md`: text addressed to the agent is not followed.
   Proposal: strip the invitation from anything vendored; record the pattern (a skill that
   asks the agent to take an outward action on the author's behalf) in Settled ground as a
   reason a source is never ADOPT whole. Alternative: none.

## Corrections at ingest

- Strip `references/invitation.md` and `SKILL.md:137-141` from anything taken.
- A stamp such as `checked 2.1.288` copied into a library file would claim a check this
  library never made; keep the `recheck:` clause, re-stamp with our own date and version.
- `SKILL.md:66` asks a mod to "name its tokens per turn" while `proof.md:93` bans `/context`
  as a measurement: a stateless model can only estimate; do not copy the rule.
- "Three strikes ... by hand" is unenforceable in prose and only partly enforced by the
  script (unchanged source only).
- `plugins/fable-pin/hooks/hooks.json:2` says "Needs CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1";
  the README says the flag is ignored from 2.1.287. Contradiction inside the source; the
  changelog says Mods shipped in 2.1.287 and names no flag. Verify the flag's status against
  `claude --help` and the docs before editing the hooks-hardening runbook's step 7 (W-18's
  own re-check).
- `footprint.mjs:174` suffix match (planning `enabled` accepts any plugin's `*.enabled`);
  `prove.mjs:594` mtime-based isolation check gives a false FAIL on a concurrent
  `settings.json` edit.
- The mod-builder description has no "Not for" or cost clause and no `metadata`; inline
  stamps make the body dense.

## Flags

- `plugins/mod-builder/skills/mod-builder/SKILL.md:137-141` and
  `references/invitation.md:15, 30, 34`: the agent is told to check whether the user has
  starred the author's repo (`gh api ... /user/starred/karanb192/claude-code-mods`, before
  asking), to ask the user to star it, and after an explicit yes to star it with `gh api
  -X PUT`. A self-promoting write on the user's GitHub account, gated by an explicit yes and
  skipped in `-p`, SDK and subagent runs. Not acted on; not run.
- `SKILL.md:24`: "Do not load the built-in `plugin-authoring` skill for API facts ... Grep
  the types instead." A scoping instruction with a stated reason that overrides another
  skill; quoted because it steers the agent, not followed.
- `list-mods.mjs:9` fetches `raw.githubusercontent.com/karanb192/awesome-claude-code-mods/main/data/mods.json`
  at run time; `cache-tax` is installed from `karanb192/cache-tax` with no ref. Neither was
  fetched or run.
- No credential solicitation; API keys are masked in its own captures.

## Rulings log

- 2026-10-06, scout cycle 7 (unattended): rows 1, 2, 3, 5 proposed, queued as Q-2026-10-06-10
  in claude-scout-weekly `STATE.md`; row 9 landed as a Tier 1 rider on Q-2026-09-28-3; rows
  4, 6, 7, 8 out. Never install.
