---
contract: v1
source: https://claude.com/blog/the-ai-native-sdlc-playbook
type: article
pin: fetched 2026-09-02T17:17:39Z, sha256 adfcd44e65105377bc05c3577a0193bb4f8bc1b77e3597e7ff4852b0ce1a213f (article body, nav chrome stripped)
reviewed: 2026-09-02
verdict: HARVEST
recheck: 2026-12-01 (WATCH row 9 only)
applied: the commit that adds this file (workbench 0.7.1)
evidence: docs/reviews/2026-09-02-ai-native-sdlc-playbook/ (cleanroom-review.md, comparison.md, decisions.md); scratch paths do not survive, so the three files are copied here
---

# ai-native-sdlc-playbook

**Verdict:** HARVEST. The article's core ideas are already rules here with their
originating failures attached; six fragments where a rule had no procedure or no
tool-layer enforcement behind it are worth taking, five landed as one-paragraph
edits and three changes to installed behavior await Graham's ruling.

**Ancestry:** none. No reference in either direction; the library's matching rules
predate the article. Convergent.

## What landed

- Row 1, Low-finding cap and CI-enforced exclusion: `plugins/workbench/skills/fable-project-review/SKILL.md` Phase 2, this commit.
- Row 2, trigger test before promotion: `docs/authoring-standard.md`, "The description is the router", this commit.
- Row 3, evals run on configuration change and gate the merge, binding from the first eval case: `docs/authoring-standard.md`, "Change hygiene", this commit.
- Row 4, behavioral regression routes to an eval case: `plugins/workbench/skills/retro/SKILL.md` §3 table, this commit.
- Row 5, red test first, committed, frozen: `plugins/workbench/skills/new-project/scripts/scaffold.sh` rule 6 and `references/conventions.md` SPEC.md §6, this commit.
- Row 9, σ-banded autonomy tiers: WATCH, recheck 2026-12-01; landing spot `pipeline-foundry` §8 if a project gains a metric with a rolling baseline.

## Open for Graham (proposed, not applied)

- Row 6, a PreToolUse hook freezing `tests/**` during a flagged fix task, M effort, for the python archetype. Currency check 2026-09-02: `Edit|Write` matchers, exit 2 blocking, and `${CLAUDE_PROJECT_DIR}` are all current.
- Row 7, `permissions.deny` for credential files in `~/.claude/settings.json`: out, Graham 2026-09-02. Declined after the trade-offs: the deny covers the Read tool only, blocks hard rather than prompting, and no credential-read incident is on record here. The prose rule stays the control.
- Row 8, an explanatory Bash gate hook on pushes and production writes: out, on recommendation, 2026-09-02.

## What was declined, and why

- Rows 10 to 25 (REDUNDANT): two-strike CLAUDE.md rule, advisory vs deterministic controls, plan-quality bar, rollback rehearsal, one source of truth, no mid-build approval prompts, done means verified, the intent/spec/plan chain, verifier subagent, worktree parallelism, the CLAUDE.md play, plan mode, feedback-loop mechanics, CI/CD order, auto-mode conditions, intent capture. Each is in `~/.claude/CLAUDE.md` or a library body with the failure that produced it; the article attaches none.
- Rows 26 to 29 (DISCARD): measurement definitions with no baseline, Claude Security (Enterprise beta), Claude Tag (Slack beta), the self-contradicting dependency graph.
- The article's runnable snippets: `production-gate.sh` and `agent-evals.yml` are defective as written (see comparison.md §7).

## Flags

Quoted with path in `decisions.md` "Flags": skill, subagent, CLAUDE.md, and REVIEW.md bodies written as imperatives to an agent (L446 to L456, L527 to L529, L591 to L592, L729 to L742); instructions to install into `.claude/skills/`, `.claude/settings.json`, and managed settings (L407, L777, L822); `npm install -g @anthropic-ai/claude-code` in a CI example (L657). All inside fenced examples; none acted on. Every outbound link is an Anthropic property and no outcome claim is cited.

## Re-review trigger

The pin moving (re-fetch and compare the sha256); `claude plugin eval` leaving early access, which would make row 3's mechanism real; any project here gaining a metric with a rolling baseline (row 9); or the recheck date 2026-12-01.
