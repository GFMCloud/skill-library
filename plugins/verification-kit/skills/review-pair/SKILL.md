---
name: "review-pair"
description: >-
  Get an independent pass/fail verdict on a change spec or diff before it is applied to
  something that matters, using a reviewer subagent that never sees the builder's
  conversation. Use before applying any change spec produced by a bounded loop or a
  goal-driven session, whenever the target is a real file, a real deploy, or anything
  where a wrong apply costs a rework cycle. Not for a plain code-review request with no
  goal block behind it, and not a substitute for pre-delivery-verifier: that agent checks
  a finished artifact against acceptance criteria after the fact; this skill gates one
  proposed change before it lands, against the goal it is supposed to satisfy.
metadata:
  maturity: incubator
---

# review-pair

Wraps a read-only subagent as the independence mechanism for a builder/reviewer split.
The reviewer never gets the builder's conversation, reasoning, or prompt: a non-fork
subagent's initial context has no parent history by construction, and this skill takes
that as the model for reviewer independence rather than trying to enforce blindness by
instruction (research row R-4). Shared context is what makes a second opinion restate
the first one.

See [references/reviewer-agent.md](references/reviewer-agent.md) for the subagent
definition to drop into a project's `.claude/agents/`, and
[references/verdict.md](references/verdict.md) for how to fill out the Verdict object
the reviewer returns.

## Inputs

- A Goal block v1 (interface spec section 1) for the change under review: the ask, the
  end state, the check, and the constraints. The reviewer scores the change against this,
  not against its own idea of good code.
- The change spec or diff to review: a patch, a file list with contents, or a described
  set of edits not yet applied.
- The target: the path, repo, or resource the change would land on.
- Nothing else. The reviewer gets exactly the goal block and the change; not the
  builder's transcript, prompt, or reasoning. This is the rule the toolkit itself was
  reviewed under: reviewers receive the interface spec and the skill directory only.

## Verify

Run [scripts/verdict-check.sh](scripts/verdict-check.sh) against the reviewer's output
file. It checks that the Verdict object v1 is well-formed (every required field
present, `result` in `{pass, fail}`, `severity` in the allowed set, `confidence` in
`0..1`, `issues` empty iff `result: pass`, `new_information` a boolean) and, given a
pair of verdict files from two review rounds on the same target, applies the hold rule:
a second `fail` whose `new_information` is `false` is a repeat fail, and the script
prints `HOLD` and exits 2. A verdict object that fails this check is not a review
result; it is a malformed reviewer output and the apply does not proceed on it either
way.

Known weakness: the script validates shape and the hold rule. It cannot check that the
reviewer actually looked at the change rather than rubber-stamping it; that is what the
subagent's `permissionMode: plan` (or read-only `tools` list), independent model, and
lack of parent history are for, not the validator.

## Done when

A `pass` verdict exists for the change, the verdict object is written to the run log
before the apply happens, and the change has been applied. One clean pass verdict from
an independent reviewer is sufficient; do not seek a second opinion after a pass.

## Stop when

- Two `fail` verdicts have been returned for the same target and the second cites no
  new information (`new_information: false`): hold the change and queue it for Graham.
  Do not attempt a third builder pass without his ruling.
- The goal block is missing or incomplete: nothing runs until every field except
  `rubric` is filled, per Goal block v1's own rule. Ask for the missing field rather
  than reviewing against a guess.
- The reviewer's output cannot be parsed as a Verdict object v1: report the malformed
  output verbatim and stop. A malformed verdict is not a pass by default.
- A reviewer model cannot be reached, or no model differing from the builder's is
  configured: stop and say so. Running the reviewer on the same model as the builder
  defeats the independence mechanism this skill exists to provide (research: shared
  context and self-preference bias both survive same-model review).

## Procedure

1. Confirm the Goal block v1 and the change spec are both in hand. If either is
   missing, stop per "Stop when" above.
2. Spawn the reviewer using the subagent definition in
   [references/reviewer-agent.md](references/reviewer-agent.md): `permissionMode: plan`
   (or an equivalent read-only `tools` list), `maxTurns` set to a small bound, and
   `model` set to a value that differs from the model that produced the change. Pass it
   only the goal block and the change; nothing about how the change was produced.
3. The reviewer returns a Verdict object v1 (interface spec section 3). Write it to the
   run log before doing anything else with it.
4. Run `scripts/verdict-check.sh` against the verdict file. On a script failure, treat
   the verdict as malformed and stop.
5. On `result: pass`, apply the change. Nothing else is required.
6. On `result: fail`, hand the builder the `issues` list and one more attempt, per
   `bounded-loop`'s budget for this stage. Have the reviewer produce a second verdict
   against the revised change, setting `new_information` by comparing what it cites
   against the first verdict's `issues`.
7. Run `scripts/verdict-check.sh` against both verdict files together (first, second).
   If it prints `HOLD`, stop per "Stop when": hold the target and queue it for Graham.
   Otherwise treat the second verdict the same as step 5 or 6.

## Output contract

Produces a Verdict object v1 as defined in `docs/toolkit-interface-spec.md` section 3. Consumes
a Goal block v1 as defined in `docs/toolkit-interface-spec.md` section 1. Field lists live only
in the interface spec; this skill and its references cite them by name and version.
