# Failures: sweep-<NAME>

Orchestrator-only. Workers never write here; they mark `status: failed` in their own
`state/item-<ID>.md` and stop. The orchestrator reads failed state files and logs a
row here at the end of each batch.

| id | target | failure summary | state file | disposition |
|---|---|---|---|---|
| item-9999 | `<TARGET-THAT-MUST-FAIL>` | *(fill in from its state file once the poisoned item has run, this row is the proof the gate works)* | `state/item-9999.md` | expected: proves the gate |

Disposition values: `retry` (transient, re-run as a new pending item), `skip`
(genuine exception, documented and left failed), `needs-human` (escalate at the next
natural pause, not mid-sweep).
