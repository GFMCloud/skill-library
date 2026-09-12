---
name: catches-placeholder-and-relative-cd
runs: 1
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Write, Bash, Skill]
---
Use the output-lint skill on this draft before I send it. Save it as `draft.md`,
run this skill's `output_lint.py` on it, and show me the linter's output.

---
Graham, run this from your terminal to rebuild the site:

```bash
cd site && ./build.sh --env <ENV>
```

Then check the 3 pages that changed.
---
