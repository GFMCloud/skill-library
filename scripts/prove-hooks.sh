#!/usr/bin/env bash
# prove-hooks.sh - prove every hook in a Claude Code settings file by deliberate failure.
# Usage: bash scripts/prove-hooks.sh [path/to/settings.json]   (default ~/.claude/settings.json)
#
# For every hook command registered in the settings file, run the command twice with the
# stdin JSON Claude Code would send it: a POSITIVE control (the payload the hook exists to
# refuse; it must answer with a deny or block) and a NEGATIVE control (a payload it must
# let through; it must answer with no decision or an allow). Both verdicts are asserted.
# A hook with no fixture, a hook that cannot run, or a settings file with no hooks block
# is RED, never silent: a guard that cannot fire is a failed guard (global rule "a gate or
# validator is trusted only after being proven by deliberate failure"; hstack review
# 2026-09-03 rows 1, 3, 5).
#
# Fixtures live in scripts/prove-hooks.d/<Event>__<matcher>[__<index>].json:
#   {"positive": <stdin json>, "negative": <stdin json>}
# Placeholders inside fixture strings are materialized as temp files before the run:
#   {{TMP_EMDASH}}  a file containing an em dash      {{TMP_PLAIN}}  a plain ASCII file
# Add a fixture for every new hook in the same commit that adds the hook.
#
# Detector arm vs exemption arm (hstack row 3, the second step, not yet implemented): a
# dead detector UNDER-blocks (positive control passes through), a dead exemption
# OVER-blocks (negative control is denied). The two controls above catch both; a
# mutation arm that corrupts each hook's pattern and expects the positive control to
# start passing would prove the fixtures themselves. Do that when a second hook exists.
#
# Re-verify against your Claude Code version (hstack row 5): the hstack author reports
# that settings keys such as `fallbackModel` and `workflowSizeGuideline` have silently
# dropped the whole hooks block in some versions. This script verifies hooks by side
# effect (the command ran and answered), never by the presence of a config key. If the
# hooks block is missing, the result is RED with that hint.
#
# Re-run after every Claude Code update: 2.1.260 alone fixed four ways a permission rule
# silently failed to apply (parentheses in paths, an uncompilable pattern, zsh substitution
# auto-approval, trailing text), so a hook or rule that was green last week is unproven today.
#
# Exit 0 only when every hook is GREEN. Output is one line per hook plus a summary.
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SETTINGS="${1:-$HOME/.claude/settings.json}"
exec python3 - "$SETTINGS" <<'PY'
import json, os, re, subprocess, sys, tempfile

settings_path = sys.argv[1]
fixture_dir = os.path.join(os.getcwd(), "scripts", "prove-hooks.d")
results = []

def red(label, why): results.append(("RED", label, why))
def green(label, why): results.append(("GREEN", label, why))

try:
    with open(settings_path) as fh:
        settings = json.load(fh)
except Exception as e:  # unreadable settings is a failed guard, not a skipped one
    red("settings", f"cannot read {settings_path}: {e}")
    settings = {}

hooks = settings.get("hooks") if isinstance(settings, dict) else None
if not hooks:
    red("settings", f"no hooks block in {settings_path} (a key that silently disables hooks? see header)")

tmpdir = tempfile.mkdtemp(prefix="prove-hooks-")
def materialize(name, content):
    p = os.path.join(tmpdir, name)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(content)
    return p
placeholders = {
    "{{TMP_EMDASH}}": materialize("emdash.html", "<p>before — after</p>\n"),
    "{{TMP_PLAIN}}": materialize("plain.html", "<p>before and after</p>\n"),
}
def fill(obj):
    s = json.dumps(obj)
    for k, v in placeholders.items():
        s = s.replace(k, v)
    return s

def verdict(stdout):
    """deny | allow | error. A hook allows by staying silent or by saying so."""
    text = stdout.strip()
    if not text:
        return "allow"
    try:
        d = json.loads(text)
    except json.JSONDecodeError:
        return "error"
    hso = d.get("hookSpecificOutput", {}) if isinstance(d, dict) else {}
    if hso.get("permissionDecision") == "deny" or d.get("decision") == "block":
        return "deny"
    if hso.get("permissionDecision") in ("allow", "ask") or d.get("decision") == "approve":
        return "allow"
    return "error"

def run(cmd, payload):
    try:
        p = subprocess.run(cmd, shell=True, input=payload, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return "error", "timeout after 30s"
    if p.returncode not in (0, 2):  # 2 is Claude Code's blocking exit code
        return "error", f"exit {p.returncode}: {p.stderr.strip()[:200]}"
    return verdict(p.stdout), p.stdout.strip()[:200]

for event, entries in (hooks or {}).items():
    if not isinstance(entries, list):
        continue
    for entry in entries:
        matcher = str(entry.get("matcher", "*"))
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", matcher)
        for j, hook in enumerate(entry.get("hooks", [])):
            label = f"{event} matcher={matcher} #{j}"
            if hook.get("type") != "command" or not hook.get("command"):
                red(label, "not a command hook; nothing to prove")
                continue
            candidates = [f"{event}__{safe}__{j}.json", f"{event}__{safe}.json"]
            fixture = next((os.path.join(fixture_dir, c) for c in candidates
                            if os.path.exists(os.path.join(fixture_dir, c))), None)
            if not fixture:
                red(label, f"unproven: no fixture ({' or '.join(candidates)} in scripts/prove-hooks.d/)")
                continue
            try:
                fx = json.load(open(fixture))
                pos, neg = fx["positive"], fx["negative"]
            except Exception as e:
                red(label, f"bad fixture {os.path.basename(fixture)}: {e}")
                continue
            pv, pout = run(hook["command"], fill(pos))
            nv, nout = run(hook["command"], fill(neg))
            if pv == "deny" and nv == "allow":
                green(label, f"positive=deny negative=allow (fixture {os.path.basename(fixture)})")
            else:
                why = []
                if pv != "deny":  why.append(f"positive control was {pv} (dead detector under-blocks): {pout or '<empty>'}")
                if nv != "allow": why.append(f"negative control was {nv} (dead exemption over-blocks): {nout or '<empty>'}")
                red(label, "; ".join(why))

reds = [r for r in results if r[0] == "RED"]
for status, label, why in results:
    print(f"{status}  {label}  {why}")
print(f"\n{len(results)} hook check(s): {len(results) - len(reds)} green, {len(reds)} red")
sys.exit(1 if reds or not results else 0)
PY
