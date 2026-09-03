---
contract: v1
source: https://github.com/multica-ai/andrej-karpathy-skills
type: skill-collection
pin: 2c606141936f1eeef17fa3043a72095b4765b9c2
reviewed: 2026-09-02
verdict: HARVEST
recheck: 2026-12-01
applied: pending (filled by the follow-up commit that names this one)
evidence: docs/reviews/2026-09-02-andrej-karpathy-skills/ (cleanroom-review.md, comparison.md, currency-check.md, decisions.md)
---

# andrej-karpathy-skills

**Verdict:** HARVEST. One short skill restating four principles from a single X post; two are redundant against the harness prompt and the global working agreements, one contradicts them, and two fragments are real gaps that are banked here until they earn a line.

**Ancestry:** none. No file in the library or ~/.claude names the source; independent origin.

## What landed

- Row 3, step-to-verify pointer: one bullet "Declare the check before the step" in `plugins/foundry-core/skills/proof-of-work/SKILL.md`, version 1.0.0 to 1.1.0, foundry-core 0.2.2, CHANGELOG entry dated 2026-09-02. Ratified by Graham.
- Rows 1 and 2 (orphan-cleanup asymmetry, match existing style, code-shape anti-overengineering): banked, not written. The global CLAUDE.md economy rule requires two corrections; a 60-day transcript scan found one (over-engineering, process shape) and zero for drive-by edits, style drift, or deleted code. The block below is the paste for when the second correction lands, target `~/.claude/CLAUDE.md` under Working agreements.

### Banked block (rows 1 and 2)

```markdown
### Surgical edits

- When an edit orphans an import, variable, or function, remove it in the same
  change. Dead code that was already dead before the edit stays; mention it, never
  delete it unless asked. Check: every removed line traces to something the edit made
  unused.
- Match the file's existing style (quotes, type hints, docstrings, whitespace) even
  where a different choice would be better. A diff that changes lines the request
  did not touch is wrong even when every changed line is an improvement.
- Inside the requested scope, no abstraction for single-use code, no configurability
  or flexibility nobody asked for, no handling for cases that cannot occur. Add the
  layer when the second caller exists, not before.
```

Source: `skills/karpathy-guidelines/SKILL.md` lines 27-30 and 39-47 at the pin, restyled (no em dashes, scope/action/exception/check shape, the circular "senior engineer" and "200 lines" lines dropped).

## What was declined, and why

- Principle 1, Think Before Coding: redundant against the harness prompt and "Intent before execution", and its stop-and-ask default contradicts the "Standing defaults" section. Headless runs cannot honor it.
- Principle 2 and 3 opening bullets (scope discipline): the harness prompt already says "the requested scope is the deliverable".
- Principle 4, Goal-Driven Execution: proof-of-work and evidence-report cover it with an escape hatch and non-code artifact classes the source lacks.
- EXAMPLES.md: orphaned in its own repo, and the test-first example is broken (Python sort is stable; the before and after code are identical; the test passes 10/10 against the unfixed function, proven by execution). Revisit only if a coding-hygiene skill with a references directory ever exists.
- "These guidelines are working if" line: four unmeasured signals; the authoring standard's eval-case rule is stronger.
- The plugin as an install unit: description with no negative scope would fire on all coding work beside proof-of-work; no LICENSE file; no commit since 2026-04-20 and every PR since closed by its own author.

## Flags

Quoted, not acted on:
- `README.md:122-126` asks to append the file to the reader's CLAUDE.md with `echo "" >> CLAUDE.md` then `curl ... >> CLAUDE.md`. Unguarded; appended to this machine's global file it would contradict "Intent before execution" in the same file.
- `README.md:104-111` asks for `/plugin marketplace add` and `/plugin install`.
- `.cursor/rules/karpathy-guidelines.mdc:3` `alwaysApply: true`.
- `README.md:3-5` promotion of the author's other project and X account.
- `SKILL.md:9` sole authority is `https://x.com/karpathy/status/2015883857489522876`, not fetched.

## Re-review trigger

- The pin moving with a maintainer commit (none since 2026-04-20 as of 2026-09-02); PRs #188 (self-check), #196 (fix the sort example), or a no-test fallback merging.
- The second user correction in categories A to D of the transcript scan, which promotes the banked block into `~/.claude/CLAUDE.md`.
- Recheck date 2026-12-01.
