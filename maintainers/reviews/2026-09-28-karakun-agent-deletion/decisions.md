# Decisions: karakun-agent-deletion

contract: v1
source: https://dev.karakun.com/2026/08/28/coding-agent-pushed-deletion-to-main.html
type: article
pin: fetched 2026-09-28, sha256 b535965045356645e25120c292bacb96765a2a633d0f59b06b117914f2ba78fe (3,389 words; published 2026-08-28, François Martin, Karakun; first sighting via HN 2026-09-25)
reviewed: 2026-09-28
verdict: HARVEST
recheck: -
evidence: maintainers/reviews/2026-09-28-karakun-agent-deletion/cleanroom-review.md, maintainers/reviews/2026-09-28-karakun-agent-deletion/comparison.md

## Verdict reasoning

A first-hand postmortem: a Claude Code "unit test" ran `main()` on import, pushed invalid YAML
to two `main` branches, then a `git revert` in a `--depth 1` clone staged the whole tree for
deletion (151 and 723 files) and that was pushed too; one push triggered a production
deploy that failed only by luck. The prescription is three layers (branch protection, a
`pre-push` hook keyed on an inherited agent environment variable, a short rule block), with
the author's own small replays (n = 5 to 12, no transcripts). The clean room rated evidence
3 of 5 and novelty 4 of 5. The comparison found three real gaps in the installed set and one
verified defect: deny-destructive's force-push rule does not fire on `--force-with-lease`
(executed check, five cases). HARVEST: six rows, all Tier 3 (hooks, settings, and the global
CLAUDE.md are Graham's). What would change the verdict: nothing; the rows are the value.

## Ancestry

none. Convergent: two parties hit the same problem (an agent that can run `git push` from a
Bash tool call) and built different defenses.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour, one sitting | `M` an afternoon, one PR | `L`
multi-session, or a merge under the 500-line body cap with more than a handful
of edits; L always goes through `phased-harness`.
Adoption cost is mandatory and never "none": what this adds to the maintenance
surface and how it gets backed out.

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | deny-destructive's force-push rule passes `--force-with-lease`, `--force-with-lease --force-if-includes`, and `--force-with-lease=<ref>` (regex `\s(--force\|-f)(\s\|$)` requires whitespace after `--force`); the global rule says force pushes are never pre-authorizable in any form, and the article shows `--force-with-lease` alone is defeated by a background fetch | defect in the incumbent | Widen the rule to `--force-with-lease` and `--force-if-includes` forms, test-first: three new positives in `prove-hooks.d`, replay against history with `replay-hooks.py` before wiring | `candidate.md` lines 300-320 (the lease-defeat test); incumbent `deny-destructive.py:53`; executed check `regex-check.py` in the run log | `~/.claude/hooks/deny-destructive.py` (hooks runbook, hooks-registry row) | S | one more rule to keep proven after every CLI update; backed out by restoring the regex | proposed (Tier 3: a hook file) | Graham |
| 2 | A git-level `pre-push` hook keyed on the inherited `CLAUDECODE=1` marker (verified set in this session's Bash children), installed through `core.hooksPath`, refusing pushes to protected branches from agent-spawned processes including scripts the agent wrote | SUPERIOR SUBSTITUTE for the push half of deny-destructive | Build as a second layer beside the PreToolUse hook: git invokes `pre-push` whatever process started the push, which command-text matching cannot see (the incident's push came from inside Python). Override routes through the Graham-via-inbox tier, never an agent-settable variable | `candidate.md` lines 230-260 (env marker, hook design); `martinfrancois/agent-git-guard` not inspected | `~/.claude/hooks/` plus `maintainers/hooks-registry.md` (outside-the-table row, `readonly-agent-guard.py` precedent) | M | a hook that fires on every push Graham makes too (it does nothing without the marker); fails open if the marker is renamed; backed out by unsetting `core.hooksPath` | proposed (Tier 3: settings and a hook; a runbook) | Graham |
| 3 | Read `git diff --cached --stat` before every commit and account for every file it lists; an unintended file or deletion is a stop | COMPLEMENT | One bullet in the Concurrency section beside the pre-push SHA check: a commit-time check, which nothing here has (proof-of-work's diff step fires at done time, the carve-out's at push time) | `candidate.md` lines 356-358; incumbents `global-push-rules.md` (carve-out), `proof-of-work/references/code-checklist.md` phase 6 | `~/.claude/CLAUDE.md` (Concurrency and multi-agent runs) | S | one always-loaded line; backed out by deleting it | proposed (Tier 3: global CLAUDE.md) | Graham |
| 4 | Never `git revert` in a shallow clone: a depth-1 HEAD is a grafted root, so the revert stages the whole tree for deletion with exit 0; a normally safe command made dangerous by repository state a text deny-list cannot see | COMPLEMENT | A "known weaknesses" line in deny-destructive's docstring naming the class, plus one bullet: before `git revert` in any clone run `git rev-parse --is-shallow-repository`, unshallow first | `candidate.md` lines 120-160 (mechanism, links git docs) | `~/.claude/hooks/deny-destructive.py` docstring and `~/.claude/CLAUDE.md` | S | none beyond two lines; backed out by deleting them | proposed (Tier 3) | Graham |
| 5 | "If a push already did damage, tell me before you repair it. Repair by adding a commit." | COMPLEMENT | One bullet in the Concurrency section; the incident's revert-of-a-revert is the case | `candidate.md` line 364 | `~/.claude/CLAUDE.md` (Concurrency) | S | one always-loaded line; backed out by deleting it | proposed (Tier 3: global CLAUDE.md) | Graham |
| 6 | Test instruction-file rules against the agent in throwaway repos with and without each rule, with a pressure variant ("production is down"), and cut rules the agent follows anyway (2 of 7 pressure runs overrode the PR rule; 12 of 12 never self-set the override) | COMPLEMENT | Design input for the first `claude plugin eval` suite: a pressure-variant case; rides Q-2026-09-14-1 with placebo row 1 | `candidate.md` lines 325-335, 388-398 | `STATE.md` queue entry Q-2026-09-14-1 (this project) | S | a queue note; backed out by deleting the sentence | proposed (Tier 1 here: a queue note) | scout |
| 7 | Land changes on the default branch through a pull request; ask before merging | philosophy conflict | Do not adopt as written: contradicts the push carve-out (see Conflicts) | `candidate.md` line 359 | - | - | - | out | - |
| 8 | Branch protection on personal repos once an agent can reach them; a separate agent identity with no bypass rights | COMPLEMENT, server side | Outside the library; a GitHub settings decision for Graham | `candidate.md` lines 190-215 | - | S | - | out (noted for Graham) | - |
| 9 | `--force-with-lease --force-if-includes` when a force push is approved (git 2.30+; this machine runs 2.54) | INGESTIBLE FRAGMENT | Footnote wherever a human-approved force push is documented; the blanket ban stands | `candidate.md` lines 300-320 | `~/.claude/CLAUDE.md` (Push carve-out) | S | one clause; backed out by deleting it | proposed (Tier 3, low) | Graham |
| 10 | "Does this result make any sense?" (exit 0 from a destructive revert) | REDUNDANT | proof-of-work: "a passing check at the wrong level is more dangerous than no check at all" | `candidate.md` closing section | - | - | - | out | - |

## Conflicts for the user to rule on

1. Row 7. "**Push carve-out.** A session may push without asking only its own commits, to a
   repo whose `git remote get-url origin` is under `github.com/GFMCloud/`, after ..." (global
   CLAUDE.md) against "Land changes on the default branch through a pull request, and ask
   before merging unless a standing rule allows self-merge" (the article's rule block, written
   by someone just burned by a direct push; PR plus required CI would have stopped both of
   its incidents). Proposal: keep the carve-out (its preconditions already include CI green
   where the repo has CI) and add rows 3 and 5 as commit-time and repair-time stops; the
   carve-out's own "docs-only commits that deploy nothing may go direct" clause is the one
   place the article's argument bites, since a deploying repo with no CI is where a bad push
   lands. Alternative: require a PR for any repo whose default branch deploys.

