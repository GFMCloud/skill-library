# Decisions: andrej-karpathy-skills

contract: v1
source: https://github.com/multica-ai/andrej-karpathy-skills (formerly forrestchang/andrej-karpathy-skills; the old path redirects)
type: skill-collection
pin: 2c606141936f1eeef17fa3043a72095b4765b9c2
reviewed: 2026-09-02
verdict: HARVEST
recheck: n/a
evidence: cleanroom-review.md, comparison.md, currency-check.md (all in this scratchpad; copied into the review record directory at Step 6)

## Verdict reasoning

One 67-line skill, byte-identical in three files, restating four principles from a single X post. Two of the four are redundant against the Claude Code harness prompt and the global working agreements, and Principle 1 (stop and ask on any unclarity) directly contradicts the harness's proceed-and-flag default and the "Standing defaults" section of the global CLAUDE.md. Two rows are genuine gaps nothing on disk covers: the your-orphans/their-orphans dead-code asymmetry plus "match existing style", and the code-shape anti-overengineering bullets. HARVEST those; nothing else. The verdict would flip to SKIP if the transcript check shows these failure modes have never cost a correction here (the CLAUDE.md economy rule), and to ADOPT never: the description has no negative scope and would fire on every coding task, colliding with proof-of-work.

The repo's popularity (209,665 stars, 21,334 forks as of 2026-09-02) is not evidence of quality; it has had no commit since 2026-04-20, every PR since then was closed by its own author, and there is no LICENSE file.

## Ancestry

