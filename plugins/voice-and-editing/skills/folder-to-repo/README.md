# Turning a folder into a private GitHub repository

Part of the [voice-and-editing](../../README.md) pack.

A project folder on your computer has grown into something worth keeping, and you want it on GitHub so it is backed up and has a history. The git commands for that are short. The part that goes wrong is everything around them: giving the repository a name you will still understand in a year, putting a README and a `.gitignore` in before the first commit, and above all catching a password or a key before it goes in. A file's history in git is permanent, so a key that lands in the first commit stays recoverable even after you delete the file. This skill runs the scan first, stops if it finds a key sitting inside a file you need to keep, and only then creates the repository, private by default, and uploads the folder.

## Say this to use it

Any of these will do:

- "put this folder on GitHub"
- "turn this into a git repo"
- "version control this project for me"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:folder-to-repo
```

It will ask you to confirm the folder, confirm the name it proposes, and confirm the README it filled in from what it found. If the folder already has a history, it stops and says so, because that is a different job.

## What you'll get

The scan result first, then a private repository with the folder in it.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Checked 214 files.

Whole-file secrets (added to .gitignore, not uploaded):
  .env
  terraform.tfvars

Embedded secrets: none.

Proposed name: lab-invoice-parser
  What it is: parses supplier invoices into a spreadsheet.
  Status: experiment.

First commit made (31 files).
Created a private repository and uploaded it.
Two files were left out by the scan. Both are listed above.
```

## Good to know

- **The scan is weaker than its name sounds.** It ignores any line containing a word like "example", "test_key", "dummy", "changeme", or three dots. A real key sitting on such a line is passed over without a word. A clean result is a good sign, not a guarantee, so read `git status` yourself before the commit as the skill tells Claude Code to.
- **When the scan does find something, it prints part of it.** Up to sixty characters of the match go to the screen. If the key is real, part of it is then in the record of your session.
- **A key found inside a file you need to keep is a hard stop.** It will not commit or upload. It shows you the file and the line, and leaves the fix to you. If the key was ever real, treat it as burned and replace it before continuing.
- **It creates a git repository in your folder and makes the first commit there.** Before that it copies in a README and a `.gitignore` if the folder has neither, and fills the README in from what it can work out about the project. If you already have a README it leaves yours alone.
- **It does not check which GitHub account is signed in.** On a computer signed in to two accounts, the new repository can land under the wrong one. Check first, because moving it afterwards is more work than checking.
- **It deletes a file called `START_HERE.md` from your folder at the end.** That instruction is left over from an earlier version of the skill and no such file ships with it now. It does nothing unless your own folder happens to contain a file with that name, which would then be removed.
- **The naming rule is the author's, not a standard.** It proposes names with one of his three category prefixes. Change those to your own before you use it, or ignore the name it suggests.
- **Only for a folder with no history.** If there is already a `.git` folder inside, it stops rather than trying.
- **It needs Python and git installed**, and either a connected GitHub tool or the `gh` command line tool signed in to the account you want the repository under. Without either it does the local steps and hands you the commands to run yourself rather than claiming it uploaded anything.

## What next

- If the project already has a history and you want to give a copy to somebody else without your personal files going with it, use [repo-handoff](../repo-handoff/) instead.
- To have the new project reviewed once it is up, see [fable-project-review](../fable-project-review/).
- To check one change for security problems before it ships, see [security-checklist](../../../verification-kit/skills/security-checklist/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
