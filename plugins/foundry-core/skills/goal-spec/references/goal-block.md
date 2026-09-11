# Filling a Goal block v1

The shape itself is defined once, in the toolkit interface spec
(`docs/toolkit-interface-spec.md`, section 1). This file is guidance on how to fill
each field; it does not redefine the shape. If the two ever disagree, the
interface spec wins.

## Field by field

**`ask`**: Graham's own words, unedited. Do not clean it up or summarize it;
the raw ask is what later readers use to check this skill classified it
correctly.

**`kind`**: `measurable` or `judgment`. Ask: can I name a command, or an
observable Claude can surface in the transcript, whose output settles the
question with no interpretation? If yes, `measurable`. If the honest answer
requires a human or model to weigh several qualities against each other
(does this read well, is this a good tradeoff, is this design tasteful),
`judgment`. When in doubt, try to write the check first: failing to write
one that isn't circular ("a reviewer says it's good") is the signal it is
`judgment`.

**`end_state`**: one measurable end state for `measurable`; for `judgment`,
the rubric's pass line (the one sentence that says what passing the rubric
means, e.g. "every criterion in the rubric scores at or above 3 of 5").
Never two end states joined with "and": if the ask has two independent
conditions, that is a sign that the goal condition or the check are underspecified. See rubric-guide.md for the judgment case in full.

**`check`**: a command, or an observable Claude can surface verbatim in the
transcript. Per R-1, the `/goal` evaluator never runs commands itself; it
judges what Claude surfaced. That means the check's output must actually
appear in the transcript for `/goal` to see it: naming a command that
produces output nobody prints defeats the whole mechanism. Prefer a command
that fails loudly (non-zero exit, or a clearly wrong printed value) over one
that silently returns something ambiguous.

**`expected`**: the exact exit code or value that means the condition is
met. State it precisely enough that two different readers would agree
whether a given run passed. "Looks good" is not a value; "exit 0" and
"perf>=90 a11y>=90" are.

**`baseline`**: the check's output *before any work starts*, verbatim, with
the timestamp it was captured. This is recorded by actually running `check`
once, never by recalling a past run, never by estimating. If `check` cannot
be run yet (the target doesn't exist), that is a Stop-when condition in
SKILL.md, not a reason to leave `baseline` empty or guessed.

**`constraints`**: one item per thing that must not change while the work
happens. Keep these falsifiable ("no content changes to the hero copy") not
aspirational ("keep it looking nice").

**`budget`**: the turn or time clause in `/goal` wording, e.g. "stop after 3
attempts" or "stop after 10 minutes". Every goal block carries one; an
unbounded goal is an unbounded loop with a description.

**`human_gate`**: the one action that needs Graham, stated as an action
("deploying the fix branch to production"), or the literal string `none`
when nothing in the loop needs him.

**`rubric`**: present only when `kind: judgment`. A repo-relative path to
the rubric file (see rubric-guide.md). Omit the field entirely for
`measurable` goals; the check script in this skill treats it as the one
field allowed to be absent.

**`goal_condition`**: the single line derived from `end_state`, `check`,
`expected`, and `budget`, phrased so it could be pasted directly after
`/goal`. This is the field a reader checks first; get the other fields right
and this one falls out of them.

## Worked example (from the interface spec)

```yaml
goal_block: v1
ask: "get the homepage lighthouse scores up"
kind: measurable
end_state: all four Lighthouse category scores at or above 90 on https://gfmcloud.com/
check: npx lhci collect --url=https://gfmcloud.com/ && node scripts/lh-scores.js
expected: "perf>=90 a11y>=90 bp>=90 seo>=90"
baseline: "perf=71 a11y=88 bp=92 seo=100  (2026-09-11T14:02:11-05:00)"
constraints: [no content changes to the hero copy, no new third-party scripts]
budget: stop after 5 tries
human_gate: deploying the fix branch to production
goal_condition: "all four Lighthouse scores at or above 90 on gfmcloud.com per scripts/lh-scores.js, stop after 5 tries"
```

Note there is no `rubric` field here: this is a `measurable` goal.

## Common mistakes

- Writing a check that only a human can run ("look at the page and see if it
  feels fast"): that is a judgment ask wearing a measurable label. Reclassify
  it.
- Recording `baseline` from memory of a past run instead of a fresh one.
  Timestamps that don't match "now" are a tell.
- A `goal_condition` with no number in it. Every stop clause names a count
  or a duration; "stop when it seems done" is not a budget.
- Two goals bundled into one `end_state`. Split them into two goal blocks
  instead of joining them with "and."
