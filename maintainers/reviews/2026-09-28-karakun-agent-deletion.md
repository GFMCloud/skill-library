---
contract: v1
source: https://dev.karakun.com/2026/08/28/coding-agent-pushed-deletion-to-main.html
type: article
pin: fetched 2026-09-28, sha256 b535965045356645e25120c292bacb96765a2a633d0f59b06b117914f2ba78fe
reviewed: 2026-09-28
verdict: HARVEST
recheck: -
applied: none (rows proposed to the scout queue Q-2026-09-28-5; this record's own commit)
evidence: maintainers/reviews/2026-09-28-karakun-agent-deletion/ (cleanroom-review.md, comparison.md, decisions.md, article.md); run log ~/work/claude-scout-weekly/runs/2026-09-28.md
---

# karakun-agent-deletion

**Verdict:** HARVEST. A first-hand postmortem (François Martin, 2026-08-28; surfaced on HN
2026-09-25) of a Claude Code auto-mode session that pushed a shallow-clone `git revert`
deleting 151 and 723 files to two `main` branches; its three-layer fix (branch protection,
a `pre-push` hook keyed on the inherited `CLAUDECODE=1` marker, a short rule block) names
three gaps in the installed set, and the comparison found a verified defect: the installed
force-push deny rule does not fire on `--force-with-lease` in any of its forms (executed
check, five cases). Six rows, all Tier 3 because every target is a hook file, settings, or
the global CLAUDE.md.

**Ancestry:** none; convergent defenses against the same problem.

## What landed

Nothing in the library. Row 6 (a pressure-variant eval case) is a queue note on
Q-2026-09-14-1 in the scout's STATE.md (Tier 1 there).

## What was declined, and why

- "Land changes through a pull request": contradicts the push carve-out; recorded as a
  conflict for Graham, not adopted.
- Branch protection and a separate agent identity: server-side GitHub settings, outside the
  library; noted for Graham.
- "Does this result make any sense?": proof-of-work already says it, with three logged cases.
- The third-party hook repo (`martinfrancois/agent-git-guard`): not inspected, not installed.

Proposed, not applied (Q-2026-09-28-5): widen the force-push rule (row 1, test-first); a
git-level `pre-push` hook keyed on the agent marker (row 2, M, a runbook); `git diff --cached
--stat` before every commit (row 3); the shallow-clone revert hazard as a known weakness plus
a bullet (row 4); "tell me before you repair; repair by adding a commit" (row 5);
`--force-if-includes` as a footnote (row 9).

## Flags

- Lines 356-371: a `## Git` rule block addressed to an agent, meant for CLAUDE.md.
- An override variable (`AGENT_GUARD_APPROVE=1`) named where agents read it.
- A recommendation to install third-party code as a git hook.
- None of it acted on.

## Re-review trigger

None for the article. Row 2's hook, if built, is re-proven after every CLI update because
the marker name is version-bound (the article's own currency-risk list, items 1 and 4).