2. Row 2's override path. The article's hook honours `AGENT_GUARD_APPROVE=1`, an agent-visible
   variable it also planted in CLAUDE.md. Proposal: no agent-settable override; the hook
   refuses, the session stops, and Graham pushes by hand or via the inbox. Alternative: an
   override file outside the repo that only Graham writes.

## Corrections at ingest

- The rule block's last bullet ("A `pre-push` hook refuses these pushes") is false here until
  row 2 is built; never paste it first.
- The article's table "refused in 5 of 7 runs" for script-mediated pushes was not measured
  (only direct pushes were tested; both reviewers checked). Do not cite that column.
- First-person owner voice ("tell me", "my overrides, never yours") is rewritten into the
  library's third-person, dated-ruling style.
- The stray first line "raccoon" in the saved article is site chrome (2 hits in the page
  HTML), not content.
- Environment-marker names (`CLAUDECODE`, `CODEX_THREAD_ID`) are version-bound; the hook
  fails open if renamed. Re-verify after CLI updates (prove-hooks.sh is the vehicle).

## Flags

- Lines 356-371: a `## Git` rule block addressed to an agent, meant for CLAUDE.md or
  AGENTS.md. Quoted in the clean-room review; not installed.
- Line 372-380: a recommendation to install third-party code (`martinfrancois/agent-git-guard`)
  as a git hook. Not inspected, not installed.
- The override variable `AGENT_GUARD_APPROVE=1`, named where agents will read it.
- None of it acted on.

## Rulings log

- 2026-09-28, scout cycle 6: all rows proposed; nothing applied. Rows 1 to 5 and 9 are Tier 3
  (hook files, settings, global CLAUDE.md). Row 6 is a Tier 1 queue note (done this cycle).
