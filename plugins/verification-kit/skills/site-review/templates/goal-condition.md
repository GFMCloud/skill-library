# The `/goal` condition and the Goal block v1 it derives from

site-review is a `foundry-core:goal-spec` template: instead of asking
goal-spec to invent a check from scratch, this file supplies the check,
`expected`, and `goal_condition` fields already filled for the site-review
case. The shape itself (Goal block v1) is defined once, in the harness
interface spec (`docs/interface-spec.md`, section 1); this file does not
redefine it, only shows the site-review instance of it.

## Filled Goal block v1

```yaml
goal_block: v1
ask: "<the user's ask, unedited, e.g. 'review the gfmcloud.com homepage'>"
kind: measurable
end_state: all four Lighthouse category scores at or above 90 and zero broken links (linkinator) on <url>
check: |
  npx --yes lighthouse <url> --output=json --output-path=<out>/lighthouse.json --chrome-flags="--headless=new" &&
  npx --yes linkinator <url> --recurse --format=json > <out>/linkinator.json &&
  python3 scripts/score-table.py <out>/lighthouse.json <out>/linkinator.json
expected: "exit 0 (score-table.py's own contract: 0 means all four categories >= 90 and zero broken links)"
baseline: "<score-table.py's table output on the first run, verbatim, with the timestamp it was run>"
constraints: [no content changes to copy the site owner has not approved, no new third-party scripts added solely to chase a score]
budget: stop after 5 tries
human_gate: deploying any fix to production
goal_condition: "all four scores at or above 90 and linkinator reports zero broken, stop after 5 tries"
```

Note the `check` line composes three commands: Lighthouse, linkinator, and
the gate script that turns their two JSON files into the table and the exit
code `/goal`'s evaluator actually needs to see printed in the transcript (the
evaluator judges the transcript, never runs a command itself — R-1). The
`goal_condition` line is the one to paste after `/goal`; it is the roadmap
entry's fix-phase condition verbatim.

## The `/goal` invocation

```
/goal all four scores at or above 90 and linkinator reports zero broken, stop after 5 tries
```

Run this only after the baseline table has been printed once (so the
starting red rows are on record) and only against the fix branch, never
directly against production (`human_gate` above).

## Re-score with review-pair

Each attempt inside the `/goal` loop produces a new pair of Lighthouse and
linkinator JSON files and a new score-table.py run. Before treating an
attempt as the fix, hand its diff and this Goal block to
`verification-kit:review-pair` for an independent re-score. review-pair
returns a Verdict object v1 (interface spec section 3); apply the change only
on `result: pass`. This is the "review-pair re-scoring independently" step
in the roadmap entry — it is a second, independent check on the change, not a
replacement for score-table.py's own exit code.

## On budget exhaustion

If 5 attempts pass without meeting the condition, `bounded-loop`'s Stop hook
(if wired in) or the `/goal` loop itself produces an Escalation report v1
(interface spec section 2). Its `last_failing_output` field is the final
`score-table.py` run's verbatim output; its `likely_causes` should name the
specific red rows still failing, not a generic "performance is low." Never
paraphrase the table into the escalation — copy it.
