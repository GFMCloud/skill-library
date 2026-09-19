# Watching something that changes on its own

Part of the [long-projects](../../README.md) pack.

Some things change without you doing anything: an alarm goes off, a pull request becomes ready, a number crosses a line, another program drops a file somewhere. Checking them by hand is easy to forget, and a check that reports every time it runs turns into noise you stop reading. This skill sets up a check that runs on a schedule and reports only when the thing being watched moves from one state to another. Nothing changed means nothing to read. It also asks you up front which follow-up actions it may take by itself and which it must queue for your approval, and it refuses to treat an action you did not list as allowed.

## Say this to use it

Any of these will do:

- "watch this alarm and only tell me when it changes"
- "tell me when this pull request is ready"
- "poll for this file and only bug me on a change"

Or, to be certain this skill and no other one runs:

```
/long-projects:change-watch
```

It will ask what is being watched and the command that reads its current state, where its small state file should live, where reports should go, which follow-up actions are safe to run and which need your approval, and which of its three ways of running to use. That last one is a real decision, not a default, and it makes the choice with you as its first step.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Cycle at 09:00
NO-REPORT  cloudwatch:orders-api-5xx  (still OK, last change 3 days ago)

Cycle at 09:15
REPORT  cloudwatch:orders-api-5xx  OK -> ALARM

  What changed: error rate crossed the threshold at 09:12.
  Checked: last deploy was 08:58, three commits.
  Ran (safe, on your list): staging check against the new build. Passed.
  Queued for you (approval-only, not run): roll back the 08:58 deploy.

Cycle at 09:30
NO-REPORT  cloudwatch:orders-api-5xx  (still ALARM, already reported at 09:15)
```

## Good to know

- **It registers something that keeps running after you walk away.** That is the point of the skill: a repeating scheduled task on your computer, or a job in Anthropic's cloud. You register it yourself as part of setting the watch up.
- **It rewrites its state file on every single check.** There is one file per watched thing, holding what state was last seen and what was last reported. The file is rewritten whether anything changed or not.
- **It reports once per change, not once per episode.** A thing that flips back and forth produces one report per flip. There is no smoothing, so a genuinely unstable source will report a lot. The skill states this plainly as a known cost.
- **An action it has not been told about is refused, not guessed.** Follow-up actions are looked up in a rules file you write. An action missing from that file stops the cycle with an error rather than being treated as safe.
- **It ships two small Python programs and needs Python to run them.** One updates the state file and decides whether to report, the other classifies a follow-up action.
- **It goes online only if the thing being watched is online.** Two of its three ways of running use Anthropic's cloud or accept an incoming request from a monitoring service. The local way makes no network calls of its own, beyond whatever your reading command does.
- **It handles no keys or passwords.** The cloud option relies on a token that belongs to that cloud job and is held outside this skill.
- **Its state file reader is not a full parser.** It understands five fields written as `name: value` and silently ignores anything else in the file, which the skill says itself.
- **Parts of it depend on skills in other packs.** The scheduled option uses `schedule-harness` from the `voice-and-editing` pack, which the skill's own text notes did not exist when it was written. The optional staging check uses `smoke-gate` from `verification-kit`. One of its three ways of running needs a Claude Code feature that is still in research preview.

## What next

- Want the staging check that a safe follow-up action can run? That is [smoke-gate](../../../verification-kit/skills/smoke-gate/).
- Watching a long job that is already running, rather than a source? The `loop-operator` agent in this pack does that instead.
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
