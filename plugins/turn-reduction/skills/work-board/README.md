# A work board with a decision inbox

Part of the [turn-reduction](../../README.md) pack.

This skill gives a project one board where its open work and your pending decisions live, so a session does not stop to ask you things in the chat. The board is a private page on your claude.ai account with five fixed columns and a "Needs you" tab. Each question there comes with a recommended answer and one line of why, and you answer with Accept, Amend or Discuss from any device, including your phone. When a session needs you to run a command, the card is marked "You run this" and shows the command with a Copy button and what you should see; once you have run it, answer I ran it. Sessions read your answers when they start and finish, act only on answers to the current version of a question, and move on to the next ready card by themselves. A card reaches Done only with evidence and a green light from a reviewing session. When you have answered or finished cards and want a session to know now, press **Tell Claude** at the top of the board: it posts a comment on the board and sends it to a Claude session that is watching it. If no Claude Code session is watching, claude.ai may answer with its own chat Claude, which cannot reach your Mac; your answers still wait on the cards for the next session.

## Say this to use it

- "set up a work board for this project"
- "adopt a board for this repo, it already has a list of open work"
- "the board template changed, regenerate this project's page"

Or, to be certain this skill and no other one runs:

```
/turn-reduction:work-board
```

It asks for the project name and, optionally, deadline groups such as "This week" and "Before launch". Without them the board has one group.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
rendered ~/work/GitHub/billing-export/.claude/work-board.html
(published as a private page: https://claude.ai/artifact/...)
wrote ~/work/GitHub/billing-export/.claude/board.json
wrote ~/work/GitHub/billing-export/authorization.json (starter tiers; trim the granted list)
seeded 6 cards: 4 Ready, 2 Needs you

Needs you (2)
  Use SQLite for v1 instead of Postgres?
  DEFAULT: Yes, SQLite for v1; revisit at 10k rows
```

## Good to know

- **It publishes one private page to your claude.ai account.** Claude does this with its own publishing tool. The page stores its cards in that page's own database. Nothing is shared until you share the link.
- **It writes three files into the project.** `.claude/board.json` (the page's address and the deadline groups), `.claude/work-board.html` (the page itself, generated from the template, never edited by hand) and `authorization.json` (what sessions may do without asking). It refuses to overwrite any of them. For an existing project it keeps an `authorization.json` that is already there.
- **The starter `authorization.json` grants real actions.** It lets sessions commit, push their own commits to a GitHub repository under the GFMCloud account after a safety check, merge and deploy to staging after a reviewing session approves, and move cards. Production, credentials, deleting things, spending money and changing what the project is for always go to your inbox instead. Cut the granted list down to what is true for the project.
- **It installs a hook.** When this pack is installed, a small program runs each time Claude Code finishes a turn. It does nothing in a project without `.claude/board.json`. In a project with one, it stops the turn from ending once if the session committed, pushed, merged, deployed or wrote to the cloud without updating the board, or if it ended by asking you a should-I question in the chat instead of adding it to the inbox. It reads that session's own conversation record on your computer to decide, and fails open on any error.
- **The push check never pushes.** `push_check.sh` confirms the active GitHub account is GFMCloud, the repository is under GFMCloud, `gitleaks` finds no secret, and the commits about to go out are exactly the ones the session made. The push is a separate step.
- **Two ways to turn it off per project.** Rename `authorization.json` to `authorization.json.superseded` and sessions may ask in the chat again; the logging rule stays. Rename `.claude/board.json` to `board.json.superseded` and the hook does nothing there.
- **The page loads three fonts from Google.** Without a network it falls back to system fonts. A local preview with no claude.ai around it shows clearly labelled fixture cards, never your data.
- **It needs Python 3.9 or newer, `git`, `gh` and `gitleaks`.** `gh` and `gitleaks` are only for the push check.

## What next

- [standing-authorization](../standing-authorization/) explains the permissions file the board setup generates.
- New projects get a board from `new-project` in the project-starters pack, before their first publish.
- Back to the [turn-reduction pack](../../README.md).
