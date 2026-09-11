# Filling out Escalation report v1

The shape and its fields are defined once, in `docs/interface-spec.md` section 2
(Escalation report v1) in the harness that built this skill; this page never
redefines a field. `stop-hook-verify.sh` writes the file; this page is how a
reader (human or agent) checks that what it wrote is right, and how to fill
the two fields the script cannot compute for you.

The spec's own example (quoted verbatim, for reference; the field list lives
in the spec, not here):

```yaml
escalation: v1
goal_block: runs/goal-2026-09-11.yaml
attempts: 3 of 3
last_failing_output: |
  FAIL tests/test_parse.py::test_empty_header - AssertionError: expected 0 got 1
tried:
  - {attempt: 1, diff_hash: 4f1c2a9, summary: strip header before count}
  - {attempt: 2, diff_hash: 88be013, summary: guard on zero-length input}
  - {attempt: 3, diff_hash: c0ffee1, summary: move guard above the split}
cause_class: ambiguous_check_feedback
likely_causes: [the test expects the header row excluded from the count, the fixture has a trailing newline the parser counts]
question: should an empty header row count as a record?
```

## What the script fills automatically

`cause_class` is set per the rules in `docs/interface-spec.md` section 2
(Escalation report v1); this page does not redefine them. The script fills
`attempts`, `last_failing_output`, `tried` (with real `diff_hash` values from
the workspace snapshot), and `cause_class` straight out of
`stop-hook-verify.sh`'s state file; see `scripts/_verify_impl.py`'s
`write_escalation`. Do not hand-edit these; if one looks wrong, the state
file (`--state`) is the thing to inspect, not the escalation file.

The Stop hook itself only ever detects the two-identical-hashes route to
`cause_class: no_progress`. The spec's other route to the same class, an
operator or a `/goal` evaluator reporting an "impossible" verdict, is not
something the hook can see; that route sets `no_progress` from outside the
script's own state file.

Known weakness, stated beside the rule: `unreachable_condition` vs.
`ambiguous_check_feedback` is a heuristic on output equality, not a semantic
read of *why* the check keeps failing. A check whose output is
non-deterministic (a timestamp, a random ID) will always classify as
`ambiguous_check_feedback` even when the underlying condition is genuinely
unreachable, because the text never repeats. If the check embeds anything
non-deterministic in its output, read `tried` yourself before trusting the
class.

## What a human (or the agent presenting the report) fills in

The script cannot write these two well; they are template placeholders the
presenter completes before handing the report to Graham:

- `goal_block`: the path to the actual Goal block v1 file for this run, or
  its inline `goal_condition` line, if one exists. The script only knows
  whatever string was passed as `--goal`; when nothing was passed it writes
  `not provided`. Replace that before presenting.
- `likely_causes` and `question`: the script writes generic, structurally
  correct defaults for each `cause_class` (see `_verify_impl.py`'s call
  sites). They are usable as-is for a first pass, but the two-line rubric in
  the interface spec ("exactly two, one line each") is best served by
  someone who has actually read `last_failing_output` and `tried` tightening
  the wording to the specific failure, not the generic class.

## Presenting it

Per `## Output contract` in SKILL.md: read `escalation.yaml` from the path
`stop-hook-verify.sh` printed, and present it verbatim (tighten
`likely_causes`/`question` per above), not summarized. The reader should be
able to see the exact failing output without re-running anything.
