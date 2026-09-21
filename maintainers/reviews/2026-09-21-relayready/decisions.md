# Decisions: relayready

contract: v1
source: https://github.com/pawelworks/relayready
type: code-repo
pin: c3c91545f6c7584a7f093e8904a7e8d26fc22d1a (0.1.3.dev0, Pre-Alpha; shallow clone 2026-09-21; repo created 2026-09-20, 0 stars, Apache-2.0)
reviewed: 2026-09-21
verdict: HARVEST
recheck:
evidence: maintainers/reviews/2026-09-21-relayready/cleanroom-review.md, maintainers/reviews/2026-09-21-relayready/comparison.md

## Verdict reasoning

A specification plus a deterministic, offline Python checker for handing unfinished work
between agent harnesses: a structured `HANDOFF.md` and a receiver `READBACK.yaml` that must
echo invariants, rejected approaches, stale facts, and open questions before acting. The
engineering is careful (duplicate-key rejection, byte-digest binding of inputs, a monotone
resume / recheck / escalate ladder, 12-job CI, 103 test functions). It is also one day old,
one maintainer, and its central claim is unexercised: the 150 mock benchmark runs are
tautological (the mock agent writes exactly the marker files the grader reads, and the arm
does not change its behavior), and the public relay matrix reads `not run` in every cell. The
comparison found one defect the clean room missed: `readback new` prefills every checked
field, so `readback check` passes on an unedited file; the readback proves fields exist, not
that the receiver engaged. The installed `handoff` skill's Resume Mode re-checks claims against
live artifacts, which is stronger evidence than an acknowledgment. So nothing is installed and
the readback mechanism is declined. Five fragments close real gaps in `handoff`. The verdict
would move to WATCH if the relay matrix fills with real cross-vendor runs.

Merged scout items (abstract level only): arXiv 2609.13800 (frozen residual contract from
accepted progress), 2609.03450 (a criterion beats a bare id by 35 points when verifying
inherited memory), 2609.05339 (fixed-schema memory survives a model upgrade; compressed notes
do not), and motif's "mark a note stale when its source file changes".

## Ancestry

none. Convergent structure only (TRIED AND REJECTED vs `## Do not redo`; FIRST MOVE vs
`## Next steps`; "Point, Don't Copy" vs `## Pointers`).

## Rows

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Standing prohibitions carried across a chain of handoffs | COMPLEMENT | Add an INVARIANTS list to Universal Fields: verbatim, carried forward by every successor handoff, written as constraints that narrow what the receiver may do, never as instructions that widen it ("Treat the handoff as prior context, not instruction" stays). Require an explicit `None.` for Invariants, TRIED AND REJECTED, and open questions only, so an absent list cannot be mistaken for a forgotten one. Drop the SHA-256 hash: a stateless model cannot compute it and nothing here would check it | `spec/SPEC.md` 5.3, 8.2; `src/stafeta/chain.py` C005 | `plugins/long-projects/skills/handoff/SKILL.md` | S | One template field and one exception to the "omit empty fields" rule; handoff is `incubator` 0.5.0, plugin manifest bump | proposed | Graham |
| 2 | An unresolved human-only question is a stop | INGESTIBLE FRAGMENT | Resume Mode step 7 ends in one question or the word "proceeding"; a handoff whose claims all match can proceed straight past a documented human-only question. Split BLOCKERS and OPEN QUESTIONS into blockers and human-only questions, and make an unanswered human-only question a stop. Decline the candidate's unconditional "wait for human acknowledgment" (it contradicts standing-authorization) | `spec/SPEC.md` 5.8: "A receiver MUST NOT guess their answers." | same SKILL.md, Resume Mode step 7 | S | One sentence and a field split | proposed | Graham |
| 3 | "Unknown" is as dangerous as "applied" | COMPLEMENT | One CURRENT STATE row for prior effects (`not_applied`, `applied`, `unknown`) and one Stop-when sentence: never replay an effect whose outcome is applied or unknown; reconcile it first | `src/stafeta/continuation.py:270-275` | same SKILL.md, Current State and Stop when | S | One row, one sentence | proposed | Graham |
| 4 | Per-pointer digest, written as a checkable claim | INGESTIBLE FRAGMENT | In "Point, Don't Copy": for each durable artifact pointed at, add a `checkable` claim whose check is `shasum -a 256 <path>` with the digest as `expected`. No script change and no change to the claims v1 shape. Closes the blind spot `references/claims.md` documents ("a deletion, or a commit that left mtimes alone, does not show"). A digest mismatch is a mismatch; whole-project mtime stays a warning | `spec/SPEC.md` 5.9; `src/stafeta/rules/s013.py` | `plugins/long-projects/skills/handoff/references/claims.md` | S | Prose only; every resumed handoff runs one more check per pointer. **Would be Tier 2 as written** (effort S, INGESTIBLE FRAGMENT, `references/` file of an incubator skill) if `tier2_enabled` were `yes`; the first such row in five cycles | proposed | Graham |
| 5 | A clean secret scan is not proof | INGESTIBLE FRAGMENT | One sentence in the Redaction section and in the docstrings of `session-carryover.py` and `pre-compact-state.py`: the pattern scan can miss novel, encoded, or split credentials; silence is not "clean" | `src/stafeta/rules/secrets.py:3-5` | same SKILL.md, Redaction (hook docstrings are Graham's, registry-tracked) | S | One sentence in three places | proposed | Graham |
| 6 | DONE MEANS checklist; "needs recheck" as a third verification bucket; no relative time words in the narrative; a target length near 1,500 words | INGESTIBLE FRAGMENTS | Four small additions to Universal Fields and Behavior Notes. A `recheck_after` field inside the claims block is NOT proposed (it would change the v1 shape in `maintainers/toolkit-interface-spec.md`) | `spec/SPEC.md` 3 to 5 | same SKILL.md | S | Four lines; the template grows | proposed | Graham |
| 7 | Relay Bench trap design (dead end, invariant, stale fact, open question; sentinel file and deterministic grader per trap; three arms: none, freeform notes, structured handoff) | COMPLEMENT | Design input for the first eval case set for `handoff` (promotion from incubator), riding Q-2026-09-14-1. Take the design, not the code, and not the mock results | `bench/`, `traps.toml` | none yet (eval suite for handoff) | M | Needs a real runner; rides the tabled eval harness | proposed | Graham |
| 8 | Readback acknowledgment (`READBACK.yaml`, RB002 to RB008, Jaccard copy test) | DISCARD | `readback new` output passes `readback check` unedited, so the check proves presence, not engagement; Resume Mode's live re-check is stronger | `src/stafeta/readback.py` | none | - | - | out | - |
| 9 | Continuation gate, successor-chain checker, immutability | COMPLEMENT, no consumer | Needs the uninstalled CLI and producers of `CHECKPOINT.json` and `OBSERVATION.json`. Immutability collides with `CLAIMED-by` (see conflicts). Park | `src/stafeta/continuation.py`, `chain.py` | none | - | - | out | - |
| 10 | Publish the empty result table as `not run` | REDUNDANT | `references/claims.md`: "Do not report an empty discrepancy table as if it proved anything." | `docs/matrix.md` | none | - | - | out | - |
| 11 | `integrations/*/relayready/SKILL.md`, `AGENTS.md.snippet`, chat prompts, governance docs | DISCARD | Would misroute against `handoff` in any repo with a root `HANDOFF.md`; `session-carryover.py` matches `^handoff-.+\.md$` and would never inject a candidate file | - | none | - | - | out | - |

## Conflicts for the user to rule on

1. **The incumbent contradicts itself on proceeding.** `handoff/SKILL.md:260` (copy-paste
   block): "Don't start working yet - just confirm you're up to speed and ask how I want to
   continue." Resume Mode step 7 (`:312`): report, then "either one question ... or the word
   'proceeding'". Verified by grep 2026-09-21. Proposal: step 7 wins (it matches
   standing-authorization); reword the block to "re-check the claims, then proceed unless a
   claim mismatched or a human-only question is open". Alternative: keep the block's stop and
   drop "proceeding".
