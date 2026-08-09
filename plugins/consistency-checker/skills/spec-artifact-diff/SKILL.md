---
name: "spec-artifact-diff"
description: "Check a document against the thing it describes — does this README match the code, do these counts and claims hold against the tree, has this spec drifted from the artifacts. Use whenever a document's claims need checking against a directory, repo, or running system, and after editing a spec and its dependent documents in the same session."
metadata:
  maturity: incubator
---

# spec-artifact-diff

The procedure for turning prose into a list of falsifiable claims and checking
each one against the thing it describes.

Use inline for a single document. For a document *set*, use the
`consistency-checker:cross-document-checker` agent instead — the check is more
reliable when run by something that did not write the documents.

## Step 1 — Name the ground truth

Before reading any prose, decide what the authority is and get it in front of
you. In order of preference:

1. The running system (a command executed, its output captured).
2. The artifact on disk (the tree, the file, the git log).
3. Nothing else. A second document is another claim.

Record the command you used. It goes in the report.

## Step 2 — Extract claims, not meaning

Read each document once looking only for assertions a command could falsify.
Ignore argument, rationale, and intent. Write each claim down verbatim with its
location.

The high-yield classes, ordered by how often they actually break:

| Class | Looks like | Check with |
|---|---|---|
| Counts | "18 files", "nine components" | `find`/`ls` piped to `wc -l` |
| Scope quantifiers | "each", "every", "only", "all", "empty" | enumerate the set and test the predicate on every member |
| Status words | "verified", "tested", "complete" | locate the evidence the word claims exists |
| Cross-references | "§8", "item 4", "issue #53948" | resolve the target and confirm it says what the reference implies |
| Identifiers | SHAs, versions, byte counts, paths | `git log`, `stat`, `wc -c` |
| Arithmetic | percentage splits, "N of M", subtotals | add it up |

A quantifier is a claim about **every** member of a set. Checking one member
and generalising is how "one placeholder component each" survived a review over
a set that was unevenly distributed.

## Step 3 — Run the check

One check per claim, executed. Not inferred, not recalled, not read off a
second document.

Where a tool reports its own outcome, verify the outcome independently, **and
verify at the level the failure lives.** Originating failure, 2026-07-27:
`claude plugin validate` at a marketplace root reported "Validation passed"
while an agent's frontmatter was unparseable. The root check passed precisely
because it never descended to where the defect was. Per-plugin validation
caught it in one command.

## Worked example: a check scoped to the wrong thing

This skill already warns that a check can pass because it never reaches the
defect. There is a second form of the same error, and it is harder to see: **a
check scoped to a directory tree rather than to the active version.**

### The setup

A marketplace's plugin files were edited and pushed. The question was whether
the installed cache actually reflected the repo. The check used was:

```bash
find ~/.claude/plugins/cache/gfm-foundry -name '*.md' | xargs wc -c
```

Byte counts matched the repo. The check passed. **It was not a check.**

### Why it proves nothing

The plugin cache stores **each installed version in its own directory**, and
orphaned versions are only removed **14 days** after they are superseded — a
deliberate grace period so concurrent sessions that already loaded the old
version keep working.

So at any moment the cache legitimately holds several versions of the same
file. A tree-wide search finds the correct bytes in *some* directory. It would
have reported exactly the same "match" if every plugin were serving stale
content, because it never asked **which version is live.**

In the session where this was used it passed for the right answer by luck. The
same command had already been wrong once that day: after a shared dependency
was edited, both `marketplace update` and a dependent's `install` reported
success while the dependency's cache still held the superseded file and was
missing a new one entirely — because reinstalling a *dependent* does not
refresh an already-installed *dependency*.

### The correct form

Resolve the version actually in use, then compare against that path only:

```bash
claude plugin details <plugin>@<marketplace>   # resolve the pinned SHA
diff <repo-path>/SKILL.md \
     ~/.claude/plugins/cache/<marketplace>/<plugin>/<PINNED_SHA>/skills/<skill>/SKILL.md
```

Pinned SHAs **legitimately differ per plugin** in the same marketplace, so a
single SHA cannot be assumed across a whole marketplace.

### The general form

Both failures in this family have the same shape: **the scope of the check
excluded the place the failure lives.**

| Check | Scope | What it could not see |
| --- | --- | --- |
| `claude plugin validate` at the marketplace root | The manifest | An agent's unparseable frontmatter one level down |
| `find` across the cache directory | Every version ever fetched | Which version is actually being served |

**When writing a check, state what it would fail to detect.** If that answer
is "the thing I am checking for," the check is decoration.

Note also that Glob and Grep *do* skip orphaned version directories — so a
check written with those tools would not have had this flaw. Shell `find`
does not skip them. **The tool you reach for changes what your check can
see**, which is one more reason to name the scope explicitly rather than
trusting a search to do it for you.

## Step 4 — Classify each defect

- **Documentation defect** — the artifact is right, the prose is wrong. The fix
  is to the prose. This is the overwhelming majority. *Who* applies it depends
  on who is running this procedure: a session working inline fixes its own
  prose; `cross-document-checker` reports and never edits, whatever it is told.
- **Artifact defect** — the prose describes the intended state and the artifact
  missed it. Fix the artifact, separately, as its own piece of work.
- **Conflict** — two documents assert different decisions. Not a diff. Escalate
  with both locations named.

Never resolve a defect by changing the artifact so the prose becomes true.

## Step 5 — Report

Four fields per defect, all required:

```
CLAIM:  "18 files" — status.md, "Where item 3 landed"
WHERE:  claude/status.md:14
TRUTH:  16 tracked files
CHECK:  git ls-files | wc -l
```

Then a one-line pass summary: how many claims were extracted, how many checked
clean, how many defects, split by class. A clean pass still gets a report.

## Known failure mode of this skill

Extraction is the weak step, not verification. Claims that read as narrative
rather than as numbers get skipped — "the acceptance check ran against this
exact tree" is a falsifiable claim about a commit SHA wearing prose clothing.
When a sentence asserts *that something happened*, it is a claim; find the
identifier it implies and check that.
