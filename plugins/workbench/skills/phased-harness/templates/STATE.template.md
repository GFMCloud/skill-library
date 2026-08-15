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

## Decision log

<!-- Append: date - decision - one-line rationale. Never rewrite old entries. -->
<!-- Gate rulings go here in full, including the ones ratified "as proposed", and
     including any side effects reassigned because a ruling overrode a proposal. -->

## Evidence

<!-- Executed evidence, not checkmarks: the command run and its actual output.
     Deliberate-failure proofs of any validator/CI gate go here verbatim.
     Capability preflight results go here. Format per foundry-core:evidence-report. -->

## Anomalies

<!-- Things the runbooks did not anticipate. One entry each:
     date - what/where - why it does not fit - one-line recommendation.
     Anomalies are LOGGED and reviewed at the next gate, never silently resolved
     and never raised one-by-one mid-run. -->

## Session log

<!-- One line per session: date - phase worked - outcome / stopping point. -->
