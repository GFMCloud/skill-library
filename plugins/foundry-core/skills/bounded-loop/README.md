# Stopping a fix loop

Part of the [foundry-core](../../README.md) pack.

When you ask Claude Code to keep working until a test passes, two things tend to go wrong. It judges the test from what it wrote in the conversation rather than from running it, and it retries without any limit. This skill sets up a check that Claude Code cannot talk its way past: your own command is run automatically at the end of every turn, and a turn whose check failed is blocked with that command's real output attached. It counts attempts, and when the count runs out it writes a report saying what was tried and what the failure was, instead of carrying on. It also stops early in two cases: if a file you told it to protect was edited, and if two attempts in a row leave the project unchanged. A turn here means one round of you asking and Claude Code answering.

## Say this to use it

Any of these will do:

- "keep fixing this until the tests pass, but stop after three tries"
- "run the build after every turn and block on failure"
- "set up a bounded loop on `pytest -q` for this repo"

Or, to be certain this skill and no other one runs:

```
/foundry-core:bounded-loop
```

It will ask for the command that decides pass or fail, the project folder to run it in, how many attempts are allowed, and which files must not change while the loop runs. That last one matters: a test file that is not protected can be edited to make a failing attempt look like it passed.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Attempt 2 of 3 blocked. Check: npm test
  FAIL  src/parse.test.js > handles empty input
  Expected: []   Received: undefined
  1 failed, 24 passed

Attempt 3 of 3. Check: npm test
  25 passed
Target met at attempt 3.
```

If the attempts run out instead, you get a report naming the budget, what changed on each attempt, the last failing output word for word, and why it stopped.

## Good to know

- **It keeps running after you set it up.** An entry is added to your project's `.claude/settings.json`, the file where Claude Code keeps settings for one project. From then on your command runs by itself at the end of every turn, in that project, until it passes or the attempts run out.
- **It reads every file in the project folder, every time it runs.** That is how it notices whether anything changed between attempts. A `.env` or a key file sitting in the folder is read into memory; only a fingerprint of the contents is kept, not a copy.
- **It writes what your command printed to disk, in plain text.** The state file keeps each attempt's full output and the report keeps the last failing output word for word. Anything your check prints, including a password it happens to echo, ends up in a file inside your project.
- **It writes into a `.bounded-loop` folder in your project by default.** One state file, and a report only if it gives up.
- **It runs whatever command you named, through `bash`.** If that command goes online, so does this. The skill contacts nothing itself.
- **Three attempts unless you say otherwise.** That number is a choice, not a measured best. Use fewer when the check is cheap to run.
- **A green result only proves the check you gave it.** The skill's own notes say so: a check that exercises one part of your code cannot catch a problem three files away. Use it for small, bounded jobs with one clear check.
- **It never asks for a key, a password or a sign-in.**
- **It needs `bash` and `python3`,** two free tools that computers used for programming usually have.

## What next

- Work out the check and the attempt limit first: [Agreeing what done means](../goal-spec/) produces exactly what this skill needs.
- The evidence standard this loop enforces: [Proving work is done](../proof-of-work/).
- For a check that runs after a deploy rather than after every turn: [smoke-gate](../../../verification-kit/skills/smoke-gate/).
- Back to the [foundry-core pack](../../README.md), or to [skill-library](../../../../README.md).