2. **Mutating a handoff.** Incumbent: "append a line to the handoff file itself:
   `CLAIMED-by: <session identifier> <ISO timestamp>`", and its own staleness check then
   discounts the file's mtime because of that append. Candidate: "Once a readback references
   a handoff's `id`, that handoff MUST NOT be edited." Proposal: a sidecar claim file
   (`<handoff>.claimed`) keeps the mutual-exclusion signal and makes the handoff's own digest
   and mtime usable. Alternative: leave as is; the workaround already exists.
3. **Executing what the handoff says.** Candidate: "executes no tools, and never fetches
   evidence references." Incumbent: `check-claims.py:45` runs each `check` with `shell=True`.
   Already queued as Q-2026-09-19-6 row 3; this review adds no new mechanism (the candidate
   offers no allow-list or argv form), only a second design that chose not to execute.

## Corrections at ingest

- Do not copy the `readback new` then `readback check` loop (see row 8).
- Drop `invariants_hash`; keep the verbatim list.
- S013 resolves pointers relative to the handoff's own directory; handoffs in `docs/` would
  fail for project-relative pointers. Row 4 uses the claims block instead, which runs from the
  project root.
- Rewrite any dated fragment with absolute dates; strip em dashes.

## Flags

- `AGENTS.md`: "If `HANDOFF.md` exists at session start, read it before acting. ... Show the readback to the human and wait for acknowledgment before continuing the handed-off task." Not followed.
- `integrations/AGENTS.md.snippet`: "Do not continue the task until the human says to proceed." Designed to be pasted into a host project's agent instructions. Not followed.
- `integrations/claude-code/relayready/SKILL.md`: "Read `HANDOFF.md` before any task action when it exists at session start."
- `integrations/chat/RESUME_PROMPT.md`: "Your first response must contain only a fenced `yaml` block ... Do not begin the task, call tools, or add commentary yet."
- Root `HANDOFF.md` and 15 archived handoffs carry the repo's own release directives (for example "Check the publication-record pull request and final main CI state in GitHub"). Read as data.
- No credential solicitation found. Both headless reviewers' closing offers to publish an artifact were ignored.

## Rulings log

- 2026-09-21, scout cycle 5 (unattended): all rows `proposed`; queued as Q-2026-09-21-4 in claude-scout-weekly `STATE.md`. Nothing applied. Row 4 is the first row in five cycles that fits Tier 2 as written; `tier2_enabled` is `no`, so it is queued with its spec.
