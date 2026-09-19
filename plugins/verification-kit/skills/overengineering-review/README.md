# Finding code that does not need to exist

Part of the [verification-kit](../../README.md) pack.

Projects collect code nobody needs: a setting nothing reads, a layer with one user, a hand-written copy of something the language already provides, an outside tool pulled in for a single line. Each one looked reasonable when it was added, and together they make the project harder to change. This skill reads a change or a whole project and gives you a list of things that could be removed, with the code quoted and, for anything it claims is unused, the search it ran to show that. It removes nothing itself. You decide what goes.

## Say this to use it

Any of these will do:

- "is this over-engineered?"
- "what can we delete here?"
- "audit this repo for unnecessary complexity"

Or, to be certain this skill and no other one runs:

```
/verification-kit:overengineering-review
```

It will ask whether you mean one change or the whole project, and which starting point to compare a change against. For a whole project it will ask which folders to leave out, and it skips code copied in from elsewhere and generated files without asking.

## What you'll get

A list of cuts, biggest first, each on one line with the file, the quoted code, and the check behind it. Anything it could not confirm is listed separately, and it ends by saying which folders it read and which it did not.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
overengineering-review v1  scope: repo at ./billing

covered: src/, cli/, config/     not covered: none

confirmed:
  src/retry.py:L12-48 yagni: RetryPolicy class. Inline the one call into client.py.
    check: git grep -n "RetryPolicy(" -> 1 match, src/client.py:40
  src/util.py:L60-74 stdlib: hand-written chunking loop. Use itertools.batched.
    check: python -c "import itertools; itertools.batched" -> no error
unconfirmed:
  cli/export.py:L5 delete: --legacy-format flag, nothing sets it.
    not-checked: the flag name is built from a string at runtime

net: -47 lines, -1 dependency possible (confirmed only; 1 unconfirmed not counted)
not reviewed: correctness, security, performance.
seen in passing: none
```

## Good to know

- **It deletes nothing.** The output is a list. Every removal is yours to make.
- **It reads your code and runs searches that only look.** Searches such as `git grep` and printing a range of lines from a file. Nothing is written, moved or deleted.
- **It needs `git`.** The searches and the compare-against-a-starting-point mode both use it.
- **It never goes online, and never touches an account, key or password.**
- **A claim that something is unused comes with the search that would have disproved it.** When the search cannot see the answer, because the name is built at runtime or the code is used by another project, the finding is marked unconfirmed rather than dropped or asserted.
- **Tests, checks and security controls are never listed as things to cut.** Nor is error handling where a real failure can happen, such as network or file access.
- **It is silent on bugs and security holes, and says so in the report.** A clean result here is not a clean review. Anything it happens to notice goes in a "seen in passing" line without being investigated.
- **Nothing mechanical enforces its own evidence rule.** The report is checked by the same session that wrote it, which is the weakest kind of check.

## What next

- Want the bugs, not the bloat? [orch-review](../../../long-projects/skills/orch-review/) reviews a change with several independent reviewers.
- Shipping the change afterwards? [security-checklist](../security-checklist/) is the security pass for one change.
- Back to the [verification-kit pack](../../README.md), or to [skill-library](../../../../README.md).
