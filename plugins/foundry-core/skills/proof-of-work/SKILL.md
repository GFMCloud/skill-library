---
name: "proof-of-work"
description: "Produce executed evidence that a piece of work actually works before presenting it as done — run the code against representative data, inspect the render, print the validation output. Use before declaring any artifact complete, and whenever a tool reports its own success."
metadata:
  maturity: stable
  version: 1.0.0
  reviewed: 2026-08-09
---

# proof-of-work

The evidence standard. `evidence-report` is how the evidence gets written up;
this is what qualifies as evidence in the first place.

## The standard

An artifact is not done because it looks done. It is done when there is
executed evidence attached.

- **Run the thing.** Grep, lint, type-check, and self-review do not count as
  verification where the failure mode can hide from them. They are pre-filters.
- **State what was run, against what input, and what came back.** All three. A
  result with no input named is not reproducible.
- **Verify at the level the failure lives.** A check that structurally cannot
  see the defect is not a check, however green it comes back.

## A success message is not evidence

Where a tool reports its own outcome, confirm the outcome independently by
inspecting what it claims to have produced. Three logged instances, all in this
project's own tooling, all found by testing rather than by reading:

1. `anthropics/claude-code` issue #53948 — plugin install creates an empty
   `skills/` cache directory and reports success anyway. Regression in
   v2.1.117, closed as not planned.
2. `claude plugin marketplace update` reported success on a manifest whose
   plugin sources could not resolve at install.
3. `claude plugin validate` at a marketplace root reported "Validation passed"
   while an agent's frontmatter was unparseable — the root check never
   descended to the plugin directory where the defect was. That agent would
   have loaded with empty metadata: inert, not erroring.

Instance 3 is the one worth internalising. The check passed *because* it was
run at the wrong level, and a passing check at the wrong level is more
dangerous than no check at all — it converts an unknown into a false known.

## What counts, by artifact class

- **Code** — executed against representative input, output inspected. Not a
  test that asserts the function was called.
- **Document** — the claims extracted and checked against the artifact they
  describe (`consistency-checker:spec-artifact-diff`). Reading it again is not
  a check.
- **Deployment** — the deployed thing exercised at its real endpoint. A green
  pipeline is a claim about the pipeline.
- **Data** — row counts in and out, and the rejects examined. A job that
  reports success having silently dropped 12% is the standard failure.
- **Config and manifests** — installed or loaded somewhere real, and a
  component invoked. Validation is necessary, not sufficient.

## When evidence cannot be produced

Say so, in those words, and put it in the not-verified list. Do not substitute
reasoning about why it probably works.

Before routing a check to a human, establish that you genuinely cannot run it
yourself — most historically were runnable by the executor. Where one truly
is not, hand over the exact command to paste rather than a description of what
to do.

## Pairs with

- `evidence-report` (`foundry-core`) — the report format, including the
  mandatory not-verified list.
- `verification-kit:pre-delivery-verifier` — runs this standard over an
  artifact before delivery, and cannot repair what it finds.
