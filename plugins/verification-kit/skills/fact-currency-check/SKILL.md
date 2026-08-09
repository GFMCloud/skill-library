---
name: "fact-currency-check"
description: "Check whether a claim, citation, version number, or referenced issue is still true today rather than true when it was written. Use before acting on returned research, and specifically when an open issue is being read as an unmet need."
metadata:
  maturity: incubator
---

# fact-currency-check

Identified as needed in three past projects. Executed in zero of them.

Returned research arrives with citations attached and reads as finished. It is
not consumable as-is. The item-2 research pass on this project returned four
load-bearing claims: one confirmed but understated, one first-party
confirmation that held, one **stale in a way that reversed its own
conclusion**, and one false negative on a fact that was published in the docs.
Two of four needed correction.

## Procedure

**1. Mark which claims are load-bearing.** A claim is load-bearing if a
decision changes when it flips. Check those. Do not check the rest — currency
checking everything is how this step gets skipped entirely.

**2. For each, find the primary source and say what "primary" means here.**

- For a **fact**: the first-party source, not a summary of it.
- For **behavior**: the running system. **First-party documentation is not a
  primary source for behavior.** Originating failure, 2026-07-27: the
  `metadata.pluginRoot` mechanism is documented, has a worked example, and does
  not function on the current release. It took a five-minute test to find and
  would have silently broken the install.
- For a **status** (shipped / open / deprecated / supported): the system of
  record, checked today.

**3. Date the claim.** Every verified claim carries an as-of date. A claim
without one is a claim about an unspecified past.

**4. Record what changed.** If the source now says something different from
what the research said, that delta is the output — not a silent correction.

## Two failure modes that recur

**An open issue is not evidence of an unmet need.** Item 2 read a feature
request as still-current because the issue had never been closed. The ask had
shipped. Issues go stale open far more often than they go stale closed — check
whether the thing was done, not whether the ticket was tidied.

**"No evidence found" means "did not look hard," not "does not exist."** Item 2
returned a clean no-evidence-found for a fact that was sitting in the published
documentation. Treat a negative result from a research tool as an
unsuccessful search, and search again differently before recording absence.

## Also worth re-checking

- **Version floors and deprecations** — "requires v2.1.110+" was true once.
- **Regressions** — a documented behavior that worked at the time of writing
  may have regressed since. Symlink dereference within a marketplace is the
  logged case: documented, worked, regressed in v2.1.117, closed as not
  planned.
- **Anything phrased as "currently," "recently," or "as of now"** with no date
  attached.

## Output

Per load-bearing claim: the claim, the primary source consulted, the as-of
date, and one of CONFIRMED / CHANGED / UNVERIFIABLE. `CHANGED` carries the new
value and what it invalidates downstream.
