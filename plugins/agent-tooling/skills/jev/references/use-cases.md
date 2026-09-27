# Jev use-case shapes

Twelve shapes of work where Jev has been shown to fit, or shown not to. Use it in Step 1 to
name what a candidate decision point is, and in Step 2 to check its fit signals. Sources:
**[docs]** TypeSafe's own pattern and cookbook pages (numbers there are vendor claims);
**[repo]** repos reviewed in `~/work/jev-lab/REPORT.md` section 5, pinned in its SOURCES.md;
**[lesson]** measured in `~/work/jev-lab/lab/LESSONS.md`. Doc paths are relative to
`https://docs.typesafe.ai/`; add `.md` to any page path for Markdown.

For every shape the fit gate is the same: can code assemble the evidence in full?

## 1. Routing and intent classification

- **Looks like:** incoming messages, tickets or requests sent to one of several handlers.
- **Evidence code assembles:** the message itself, plus any account or order fields.
- **Questions:** one Choice over the handlers with an `other` option; speculative
  follow-up Choices for each branch in the same call; confidence decides act or ask.
- **Shown in:** [docs] `patterns/intent-routing`, `primitives/choice` (support triage),
  `demos/smart-home`; [repo] json-render (Choice-only evaluator), ellipsis-dev/blink.
- **Fit notes:** strong when the handlers are a fixed list. Weak when the right handler
  depends on history the message does not carry.

## 2. Record matching, dedupe and entity alignment

- **Looks like:** "is this the same person, product, player or company as that one?";
  fuzzy string matching with a tiebreak rule; a review CSV of ambiguous matches.
- **Evidence code assembles:** the new record and each candidate record, field by field.
- **Questions:** one Noul per candidate pair, the candidate placed in structured
  `instructions` and the question text fixed; optional Nouls per field that surface which
  fields disagree; threshold in code, middle to review. When a cheap matcher (fuzzy
  string score, search) already ranks candidates, pass its top three to one Choice with a
  `none` option instead of judging only its first pick: judging one candidate cannot
  recover when the matcher picked the wrong record ("The Road" against "On the Road").
- **Shown in:** [docs] `primitives/noul` (resume duplicate check), `cookbooks/entity_alignment`;
  [test] the 2026-09-27 fresh-session test of this skill, where the control session found
  the top-three form and the skill session only flagged the gap.
- **Fit notes:** the strongest general fit found: both records already exist in code.
  On this machine: fantasy-draft-data's `match_names()` (ids.py) and its
  `id_match_review.csv` of hard cases is a candidate, untested as of 2026-09-27.

## 3. Checklist and compliance screening

- **Looks like:** one document checked against a list of conditions (a policy, a
  regulation, a review checklist, spam or phishing signals).
- **Evidence code assembles:** the document, split into named fields where it can be.
- **Questions:** one Noul per condition, all in one call; combine in code.
- **Shown in:** [docs] `cookbooks/parallel_questions` (13-question checklist),
  `concepts/how-to-build-with-system-one` (spam decomposed into six Nouls),
  `cookbooks/llm_guardrails`.
- **Fit notes:** strong when each condition is observable in the text. A condition that
  needs outside facts belongs in a verification step before Jev.

## 4. Composite scoring and prioritisation

- **Looks like:** "how urgent / severe / good is this?", a ranking, a priority queue.
- **Evidence code assembles:** the item.
- **Questions:** one Score per dimension with levels that describe situations, not
  degrees; normalise each by its top level; weights in code.
- **Shown in:** [docs] `patterns/composite-scoring`, `primitives/score`.
- **Fit notes:** good when the dimensions are independent. A level list you cannot
  describe distinctly means the dimension is not ready.

## 5. Retrieval, re-ranking and "which record applies"

- **Looks like:** choosing which rule, skill, document or passage bears on an item.
- **Evidence code assembles:** the item and a shortlist of candidate records in full.
- **Questions:** one Noul per item-candidate pair ("is this aimed at the same problem?"),
  sorted by value; a second call on the top few if a closer judgment is needed.
- **Shown in:** [docs] `cookbooks/rerank_typesafe`, `cookbooks/skill_suggestion`,
  `cookbooks/classifying_rag_passages`; [lesson] Lesson 5: the same_problem fan-out named
  the exact rule for both contradiction items (0.89, 0.79).
