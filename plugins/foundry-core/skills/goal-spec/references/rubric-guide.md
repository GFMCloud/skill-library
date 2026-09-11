# Writing a criterion-separated rubric

Applies when a Goal block v1's `kind` is `judgment`. Per the research record's
secondary finding for T1: rubrics for judgment tasks are criterion-separated
and scored independently, never rolled into one holistic number. This file
is guidance for writing that rubric; it does not define the Goal block
shape (interface spec, section 1) or introduce a new shape of its own.

## Why not one score

A single 1-10 "how good is this" number hides which quality failed. It also
invites anchoring: a reviewer who forms one overall impression first tends
to back-fill the number to match it, rather than checking each quality on
its own. Separating criteria forces each one to be judged on its own
evidence.

## Shape of a rubric file

Plain Markdown, one section per criterion. Each criterion:

- Is named as a single quality, not a compound one ("clarity of the opening
  paragraph", not "clarity and structure").
- States what a pass looks like, concretely enough that two different
  reviewers would agree on a verdict most of the time.
- Is scored independently: reading criterion 2 should not require having
  formed a verdict on criterion 1 first, and the file's scoring instructions
  say so explicitly.
- Never nets out into one combined score in the rubric file itself. If a
  single overall verdict is genuinely needed downstream (a review-pair
  `pass`/`fail`), that verdict is a separate, explicit rule stated once
  ("pass requires every criterion at or above 3 of 5"), not an average.

Template:

```markdown
# Rubric: <name>

Score each criterion independently. Do not let one criterion's score
influence another. Report all criterion scores, not just the total.

## Criterion 1: <single quality>

Pass: <concrete description of what a pass looks like>
Fail: <concrete description of what a fail looks like>
Score: 1-5, independent of the other criteria.

## Criterion 2: <single quality>

Pass: ...
Fail: ...
Score: 1-5, independent of the other criteria.

## Overall

Pass requires: <the explicit combination rule, e.g. "every criterion at or
above 3", never an average of the criterion scores>.
```

## Worked example

Ask: "review my homepage" (judgment — no single command settles "is this a
good homepage").

```markdown
# Rubric: homepage-review

Score each criterion independently. Do not let one criterion's score
influence another. Report all criterion scores, not just the total.

## Criterion 1: first-screen clarity

Pass: a visitor who has never seen the site can state what it does and who
it is for within 5 seconds of looking at the hero section alone.
Fail: the hero section requires scrolling or reading body copy to answer
either question.
Score: 1-5, independent of the other criteria.

## Criterion 2: call-to-action visibility

Pass: exactly one primary action is visually dominant above the fold, and
its label states the action in a verb phrase ("Start free trial", not
"Learn more").
Fail: zero or more than one visually dominant action above the fold, or a
vague label.
Score: 1-5, independent of the other criteria.

## Criterion 3: load-bearing trust signals

Pass: at least one concrete, checkable trust signal is visible above the
fold (a named customer logo, a specific number, a dated review) — not a
generic claim ("trusted by thousands").
Fail: no concrete signal above the fold, or the only signals are generic
claims.
Score: 1-5, independent of the other criteria.

## Overall

Pass requires: every criterion at or above 3 of 5. A single criterion below
3 holds the review regardless of the other two scores.
```

This is the `end_state` a Goal block v1 with `kind: judgment` would cite:
"every criterion in rubrics/homepage-review.md scores at or above 3 of 5."
The `check` field for a judgment goal is the act of applying the rubric and
surfacing the per-criterion scores in the transcript — there is no shell
command, but the scores must still be printed verbatim, the same rule R-1
puts on a measurable check's output.

## Common mistakes

- Two criteria that are really one quality asked twice ("visual appeal" and
  "aesthetic quality") — collapse them.
- A pass line that only a domain expert could apply ("professional design
  sensibility") — rewrite it as an observable a non-expert reviewer could
  check.
- A combination rule that averages instead of gating ("average of 3.5 or
  above passes") — this hides one bad criterion behind two good ones. Prefer
  a floor per criterion.
