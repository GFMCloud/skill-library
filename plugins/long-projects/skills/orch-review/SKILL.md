---
name: orch-review
description: >-
  Review a diff (local uncommitted changes, or a GitHub PR by number or URL) with several
  independent reviewers in parallel, deduplicate their findings, adversarially verify the
  serious ones, and report blocking versus advisory findings under a fail-closed
  contract: it never presents a clean approval when any part of the review did not run.
  Use when the user says "orch-review", "review this PR with multiple reviewers",
  "fan-out review", or at the review phase of orch-pipeline. Not a replacement for
  review-pair (which gates one change spec against its goal) or for the built-in
  /code-review. Costs three to five subagent spawns per run; read-only, it fixes nothing.
metadata:
  maturity: incubator
  reviewed: 2026-10-11
---

# Orchestrated diff review

A single reviewer's clean result looks the same whether it reviewed everything or
quietly skipped half. This skill splits the review by dimension, checks the serious
findings a second time, and refuses to say "approved" unless every dimension ran.

Adapted from the ECC project's `/orch-review` command (MIT, v2.2.1), reviewed
2026-09-17. Record: `maintainers/reviews/2026-09-17-ecc/`. The source handed the fan-out to a
JavaScript workflow file in the ECC repository. That file was not adopted (no ECC code
runs here), so the fan-out, dedup and verify steps are specified below and run through
the Agent tool. What was kept is the input handling, the result shape and the
fail-closed contract.

## Inputs

One argument, optional:

| Argument | Mode |
|---|---|
| blank | local: uncommitted changes against `HEAD` |
| an integer, or a `https://github.com/<owner>/<repo>/pull/<N>` URL | PR |

**Never pass the raw argument to a shell.** Extract the integer; if the argument is
anything other than a bare integer or a pull-request URL ending in one (extra text,
shell metacharacters, another kind of URL), stop with an error. Only the extracted
integer appears in a command.

## Steps

1. **Gather.** Local: `git diff --name-only HEAD` and `git diff HEAD`. PR:
   `gh pr diff <N>` and `gh pr view <N> --json files --jq '.files[].path'`. Empty diff:
   stop with "Nothing to review." Drop binary and generated files from the file list.
   Note the dominant language from the file extensions; leave it unset when mixed.
2. **Premises.** Fill the Premises table from
   [templates/reviewer-brief.md](templates/reviewer-brief.md), per "Premises in the
   brief" below, and read the running system's own log for every inferred premise about
   a running system.
3. **Fan out**, one read-only subagent per dimension, each given the diff, the file
   list and the Premises table, and nothing else from this conversation. State the model
   before spawning.
   - correctness and maintainability against the surrounding code;
   - silent failures: `verification-kit:silent-failure-hunter`;
   - security, only when the file list touches a security trigger (authentication or
     authorization, user input, database queries, file-system paths, external API calls,
     cryptography, secrets), using `verification-kit:security-checklist` as the reference.
   Every finding must carry file, line, severity and the quoted code.
4. **Deduplicate** on the quoted code, normalized for whitespace. Keep the highest
   severity of each duplicate group.
5. **Verify.** For every unique critical or high finding, a fresh subagent tries to
   refute it from the code. Confirmed and could-not-verify findings stay blocking;
   refuted ones move to advisory, marked as refuted.
6. **Report**, in the shape below.

## Premises in the brief

The brief handed to each reviewer carries a Premises table
([templates/reviewer-brief.md](templates/reviewer-brief.md)): each fact the change relies
on, marked observed (the command and the output reference that showed it) or inferred
(from what). The orchestrator reads the running system's own log for every inferred
premise about a running system before the brief is sent; a brief with an unchecked
inferred premise about a running system is not sent. Reason: on 2026-10-11 a reviewer
accepted "R1's cwd is its first repo" as fact; it was inferred from a different routine's
proof and never checked against R1's run log, and R1's next scheduled run wrote nothing.

## Fail-closed contract

If any dimension errored, timed out, hit a rate limit, or could not be spawned, the
result is `incomplete`, the failed dimensions are named, and the verdict is not
`APPROVE`. Do not fall back to a hand-rolled review and do not imply the diff was
approved. A concurrency limit means wait; a rate limit means stop.

Known weakness: reviewers read, they do not execute. A finding that needs a test run to
confirm stays in blocking as could-not-verify, which is noisy by design.

## Verify

The stats line accounts for every raw finding: raw = unique + duplicates, and unique =
confirmed + unverified + refuted + medium-and-low. Pass means the arithmetic holds and
every blocking finding quotes code that exists at the cited line.

Before the brief is sent, every Premises row fills exactly one evidence column, and no
row about a running system is still Inferred. This is a reading check, not a script.

## Done when

The report is presented with a verdict, the stats line, every blocking finding with its
evidence, and the list of dimensions that ran.

## Stop when

- The argument fails validation.
- The diff is empty, or the PR is not found, or PR mode is asked for and `gh` is absent
  (suggest local mode on a checked-out branch).
- A Premises row about a running system is still Inferred and that system's own log
  cannot be read from this session: the brief is not sent. Say which log is needed.
- A rate limit arrives mid fan-out: report `incomplete` with what did run.

## Output contract

Version 1. Consumed by `orch-pipeline` at its review phase.

```
verdict:    APPROVE | CHANGES_REQUESTED | INCOMPLETE
dimensions: <ran> of <planned>   failed: <name: error, ...>
stats:      raw <n>  unique <n>  confirmed <n>  unverified <n>  refuted <n>
blocking:   <file>:<line> <severity> <issue>  evidence: <quoted code>  [confirmed | could not verify]
advisory:   <file>:<line> <severity> <issue>  [medium/low | refuted]
not checked: <what no dimension covered>
```

This is a report to a human. The skill commits nothing and approves nothing on its own.
