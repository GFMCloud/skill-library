---
contract: v1
source: https://github.com/bojieli/ai-agent-book (docs/en/README.md; English text in book-en/)
type: article
pin: git 8b45707504df0631be097f79ba8ec3fea245ff23 (2026-09-02T03:04:19Z)
reviewed: 2026-09-02
verdict: HARVEST
recheck: n/a
applied: the commit that adds this file (workbench 0.7.2) for the six S rows; rows 4 and 21 by PR from branch harvest/ai-agent-book-stable-rows (see "Pending by PR")
evidence: docs/reviews/2026-09-02-ai-agent-book/ (cleanroom-review.md, comparison.md, decisions.md); scratch paths do not survive, so the three files are copied here
---

# ai-agent-book

**Verdict:** HARVEST. A 190k-word practitioner book on building LLM agent harnesses; this
library drives Claude Code sessions and builds no harness, so half of its 30 strongest
techniques have no consumer here and most of the rest are already rules in the global
working agreements or a library skill. Eight fragments fill real gaps in existing files.
No new skill.

**Ancestry:** none. Neither project mentions the other in tree or history (grep and git
log, both directions). Convergent practice.

## Method

Eleven clean-room reviews (one per chapter, `claude -p --setting-sources "" --model sonnet`,
read-only tools, article rubric), one clean-room synthesis at the CLI default model, one
Sonnet comparison agent against 24 incumbent skills plus the authoring standard and the
global CLAUDE.md. The book is too large for one headless context, which is why the clean
room was chunked by chapter. Companion code was cloned to read; nothing was run.

## What landed

- Row 2, ablation diagnostic for an underperforming skill or prompt:
  `plugins/workbench/skills/model-effort-advisor/references/decision-rubric.md`,
  "Diagnosing a skill or prompt that underperforms", this commit.
- Row 3, boundary set and retention set for any fix: `docs/authoring-standard.md`,
  "Change hygiene", this commit.
- Row 9, paired per-item wins and a stated sample size or interval:
  `plugins/workbench/skills/experiment-harness/templates/run.template.md`, Verdict field,
  this commit.
- Row 19, reviewer sees the artifact and criteria, never the builder's rationale:
  `plugins/workbench/skills/model-effort-advisor/references/subagent-routing.md`,
  "Build/Review Pairing", this commit.
- Row 22, descriptions carry negative scope and cost; fix the description before
  changing the model: `docs/authoring-standard.md`, "The description is the router",
  this commit.
- Row 31, rules shaped as scope, action, exception, verification:
  `docs/authoring-standard.md`, "Body", this commit.

## Pending by PR

- Row 4, never sum isolated optimization savings: `plugins/foundry-core/skills/evidence-report/SKILL.md`,
  "Rules", version 1.0.0 to 1.1.0.
- Row 21, head-and-tail excerpt with an explicit omission marker:
  `plugins/turn-reduction/skills/capability-preflight/preflight.py`, `excerpt()`,
  version 1.0.0 to 1.1.0, proven by a fixture whose only failure line sits past the head window.

Both are stable skills, so they change by PR per the authoring standard. Graham ruled
"go with the PR" on 2026-09-02. This record is updated with the merge commit when it lands.

## Ruled by Graham, 2026-09-02

- Question 1, stable-skill rows 4 and 21: go with the PR.
- Question 2, philosophy conflict between "a red validator is a bug in the content" (global
  CLAUDE.md) and the book's "the evaluation system may have broken first" (chapter 7):
  record the reconciliation, no CLAUDE.md change. They reconcile through the existing rule
  that a validator is trusted only after being proven by deliberate failure; the
  red-validator rule applies to a proven validator, the book's warning to an unproven one.

## What was declined, and why

- Rows 1, 5, 6, 8, 10, 11, 13 to 16, 18, 25 to 29 (COMPLEMENT, no consumer): KV-cache prefix
  discipline, contextual retrieval, sandbox architecture, Pass@k vs Pass^k reporting,
  idempotent retries, progressive tool disclosure, RL gating and masking, LoRA defaults,
  RAG chunking, retrieval-layer permissions, coding-agent tool design, interruption
  protocol, event classification, judge rubrics, first-error attribution. True, and nothing
  on this machine builds the thing they apply to.
- Rows 7, 12, 17, 20, 23, 24, 30, 32 (REDUNDANT): server-side ground truth, code-maintained
  counts, evidence is not instruction, proposer-reviewer gates, architecture escalation,
  recovery ceilings, multi-agent locking, rule-list bloat. Each is already in the global
  CLAUDE.md or a library body, usually with a stricter evidence bar than the book meets.
- No number from the book was imported. Its headline figures (30%/45% ablation deltas,
  15 vs 21 iterations, 60% to 95% recovery, 70 to 80% distillation recovery) are disclaimed
  or contradicted by the book's own companion repositories; the 52.8% to 66.5% harness
  result is attributed but never cited. Details in cleanroom-review.md sections 6 and 8.

## Flags

None acted on. Pedagogical prompt-injection strings inside the anti-injection section
(`book-en/chapter2.md:731,739,751,753`); descriptive discussion of CLAUDE.md, AGENTS.md,
SOUL.md and MEMORY.md with no instruction to create or install any (`book-en/chapter5.md:92`);
a sponsor referral link with a promo code in `docs/en/README.md`. Nothing in the book is
addressed to an agent.

## Re-review trigger

The pin moving past `8b45707` on the English text of chapters 7 or 9 (evaluation and
continual evolution, the two chapters whose evidence held up under recomputation); the
library gaining a skill that builds an agent harness or an eval loop, which would turn
several COMPLEMENT rows into candidates; or the eval-case rule in the authoring standard
acquiring its first real case, when row 3's wording gets tested against practice.
