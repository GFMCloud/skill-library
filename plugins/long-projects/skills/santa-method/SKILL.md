---
name: santa-method
description: >-
  Verify output that has no deterministic check (published writing, customer-facing copy,
  documentation, generated batches, claims and citations) with two independent reviewer
  subagents that share a rubric and nothing else; both must pass, fixes are limited to
  what was flagged, fresh reviewers each round, and after three rounds it escalates to a
  human. Use when the user says "santa method", "check it twice", "two independent
  reviewers", or when output will be published or sent without a human reading every
  line. Not for anything a build, test or lint can decide (run those), not for gating one
  change spec against its goal (review-pair), not for decisions (council). Costs two
  subagent spawns per round, roughly two to three times the generation cost.
metadata:
  maturity: incubator
---

# Santa method: check it twice

An agent reviewing its own output shares the blind spots that produced it. Two reviewers
with no shared context, judging against the same written rubric, break that. If only one
of them catches a problem, the problem is real: the other's miss is exactly what this
exists to cover.

Adapted from the ECC project's `santa-method` skill (MIT, v2.2.1; the source credits
Ronald Skelton, RapportScore.ai), reviewed 2026-09-17. Record:
`maintainers/reviews/2026-09-17-ecc/`. The source's effectiveness figures were not carried
over: none of them has been measured here.

## Inputs

- The task specification the output was produced from.
- The output under review.
- A rubric. Every criterion has an objective pass condition; a criterion that can only
  be judged by taste is removed or rewritten. If there is no rubric, write one and show
  it to the user before round 1.

Starting criteria, to cut down per task:

| Criterion | Pass when | Typical failure |
|---|---|---|
| Factual accuracy | every claim traces to the source material | invented numbers, wrong versions, APIs that do not exist |
| No fabrication | every entity, quote, URL and reference exists | dead links, quotes with no source |
| Completeness | every requirement in the spec is addressed | a skipped section or edge case |
| Constraints | project rules hold (style rules, banned terms, required disclaimers) | a rule broken |
| Internal consistency | no section contradicts another | A says X, B says not X |
| Technical correctness | code and commands are sound as written | syntax errors, wrong flags |

For code add error handling, input validation and secrets; for regulated text add
required disclaimers and no outcome guarantees.

## Steps

1. **Generate** as normal. This skill is a verification layer, not a way of writing.
2. **Review twice, in parallel.** Two fresh subagents, read-only, each given the spec,
   the output and the rubric, and nothing else: not the conversation, not each other's
   result. State the model first. Each returns a structured verdict:

   ```json
   {"verdict": "PASS | FAIL",
    "checks": [{"criterion": "...", "result": "PASS | FAIL", "detail": "exact problem, quoted"}],
    "critical_issues": ["must fix"], "suggestions": ["optional"]}
   ```

   The reviewer prompt says: you have seen no other review; evaluate every criterion;
   your job is to find problems, not to approve.
3. **Gate.** Pass only when both verdicts are `PASS`. Otherwise merge and deduplicate
   the critical issues from both.
4. **Fix only what was flagged.** No refactoring, no unrequested improvements.
5. **Review again with new reviewers.** A reviewer that remembers the last round is
   anchored by it. Repeat from step 3.
6. **Three rounds, then escalate.** Hand the user the output, the open issues and the
   round history. When the fix loop runs unattended, run it under
   `foundry-core:bounded-loop`.

**Batches.** For a large batch, review a random sample (about 15 percent, at least 5
items). Classify failures by type; when a pattern shows, fix the whole batch for that
pattern, then draw a new sample. A clean sample is evidence about the sample: say so,
and state the sample size.

## Failure modes, beside the rule

| Failure | Sign | Response |
|---|---|---|
| Never converges | new issues every round | the three-round cap, then a human |
| Rubber stamp | both pass everything | adversarial prompt; plant a known defect once to prove the rubric can fail |
| Taste drift | style flagged as error | tighten the rubric to objective conditions |
| Fix regression | fixing A breaks B | fresh reviewers each round |
| Shared blind spot | both miss the same thing | independence reduces this, it does not remove it; for critical output add a human spot check |
| Cost | many rounds on large output | sampling, and a stated budget per cycle |

## Verify

Show both raw verdicts for the final round, and, once per rubric, the result of a
planted defect that both reviewers were expected to fail. Pass means both final verdicts
are `PASS` and the rubric has been shown to be able to fail.

## Done when

Both reviewers of the same round return `PASS`, and the round count, the issues fixed
and the share of issues caught by only one reviewer are reported. The user decides what
happens to the output next; this skill publishes and sends nothing.

## Stop when

- Round 3 ends without two passes: escalate with the history.
- A reviewer cannot be spawned (concurrency limit: wait; rate limit: stop). One reviewer
  is not this method; do not substitute yourself for the second.
- The rubric has a criterion no reviewer can decide from what it was given.

## Output contract

None consumed by other skills.

```
Santa: <title>   rounds: <n>   result: PASS | ESCALATED
Round <n>: reviewer B <verdict>, reviewer C <verdict>; issues <n> (flagged by both <n>, by one <n>)
Fixed: <list>        Open: <list or none>
Not checked: <what the rubric does not cover>
```
