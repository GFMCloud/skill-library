# Review rubric

## Repo maturity signals (the cheap real checks)

All verifiable from the GitHub API or a shallow clone, no code execution:

| Signal | How | What it tells you |
|---|---|---|
| Last commit date | default-branch head | 18 months idle is a different proposition than shipping weekly |
| Commit cadence | last ~50 commits' dates | steady, bursty, or abandoned-then-revived |
| Open-issue shape | skim newest 10 to 20 | usage questions (healthy) vs. unanswered bug reports (rot) |
| Dependency count | manifest (package.json, pyproject, go.mod, Cargo.toml) | each dependency is inherited maintenance surface |
| License | LICENSE file, not the README badge | no license means no adoption, full stop |
| Tests | test dir exists AND CI config runs it | tests that exist but never run count as claimed, not verified |
| Bus factor | contributors of last 12 months | one-person projects inherit that person's availability |

## Verdict criteria

- **ADOPT**: use the thing as-is (install it, deploy it, subscribe to it). The
  bar: verified evidence, acceptable adoption cost, and no existing capability
  already covering it.
- **HARVEST**: the thing itself is not wanted, but named ideas, techniques, or
  fragments in it are. The harvest block is the deliverable.
- **WATCH**: promising but not ready (too young, unclear maintenance, missing
  feature). Requires `recheck:` date; the re-review starts from the prior note.
- **SKIP**: nothing to take. Say why in one or two sentences and stop. SKIP is
  the expected most-common verdict; a pipeline where it is rare is broken.

When torn between two verdicts, take the lower-commitment one; the note records
what would upgrade it.

## Effort scale (harvest block)

- **S**: under an hour, one sitting
- **M**: an afternoon, one PR
- **L**: multi-session; must go through a project harness, not a harvest

## Adoption cost prompts

Answer for every harvest row; "none" is almost never true:

- What breaks or goes stale if this is never touched again?
- Does it need updates, monitoring, credentials, or an open port?
- What is the removal path, in one sentence?
- Does it duplicate a job something else on the account already does?
