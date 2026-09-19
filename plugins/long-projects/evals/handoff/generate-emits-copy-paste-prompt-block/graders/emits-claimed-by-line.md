---
type: regex
pattern: "CLAIMED-by:"
match: contains
---

This case tests Step 6, "Output the Copy-Paste Prompt Block"
(`SKILL.md:240-261`), and specifically the claiming instruction at `SKILL.md:252`,
which the emitted block carries verbatim: append `CLAIMED-by: <session identifier>
<ISO timestamp>` to the handoff file, and stop if a CLAIMED-by line that is not
yours is already there. The failure mode is the common one: the model writes a good
handoff file and stops there, so the next session is handed a document with no
claiming step and no instruction to run Resume Mode.

The literal `CLAIMED-by:` appears nowhere in the prompt and is not a phrase a model
invents on its own, so its presence decides that the skill's Step 6 block was
actually emitted rather than paraphrased away.
