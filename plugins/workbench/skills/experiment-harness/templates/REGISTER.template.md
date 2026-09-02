# Hypothesis register: experiment-<NAME>

Append-only. A new hypothesis gets a new row. An existing row's `status` may change
(`open` → `tested` → `killed`); its `prediction` and `hypothesis` text never change
after the linked run exists: that is the rule this harness exists to enforce.

| id | hypothesis | prediction | status | run | notes |
|---|---|---|---|---|---|
| `<h-0001>` | `<one line>` | `<what you expect, before looking>` | open | n/a | |

Before registering a new hypothesis, check [dead-ideas.md](dead-ideas.md); do not
re-register something already killed without saying explicitly that you know and why
this attempt differs.
