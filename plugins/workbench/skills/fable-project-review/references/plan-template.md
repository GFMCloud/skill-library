<!--
INSTRUCTIONS FOR THE MODEL WRITING THIS PLAN (Fable 5, Phase 3) - delete this
comment block before presenting the plan to the user.

This file is the ONLY bridge between the review session and the execution
session. The executor is a cheaper model, in a brand-new session, with none
of this conversation available to it - no review notes, no back-and-forth,
no "as discussed." If a work item only makes sense to someone who sat
through the review, it is broken. Before finalizing, re-read every item and
ask: "could a model with zero context execute this correctly?" If the
answer is no, add whatever's missing - don't shorten it to save space.

Self-containment checklist (apply to every work item before finalizing):
- Exact file path(s), not "the config file" or "the main component"
- A verbatim current-state excerpt, so the executor can confirm it's editing
  the right thing before it edits anything
- A concretely described end state - not "fix this" or "clean this up"
- Acceptance criteria that don't require judgment to check, wherever possible
  (a command that exits 0, a string that's absent, a test that passes)
- Explicit non-goals, so the executor doesn't "improve" adjacent code
- No pronouns or references that only resolve inside the review session
  ("the issue above," "like we said," "per the discussion")

Keep every work item's ID stable once assigned (WI-01, WI-02, ...) - verify
mode references these IDs later, potentially across multiple follow-up plans.
-->

# Improvement Plan - [Project Name]

**Reviewed:** [YYYY-MM-DD]
**Reviewer:** Fable 5
**Executor:** [Opus 4.8 / Sonnet 4.6 - whichever this plan recommends]
**Plan version:** [v1, or v2 if a prior plan for this project exists]
**Supersedes:** [n/a, or the filename of the prior plan this replaces/extends]

## 1. Project goal

[One paragraph, in plain language, stating what this project is for. If the
project had a stated goal (README, doc, or the user gave one directly),
quote or restate it here. Every finding and work item below should trace
back to this goal - if it doesn't serve the goal, it shouldn't be in the plan.]

## 2. What this review covered

[Bullet list of what was actually inventoried - directory tree, specific
docs read, git log range, which files were opened. This tells the executor
what ground the review stands on, and tells the user what wasn't looked at.]

- [e.g., "Full source tree under src/, excluding node_modules and dist"]
- [e.g., "README.md, CONTRIBUTING.md"]
- [e.g., "git log --oneline -20"]
- [Anything explicitly NOT reviewed, and why - so gaps are visible, not silent]

## 3. Summary

[3-6 sentences. What's the overall state of the project? What's the single
biggest thing this plan fixes? No padding - if something's fine, that's not
mentioned here, it's just absent from the work items below.]

## 4. Execution order

[State the order work items should be executed in, and why. Most plans are
mostly priority order (Critical, then High, then Medium, then Low), but call
out any exceptions explicitly - e.g., "WI-04 must land before WI-02 because
WI-02 edits a file WI-04 renames." If items are independent and order truly
doesn't matter, say so, so the executor doesn't invent a dependency that
isn't there.]

1. WI-[NN] - [title]
2. WI-[NN] - [title]
3. ...

## 5. Work items

<!-- Repeat this block for every finding. Delete unused priority sections if
there are no items at that level - don't leave empty headers. -->

### Critical

#### WI-01: [Short, imperative title - e.g., "Fix unhandled null in checkout total"]

- **Priority:** Critical
- **Depends on:** [none | WI-0X - one sentence on why]
- **File(s):** [exact path(s) from repo root, e.g., `src/checkout/total.ts`]

**Current state** (as of this review):

```
[Verbatim excerpt - a few lines, with a line number reference if the file is
long, e.g. "lines 40-52" - showing the actual problem, not a paraphrase.]
```

**Problem:** [One or two sentences, fully self-contained. State what's wrong
and why it matters, without assuming the reader saw any prior discussion.]

**Desired end state:** [Concrete description of what the file/behavior/doc
should look like after this item is done. Describe the outcome, not just
the action - "the function returns 0 instead of throwing when the cart is
empty" not "handle the empty case."]

**Acceptance criteria:**
- [ ] [Mechanically checkable where possible - a command, a test, a grep
  that returns nothing, a specific behavior to trigger and observe]
- [ ] [Second criterion if needed]

**Non-goals for this item:** [What the executor should NOT do while touching
this file - e.g., "don't refactor the surrounding pricing logic," "don't
change the public function signature."]

**Context the executor needs:** [Anything else required to execute this
correctly with no other access - related files, a convention used elsewhere
in the codebase, a library version constraint, why a seemingly-obvious
alternative fix won't work.]

---

### High

#### WI-02: [title]

[Same structure as above.]

---

### Medium

#### WI-03: [title]

[Same structure as above.]

---

### Low

#### WI-04: [title]

[Same structure as above. Low-priority items can be terser, but never skip
file path, current state, end state, or acceptance criteria - "polish" items
are exactly the ones that get executed sloppily if under-specified.]

---

## 6. Global non-goals

[Things that apply across the whole plan, not just one item - scope fences
the executor should respect throughout. E.g., "Do not upgrade dependencies
as part of this plan," "Do not touch files under legacy/," "Do not change
the public API surface unless a work item explicitly says so."]

## 7. Handoff notes for the executor

[Anything the executor should know before starting that doesn't belong to
a single work item - e.g., "run the test suite before starting to confirm
your baseline is green," "commit after each work item, not all at once,"
"if an acceptance criterion can't be met as written, stop and flag it rather
than reinterpreting it."]

## 8. Verification tracking

<!-- Leave this table's Status column blank in the initial plan - it gets
filled in during verify mode, one row per work item, using its stable ID. -->

| ID | Title | Priority | Status | Evidence |
|----|-------|----------|--------|----------|
| WI-01 | [title] | Critical | | |
| WI-02 | [title] | High | | |
| WI-03 | [title] | Medium | | |
| WI-04 | [title] | Low | | |
