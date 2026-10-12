---
name: "standing-authorization"
description: "Read what you are already authorized to do out of a file instead of asking: a granted list, a stop-list, and ceilings that resolve to one value in one place. Use at the start of every session, and again before sending any question that begins should I, shall I, or do you want me to. Also checks a whole plan's steps, and the Claude Code allow rules the grants need, before work starts."
metadata:
  maturity: stable
  version: 1.2.0
  reviewed: 2026-10-11
---

# standing-authorization

The rule already existed: *"if the executor has a clear recommended action within
ceilings, take it and log it. Do not ask."* It was violated 17 times across the audit,
five of them in a single session, by sessions that had **just written the rule down**.

Prose did not bind. So this is not more prose. It is a file the agent reads and a check
that can look at a question and say the question is a defect.

## Inputs

The project's `authorization.json` (granted list, stop list, ceilings), and the question
the agent is about to send. For `check-plan`, the plan file. For `permissions`, the
project's `.claude/settings.local.json` and `~/.claude/settings.json`.

## Verify

`authz.py validate` exits 0 on the file; `authz.py check` returns exactly one of
`ALREADY-GRANTED`, `STOP-LISTED`, `NOT-COVERED` with the exit code the table below
gives it. `bash fixtures/run-fixtures.sh` prints `ALL PASS` and exits 0: it proves
`permissions` and `check-plan` fail on deliberate bad fixtures and pass on good ones.

## Done when

`ALREADY-GRANTED`: the action is taken inside its ceiling and logged where `log_to`
says, and the question is not sent. `NOT-COVERED`: the question is sent, and the answer
is added to the file so it cannot be asked twice. Before a granted chore starts,
`permissions` exits 0; before a written plan starts, `check-plan` on it exits 0.

## Stop when

`STOP-LISTED`: asking is correct and stays correct. `validate` fails: fix the file before
trusting any `check`. The granted list is empty, which is the state this file exists to
leave. The question is phrased in words no `match` entry anticipates: that is a miss,
so ask, then add the phrasing rather than widening the keywords. `permissions` exits 1:
hand Graham its output as one paste and start no chore that needs a missing rule until
it exits 0.

## Run it

```bash
# at session start, read what you may already do
python3 <this-skill-dir>/authz.py list authorization.json

# before sending any "should I…", is this already answered?
python3 <this-skill-dir>/authz.py check authorization.json --ask "should I commit these?"

# after editing the file
python3 <this-skill-dir>/authz.py validate authorization.json

# at adoption, and whenever a grant is added: do the settings allow what is granted?
python3 <this-skill-dir>/authz.py permissions authorization.json \
  --settings .claude/settings.local.json --settings ~/.claude/settings.json

# before starting a written plan: would any step turn into a question?
python3 <this-skill-dir>/authz.py check-plan authorization.json --steps PLAN.md
```

Absolute path when you need one: read `installPath` for `turn-reduction@gfm-foundry` out
of `~/.claude/plugins/installed_plugins.json`. Never construct it.

To start a new project's file, generate it rather than hand-copying:

```bash
# interactive: asks for the project name and the three ceiling values
python3 <this-skill-dir>/authz.py init authorization.json

# non-interactive: flags plus defaults
python3 <this-skill-dir>/authz.py init authorization.json --project my-project --yes
```

`init` parameterizes `authorization.example.json` (the single editable home of the
starter lists): your project name and ceiling values go in, the granted and stop lists
come through verbatim. It refuses to overwrite an existing file, and it never invents a
grant: every starter match token is a multi-word phrase, because under the substring
matcher a bare word like `proceed` or `cat` grants nearly anything (a first version of
this command proved that: 10 of 10 dangerous probe asks auto-granted; the shipped
example scores 0 of 10). After generating, TRIM the granted list down to what is true
for that project. Removing a grant is safe; the reverse is not.

## The three verdicts

`check` returns one of three, and the exit code is the point:

| verdict | exit | meaning |
| --- | --- | --- |
| `ALREADY-GRANTED` | 1 | **the ask is the defect.** Take the action, stay inside the ceiling it prints, log it where the entry says |
| `STOP-LISTED` | 0 | asking is correct and stays correct |
| `NOT-COVERED` | 0 | asking is correct. When the answer comes back, add it to the file so it cannot be asked twice |

`ALREADY-GRANTED` failing is deliberate. An approval turn that the file had already
granted is a defect with a location, not a matter of style.

## Settings that match the grants: `permissions`

Rule: a granted entry whose action needs a command the permission layer would block
lists the literal allow rules in `permissions`. Run `permissions` at adoption and each
time a grant is added, before any chore it covers. While it exits 1, hand Graham its
output as one paste, then rerun it; start the chores only when it exits 0. Never ask for
the blocked action itself. Reason: Claude Code's permission layer never reads
`authorization.json`, so a granted chore (a merge, a worktree removal, a branch
deletion) is still blocked at run time and comes back to Graham one action at a time. On
2026-10-11 that was four single-action pastes in one session, and a paste covering merge
and worktree removal but not branch deletion left a merged branch behind.

