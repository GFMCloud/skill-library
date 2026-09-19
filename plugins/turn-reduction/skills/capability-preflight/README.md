# Checking access before the work starts

Part of the [turn-reduction](../../README.md) pack.

Work stalls when Claude Code turns out not to be able to reach something it needed: a folder, a server, a repository, an account. You usually find out in the middle, and then you finish that step by hand. This skill moves the discovery to the front. You write down every system the job touches, and for each one a command that reads from it and a command that writes to it. It runs them all in one pass and tells you which ones are proven and which are not. Anything that fails comes back in one list, with the fix you wrote next to it, so you deal with all of it once instead of one surprise at a time.

Each system also gets a test that is meant to fail, such as the same request with the sign-in removed. If that one succeeds, the check proved nothing, and the skill says so rather than reporting a pass.

## Say this to use it

Any of these will do:

- "check we can actually reach everything before we start"
- "preflight the systems this job needs"
- "before you begin, prove you can read and write each of these"

Or, to be certain this skill and no other one runs:

```
/turn-reduction:capability-preflight
```

It will ask which systems the work touches, and for each one what counts as proof and what you would do if it failed. It writes those answers into a manifest file, which is the list it then runs.

## What you'll get

A line per system with a verdict, then everything that failed gathered at the end.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
PREFLIGHT: publish the September report

project repo working tree      PROVEN
  population: every file tracked by git under $PROJECT_ROOT
  excludes:   untracked files, submodules, the .git folder
  read  ok  204 files
  write ok  wrote and removed .probe
  control   failed as required

reports API                    NOT PROVEN
  read  ok  200, 12 records
  write no  403 Forbidden
  control   SUCCEEDED, which should not happen

BLOCKERS (1)
  reports API: the token in use is read-only.
    remedy: issue a write-scoped token and put it in the usual place.

This run covers only the systems named in the manifest. One is not proven.
```

## Good to know

- **It runs whatever you put in the manifest.** The commands go through `bash` with your own account, so they can read, write and delete anything you can. The file is only as safe as what you wrote in it. That is the design, not an accident.
- **Every system must have a write test, so something is always written somewhere.** The example in the skill creates a small `.probe` file in your project folder and removes it again. A delete you write into a manifest will run.
- **It writes a record file only if you ask for it.** Pass `--json` with a path and it saves the full result there. Otherwise it prints and saves nothing.
- **It can go online, because you told it to.** The program makes no network call itself, but the skill tells you to write tests for the APIs your work depends on, and those calls reach the internet.
- **It never reads a store of passwords.** A test that signs in uses the sign-in already on your computer, and the program tries to blank out anything token-shaped or password-shaped before printing what a test returned.
- **It refuses some manifests before running anything.** Commands containing `||`, `; true`, `&& true`, `set +e` or `; exit 0` are rejected, because a test that cannot report failure is not a test. This checks the shape of your commands. It does not limit what they are allowed to do.
- **It proves only what you listed, at the moment it ran.** It cannot find the system you forgot, and a sign-in that expires an hour later will not be caught by a check that passed this morning.
- **What it needs first.** Python 3.9 or newer and `bash`, plus whichever command-line tools your own tests call. Nothing keeps running afterwards: each test is stopped after 30 seconds unless you say otherwise.

## What next

- Once access is proven, [standing-authorization](../standing-authorization/) records what Claude Code may then do without asking you each time.
- The tests here are built to satisfy the standard in [proof-of-work](../../../foundry-core/skills/proof-of-work/), in the `foundry-core` pack.
- For work that runs over many sessions, [phased-harness](../../../long-projects/skills/phased-harness/) sets up the project this check would run at the top of.
- Back to the [turn-reduction pack](../../README.md), or to [skill-library](../../../../README.md).
