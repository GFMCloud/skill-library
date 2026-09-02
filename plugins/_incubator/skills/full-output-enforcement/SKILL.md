---
name: full-output-enforcement
description: >-
  Overrides default LLM truncation. Enforces complete code generation, bans
  placeholder and "rest follows the same pattern" shortcuts, and handles a
  token-limit split into a clean resumable breakpoint instead of a compressed
  ending. Use when the user says "full implementation", "complete file", "no
  placeholders", "don't truncate", "write the whole thing", "all N components",
  or "no `// ...`", and on any task whose value depends on exhaustive,
  unabridged output. Not for one-line answers, quick questions, or
  explanations, where brevity is correct.
metadata:
  maturity: incubator
---

# Full-Output Enforcement

Applies when the user asked for something in full. Not for one-line answers, quick
questions, or explanations, where brevity is correct.

## Baseline

Treat every task as production-critical. A partial output is a broken output. Do not
optimize for brevity. Optimize for completeness. If the user asks for a full file,
deliver the full file. If the user asks for 5 components, deliver 5 components. No
exceptions.

## Banned Output Patterns

The following patterns are hard failures. Never produce them:

**In code blocks:** `// ...`, `// rest of code`, `// implement here`, `// TODO` (scoped
below), `/* ... */`, `// similar to above`, `// continue pattern`, `// add more as
needed`, bare `...` standing in for omitted code

**In prose:** "Let me know if you want me to continue", "I can provide more details if
needed", "for brevity", "the rest follows the same pattern", "similarly for the
remaining", "and so on" (when replacing actual content), "I'll leave that as an
exercise"

**Structural shortcuts:** Outputting a skeleton when the request was for a full
implementation. Showing the first and last section while skipping the middle.
Replacing repeated logic with one example and a description. Describing what code
should do instead of writing it.

**TODO scope.** The `// TODO` ban binds when the user asked for a full
implementation: a placeholder standing in for code or content requested in full is a
hard failure. An instructed placeholder (an image slot the user must fill, such as
`<!-- TODO: hero product photo, 1600x1200 -->`) or a genuine tracked TODO in
otherwise complete code is not banned.

## Execution Process

1. **Scope.** Read the full request. Count how many distinct deliverables are expected
   (files, functions, sections, answers). Lock that number.
2. **Build.** Generate every deliverable completely. No partial drafts, no "you can
   extend this later."
3. **Cross-check.** Before output, re-read the original request. Compare your
   deliverable count against the scope count. If anything is missing, add it before
   responding.

## Handling Long Outputs

When a response approaches the token limit:

- Do not compress remaining sections to squeeze them in.
- Do not skip ahead to a conclusion.
- Write at full quality up to a clean breakpoint (end of a function, end of a file,
  end of a section).
- End with:

```
[PAUSED: X of Y complete. Send "continue" to resume from: next section name]
```

On "continue", pick up exactly where you stopped. No recap, no repetition.

## Quick Check

Before finalizing any response, verify:
- No banned patterns from the list above appear anywhere in the output
- Every item the user requested is present and finished
- Code blocks contain actual runnable code, not descriptions of what code would do
- Nothing was shortened to save space

Scope boundary: this skill prevents truncation as output is generated;
`turn-reduction:output-lint` lints a finished message for unsubstituted placeholders,
and `foundry-core:proof-of-work` verifies a finished artifact.
