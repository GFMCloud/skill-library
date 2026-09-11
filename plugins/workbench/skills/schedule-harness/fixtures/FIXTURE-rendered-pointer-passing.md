FIXTURE: complete rendered pointer, the passing counterpart to
FIXTURE-rendered-pointer-failing.md, for the deliberate-failure proof of
scripts/check-pointer.py. Never a real scheduled-task pointer; never registered with
the desktop app or mcp__scheduled-tasks__create_scheduled_task; never presented as a
finding about real data.

---
name: FIXTURE-cfb-picks-sunday-grade
description: FIXTURE — a complete pointer for the check-pointer.py proof.
---

Harness: /Users/gfm/work/cfb-picks-harness
Phase skill: /Users/gfm/work/cfb-picks-harness/.claude/skills/phase/SKILL.md
Mode: grade
Absolute limits:
- no git push
- no deletion (rename to .superseded)
- no credentials
- no edits under ~/.claude/plugins/
- no edits to the harness's own CONFIG.md, CLAUDE.md, or prompts/
- no edits in a repo with uncommitted changes this run did not make
- hook timeout: 120
- consecutive-retry cap on a failed or rate-limited step: 2
- anything the run would have asked becomes a queued Tier 3 item
