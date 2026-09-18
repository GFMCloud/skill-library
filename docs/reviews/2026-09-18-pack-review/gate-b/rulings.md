# Gate B rulings: set-1

Graham's words are quoted verbatim. Rows not named here have no ruling yet.

## 2026-09-18, first reply

> B5 - Adopt as a sep skill as well
> B7- leave out

- **B5 security-audit, src4:** adopt the candidate as a separate skill alongside
  security-checklist. This overrides the walkthrough's `reference-only` recommendation and
  matches the page's wording ("adopt alongside"). Side effects of the override: the
  candidate ships Node scripts, `auth_candidate_code` is `no`, and the walkthrough names a
  plan-gate for the install. Owner: the landing session (Phase 5), which writes the
  plan-gate and stops for approval before any script from the clone is copied or run.
  Nothing is merged into `security-checklist`.
- **B7 delegation, src2:** out. Matches the walkthrough. The page's "small take at most"
  wording in `recommendations.tsv` is corrected to match and the page regenerated.

## 2026-09-18, second reply

Asked: "Do you ratify B1, B2, B3, B4 and B6 as recommended?" and whether the file-mode
fix rides the landing branch.

> yes all as recommended, file-mode fix rides the branch

- **B1 diagram, B2 overengineering-review, B3 evidence, B4 figures, B6 experiment-loop:**
  ratified as recommended in `walkthrough.md`, lane `incubator`, targets as named there.
- **orchestration, src3:** out, keep yours, as recommended. Items "found but not
  compared" stay out.
- **File-mode fix** for the toolkit-review scripts: rides the landing branch as its own
  commit.

## Not ruled

- Whether any worth-adopting repo gets a `source-intake` run: no answer; stays an open
  item in `STATE.md`, owner Graham. Nothing is run.
- Em dashes in quoted judge text on the page: no objection raised; left verbatim.

## Status per decisions.md row

1 delegation out; 2 diagram ratified; 3 evidence ratified; 4 experiment-loop ratified;
5 figures ratified; 6 orchestration out; 7 and 8 overengineering-review ratified;
9 security-audit ratified (as a separate skill, behind a plan-gate, see first reply).

## 2026-09-18, third reply: plan-gate for row 9

Asked: the three questions in `plan-gate-security-audit.md`, each with a default
(vendor the 20 files unmodified with LICENSE and SOURCE.md; run the candidate's two test
files once after a line-by-line read of both validators; keep the name `security-audit`).

> approve with defaults

- This is a dated override of two declared boundaries, for row 9 only: the Phase 5
  runbook's "Never copy a candidate file in whole", and `auth_candidate_code: no`.
- `auth_candidate_code` opens for exactly four files, `validate-findings.cjs`,
  `validate-coverage-ledger.cjs` and their two `.test.cjs`, run with `node` in the
  landing worktree, after both validators have been read in full by the landing session.
  Nothing else from any candidate clone is run.
- If the read finds anything beyond reading named input files and printing, the landing
  stops and reports.
