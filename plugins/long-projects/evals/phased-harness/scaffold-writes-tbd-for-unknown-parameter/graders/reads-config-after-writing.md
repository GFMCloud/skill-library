---
type: tool_order
before: Write
after: Bash
---

The prompt asks for `cat ./eval-harness/CONFIG.md` after scaffolding. The Bash
read has to follow the Write of CONFIG.md, not precede it (a Bash call before any
Write would be catting a file that does not exist yet, or catting something else
and papering over it in the response text).
