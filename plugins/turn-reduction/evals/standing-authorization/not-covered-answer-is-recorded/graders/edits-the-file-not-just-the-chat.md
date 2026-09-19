---
type: tool_used
tool: Edit
---

The rule under test is that a NOT-COVERED answer is added to `authorization.json`
itself, not just reported back in the reply. `authorization.json` already exists
(it was written in the first step), so recording the answer means modifying that
existing file, which is an Edit, not a fresh Write. A run that only tells Graham
"go ahead, I will remember" and never touches the file has left the question askable
a second time, which is exactly the failure this case is written against.
