# Checking a message before it goes out

Part of the [turn-reduction](../../README.md) pack.

Some messages cost you a round trip the moment they arrive. A command with a blank still in it, so pasting it fails. A block of Python labelled as if it were a terminal command. A command that only works in a folder nobody named. A sentence saying a file will be written, written before the file exists. A count of things with no list behind it. This skill checks a draft message, document or set of instructions for six faults of that kind, before it reaches you, and prints what it found with the line it found it on. It changes nothing and sends nothing.

It also prints, on every run, the two faults it does not check: whether the thing you are being asked to do is in the first line, and whether the message is asking you for more than one decision at once. Those are stated as rules, so a clean result is never read as a verdict that the message was good.

## Say this to use it

Any of these will do:

- "lint this before you send it"
- "check these instructions for placeholders and broken commands"
- "run output-lint over this hand-off note"

Or, to be certain this skill and no other one runs:

```
/turn-reduction:output-lint
```

It will ask for the draft: a file to read, or the text itself. It checks one message at a time.

## What you'll get

A list of what it found in that one draft, each with its line, and a footer naming the two things it did not check.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
draft.md:6: ERROR [announced-write] a write is announced before it is made
draft.md:9: ERROR [cwd] `pytest -q` depends on the working directory and none is stated
draft.md:14: ERROR [uncited-count] "12 tests" is a bare count
draft.md:18: WARN [placeholder] unsubstituted <path-to-notes> in prose

SCOPE OF THIS RESULT
------------------------------------------------------------------------------
  Checked: 2 fenced block(s) and the prose around them, in this input only.
  Six mechanical rules ran: placeholder, interpreter, cwd, glob,
  announced-write, uncited-count. A clean result means those six found
  nothing here. It is not a statement about the message being good, and it
  does not carry to any other message.

NOT CHECKED
------------------------------------------------------------------------------
  - Lead with the ask.
    Nothing here checks this.
  - One decision per message where possible.
    Nothing here checks this.

FAIL, 3 error(s), 1 warning(s)
```

## Good to know

- **It writes nothing and changes nothing.** It reads the one draft you point at and prints findings. It never edits the draft for you.
- **It never runs the commands in the text.** It looks at them as text and matches patterns. A command in the draft stays a command in the draft.
- **It prints your own words back, including a secret if one is there.** The findings quote the piece of the draft that triggered them, and this program blanks nothing out. Do not point it at a draft containing a password or a key.
- **A clean result covers six rules and that draft only.** It is not a judgment that the message is good, and it says nothing about the next message you send.
- **It is for outgoing messages, not reference documents.** Documentation quotes placeholders and counts on purpose, so running it over documentation produces noise. The skill says so itself.
- **It goes nowhere online.** No network call, no account, no sign-in.
- **What it needs first.** Python 3.9 or newer, a free programming tool that most computers set up for programming already have.

## What next

- To stop a question being asked at all rather than phrasing it better, use [standing-authorization](../standing-authorization/).
- The rule about not announcing a write before making it comes from [proof-of-work](../../../foundry-core/skills/proof-of-work/), in the `foundry-core` pack. [evidence-report](../../../foundry-core/skills/evidence-report/) is how the finished report is meant to read.
- Back to the [turn-reduction pack](../../README.md), or to [skill-library](../../../../README.md).
