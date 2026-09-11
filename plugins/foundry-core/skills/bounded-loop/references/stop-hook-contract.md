FIXTURE: no. This is the verified doc contract stop-hook-verify.sh implements,
quoted so the next reader does not have to trust the script or this skill's
paraphrase of it. Source: `code.claude.com/docs/en/hooks`, fetched 2026-09-11.

## Stdin: the hook's JSON input

The Stop hook receives common input fields plus its own, in this shape (quoted
from the docs):

```json
{
  "session_id": "abc123",
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "scratchpad_dir": "/tmp/claude-1000/-home-user-my-project/abc123/scratchpad",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "last_assistant_message": "..."
}
```

The docs also note: "Hooks that need the final assistant text of the current
turn should use `last_assistant_message` on Stop and SubagentStop instead of
reading the transcript." `stop-hook-verify.sh` does not need the assistant's
text (it verifies the workspace, not the transcript), so it reads only `cwd`
from this JSON, and only as a fallback when `--repo` is not passed explicitly.

## Exit code 2: the blocking path

From the "exit code 2 behavior per event" table: "`Stop` | Yes | Prevents
Claude from stopping, continues the conversation."

From the general exit-code-2 section: "Exit 2 means a blocking error. On
events that can block, exit 2 blocks whether or not you print JSON: even a
JSON `permissionDecision` of `"allow"` can't override it. Claude Code still
reads any valid JSON output on stdout." And: "The blocking message is the
reason from your JSON's blocking decision when it makes one, and your stderr
text otherwise."

`stop-hook-verify.sh` never prints a JSON blocking decision — it prints the
check's verbatim output to stderr and exits 2. Per the quoted line above, that
stderr text **is** the blocking message Claude sees, which is what the
roadmap entry's "blocks the turn... with the actual output as
`additionalContext`" cashes out to in verified terms. See "What this skill
does NOT claim" below for the one thing left unconfirmed.

## Exit code 0: the release path

The docs list four events where plain-text stdout becomes visible context:
"For most events, Claude Code writes stdout to the debug log and doesn't show
it in the transcript. The exceptions are `UserPromptSubmit`,
`UserPromptExpansion`, `SessionStart`, and `PostModelSwitch`..." `Stop` is not
one of the four, so `stop-hook-verify.sh`'s stdout on exit 0 (the "target
met" line, or the printed escalation report) lands in the debug log only, not
automatically in the transcript. That is why SKILL.md tells the agent to read
`escalation.yaml` itself and present it — the hook's job is to gate and
record state, not to narrate.

## Decision control (Stop-specific)

The docs' decision-control table for Stop names a `"decision": "block"`
field with an associated `reason` ("Explanation of why the stop is
blocked"). `stop-hook-verify.sh` does not use this path — it uses the plainer
exit-2-plus-stderr path above, which the docs confirm has the same effect
(the turn cannot end) without needing to emit JSON.

## What this skill does NOT claim

The docs mention `additionalContext` once, generically: "for events that use
the standard decision model, Claude Code ignores the exit code and the JSON
alone decides the outcome: each field the event supports is honored,
including `permissionDecision`, `additionalContext`, `updatedInput`, and
`systemMessage`." The page does not enumerate, in the content available at
fetch time, which specific events honor `additionalContext` — the "decision
control" table that would say so per event was not fully present in what
this skill's builder could retrieve. So this skill does not assert that Stop
accepts a JSON `additionalContext` field; it relies only on the verified
stderr-becomes-blocking-message behavior above, which is sufficient to carry
the check's output back to Claude. If a future reader confirms Stop does
accept `additionalContext`, switching to it is a small change to
`_verify_impl.py`'s failing-attempt branch (emit JSON with `additionalContext`
instead of plain stderr) — note it as an open item rather than assuming it
silently.

## SubagentStop

The docs confirm `SubagentStop` exists as a separate event alongside `Stop`.
This skill only installs a `Stop` hook; a bounded loop running inside a
subagent (rather than the main session) would need the hook registered on
`SubagentStop` instead, which `stop-hook-verify.sh` supports unchanged since
it only reads `cwd` from stdin — only the hook registration in
`.claude/settings.json` differs.
