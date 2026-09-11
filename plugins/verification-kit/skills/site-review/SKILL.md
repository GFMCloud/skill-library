---
name: site-review
description: >-
  Score a live site or web tool on Lighthouse performance, accessibility,
  best practices, and SEO (target 90 each); check for zero broken links with
  linkinator on the live crawl; capture 375px-viewport and dark-theme
  screenshots; and run a criterion-separated content checklist. Emits a
  before/after scored table and a prioritized fix list, then runs the fix
  phase under `/goal` with review-pair re-scoring each attempt. Use for any
  review of a live site or web tool, on phrases like "review this site",
  "check the site's Lighthouse scores", "find broken links on", or "is this
  site ready". Not for a design-only critique with no live URL (that has no
  check to run), and not a substitute for a real Core Web Vitals or WCAG
  audit; see the labels in `## Output contract`.
metadata:
  maturity: incubator
---

# site-review

A `foundry-core:goal-spec` template for one specific, recurring ask: is this
live site or web tool actually in good shape. It fills the Goal block v1's
`check`, `expected`, and `goal_condition` fields with the Lighthouse and
linkinator commands below (see
[templates/goal-condition.md](templates/goal-condition.md)) instead of
deriving them from scratch each time, and it supplies the one part `/goal`
and goal-spec cannot: a criterion-separated content checklist for the parts
no CLI tool scores (see [references/rubric.md](references/rubric.md)).

## Inputs

- A URL for the live site or tool. site-review scores the deployed,
  rendered site, never a local build or a static export. Lighthouse and
  linkinator both need a real HTTP response (linkinator specifically crawls
  a live rendered site; a file-based alternative like `lychee` is not what
  this skill wraps, see [references/rubric.md](references/rubric.md)'s
  sibling note in the interface spec's composition map).
- Optional: content checklist additions beyond the default rows in
  [references/rubric.md](references/rubric.md).
- Nothing else required to start the first (baseline) scoring pass. The fix
  phase additionally needs a fix branch to work on and Graham's confirmation
  before anything is deployed (see `human_gate` in
  [templates/goal-condition.md](templates/goal-condition.md)).

## Verify

Run the three commands from [templates/goal-condition.md](templates/goal-condition.md)
against the target URL, then the gate script against their two JSON outputs:

```bash
npx --yes lighthouse <url> --output=json --output-path=<out>/lighthouse.json --chrome-flags="--headless=new"
npx --yes linkinator <url> --recurse --format=json > <out>/linkinator.json
python3 scripts/score-table.py <out>/lighthouse.json <out>/linkinator.json
```

`score-table.py` exits 0 when all four Lighthouse categories score at or
above 90 and linkinator reports zero broken links, 1 otherwise (see the
script's own docstring for the exact field paths it reads:
`categories.<id>.score` and `links[].state`). This exit code is what the
`/goal` condition in [templates/goal-condition.md](templates/goal-condition.md)
checks for; see that file for the full Goal block v1.

For the 375px-viewport and dark-theme passes, run Lighthouse a second time
with device emulation and a forced dark color scheme, and capture a
screenshot of both:

```bash
npx --yes lighthouse <url> --output=json --output-path=<out>/lighthouse-375.json \
  --chrome-flags="--headless=new --force-dark-mode --enable-features=WebContentsForceDark" \
  --screenEmulation.mobile --screenEmulation.width=375 --screenEmulation.height=812 \
  --screenEmulation.deviceScaleFactor=2 --emulated-form-factor=mobile
```

Known weakness: Lighthouse has no first-class "dark theme" audit. The
`--force-dark-mode` Chrome flags are a best-effort proxy for
`prefers-color-scheme: dark`, not an official Lighthouse feature, so treat
this run's screenshot (not its category scores) as the actual dark-theme
evidence; the scores from this pass are informational, not part of the
`/goal` condition, which is scored from the default-viewport run only.

Run [references/rubric.md](references/rubric.md)'s content checklist against
the rendered site at both viewports, scoring each row independently.

**Tool presence, checked on this machine before this build (not run against
any live site in this build):**

```
$ npx --no-install lighthouse --version
npm error npx canceled due to missing packages and no YES option: ["lighthouse@13.4.1"]
exit 1

$ npx --no-install linkinator --version
npm error npx canceled due to missing packages and no YES option: ["linkinator@8.1.0"]
exit 1
```

Neither package is cached locally as of this build. The `npx --yes` commands
above will download them on first real use; that first run needs network
access and is not something this skill pre-installs globally, per the
harness guardrail against installing these tools machine-wide.

## Done when

The scored table shows all four Lighthouse categories at or above 90 and
linkinator reports zero broken links on the target URL, both 375px-viewport
and dark-theme screenshots have been captured and reviewed, and every row of
the content checklist (`references/rubric.md`, plus any additions named in
Inputs) is PASS. The report contains a before table, an after table, and a
fix list with a status per item (roadmap entry, "Output").

## Stop when

- **Budget exhausted.** Five `/goal` attempts complete without meeting the
  condition: stop, do not attempt a sixth, and produce an Escalation report
  v1 (interface spec section 2) naming the specific rows still red, never
  a generic "performance is low" (roadmap entry, "Failure").
- **The URL does not resolve, or Lighthouse/linkinator cannot reach it.**
  Report the exact command and its error, and stop rather than guessing at
  scores or fabricating a baseline.
- **review-pair returns two `fail` verdicts with no new information** on the
  same fix attempt: hold the change per review-pair's own Stop-when rule and
  queue it for Graham, rather than spending remaining budget on a third
  attempt.
- Done (all four scores at or above 90, zero broken links, checklist
  complete, screenshots attached).

## Output contract

Consumes a Goal block v1 as defined in the harness interface spec
(`docs/interface-spec.md`, section 1); fills it per
[templates/goal-condition.md](templates/goal-condition.md) and hands it to
`/goal` for the fix phase.

Consumes a Verdict object v1 as defined in the harness interface spec,
section 3, from `verification-kit:review-pair`'s independent re-score of
each fix attempt; applies a fix only on `result: pass`.

On budget exhaustion, site-review is escalated by
`foundry-core:bounded-loop`'s Escalation report v1 as defined in the harness
interface spec, section 2, not by producing one itself: `last_failing_output`
is the final `score-table.py` run's verbatim output and `likely_causes` names
the specific red rows, not a paraphrase.

Field lists for all three shapes live only in the interface spec; this
skill and its references cite them by name and version and never redefine
them.

**Mandatory labels, printed with every scored table** (roadmap entry,
"Output"), and reproduced verbatim by `score-table.py`:

- The performance score is a lab proxy and does not certify Core Web Vitals
  or INP.
- The accessibility score is an automatable-issue floor, not WCAG
  compliance. (axe-core-class checks catch roughly the automatable third to
  half of WCAG issues; research record, secondary findings, T6.)

## First use

Per the roadmap entry: gfmcloud.com homepage first, then the SCL site. Both
runs are live-site reviews and are out of scope for this build (Phase 3
builds the skill; it does not execute a review against a real site).
