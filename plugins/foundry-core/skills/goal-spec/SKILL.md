---
name: goal-spec
description: >-
  Turn an open-ended ask into a Goal block v1 before any unattended or
  `/goal`-driven work starts: classify the ask as measurable or judgment,
  name a runnable check or a criterion-separated rubric, record the baseline
  by running the check once, and name the human gate. Use for any ask that
  would otherwise start with "improve," "review," "clean up," "optimize," or
  "make better," and for anything about to run under `/goal` or a bounded
  loop. Refuses and asks one question when no check can be named and no
  rubric fits. Not for asks that already carry a concrete, verifiable
  end state; those can go straight to `/goal` without this skill's overhead.
metadata:
  maturity: incubator
---

# goal-spec

Every unattended or `/goal`-driven task needs one thing before it starts: a
condition someone (or something) can check without asking the author what
they meant. This skill turns an ask in Graham's own words into that
condition, or refuses to start until one exists.

See [references/goal-block.md](references/goal-block.md) for how to fill
each field of the Goal block, with the worked example from the interface
spec. See [references/rubric-guide.md](references/rubric-guide.md) for how
to write a criterion-separated rubric when the ask is judgment, not
measurable.

## Inputs

- The ask, in Graham's own words, unedited.
- The artifact or system the ask targets (a file, a URL, a repo, a running
  service), enough to actually run a check against it.
- Nothing else. This skill does not need a budget or a human gate supplied
  up front; it derives sensible defaults and states them for confirmation.

## Verify

Run [scripts/goal-block-check.sh](scripts/goal-block-check.sh) against the
goal block file this skill wrote. The script itself does not depend on cwd
(it only reads the path given as its argument), but that argument, and the
`scripts/` prefix, are both relative, so state the skill's own directory with
a `cd` line first:

```bash
cd /Users/gfm/skill-library/plugins/foundry-core/skills/goal-spec
scripts/goal-block-check.sh fixtures/goal-block-complete.FIXTURE.yaml
```

Once this skill is installed as a plugin, use the installed copy's own
directory instead of the source path above: read `installPath` for
`foundry-core@skill-library` out of `~/.claude/plugins/installed_plugins.json`,
never construct it, then cd into that installPath's own `skills/goal-spec`
directory before running the same command.

Pass means: every field is filled except `rubric` (which is required only
when `kind: judgment` and absent otherwise), `baseline` is non-empty, and
`goal_condition` contains a recognizable stop clause (a turn count or a time
bound). Exit 0 is pass; exit 1 is fail, with the missing or malformed field
named on stderr.

For a judgment goal block, `Verify` additionally means: the rubric file
named in `rubric` exists, and its criteria are each scored independently
(see [references/rubric-guide.md](references/rubric-guide.md) for the shape
the check does not itself parse deeply: the script checks the field is
filled and points at a real file, not that the rubric is well-formed).

This Verify section (the runnable block above and the surrounding prose) was
checked with `turn-reduction`'s `output-lint` before this skill was proposed
for promotion. Running the command above against the passing fixture prints:

```
$ cd /Users/gfm/skill-library/plugins/foundry-core/skills/goal-spec
$ scripts/goal-block-check.sh fixtures/goal-block-complete.FIXTURE.yaml
PASS: fixtures/goal-block-complete.FIXTURE.yaml is a complete Goal block v1
```

exit 0.

## Done when

A Goal block v1 (interface spec section 1) exists with every field but
`rubric` filled, `baseline` recorded from an actual run of `check` (never
recalled or guessed), and `goal_condition` phrased as a single line that
could be pasted after `/goal`. For a judgment ask, a criterion-separated
rubric file exists at the path named in `rubric`, each criterion scored
independently, never collapsed into one holistic number.

## Stop when

- **No check can be named and no rubric fits.** The ask has no observable
  end state and no criteria that could be scored independently (example:
  "make the README nicer, no criteria, do not ask me"). Refuse to produce a
  goal block. Ask exactly one question that would unblock either path (a
  measurable check or a rubric criterion) and stop. Never invent a check or
  a rubric to avoid asking.
- **The budget clause is missing and Graham has not stated one.** Propose the
  library default (3 attempts, per `bounded_loop_default_budget` in
  toolkit-build-harness's `CONFIG.md` when that harness is in play, else "stop
  after 3 attempts") and ask for a one-word confirm rather than guessing
  silently: this is the one field this skill is allowed to default instead
  of refuse on, because a sane default exists and an unbounded loop does not.
- **The check cannot actually be run** (the target doesn't exist yet, the
  command errors for reasons unrelated to the goal). Say so, name the exact
  command that failed and its output, and stop rather than record a
  fabricated baseline.
- Done (a complete Goal block v1, baseline recorded, ready to hand to
  `/goal` or `bounded-loop`).

## Output contract

Emits a Goal block v1 as defined in the harness interface spec
(`docs/interface-spec.md`, section 1). This skill never redefines that
shape's fields; see [references/goal-block.md](references/goal-block.md) for
guidance on filling each one and the worked example from the spec.

Known weakness: the check script validates that fields are filled and that
`goal_condition` contains a stop-clause-shaped substring (a digit followed by
a time/attempt word). It cannot judge whether the check named is actually
the right check for the ask, or whether a rubric's criteria are genuinely
independent rather than restated versions of each other: that judgment is
this skill's job at authoring time and a human reviewer's job at promotion,
not the script's.
