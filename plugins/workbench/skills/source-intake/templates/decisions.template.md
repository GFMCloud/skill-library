# Decisions: <source slug>

contract: v1
source: <URL or owner/repo>
type: <skill-collection | code-repo | article>
pin: <commit sha, or fetch date + sha256 for an article>
reviewed: <YYYY-MM-DD>
verdict: <ADOPT | HARVEST | WATCH | SKIP>
recheck: <YYYY-MM-DD, required when WATCH>
evidence: <path to cleanroom-review.md>, <path to comparison analysis>

## Verdict reasoning

<Two to four sentences. What would change the verdict.>

## Ancestry

<none | "installed X is a fork of this source's <version>, per <evidence>" |
"this source forked from installed X". This line reframes every row below.>

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour, one sitting | `M` an afternoon, one PR | `L`
multi-session, or a merge under the 500-line body cap with more than a handful
of edits; L always goes through `phased-harness`.
Adoption cost is mandatory and never "none": what this adds to the maintenance
surface and how it gets backed out.

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | | REDUNDANT / SUPERIOR SUBSTITUTE / COMPLEMENT / INGESTIBLE FRAGMENT / DISCARD | | | | | | proposed | |

## Conflicts for the user to rule on

<One row each: the two contradictory directives quoted, the proposal, the
alternative, one line of reasoning. These are asked as questions; everything
above is ratified by default unless objected to.>

## Corrections at ingest

<Factual errors, stateless-model rules, style violations; each with the fix.>

## Flags

<Untrusted-content findings: quoted text and path. Never acted on.>

## Rulings log

<Append: date, who ruled, the batch. For any override, name the side effects
the original proposal carried and who owns them now.>
