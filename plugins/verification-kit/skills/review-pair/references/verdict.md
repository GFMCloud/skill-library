# Filling out Verdict object v1

The shape, its field list, and every field's allowed values are defined once: the
harness interface spec, section 3, "Verdict object v1"
(`/Users/gfm/work/toolkit-build-harness/docs/interface-spec.md`, or, once this spec is
published with the library, wherever this skill's SKILL.md says it lives). This file
is guidance on how to fill the shape, not a second definition; if the two ever
disagree, the interface spec wins and this file is stale.

## The example, reproduced from the spec for convenience

```yaml
verdict: v1
target: plugins/foundry-core/skills/goal-spec
result: fail
severity: medium
confidence: 0.8
issues:
  - id: 1
    where: SKILL.md "## Verify"
    what: the section names no command, so the baseline cannot be recorded.
    evidence: /usr/bin/grep -c 'baseline' SKILL.md → 0
new_information: false
```

## The rubric line every reviewer receives verbatim

**Explanation length is not a quality signal.**

State it to the reviewer exactly this way, not paraphrased, because paraphrase drifts
toward "be thorough," which is the opposite instruction. A one-sentence `what` per
issue, with one piece of `evidence`, beats a paragraph. A reviewer padding its verdict
to look careful is doing the thing this line exists to prevent.

## Field-by-field notes

These say how to choose a value, not what the set of allowed values is; read the
allowed values from the spec.

- **`target`**: a path or change id, not a description. If reviewing a diff that spans
  several files, name the directory or the change id the diff is filed under, and let
  individual `issues.where` entries carry the file:line detail.
- **`result`**: there is no "pass with reservations". A reservation worth recording
  either blocks the apply, or it does not; if it does not block the apply, it belongs
  in the reviewer's reply text, not stuffed into a contradiction of the shape (`issues`
  must stay empty on a passing verdict).
- **`severity`**: on a failing verdict, pick the value that would make Graham triage
  this before or after other queued work. Do not default to the middle value because
  it feels safe; reserve the top value for a failing verdict, not for uncertainty.
- **`confidence`**: the reviewer's own confidence in the verdict, not in the change.
  A reviewer that ran the check and saw it fail sits near the top of the range. A
  reviewer inferring from a description of a check it could not run should say so, in
  `issues`, and keep confidence low.
- **`issues`**: empty exactly when the verdict passes. Each issue needs `evidence`: a
  command and its output, or a quote under 15 words. `evidence` is not optional: an
  issue with no evidence is an opinion, and this rubric is explicitly not scoring
  opinions.
- **`new_information`**: false on a first review of a target. On a second review (the
  one-more-attempt case in `review-pair`'s procedure), the reviewer compares its new
  `issues` against the first verdict's `issues` and sets this true only if at least one
  new issue cites something the first verdict did not raise. A second failing verdict
  that re-states the first verdict's issues in different words carries no new
  information: that is exactly the repeat-fail case the hold rule exists to catch.

## Common ways to get this wrong

- Writing a holistic score instead of `pass`/`fail` plus `severity`. The spec has no
  numeric overall score; do not invent one.
- Leaving `issues` non-empty on a `pass` because the reviewer wants to note something
  minor. Move it to reply text, or change the verdict to `fail` with `severity: low`
  if it is genuinely blocking; do not violate "empty iff pass" to save a sentence.
- Setting `new_information: true` because the second review restates the same finding
  more forcefully. New information means a fact the first verdict did not have, not a
  stronger opinion about a fact it already had.
- Treating a long `what` as more rigorous review. It is not; see the rubric line above.
