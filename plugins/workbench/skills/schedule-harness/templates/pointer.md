Scheduled-task pointer v1, as defined in the harness interface spec
(`/Users/gfm/work/toolkit-build-harness/docs/interface-spec.md`, section 7). This is
the one editable home for the pointer's shape, including the Absolute-limits block v1
text embedded in it (`templates/limits-block.md.superseded` is a retired duplicate;
this file is the only place that text is edited now). `scripts/render-pointer.py`
fills the placeholders below from a small YAML or JSON input, and the result is what
gets saved to `~/.claude/scheduled-tasks/<name>/SKILL.md` when Graham (or the
`mcp__scheduled-tasks__create_scheduled_task` tool, with his approval) registers the
task. This skill never writes into `~/.claude/scheduled-tasks/` itself.

Frontmatter carries only `name` and `description`, nothing else, because the platform
reads only those two keys from this file (see references/platform-facts.md: "The file
uses YAML frontmatter for `name` and `description`, with the prompt as the body.").

The body is in the exact order the spec fixes: the harness directory (absolute), the
phase skill to read (absolute path), the mode, the absolute-limits block, nothing else.

---

```markdown
---
name: {{name}}
description: {{description}}
---

Harness: {{harness_path}}
Phase skill: {{phase_skill_path}}
Mode: {{mode}}
Absolute limits:
- no git push
- no deletion (rename to .superseded)
- no credentials
- no edits under ~/.claude/plugins/
- no edits to the harness's own CONFIG.md, CLAUDE.md, or prompts/
- no edits in a repo with uncommitted changes this run did not make
- hook timeout: {{hook_timeout}}
- consecutive-retry cap on a failed or rate-limited step: {{retry_cap}}
- anything the run would have asked becomes a queued Tier 3 item
```
