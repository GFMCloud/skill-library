# Designing Jev questions

Rules from Graham's lessons (2026-09-27, `jev-1.13.0`, native API), each with the evidence
behind it. Source for every number: `~/work/jev-lab/lab/LESSONS.md` and the
`lesson*-results.json` files beside it. Shape each question from these; read the official
`typesafe:typesafe-ai` skill for syntax.

## The three inputs

| Input | Job | Rule |
|---|---|---|
| state | the evidence, plus anything to compare it against | a JSON object with named fields; only what the questions need |
| instructions | the question | one narrow question; point at state fields with backticks (`` `item.claim` ``); may be an object with `question`, `focus`, `compare` |
| criteria | the yardstick | Choice options as what / not_for / examples; Score levels that describe situations; Noul `true` and `false` when the line is subtle |

Jev judges only against what these say. The question id is never sent to the model.

## Evidence rules

1. **Give Jev the records the decision is really made against, in full.** Lesson 5, the
   same two questions: the scanner's incumbent names only, 5 of 15 known `same` items
   routed covered; every working-agreement section and settled ruling in full, 10 of 15.
2. **A title is not a record.** The scanner named rules like `global rule "CLAUDE.md kept
   short"`; Jev had nothing to find a disagreement with (Lesson 5 v1).
3. **More text helps only when it holds the deciding fact.** Lesson 3: the whole handoff
   SKILL.md turned C-16 right; long CLAUDE.md sections gave changelog items more to
   "dispute" and pushed them to contradicts. Overall, fuller state scored 11 of 23 against
   15 for the short form.
4. **Check the plumbing.** A 200-character section filter silently dropped the one rule
   C-18 contradicted; with it restored, Jev matched both contradiction items to that rule
   (Lesson 5). Print the record count and spot-check that the expected records are there.
5. **Use each record as it stood when the past decision was made.** Two incumbents in the
   scout test set were added after the run that labelled them; using today's text would
   have leaked the answer (Lesson 3 builder, git at the recorded HEAD).
6. **Jev cannot fetch or reason a step further.** C-18's contradiction came from docs the
   orchestrator fetched; Jev, given the item and the rule, did not find it. Put any
   verification before Jev, in code or a stronger model.

## Question rules

1. **One question, one property the state can answer.** Lesson 3: `covers_job` mixed "same
   problem?" with "fully solved?", and the combine rule sent every `extends` item to `new`
   (9 of 23). Split, it held at 12 of 23 across six trials.
2. **A question whose values barely vary is measuring nothing.** `adds_mechanism` came
   back 0.5 to 0.89 for almost every item; `fully_solves` 0.07 to 0.33 for every item,
   `same` ones included. Drop or rewrite it; do not tune a threshold on it.
3. **Do not ask about intent the state does not hold.** "Would it change what gets
   built?" depends on Graham's plans; Jev answered yes to nearly everything.
4. **Define every option, including where it stops.** Lesson 2: undefined labels drew a
   confidently wrong class (every `same` came back `extends`, three at 0.96 and up).
   Adding not_for lines and a focus note turned those into low-confidence answers a gate
   can catch.
5. **An item describing a failure the reference exists to catch is not a contradiction.**
   Say so in the criteria (Lesson 2, C-63 "hooks fail silently" against prove-hooks).
6. **Records phrased as prohibitions attract false disputes.** S-2 ("this project never
   writes memory") drew three false contradiction flags (Lesson 5). Keep scope and
   ownership rules out of a dispute check.
7. **Choose the type by what code does with the answer.** Choice picks a branch, Score is
   compared to a threshold, Noul feeds an `if`. A Noul of 0.5 is a coin flip, not a
   medium amount.
8. **Escape options.** The docs advise an `other` or `none` on every Choice. Not measured
   here: in Lesson 1 `other` was offered and not chosen; the useful signal was the 0.24
   confidence.

## Reading the answers

- **Confidently wrong on a whole class:** the criteria draw a different line than the
  person who made the past decisions. Fix the definitions.
- **Unsure:** the evidence is thin or the case is borderline. Fix the state, or send the
  band to review.
- **Decomposed questions are steadier and easier to debug** than one broad Choice: 0 or 1
  label changes across three trials against 2 or 3 for the Choice (Lesson 3), and each
  failure shows up in one named question. They did not raise agreement on their own.

## Measuring

- Split tuning and held-out sets before writing the first question; hold the criteria's
  examples out of both.
- Report agreement with past decisions, never accuracy.
- Identical inputs moved by 3 items in 23 across runs (seven runs of one setup: 12 to 15).
  Rerun before believing a smaller difference.
- A revision tuned on a set is tested on items it never saw. The scout's held-out run was
  used once for a revision, so its v2 numbers are not a clean hold-out.
- Prove the fail-closed gate by deliberate failure with a fake client before a real run.
