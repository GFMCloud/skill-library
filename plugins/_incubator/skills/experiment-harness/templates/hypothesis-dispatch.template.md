---
name: hypothesis
description: >-
  Register a new hypothesis for `<PROJECT-NAME>` and write its prediction before
  any run happens. Use when starting a new idea, a new angle on the model, or
  before running anything whose result you have not yet predicted.
metadata:
  maturity: stable
  version: 1.0.0
  reviewed: <YYYY-MM-DD>
---

# Register a hypothesis: `<PROJECT-NAME>`

## Steps

1. Read [dead-ideas.md](../../../dead-ideas.md). If the proposed hypothesis matches
   or closely resembles a killed one, stop and confirm with the user explicitly:
   name the prior attempt, why it was killed, and what is different this time. Do
   not silently re-register it.
2. Read [REGISTER.md](../../../REGISTER.md). Assign the next `id`, append one row
   with `status: open`, the hypothesis, and the prediction.
3. Create `runs/run-<NNNN>-<slug>.md` from the run template, with the **Hypothesis**,
   **Prediction**, and **Config** sections filled in and `created` timestamped now.
   Leave **Result** and **Verdict** empty: those belong to `/run`, after execution,
   not now.
4. Save. Do not execute the run in this step, even if it would be convenient. The
   gate is exactly this separation: the prediction exists on disk before anything is
   looked at.
5. Tell the user the run file id and that `/run` is the next step when ready.

## Guardrails

`REGISTER.md` and `dead-ideas.md` are append-only; this skill never edits an existing
row's hypothesis or prediction text. Only this session writes them; do not delegate
either write to a subagent that could run concurrently with another writer.
