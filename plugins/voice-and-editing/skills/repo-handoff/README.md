# Handing a project to somebody else

Part of the [voice-and-editing](../../README.md) pack.

Somebody wants to run a project you built around your own material: your name and contact details in the settings, your data files, your league or client names, maybe audio or articles you do not own. You cannot give them the folder as it stands, and deleting the obvious files is not enough, because a project's history keeps every version of every file that was ever in it. This skill searches both the current files and the whole history for the words that identify you, sorts every file into ships, needs changing, or never ships, then builds a fresh copy in a separate scratch folder with no history behind it. It proves that copy clean with a search and a secret scanner before it creates anything, then makes a private repository for the recipient and writes them a walkthrough it has run itself first.

## Say this to use it

Any of these will do:

- "make a copy of this project I can hand to a friend"
- "sanitize this repo before I share it"
- "set this project up for someone else to run"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:repo-handoff
```

It will ask who the recipient is and where their copy should live, and it will ask you for the list of words that identify you: your name, employer, phone, email address, team or client names, account numbers, and any kind of file you want kept out. It shows you that list and lets you add to it before it starts searching. It does not guess any of these.

## What you'll get

The proof that the copy is clean, then the repository and the walkthrough.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Never ships (4 files)
  data/members-2026.csv     personal data
  notes/interview.m4a       recording I do not own
  .env                      keys
  config/my-league.json     replaced by config/example.json

Clean check on the delivered copy
  identifier 1: 0 files
  identifier 2: 0 files
  gitleaks exit: 0
  find for .env, keys, credentials: nothing

Created a private repository for the recipient.
Ran all 7 commands from AGENT-WALKTHROUGH.md against the copy.
Command 4 printed a different number than the document claimed.
Document corrected, command rerun, both now agree.

They must supply: their own league file, their own API key.
```

## Good to know

- **Your own project is not changed.** The copy is built in a separate scratch folder. Your files, your history and the address your project uploads to are left as they were.
- **The copy starts with no history.** Your history never travels with it, which is the point, since the identifying material is usually somewhere in it.
- **It searches the history, not only the current files.** For each word you gave it, it searches every version of every file that project ever had.
- **Two points stop the work.** A word or a key still present in the copy stops it before anything is created. A command in the walkthrough that fails, or prints a different figure than the document claims, stops it before handover. Both mean fix and rerun, not carry on.
- **It runs the commands it wrote itself.** The last step takes the walkthrough document it has written and runs every command in it against the new copy, so the instructions are proven before the other person follows them. That does mean the skill runs commands it composed, against the copy, and the output of each goes into the record.
- **It needs `gitleaks`, a secret scanner, and stops without it.** It also needs git and the `gh` command line tool signed in.
- **It uses your GitHub sign-in and does not check which one.** On a computer signed in to two accounts the new repository can land under the wrong one. Check first.
- **Check who can see the repository before the first upload.** The bundled checklist records a real case where a public copy of a project was about to receive personal data, which is why the check comes before the write rather than after.
- **It is not a way to give somebody your sign-in.** The recipient uses their own account, or none. Anything they must supply themselves is listed for you at the end.

## What next

- If the folder has no history yet and it is your own project going up, use [folder-to-repo](../folder-to-repo/) instead.
- To have the copy reviewed before you hand it over, see [fable-project-review](../fable-project-review/).
- To check one change for security problems before it ships, see [security-checklist](../../../verification-kit/skills/security-checklist/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
