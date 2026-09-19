---
contract: v1
source: https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/
type: article
pin: fetched 2026-09-14T23:30:18Z, sha256 in the review directory's pin.txt
reviewed: 2026-09-14
verdict: HARVEST
recheck: n/a
applied: row 1 as a cross-reference in the config-drift-checker decisions file (same commit as this record); row 2 proposed to /phase ratify in claude-scout-weekly (Q-2026-09-14-9)
evidence: docs/reviews/2026-09-14-google-harness-engineering/
---

# google-harness-engineering

**Verdict:** HARVEST, thin. Two constraints for the tabled skill regression harness (no
tuning against the gating suite; a negative control per case) and one seed idea (cases
from observed failures, strictness matched to task openness); the article itself has no
data and contradicts its own "fast, deterministic" framing.

**Ancestry:** none. Independent arrival on ground the library surveyed and shelved on
2026-09-03 (config-drift-checker row 3).

## What landed

- Row 1: two rider lines under config-drift-checker decisions row 3 (this commit).
- Row 2: proposed; rides Q-2026-09-14-1 (first eval suite on `claude plugin eval`).

## What was declined, and why

- Assert on intermediate steps: proof-of-work already states the broader rule with three
  dated incidents behind it.
- Gate on aggregate pass rates: experiment-harness's run template requires paired per-item
  wins and a stated sample size, a stricter form.
- The self-tuning prompt loop: violates the frozen-holdout rule and the bounded-loop rule;
  row 1 forbids it for the tabled harness.
- The illustrative seed behaviors: prompts, not a method.

## Flags

none.

## Re-review trigger

A follow-up with measured before-and-after data, or config-drift-checker row 3 being
unshelved (then rows 1 and 2 are read at scaffold time).
