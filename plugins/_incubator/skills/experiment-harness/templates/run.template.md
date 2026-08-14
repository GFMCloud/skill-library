---
id: run-<NNNN>-<slug>
hypothesis: <h-id from REGISTER.md>
created: <ISO-8601, when Hypothesis/Prediction/Config were saved, BEFORE running>
executed: <ISO-8601 or empty, filled only after the run actually happens>
---

## Hypothesis

`<The claim being tested, one or two lines. Copied from REGISTER.md at creation.>`

## Prediction

`<What you expect to see, stated concretely enough to be scored against the result:
a number, a direction, a threshold. Written and saved BEFORE the run executes. /run
will not fill in Result/Verdict below unless this section already exists.>`

## Config

`<The exact configuration that produced this run: parameters, data version, code
revision, command line. Enough to reproduce the run from this file alone.>`

---

*Everything below this line is written by `/run`, after execution, never before.*

## Result

`<What actually happened: the raw output, not an interpretation.>`

## Verdict

`<confirmed / refuted / inconclusive, plus one line comparing Result against
Prediction. If refuted or the idea is abandoned, add a row to dead-ideas.md and
update this hypothesis's status in REGISTER.md.>`