- **Fit notes:** a cheap front end for other shapes; often the most useful part.

## 6. Verifying an extraction or a claim against its source

- **Looks like:** checking that an extracted field, a citation or a quoted figure matches
  the source text; a cheap extractor whose output needs a check.
- **Evidence code assembles:** the source text and the extracted value.
- **Questions:** a Noul per field ("does `extracted_value` match `field` in `source_text`?")
  or a Choice among regex-found candidates; escalate failures to a stronger model.
- **Shown in:** [docs] `cookbooks/citation_check`, `cookbooks/sde_cascade`,
  `cookbooks/pre_parsed_value_extraction_cookbook`, `primitives/advanced`.
- **Fit notes:** strong; the source is already in hand. Numbers and dates are compared in
  code, not by Jev.

## 7. Walking a taxonomy

- **Looks like:** classifying into a deep hierarchy (product categories, codes, a skill
  catalogue tree).
- **Evidence code assembles:** the item and the tree.
- **Questions:** one Choice per level, each option's value its subtree; beam search over
  the probabilities when the split is close.
- **Shown in:** [docs] `primitives/advanced`, `cookbooks/hierarchical_classification`,
  `cookbooks/classification_using_confidence`.

## 8. Confidence-gated actions in an agent or tool

- **Looks like:** an agent or script about to take an action (click, call a function,
  run a command) that should act, confirm or abstain.
- **Evidence code assembles:** the request and the available actions or arguments.
- **Questions:** Choices over actions and closed-set arguments; a Noul that flags
  destructive actions with a stricter bar.
- **Shown in:** [docs] `patterns/confidence-routing`, `cookbooks/function_calling`;
  [repo] lahfir/agent-desktop `scripts/jev/policy.mjs` (best gate example),
  browser-use/jev-ultrafast (speculative fan-out; indexes responses without checks,
  issue #133).
- **Fit notes:** sends on-screen or request content to TypeSafe on every turn; check the
  data decision first.

## 9. Search inside a document or a repo

- **Looks like:** "where does this document or codebase handle X?"
- **Evidence code assembles:** the document split into numbered lines or blocks, or a
  file tree.
- **Questions:** a Choice whose options are line or file ids, plus a Noul "does the
  document contain an answer at all?".
- **Shown in:** [docs] `cookbooks/semantic_find`, `cookbooks/autoformat`; [repo]
  dzhng/jevgrep, ellipsis-dev/blink.

## 10. Features for a downstream model

- **Looks like:** free text that should become numeric inputs to a classical model.
- **Questions:** many Nouls and Scores as features; the downstream model learns weights.
- **Shown in:** [docs] `cookbooks/autoresearch_feature_discovery`.

## 11. Guarding an LLM's input or output

- **Looks like:** screening prompts or responses for hazards before they reach a user or
  a tool.
- **Questions:** hazard Nouls plus a severity Score; pass, review, block or route in code;
  validate every response before trusting it.
- **Shown in:** [docs] `cookbooks/llm_guardrails`; [repo] sharziki/semdecide
  (`validate_response()`), jkudish/jev-mcp (fail-closed validators).

## 12. Novelty and contradiction against a rulebook (a weak fit, measured)

- **Looks like:** "is this idea already covered by what we have, does it extend it, or
  does it argue we are wrong?"
- **Evidence code assembles:** the item and the rule texts, if they can be pulled in full.
- **What happened:** [lesson] the weekly scout's triage. Jev separated "same problem or
  not" and caught contradictions an item states outright. It could not reproduce the
  scout's same-versus-extends call (that turns on whether the extras matter to Graham)
  and missed contradictions whose deciding fact came from documents the orchestrator
  fetched. Verdict: a weak fit, because the evidence takes research to assemble.
- **Fit notes:** use shape 5 as a pointer to the record a person should read; keep the
  final call with whoever does the verification.

## Not a fit at all

Generating or rewriting text (llama-offload or Claude); arithmetic, counting and date
comparison (code); anything whose deciding fact must be fetched or reasoned out in several
steps; private data while `~/work/jev-lab/DATA-DECISION.md` says public only.
