# Agreeing what done means

Part of the [foundry-core](../../README.md) pack.

Requests like "improve this", "clean it up" or "make the page better" have no end. Claude Code will do something, and whether that something was right is a matter of opinion afterwards. This skill turns the ask into a written target before any work starts: what counts as done, a command that can actually be run to test it, how things stand right now measured by running that command once, how many attempts are allowed, and who decides. If the ask cannot be made testable and cannot be scored against written criteria either, it refuses to write a target, asks you one question, and stops rather than invent a check to look busy.

## Say this to use it

Any of these will do:

- "turn this into a proper goal before you start"
- "what would done look like here?"
- "write a goal block for this, then run it"

Or, to be certain this skill and no other one runs:

```
/foundry-core:goal-spec
```

It will ask for the ask in your own words and for the thing it targets, a file, a folder, a web address or a running service, and it needs that to be real enough to run a check against. It works out the attempt limit and who signs off by itself and tells you what it chose, so you can correct it.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
kind:           measurable
goal_condition: every page under docs/ loads with no broken link, stop after 3 attempts
check:          npx linkinator ./docs --recurse
baseline:       ran at 09:14 today: 214 links checked, 7 broken
budget:         3 attempts
human_gate:     Graham confirms before anything under docs/api is edited

Refusing on the second half of your ask. "Make the writing nicer" has no
check I can run and no criteria to score it against. One question: is
there a style guide I should score each page against, or a person who
decides? Either one unblocks it.
```

## Good to know

- **It writes a goal file where you agree, and nothing else.** For a goal judged against criteria rather than measured, it also writes a rubric file at a path you agree on. It deletes and moves nothing.
- **It runs your check command once, before work starts.** That is how the starting measurement is real rather than recalled. If your check goes online, that one run goes online. The skill itself contacts nothing.
- **It reads `~/.claude/plugins/installed_plugins.json`** to find out where it was installed (`~` means your home folder).
- **Its validator is weaker than it sounds.** The script looks for the field names at the start of a line, so it will accept a goal file that is not correctly formatted as long as those names are present.
- **Its instructions for running that validator name the author's own folder.** The command shown begins by moving into `/Users/gfm/skill-library/...`, which will not exist for you. The paragraph straight after tells you to use your own installed copy's folder instead, which you find in the file named above.
- **It cannot tell whether your check is the right check.** Its own notes say this. It can tell that a check exists and was run, not that passing it means the work is good.
- **It refuses rather than guesses.** No runnable check and no criteria means one question and a stop, with one exception: if only the attempt limit is missing, it proposes three and asks you to confirm.
- **It needs `bash`,** a free tool that computers used for programming usually have.

## What next

- To have that check run by itself after every turn, with a limit: [Stopping a fix loop](../bounded-loop/).
- The standard the finished work is held to: [Proving work is done](../proof-of-work/), written up with [Writing up the evidence](../evidence-report/).
- If the work is risky rather than vague, agree the plan before it starts instead: [plan-gate](../../../turn-reduction/skills/plan-gate/).
- Back to the [foundry-core pack](../../README.md), or to [skill-library](../../../../README.md).
