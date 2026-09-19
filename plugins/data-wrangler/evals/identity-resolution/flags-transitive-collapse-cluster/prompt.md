---
name: flags-transitive-collapse-cluster
runs: 1
max_turns: 10
timeout_seconds: 180
allowed_tools: [Read, Skill]
---
Use the identity-resolution skill. Match these three vendor records from an invoice
cleanup. None of them share a canonical identifier: no vendor ID, no email, nothing
but the name string.

Records: V1 "Bramwell Steele Co", V2 "Bramwell Steel Co", V3 "Bramwell Steele Corp"

FIXTURE similarity scores (already computed, do not recompute them):
- V1 vs V2: 0.93
- V2 vs V3: 0.91
- V1 vs V3: 0.71

Accept threshold 0.9, reject threshold 0.6, agreed now for this run.

Give me the mapping table. Do not run any commands; the data above is complete.
