---
type: regex
pattern: "is for source 'cloudwatch:demo-alarm-fixture'"
match: contains
---

Confirms the run actually hit the mismatch condition rather than skipping the
step script or silently assuming success. This is the exact literal text
watch-step.py writes to stderr for this fixture and source pair, so it is
decidable independent of how the model phrases its own report.
