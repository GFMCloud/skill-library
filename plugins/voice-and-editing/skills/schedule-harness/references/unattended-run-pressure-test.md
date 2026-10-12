# Unattended-run pressure test

Run this checklist against the harness design before its first unattended run, after the
attended "Run now" and before the task is left on its schedule. Reason: on 2026-10-10
three review rounds (verifiers, architecture, plan) passed a cloud-routine design, and a
fourth round, this unattended-run pressure test, found four blockers among these items.

## How to run it

For every routine or scheduled task in the design, answer each item with its evidence:
the file and line, the config value, or the registration field that shows it holds. An
item with no evidence fails. An item that cannot apply on this host (a desktop task has
no attached-repo list) is marked n/a with the reason. One failing item blocks the first
unattended run; fix the design or the render input, then run the checklist again.

## The nine items

1. **Network allowlist per source host.** Every host a routine fetches from is on that
   routine's network allowlist, checked against its fetch list, because a missing host
   fails only at run time, when nobody is watching.
2. **Allowed tools per routine.** Each routine's allowed-tools list names every tool its
   prompt calls, because an unattended run cannot answer a permission prompt and stalls.
3. **Attached repos per routine.** Each routine has attached every repo its prompt reads
   or writes, because a repo that is not attached is absent at run time and a write aimed
   at it lands nowhere.
4. **Dependency build order.** Each component is built before the first gate that needs
   it (a reviewer is not built after the gate that needs it), because a gate with no
   reviewer yet either stalls or passes by default.
5. **One home per prompt.** Each routine's prompt text lives in one file and every other
   place points at it, because two copies drift and the run executes the one nobody
   edited.
6. **A status written on every exit path.** Success, failure, skip, timeout and rate
   limit each write the run's status before exit, because a run that exits silently
   looks the same as a run that never started.
7. **Idempotent dated outputs.** Outputs are named by run date and a second run on the
   same date replaces rather than duplicates, because catch-up and retries run the same
   date twice.
8. **Clocks a few minutes past the hour.** Schedules sit a few minutes off the hour
   (06:07, not 06:00), because the top of the hour is when other scheduled jobs fire and
   rate limits cluster.
9. **No untrusted body in a session that can push.** A run that reads fetched or
   outside-written content (a web page, an email, an issue body) has no push or merge
   permission, because an instruction planted in that body could then reach the remote.

## Known weaknesses

The checklist is read against the design and its config, not against a run. It cannot
show that the platform enforces an allowlist or tool list as written; the first two
unattended runs' logs (SKILL.md, "Done when") are what prove that. It also covers only
these nine items: a defect outside them is not caught here.
