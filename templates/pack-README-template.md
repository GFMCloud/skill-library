<!--
Blank template for a pack page. Copy this to plugins/<pack>/README.md and replace
everything in <angle brackets>. Delete every HTML comment before you commit,
except the two generated markers under "What's inside".

Keep the headings and their order exactly as they are. A reader who has read one
pack page should find the same thing in the same place on every other one.

Write for someone who has never installed a plugin. The main README defines
skill, pack, agent, hook, marketplace, slash command and repository. Any other
technical word gets a few plain words of explanation the first time you use it,
or is avoided. No em dashes. No selling.
-->

# <pack-name>

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

<!--
Two short paragraphs. The problem as the reader meets it, then what the pack does
about it. No adjectives about how good it is.
-->

## When would I use this?

<!--
Four to six bullets, each a situation the reader is in, in ordinary words. Write
moments, not features.
-->

- <situation>
- <situation>
- <situation>
- <situation>

## What's inside

<!--
Do not type the table. It is generated between the two markers from
plugins/<pack>/reader-table.tsv, one row per skill folder and per agent file.
Edit that file, then run: bash maintainers/scripts/generate-inventory.sh
The validator fails (F13) when the table is stale or a skill has no row.

reader-table.tsv is tab-separated and its first line is exactly:
kind	name	what_it_does	what_you_say	what_you_get	on_your_computer
kind is skill or agent. what_you_say is a phrase a person would really type, in
double quotes. on_your_computer says what this one skill reads, writes, runs or
connects to on the reader's computer, in one or two plain sentences, or the single
word Nothing. Write it from reading the skill's files, never from memory. A skill
whose cell says anything other than Nothing needs its own page
(templates/skill-page-README-template.md).

After the markers, one or two plain sentences that help choose between the skills.
-->

<!-- generated:whats-inside -->
<!-- /generated:whats-inside -->

## What this does on your computer

<!--
Every row, every time. Write None. where nothing applies; a missing row reads as
something being hidden. Name the skill that does each thing, name any software it
installs, give real paths. Use <br> between items when a cell lists several.
Every statement must be true of the files in this pack today. If a row here stops
being true, this table and the safety section of the main README change in the
same commit.

After the table, a paragraph starting "One limit." or "Two limits." for anything
a reader should know: a guarantee that is only written instructions, a check that
is weaker than it sounds. Leave it out if there is nothing.
-->

| | |
| :--- | :--- |
| Files read | <what, which skill, and only when> |
| Files written | <what, which skill, and where> |
| Files deleted or moved | <what, and what confirmation is required first> |
| Programs and scripts | <None. or exactly what runs and when> |
| Internet access | <None. or exactly what is fetched and from where> |
| Accounts, keys or passwords | <None. or exactly what is needed and why> |

## How the skills work together

<!--
A numbered list in the order a person would use them, or one sentence saying they
are independent and which moment each covers. Do not invent a relationship to
fill the section.
-->

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install <pack-name>@skill-library
```

The first line is only needed once, however many packs you install.

<!--
If the pack declares a dependency in plugin.json, say which pack is installed
along with it. If a skill needs other software, say which skill needs what.
-->

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
