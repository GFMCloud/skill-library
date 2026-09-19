# Checking a document against what it describes

Part of the [consistency-checker](../../README.md) pack.

This skill takes one document, such as a README, a plan or a status note, and pulls out every sentence in it that a command could prove wrong. Counts of files or tests. Words like "every", "only" and "all". Version numbers. Pointers to a section or an issue. Names of commands the program is supposed to have. Then it runs a command for each one and shows you the command and the result, so you can see what the answer rests on. It does not take the document's word for anything, and it does not take a second document's word either. Documents drift out of date quietly, and this is how you find out where.

## Say this to use it

Any of these will do:

- "does this README still match the code?"
- "check the claims in this plan against the folder"
- "this says every step is tested. is that true?"

Or, to be certain this skill and no other one runs:

```
/consistency-checker:spec-artifact-diff
```

It will ask you which document to check and what to check it against, for example the folder you are in, or the output of a command. Answer in plain English. If you do not say, it will pick the files in front of it and tell you what it picked.

## What you'll get

Below is the actual output from running this skill on a small practice project made up for the purpose, a note-keeping program whose README had been left out of date on purpose, with four of the findings and two of the closing notes cut here to keep the page short.

````
The README doesn't match the code. I've run all the checks, and here is the report.

**Ground truth:** the files on disk (`find`, Grep, and `python3 -m unittest discover -s tests -v`). There is no git repo here, so I couldn't check history.

**Defects**

```
CLAIM:  "It has 4 source files"
WHERE:  README.md:5
TRUTH:  2 source files in src/ (__init__.py, notes.py); __init__.py is empty. 3 .py files including the test file.
CHECK:  Glob/find of *.py
```
```
CLAIM:  "and 12 tests"
WHERE:  README.md:5
TRUTH:  3 tests. The runner reported "Ran 3 tests ... OK"; Grep found 3 `def test_` definitions.
CHECK:  python3 -m unittest discover -s tests -v
```

(four more findings cut here)

**Clean claims**
- The four commands `add`, `list`, `search`, and `notes add "text"` work as described. The first three exist in `main()`, and `search` is case-insensitive.

(two further notes cut here)

**Pass summary:** I extracted 11 claims. 5 checked clean or were unfalsifiable, and 6 are defects (2 counts, 1 scope quantifier, 1 identifier, 1 feature claim, 1 rationale).

Want me to fix the README? I'd correct the counts and version, drop the `export` line, fix the coverage claim, and reword the Python line. I'd leave the `export` decision to you.
````

## Good to know

- **It only looks, until you ask it to do more.** The check itself writes nothing. If you then say yes to the offer at the end, it edits the prose of the document it checked, and nothing else.
- **It never changes the files to make the document true.** If the document describes a feature that does not exist, it says so and leaves the decision with you.
- **The commands it runs only read.** In a terminal these are `find`, `ls`, `wc`, `diff`, `stat`, `git log`, and `claude plugin validate` when the thing being checked is a Claude Code pack.
- **It goes nowhere online and uses no account, key or password.** Everything it looks at is on your own computer.
- **It runs in the conversation you are already in.** No separate helper is started, so it costs you the time and the words of one longer answer. A long document means more claims and more commands.
- **Finding the claims is the weak step, not checking them.** A claim dressed as a story, such as "the check was run against this exact version", is easy to read past. If you know of one, name it and ask for it to be checked.
- **It needs something real to check against.** The output of a command, the files on disk, or the project's history. If all you have is a second document, that is another claim, not proof.

## What next

- Checking several documents at once, and against each other? Use the [cross-document-checker](../../agents/cross-document-checker.md) agent in this pack instead. It starts fresh and did not write any of the documents it is checking.
- Want the same treatment for a claim about the outside world, such as a version number or a link to someone else's issue? That is [fact-currency-check](../../../verification-kit/skills/fact-currency-check/).
- Want Claude Code to show its evidence before it says a job is done, rather than after? That is [proof-of-work](../../../foundry-core/skills/proof-of-work/).
- Back to the [consistency-checker pack](../../README.md), or to [skill-library](../../../../README.md).
