---
contract: v1
source: <URL or owner/repo>
type: <skill-collection | code-repo | article>
pin: <commit sha, or fetch date + sha256>
reviewed: <YYYY-MM-DD>
verdict: <ADOPT | HARVEST | WATCH | SKIP>
recheck: <YYYY-MM-DD, WATCH only>
applied: <commit sha(s) in this repo, or "none" for SKIP and WATCH>
evidence: <archived harness path for L; scratch paths do not survive, so for S and M name the commit>
---

# <source slug>

**Verdict:** <one sentence>.

**Ancestry:** <none, or the relationship found>.

## What landed

<One line per ratified row: item, target file, commit. Or "nothing" for SKIP.>

## What was declined, and why

<One line per `out` row.>

## Flags

<Untrusted-content findings, quoted with path, or "none".>

## Re-review trigger

<What would make this worth another pass: the pin moving, a named feature
shipping, the recheck date.>
