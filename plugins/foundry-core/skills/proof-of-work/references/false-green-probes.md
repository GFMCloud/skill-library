# False-green probes

Three questions to ask of any check before its green result is reported as evidence,
plus one about where the expected answer came from. Each names a way a check exits 0
while checking nothing. Harvested from the silent-failure-catalog review (2026-09-21,
`maintainers/reviews/2026-09-21-silent-failure-catalog.md`) and a 2026-09-28 post on
proving tests can fail; the smoke-gate false green that review reproduced (`SMOKE PASS`
with zero assertions, and with the target unreachable) is the local case.

## 1. Count the check's output states

A check that can only ever print one thing is not a check. Before trusting it, list the
distinct outcomes it has produced in its history, or make it produce a second one on
purpose. A validator that has never been seen red, a smoke run whose assertion list is
empty, a test runner that reports "ran" on an exit code of 0 from a command that ran no
tests: each has one output state. Proof-of-work's `scripts/run-checks.sh` fails a tests
phase that collected zero tests for this reason, and its fixture proof makes it do so.

## 2. Could this evidence be true while the claim is false?

Take the claim and the evidence as two separate sentences, and look for a world in which
the second holds and the first does not. "The build printed Success" is true in a world
where the output file is empty. "The deploy pipeline is green" is true in a world where
the deployed endpoint returns the previous version. "No errors in the log" is true when
the log was truncated before the error. When such a world exists, the check ran at the
wrong level (see "Verify at the level the failure lives"), and a second check at the right
level is needed before the claim is made.

## 3. A metric close to the request count measures exposure, not usage

A number that rises with every request (a counter incremented on entry, a log line per
call, a "loaded" flag) says the code path was reached, not that it did its job. A metric
that is almost equal to the request count is a candidate for this: it is counting
attempts. Ask what would differ between the metric when the feature works and when it is
silently broken; if the answer is nothing, find or add the metric that would differ.

## 4. Where did the expected answer come from?

Beyond a passing test, show one plausible broken implementation the test rejects, and say
where the expected value came from: a hand calculation, an independent tool, a fixture
with a known answer, or the same code that is under test (which proves only that the code
agrees with itself). A test whose oracle was copied from the first run's output passes
by construction. Record the oracle's provenance beside the test in the evidence report;
"expected: from the implementation's own output" is a finding, not a pass.
