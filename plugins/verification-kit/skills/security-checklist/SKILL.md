---
name: security-checklist
description: >-
  A PASS/FAIL security checklist for one change or one file before it ships. Load this
  FIRST, before reading the file, when the user asks "is this safe to deploy", "safe to
  ship", "safe to merge", "security pass" or "security checklist", or when a change
  about to deploy touches authentication, user input, database queries, file paths,
  external APIs, secrets or infrastructure; also the security dimension of orch-review.
  Do not skip it for a small file, a deploy-safety question gets the checklist. Covers secrets,
  input validation, injection, authn and authz, XSS, CSRF, rate
  limiting, data exposure, dependencies, and cloud items (IAM, network, logging, CI/CD,
  CDN, backups). It reviews and reports only, every remediation is a proposed action
  behind a stop-and-confirm gate, and it never touches a credential. Not a full codebase
  audit or pen test (that is security-audit), not a general bug review, not the built-in
  /security-review command. Loading both reference files is a long read (about 300
  lines).
metadata:
  maturity: incubator
---

# Security checklist

Nothing else in this plugin carries concrete security examples for a reviewer to check
code against. This skill is that reference, with one hard rule on top of it.

Adapted from the ECC project's `security-review` skill (MIT, v2.2.1), reviewed
2026-09-17. Record: `docs/reviews/2026-09-17-ecc/`. Changes from the source: renamed,
because Claude Code ships a built-in `/security-review`; the source's imperative rows
("rotate secrets", "enable MFA", `npm audit fix`) were rewritten as findings plus gated
proposals, which both judges of the review made a condition of adopting it; its
blockchain section was out of scope and dropped.

## The stop gate (read this first)

This skill **finds and reports**. It does not remediate.

- When a check fails, the output is a finding with evidence, and a proposed action.
- A proposed action that changes anything (a dependency upgrade, a config change, a
  policy edit, a header, a firewall rule) is listed under **Proposed actions** and is
  not run until the user confirms that specific action.
- An action that touches a credential or an account setting (rotating or revoking a
  secret, enabling MFA, changing IAM, editing a secrets manager) is **never performed by
  the agent**. It is handed to the user as a step for them to do, with the reason.
  Rotation is still the right remediation for an exposed secret: deleting the commit is
  not. The point is who does it and that they chose to.
- A suspected live secret is a hard stop: report where it is, do not print its value,
  do not continue the review until the user says how to proceed.

## Inputs

- The diff or the paths under review, and what the change is for.
- Which areas apply. Default: decide from the security trigger list in the description
  and say which areas were skipped and why.

## How to review

1. Pick the areas that apply. Load
   [references/application-security.md](references/application-security.md) for code and
   [references/cloud-security.md](references/cloud-security.md) for infrastructure. Load
   only what applies.
2. For each area, search the code for the FAIL patterns before concluding PASS. "Did not
   find it" names what was searched.
3. Every finding carries file, line and the quoted code, a severity, and which checklist
   row it fails.
4. Rows that cannot be decided by reading (whether MFA is on, whether backups restore,
   whether rotation is configured) are reported as **not verifiable from the code**, with
   the read-only command or console page where the user can check. They are never marked
   PASS by assumption.

## Areas, in one line each

| Area | The question |
|---|---|
| Secrets | Is any secret in code, config, logs or history, and does startup fail loudly when one is missing? |
| Input validation | Is every external input validated against a schema, by allow-list, before use? |
| Injection | Is every query parameterized, with no string-built SQL or shell? |
| Authn and authz | Is the token kept out of script-readable storage, and is authorization checked before every sensitive operation? |
| XSS | Is user HTML sanitized and is there a strict CSP without `unsafe-inline` or `unsafe-eval`? |
| CSRF | Do state-changing requests need a token, and are cookies `SameSite`? |
| Rate limiting | Are endpoints limited, with tighter limits on expensive ones? |
| Data exposure | Are logs and error responses free of secrets, personal data and stack traces? |
| Dependencies | Is there a committed lock file, a clean audit, and an update path? |
| Cloud | Least-privilege IAM, no public data stores, restricted ingress, logging, OIDC in CI, tested backups |

## Verify

Every FAIL quotes code that exists at the cited line, every PASS names what was searched,
and the proposed-actions list contains no action that was already run. Pass means a
second reader can reproduce each finding from the report alone.

## Done when

The report below is delivered with all applicable areas marked PASS, FAIL, or not
verifiable, and nothing has been changed.

## Stop when

- A suspected live secret is found (see the stop gate).
- The user has not confirmed a proposed action: the review ends at the proposal.
- An area needs access the agent does not have (a cloud console, a production
  environment): mark it not verifiable and name what would show it.

## Output contract

Version 1. Consumed by `long-projects:orch-review` as its security dimension.

```
Security checklist: <scope>
<area>: PASS | FAIL | NOT VERIFIABLE   searched: <patterns, paths>
  <file>:<line> <severity> fails "<checklist row>"  code: <quoted>
Proposed actions (none has been run; each needs its own confirmation):
  1. <action>  why: <finding>  who: agent after confirm | user only (credential or account)
Not checked: <areas skipped and why>
```

Known weakness: this is a checklist read against source. It finds known patterns; it
does not find logic flaws, and a clean result is not a statement that the system is
secure.
