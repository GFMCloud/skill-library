# Seen-index entry v1 template

The Seen-index entry v1 shape is defined once, in the harness interface spec
(`/Users/gfm/work/toolkit-build-harness/docs/interface-spec.md`, section 6).
This file is the fill-in-the-blanks template plus the spec's own example. It
never redefines the field list; if the spec changes the shape, edit the spec,
not this file.

## Template

```yaml
seen: v1
source: <alarm name, PR number, metric name, marker path>
last_state: <the value last observed>
last_seen: <timestamp of the last observation, any state>
last_reported: <timestamp of the last report, or never>
```

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
- The predicate that decides a transition is `current_state != last_state`,
  never "is this state already in the index." A first observation seeds
  `last_state` and reports nothing, because there is no prior state to
  transition from.
