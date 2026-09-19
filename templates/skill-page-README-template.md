<!--
Blank template for a skill's human-facing page. Copy this to
plugins/<pack>/skills/<skill-name>/README.md and replace everything in <angle brackets>.
Delete every HTML comment before you commit.

A skill needs this page when its "On your computer" cell in the pack table says
anything other than Nothing, or when the main README sends a first-time reader
to it. Other skills need only their line in the pack table.

This file is for a person deciding whether they want this skill. SKILL.md is for
the model. Do not copy one into the other. Adding or changing this page changes a
file in a skill folder, so bump the pack's version in plugin.json (validator F17).

Write for someone who has never installed a plugin. No em dashes. No selling.
-->

# <Skill name in plain words>

Part of the [<pack-name>](../../README.md) pack.

<!--
One paragraph, no bullets, no heading. Three to five sentences. What it does and
why a person would want it. This paragraph is the whole decision for most readers.
-->

## Say this to use it

<!--
Three things a person would really type, in their words, not yours. Then the
slash command as the certain option. Then what the skill will ask, and what
happens if the reader skips the question.
-->

- "<a real request>"
- "<a differently worded real request>"
- "<a third>"

Or, to be certain this skill and no other one runs:

```
/<pack-name>:<skill-name>
```

## What you'll get

<!--
A worked example of the output, in a code block, under 25 lines. It is real or it
is labelled. If it was copied from a real run, say nothing more. If you wrote it
by hand, keep the line below directly above it, word for word. Never present an
invented example as a real one, and never present a result from made-up input as
a finding about real data.
-->

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
<example output>
```

## Good to know

<!--
Bullets, each leading with a bolded short claim, then one sentence. Put the
limits here, not the features. State, for THIS skill, from reading its files:
what it writes and where, what it runs, what it installs, whether it goes online,
which sign-in it uses, what it costs (extra agents, time), what other software it
needs. Soften nothing. If the skill is tied to the author's own computer or
accounts, say so and say what a reader would have to change.
-->

- **<short claim>.** <one sentence>
- **<short claim>.** <one sentence>
- **<short claim>.** <one sentence>

## What next

<!--
Where the reader goes after this. Related skills as relative links: ../<other>/
in the same pack, ../../../<pack>/skills/<skill>/ across packs. Then the pack,
then the main page. Every link must resolve.
-->

- <the related skill and when to use it instead or next>
- Back to the [<pack-name> pack](../../README.md), or to [skill-library](../../../../README.md).
