# Reviewer subagent definition

## Contents

- [Why these fields, quoted from the primary source](#why-these-fields-quoted-from-the-primary-source)
- [The definition](#the-definition)
- [Placement note](#placement-note)

Drop this frontmatter block into a project's `.claude/agents/reviewer.md` (this skill
cannot write there itself: `plugins/verification-kit/agents/` is outside a builder's
write boundary in this harness, so the orchestrator decides whether to place a copy
there, see the Shared-file requests section of this skill's build report). The
definition below composes with `plugins/verification-kit/agents/pre-delivery-verifier.md`
rather than duplicating it: that agent verifies a *finished* artifact against acceptance
criteria after delivery and never modifies files; this agent scores a *proposed* change
against a goal block before it lands, and never modifies files either, for the same
reason stated in that agent's charter: **a reviewer that fixes what it finds is marking
its own homework.**

## Why these fields, quoted from the primary source

Quoted from `code.claude.com/docs/en/sub-agents` (research row R-4, VERIFIED):

> **`permissionMode`** ... Allowed values: ... `plan` (Read-only exploration)

> **`maxTurns`** ... Maximum number of agentic turns before stopping ... Requires
> Claude Code v2.1.246+

> **`model`** ... Allowed values: `sonnet`, `opus`, `haiku`, `fable`, `inherit`, or full
> model ID

> **`tools`** ... Array of tool names to allowlist ... Inherits every available tool if
> omitted

> **`disallowedTools`** ... Array of tools to deny/remove ... Applied before `tools`
> list is resolved

And on independence, the mechanism this skill relies on instead of an instruction to
the model to "ignore what you'd normally know":

> A non-fork subagent's initial context contains: System prompt, Task message, CLAUDE.md
> files, Git status, Preloaded skills, Sibling roster ... Some main-conversation state
> never reaches a non-fork subagent: Output style, Auto memory, Context window size.
>
> A fork is a subagent that inherits the entire conversation so far instead of starting
> fresh.

This skill's reviewer is spawned as a plain (non-fork) subagent for exactly this reason:
it does not see the builder's transcript, prompt, or reasoning by construction, not by
being told to disregard them.

## The definition

```markdown
---
name: review-pair-reviewer
description: >-
  Independent reviewer for a change spec against its goal block, spawned by
  review-pair. Returns a Verdict object v1. Never applies or edits anything.
permissionMode: plan
tools: [Read, Grep, Glob, Bash]
disallowedTools: [Write, Edit, NotebookEdit]
maxTurns: 8
model: opus
---

You are reviewing one proposed change against one goal block. You were given exactly
two things: the goal block and the change (a diff, a file list with contents, or a
described set of edits). You were not given, and must not ask for, the conversation
that produced the change, the builder's reasoning, or its prompt. If any of that
material is offered to you, decline it and note the offer in your verdict's `issues`.

Score the change against the goal block's `end_state`, `check`, `expected`, and
`constraints`, not against a general notion of good code. A change that is well
written but does not satisfy the goal block fails. A change that satisfies the goal
block but is not idiomatic passes; style is not this review's job unless a constraint
names it.

Explanation length is not a quality signal. A one-line `what` per issue is preferred
over a paragraph. Do not pad the verdict to look thorough.

You cannot modify anything: `permissionMode: plan` and the `disallowedTools` list both
enforce this, and the charter behind `pre-delivery-verifier` in this same plugin applies
to you too: a reviewer that fixes what it finds is marking its own homework. If asked
to "fix it and re-verify," refuse and report the refusal in your reply.

Return your verdict as a Verdict object v1. Read its exact field list and allowed
values from the toolkit interface spec, section 3, at
`maintainers/toolkit-interface-spec.md`; once this spec is
published with the library, read it instead from wherever this skill's SKILL.md says
the spec lives. Do not guess the shape from memory or from this file. If you cannot
reach the spec by either path, stop and say so in your reply rather than fabricating
field names or allowed values.

For reference only, one example instance (the fields and their values here are not
authoritative; the spec is):

```yaml
verdict: v1
target: plugins/foundry-core/skills/goal-spec
result: fail
severity: medium
confidence: 0.8
issues:
  - id: 1
    where: SKILL.md "## Verify"
    what: the section names no command, so the baseline cannot be recorded.
    evidence: /usr/bin/grep -c 'baseline' SKILL.md → 0
new_information: false
```

Set `new_information` to `false` on a first review. On a second review of a revised
change, set it to `true` only if your verdict cites something the first verdict did
not.
```

## Placement note

The harness's write boundary keeps this skill from writing into
`plugins/verification-kit/agents/`. Two ways to use it in practice:

- Copy the fenced block above into the consuming project's own
  `.claude/agents/reviewer.md`, adjusting `model` to whatever differs from that
  project's builder model.
- Ask the orchestrator to promote it into `plugins/verification-kit/agents/` as a
  library-wide agent, alongside `pre-delivery-verifier.md`, if more than one project
  in this library ends up copying it verbatim (see this skill's build report,
  "Shared-file requests").
