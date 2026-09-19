# Finding discipline for the reviewer

Given to the reviewer subagent alongside the goal block and the change when the change is
code. It cuts the two ways a model reviewer wastes a verdict: findings it cannot stand
behind, and stock complaints that are usually wrong.

Adapted from the ECC project's `code-reviewer` agent (MIT, v2.2.1), reviewed 2026-09-17.
Record: `maintainers/reviews/2026-09-17-ecc/`. Both judges of that review found the agent itself
superseded by this skill and asked for these two lists only.

## Four questions before an issue goes in the verdict

Answer all four. On any "no" or "unsure", lower the severity or drop the issue.

1. **Can I cite the exact line?** File and line. "Somewhere in the auth layer" is dropped.
2. **Can I name the failure?** The input, the state, and the bad outcome. With no trigger
   to name, this is pattern-matching, not review.
3. **Did I read around it?** Callers, imports, tests. Many apparent defects are handled
   one frame up or ruled out by a type.
4. **Is the severity defensible?** A missing doc comment is never high. Inflated severity
   costs more trust than a missed finding.

This does not loosen the verdict. An issue that survives the four questions and blocks
the goal still fails the change.

## Usually false in JavaScript, TypeScript and React code

Skip these unless there is evidence specific to this codebase. Known weakness: the list
comes from one source project's experience and has not been measured here.

- "Add error handling" where the caller or the framework already handles it (error
  middleware, error boundaries, an upstream `.catch`, a top-level `try`).
- "Missing input validation" on an internal function whose callers validate. Trace one
  caller first.
- "Magic number" for well-known constants: HTTP status codes, `1000` ms, `60`, `24`,
  `1024`, index `0` or `-1`, a single-use local whose name says what it is.
- "Function too long" for an exhaustive `switch`, a config object, a test table or
  generated code. Length is not complexity.
- "Missing doc comment" on a self-describing internal helper.
- "Prefer `const`" where the variable is reassigned. Read the whole function.
- "Possible null dereference" where the previous line narrows the type or a guard is in
  scope. Follow the type flow.
- "N+1 query" on a fixed, tiny loop or a path that already batches.
- "Missing `await`" on a deliberately detached call (logging, metrics, a queue push).
  Look for a comment or a `void` prefix.
- "Should use TypeScript" in a JavaScript-only file. Match the project.
- "Hardcoded value" in a test fixture or a documentation example. Tests should have
  hardcoded expectations.
- Security theater: `Math.random()` for jitter or sampling; `eval` in something that is
  explicitly a code-loading surface.
