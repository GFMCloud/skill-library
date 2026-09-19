# Security

## Why this matters for a pack repository

A Claude Code pack can run programs on your computer with your own user permissions. That is true of any pack from anywhere, including the ones here. Anthropic does not check what is inside a third-party pack and cannot promise it does what it says it does. Install only from sources you trust, and read what a pack says it does before you install it.

## What the packs here do

Some packs here are instructions only. Others ship programs, go online, or use a sign-in that is already on your computer. One pack, `verification-kit`, installs a hook, which is a program that runs by itself in every session.

The list of what each pack does is kept in one place so it cannot disagree with itself: the section "Is this safe? What does it do on my computer?" on the [main README](README.md), and the table "What this does on your computer" on each pack's own page. Those tables were written from reading the files, and a change that makes one untrue has to correct it in the same change.

You do not have to take that on trust. Every skill is a text file. Open `plugins/<pack>/skills/<skill>/SKILL.md` in your browser and read it. Programs a skill ships sit in the same folder, usually under `scripts/`.

## Reporting a problem

Do not open a public issue for a security problem. A public issue tells everyone about the problem before there is a fix.

Report it privately through GitHub:

1. Open the [Security tab](https://github.com/GFMCloud/skill-library/security) of this repository.
2. Choose "Report a vulnerability".
3. Say which file or pack, what it does that it should not, and how you noticed.

Only people who maintain this repository can read what you send. You need a GitHub account to use that form. This library is maintained by one person, so there is no promised response time.

## What counts as a security problem here

- **A skill or a program that does something its pack page does not say it does.** For example, a skill that writes outside the folder its page names, or goes online when its page says it does not.
- **A request for a credential in the conversation.** No skill here should ask you to paste a password, a key or a token, in any wording.
- **A credential written somewhere it should not be,** such as a log, a report or a file that gets committed.
- **Instructions that could make Claude Code act on text from a file or a web page it was asked to read,** rather than treating that text as data.
- **A delete, move or overwrite without an explicit yes,** where the pack page says one is required.
- **A way past the `verification-kit` hook that its pack page does not already list.** That page says plainly what the hook does not catch.
- **A claim in a safety table that is no longer true** after a change.

## What is not a security problem

A skill giving a wrong answer, missing something in a review, or misreading a file is a bug. Use the ordinary "Something is not working" issue form for those.

## If you install packs from elsewhere

Three habits worth keeping:

1. Read the `SKILL.md` files before installing. They are text.
2. Look for a `scripts/`, `hooks/` or `bin/` folder, or an `.mcp.json` file. Those mean the pack can run programs or reach other services. That is not automatically wrong, and several packs here have them, but it should be explained on the pack's own page. If it is not explained, do not install it.
3. Install one pack at a time and use it for a while before adding another. It is much easier to notice something odd when you know what caused it.
