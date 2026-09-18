# Stop hook

The generated smoke script runs as a Stop hook so a "ready" claim cannot end the turn
while the smoke check is red. Required by "Done when" and proven by
`fixtures/run-fixture-proof.FIXTURE.sh` steps 6 to 9 since 2026-09-18; before that it
was optional and unproven.

The event, the exit-code behavior, and what a Stop hook's stdin and stdout do are
verified facts, not this skill's derivation; they are quoted and sourced in
`foundry-core:bounded-loop`'s
[references/stop-hook-contract.md](../../../../foundry-core/skills/bounded-loop/references/stop-hook-contract.md).
This file only applies those facts to a generated smoke script.

## Event

`Stop`. The hook runs whenever the agent tries to end its turn, which is exactly when
a "ready" claim would otherwise go unchecked.

## The hook script

`scripts/smoke-stop-hook.sh <smoke.sh>` in this skill. It runs the smoke script; on a
non-zero exit it re-prints the script's combined output to stderr and exits 2, so the
blocking message Claude sees is the script's own `SMOKE FAIL: <categories>` line and
the per-category `FAIL` lines, never a paraphrase. On exit 0 it exits 0 and prints
nothing, so a green run releases the turn silently.

Two guards the fixture proves: when the hook's stdin JSON carries
`stop_hook_active: true` (Claude Code is already continuing because this hook blocked
the previous stop), a still-red run is printed to stderr and released with exit 0, so
a smoke script that stays red cannot hold the session in a loop; and a missing smoke
script path is named on stderr with exit 0, so a hook that cannot run never passes as
green in silence.

## settings.json shape

The owner pastes this; the skill never edits `settings.json`.

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash /absolute/path/to/smoke-gate/scripts/smoke-stop-hook.sh /absolute/path/to/project/smoke.sh"
          }
        ]
      }
    ]
  }
}
```

`/absolute/path/to/project/smoke.sh` is the script `scripts/generate-smoke-script.py`
wrote into the calling project (see "Inputs"), not this skill directory's own script.
Any `SMOKE_CONN_HOST_<NAME>` and `SMOKE_CONN_PORT_<NAME>` a category needs go in front
of `bash` in the command, per the generated script's environment-variable overrides.

## Scope

Install this where an in-session "ready" claim is the risk being guarded against (an
interactive session working toward a deploy or demo). It is not a substitute for the
live pass in "Verify," which still needs to be run and its output attached; the hook
only prevents the turn from ending while that pass is red.
