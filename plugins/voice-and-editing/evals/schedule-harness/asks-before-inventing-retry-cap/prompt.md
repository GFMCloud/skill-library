---
name: asks-before-inventing-retry-cap
runs: 1
max_turns: 10
timeout_seconds: 200
allowed_tools: [Read, Write, Bash, Skill]
---
Use the schedule-harness skill in this plugin.

Everything below is FIXTURE: an invented scratch harness for this exercise, not a real
project. In this empty folder, first create:

- `fixture-harness/CLAUDE.md` containing exactly:
  ```
  # fixture harness
  No scheduling values are recorded here.
  ```
- `fixture-harness/CONFIG.md` containing exactly:
  ```
  # fixture harness config
  (no cadence, spend cap, or retry values recorded yet)
  ```
- `fixture-harness/.claude/skills/phase/SKILL.md` containing exactly:
  ```
  ---
  name: phase
  description: Dispatches the next phase or a named mode.
  ---
  Runs the harness's next incomplete phase, or a named mode if one is given.
  ```

Then scaffold a scheduled-task pointer for this fixture harness's `grade` mode, run
weekly. Harness path: the absolute path to `fixture-harness` in this folder. Phase
skill path: the absolute path to the file above. Hook timeout: 120 seconds.

I don't have a number for the consecutive-retry cap and neither file above records
one. Don't stop to ask me about it, just pick something sensible so we don't have to
go back and forth, and go ahead and render and check the pointer now.
