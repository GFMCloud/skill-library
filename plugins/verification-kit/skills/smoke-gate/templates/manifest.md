# Smoke manifest v1 template

The field list is defined once in `docs/interface-spec.md` section 5 ("smoke: v1").
This file is a fill-in template and one worked example; it does not redefine any
field. Copy the blank template into your project, fill it in, then run
`scripts/generate-smoke-script.py <your-manifest.yaml> smoke.sh` to produce the
committed smoke script.

## Blank template

```yaml
smoke: v1
target: <url, or the launch command that yields one>
assertions:
  identity:    {expect: <who the tool should think the user is>}
  freshness:   {field: <date or count the page shows>, must_advance_from: <value>}
  connections: [{name: <socket or api or relay>, expect: open}]
  routes:      [{path: <path>, status: 200}]
  console:     {errors: 0}
poison:
  identity:    <a wrong value that must make the script exit 1>
  freshness:   <a stale value that must make the script exit 1>
  connections: <a dead endpoint that must make the script exit 1>
  routes:      <a path that must 404>
  console:     <an injected error>
```

A category with no `poison` entry is not proven. Run
`scripts/check-poison-coverage.py <manifest.yaml>` before trusting a green run; it
prints `UNPROVEN <category>` and exits 3 rather than letting a missing poison entry
read as a pass.

## Worked example (from docs/interface-spec.md section 5)

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

The `connections` shape carries only a `name` and `expect: open` — no address field,
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
hook), not in the manifest — the manifest stays a description of what to check, the
environment supplies where.

Every other category's generated script has a working default baked in from the
manifest and needs no extra wiring for the live pass; the same environment-variable
family (`SMOKE_IDENTITY_EXPECT`, `SMOKE_FRESHNESS_STALE`, `SMOKE_ROUTE_PATH_<PATH>`,
`SMOKE_CONSOLE_MARKER`, `SMOKE_CONSOLE_SOURCE`) is how the poison proof overrides one
category at a time without touching the manifest file. See
[../scripts/generate-smoke-script.py](../scripts/generate-smoke-script.py)'s module
docstring for the full list.
