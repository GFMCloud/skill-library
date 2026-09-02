---
name: retro
description: >-
  Write a short, gated, transcript-grounded retro for the current session and
  route each lesson to where it actually belongs (memory, project CLAUDE.md, an
  ADR, a hook, or nowhere). Use when the user says "retro", "/retro", "log a
  retro", "session retro", or at natural session-end moments after a commit
  landed, something broke and got fixed, or a decision got made that shouldn't
  need re-litigating next time. Exits silently, producing no file, when none of
  those happened. Writes to .claude/retros/ only; never touches CLAUDE.md,
  memory, or a decisions/ ADR directly, it proposes destinations and the
  session (or user) acts on the proposal.
metadata:
  maturity: incubator
---

# Retro

A retro per session, at roughly 26 sessions a week, yields about 26 documents
of which maybe 4 contain anything worth keeping. This skill exists to produce
those 4 and skip the other 22 without anyone reading them first to find out.

## 1. Gate it, this is the first action, always

Before writing anything, decide whether this session earns a retro. A session
earns one if, and only if, at least one of these is true:

- It produced a commit.
- It hit a real failure (an error, a wrong turn, a rollback) and then resolved
  or diagnosed it.
- It made a decision worth not re-litigating next time (chose between real
  alternatives, ruled something out, set a convention).

Everything else exits here. Do not write a file. Do not write a long
explanation of why you're skipping it, one line is enough: "No retro: gate
not met (no commit, no failure, no decision this session)."

**Determine the gate from evidence, not self-assessment.** Don't decide this
by recalling how the session felt, that's exactly the unreliable-narrator
failure mode section 2 exists to prevent. Check cheaply:

```bash
git -C <project-root> log --oneline --since="<session-start-time>"
git -C <project-root> status --porcelain
```

A non-empty commit log since session start satisfies the "produced a commit"
leg on its own. For the other two legs (failure hit, decision made), you need
the transcript, see section 2. If the project has no git repo, the first leg
never fires; the gate then depends entirely on the transcript scan for the
other two.

## 2. Read the transcript, not your own memory

By the time a retro gets written, your context may already be compacted. You
are not a reliable narrator of your own session, you will report the tidy
version, not what actually happened. Ground every claim in the record:

- `~/.claude/projects/<cwd-slug>/*.jsonl`, the session transcript(s).
- `git diff` / `git log`, what actually changed, if there's a repo.

**Do not read the transcript yourself.** Compose the `workbench:transcript-scanner`
agent (launch it with the `Agent` tool, `subagent_type: "workbench:transcript-scanner"`)
and ask it for exactly what section 1 and section 3 need:

- Evidence for each gate leg (commit, failure-then-fix, decision-between-alternatives),
  each with `path:line` provenance.
- For any leg that's satisfied: the specific lesson candidates, what was
  learned, what broke and why, what was decided and why, quoted or closely
  paraphrased with provenance, not invented from general knowledge of what
  "usually" goes wrong.

If the scanner reports nothing for a leg, that leg is not satisfied. Don't
fill the gap with a plausible-sounding guess.

## 3. If gated in: classify each lesson candidate

For every lesson candidate the scan turned up, decide where it belongs using
this routing table:

| Lesson type | Destination |
|---|---|
| How I want you to work (a standing preference about process, tone, or approach) | Memory, `feedback` type |
| Project mechanics or commands (how to build/run/deploy *this* project) | That project's `CLAUDE.md` |
| Architecture commitment (a structural choice that constrains future work) | A `decisions/` ADR in the repo |
| Deterministic check (something a script could catch every time) | A hook or CI, not prose |
| One-off (true once, unlikely to recur, not worth a standing rule) | The retro only, this is where it correctly dies |

**Cross-project special case:** the memory directory is scoped per working
directory. A lesson that applies across projects, not just this one, does not
belong in this project's memory, it belongs in `~/.claude/CLAUDE.md` instead
(the "how I want you to work" row, but landing globally rather than
per-project).

**Do not create a `learnings/` directory or any other second store.** The
memory system already exists, already auto-loads, and already does this job.
A parallel store of the same kind of content rots because nothing ever reads
it consistently, that's the exact failure this rule exists to prevent.

This skill **proposes** destinations. It does not edit memory, CLAUDE.md, or
a decisions folder itself, recommend the routing in the retro file and in
your response, and let the session (with the user, for anything that isn't a
pure one-off) actually make the edit. Writing the retro is not the same as
acting on it.

## 4. Where retros land

Always `.claude/retros/` under the project root, one file per session that
passes the gate. Create `.claude/retros/` if it doesn't exist yet, `.claude/`
being present or absent doesn't depend on git; it's the same per-project
mechanism directory that already holds skills and settings elsewhere on this
machine.

**No-git-repo case (decided here, since the original design left it open):**
same location, `.claude/retros/` under whatever you're treating as the
project root for this session (the working directory if there's no more
specific root). Git absence only removes the "produced a commit" gate leg and
the `git diff`/`git log` evidence sources in section 2, it does not change
where the file goes. Don't invent a different convention for git-less
projects; the point of a fixed location is that nothing has to guess.

## 5. File schema

`.claude/retros/YYYY-MM-DD-<slug>.md`, one file per session, `<slug>` a short
kebab-case description of the session's main thread (e.g.
`2026-08-13-cloudflare-pages-cutover`). Use the template at
[templates/retro-template.md](templates/retro-template.md), copy it, fill
every field, delete the lesson blocks you don't need, never leave a
placeholder unfilled in the saved file.

**Output contract, version 1.0.0:** the template's field set (Gate reason,
one lesson block per candidate with Lesson / Evidence / Confidence /
Destination / Status) is the format. If a future change to this skill adds,
renames, or removes a field, that's a breaking change to this contract, bump
this version and note the migration in this file.

## 6. What this skill does not do

- No weekly review, no cross-session synthesis, no promotion automation. That
  was the original three-piece design (`/retro`, `/retro-review`, a scheduled
  task); only `/retro` is built. Run this against real sessions first, build
  the review once a corpus of retros exists to review, per the original
  design's own recommendation.
- No tracking of "this rule hasn't been referenced in N sessions." The
  original design depended on this for a demotion pass in the (unbuilt)
  weekly review. No mechanism for it exists yet, this skill does not attempt
  one. A future `/retro-review` will need to solve this before it can do
  demotion, not just promotion.
- No scheduled task. Nothing in this skill or plugin creates one.
