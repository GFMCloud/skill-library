---
contract: v1
source: https://github.com/simplybychris/handoff-skill
type: skill-collection
pin: 8990d64805fe340c9e79f59db5a93da273559dc6
reviewed: 2026-09-18
verdict: HARVEST
recheck: none
applied: branch toolkit-review, the commit titled "handoff 0.5.0: fragment from simplybychris/handoff-skill", ruled by Graham 2026-09-18 ("apply the fragment, merge and push it")
evidence: 2026-09-18-handoff-skill/ (both extraction reports and the rejected first attempt with its note, both judgments, ledger, decisions, patch, usage)
---

# simplybychris/handoff-skill

**Verdict:** the installed `workbench:handoff` supersedes the candidate's skill, both judges
agreeing, and one fragment from the candidate is worth folding in: its emergency
procedure for when auto-compaction fires before a handoff is written (KEEP, SUMMARIZE,
DROP), the habit of saving at about half of context rather than at the edge, and its
prompt to promote durable facts to a memory file. The two slash commands are redundant.

**Ancestry:** none found; the judges saw no shared text.

**Method:** the first real `toolkit-review` run, size `spot`, mode `subset`: one slot
(`handoff`), the installed skill on one side, the candidate's skill and two commands on
the other. Neutral extraction per side by headless Sonnet under the clean profile. The
installed side's first report was rejected by `check-extract.sh` for quoting the library's
repository name inside a verbatim fixture warning; the checker archived it, wrote the
rejection note, and the second attempt passed. Two headless Sonnet judges read the two
reports with the order swapped; both passed `check-judgment.sh` on attempt 1, both derived
`merge`, and both classed all four items identically. Spend 339,760 tokens, of which the
re-dispatch was 132,563. The judges saw the run path `/private/tmp/tr-runs/spot-1` and
the owner's email block (standing limit); both said they did not try to infer origin.

## What landed

Row 1, as three additions to `plugins/workbench/skills/handoff/SKILL.md` (handoff 0.5.0):
the keep, summarize, drop triage in the auto-compaction row of the Before Compaction table;
a paragraph on writing the file at about half of context and finishing the micro-step
first; and the offer to move durable facts to memory in Behavior Notes. Checked before
writing: the source file at the pin says exactly what both judges described, and the
installed section held none of the three.

## Rows (rubric v2, both judges)

| # | Candidate item | Class | Judges' note |
|---|---|---|---|
| 1 | `skills/session-handoff` | `FRAGMENT -> workbench:handoff` (2 of 2) | Core save/resume format is outclassed by the installed skill's mechanized re-check of typed claims; its auto-compact fallback (KEEP/SUMMARIZE/DROP), "save at 50 to 60 percent of context" habit and memory-promotion prompt are gaps the installed skill's report does not show. |
| 2 | `commands/handoff.md` | `REDUNDANT` (2 of 2) | A trigger wrapper; the installed skill already fires on the phrase. |
| 3 | `commands/pickup.md` | `REDUNDANT` (2 of 2) | A trigger wrapper for resume with an optional "light look at reality"; the installed resume re-runs every typed claim and stops on a mismatch. |

Installed `workbench:handoff`: `SUPERSEDES skills/session-handoff` from both judges;
deciding criteria "Enforcement mechanism and Fit with the bar" in both judgments.

Proposed target for row 1: `workbench/skills/handoff/SKILL.md`, a short "before context
runs out" section (save early, and what to keep, summarize or drop when compaction is
imminent), effort S, adoption cost one more section to keep true as the compaction hooks
from workbench 0.13.0 change what "imminent" means; backed out by reverting the commit.

## What was declined, and why

Rows 2 and 3: the commands add no content the installed skill lacks.

## Flags

None. The candidate's README addresses the user, not the agent.

## Re-review trigger

The pin moving past `8990d64` with a change to the emergency-fallback procedure, or the
installed handoff gaining a compaction section of its own.
