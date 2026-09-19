---
name: <must-equal-directory-name>
description: >-
  <What this skill produces, when to use it, and the trigger phrases a user would
  actually say. Third person. This field is how the skill gets chosen at all.>
metadata:
  maturity: incubator        # incubator | stable | deprecated (a label; no staging pack)
  # version: 1.0.0           # required once stable (semver)
  # reviewed: YYYY-MM-DD     # required once stable
  # supersedes: <skill-name> # required when deprecated
# allowed-tools:             # optional runtime fields; set them deliberately
# model:
# disable-model-invocation: true   # slash-command-only; turns off auto-invocation
---

<!--
Blank template for a SKILL.md. Copy this to
plugins/<pack>/skills/<skill-name>/SKILL.md and replace everything in <angle brackets>.
Delete every HTML comment before you commit.

Frontmatter rules, all of which a check or a reviewer will catch:
  name         Must equal the folder name exactly. Lowercase letters, numbers and
               hyphens only. Under 64 characters. No leading, trailing or doubled
               hyphens. Must not contain the words "anthropic" or "claude".
               Never helper, utils, tools, data, documents. Not used by any other
               skill in any pack.
  description  Third person. Says WHAT it produces and WHEN to use it, with the
               words a user would really say. Say what it is not for and what it
               costs (a subagent, a long read, a network fetch). At least 40
               characters, well under 1,024. Write it first, before the body.
  maturity     New skills start as incubator, inside the pack they belong to.
               Promotion to stable adds version and reviewed; nothing moves.

Body rules:
  Under 500 lines. Long material goes in references/ and is linked from here.
  Assume the model is already capable. Write only what it could not have known.
  One term per concept. Concrete examples, never abstract ones.
  Forward slashes in every path.
  Every file this body names ships with the skill (validator F18).
  Eval cases do not go in this folder. They live in plugins/<pack>/evals/<skill-name>/.
  No em dashes, except inside a code fence or a blockquote that has to show one.
  If this file is another project's text kept unmodified, put a SOURCE.md beside
  it naming the upstream and the commit; its text is then left as written.

The four contract sections below are this library's add-on to the standard. Keep
their names and their order. The validator fails a stable skill that lacks one
and warns on an incubator skill.
-->

# <Skill title>

<!-- One line saying what this produces. Not a restatement of the description. -->

<!--
The steps, the output format and the rules go here, structured around what the
skill must DO. Shape each rule as: when X, do Y, unless Z, proven by W. Link
long material like this, one level deep only. Delete the line if there is none.
-->

See [references/<file>.md](references/<file>.md): <what is in it, and when it is needed>

## Inputs

<!-- What the skill needs before it starts: files, values, questions answered. "None" is a valid one-line answer. -->

## Verify

<!-- The check the skill runs or shows to prove its work held: the command, the thing observed, or the fixture, and what output means pass. -->

## Done when

<!-- The end state, stated so a reader can confirm it without asking the author. One measurable line. -->

## Stop when

<!-- At least one condition that is not "done": a budget used up, a blocker only the user can clear, no check that can be named. -->

## Output contract

<!--
Only if other agents, skills or pipelines consume this skill's output. Define the
format here or in a referenced schema file, and give it a version. A change to it
is a breaking change. Delete this section otherwise.
-->
