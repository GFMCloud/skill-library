# Retro: <one-line session summary>

Date: YYYY-MM-DD
Project: <project name / root path>
Session transcript: `~/.claude/projects/<cwd-slug>/<sessionId>.jsonl`

## Gate

<Which leg(s) triggered this retro. Cite evidence, not recollection.>

- [ ] Produced a commit: `<commit sha(s)>`, `git log` evidence
- [ ] Hit a real failure and resolved/diagnosed it: `path:line` in transcript
- [ ] Made a decision worth not re-litigating: `path:line` in transcript

## Lessons

<One block per lesson candidate the transcript scan turned up. Delete blocks
you don't need. Do not leave a block half-filled, if a field has nothing
real to put in it, the lesson probably isn't real either; drop it.>

### Lesson 1: <one-line statement>

- **Evidence:** `<transcript path:line, or git diff/log reference>`:
  <what the evidence actually shows, quoted or closely paraphrased>
- **Confidence:** high | medium | low
- **Destination:** memory (feedback) | project CLAUDE.md | decisions/ ADR |
  hook/CI | retro-only
- **Status:** proposed | acted-on | rejected
  <If acted-on: what changed and where, e.g. "added to ~/.claude/CLAUDE.md
  under Working agreements" or "filed decisions/0007-<slug>.md".>

### Lesson 2: <one-line statement>

- **Evidence:**
- **Confidence:**
- **Destination:**
- **Status:**

## Not promoted

<Anything the scan flagged that didn't clear the bar for a lesson block:
one line each, so the reasoning isn't lost even though nothing gets filed.>
