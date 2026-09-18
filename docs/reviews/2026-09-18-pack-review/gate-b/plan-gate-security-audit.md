# Plan-gate: row 9, security-audit as a separate skill (2026-09-18)

Status: waiting for Graham's approval. Nothing in this plan has been done. No file from
the candidate has been copied and none of its code has been run.

Ruling this serves (Gate B, quoted): "B5 - Adopt as a sep skill as well".

## Goal, restated

Install the full-codebase security audit from `cloudflare/security-audit-skill` (pin
c1c8a8c1471069fb0e188eeaff69b8e8db6564a8, MIT, Copyright Cloudflare, Inc.) as its own
skill in `verification-kit`, beside `security-checklist`, which stays the cheap
per-change pass and is not edited. Both judges classed the pair COMPLEMENT.

Why this is a gate and not a landing: every other row in this run was prose rewritten in
the library's voice. This one is 20 files and 5,276 lines, 3,037 of them executable Node
(two validators and their two test files), whose value is that they are used as written.
That collides with two standing rules: the runbook's "never copy a candidate file in
whole", and `auth_candidate_code: no`.

## What was established by reading only (nothing executed)

- Files: `SKILL.md` (192 lines), 14 reference `.md` files (1,778 lines), `report-schema.json`
  (461), `validate-findings.cjs` (773), `validate-coverage-ledger.cjs` (872), and a
  `.test.cjs` for each (652, 740).
- `grep -n -E "require\(|child_process|exec\(|spawn|https?:|fetch\(|net\.|writeFile|unlink|rmSync|process\.env"`
  over the two validators returned six lines, all `require` of `fs`, `path` (or the
  `node:` forms) and `util`'s `TextDecoder`. No network, child-process, environment or
  file-write call matched. This is a grep, not an audit: it cannot see a call built from
  strings.
- The skill's own frontmatter says it is guidance by default and runs the complete
  workflow only on an explicit audit request. It delegates to two sub-agent roles through
  the Task tool.
- No `package.json` in the skill directory, so no install step and no third-party
  dependency; the runtime need is `node`.

## Blocking questions (each with a recommended default)

1. **Vendor or reference?** Recommended: vendor the 20 files unmodified into
   `plugins/verification-kit/skills/security-audit/` with the MIT `LICENSE` beside them and
   a `SOURCE.md` naming the repo and pin, and add only a library frontmatter block
   (`metadata.maturity: incubator`). The alternative, rewriting it in the library's
   voice, would discard the validators, which are the reason both judges rated it above
   the checklist on enforcement. Vendoring is an explicit exception to "never copy a
   candidate file in whole" and needs your yes in those terms.
2. **May the candidate's tests be run once, here, as the acceptance check?** Recommended:
   yes, exactly `node --test validate-findings.test.cjs validate-coverage-ledger.test.cjs`
   in the landing worktree, after a line-by-line read of both validators by this session.
   This is the one action that opens `auth_candidate_code`, for these four files only. If
   no: the skill lands as unverified and says so in its own text, which I would not
   recommend for something whose claim is fail-closed validation.
3. **Name.** Recommended: keep `security-audit`. It collides with no library or
   project-local skill name. The built-in `/security-review` is a different command and
   the description will say so.

## Assumptions (numbered, each falsifiable)

1. `node` is on PATH on this machine at a version with `node --test` (18 or later).
   Falsified by: `node --version`.
2. The validators read only the paths given as arguments and write nothing. Falsified by:
   the line-by-line read in step 2, or a test run that leaves any file outside a temp dir.
3. The library validator accepts the vendored skill as incubator: the 14 reference files
   sit at the skill root, not under `references/`, and F18 checks only six directory
   names, so it passes. Falsified by: `validate-skills.sh` exit non-zero.
4. The candidate's `SKILL.md` body is under 500 lines (192) and needs no split.
5. Its description does not steal routing from `security-checklist`: the audit fires on
   "audit", "pen test", "full review"; the checklist on "security pass", "is this safe to
   deploy". Falsified by: asking for a per-change security pass three ways in a fresh
   session after install and seeing the audit load. Not checkable before merge.
6. Two sub-agent roles per full audit is an accepted cost; the description will state it.

## File-level plan (after approval, in the landing worktree only)

1. Read both validators in full, as data. Stop and report if anything beyond reading the
   named input files and printing appears.
2. Copy the 20 files to `plugins/verification-kit/skills/security-audit/`; add `LICENSE`
   (from the repo root) and `SOURCE.md` (repo, pin, date, "vendored unmodified except
   frontmatter").
3. Edit `SKILL.md` frontmatter only: add `metadata.maturity: incubator`; extend the
   description with negative scope (not the per-change pass: `security-checklist`; not
   the built-in `/security-review`) and cost (node, two sub-agent roles, a long read).
4. If question 2 is yes: run the two test files once; record command and output.
5. Prove the validators by deliberate failure on the library's side too: one
   `findings.json` that must fail and one that must pass, outputs recorded.
6. `verification-kit` 0.4.0 to 0.5.0, CHANGELOG entry, `generate-inventory.sh`,
   `validate-skills.sh` exit 0, gitleaks on the staged diff, one commit naming ledger
   row 9. No push.

## What changes if you say no

Row 9 moves to `reference-only` in `decisions.md`, the page's recommendation cell is
reworded to match and the page regenerated. Nothing to clean up in the library.

## Dependency on the clone

The source is `run_dir/candidates/src4`. Phase 6 offers a deletion command for
`candidates/`. If this plan is still open at that point, the offer excludes `src4`; the
pin makes it re-fetchable either way.
