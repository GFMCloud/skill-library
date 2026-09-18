---
name: overengineering-review
description: >-
  Review a diff or a whole repository for unnecessary code and abstraction only, and
  report what to cut: dead flexibility, abstractions with one implementation, config
  nobody sets, hand-rolled standard-library functions, dependencies the platform already
  ships. One line per finding with the quoted code and, for any "unused" or "only one
  caller" claim, the executed check that shows it. Use when the user says "is this
  over-engineered", "what can we delete", "review for over-engineering", "find bloat",
  "audit this repo for complexity", or "simplify review". It lists cuts and applies
  nothing. Not a correctness, security or performance review (use orch-review,
  code-review or security-checklist, and this skill says in its report that those were
  not done). Not the built-in /simplify, which edits the diff in place. Not a gate on a
  change spec (review-pair). Repo scope is a long read; it reports the directories it
  did not cover.
metadata:
  maturity: incubator
---

# overengineering-review

Find code that does not need to exist. The best outcome of this review is a shorter
diff or a smaller repository; a finding that does not name what replaces the cut code
(possibly nothing) is not a finding.

Built 2026-09-18 from a `toolkit-review` set run: nothing installed reviewed for
unnecessary code, and both judges named the two candidate items that did
(`ponytail-review`, `ponytail-audit`, `DietrichGebert/ponytail` at e3ba2aa, MIT). The tag
set is theirs. The evidence contract, the coverage report and the equivalence rule are
this library's, added because the candidates had no verification of their own.

## Inputs

- **Scope:** `diff` (default when there are uncommitted changes or the user names a PR
  or base ref) or `repo` (the user asks about a codebase, a directory, or "bloat").
- For `diff`: the base ref. Default `origin/main`; say which was used.
- For `repo`: the root, and any directory the user excludes. Vendored code, generated
  output and lockfiles are excluded without asking.

## The five tags

Every finding carries exactly one.

- `delete:` dead code, an unused flag or option, a speculative feature. Replaced by
  nothing.
- `yagni:` an interface or base class with one implementation, a factory with one
  product, a wrapper that only delegates, a config value nothing sets, a layer with one
  caller. Replaced by the inlined thing, until a second caller exists.
- `stdlib:` a hand-rolled version of something the language's standard library ships.
  Name the function.
- `native:` a dependency, or code, doing what the platform or framework already does.
  Name the feature.
- `shrink:` the same logic in fewer lines. Show the shorter form.

## Evidence contract

A finding is one line:

```text
<file>:L<start>[-<end>] <tag> <what to cut>. <what replaces it>.  evidence: <quoted code>  check: <command> → <output> | not-checked: <reason>
```

- **The quoted code exists at the cited line.** When a finding is written, the quote is
  copied from the file, not recalled. Proven by: `sed -n '<start>,<end>p' <file>` shows
  it. A finding whose quote cannot be found at its line is dropped, not reworded.
- **A claim about the rest of the codebase carries its check.** `delete:` and `yagni:`
  findings assert something about code outside the cited lines: nothing calls this,
  nothing sets this, there is one implementation. When a finding makes that claim, run
  the search that would refute it and record it as `<command> → <output>` (for example
  `git grep -n "RetryPolicy(" → 1 match, src/client.py:40`). Unless the search cannot be
  run or cannot see the usage (reflection, a plugin registry, a string-built name, a
  public API with callers outside the repo): then write `not-checked: <reason>` and the
  finding is reported as unconfirmed. A bare "appears unused" is not accepted.
- **A replacement does the same job.** `stdlib:` and `native:` findings name the
  replacement and state any behavior difference: what the hand-rolled code accepts or
  rejects that the replacement does not. The source pack's own benchmarks record this
  failure: reaching for a standard-library parser where the code was validating, which
  are different jobs. If equivalence was not established, the finding says
  `not-checked: equivalence`.
- `shrink:` findings show the shorter form in full, so the reader can check it.

## What is never a finding

- A test, a smoke check, an assertion, a validator or a gate. Verification is not bloat.
- Error handling at a real boundary: network, file, database, user input, another
  team's API. Handling for a case that cannot occur is a `delete:` finding; say why it
  cannot occur.
- A security control, a permission check, a rate limit, a secret scan.
- Code that was already there in `diff` scope. Review the lines the diff adds or
  changes. Pre-existing over-engineering is mentioned in one closing line, never listed.
- Style, naming, formatting.

## Steps

1. Settle scope and say it in one line, with the base ref or the root.
2. **`diff` scope:** read the full diff, then each touched file far enough to judge the
   added code in context. **`repo` scope:** do not assume the tree fits in context. Read
   the dependency manifest first (every dependency is a `native:` or `stdlib:`
   candidate: find what it is imported for), then go directory by directory, largest
   first. Look for: dependencies used for one call, single-implementation interfaces,
   factories with one product, wrappers that only delegate, files that export one
   thing, flags and config nothing reads, hand-rolled standard library. Keep a list of
   directories read and not read.
3. Write each finding in the contract format. Run the check for every claim about the
   rest of the codebase before writing the finding, not after.
4. Re-open every cited location and confirm the quote. Drop what does not match.
5. Rank by lines removed, largest first. In `repo` scope, report at most 25 and say how
   many more were found.
6. Write the report. Apply nothing.

## Verify

Every finding's quote was re-read at its cited line in step 4, and every `delete:` and
`yagni:` finding has either an executed check with its output or a `not-checked:`
marker. The report's `net` line counts confirmed findings only, and the unconfirmed
count is printed beside it.

Known weaknesses, at the same altitude as the rule: nothing mechanical enforces the
contract; it is checked by the session that wrote the findings, which is the weakest
kind of check. `git grep` misses dynamic dispatch, reflection and callers in other
repositories, which is why those cases are `not-checked` and never confirmed. No eval
cases exist yet; this is incubator.

## Done when

The report below is delivered, every finding in it meets the evidence contract, and the
coverage and not-reviewed lines are present.

## Stop when

- The diff is empty or the scope cannot be resolved: ask for the base ref or the root.
- `repo` scope and the tree is too large to finish in this session: stop, report what
  was covered and the findings so far, and name the directories not read. A partial
  audit presented as a whole one is the failure to avoid.
- A finding would require running the project's code to confirm and running it is not
  authorized: mark it `not-checked` and continue.

## Output contract

Version 1.

```text
overengineering-review v1  scope: <diff against <ref> | repo at <root>>
covered: <files or directories read>     not covered: <directories not read, or none>

confirmed:
  <one finding per line, contract format, ranked by lines removed>
unconfirmed:
  <findings carrying not-checked, same format>

net: -<N> lines, -<M> dependencies possible (confirmed only; <K> unconfirmed not counted)
not reviewed: correctness, security, performance.
seen in passing: <one line per bug or security issue noticed, or none>
```

When there is nothing to cut, the confirmed and unconfirmed blocks are replaced by the
single line `Nothing to cut.` and the coverage and not-reviewed lines stay.

The `not reviewed` line is mandatory. This review is silent on bugs and security holes
by design, and a reader who sees a clean over-engineering report must not read it as a
clean review. `seen in passing` is where a problem noticed along the way goes: it is
never suppressed because it is out of scope, and never investigated further here.
