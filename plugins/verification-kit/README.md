# verification-kit

Part of [skill-library](../../README.md). If the words skill, pack, agent or hook are new to you, that page explains them first.

## What problem this solves

Claude Code tends to say "done" when the work looks done. The tests were written but not run. The site was deployed but nobody loaded it. The research quotes a version number that was right two years ago. Each of these passes a quick look and fails later, when it costs more.

This pack gives Claude Code ways to check before it reports: run the real test, load the real page, look up the claim today, and get a second reviewer who did not write the work.

## When would I use this?

- Claude Code says a task is finished and you want proof, not a summary.
- You are about to act on research and want to know which claims are still true.
- A change is about to ship and touches sign-in, user input, secrets or cloud settings.
- You deployed something and want a quick automatic check that it is really up.
- Your website feels slow or has broken links and you want numbers.
- A project has grown and you suspect half of it is not needed.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/verification-kit/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [fact-currency-check](skills/fact-currency-check/README.md) | Checks whether a claim, version number, citation or referenced issue is still true today, not just true when it was written. | "is this still true?" or "check these claims before we act on them" | Each claim marked current, stale, or not checkable, with the source it was checked against. | Looks things up online, and may run the software a claim is about. Changes nothing. |
| [overengineering-review](skills/overengineering-review/README.md) | Reads a change or a whole project and lists code that could be removed: options nobody sets, layers with one user, hand-made copies of built-in functions. | "is this over-engineered?" or "what can we delete?" | One line per finding with the code quoted and the search that backs it. It removes nothing. | Reads your code and runs searches that only look, such as `git grep`. Changes nothing. |
| [review-pair](skills/review-pair/README.md) | Has a second, separate reviewer judge one proposed change against its stated goal before the change is made. | "gate this change with review-pair" | A written verdict of pass or fail with reasons. On a pass, the change is applied. | Starts a second Claude helper, runs a small checking script on its answer, and on a pass applies the reviewed change to your files. |
| [security-audit](skills/security-audit/README.md) | A full security audit of a codebase from its source: finds weaknesses, tries to reproduce them safely, and writes a findings report. It is a large third-party skill from Cloudflare, included unchanged. | "run a full security audit of this repo" | For a question, advice in the conversation. For a full audit, a folder of reports including a list of findings. | For a full audit it creates a reports folder in your home directory, starts several helper agents up to a limit it sets at the start, and may build and run the code being audited inside a sandbox, a restricted area with no internet. Needs Node. |
| [security-checklist](skills/security-checklist/README.md) | A pass or fail security checklist for one change or one file before it ships: secrets, input handling, sign-in, data exposure, dependencies, cloud settings. | "is this safe to deploy?" | A checklist with pass, fail or not checkable per item, and proposed fixes it does not carry out. | Reads the code you point at and may run a dependency check (`npm audit`, `pip-audit`), which contacts the package registry. Changes nothing. |
| [site-review](skills/site-review/README.md) | Scores a live website for speed, accessibility and broken links, then fixes problems on a separate branch, so your main files stay as they were until you accept the fixes. | "review my site at https://example.com" | A score table, the list of broken links, screenshots, and proposed fixes. | Downloads two website-checking tools (Lighthouse and linkinator) on first use, runs a hidden Chrome window against the live site, follows its links, writes report files, and edits your site's files on a separate branch. Needs Node. |
| [smoke-gate](skills/smoke-gate/README.md) | Builds a quick "is it actually up?" check for something you deployed, and proves the check can fail before trusting it. | "make a smoke test for this deploy" | A small script in your project that checks your site or service, a log of each run, and one screenshot. | Writes a script into your project, makes network requests to the address you name, and can be set up to stop Claude Code from finishing a turn while the check fails. Needs Python, PyYAML and `curl`. |

This pack also ships agents. An **agent** is a helper that Claude Code hands a whole job to; it works on its own and reports back.

| Agent | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [pre-delivery-verifier](agents/pre-delivery-verifier.md) | Checks a finished piece of work against its acceptance list by running the real checks, before you are told it is done. | "verify this before you hand it over" | A report of each check run, its actual output, and whether the work passed. | Runs your own build, tests or checkers. It is set up so it cannot change files. |
| [silent-failure-hunter](agents/silent-failure-hunter.md) | Reads code for failures that would happen quietly: errors that are caught and ignored, fallbacks that hide a real problem. | "hunt for silent failures in this module" | A list of findings with file and line. It fixes nothing. | Reads your code. Runs nothing and changes nothing. |
<!-- /generated:whats-inside -->