none. `grep -ril karpathy` over ~/skill-library and ~/.claude returns nothing outside this session; no CHANGELOG or merge note names the source. Independent origin.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour, one sitting | `M` an afternoon, one PR | `L`
multi-session, or a merge under the 500-line body cap with more than a handful
of edits; L always goes through `phased-harness`.
Adoption cost is mandatory and never "none": what this adds to the maintenance
surface and how it gets backed out.

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Orphan-cleanup asymmetry + match existing style ("Remove imports/variables/functions that YOUR changes made unused. Don't remove pre-existing dead code unless asked." / "Match existing style, even if you'd do it differently.") | COMPLEMENT | Add a short "Surgical edits" block (about five lines) under Working agreements in the global CLAUDE.md, same shape as "Edit the generator, never the output". Combined with row 2. | skills/karpathy-guidelines/SKILL.md:39-47 | /Users/gfm/.claude/CLAUDE.md (git-versioned locally; outside skill-library, so the review record names the ~/.claude commit) | S | About five lines loaded into every session for the life of the file. Backed out by deleting the block; ~/.claude is git-versioned. | overridden: Graham ruled to add the block to ~/.claude/CLAUDE.md anyway (commit 566c71a there), with one correction on record against the economy rule's two | Claude |
| 2 | Code-shape anti-overengineering bullets ("No abstractions for single-use code. No 'flexibility' or 'configurability' that wasn't requested. No error handling for impossible scenarios.") | COMPLEMENT | Fold into the same block as row 1, restyled. Drop the circular "would a senior engineer" line and the "200 lines could be 50" tautology. | skills/karpathy-guidelines/SKILL.md:27-30 | /Users/gfm/.claude/CLAUDE.md | S | Shares row 1's cost; no separate backout. | overridden: landed with row 1 | Claude |
| 3 | Step-to-verify plan template ("1. [Step] -> verify: [check]") as a pre-execution pointer | INGESTIBLE FRAGMENT | One sentence in proof-of-work's "Pairs with" or "The standard" section: for multi-step work, declare each step's check before running it. Stable-skill change: version 1.0.0 to 1.1.0, reviewed date, CHANGELOG line. | skills/karpathy-guidelines/SKILL.md:60-64 | plugins/foundry-core/skills/proof-of-work/SKILL.md | S | A version bump and CHANGELOG line on a stable skill for one sentence; foundry-core plugin version bump so caches refresh. Backed out by reverting the commit. | ratified by Graham 2026-09-02 | Claude |
| 4 | Principle 1, Think Before Coding (stop and ask on any unclarity; present all interpretations) | REDUNDANT, and contradicts the harness | Take nothing. Harness prompt and global CLAUDE.md "Intent before execution" already cover the useful part with a narrower, better-specified trigger. | SKILL.md:13-22 | (none) | | | out | |
| 5 | Principle 2 opening bullet ("No features beyond what was asked") and Principle 3 opening bullets (don't improve adjacent code, don't refactor what isn't broken) | REDUNDANT | Covered verbatim in spirit by the harness prompt ("The requested scope is the deliverable"). | SKILL.md:26, 40-41 | (none) | | | out | |
| 6 | Principle 4, Goal-Driven Execution (test-first transforms) | REDUNDANT, inferior | proof-of-work and evidence-report cover it with an escape hatch and non-code artifact classes the source lacks. | SKILL.md:50-66 | (none) | | | out | |
| 7 | EXAMPLES.md (522 lines of before/after examples) | COMPLEMENT with defects | Not now. Orphaned in its own repo, and its flagship test-first example is factually broken (stable sort; before and after code identical). Revisit only if a coding-hygiene skill with a references/ directory ever exists. | EXAMPLES.md | (none) | | | out | |
| 8 | "These guidelines are working if" success-signal line | REDUNDANT | Four subjective signals, no baseline. authoring-standard.md's eval-case rule is the stronger mechanism. | CLAUDE.md:65, .cursor/rules/karpathy-guidelines.mdc:70 | (none) | | | out | |
| 9 | The plugin as installable unit (marketplace.json, plugin.json) | DISCARD | Description has no negative scope and fires on all coding work; would load duplicate verification guidance beside proof-of-work. No LICENSE file. Unmaintained. | .claude-plugin/* | (none) | | | out | |
| 10 | CLAUDE.md / .cursor rule copies | DISCARD | Byte-identical duplicates of the skill body; the repo hand-syncs three copies. Nothing to take beyond rows 1-2. | CLAUDE.md, .cursor/rules/karpathy-guidelines.mdc, CURSOR.md | (none) | | | out | |

## Conflicts for the user to rule on

**Question 1 (rows 1 and 2): where does the harvested block live, or does it wait?**
The CLAUDE.md economy rule ("Write a project fact down only once it has cost a correction twice") argues against adding lines on a review's say-so. A transcript scan of the last 60 days for user corrections about drive-by edits, style drift, orphaned or deleted code, and over-abstraction is the evidence; its result is recorded in the Rulings log below.
- Proposal: add the block to the global CLAUDE.md if the scan shows two or more corrections in these categories; otherwise record the block text in the review record as a banked candidate and set no recheck (it is one paste away when the second correction happens).
- Alternative A: a new incubator skill in foundry-core. Rejected by Claude because its description would have to match all coding work, which is the routing failure the authoring standard names, and because the clean-room reviewer's point holds: this content is a global style rule, not a triggered capability.
- Alternative B: add it regardless of the scan. Cheap, checkable, but it sets a precedent against the economy rule.

**Question 2 (row 3): take the step-to-verify pointer into proof-of-work, or not?**
- Proposal: take it, as one sentence, because it is the one part of Principle 4 that is pre-execution rather than post-execution and proof-of-work has no "before you start" line.
- Alternative: out. The model already produces step plans unprompted, and plan-gate covers the cases where a plan matters. Claude rates this the weakest row; objecting costs nothing.

## Corrections at ingest

- Restyle to the no-em-dash rule (the SKILL.md copy uses plain hyphens; README.md uses ten em dashes; take text from SKILL.md, not README).
- Drop "Ask yourself: Would a senior engineer say this is overcomplicated?" (criterion outsourced to an imagined third party) and "If you write 200 lines and it could be 50, rewrite it" (the antecedent contains the judgment).
- Shape each ingested rule as scope, action, exception, verification per authoring-standard.md; the source's bullets are bare imperatives.
- Attribute as an informal practitioner observation (one X post, not fetched or verified), not a reference.
- No "stop and ask" language enters anything on this machine; headless runs cannot honor it.

## Flags

Untrusted-content findings, quoted with path, none acted on:
- README.md:122-126 asks the reader to append the file to their CLAUDE.md: `echo "" >> CLAUDE.md` / `curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md`. Unguarded; run twice it duplicates. Appended to this machine's global file it would sit in the same file as, and contradict, "Intent before execution".
- README.md:104-111 asks for marketplace install: `/plugin marketplace add forrestchang/andrej-karpathy-skills` / `/plugin install andrej-karpathy-skills@karpathy-skills`.
- .cursor/rules/karpathy-guidelines.mdc:3 `alwaysApply: true` (auto-injection into every Cursor request).
- README.md:3-5 third-party promotion: "Check out my new project [Multica]..." / "Follow me on X".
- SKILL.md:9, README.md:7 sole authority is an external URL: `https://x.com/karpathy/status/2015883857489522876`. Not fetched.

## Rulings log

- 2026-09-02, Claude (proposed): rows 4-10 out by default; rows 1-3 pending question 1 and question 2. Transcript scan result (workbench:transcript-scanner, Sonnet, 434 jsonl files, 60 days, human turns only): A drive-by edits 0, B style drift 0, C deleted code 0, D over-engineering 1 (session b5036374, 2026-08-12, a 7-step manual refresh procedure proposed for a cron-driven artifact; process shape, not code shape). Caveat from the scanner: about half the corpus is subagent transcripts with no human turns. Threshold of two corrections not met; rows 1-2 banked per the CLAUDE.md economy rule. Question 1 closed by evidence. Question 2 (row 3) put to Graham.
- 2026-09-02, Graham: row 3 ratified (Take it). Rows 1-2 banked, 4-10 out, as proposed. Applied in one commit on main; no push.
- 2026-09-02, Graham: override on rows 1-2, "Add the banked block to CLAUDE.md anyway." Landed in ~/.claude/CLAUDE.md as "Surgical edits" (commit 566c71a). Side effects re-derived: the CHANGELOG bullet, the review record's What landed and re-review trigger, and this table all said banked and were corrected in the same pass. Verdict unchanged (HARVEST); recheck date unchanged.
