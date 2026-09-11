---
name: smoke-gate
description: >-
  Generate a smoke-test script from an assertions manifest (identity, data freshness,
  live connections, key routes, zero console errors), prove each assertion category
  by poisoning it to a recorded exit 1, then run it live for a real exit 0 with a
  screenshot attached. Use before any "ready," "live," or "working" claim about an
  interactive artifact: a staging deploy, a war-room demo, a promote-to-production
  step. Not for a one-off manual check with no committed script, and not a substitute
  for `deploy-verify-fix`'s diagnose-and-fix loop: this only produces and proves the
  gate that loop's verify step should call.
metadata:
  maturity: incubator
---

# smoke-gate

A "ready" claim is worth nothing if the check that produced it never demonstrably
fails. This skill turns a Smoke manifest v1 into a committed smoke script, proves
each assertion category can independently fail (poisoned, exit 1) before trusting
any of it, then runs the unpoisoned script live for the exit-0 evidence a "ready"
claim needs.

See [templates/manifest.md](templates/manifest.md) for the manifest shape and the
wiring notes the generator needs beyond the shape itself (connection addresses are
resolved from environment variables, not manifest fields, because the shape carries
only a connection's name). See
[references/webapp-testing-intake.md](references/webapp-testing-intake.md) for what
was reused from Anthropic's `webapp-testing` skill and what was not.

## Inputs

- A Smoke manifest v1 (toolkit interface spec section 5): `target` and five
  assertion categories (`identity`, `freshness`, `connections`, `routes`,
  `console`), each with a matching `poison` entry. The generator refuses to emit a
  script for any category missing a `poison` entry, exit 1, naming the category, see
  "Verify".
- For each `connections` entry, an address to check at run time
  (`SMOKE_CONN_HOST_<NAME>` / `SMOKE_CONN_PORT_<NAME>`; see the template's wiring
  notes). Nothing else is required before generation; the address is only needed to
  run the generated script.

## Verify

1. Generate the script:
   `scripts/generate-smoke-script.py <manifest.yaml> <out.sh>`.
2. Check poison coverage before trusting any run of it:
   `scripts/check-poison-coverage.py <manifest.yaml>`. Exit 0 means every category
   has a poison entry; exit 3 lists which categories are unproven, one line each
   (`UNPROVEN <category>: no poison entry`). An unproven category is never reported
   as passed, in the run log or anywhere else, see
   `fixtures/manifest-missing-poison.FIXTURE.yaml` for the poisoned proof of this
   rule itself.
3. Prove the script, one category at a time: run it once per category with that
   category's poison override active (see the environment-variable table in
   `scripts/generate-smoke-script.py`'s docstring) and everything else at its
   passing default. Each run must exit 1 and name the poisoned category in its
   `SMOKE FAIL: <categories>` line. Five categories, five recorded exit-1 runs,
   captured verbatim.
4. Run the script with no overrides against the real target. This is the live pass:
   it must exit 0, and its full output plus one screenshot are attached to the
   run log. Take the screenshot with the Browser tool or Playwright when either is
   available; when neither is (a headless CI run, a fixture target with no browser
   in front of it), the run log says `screenshot: not available` and states why,
   rather than skipping the line.

Known weakness: the generated script's `console` check is a text-marker grep, not a
real DevTools console read (see `references/webapp-testing-intake.md`). It proves
the *category can fail and pass on command*, not that a real browser saw zero
console errors: that stronger claim needs the Browser tool or Playwright wired to
the actual check, which this skill's generic script does not embed by design (a
committed script should not require a Playwright runtime everywhere it runs).

Offline proof for this skill's own gate:
`bash fixtures/run-fixture-proof.FIXTURE.sh` (script-relative paths, runs from any
directory). It starts a local fixture target (`fixtures/fixture_server.py`),
generates a script from `fixtures/manifest.FIXTURE.yaml`, runs steps 2-4 above
against it, and also runs `check-poison-coverage.py` against
`fixtures/manifest-missing-poison.FIXTURE.yaml` to prove the unproven-category
report. See the build report for its captured output.

## Done when

The live pass exits 0 with its output and a screenshot (or a stated reason none is
available) attached, and every assertion category in the manifest has a poison run
recorded with exit 1 in the same run log, on the same script, against the same
target. A live exit 0 with fewer poison categories proven than the manifest declares
is not done; it is an unproven pass.

## Stop when

- **Any assertion is red on the live pass.** Do not report "ready." Hand the run log
  and the manifest to `foundry-core:bounded-loop` as the failing check for its
  budgeted retry loop, or straight to a human if there is no budget configured.
- **A category has no poison entry.** `check-poison-coverage.py` exits 3: report
  that category as unproven in the run log, fill in its poison entry, and re-run
  before calling anything green. Never treat an unproven category as a pass because
  the others went green.
- **The connection address for a `connections` entry is not set.** The generated
  script fails fast with `set SMOKE_CONN_HOST_<NAME>...` rather than silently
  skipping the check; supply it and re-run, do not treat the parameter error as a
  category result.
- **No target is reachable at all** (DNS, auth, or the launch command itself fails
  before any assertion runs). This is not a red assertion, it is a setup failure:
  say so distinctly in the run log so a human does not read it as "the app is
  broken" when it may be "the check never started."

## Output contract

Produces: a smoke script generated from the Smoke manifest v1 (committed to the
calling project, not to this skill directory), a run log containing the five
poisoned exit-1 results and the one live exit-0 result with its verbatim output, and
one screenshot from the live pass (or a stated absence).

Consumes: a Smoke manifest v1 as defined in the toolkit interface spec, section 5.

On a red live pass, this skill's run log becomes the `last_failing_output` carried
by `foundry-core:bounded-loop`'s Escalation report v1, as defined in the harness
interface spec, section 2: smoke-gate feeds bounded-loop's loop, it does not
produce the report. The failing assertion category becomes the one-line basis for
`likely_causes`, and `cause_class` is set per bounded-loop's own rules
(`ambiguous_check_feedback` for a genuinely unclear assertion failure,
`unreachable_condition` when the target itself could not be reached). smoke-gate
does not redefine the Escalation report shape; it only supplies the fields
bounded-loop's contract asks a failing check to supply.

For the staging-to-production promote flow, smoke-gate composes with
`deploy-ops:deploy-verify-fix`: that skill's "Verify at the level the failure
lives" step is exactly this skill's live pass, and its "diagnose from real output"
step reads this skill's run log rather than re-deriving a new check.

## Optional Stop hook

The generated smoke script can optionally be installed as a Stop hook, so a "ready"
claim cannot end the turn while smoke is red. This is optional, not required by
"Done when," and not proven by a fixture in this build. See
[references/stop-hook.md](references/stop-hook.md) for the event, the
`settings.json` shape, the command, and the exit-2-with-stderr blocking path, sourced
from `foundry-core:bounded-loop`'s stop-hook contract reference.
