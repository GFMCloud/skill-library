# A full security audit of a codebase

Part of the [verification-kit](../../README.md) pack.

This skill works through a codebase looking for weaknesses that let someone do something they should not be able to do, tries to reproduce each one in a shut-off copy of the project, and writes up what it found with the source evidence, how serious it is, and the smallest change that fixes it. It works from the code itself and never touches a live or deployed system. It is long: a full audit reads the project in passes, uses several helper agents, and produces a folder of reports rather than an answer in the conversation.

**This one is not ours.** It comes from Cloudflare, is included exactly as they published it apart from a few lines of labelling, and is used under the MIT licence. Details are in [SOURCE.md](SOURCE.md); the licence text is in [LICENSE](LICENSE). Because it is unchanged, it reads differently from the other pages here, and its background files sit loose in its folder instead of in a `references` folder.

## Say this to use it

Any of these will do:

- "run a full security audit of this repo"
- "pen test this service from the source"
- "I want a findings report for this codebase"

Or, to be certain this skill and no other one runs:

```
/verification-kit:security-audit
```

There are two modes, and it will ask which you meant if your wording could go either way. For a security question or a look at one area, it answers in the conversation and writes nothing. For a full audit it first settles the project folder, where the reports go, which commit is being reviewed, how deep to go, and how many helper agents it is allowed to use.

## What you'll get

For a question, an answer in the conversation. For a full audit, a folder of files: a report, a detailed list of findings, a list of things it could not settle from the code alone, and the machine-readable records behind them.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Audit complete. Profile: standard. Output: ~/security-audit-skill/billing-api/run-1

REPORT.md                  2 confirmed, 3 need validation, 5 rejected
FINDINGS-DETAIL.md         per finding: source path, reproduction, fix
NEEDS-VALIDATION.md        what to check yourself, and how

Confirmed:
  high    Any signed-in tenant can read another tenant's invoices.
          src/invoices/query.ts:88, reproduced against dummy tenants in the sandbox.
  low     Internal build paths are returned in error responses.

Coverage: 14 of 14 planned areas. No prior run to compare against.
```

## Good to know

- **A full audit writes a folder into your home folder, not into your project.** The default is `~/security-audit-skill/<project-name>/run-<number>`, where `~` is your home folder and the number counts up from 1 for each run. Seven report and record files go there, plus a working folder per helper agent. This is the one place in this pack that writes outside a path you named, and it is deliberate: the reports stay out of the project so they are never committed by accident.
- **You can put the reports somewhere else, including inside the project,** but only by asking for it, and it will first check that the folder is one your version control ignores. If it cannot confirm that, it stops and asks for a path outside the project.
- **It never changes the code it is auditing.** The audit describes fixes. It does not make them.
- **Answering a question writes nothing at all.** Loading the skill does not start the audit. The folder is created only when you ask for a full audit or a report.
- **It may build and run the code under review, and only inside a sandbox.** A sandbox here means a restricted area your operating system enforces, in which the code has no internet, starts with an empty set of settings, cannot write anywhere except its own scratch folder, cannot change the project, and is cut off at set limits of processor time, memory, number of processes, file size, disk use and wall-clock time.
- **If your computer cannot provide every one of those controls, it does not run the code at all.** It records the missing control as a blocker and describes a safe way to check by hand instead.
- **It gives itself no internet access.** It does not download anything, does not install missing dependencies, and does not contact a deployed site, a live service, or shared infrastructure. Whatever the project needs must already be on your computer, or that check goes unrun.
- **It uses no real accounts, keys or passwords.** Reproductions use made-up users and made-up secrets, and the sandbox is started empty rather than having real settings stripped out afterwards.
- **A full audit starts several helper agents,** for mapping the code, hunting, challenging the hunt, and verifying findings. Each one costs model usage. It sets a limit on how many it may use before it starts, and if the limit cannot cover the minimum it launches none and tells you.
- **It needs Node.** Two small checkers that come with the skill, `validate-findings.cjs` and `validate-coverage-ledger.cjs`, run on Node and check the report records. Each one reads only the file named on the command line and returns a pass or fail.
- **It never claims to have covered everything.** Every run records what it looked at and what it did not, and a shortened or narrowed run presents itself as partial.

## What next

- Checking one change before it ships, rather than the whole project? [security-checklist](../security-checklist/) is the short version, and it is the one to reach for most of the time.
- Looking for failures that happen quietly rather than security holes? That is the `silent-failure-hunter` agent, described on the [pack page](../../README.md).
- Back to the [verification-kit pack](../../README.md), or to [skill-library](../../../../README.md).
