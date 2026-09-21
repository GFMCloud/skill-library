---
contract: v1
source: https://github.com/ahasha/learning-plugin
type: code-repo
pin: 947f9eedb26d715e2a38e78ad96259c06820802e
reviewed: 2026-09-21
verdict: HARVEST
recheck:
applied: none (six rows proposed, Q-2026-09-21-1 and Q-2026-09-21-5 in claude-scout-weekly STATE.md)
evidence: maintainers/reviews/2026-09-21-learning-plugin/ (decisions.md, cleanroom-review.md, comparison.md, claude-code-docs-memory-rules-section.md, pin.txt)
---

# learning-plugin (scoped-learnings)

**Verdict:** HARVEST. The plugin is not installed: its Stop hook self-assesses where retro gates on evidence, its recording skill writes before it shows the diff, and its checker has a confirmed parser bug and no tests. What it stands on matters more than it does: Claude Code documents path-scoped rules (`.claude/rules/*.md` with `paths:`, and `~/.claude/rules/`) as a native, load-on-matching-Read mechanism, which four scout cycles had not recorded and which the ratified JIT-rules prototype runbook would re-implement with a hook.

**Ancestry:** none.

## What landed

Nothing. All rows are proposed (scout cycle 5, unattended, Tier 2 off):

- Row 1: re-scope the JIT-rules prototype native-first (three arms; keep the hook only if a new-file Write with nothing read shows no rule text; fix the runbook's step 1 vs step 3 contradiction; re-rule precedent row 1).
- Rows 2 to 4 (S, retro): routing rows for `.claude/rules/` and `~/.claude/rules/`; "the rule, then the reason"; staleness tested against the code, with "A stale rule is worse than no rule: it is confidently wrong."
- Row 5 (M): the glob-staleness linter, only if rule files are adopted, after four fixes.
- Row 6 (S): once-per-session marker claimed before acting, if the hook survives.

## What was declined, and why

- Row 7: redundant with retro's routing table and the Boundaries rule.
- Row 8: the Stop hook, both skills as shipped, and the plugin packaging collide with retro on the end-of-task trigger surface (retro owns it by ruling) and would misroute "remember that I prefer X" into project CLAUDE.md.

Two conflicts are recorded for Graham: the economy rule's premise ("every line loads into every session") against the documented native scoping, and the admission threshold.

## Flags

`hooks/learning-check.sh:60` injects an instruction that ends "do not mention this check"; `skills/record-learning/SKILL.md:33-35` has the agent write to the files that configure future agents, gated by prose only. Quoted in decisions.md; not installed, not followed. No credential request, no network call.

## Re-review trigger

None for the plugin. The native mechanism is the thing to re-check: read the docs page again when the JIT prototype is run.
