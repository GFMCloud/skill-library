# Install help

Part of [skill-library](../README.md).

Everything on this page is typed **inside a running Claude Code session**, at the prompt where you normally type your requests. Not at an ordinary terminal prompt.

The two commands the main page gives you are:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install foundry-core@skill-library
```

The first is needed once, ever. The second is needed once per pack, with that pack's name in place of `foundry-core`.

The sections below are in the order the problems tend to happen.

## Nothing happened when I typed the command

Check where you typed it. If the line you are typing on does not belong to Claude Code, these commands do nothing at all.

Open a terminal, type `claude` and press Enter. Wait for Claude Code's own prompt to appear. Then type the command there.

If you are in Claude Code and it answered in prose instead of running something, check the slash. It has to be the first character on the line, with no space in front. `/plugin` works. ` /plugin` does not.

## Adding the marketplace did not work

**"Marketplace not found", or nothing was added.** Check the spelling. It is `GFMCloud/skill-library`: the owner's name, a slash, then the repository's name. No `https://`, no `github.com/`, no trailing slash.

**You are not sure whether it worked.** A successful add prints a confirmation naming the marketplace `skill-library`. If you missed it, running the add command again does no harm.

**It still fails.** The command reaches GitHub, so it needs an internet connection. If you are behind a company network that blocks GitHub, this will not work from there.

## Installing a pack did not work

**"Marketplace not found" when installing.** You have run the install command before the add command. Run the `marketplace add` line first, then the install line.

**The pack name was not recognized.** The install command is the pack's name, then `@skill-library`, with no spaces:

```
/plugin install verification-kit@skill-library
```

The exact names are in the table on [the main page](../README.md). If you are not sure which one you want, see [which-pack.md](which-pack.md).

**It installed something extra.** If the message says `+ 1 dependency: foundry-core`, that is expected. Some packs need `foundry-core` to work, and Claude Code installs it for you. [which-pack.md](which-pack.md) says which ones.

**You were asked where to install it.** Claude Code asks you to pick a scope. **User** means the pack is available in every folder you work in, which is what most people want. **Project** means this one repository, for everyone working in it. **Local** means this one repository, for you alone. Press Enter to confirm your choice.

**The install screen did not tell you what is inside the pack.** For a marketplace like this one, the "Will install" list, the context cost and the last-updated date may be missing or may say the contents are worked out at install time. That is not a fault, but it does mean the screen will not tell you what you are getting. Read the pack's own page here instead. Every skill is plain text you can open in your browser first.

**You want to check whether it installed.** List what you have:

```
/plugin list
```

Your pack should appear by name.

## The pack is installed but the skills are not there

Type:

```
/reload-plugins
```

If it warns that your next message will re-read the whole conversation, and you do not mind that, run `/reload-plugins --force`. Otherwise close Claude Code and start it again, which has the same effect.

## The skill is there but does not start when I describe what I want

Claude Code picks a skill by reading its one-sentence description and comparing it with what you asked. If your wording is far from that description, it may pick nothing.

Two fixes. Reword your request using the words on the skill's own page. Or name the skill directly with its slash command, which is the pack name, a colon, then the skill name:

```
/consistency-checker:spec-artifact-diff
```

Not `/spec-artifact-diff`. The pack name in front is there so two packs can each have a skill of the same name without a clash. If you cannot remember the rest, type `/` and start typing the pack name, and Claude Code will offer the options.

[how-a-skill-works.md](how-a-skill-works.md) explains why this happens.

## The skill started and then said it needs other software

Some skills here run small programs, and those programs need something already on your computer, such as Python, Node or `git`. The skill checks first and tells you what is missing.

Each pack page lists which of its skills needs what, under **Install**. [which-pack.md](which-pack.md) has the same information in one table. Install the missing program the way you normally would on your computer, then run the skill again.

A few skills install what they need themselves rather than stopping to ask. The pack pages say which, so read the page before running one of those if you would rather it did not.

If you do not want to install the extra software, that one skill will not work and the rest of the pack still will.

## Updating a pack

To get the newest version of this catalog:

```
/plugin marketplace update skill-library
```

Claude Code also checks for updates on its own shortly after a session starts, and tells you when there is one.

## Removing a pack

To remove one pack and keep the others:

```
/plugin uninstall foundry-core@skill-library
```

To turn a pack off without removing it, so you can turn it back on later:

```
/plugin disable foundry-core@skill-library
```

And to turn it back on:

```
/plugin enable foundry-core@skill-library
```

A pack that was installed as a dependency stays after you remove the pack that needed it. Claude Code tells you so when you uninstall: for example, removing `consistency-checker` reports that `foundry-core` is no longer needed. To clear those leftovers, run `claude plugin prune` in an ordinary terminal, outside Claude Code. Use `/plugin list` to see what is still there.

## Removing everything

Removing the marketplace also uninstalls every pack you installed from it. That is one command:

```
/plugin marketplace remove skill-library
```

Files a skill wrote while you were using it stay where they are. They are your files, in your projects, and nothing removes them for you. The main page's table under [Is this safe?](../README.md#is-this-safe-what-does-it-do-on-my-computer) lists the places a skill writes to outside your project folder.

## If you installed `workbench` or `graham-voice` before 19 September 2026

Those two packs were reorganized. You do not have to do anything in most cases.

- `workbench` is now `long-projects`, and `graham-voice` is now `voice-and-editing`. Claude Code moves you onto the new names by itself.
- If Claude Code reports that the old pack is missing, run the install command for the new name once:

```
/plugin install long-projects@skill-library
```

```
/plugin install voice-and-editing@skill-library
```

- Some skills that used to be in `workbench` now live in two other packs, `project-starters` and `agent-tooling`. Those are not moved for you. If you want them, install them by hand with the same command.

[CHANGELOG.md](../CHANGELOG.md) has the full list of which skill went where.

## Still stuck

Open an issue at [github.com/GFMCloud/skill-library/issues](https://github.com/GFMCloud/skill-library/issues). Say what you typed and what you saw. A copy of the line and the message it gave you is enough.

## Back to the main page

[skill-library](../README.md) lists all the packs and explains the terms used here.
