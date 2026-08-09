# Archetype: python (pipeline / CLI / analysis)

Layout: flat package named after the slug (`my_project/`), `tests/`, `data/` (gitignored),
`pyproject.toml` with ruff + pytest configured, CI running lint and tests.

## What SPEC.md needs

- **§2 Decisions** — data sources and why those, storage format, Python version, the
  handful of libraries that shape the design.
- **§4 Design** — the pipeline steps in order, and what each writes. For anything
  data-shaped, name the join key early; identity resolution across sources is where these
  projects actually get hard.
- **§5 Dependencies and access** — every external endpoint, its auth mechanism, and its
  rate limit. Rate limits belong in the spec because the pressure to "just lower the
  delay" arrives later, in a hurry, from someone who did not read the terms.
- **§6 Verification** — the real commands:

  ```bash
  ruff check . && ruff format --check .
  pytest
  python -m <pkg> --check        # hits the source, prints what it found, writes nothing
  ```

## Traps worth a hard rule

- **Floored pins.** `==`, not `>=`. Two runs of the same commit should not resolve to
  different dependency trees. This matters most for pre-1.0 packages and for unofficial
  clients wrapping private APIs, which change without notice.
- **No `--check` mode.** Every fetcher should have one: hit the source, print what came
  back, write nothing. It is how you find out the upstream changed shape *before* a real
  run half-writes a dataset.
- **Relaxing an assertion to make a run pass.** If totals are supposed to reconcile, a
  failing check means the data or the code is wrong. Loosening the check converts a loud
  failure into a silent one.
- **Committing data.** `data/` is gitignored and reproducible from the pipeline. Beyond
  repo size, an own-account export from an upstream service often carries fields the
  public API does not — obscured coordinates, private notes — and that is how a public
  repo leaks something nobody meant to publish.
- **Asserting exact counts in docs.** Live sources move. Assert invariants (parents equal
  the sum of their children) rather than totals; write totals down as dated snapshots.
