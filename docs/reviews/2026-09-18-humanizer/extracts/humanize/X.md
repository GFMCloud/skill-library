### Items

| id | type | what it does |
|---|---|---|
| item-ebef553d | skill | Guides an agent in drafting or editing outbound written communication (emails, chat/DM, notes) so it reads as written by a specific individual rather than as generic AI output, with per-channel and per-recipient tone rules and lists of words/patterns to avoid. |

### For each item

**item-ebef553d**
- **Trigger:** Loads on-demand. Per its description, it triggers on any request to write, draft, edit, clean up, or "make this sound like me" for emails, chat messages, or notes/activity logs, on pasted-in messages needing a reply, or on follow-up help for a conversation; the description states it should default to loading for "outbound written communication of any kind."
- **What it makes the agent do:** Follows a 10-step drafting process: identify the channel (email/chat/notes), identify the recipient and relationship, identify context (instructional, escalated customer, leadership) and apply tone exceptions, "Lead with the ask or the point. Strip everything that doesn't serve it," apply listed stylistic patterns and ask "would [the author] actually send this?", "Check for em dashes and filler closers. Both are silent draft-killers. Scan before delivering," apply a channel/relationship-appropriate sign-off, "Use the message_compose_v1 tool when available" (with a subject line for emails and 2-3 goal-labeled variants for high-stakes cases), jump straight to a reply draft for pasted-in inbound messages without summarizing, and "Flag anything risky (customer escalation, pricing/commercial implications, compliance topics...) at the end of the draft, not woven into it." It also enforces three "non-negotiables" (no em dashes, no listed AI-filler phrases, no over-explanation), longer blocklists of tell-tale words/phrases and structural patterns to avoid, and channel-specific formatting rules (e.g., plain text with no markdown when content will be pasted elsewhere, specific greeting/sign-off conventions per channel).
- **Enforcement:** Prose only. There is no executable checker; the file relies on the agent reading its own draft back and manually scanning for banned words/patterns ("Scan every draft for em dashes and replace every instance before delivering"). No enforcement files are present, and there is no stated fail-open/fail-closed behavior since there is nothing that runs or exits.
- **Dependencies:** References a tool called "message_compose_v1" to use "when available," but this tool is not part of the item and no runtime, CLI, or service is otherwise named. No other items are referenced as dependencies.
- **State it writes:** None. The skill produces draft text as its output; it does not describe writing any file, log, or directory.
- **Fit with the bar:**
  - Plan then stop before consequential work: partial/ignored. The process ends with producing a draft and a risk flag, e.g. "Flag anything risky ... at the end of the draft, not woven into it," but there is no instruction to pause or seek approval before the draft is sent or acted on; sending itself is outside its stated scope.
  - Executed evidence before "done": ignored. Completion is judged by a subjective read-back ("would [the author] actually send this?") rather than any recorded check or evidence.
  - Say what was and was not checked: partial. The end-of-draft risk flag is the closest analog, but it only surfaces risky content, not a list of what stylistic or factual checks were actually run against the draft.
- **What it does not cover:** No guidance on verifying factual accuracy of drafted content; no mechanism for confirming em-dash/filler removal beyond a manual scan instruction; no coverage of languages other than the implied default; no instructions for the actual sending/delivery step; no versioning or test coverage for the skill's own rules.

### Agent-directed text

none

### Could not determine

The file references a tool named "message_compose_v1" ("Use the message_compose_v1 tool when available") but does not include or describe that tool, so its behavior, availability, or interface cannot be determined from these files.