**This pack also installs one hook.** A **hook** is a small program that Claude Code runs by itself at a set moment, without being asked. This one is called `readonly-agent-guard`. Once the pack is installed, it runs before every shell command Claude Code is about to run, in every session. Almost always it does nothing and lets the command through. It only acts when the command comes from one of six named agents that are meant to look and not touch. For those, it refuses commands that would write, move or delete files outside Claude Code's temporary work folder. The six are `pre-delivery-verifier` and `silent-failure-hunter` from this pack, `cross-document-checker`, `transcript-scanner` and `loop-operator` from other packs here, and Claude Code's built-in `Explore`. The hook reads nothing but the command, writes nothing, and never goes online. It needs Python, a free programming tool that most computers set up for programming already have.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | The code, documents or report files you point a skill at. `security-audit` reads the whole project you name. The hook reads only the command it is checking. |
| Files written | `smoke-gate` writes a check script and a log into your project. `site-review` writes report files and screenshots to a folder you choose, then edits your site's files on a separate branch. A branch is a separate copy of the work kept by git, the tool programmers use to track changes, so your main files stay as they were until you choose to merge the branch in. `review-pair` applies the change it reviewed, only after a pass. `security-audit`, in full audit mode, creates `~/security-audit-skill/<project>/run-<number>` in your home folder and writes its reports there. The other skills, both agents and the hook write nothing. |
| Files deleted or moved | None by this pack. A change applied by `review-pair` does whatever that change does. |
| Programs and scripts | Small programs ship with the pack: the hook and its self-test, one checker for `review-pair`, one score-table script for `site-review`, three scripts plus a practice server and its test for `smoke-gate`, and two report checkers with their tests for `security-audit`. Only those two report checkers need Node. Skills also run tools already on your computer: your project's own tests and build, `git`, `curl`, `npm audit`, and `npx` for `site-review`. `security-audit` may build and run the code it is auditing. It does that only inside a sandbox, a restricted area set up by your operating system where the code has no internet, cannot change your project, and is cut off at set limits of time and memory. If your computer cannot provide one, it does not run the code at all. |
| Internet access | `fact-currency-check` looks claims up online. `site-review` downloads Lighthouse and linkinator, two website-checking tools, on first use. They come from npm, the public download site for Node tools. It then loads the live site you name and follows its links. `smoke-gate` connects to the address you name. `security-checklist` contacts the package registry if it runs a dependency check. `security-audit` forbids itself any internet access. Nothing sends your files anywhere. |
| Accounts, keys or passwords | None. No skill asks for a key or signs in to anything. If `security-checklist` finds what looks like a real password in your code, it tells you where, never prints it, and leaves replacing it to you. |

Two limits. First, the hook does not catch everything. The two agents are set up without Claude Code's file-editing tools, and the hook blocks the usual ways a command writes a file. Its own notes list ways it misses, such as a write hidden inside another script. Second, `smoke-gate`'s check of browser error messages is a simple text search, not a real browser reading, which the skill says itself.

## How the skills work together

They do not depend on each other. Each covers a different moment:

1. **Before acting on information:** `fact-currency-check`.
2. **Before making a change:** `review-pair` gets a second opinion on it.
3. **Before calling work done:** the `pre-delivery-verifier` agent runs the real checks. The `silent-failure-hunter` agent looks for errors that would be hidden.
4. **Before shipping:** `security-checklist` for one change. `security-audit` when you want the whole codebase examined, which takes much longer.
5. **After shipping:** `smoke-gate` checks it is up. `site-review` measures a live website.
6. **Any time:** `overengineering-review` lists what could be removed.

The two security skills are easy to confuse. `security-checklist` is a short list for one change. `security-audit` is a long examination of everything.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install verification-kit@skill-library
```

The first line is only needed once, however many packs you install.

This pack needs the `foundry-core` pack, so Claude Code installs that one at the same time. The install message says `+ 1 dependency: foundry-core`.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
