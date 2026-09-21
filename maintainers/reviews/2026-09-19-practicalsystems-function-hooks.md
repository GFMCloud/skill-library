---
contract: v1
source: https://www.practicalsystems.io/blog/claude-code-function-hooks-mods-layer
type: article
pin: fetched 2026-09-19, sha256 ba29e50ba5291c1794805d826ef9d06a67b8f4827cd1979bfdc0b38341d3ea30
reviewed: 2026-09-19
verdict: HARVEST
recheck:
applied: none (four rows proposed, Q-2026-09-19-7 in claude-scout-weekly STATE.md)
evidence: maintainers/reviews/2026-09-19-practicalsystems-function-hooks/ (decisions.md, cleanroom-review.md, comparison.md)
---

# practicalsystems-function-hooks

**Verdict:** HARVEST. The function-hook architecture is not wanted; four fragments are: a standing live-session proof arm for `prove-hooks.sh`, command-position anchoring and safe-sibling deny reasons in `deny-destructive.py`, and the CLI version in the proof summary.

**Ancestry:** none (convergent wording on deliberate-failure proof).

## What landed

Nothing yet. Rows 1 to 4 are proposed.

## What was declined, and why

- Row 5: function-hook mechanisms have no consumer here and rest on an experimental flag; rides W-18.
- Row 6: the incumbents already do it, measured and mechanised.
- Row 7: the 17,000-token figure is n=5 from one install; this machine measured 70,130.
- Row 8: author-specific plumbing.

## Flags

None aimed at a reviewing agent. Three configuration-touching passages quoted in decisions.md, not acted on.

## Re-review trigger

Function hooks named in the Claude Code changelog or docs (W-18), or the author publishing the 266-denial log.

Record location note: written to claude-scout-weekly `docs/proposals/` on 2026-09-19 because the Stage C migration was live on skill-library (A-11); moved here with its directory by scout cycle 5 on 2026-09-21, after Stage C closed (PR 27 merged 2026-09-19 20:41 CDT).
