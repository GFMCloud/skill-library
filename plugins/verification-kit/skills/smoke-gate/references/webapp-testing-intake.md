# Intake: Anthropic's `webapp-testing` skill

Orchestrator substitution (harness anomaly A10, `STATE.md`): the roadmap step reads
"First run `source-intake` on Anthropic's `webapp-testing` skill." That skill was not
run; instead this builder fetched the upstream `SKILL.md` directly and read it. This
file is that intake, in the shape the substitution asked for: what machinery it
offers, what was reused as a pattern (with citation), what was not, and why.

Source fetched: `https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md`
(research record row R-12 confirms the path; contents were not read there). The
fetch succeeded. Its `scripts/` directory was also listed
(`https://api.github.com/repos/anthropics/skills/contents/skills/webapp-testing/scripts`)
and contains exactly one file, `with_server.py`.

## What it offers

- **Server lifecycle management**: `with_server.py` starts one or more dev servers
  (backend and frontend together, when both are needed) before running an automation
  script against them, and tears them down afterward. This is the piece the roadmap
  step names explicitly ("reuse its server-lifecycle... machinery if it fits").
- **Browser automation via Playwright**: programmatic clicking, typing, and
  navigation against a running local web app, driven from Python.
- **Screenshot and DOM inspection**: capturing the rendered page and reading its
  structure for debugging, plus browser console log capture.
- **A stated workflow discipline**: "reconnaissance then action", wait for network
  idle, screenshot and inspect the DOM, identify selectors, only then interact. This
  is a practice, not a mechanism; it is not something this skill's generated bash
  script needs to reuse, since the generated script never drives a browser.
- Reference examples covering element discovery and running against static
  `file://` HTML.

## What smoke-gate reused, and how

- **The server-lifecycle pattern**, not the code. `scripts/generate-smoke-script.py`
  and the fixture proof follow the same shape `with_server.py` uses: start the
  target process, wait for it to announce readiness, run checks against it, always
  tear it down, implemented independently in
  [../fixtures/run-fixture-proof.FIXTURE.sh](../fixtures/run-fixture-proof.FIXTURE.sh)
  and [../fixtures/fixture_server.py](../fixtures/fixture_server.py). No code from
  `with_server.py` was copied into this repository; the library's own guardrail
  ("Do not copy its scripts into the library; reference by URL") plus this project's
  house rule (compose first-party primitives, do not re-implement them, and do not
  duplicate an existing implementation) both point the same way: name the pattern,
  do not vendor it.
- **The "verify at the level the failure lives" idea** behind reconnaissance-then-
  action lines up with this skill's own rule that a live pass must attach a real
  screenshot, not a claim that the page loaded.

## What smoke-gate did not reuse, and why

- **Playwright-driven browser automation.** The `console` assertion category in a
  real deployment needs a real browser's DevTools console, which only Playwright or
  the Browser tool can read. smoke-gate's generated script does not embed a browser
  automation stack; it is a thin, dependency-free bash script (curl and `/dev/tcp`)
  meant to be committed to an arbitrary project and run in CI or a Stop hook where a
  Playwright runtime cannot be assumed. `SKILL.md`'s "Verify" section states this
  gap explicitly: the fixture's `console` check is a text-marker stand-in, and a real
  console-error count is out of the fixture's reach and out of the generated script's
  reach too; that step is left to whichever caller has Playwright or the Browser
  tool available, per the roadmap step's own text ("capture a screenshot" via the
  live pass, not via the generated script).
- **The static-`file://`-URL example and element-discovery examples.** Not relevant
  to a target that is a running URL or launch command, which is what the Smoke
  manifest v1 shape assumes (`target: <url, or the launch command that yields one>`).

## If the fetch had failed

It did not; both fetches (`SKILL.md` and the `scripts/` listing) succeeded and are
reported above. Had `SKILL.md` been unreachable, this skill would have proceeded
without it per the harness instruction, noting the failure here and in the build
report, and would have relied on the generic reconnaissance-then-action practice
already documented in `foundry-core:proof-of-work` instead.
