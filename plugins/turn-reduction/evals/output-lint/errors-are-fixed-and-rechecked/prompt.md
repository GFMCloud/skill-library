---
name: errors-are-fixed-and-rechecked
runs: 1
max_turns: 16
timeout_seconds: 300
allowed_tools: [Read, Write, Bash, Skill]
---
Use the output-lint skill on the draft below. Save it as `draft.md`. I want to send this
message today, so save the version you would actually send as `draft-fixed.md`, then tell
me whether it is clear to send and show me the linter's output for that version. The
draft is a FIXTURE invented for this exercise; the job, the repo and the manifest do not
exist.

---
Graham, here is the check for the ingest job.

I'll add the retry wrapper and deploy it this evening.

Run this from the project root at `~/work/ingest` to reproduce the version mismatch:

```bash
import json
print(json.load(open("manifest.json"))["version"])
```
---
