---
type: regex
pattern: "claims: v1"
match: contains
target: { source: file, path: handoff-eval.md }
---
The handoff must include a Typed claim v1 block, not just narrative prose, so a resume
session has something mechanical to re-check.
Read from the files the run created, because the block belongs in the handoff file, not in
the chat reply.