| output | exit | meaning |
| --- | --- | --- |
| `N of M granted rule(s) missing, needed by: ...` then a `{"permissions": {"allow": [...]}}` fragment | 1 | hand Graham the fragment as one paste into the project's settings; no chore that needs it starts yet |
| `all N granted rules present` | 0 | the settings hold every rule the grants list; start |

A missing settings file, or one with no `permissions.allow`, is read as an empty list
and the output says so. The command reads settings files and writes nothing; who edits
them is the global rule's business, not this skill's.

Known weaknesses: matching is exact string equality after whitespace normalisation, with
no wildcard reasoning. A broader rule that would cover a shape (say `Bash(git -C *
branch*)`) does not count, so the paste can ask for a rule the settings already cover;
and the check proves only that the string is present, not that the auto-mode classifier
will allow the command. It reads only the files named with `--settings`.

## A plan checked before it starts: `check-plan`

Rule: before starting a written plan in a project with this file, run `check-plan` on
it. Each numbered or bulleted line is one step (every non-empty line, when the file has
no list). Fix every `STOP-LISTED` or `NOT-COVERED` step before starting: reword the step,
correct the `match` token, or ask Graham once for what is genuinely uncovered. Reason:
substring matching silently turns planned steps into questions. On 2026-10-10 four
planned steps were wrongly stop-listed and four grants came back not-covered, and it
took two patch rounds to find out.

| output | exit | meaning |
| --- | --- | --- |
| one line per step: verdict, matched token (`-` for none), step text | | read every line, not only the summary |
| any step `STOP-LISTED` or `NOT-COVERED` | 1 | that step would become a question mid-run; fix it before starting |
| every step `ALREADY-GRANTED` | 0 | the plan runs without a question |
| no steps found in the file | 1 | nothing was checked |

Known weaknesses: it uses the same substring classifier as `check`, so a step classed
`ALREADY-GRANTED` by an accidental substring passes; read the matched token on each
line. A step written across several lines is read as its first line only.

## The file

```json
{
  "project": "what this file governs",
  "ceilings": {
    "commits_before_review": { "value": 10, "unit": "commits on one branch" }
  },
  "granted": [
    {
      "action": "commit to a branch that is not the default branch, up to the commit ceiling",
      "match": ["should i commit", "ok to commit"],
      "ceiling": "commits_before_review",
      "log_to": "git history plus a PROGRESS.md line",
      "permissions": ["Bash(git -C /path/to/repo commit *)"]
    }
  ],
  "stop": [
    { "action": "rewrite history", "match": ["force push", "--force", "rewrite history"] }
  ]
}
```

`match` entries are case-insensitive substrings of the question, or `re:` followed by a
regex. `ceiling` names one entry in `ceilings`, or lists several. The stop-list is checked
first and always wins. `permissions` is optional: a non-empty array of allow-rule strings
written exactly as they appear in a Claude Code settings `permissions.allow` list.

## What `validate` enforces, and why each one

**Every ceiling resolves to one stated value in one place.** A prior project referenced
"the turn ceiling" from four documents and defined it in none, and the cross-references
made the phantom read as *more* settled, not less. So: a referenced-but-undefined ceiling
is an error; a ceiling with no `value` is an error; a ceiling with no `unit` is an error,
because a bare number is not a ceiling. Duplicate keys are caught at parse time rather
than silently collapsing to the last one.

**A ceiling named in prose must be bound.** An action whose text says "limit", "cap",
"budget" or "ceiling" without a `ceiling` key is an error. That sentence is where phantoms
come from.

**Granted without logged is not granted.** Every granted entry needs `log_to`. The
original rule was "take it **and log it**"; dropping the second half turns standing
authorization into an unaudited free hand.

**One keyword, one side.** A `match` keyword appearing in both lists is an error. An
ambiguous rule is the rule that gets ignored: which is how the prose version died.

**An empty granted list is an error.** Empty is the state this file exists to leave.

**`permissions` is a non-empty array of non-empty strings, or absent, and only on a
granted entry.** Any other shape is an error, and `permissions` refuses to run on an
invalid file, because a malformed rule list cannot be checked as written. On a stop entry
it is an error too: a stop-listed action is asked, never run, so it needs no allow rule,
and a list there would be a grant hiding on the wrong side.

## Scope

`validate` checks structure. It does not judge whether the granted list is the *right*
list: that is Graham's, and only his. `check` classifies a question against the keywords
in one file; a question phrased in words no `match` entry anticipates comes back
`NOT-COVERED`, which is a miss, not a pass. When that happens the fix is to add the
phrasing, not to widen the keywords until everything matches.

The file governs one project. It says nothing about any other.

## Pairs with

- `turn-reduction:output-lint`: improves the asks that survive this.
- `turn-reduction:capability-preflight`: proves the access that granted actions assume.
