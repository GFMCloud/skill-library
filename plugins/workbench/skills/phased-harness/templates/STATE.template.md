# Project state

**The single resume point.** Keep it current *as you work*, not just at the end - if
the session dies, the next one must be able to continue from this file plus the
runbooks alone. Never rely on conversation memory.

**Status:** `<not started | in progress, phase N | COMPLETE (date)>`

## Phase tracker

- [ ] Phase 0 - `<PHASE-0-NAME>`
- [ ] Phase 1 - `<PHASE-1-NAME>` (read-only)
- [ ] Phase 2 - `<PHASE-2-NAME>` / **Gate A**
- [ ] Phase 3 - `<PHASE-3-NAME>`
- [ ] Phase 4 - `<PHASE-4-NAME>`
- [ ] Phase 5 - `<PHASE-5-NAME>` / **Gate B**

## Spend log

<!-- One entry per phase, two lines each, running total against the spend cap where
     CONFIG.md sets one (toolkit-build-harness named it `spend_cap_usd`):
     - Phase N - subagents: <tokens per subagent, from their completion notices>;
       eval cost from the eval JSON if any - list-price estimate - running total.
     - Phase N - orchestrator: <estimated tokens for the orchestrating session itself>.
       Subagent notices never include the orchestrator; a harness that logs only
       subagents meters part of its spend (toolkit-build-harness A13, 2026-09-11).
       Estimate it from the session's usage display or the transcript size, and say
       which. -->

## Decision log

<!-- Append: date - decision - one-line rationale. Never rewrite old entries. -->
<!-- Gate rulings go here in full, including the ones ratified "as proposed", and
     including any side effects reassigned because a ruling overrode a proposal. -->
<!-- A plan that collided with an invariant goes here too: what collided, and the
     ruling. The phase bends, the invariant does not; amending one is its own gated
     act, never a side effect of the phase that hit it. -->

## Evidence

<!-- Executed evidence, not checkmarks: the command run and its actual output.
     Deliberate-failure proofs of any validator/CI gate go here verbatim.
     Capability preflight results go here. Format per foundry-core:evidence-report. -->

## Anomalies

<!-- Things the runbooks did not anticipate. One entry each:
     date - what/where - why it does not fit - one-line recommendation.
     Anomalies are LOGGED and reviewed at the next gate, never silently resolved
     and never raised one-by-one mid-run. -->

## Open items

<!-- Residue: what this project found and did not close, deferred, or scoped out.
     One line each: what - why it is still open - WHO OWNS IT NEXT.
     Unlike Anomalies, these are not reviewed at the next gate; they are what
     survives the final one, so the final phase must give every entry a
     destination (an owner here, a named successor project, or dropped with the
     reason) before the harness may close. -->

## Session log

<!-- One line per session: date - phase worked - outcome / stopping point. -->
