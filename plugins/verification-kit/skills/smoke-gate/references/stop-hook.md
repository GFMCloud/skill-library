# Optional Stop hook

The roadmap entry for this skill includes the option to install the generated smoke
script as a Stop hook, so a "ready" claim cannot end the turn while the smoke check is
red. This is optional: nothing in "Verify" or "Done when" requires it, and it is not
proven by a fixture in this build (the fixture proof in `fixtures/run-fixture-proof.
FIXTURE.sh` runs the generated script directly, never through a hook).

The event, the exit-code behavior, and what a Stop hook's stdin and stdout do are
verified facts, not this skill's derivation; they are quoted and sourced in
`foundry-core:bounded-loop`'s
[references/stop-hook-contract.md](../../../foundry-core/skills/bounded-loop/references/stop-hook-contract.md).
This section only applies those facts to a generated smoke script.

## Event

`Stop`. The hook runs whenever the agent tries to end its turn, which is exactly when
a "ready" claim would otherwise go unchecked.

## settings.json shape

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'out=$(/absolute/path/to/smoke.sh 2>&1); code=$?; if [ \"$code\" -ne 0 ]; then echo \"$out\" 1>&2; exit 2; fi; exit 0'"
          }
        ]
      }
    ]
  }
}
```

`/absolute/path/to/smoke.sh` is the script `scripts/generate-smoke-script.py` wrote
into the calling project (see "Inputs"); it is not this skill directory's own script,
and per that generated script's own environment-variable overrides (its module
docstring), the hook's command can pin `SMOKE_CONN_HOST_<NAME>` etc. inline before the
`bash -c` if a category needs one.

## The command's exit-2 path

`stop-hook-contract.md` establishes, from the docs: exit code 2 on a `Stop` hook
"prevents Claude from stopping, continues the conversation," and the blocking message
Claude sees is "your stderr text" when the hook prints no JSON blocking decision. The
command above follows the same shape `bounded-loop`'s own hook uses: capture the
smoke script's combined output, and only on a non-zero exit re-print that output to
stderr and exit 2, so the blocking message is the smoke script's actual `SMOKE FAIL:
<categories>` line and the per-category `FAIL ...` lines, never a paraphrase.

On a zero exit the command exits 0 and, per the same reference, plain stdout on `Stop`
"lands in the debug log only, not automatically in the transcript", so a passing
smoke run releases the turn silently, which is the intended behavior (nothing to
report when everything is green).

## Scope

Install this only where an in-session "ready" claim is the risk being guarded against
(an interactive session working toward a deploy or demo). It is not a substitute for
the live pass in "Verify," which still needs to be run and its output attached; the
hook only prevents the turn from ending while that pass is red.
