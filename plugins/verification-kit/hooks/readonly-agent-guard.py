#!/usr/bin/env python3
"""readonly-agent-guard.py: deny write-shaped Bash commands inside read-only subagents.

PreToolUse hook, matcher Bash, shipped by the verification-kit plugin (hooks/hooks.json),
so its one editable home is this repository and it installs with the plugin.

Scope: fires only when the hook input carries an `agent_type` that names one of the
read-only agents below (plain or plugin-qualified). In a main session, or in any other
agent, it prints nothing and decides nothing. Inside a read-only agent it denies a Bash
command that would write outside the session scratchpad: a redirect (`>`, `>>`), `tee`,
`sed -i`, `mv`, `cp`, `rm`, `mkdir`, `touch`, `chmod`, `ln`, `install`, a git command
that changes the tree or the remote, and `python -c` or `node -e` with a write call.
Writes whose every target is under `scratchpad_dir`, `/tmp` or `/dev/null` are allowed,
so a verifier can still keep notes.

Why: `pre-delivery-verifier`'s non-modification guarantee rested on `disallowedTools`
and its charter; a sibling with the same list rewrote a file through a heredoc
(2026-08-02), and three read-only subagents in the ECC evaluation wrote files under a
prose limit (2026-09-17). This is the tool-layer boundary the charter pointed at.

Fails open with a stderr line when its input cannot be parsed: it cannot tell whether it
is inside a subagent, and failing closed would deny every Bash call in every session.
Known weakness: a command hidden behind `eval`, `bash -c "$VAR"` or a script the agent
did not write is not seen; the scratchpad allowance trusts the path as written.
"""
import json, os, re, sys

READONLY_AGENTS = {
    "pre-delivery-verifier", "silent-failure-hunter", "cross-document-checker",
    "transcript-scanner", "loop-operator", "Explore",
}

def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                      "permissionDecision": "deny", "permissionDecisionReason": reason}}))
    sys.exit(0)

try:
    data = json.load(sys.stdin)
except Exception as e:
    sys.stderr.write("readonly-agent-guard: unparseable hook input (%s); not deciding\n" % e)
    sys.exit(0)
agent = str(data.get("agent_type") or "")
if not agent:
    sys.exit(0)
short = agent.split(":")[-1]
if short not in READONLY_AGENTS:
    sys.exit(0)
if data.get("tool_name") != "Bash":
    sys.exit(0)
cmd = str((data.get("tool_input") or {}).get("command") or "")
if not cmd.strip():
    sys.exit(0)
allowed_roots = [p for p in (data.get("scratchpad_dir"), "/tmp", "/private/tmp", "/dev/null") if p]

def target_allowed(path):
    path = path.strip().strip("'\"")
    if not path or path.startswith("-"):
        return False
    return any(path == r or path.startswith(r.rstrip("/") + "/") for r in allowed_roots)

# Redirects: every `>`/`>>` target must be an allowed path. Ignore `2>&1` and `2>/dev/null`.
redirs = re.findall(r"(?<![0-9&])>>?\s*([^\s;&|)]+)", cmd)
for t in redirs:
    if t.startswith("&"):
        continue
    if not target_allowed(t):
        deny("readonly-agent-guard: %s may not write; redirect to %s is outside the scratchpad" % (short, t))
patterns = [
    (r"(^|[;&|]\s*)tee\b", "tee"),
    (r"\bsed\s+(-[a-zA-Z]*i|--in-place)", "sed -i"),
    (r"(^|[;&|]\s*)(mv|cp|rm|mkdir|touch|chmod|chown|ln|install|rsync)\b", None),
    (r"\bgit\s+(commit|push|add|rm|mv|checkout|switch|reset|rebase|merge|stash|apply|am|cherry-pick|tag|branch\s+-[dDm]|worktree\s+(add|remove)|clean)\b", "git write"),
    (r"\b(python3?|node)\s+-[ce]\s.*\b(open\([^)]*['\"][wa]|writeFileSync|writeFile|fs\.write|Path\([^)]*\)\.write)", "inline write"),
]
for pat, label in patterns:
    m = re.search(pat, cmd)
    if not m:
        continue
    name = label or m.group(2)
    # A file command whose every path argument is under an allowed root is fine.
    if label is None:
        args = [a for a in cmd.split() if not a.startswith("-") and a != name]
        if args and all(target_allowed(a) for a in args[-2:]):
            continue
    deny("readonly-agent-guard: %s may not write; '%s' changes files. Report the finding; the session that built the artifact repairs it." % (short, name))
sys.exit(0)
