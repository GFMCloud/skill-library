# Smoke manifest v1 template

The field list, its types, and the semantics of `assertions` and `poison` are defined
once, in `docs/interface-spec.md` section 5 ("smoke: v1"). This file does not restate
that list. Copy the shape from the spec (or from the worked example below, which is
the spec's own example instance), fill it in for your project, then run
`scripts/generate-smoke-script.py <your-manifest.yaml> smoke.sh` to produce the
committed smoke script.

## Per-field usage notes

Notes below say something the spec does not; they are not a restatement of the field
list.

- **Picking a poison value**: choose the smallest change that flips the assertion from
  true to false while staying realistic enough to prove the check actually inspects
  the field, not just a name. `identity`: a session identity the app would never
  actually report (a wrong name or role), not garbage the app would reject before
  identity is even checked. `freshness`: a date before `must_advance_from`, ideally
  one that would have been current at some past point, so a script that runs the
  freshness comparison backwards would still record a plausible-looking failure
  instead of an obviously-broken one. `connections`: `127.0.0.1:1` (a port almost
  nothing binds) is a reliable dead endpoint that fails fast without a real network
  timeout. `routes`: a path close to a real one (`/standings-old` next to
  `/standings`) so the check is proven to key on the exact path, not just "some path
  404s". `console`: a distinctive string (`FIXTURE simulated console error: ...`)
  that could not appear in real page output by coincidence.
- **`console` has no `poison` entry by default in a blank manifest.** The generator
  refuses to generate a script for any assertion category with no matching `poison`
  entry (exit 1, "UNPROVEN `<category>`: no poison entry") rather than emitting a
  script that would silently default to an empty marker and report that category as
  passed without ever proving it can fail. Fill in `poison.console`, and every other
  category's `poison` entry, before generating.
- Run `scripts/check-poison-coverage.py <manifest.yaml>` before trusting a green run
  on any category; it prints `UNPROVEN <category>` and exits 3 rather than letting a
  missing poison entry read as a pass.

## Worked example (the spec's own example instance, section 5)

```yaml
smoke: v1
target: https://staging.sloshball.example/
assertions:
  identity:    {expect: "Graham (commissioner)"}
  freshness:   {field: "Rosters updated", must_advance_from: "2026-09-07"}
  connections: [{name: live-scores-socket, expect: open}]
  routes:      [{path: /standings, status: 200}, {path: /teams/1, status: 200}]
  console:     {errors: 0}
poison:
  identity:    "Guest"
  freshness:   "2026-09-01"
  connections: wss://127.0.0.1:1/dead
  routes:      /standings-old
  console:     "throw new Error('FIXTURE poison')"
```

## Wiring notes the generator needs beyond the manifest shape

The `connections` shape carries only a `name` and `expect: open`, no address field,
because the shape is generic across whatever "a socket or api or relay" means for a
given project. The generated script resolves an address for each connection name from
environment variables at run time, not from the manifest:

```text
SMOKE_CONN_HOST_<NAME>   host to TCP-check for connection <NAME>
SMOKE_CONN_PORT_<NAME>   port to TCP-check for connection <NAME>
```

where `<NAME>` is the connection's `name` with every non-alphanumeric character
replaced by `_`, upper-cased (`live-scores-socket` -> `LIVE_SCORES_SOCKET`). Set these
in the environment that runs the smoke script (a deploy script, a CI job, a Stop
hook), not in the manifest. The manifest stays a description of what to check, the
environment supplies where.

Every other category's generated script has a working default baked in from the
manifest and needs no extra wiring for the live pass; the same environment-variable
family (`SMOKE_IDENTITY_EXPECT`, `SMOKE_FRESHNESS_STALE`, `SMOKE_ROUTE_PATH_<PATH>`,
`SMOKE_CONSOLE_MARKER`, `SMOKE_CONSOLE_SOURCE`) is how the poison proof overrides one
category at a time without touching the manifest file. See
[../scripts/generate-smoke-script.py](../scripts/generate-smoke-script.py)'s module
docstring for the full list.
