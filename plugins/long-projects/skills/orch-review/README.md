# Reviewing a code change with several reviewers

Part of the [long-projects](../../README.md) pack.

One reviewer that reports "looks fine" looks exactly the same whether it read every file or quietly skipped half of them. This skill splits the review into separate jobs, correctness, hidden failures, and security where the change touches sign-in or user input, and gives each one to a separate Claude helper that sees the change and nothing else. It then removes findings the helpers both raised, and sends every serious one to a fresh helper whose job is to argue it is wrong. What survives that is reported as blocking. If any part of the review did not run, it says so and refuses to report an approval.

## Say this to use it

Any of these will do:

- "orch-review these changes"
- "review this pull request with several reviewers"
- "fan-out review on 412"

Or, to be certain this skill and no other one runs:

```
/long-projects:orch-review
```

It takes one thing, and you can leave it out. Leave it out and it reviews the changes you have not yet recorded in your project's history. Give it a number, or a GitHub address ending in a number, and it reviews that pull request instead. A pull request is a change offered to a shared project on GitHub, waiting for someone to accept it.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
verdict:    CHANGES_REQUESTED
dimensions: 3 of 3   failed: none
stats:      raw 11  unique 8  confirmed 2  unverified 1  refuted 1

blocking:
  api/upload.py:64  high  path taken from the request is joined to the upload
                    folder with no check, so "../" escapes it
                    evidence: dest = os.path.join(UPLOAD_DIR, request.form["name"])
                    [confirmed]
  api/upload.py:81  high  the except block writes to the log and returns 200, so
                    a failed save is reported to the caller as a success
                    evidence: except Exception as e: log.warning(e); return 200
                    [could not verify: needs the tests run]

advisory:
  api/upload.py:22  medium  the retry count is fixed at 3 and is not read from
                    settings like the others
  api/upload.py:95  low  refuted: the reviewer read this as an unclosed file,
                    the "with" block two lines up closes it

not checked: the JavaScript in web/upload.js, no reviewer covered it
```

## Good to know

- **It changes no files and approves nothing.** It reads the change and prints findings. Acting on them is yours.
- **It runs two things on your computer.** `git diff`, to see your uncommitted changes, and for a pull request the GitHub command line tool `gh`. It needs both of those installed for their modes.
- **Pull request mode goes online, local mode does not.** `gh` contacts GitHub. Reviewing your own uncommitted changes makes no network connection at all.
- **It uses the GitHub sign-in `gh` already has.** It never reads, asks for or writes a password or key of its own.
- **It starts three to five extra Claude helpers per run**, which costs tokens and takes longer than a single review. There is no way to run it with one.
- **It refuses an argument it does not recognise.** Only a bare number, or a pull request address ending in one, is accepted, and only the number is ever put into a command. Anything else stops the run.
- **It will not print an approval when a reviewer failed to run.** A helper that errored, timed out or could not start makes the whole result incomplete, and the missing parts are named.
- **Findings that need code to be run stay in the blocking list.** Reviewers read, they do not execute, so a suspicion they cannot settle is reported as unverified rather than dropped. This is noisy on purpose.
- **Two of its review jobs come from another pack.** Install [verification-kit](../../../verification-kit/README.md) as well, or those two jobs will not run and the result will be incomplete.

## What next

- Reviewing a whole change is the review step of [orch-pipeline](../orch-pipeline/), which also plans and makes the change.
- To judge one proposed change against what it was meant to achieve, before it is made: [review-pair](../../../verification-kit/skills/review-pair/).
- For writing rather than code, two reviewers against a rubric: [santa-method](../santa-method/).
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
