# Proving something you deployed is actually up

Part of the [verification-kit](../../README.md) pack.

"It's live" usually means the deploy command finished. This skill builds a small check that answers the question properly: is the right version serving, is the data fresh, are the connections it depends on open, do the important pages load, and are there errors on the page. Before it trusts that check, it breaks each part of it on purpose and confirms the check notices, because a check that has never failed proves nothing. Then it runs the check for real and keeps the output. You can wire the finished check in so that Claude Code cannot finish a turn while it is failing.

## Say this to use it

Any of these will do:

- "make a smoke test for this deploy"
- "prove the staging site is really up before we promote it"
- "build me a check that runs after every deploy"

Or, to be certain this skill and no other one runs:

```
/verification-kit:smoke-gate
```

It will ask for a short file listing what to check: the address of the thing being checked, and, for each of the five kinds of check, what a pass looks like and how to break it on purpose. If any kind of check has no way to break it listed, it refuses to build the script and names which one. For each connection it checks, it will ask you to set an address and a port as settings in your terminal before the check runs.

## What you'll get

A check script written into your project, a log of every run including the deliberately broken ones, and one screenshot from the real run.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Generated ./scripts/smoke.sh from smoke.yaml

Proving each check can fail:
  identity     broken on purpose -> exit 1  SMOKE FAIL: identity
  freshness    broken on purpose -> exit 1  SMOKE FAIL: freshness
  connections  broken on purpose -> exit 1  SMOKE FAIL: connections
  routes       broken on purpose -> exit 1  SMOKE FAIL: routes
  console      broken on purpose -> exit 1  SMOKE FAIL: console

Live run, nothing broken:
  exit 0  SMOKE PASS  build 2026-09-19T14:02Z, data 4 min old,
          db reachable, 6 of 6 routes 200, no error marker
  screenshot: run-log/2026-09-19-smoke.png

Turn-blocking check proved: red exits 2 and blocks, green exits 0 and releases.
Paste the settings entry from references/stop-hook.md to switch it on.
```

## Good to know

- **It writes a script into your project and makes it runnable.** It also writes a run log and one screenshot. The script is meant to be kept with your code, not hidden away.
- **The script goes online when it runs.** It fetches the address you gave it, and opens connections to the hosts and ports you named. It sends nothing else anywhere.
- **It needs Python with PyYAML to build the script,** and, to run it, `curl` and a shell that can open network connections directly, which is standard on Mac and Linux.
- **The addresses it connects to come from settings you type in your terminal,** named like `SMOKE_CONN_HOST_DB` and `SMOKE_CONN_PORT_DB`. Those are addresses and port numbers, not passwords. It asks for no account, key or password.
- **It never edits your Claude Code settings.** Turning on the turn-blocking behavior means pasting one entry into your settings file yourself. The skill hands you the text and stops there.
- **Once that entry is pasted, the check runs every time Claude Code tries to finish a turn,** and a failing check holds the turn open with the check's own output.
- **That blocking behavior lets go in two cases, on purpose.** If the check script is missing it prints a line and allows the turn. If the check fails twice in a row it allows the turn rather than looping forever. Either way you see the message.
- **The page-errors check is a text search, not a real browser reading the page.** It looks for a marker string in output you supply. It proves that part of the check can fail and pass on command. It does not prove a browser saw no errors. For that you need a browser or Playwright wired to the check yourself, which the script deliberately does not require.
- **A screenshot needs a browser or Playwright.** When neither is there, the log says so and why, rather than leaving the line out.
- **It refuses to call anything ready with an unproven check.** A kind of check with no way to break it listed is reported as unproven, never as passed, even if everything else is green.
- **There is an offline practice run you can do first.** It starts a small server on your own computer, builds a script against it, runs the whole proof, and deletes its temporary folder when it finishes. It never leaves your computer.

## What next

- Measuring a live website for speed and broken links instead? [site-review](../site-review/).
- Want the deploy diagnosed and retried when the check comes back red? [deploy-verify-fix](../../../deploy-ops/skills/deploy-verify-fix/), which uses a check like this one as its verify step.
- Want a budgeted retry loop around a failing check? [bounded-loop](../../../foundry-core/skills/bounded-loop/).
- Back to the [verification-kit pack](../../README.md), or to [skill-library](../../../../README.md).
