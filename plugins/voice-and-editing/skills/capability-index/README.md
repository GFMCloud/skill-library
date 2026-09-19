# Finding skills that are not loaded

Part of the [voice-and-editing](../../README.md) pack.

Not every skill on your computer is available in every session. Some packs are installed but switched off. Some skills belong to a single project folder and load only when you open Claude Code inside it. When you ask for something one of those covers, Claude Code does not know it exists, so it improvises a worse answer instead of saying where the better one lives. This skill is a hand-written list of those gaps. When your request matches an entry, Claude Code names what covers it, says where it lives, and offers to install it or switch it on. The list in the skill as published is the author's own, built around his machine and his projects, so for you it starts empty and you write your own entries into it.

## Say this to use it

Any of these will do:

- "is there a skill for this that isn't loaded?"
- "why doesn't Claude know how to do this here?"
- "what covers this, and where does it live?"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:capability-index
```

It will not ask you anything to begin with. If a match needs a pack installed or switched on, it asks you before running that command, and it will not run it on a no.

## What you'll get

A plain statement of what covers your request and where it is, then an offer.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
You: set up a check that tells me if the deploy is actually up.

Claude: That is covered by the verification-kit pack, which is not
installed here. Install it?

  claude plugin install verification-kit@skill-library

You: yes.

Claude: Installed. Plugin changes take effect in a new session, so
restart Claude Code and ask again. I have not tried to do the job
without it.
```

## Good to know

- **The list it ships with is the author's, and yours starts empty.** Its one entry points at a private project folder on his own computer. Until you replace it with entries of your own, the skill has nothing to point at and will stay quiet.
- **It reads which packs you have.** It reads `~/.claude/plugins/installed_plugins.json`, the file Claude Code keeps of your installed packs, lists the folders in `~/skill-library/plugins/`, and runs `claude plugin list`. Those three only look.
- **It asks before installing or switching anything on.** The install and enable commands run only after you say yes. That is the only point where anything changes, and installing a pack fetches it over the internet.
- **It writes nothing of its own.** The install command it may run is Claude Code's ordinary one, which writes into `~/.claude/plugins/`.
- **The list is kept by hand and goes stale.** It has drifted before, naming packs that had been merged into another and a marketplace that had been replaced. The skill carries the three commands for checking it against what is really installed, and it is worth running them before trusting an entry.
- **It needs the `claude` command line tool**, and the `skill-library` marketplace added if you want its install command to work. It uses no account, key or password.

## What next

- To find jobs worth turning into skills in the first place, see [skill-discovery](../skill-discovery/).
- To judge whether the skills you already have are worth keeping, see [toolkit-review](../toolkit-review/).
- To judge a single incoming repository or article before installing it, see [source-intake](../source-intake/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
