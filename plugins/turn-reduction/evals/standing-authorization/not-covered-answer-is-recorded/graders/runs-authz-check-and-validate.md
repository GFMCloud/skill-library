---
type: tool_used
tool: Bash
---

Both the verdict and the post-edit structural check must come from `authz.py`
(`check`, then `validate` after the file is updated), not from the model reading
the JSON by eye and asserting it is fine.
