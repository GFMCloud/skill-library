# Decision Rubric

Score the task on each axis below, low to high. Don't overthink the scoring, this is meant to take seconds, not a scorecard to agonize over. The point is to land on a model + effort recommendation, not to produce a rigorous evaluation.

## The Five Axes

**Reasoning**: how much multi-step logic, tradeoff-weighing, or inference is required before an answer exists?
- Low: the answer is a lookup, a format conversion, a direct extraction.
- Medium: some synthesis across a few inputs, one or two judgment calls.
- High: architecture-level tradeoffs, ambiguous requirements, multi-constraint optimization.

**Creativity**: how much of the task is generative/open-ended vs. mechanical?
- Low: fill in a template, apply a fixed rule.
- Medium: draft original content within a known format.
- High: original strategy, novel structure, greenfield design with no existing pattern to follow.

**Risk**: what happens if the output is wrong or the task is executed poorly?
- Low: easily caught and fixed, no external exposure (a draft, a scratch file).
- Medium: goes to an internal audience, costs time to redo if wrong.
- High: customer-facing, financial, security/access-control, irreversible, or feeds a decision with real consequences.

**Repetition**: is this a one-off or does it recur across many similar items?
- Low: single task, done once.
- Medium: a handful of similar items in this session.
- High: 10+ near-identical items (fan-out candidate) or a workflow that will run again and again.

**Human Oversight**: how much is a person checking the output before it matters?
- Low: someone reviews every output line by line before it ships.
- Medium: spot-checked, not exhaustively reviewed.
- High: runs unattended or ships close to directly (scheduled task, automation, bulk operation).

## Reading the Score

There's no formula that mechanically outputs a model name, use `model-catalog.md` and `effort-sizing.md` to translate the axis scores into an actual pick. As a rough shape:

- Mostly-low scores across the board → cheapest/fastest model, low effort.
- High Risk or high Reasoning, regardless of the others → bump model tier and/or effort up. These two axes dominate, a low-reasoning, low-creativity task that happens to be high-risk (e.g. touches IAM permissions or a customer contract) still deserves the more careful model.
- High Repetition → this is a fan-out signal, not a model-tier signal. Route to `subagent-routing.md` regardless of what the other axes say.
- High Human Oversight (i.e. low actual review) → treat as equivalent to bumping Risk up one notch, since nothing is catching mistakes downstream.

When two axes disagree (e.g. low reasoning but high risk), the higher one wins for model selection. Effort level can still flex independently, a high-risk, low-reasoning task might warrant a stronger model at a lower effort setting (get it right, but it doesn't need to think long to get there).
