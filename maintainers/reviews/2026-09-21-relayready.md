---
contract: v1
source: https://github.com/pawelworks/relayready
type: code-repo
pin: c3c91545f6c7584a7f093e8904a7e8d26fc22d1a
reviewed: 2026-09-21
verdict: HARVEST
recheck:
applied: none (seven rows proposed, Q-2026-09-21-4 in claude-scout-weekly STATE.md)
evidence: maintainers/reviews/2026-09-21-relayready/ (decisions.md, cleanroom-review.md, comparison.md, pin.txt)
---

# relayready

**Verdict:** HARVEST. A careful, offline handoff spec and checker, one day old, Pre-Alpha, one maintainer, with its central claim unexercised (mock benchmark is tautological; the public relay matrix reads `not run` in every cell). Not installed; the readback mechanism is declined because `readback new` output passes `readback check` unedited. Five fragments close real gaps in the installed `handoff` skill.

**Ancestry:** none; convergent structure only.

## What landed

Nothing. All rows are proposed (scout cycle 5, unattended, Tier 2 off):

- Row 1 (S): an INVARIANTS list carried verbatim by every successor handoff, as constraints only; explicit `None.` for three lists; no hash.
- Row 2 (S): an unresolved human-only question is a stop in Resume Mode step 7.
- Row 3 (S): a prior-effects row (`not_applied`, `applied`, `unknown`); never replay applied or unknown.
- Row 4 (S): per-pointer `shasum` as a checkable claim in `references/claims.md`. The first row in five scout cycles that fits Tier 2 as written.
- Row 5 (S): "a clean secret scan is not proof" in Redaction and two hook docstrings.
- Row 6 (S): DONE MEANS, a needs-recheck bucket, no relative time, a length target.
- Row 7 (M): the Relay Bench trap and three-arm design as the first eval case set for `handoff`.

## What was declined, and why

- Row 8: the readback acknowledgment proves fields exist, not that the receiver engaged; Resume Mode re-checks live artifacts.
- Row 9: continuation gate and chain checker need an uninstalled CLI and producers that do not exist here.
- Row 10: redundant with `references/claims.md`.
- Row 11: the shipped skills and the AGENTS.md snippet would misroute against `handoff`.

Three conflicts are recorded for Graham, one of them inside the incumbent: `SKILL.md:260` says "Don't start working yet" while Resume Mode step 7 ends in "proceeding".

## Flags

`AGENTS.md`, `integrations/AGENTS.md.snippet`, the per-vendor `SKILL.md` files, and `integrations/chat/RESUME_PROMPT.md` all instruct a reading agent to stop and wait for a human; the root `HANDOFF.md` carries the repo's own release directives. Quoted in decisions.md; none followed. No credential solicitation.

## Re-review trigger

The relay matrix filling with real cross-vendor runs, or a release past 0.1.x with a second maintainer.
