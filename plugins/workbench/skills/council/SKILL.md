---
name: council
description: >-
  Convene a four-voice council (your own position first, then a Skeptic, a Pragmatist and
  a Critic as fresh subagents that see only the question) for a decision with several
  credible paths and no obvious winner, and present the disagreement before a
  recommendation. Use when the user asks for second opinions, dissent, "argue the other
  side", "am I anchored", a go or no-go call, or a tradeoff such as ship now versus hold.
  Not for verifying that output is correct (santa-method), not for code review, not for
  planning implementation steps, and not for a factual question. Costs three subagent
  spawns per round.
metadata:
  maturity: incubator
---

# Council

A long conversation anchors whoever is in it. This skill gets three opinions from
contexts that never saw the conversation, and makes the synthesizer commit to a position
before reading them.

Adapted from the ECC project's `council` skill (MIT, v2.2.1), reviewed 2026-09-17.
Record: `docs/reviews/2026-09-17-ecc/`.

## Inputs

- The decision, reducible to one question: what is being decided, which constraints
  matter, what counts as success. If it cannot be reduced, ask one clarifying question
  first.
- Only the context the decision needs: the relevant files, numbers or issue text, kept
  compact. For a strategic question, usually none.

## Steps

1. **Write your own position first**, before spawning anyone: the position, the three
   strongest reasons, and the main risk in it. This is the Architect voice (correctness,
   maintainability, long-term effect). It is written down so the synthesis cannot
   quietly become a mirror of the other three.
2. **Spawn three voices in parallel**, each a fresh subagent given the question, the
   compact context, its role, and none of the conversation. State the model first.
   - **Skeptic:** challenge the framing and the assumptions; propose the simplest
     credible alternative, including "do not decide this now".
   - **Pragmatist:** speed, user impact, what actually happens operationally.
   - **Critic:** edge cases, downside risk, how the plan fails.

   ```text
   You are the <ROLE> on a four-voice decision council.
   Question: <the one question>
   Context: <only what is needed>
   Reply with: 1. Position (1 to 2 sentences)  2. Reasoning (3 short bullets)
   3. Risk (the biggest one in your own recommendation)
   4. Surprise (one thing the other voices may miss)
   Be direct. Under 300 words.
   ```
3. **Synthesize under these rules.** An external view is never dismissed without a stated
   reason. If a voice changed the recommendation, say so. The strongest dissent is
   always printed, even when rejected. Two voices aligned against the initial position
   is a real signal, not noise. Raw positions appear before the verdict.

Default is one round. For another round, keep the new question narrow and give the
Skeptic as little of the previous verdict as possible.

## Persistence

Nothing is written by default. When the council changes a decision that a project
tracks, record it where that project records decisions (a `rulings-harness` register, a
decision log, the issue), and never in an ad-hoc notes file.

## Verify

The output shows all four raw positions, a named strongest dissent, and the step 1
position as written before the voices returned. Pass means a reader can see whether
the recommendation moved and why.

## Done when

The block below has been presented and the decision is left with the user.

## Stop when

- The question cannot be stated as one decision after one clarifying question.
- The answer is a fact that can be looked up: answer it, do not convene.
- A voice fails to return (spawn limit, rate limit): present the voices that did, say
  which is missing, and do not fill it in yourself.

## Output contract

None consumed by other skills. Keep it readable on a phone.

```markdown
## Council: <short title>
**Architect:** <position>. <one line why>
**Skeptic:** <position>. <one line why>
**Pragmatist:** <position>. <one line why>
**Critic:** <position>. <one line why>

### Verdict
- **Consensus:** <where they align>
- **Strongest dissent:** <the disagreement that matters most>
- **Premise check:** <did the Skeptic challenge the question itself>
- **Recommendation:** <the synthesized path, and whether it moved from step 1>
```

The value is not agreement. It is making the disagreement visible before choosing.
