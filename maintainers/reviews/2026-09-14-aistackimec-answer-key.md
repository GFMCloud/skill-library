---
contract: v1
source: https://aistackimec.substack.com/p/we-caught-our-coding-agents-reading
type: article
pin: fetched 2026-09-14T23:30:18Z, sha256 in the review directory's pin.txt
reviewed: 2026-09-14
verdict: HARVEST
recheck: n/a
applied: row 1 as a cross-reference in the config-drift-checker decisions file (same commit as this record); row 2 proposed to /phase ratify in claude-scout-weekly (Q-2026-09-14-10)
evidence: docs/reviews/2026-09-14-aistackimec-answer-key/
---

# aistackimec-answer-key

**Verdict:** HARVEST. Three eval-environment integrity constraints for the tabled skill
eval harness (no answer reachable from the fixtures, prove the scrub inside the built
environment, audit transcripts for retrieval signatures, canaries the model cannot detect
or recite) and one paragraph on ablation rerouting; the article's numbers are not
citable (chart-only, n=64, an arithmetic slip).

**Ancestry:** none.

## What landed

- Row 1: three rider lines under config-drift-checker decisions row 3 (this commit).
- Row 2: proposed (a paragraph beside the ablation note in the authoring standard).

## What was declined, and why

- Prohibition prompt as the leak control: the global Boundaries rule already prescribes
  tool-layer enforcement, and the article's own loophole case supports it.
- Pin the harness version: fact-currency-check's regressions class covers it with a
  procedure; the prefix-cache-rate signal is noted for the cache-economics question.
- Verify a setting took effect: proof-of-work covers it.
- Behavioral observations: no procedure attached.

## Flags

none.

## Re-review trigger

A follow-up with the score tables and intervals, or SWE-Bench Pro publishing scrubbed task
images (then row 1(a) has a worked example).
