# Decisions: posthog-agents-md

contract: v1
source: https://x.com/posthog/article/2094485724171223409 ("Your AGENTS.md is holding you back", PostHog / Jina Yoon, published 2026-08-31)
type: article
pin: fetched 2026-09-02 (saved X page, /Users/gfm/Downloads/page-2026-09-02-22-37-59.md); sha256 476068f76c43349c57f768c90f8f9804e1c90e7b9f79dce60e9ecc9c809a971f
reviewed: 2026-09-02
verdict: SKIP
recheck: n/a
evidence: cleanroom-posthog.md (CLI default model, --setting-sources "", read-only tools), comparison-posthog.md (Sonnet subagent, 9 incumbents plus the authoring standard, the global CLAUDE.md, the consolidation harness and the weekly maintainer), currency-check.md

## Verdict reasoning

Nine techniques; six are covered as well or better by rulings-harness (three-way keep test instead of a binary delete), the authoring standard (boundary and retention eval sets instead of one failing-prompt list), the weekly maintainer (transcript-grounded cluster-and-verify instead of self-report clustering) and the consolidation harness (one editable home instead of a six-month reset). Two fragments fill gaps confirmed by grep in sweep-harness: the worker grades its own done check with no independent grader anywhere in the skill, and nothing asks the worker what would have made the item cheaper. One complement (skill attribution in commits) has no consumer and no incident behind it. What would change the verdict: Graham declining both sweep-harness rows makes it SKIP.

## Ancestry

none. Zero hits for posthog, wizard-ci, context-mill, commandments.yaml or pr-evaluator anywhere in the library or its history.

## Fact-currency check

The /doctor feature list is CHANGED against the docs fetched 2026-09-02: current wording is "finds unused skills, MCP servers, and plugins versus their context cost", "trims checked-in CLAUDE.md files by cutting content Claude could derive from the codebase", "reports findings first and asks for confirmation before changing anything"; the trim check needs v2.1.206 or later, not v2.1.198. No row restates the article's list. Installed: 2.1.258. Detail in currency-check.md.

## Rows

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | "If you can't name the failure it prevents, delete it" | REDUNDANT | rulings-harness keeps preferences and burn-derived rules without a nameable incident; the heuristic inverts the burden of proof and a stateless reviewer can never name the incident. Not adopted | posthog-agents-md.md 161 | n/a | | | out | |
| 2 | failures.md: re-run the prompts that caused mistakes when editing context | REDUNDANT | authoring-standard.md eval cases, boundary set plus retention set. Note: the library has zero eval cases, so the incumbent rule has never fired; a fact for Graham, not a row | 227 | n/a | | | out | |
| 3 | End-of-run question: what guidance would have prevented wasted turns | COMPLEMENT | Optional one-line field in the worker's state file, "what would have made this item cheaper or more reliable", written only when the worker has something concrete; the orchestrator lists the non-empty answers in the closing report so the stream is read, not stored. Exception: skipped for poisoned items. Verification: the closing report section is present even when empty | 243 | plugins/workbench/skills/sweep-harness/templates/WORKER.template.md (step 4) and item-state.template.md; dispatch-SKILL.template.md closing report | S | A few tokens per item and one report section; a self-report stream that retro's philosophy distrusts, so it is advisory only; back out by deleting the field | proposed; Question 2 | this session |
| 4 | Independent grader separate from the doer (wizard-ci plus pr-evaluator) | INGESTIBLE FRAGMENT | The loop as a whole is sweep-harness plus pre-delivery-verifier. Fragment: when the treatment's done check is a judgment rather than a command exit code, the orchestrator runs `verification-kit:pre-delivery-verifier` over done items before closing the sweep, with the poisoned item included so the grader is proven to reject. Named in the interview as an option, default off | 190-198 | plugins/workbench/skills/sweep-harness/SKILL.md (interview and close-out) and templates/dispatch-SKILL.template.md | S | One extra subagent pass per graded sweep; a cross-plugin dependency the skill already has precedent for (phased-harness names the same verifier); back out by removing the option | proposed (ratified by default) | this session |
| 5 | Scaled-down evals ("save prompts that check your agents") | REDUNDANT | same incumbent as row 2 | 225 | n/a | | | out | |
| 6 | Cluster and verify before acting on agent feedback | REDUNDANT | weekly maintainer: transcript survey, tiered authority, fresh-context verifier, S-30 record | 263-273 | n/a | | | out | |
| 7 | Name the skills consulted in every PR or commit | COMPLEMENT | No library target; a repo convention. Global rule: write it down only once it has cost a correction twice; it has cost zero. Propose out | 281-285 | none | | | proposed out; Question 3 | |
| 8 | Delete CLAUDE.md every six months | DISCARD | contradicts one-editable-home with continuous verification; per-item revisit dates already catch drift | 91-93 | n/a | | | out | |
| 9 | Structured commandments.yaml records | REDUNDANT | ruling.template.md (evidence, falsifier, re-test, revisit-by) is a strict superset; the quoted commandments carry none of those fields | 171-181 | n/a | | | out | |

## Conflicts for the user to rule on

Question 2 (row 3): add the optional end-of-run field to sweep-harness workers? Tension: retro's rule that an agent is not a reliable narrator of its own session. Recommendation: yes, as advisory input the orchestrator lists and never acts on unverified; it costs a line per item. Alternative: out, on the ground that the weekly maintainer already mines transcripts and a second signal needs an owner.

Question 3 (row 7): adopt a skills-consulted line in commit messages anywhere? Recommendation: out, until it costs a correction. Alternative: add it to the weekly maintainer's commit convention only.

Philosophy conflicts recorded, resolved for the incumbent, no ruling needed: the deletion heuristic versus preventive rules kept without evidence; the six-month reset versus one editable home.

## Corrections at ingest

- The /doctor feature list and "most coding agents have a built-in /doctor" are not restated (see currency check).
- "~6K tokens per session" and "removed 80% of the system prompt" are not imported.
- The article's failures.md filename collides with sweep-harness's orchestrator-only failures.md (different schema); no row adopts the name.
- The wizard's end-of-run prompt is rephrased in library style, not copied; no UTM-tagged wording lands anywhere.

## Flags

- Agent-directed content quoted in the article (the merge-queue AGENTS.md line, three SDK commandments, the wizard's end-of-run prompt): read as data, not acted on.
- Vendor post: every internal link carries newsletter UTM parameters and routes twice to posthog.com/self-driving. Evidence for implementation claims is real and openable; efficacy claims are unmeasured.
- Scrape chrome excluded.

## Rulings log

- 2026-09-02, proposed by this session. Awaiting the batch ruling on Questions 2 and 3; row 4 ratified by default unless objected to.
- 2026-09-02, Graham, batch ruling: "skip it all". Rows 3 and 4 out; Questions 2 and 3 answered no. Source verdict changed from HARVEST to SKIP. Reason given: narrow harvest not worth the maintenance surface. No side effects to reassign.
