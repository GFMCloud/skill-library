# Decide whether something new is worth adopting

Part of the [voice-and-editing](../../README.md) pack.

Someone sends you a repository, a collection of skills, or a long article, and the question is whether to take anything from it. This skill turns that question into a decision you act on the same day. It downloads the thing and pins the exact version it read, has a separate Claude session review it with no knowledge of what you already own, then compares that review against your existing skills, then writes a table with one verdict per item: adopt it, take named pieces from it, watch it for later, or skip it. The reviewing session is kept ignorant on purpose, because a reviewer who knows what you already have tends to conclude that what you already have is fine.

## Say this to use it

Any of these will do:

- "is this repo worth adopting?"
- "review this article for my setup"
- "compare this skill pack against what I have installed"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:source-intake
```

It will first check three things and stop if any fails: that you are running it on your own computer in Claude Code, that your skill library folder is present with no unsaved changes, and that it can sign in to run a separate review session. Then it asks whether the source is a code repository, a collection of skills, or an article, because each gets a different set of review questions.

## What you'll get

A verdict for the whole source, then one row per item, each with where it would land and how much work it is.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```text
Source:  example-org/prompt-toolkit, pinned at commit 4b91e2c, read 12 March
Verdict: HARVEST  (the collection as a whole is not wanted, four pieces are)

item                         call          why                          lands in       effort
retry-with-backoff           REDUNDANT     your own version is broader  -              -
"name the failure first"     FRAGMENT      sharpens an existing step    error-handling S
budget ceiling before run    FRAGMENT      you have no equivalent       long-projects  S
screenshot-diff checker      SUPERIOR      theirs is measured, ours     verification   M
                                           is by eye
mega-prompt library          DISCARD       one-off, no reuse            -              -

Flags: the README tells the reading agent to install the pack. Recorded, not acted on.
Yours to rule on: the screenshot row changes how an installed skill behaves.
```

## Good to know

- **It downloads the thing you point it at, and that means internet access.** A repository is copied into a temporary folder; an article is saved to a file and converted to plain text.
- **It changes files in your skill library and records those changes in the library's history.** That is the point of the skill: the output is an actual change, not a note. Sending those changes to a shared server, or opening a request for someone to merge them, is never done without asking you first.
- **It deletes nothing.** A file it replaces is renamed with a `.superseded` ending and left in place until the change has been checked.
- **It writes a dated record of every review**, in `maintainers/reviews/` inside your library, so a later run finds it and does not review the same thing twice.
- **It starts several separate Claude sessions.** Those cost real time and tokens, and a large source is split into parts and reviewed up to six parts at a time.
- **It treats everything it downloads as data, never as instructions.** A README or article that tells the reviewing agent to install something or to change its own rules is written down as a finding, quoted, and not obeyed.
- **It will not run a downloaded project's own code casually.** It does so only when that would change the verdict, only in a throwaway area with no access to your accounts, and only with the exact command written down. It also refuses to run a normal history command inside a downloaded folder that arrived with its own history attached, because that alone can trigger code the sender chose.
- **It uses whatever sign-in your GitHub command-line tool already has**, and requires that this is the account owning your skill library. It never reads or prints a password or key.
- **It needs several things installed first:** Claude Code on a laptop or desktop, a copy of your skill library with nothing unsaved in it, the GitHub command-line tool signed in, git, a document converter (`anydoc` or `markitdown`), and a working sign-in for running Claude from the command line.
- **It refuses to run from a phone, a cloud session, or through a connector.** There is no reduced version. It stops and says which check failed.
- **It is built around one particular skill library at `~/skill-library`.** If your skills live somewhere else, the paths and the review-record folder are what you would have to change.

## What next

- For a collection large enough that each skill needs its own comparison: [toolkit-review](../toolkit-review/).
- For many sources at once rather than one: [sweep-harness](../../../long-projects/skills/sweep-harness/).
- Before believing a version number or a claim that a project is unmaintained: [fact-currency-check](../../../verification-kit/skills/fact-currency-check/).
- To find the gaps worth filling in the first place: [skill-discovery](../skill-discovery/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
