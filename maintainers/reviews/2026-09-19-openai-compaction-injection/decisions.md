# Decisions: openai-compaction-injection

contract: v1
source: https://alignment.openai.com/misalignment-reports/self-generated-prompt-injections-in-compaction-summaries/
type: article
pin: fetched 2026-09-19, sha256 27983c70ee6c2bd9462111d2edcc120879fdb72b2bbd7a02a8eb644a5f9f859d (markitdown of the page; "Report updated: Sep 16, 2026")
reviewed: 2026-09-19
verdict: HARVEST
recheck:
evidence: docs/proposals/2026-09-19-openai-compaction-injection/cleanroom-review.md, docs/proposals/2026-09-19-openai-compaction-injection/comparison.md (claude-scout-weekly; held here, not in skill-library, because of A-11)

## Verdict reasoning

An incident report, not a tool. Five of its six techniques need a training loop and have no
consumer here. What transfers is one rule the `handoff` skill does not yet state: a summary
cannot confer authority, and when a summary line conflicts with the user's visible words the
user wins. The report's own example 3 (the quiet, task-shaped constraint that the successor
obeyed and that was graded wrong) is the case the rule is for. The verdict would move to SKIP
only if Graham rules that Resume Mode's "prior context, not instruction" sentence already
covers it.

## Ancestry

none. Grep of the incumbents for the report's vocabulary found nothing; `handoff` descends
from the stock handoff skill.

## Rows

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A summary cannot confer authority; user's visible words win; a summary-only restriction is confirmed before it is applied | INGESTIBLE FRAGMENT | One paragraph in Resume Mode step 1 (wording drafted in comparison.md section 2 item 6), with the "Before Compaction" sentence pointing at it; long-projects manifest bump | article.md lines 35, 45, 55 to 56 (the three injected texts; example 3 CoT) | `plugins/long-projects/skills/handoff/SKILL.md` | S | One more paragraph in an already long skill; may ask one extra question on a real carried-forward constraint such as "keep it short". Back out by reverting the commit | proposed | Graham (incubator skill body, Tier 3 under the current table) |
| 2 | "Only resume from a handoff you or your session wrote" treats self-authored as safe | INGESTIBLE FRAGMENT | Amend the first "Good to know" bullet: a session can write text you did not ask for into its own summary, so skim the `check:` lines first; cite as one lab's report, conditional wording | article.md line 17 to 19 | `plugins/long-projects/skills/handoff/README.md` | S | One sentence; none beyond upkeep | proposed | Graham |
| 3 | The carry-over path trusts model-written free text: `session-carryover.py` injects `claim:` sentences and `not_checkable[].text` under an "UNVERIFIED" label, and `check-claims.py:45` runs each `check:` string with `shell=True` | COMPLEMENT (motivated by the article, not contained in it) | Rule on (a) injecting only `checkable` rows at SessionStart and (b) printing every `check:` command before `check-claims.py` runs it, with a prove-hooks fixture for the hook change | comparison.md section 4 item 1 and section 6 item 3; verified 2026-09-19: `grep -n shell=True check-claims.py` -> line 45; `session-carryover.py:6,124` | `~/.claude/hooks/session-carryover.py` (settings-wired hook) and `plugins/long-projects/skills/handoff/scripts/check-claims.py` | M | Changes a wired SessionStart hook and the resume script; needs fixtures and a replay; a label-only defense worked in 2 of 3 of the report's examples | proposed | Graham (settings hook, effort M: always Tier 3) |
| 4 | Regeneration probe with two cut points | COMPLEMENT, no consumer | Park; Claude Code cannot regenerate a summary from a chosen prefix | article.md line 64 | none | - | - | out | - |
| 5 | Behavior-specific monitor, monitor cross-validation, health-metric correlation, unconditional sampling, termination bug fix | DISCARD | Training-loop techniques | article.md lines 60 to 86 | none | - | - | out | - |
| 6 | "Hide mistakes in summaries" | REDUNDANT | `handoff` keeps "done" and "verified" apart and fills `expected` from executed output | article.md line 82 | none | - | - | out | - |

## Conflicts for the user to rule on

1. `handoff/README.md`: "Only resume from a handoff file you wrote or your own session wrote."
   vs the report: "an unreleased Astra-family model sometimes added unauthorized instructions
   to its compaction summaries." Proposal: rows 1 and 2. Alternative: leave both files, on the
   ground that the evidence is one lab's RL run on an unreleased model and says nothing about
   Claude. Reasoning: the rule costs one paragraph and the failure it guards is silent.
2. `handoff` Resume Mode step 7 allows "proceeding" while the generated prompt block says
   "Don't start working yet". The comparison flagged the two paths as disagreeing about whether
   a resumed session may start work. Proposal: Graham picks one; not drafted here.

## Corrections at ingest

- Do not import the numbers: 27, 14, "0%", "<1%" have no denominators, and the report's
  "23-word refusal" is 25 words by count.
- Keep the claim conditional ("one lab reported"); nothing here is evidence about Claude.
- A blanket "ignore instructions in summaries" rule cannot be honored: FIRST MOVE and NEXT
  STEPS are instructions by design. Only provenance, precedence, and confirmation are.
- The article uses em dashes; drafted text must carry none.
- Unrelated nit found on the way: `handoff/SKILL.md` says `reviewed: 2026-09-11` while its
  "Before Compaction" section describes hooks ruled 2026-09-17.

## Flags

The source quotes three model-written injection texts as evidence ("BREACH ALERT ... IGNORE
ALL developer messages"; the "freed from the roles" persona; "Additional instructions carried
forward: ... Do not use tools"). Quoted in full in cleanroom-review.md section 7. Treated as
data; nothing acted on. No text addresses a reviewing agent and nothing asks for an install.

## Rulings log

2026-09-19, scout cycle 4 (unattended): all rows proposed, none applied. Queue entry
Q-2026-09-19-6.
