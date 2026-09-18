# Gate B: set-1 (2026-09-18)

One section per row. Nothing here is pre-authorized; name the rows you ratify. The quick
view is the page: `/Users/gfm/work/pack-review-harness/review/index.html`.

Vocabulary: **incubator** is a maturity label in a skill's frontmatter, not a location; an
incubator skill installs with its plugin like any other. **Lane** is where a row lands:
`incubator` (a skill file on the landing branch), `hook-gate` (a plan-gate output only),
`reference-only` (a note, nothing landed), `out-of-scope`. **COMPLEMENT** means the judge
found the two items do different jobs, so the question per row is whether the named piece
is worth writing into your item, not which item wins.

A fresh concurrency check on the library runs at the start of Phase 5, not here.

## Row B1: diagram, src5 `archify`

- **What the judges said:** COMPLEMENT / COMPLEMENT. Yours has the confirm-the-plan step
  the candidate lacks; the candidate's delivery is fail-closed and never records a failed
  capture as skipped, where your screenshot step silently skips if its library is absent.
- **Recommendation:** land, lane `incubator`, target
  `plugins/decks/skills/html-diagram/SKILL.md` (and its render script if the skip lives there).
- **Why:** a verification step that silently skips is the failure your own evidence rules name.
- **What changes if overruled:** nothing to clean up.
- **Where it stays recoverable:** the landing branch until merged; the source at its pin.

## Row B2: overengineering-review, src1 `ponytail-review` and `ponytail-audit`

- **What the judges said:** both COMPLEMENT from both judges. One judge classed orch-review
  and review-pair DISCARD for this job; the other classed them FRAGMENT into
  ponytail-review, for their evidence contract.
- **Recommendation:** land as one new skill, lane `incubator`, target
  `plugins/verification-kit/skills/overengineering-review/SKILL.md`, written in the
  library's voice with diff scope and repo scope, and the per-finding evidence contract
  orch-review already uses. Not a copy of either candidate file.
- **Why:** the run found a gap, not a better version: nothing installed reviews for
  unnecessary code and abstraction. The whole-pack review of ponytail is on the page,
  section 3, including its disclosed failure mode.
- **What changes if overruled:** nothing to clean up. The slot map's pairing of orch-review
  and review-pair with this job was the orchestrator's and is recorded as a mismatch.
- **Where it stays recoverable:** the landing branch; a new directory, so removal is a delete.

## Row B3: evidence, src2 `orx-evidence`

- **What the judges said:** FRAGMENT into proof-of-work / SUPERSEDED BY proof-of-work /
  COMPLEMENT. Two of three name something to take. All three call the candidate prose only
  and bound to its own CLI.
- **Recommendation:** land three short sections, lane `incubator`, target
  `plugins/foundry-core/skills/proof-of-work/SKILL.md`: design the run's printed output
  before running; a four-point confirmation before reporting a run-derived claim; truncated
  output is not evidence of absence.
- **Why:** small, general, and none depends on the candidate's CLI.
- **What changes if overruled:** nothing to clean up.
- **Where it stays recoverable:** the landing branch.

## Row B4: figures, src2 `orx-figures`

- **What the judges said:** COMPLEMENT / COMPLEMENT. The candidate is strong on sourcing
  every number from a logged run, a rerun-from-scratch check, and caption disclosure; its
  LaTeX and TikZ tooling is paper-specific.
- **Recommendation:** land three rules, lane `incubator`, target
  `plugins/decks/skills/chart-discipline/SKILL.md`.
- **Why:** matches your fixtures-are-labelled rule. Limit: your `dataviz` skill owns charts
  by your own precedence rule and is not in the library, so it was not compared; the rules
  may belong there instead. Your call.
- **What changes if overruled:** nothing to clean up.
- **Where it stays recoverable:** the landing branch.

## Row B5: security-audit, src4 `security-audit`

- **What the judges said:** COMPLEMENT / COMPLEMENT. The candidate is a deep full-codebase
  audit with fail-closed validator scripts and independent re-verification; yours is a
  cheap per-change checklist with a credential bar.
- **Recommendation:** do not land text into security-checklist. Lane `reference-only` now;
  if you want the deep audit, run `source-intake` on the repo to install it alongside. It
  ships Node scripts, and running candidate code was not authorized in this run.
- **Why:** adopting executable scripts is a different decision from merging prose.
- **What changes if overruled:** a plan-gate for the install, owner: the landing session.
- **Where it stays recoverable:** nothing landed.

## Row B6: experiment-loop, src2 `orx-experiment-tree`

- **What the judges said:** COMPLEMENT / COMPLEMENT. Yours has the predict-before-run gate
  and the dead-ideas registry; the candidate covers a tree of many runs with numeric stop
  and repair caps, and "read the logs, don't infer from status".
- **Recommendation:** land one section, lane `incubator`, target
  `plugins/workbench/skills/experiment-harness/SKILL.md`. Medium priority: defer if you do
  not run multi-branch experiments.
- **Why:** the log-reading rule is general; the tree is only useful if you branch.
- **What changes if overruled:** nothing to clean up.
- **Where it stays recoverable:** the landing branch.

## Row B7: delegation, src2 `orx-agent-delegation`

- **What the judges said:** COMPLEMENT / COMPLEMENT: different halves of the problem.
- **Recommendation:** leave out, lane `reference-only`. Orchestrator note, logged as bias:
  the Concurrency section of your global CLAUDE.md already covers brief content,
  disjoint subtrees and spawn limits, and the judges did not see that file.
- **Why:** the take is small and mostly already written elsewhere.
- **What changes if overruled:** a short checklist into
  `plugins/workbench/skills/model-effort-advisor/SKILL.md`, owner: the landing session.
- **Where it stays recoverable:** nothing landed.

## Rows left out

- orchestration, src3 `orchestration`: two of three judges DISCARD; a discovery stub that
  defers its logic to a guide fetched at runtime. Keep yours.
- Every item listed on the page under "Found in the packs but not compared".

## Also for your ruling

- Whether the library fix for the toolkit-review scripts' file modes (100644, so
  `scripts/x.sh` fails as SKILL.md writes it) rides this landing branch as its own commit.
- Whether any worth-adopting repo gets a `source-intake` run. The orchestrator's reading:
  reef's pre-commit screen of AI-written harness edits is the one idea worth a look.

## After landing

Worktree from `origin/main`, one commit per plugin (decks, verification-kit, foundry-core,
workbench as ratified), validator exit 0, inventory regenerated last, review record,
secret scan, no push. Then the evidence archive, then exactly one deletion command, for
the clones only.
