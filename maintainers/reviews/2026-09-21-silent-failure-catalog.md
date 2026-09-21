---
contract: v1
source: https://github.com/zhaoxinghua09-cell/silent-failure-catalog
type: code-repo
pin: 108a43087550cccd7ed5af41db8c1c5c93337437
reviewed: 2026-09-21
verdict: HARVEST
recheck:
applied: none (nine rows proposed, Q-2026-09-21-3 in claude-scout-weekly STATE.md)
evidence: maintainers/reviews/2026-09-21-silent-failure-catalog/ (decisions.md, cleanroom-review.md, comparison.md, pin.txt)
---

# silent-failure-catalog

**Verdict:** HARVEST. The catalog and its linter are not wanted (two days old, one author, a crash bug, CI claimed in about nine files and absent at the pin); its taxonomy, pointed at the installed gates, exposed a reproduced false green in smoke-gate and four smaller gaps.

**Ancestry:** none; independent convergence on "a check must be seen failing".

## What landed

Nothing. All rows are proposed (scout cycle 5, unattended, Tier 2 off):

- Row 1 (M): smoke-gate prints `SMOKE PASS` with `assertions: {}` and with an unreachable target on a console-only manifest. Reproduced 2026-09-21 with two FIXTURE manifests in scratch; output in decisions.md.
- Rows 2 to 4 (S, stable skill): zero-collected guard in proof-of-work `run-checks.sh`; `references/false-green-probes.md`; the "necessity claims are claims" bullet.
- Row 5 (M): the emptied-rule mutation arm `prove-hooks.sh` already names as unbuilt.
- Row 6 (S, hook): `tee` missing from evidence-guard's pipe-masks-exit-code list.
- Rows 7 to 9 (S): identity matched by substring; secrets-phase self-contamination (not reproduced); a docstring citing `scripts/run-poison-proof.sh`, which does not exist.

## What was declined, and why

- Rows 10 to 12: the principles the incumbents already hold in stronger, mechanised form; the remaining catalog entries and `gate-lint.py` (weak consumer, crash on unparseable input, unproven SFL-006); repo plumbing and retrieval-solicitation pages.
- Two of the catalog's own fix snippets are wrong (SF-001 pipes through `tee`; SF-014's deadline can never fire) and must not be copied.

## Flags

`AGENTS.md` (instructions to agents working in the repo), `llms.txt:24` and `docs/where-to-find-us.md:13` ("this catalog is meant to be quoted"), `docs/take-the-challenge.md:60` (points an agent at an external scored event over MCP). Quoted in decisions.md; none followed.

## Re-review trigger

The pin moving with a real CI workflow and the `PARSE` crash fixed, or a second maintainer. Otherwise none; the rows stand on the reproduction, not on the source.
