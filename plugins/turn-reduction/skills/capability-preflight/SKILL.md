---
name: "capability-preflight"
description: "Prove access to every system a milestone must touch before the milestone starts — a real read and a real write per system, each with a negative control that must fail. Use at the top of any milestone, before the first step runs, and whenever a step is about to be handed to a human because something looks unreachable."
metadata:
  maturity: stable
  version: 1.1.0
  reviewed: 2026-09-02
---

# capability-preflight

Nine audited sessions produced 148 human turns. The largest avoidable category was 35
turns — 23.6% of everything — of a human carrying output between an agent and a system
the agent could not reach. Every counterfactual reduced to the same sentence: *an agent
with a shell on the machine owning the step.*

That is architectural. Care does not remove it. What removes it is finding out which
systems are actually reachable **before** the work starts, in one pass, and clearing all
of them at once.

## Run it

```bash
# from the directory holding the manifest
python3 <this-skill-dir>/preflight.py capability-manifest.json
```

Absolute path when you need one: read `installPath` for `turn-reduction@gfm-foundry`
out of `~/.claude/plugins/installed_plugins.json`. Never construct it — the cache layout
is `cache/<marketplace>/<plugin>/<version>/`, and where a marketplace omits `version`
that segment is a commit SHA. A constructed path once pointed at nothing and the check
reported success anyway.

Exit codes: `0` everything proven, `1` something is not proven (see BLOCKERS), `2` the
manifest was rejected and nothing ran.

## The manifest

One entry per system the milestone touches: repo paths, git remotes, APIs, credentials,
plugin caches, mounted volumes, anything.

```json
{
  "milestone": "what this pre-flight is clearing",
  "capabilities": [
    {
      "name": "project repo working tree",
      "population": "every file tracked by git under $PROJECT_ROOT",
      "excludes": "untracked files; submodules; the .git directory",
      "remedy": "what Graham has to do if this fails — one line, actionable",
      "read":  { "cmd": "git -C \"$PROJECT_ROOT\" ls-files | wc -l", "evidence": "count>0" },
      "write": { "cmd": "printf x > \"$PROJECT_ROOT/.probe\" && cat \"$PROJECT_ROOT/.probe\" && rm \"$PROJECT_ROOT/.probe\"", "evidence": "contains:x" },
      "negative_control": {
        "cmd": "git -C \"$PROJECT_ROOT/nope\" ls-files",
        "expect": "nonzero_exit",
        "why": "what this failing proves about the probe above"
      }
    }
  ]
}
```

Commands run through `bash -c`, so `$VAR` and `~` expand normally. Keep absolute paths
out of the manifest if it is committed — use environment variables.

`evidence` (required on read and write): `nonempty`, `count>N`, `lines>=N`,
`contains:TEXT`.
`expect` on the negative control: `nonzero_exit` (default), `contains:TEXT`,
`not_contains:TEXT`.

## The four requirements, and the defect behind each

**A check that examined nothing exits non-zero.** `grep … || echo "✓"` once printed a
green tick for a directory that did not exist. So: `||`, `; true`, `&& true`, `set +e`
and `; exit 0` are rejected at manifest-validation time, before anything runs — a probe
must be able to report failure. And exit 0 is not enough on its own: the `evidence` rule
must be satisfied, or the probe comes back `INCONCLUSIVE`, which is a failure. A read
that counted zero files is the same event as a read that could not run.

**The target must be capable of failing.** An auth probe once returned `200` naming the
right league from a *public* endpoint — the identical response comes back with no
credential at all. So every capability carries a negative control: the same access,
deliberately deprived of the thing being proven, which must fail. If it succeeds the
capability is `NOT PROVEN` no matter how green the read and write were. For an API the
control is the same request with the credential stripped. For a path it is a sibling
path that does not exist. For a remote it is a bogus remote.

**State the population and what it excludes.** A diagnostic once ran only against records
that had a prior-season slot, when the cases it existed to catch have none. It passed for
two sessions because it never saw them. So `population` and `excludes` are required
fields, they print next to the verdict, and the report closes by saying that the run binds
only the capabilities the manifest named. A scoped result whose scope travelled with it
cannot be inherited by six things when it was true of one.

**Everything that fails comes back in ONE batch, before work starts.** No probe aborts the
run. Every capability is exercised, then failures print together, each with its `remedy`
line, under `BLOCKERS`. Mid-run discovery of a missing capability is the thing this
exists to prevent — send the batch, wait, re-run.

## Before you call anything unreachable

One session recorded its relays as "structural under current tooling." They were not: the
device bridge existed and **no folder had been connected**. A setup step nobody took,
filed as a tooling limit — and it stayed filed that way because nothing ever tested it.

So a capability may be declared unreachable only with a probe attached, and the script
runs it:

```json
{
  "name": "removable volume",
  "population": "the mount point $VOL",
  "excludes": "every other volume",
  "remedy": "connect the volume, or plan around it",
  "declared_unreachable": {
    "why": "the volume is not mounted on this host",
    "blocking": false,
    "probe": { "cmd": "test -d \"$VOL\" && ls -1 \"$VOL\"" }
  }
}
```

If that probe **succeeds**, the verdict is `FALSE-ARCHITECTURAL-CLAIM` and it blocks. The
thing you called impossible works. `"blocking": false` says the plan is built around the
gap; it still prints, it just does not stop the milestone.

## What this does not cover

It proves the capabilities the manifest names, at the moment it ran. It does not discover
capabilities you forgot to declare, and it does not keep them proven — a credential that
expires mid-milestone will not be caught by a pre-flight that passed this morning. When
the milestone's shape changes, the manifest changes and it runs again.

## Pairs with

- `foundry-core:proof-of-work` — the standard the probes are built to satisfy.
- `turn-reduction:standing-authorization` — what the agent may do once access is proven,
  without asking.
