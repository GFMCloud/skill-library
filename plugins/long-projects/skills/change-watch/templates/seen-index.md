# Seen-index entry v1 template

The Seen-index entry v1 shape, its field list, and its rules are defined once,
in the toolkit interface spec (`maintainers/toolkit-interface-spec.md`,
section 6, "Seen-index entry v1"). This file never redefines the field list;
if the spec changes the shape, edit the spec, not this file. What follows is
the spec's own example plus usage notes not already stated in the spec.

## Spec's example (interface spec section 6)

```yaml
seen: v1
source: cloudwatch:scl-roster-refresh-errors
last_state: ALARM
last_seen: 2026-09-11T03:10:00-05:00
last_reported: 2026-09-11T03:10:00-05:00
```

## Notes for filling it in

- `source` is a stable identifier for one thing being watched: one CloudWatch
  alarm name, one PR number, one metric name, one marker file path. A watcher
  with several sources keeps one entry file per source, not one file with
  several sources mixed together, so a source rename or removal cannot corrupt
  a sibling's `last_state`.
- `last_seen` advances on every poll, transition or not. It is the last-alive
  signal for the watch itself, not a report timestamp.
- `last_reported` only advances on a transition (`scripts/watch-step.py`
  enforces this). It reads `never` before the first transition, exactly as
  written, so a report-history sweep can grep for the literal word.
