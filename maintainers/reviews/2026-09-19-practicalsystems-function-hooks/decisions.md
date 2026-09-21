# Decisions: practicalsystems-function-hooks

contract: v1
source: https://www.practicalsystems.io/blog/claude-code-function-hooks-mods-layer
type: article
pin: fetched 2026-09-19, sha256 ba29e50ba5291c1794805d826ef9d06a67b8f4827cd1979bfdc0b38341d3ea30 (markitdown of the page; dated September 17, 2026)
reviewed: 2026-09-19
verdict: HARVEST
recheck:
evidence: docs/proposals/2026-09-19-practicalsystems-function-hooks/cleanroom-review.md, docs/proposals/2026-09-19-practicalsystems-function-hooks/comparison.md (claude-scout-weekly; held here because of A-11)

## Verdict reasoning

The function-hook architecture the article recommends is not wanted: it sits on an
experimental env flag whose absence is silent, which is the article's own first failure. Four
small fragments are wanted. The largest is a real gap: `prove-hooks.sh` proves a hook script
is correct on fixtures, not that a normal session invokes it; the only session-level proof on
record is the manual headless run in the hooks runbook result. On deliberate-failure proof,
denial tests, and noise measurement the incumbents are ahead of the article. The verdict
would move toward WATCH-plus-adopt only if function hooks ship documented and this machine
gains a consumer (W-18).

## Ancestry

none. Both sides state "prove it by deliberate failure" in different words; convergence, not
lineage.

## Rows

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Check the artifact a hook produces in a real session, not its presence in a list | INGESTIBLE FRAGMENT | Reword the `prove-hooks.sh` header (lines 63 to 66) to say it proves the script on fixtures, and add a standing live-session arm: one headless call per wired hook class after each CLI update, asserting the denial or the WARN appears in a real session; cover the plugin hook `readonly-agent-guard.py`, which the registry already lists as a residue | article.md line 202; comparison.md A4 | `maintainers/scripts/prove-hooks.sh` | M | About USD 0.30 per live call (the runbook's recorded runs cost 0.97 for three), so roughly USD 1 to 2 per CLI update; backs out by dropping the arm | proposed | Graham (library script, effort M) |
| 2 | Match a tool name only at a command position | INGESTIBLE FRAGMENT | Test-first: add wrapper-aware positives (`sudo`, `env X=1`, `xargs`, `bash -c`, `||`, `&`, newline, backticks) and one quoted-text negative to `PreToolUse__Bash__0.json`, then anchor the patterns in `deny-destructive.py`; replay on four weeks of history before and after. Fixes the documented accepted false positive (an orchestrator prompt containing the force-push string) | article.md line 174; comparison.md A7 | `~/.claude/hooks/deny-destructive.py` (settings-wired hook) | M | A destructive-command guard that under-matches costs data, so the positives must not drop; backs out by restoring the previous script, kept as `.superseded` | proposed | Graham (settings hook: always Tier 3) |
| 3 | Deny reason names the safe sibling | INGESTIBLE FRAGMENT | Keep the decision as deny; append one clause naming the safe form where one exists (`--force-with-lease`, `git branch -d`, `git reset --soft`, `rm -rf` under the scratchpad root); keep the rule name in parentheses because `replay-hooks.py:86` parses it; add a `stdout_contains` fixture per hint | article.md line 200; comparison.md A9 | `~/.claude/hooks/deny-destructive.py` | S | A few strings and fixtures; none beyond upkeep | proposed | Graham (settings hook) |
| 4 | Tie each green proof to a build | INGESTIBLE FRAGMENT | Print `claude --version` in the `prove-hooks.sh` summary line | comparison.md A8 residue | `maintainers/scripts/prove-hooks.sh` | S | One line | proposed | Graham (library script) |
| 5 | Heartbeat handoff between a classic and a function-hook layer; function-hook API (`tool.call` rewriting, `$.session.usage()`, store, bus); result redaction | COMPLEMENT, no consumer | Hold until function hooks are documented and a consumer exists here; evidence added to W-18. `prove-hooks.sh:257-259` marks any non-command hook RED, so adoption would need a new proof arm | article.md lines 43 to 99 | none | - | - | out (rides W-18) | - |
| 6 | Shadow mode; fail toward the old behavior; deliberate-failure proof; test the denials; "a false-positiving guard gets disabled"; version pin defers to a probe | REDUNDANT, incumbent superior | `replay-hooks.py` measures before wiring; `prove-hooks.sh` names `dead detector under-blocks` and `dead exemption over-blocks`; the 5-per-100 noise bar; re-prove after every CLI update | comparison.md A2, A3, A5, A6, A8, A11 | none | - | - | out | - |
| 7 | Subagent startup tax ("about 17,000 tokens") | COMPLEMENT | Do not ingest the number (n=5, one install). The method rides Q-2026-09-19-3, which measured 70,130 tokens per Agent-tool spawn on this machine | article.md lines 101 to 119 | none | - | - | out (rides Q-2026-09-19-3) | - |
| 8 | Read cache, context nudge, bus and dashboard plumbing, two-writer tagging | DISCARD | Author-specific | - | none | - | - | out | - |

## Conflicts for the user to rule on

1. Article: "Rewrite beats deny. ... Deny is reserved for what no rewrite can fix." vs the
   ruled deny (Q-2026-09-03-15 row 1): "Not a prompt: choose a different command." Proposal:
   keep deny for the destructive class and take only the message shape (row 3). A silent
   rewrite of `--force` to `--force-with-lease` leaves the model believing it force-pushed.
   Alternative: none recommended.
2. Article: "A patch change defers to the probe" vs `prove-hooks.sh:68-70`: a patch release
   invalidates last week's green. Proposal: incumbent stands; 2.1.260 fixed four silent rule
   failures and 2.1.273 reverted a deny-rule behavior again this week.

## Corrections at ingest

- Do not cite either hook count (27 in the body, 19 in a promo).
- Drop the "1,500 to 2,300 tokens high" claim; the article's own table shows reserve errors of
  -301 to +679.
- The article's command-position list omits `||`, `&`, newlines, backticks, and wrappers; row
  2 adds them.
- Any imported classic hook must emit a JSON deny: `prove-hooks.sh:221` maps empty stdout to
  allow, so an exit-2-only hook reads as a dead detector.
- Rewrite ingested text in library voice; the article is full of the contrast-and-closer
  patterns `humanizer` targets.

## Flags

Nothing addresses a reviewing agent. Three passages touch agent configuration and were not
acted on: the fenced `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`; "It's in settings now, user scope,
so every session gets it."; a link to the author's public harness repo.

## Rulings log

2026-09-19, scout cycle 4 (unattended): all rows proposed, none applied. Queue entry
Q-2026-09-19-7. Related open entry: Q-2026-09-14-2 (hung-hook control), which gains a
missing-config arm from cycle 4 C-17.
