---
name: "evidence-report"
description: "Format executed evidence into a report that states what was checked, what the check returned, and what was not checked. Use when presenting verification results, acceptance checks, or any claim that work is done."
metadata:
  maturity: stable
  version: 1.1.0
  reviewed: 2026-09-02
---

# evidence-report

The reporting half of `proof-of-work`. That skill sets the standard for what
counts as evidence; this one is how the evidence gets presented so a reader can
tell verified from assumed at a glance.

## The format

One block per claim. All four fields, no exceptions — a block missing `OUTPUT`
is an assertion wearing a report's clothing.

```
CLAIM:   foundry-core's skill lands in the plugin cache with real content
CHECK:   wc -c ~/.claude/plugins/cache/gfm-foundry/foundry-core/*/skills/proof-of-work/SKILL.md
OUTPUT:  1636 /root/.claude/.../proof-of-work/SKILL.md
VERDICT: VERIFIED — rules out #53948 (empty skills/ dir, success reported)
```

- **CLAIM** — the falsifiable statement, in the form it will be repeated.
- **CHECK** — the command or action, verbatim and re-runnable. Not "validated
  the manifest."
- **OUTPUT** — what actually came back, quoted. Trim to the decisive lines;
  never paraphrase them.
- **VERDICT** — `VERIFIED` / `UNVERIFIED` / `FAILED`, plus what the result
  rules out. A verdict that does not say what failure mode it eliminates is
  decoration.

## The not-verified list is mandatory

Close every report with what was **not** checked and why. This is the section
that makes the rest of the report trustworthy, and the one most likely to be
dropped.

```
NOT VERIFIED
- Install over the GitHub source — container has no gh auth. Needs Graham.
- disallowedTools enforcement — frontmatter parsed, enforcement untested.
```

An omitted not-verified list reads as "everything was checked." Silence and
completeness look identical in a report, which is precisely why the list has to
be explicit.

## Rules

- **Report a clean pass.** State how many claims were checked and that they
  returned clean. A verification that produces no output is indistinguishable
  from a verification that never ran.
- **Never summarise output you did not read.** If the check produced 400 lines,
  quote the decisive ones and say the rest were scanned for the specific thing
  you were looking for.
- **Count errors, not adjectives.** Tools emit reassuring words alongside
  failures. `gfm-foundry`'s normal clean state is literally "Validation passed
  with warnings" — five warnings by design, one per plugin, from the deliberate
  no-`version` policy. The number that matters is the error count.
- **Attach the identifier.** A commit SHA, a byte count, a row count, a
  timestamp. An acceptance record that does not name what it ran against cannot
  be re-checked later, and item 3 shipped exactly that defect before it was
  caught.
- **Never add isolated measurements together.** Two improvements measured
  separately do not sum when combined; they overlap, and the combined figure is
  usually smaller than the arithmetic total. A claim about several changes at
  once is measured with all of them applied, on the complete workflow, or it is
  reported as separate claims that were never combined.

## When evidence cannot be produced

Say so in the verdict line and put it in the not-verified list. Do not
substitute reasoning about why it probably works. `UNVERIFIED` with a reason is
a useful report; a confident paragraph is not.
