# A security pass on one change before it ships

Part of the [verification-kit](../../README.md) pack.

Most security problems arrive in ordinary changes: a password left in a settings file, a database query built by gluing text together, a page that prints whatever a user typed, an error message that hands back the whole stack of internal detail. This skill takes one change, or one file, and works through a fixed list of those known problems, marking each area pass, fail, or not decidable from the code. Every failure comes with the file, the line, the code quoted, and how serious it is. It fixes nothing. Every suggested fix is listed as a proposal that waits for you to say yes.

## Say this to use it

Any of these will do:

- "is this safe to deploy?"
- "do a security pass on this file before I merge it"
- "run the security checklist on these changes"

Or, to be certain this skill and no other one runs:

```
/verification-kit:security-checklist
```

It will ask what the change is for and which files to look at. It then decides which areas apply, and tells you which ones it skipped and why, rather than quietly leaving them out.

## What you'll get

A line per area with pass, fail, or not decidable from the code, and what was searched for. Then the failures with their evidence, then a list of proposed fixes, none of which has been carried out.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Security checklist: PR 214, adds the export endpoint

Secrets:          PASS            searched: api_key, secret, token, .env in the diff
Input validation: FAIL            searched: schema parse before use
  src/export.ts:31 high fails "every external input validated before use"
    code: const rows = await db.query(`select * from ${req.query.table}`)
Injection:        FAIL            same line, query built by joining text
Authn and authz:  PASS            searched: requireUser before handler
Rate limiting:    NOT VERIFIABLE  limits are set at the CDN, not in this repo
Dependencies:     PASS            npm audit -> 0 vulnerabilities

Proposed actions (none has been run; each needs its own confirmation):
  1. Replace the built query with a parameterized one and an allow-list of tables.
     who: agent after confirm
Not checked: cloud settings, no infrastructure files in this change.
```

## Good to know

- **It changes nothing.** The report is the whole output. Proposed fixes sit in a list until you confirm one by one.
- **Anything touching a credential or an account setting is handed to you, never done for you.** Rotating a secret, turning on extra sign-in steps, changing permissions: it tells you what to do and why, and you do it.
- **If it finds what looks like a live secret it stops there.** It tells you where the secret is, never prints its value, and does not carry on until you say how to proceed.
- **It may run a dependency check,** such as `npm audit`, `npm outdated` or `pip-audit`. Those contact their package advisory services, so that step goes online. Commands that would change your project, such as `npm audit fix`, are named as off limits.
- **You need `npm` or `pip-audit` for the dependency rows.** Without them those rows are reported as not checked rather than passed.
- **Things it cannot see from the code are never marked pass.** Whether extra sign-in is switched on, whether backups actually restore, whether keys get rotated: these are marked not decidable from the code, with the place you can go and look.
- **A pass is not a statement that the system is secure.** It is a checklist read against source. It finds known patterns and does not find flaws in the logic. The skill says this itself in its own closing line.
- **The rule that keeps it from fixing things is written instructions, not a switch.** It binds the conversation that follows it. It is not a lock on the tools.

## What next

- Want the whole codebase examined rather than one change? [security-audit](../security-audit/) is the long version, and it takes much longer.
- Want the change reviewed for correctness too? [orch-review](../../../long-projects/skills/orch-review/) runs several independent reviewers over a change.
- Already deployed and want to know it is up? [smoke-gate](../smoke-gate/).
- Back to the [verification-kit pack](../../README.md), or to [skill-library](../../../../README.md).
