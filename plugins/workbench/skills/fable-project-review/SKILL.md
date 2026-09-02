---
name: fable-project-review
description: Run a deep Fable 5 review of an existing project and produce a self-contained improvement plan that a cheaper model (Opus 4.8 or Sonnet 4.6) executes in a fresh session. Use whenever the user wants a full review, audit, or feedback loop on something already built - "review this project", "what would you improve", "run a Fable review", "audit what I've built", "tear this apart", "write an improvement plan" - or wants to hand execution of improvements to another model. Also covers verify mode, re-reviewing a project against a prior improvement plan after execution. Trigger even if the user doesn't say "skill" or "Fable", as long as the goal is a comprehensive review of an existing project with actionable follow-up. Works in Claude Code repos and Claude.ai/Cowork projects.
metadata:
  maturity: incubator
---

# Fable Project Review

This skill splits judgment from labor. Fable 5 does the expensive thinking - a deep review of an existing project - and writes a self-contained improvement plan. A cheaper, faster model (Opus 4.8 or Sonnet 4.6) then executes that plan in a fresh session with clean context. The plan file is the only bridge between the two sessions, so it has to stand completely on its own. Everything below serves that constraint.

The full loop: review -> plan -> execute -> verify. This skill handles review, plan, handoff, and verify. Execution happens elsewhere, on purpose.

## Phase 0 - Model check

The premise here is expensive judgment, cheap execution. Check which model is powering the current session (it's stated in the system prompt). If it isn't Fable 5, say so and let the user decide: restart on Fable 5, or proceed anyway knowing the review depth is the whole point of the skill. Don't silently proceed on a different model.

## Phase 1 - Recon

Read broadly before judging. A review built on a partial read produces confident nonsense, so inventory first. What to inventory depends on the surface:

**Claude Code / repo:**
- Directory tree (skip node_modules, .git internals, build artifacts)
- README and any docs
- `git log --oneline -20` for recent trajectory
- Entry points and config files, then the core source files
- Any prior `improvement-plan-*.md` or `verification-*.md` from earlier runs of this skill

**Claude.ai / Cowork project:**
- Project knowledge files
- Uploaded files and artifacts available in the session
- Project description or instructions if present

Also capture the project's stated goal. If no README or doc states one, ask the user for a one-sentence goal before reviewing. A review without a target is just taste - the goal is what turns "I'd do this differently" into "this doesn't serve the purpose."

## Phase 2 - Review

Review the whole project, not just code. Dimensions:

1. **Architecture & structure** - does the organization match the project's size and purpose? Look for premature abstraction, god files, tangled dependencies, missing separation.
2. **Code quality** - correctness risks, error handling, duplication, dead code, hardcoded values, naming.
3. **Docs** - does the README match reality? Stale commands, references to files that don't exist, missing setup steps, undocumented behavior.
4. **UX / design** - for anything with a surface (UI, CLI output, generated documents, web pages): readability, visual hierarchy, friction, error states.
5. **Consistency** - naming conventions, formatting, patterns applied unevenly across the project.
6. **Goal gaps** - what the stated goal promises that the project doesn't deliver yet.

Rank findings by severity: **Critical** (broken or actively misleading), **High** (will bite soon), **Medium** (friction), **Low** (polish). Tie every finding to specific files and lines or sections - a finding without a location isn't actionable, and the executor can't fix what it can't find.

Don't pad. If a dimension is clean, say so in one line and move on. The user wants signal, and a review that manufactures findings to look thorough erodes trust in the real ones.

Cap Low findings at five per review and summarize the rest as a count. Do not report anything a formatter, linter, or CI check already enforces, and nothing under a generated path. Those are noise wearing a finding's clothing, and they bury the items the executor should reach first.

## Phase 3 - Write the improvement plan

Read `references/plan-template.md` and follow it. Write the plan to the project root (or the output directory on Claude.ai) as `improvement-plan-YYYY-MM-DD.md`. If a plan with that name already exists, append `-v2` rather than overwriting - the history matters for verify mode.

The plan will be executed by a model with zero access to this session. Write every work item so that model can execute without guessing:

- Exact file paths
- A current-state excerpt (a few lines showing the problem)
- The desired end state, described concretely
- Acceptance criteria, mechanically checkable where possible
- Explicit non-goals so the executor doesn't freelance

Order items by priority and note dependencies between them. Any sentence in the plan that only makes sense with this session's context ("as discussed", "the issue above", "like we said") is a defect - the executor will stall or guess.

## Phase 4 - Checkpoint

Present the plan to the user before generating the handoff, and stop. This pause is deliberate: execution can be hours of work, and the plan is the cheapest place to cut, reorder, or edit. Don't produce the handoff package until the user signs off on the plan.

## Phase 5 - Handoff package

Generate an executor kickoff matched to the user's surface, and recommend a model with a stated lean (the user can override):

- **Opus 4.8** (`claude-opus-4-8`) - multi-file refactors, work items with residual ambiguity, judgment calls likely during execution
- **Sonnet 4.6** (`claude-sonnet-4-6`) - well-specified mechanical execution where the plan leaves little to interpret

**Claude Code:**

```
claude --model <model-id> "Read improvement-plan-YYYY-MM-DD.md at the repo root and execute it item by item in priority order. Check each item's acceptance criteria before marking it done. Stay inside the plan's scope - non-goals are listed in the plan."
```

**Claude.ai / Cowork:** a paste block for a fresh session containing the same instructions, plus a note telling the user to attach the plan file - and the project files themselves if the fresh session won't already have access to them.

The kickoff must never reference the review session. If the executor needs something, it belongs in the plan.

## Verify mode

This is what closes the loop. When a prior `improvement-plan-*.md` exists and the user asks to verify (or re-runs the review after execution), re-review the project against that plan's acceptance criteria specifically. For each work item, mark **Done / Partial / Missed** with evidence - the file and what changed or didn't. Then check for regressions the execution introduced outside the plan's scope.

Write the result as `verification-YYYY-MM-DD.md` next to the plan. If items were missed or partial, offer to cut a follow-up plan containing only the remainder - same template, new file.

## File handling

- Never overwrite prior plans or verification reports - version with a date or `-v2`
- Plans and reports are internal docs: kebab-case naming
- On Claude.ai, save outputs somewhere the user can download them and present the files when done
