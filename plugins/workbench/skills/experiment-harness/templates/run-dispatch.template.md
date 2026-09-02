---
name: run
description: >-
  Execute the next planned run for `<PROJECT-NAME>` and score it against its
  already-written prediction. Use once a hypothesis has been registered with
  `/hypothesis` and you are ready to actually run it.
metadata:
  maturity: stable
  version: 1.0.0
  reviewed: <YYYY-MM-DD>
---

# Execute a run: `<PROJECT-NAME>`

## Steps

1. Identify the planned run file: the most recent `runs/run-<NNNN>-<slug>.md` with
   an empty Result section, or one named explicitly by the user.
2. **Gate check.** Confirm the Hypothesis, Prediction, and Config sections are
   already filled and were saved before now (check the `created` timestamp against
   the current time). If Prediction is empty, stop: this run was not registered
   through `/hypothesis` and has no prior prediction to score against. Do not fill
   in a prediction now and then immediately run: that is the exact rationalization
   failure this harness exists to prevent. Send the user to `/hypothesis` first.
3. Execute the run using the Config section exactly as written. Do not silently
   change parameters mid-run; if the config needs to change, that is a new run file.
4. Fill in **Result** with the raw output, and **Verdict** (confirmed / refuted /
   inconclusive) comparing Result against the Prediction written beforehand. Set
   `executed` to now.
5. Update the hypothesis's row in `REGISTER.md`: `status: tested`, link this run
   file.
6. If the verdict is `refuted`, or the user decides to abandon the line of inquiry
   regardless of verdict, append one row to `dead-ideas.md` with the reason and this
   run file's link, and set the register row's `status: killed`.

## Guardrails

Only this session writes `REGISTER.md`, `dead-ideas.md`, and the run file being
executed. If the run itself is delegated to a subagent (an expensive fit or
simulation), the subagent writes only the Result section's raw data to a scratch
location and returns it; this session is the one that writes it into the run file
and updates the shared files afterward.
