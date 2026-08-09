---
name: "standing-authorization"
description: "Read what you are already authorized to do out of a file instead of asking — a granted list, a stop-list, and ceilings that resolve to one value in one place. Use at the start of every session, and again before sending any question that begins should I, shall I, or do you want me to."
metadata:
  maturity: stable
  version: 1.0.0
  reviewed: 2026-08-09
---

# standing-authorization

The rule already existed: *"if the executor has a clear recommended action within
ceilings, take it and log it. Do not ask."* It was violated 17 times across the audit,
five of them in a single session, by sessions that had **just written the rule down**.

Prose did not bind. So this is not more prose. It is a file the agent reads and a check
that can look at a question and say the question is a defect.

## Run it

```bash
# at session start — read what you may already do
python3 <this-skill-dir>/authz.py list authorization.json

# before sending any "should I…" — is this already answered?
python3 <this-skill-dir>/authz.py check authorization.json --ask "should I commit these?"

# after editing the file
python3 <this-skill-dir>/authz.py validate authorization.json
```

Absolute path when you need one: read `installPath` for `turn-reduction@gfm-foundry` out
of `~/.claude/plugins/installed_plugins.json`. Never construct it.

Start from `authorization.example.json` in this skill directory: copy it to the project
repo root as `authorization.json` and cut it down to what is true for that project.

## The three verdicts

`check` returns one of three, and the exit code is the point:

| verdict | exit | meaning |
| --- | --- | --- |
| `ALREADY-GRANTED` | 1 | **the ask is the defect.** Take the action, stay inside the ceiling it prints, log it where the entry says |
| `STOP-LISTED` | 0 | asking is correct and stays correct |
| `NOT-COVERED` | 0 | asking is correct. When the answer comes back, add it to the file so it cannot be asked twice |

`ALREADY-GRANTED` failing is deliberate. An approval turn that the file had already
granted is a defect with a location, not a matter of style.

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
      "log_to": "git history plus a PROGRESS.md line"
    }
  ],
  "stop": [
    { "action": "rewrite history", "match": ["force push", "--force", "rewrite history"] }
  ]
}
```

`match` entries are case-insensitive substrings of the question, or `re:` followed by a
regex. `ceiling` names one entry in `ceilings`, or lists several. The stop-list is checked
first and always wins.

## What `validate` enforces, and why each one

**Every ceiling resolves to one stated value in one place.** A prior project referenced
"the turn ceiling" from four documents and defined it in none — and the cross-references
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
ambiguous rule is the rule that gets ignored — which is how the prose version died.

**An empty granted list is an error.** Empty is the state this file exists to leave.

## Scope

`validate` checks structure. It does not judge whether the granted list is the *right*
list — that is Graham's, and only his. `check` classifies a question against the keywords
in one file; a question phrased in words no `match` entry anticipates comes back
`NOT-COVERED`, which is a miss, not a pass. When that happens the fix is to add the
phrasing, not to widen the keywords until everything matches.

The file governs one project. It says nothing about any other.

## Pairs with

- `turn-reduction:output-lint` — improves the asks that survive this.
- `turn-reduction:capability-preflight` — proves the access that granted actions assume.
