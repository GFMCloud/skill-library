#!/usr/bin/env python3
"""replay-hooks.py - measure a hook's fire rate on real command history before wiring it.

The second proof, beside maintainers/scripts/prove-hooks.sh: that script proves a hook is correct on
fixtures; this one measures how often it would fire on real traffic, which is the number
that decides whether a WARN is signal or fatigue. Rewritten from the oops-i-did-it-again
review (2026-09-07, rows 1 and 6); ruled Q-2026-09-07-8.

Usage:
  python3 maintainers/scripts/replay-hooks.py --hook "<command>" --transcripts <dir> --fixture <fixture.json>
      [--tool Bash] [--threshold 5]

  --hook         the hook command exactly as registered in settings.json
  --transcripts  a directory of COPIED Claude Code transcripts (*.jsonl, any depth).
                 Never point this at ~/.claude/projects directly.
  --fixture      the hook's prove-hooks fixture; its "born" date (YYYY-MM-DD, the day the
                 hook was wired) splits the rate into before and after, because a rule
                 cannot have influenced a command written before it existed. A fixture
                 without "born" is refused.
  --tool         tool name to replay (default Bash; Read replays tool_input.file_path calls)
  --threshold    fires per 100 commands above which a rule is flagged NOISY (default 5)

Output is counts and rates only: total commands, transcripts read, date range, and per
rule the count and rate per 100 commands before and after the born date. It never prints
a command body, a file path from a transcript, or a session id.
Exit 0 always when it ran; the NOISY flag is the finding, not an error.
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys


def iter_calls(root, tool):
    """Yield (timestamp, cwd, tool_input) for every tool_use of `tool` under root."""
    for dirpath, _, files in os.walk(root):
        for name in files:
            if not name.endswith(".jsonl"):
                continue
            path = os.path.join(dirpath, name)
            yield ("__file__", path, None)
            try:
                fh = open(path, encoding="utf-8", errors="replace")
            except OSError:
                continue
            with fh:
                for line in fh:
                    try:
                        d = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if d.get("type") != "assistant":
                        continue
                    msg = d.get("message")
                    content = msg.get("content") if isinstance(msg, dict) else None
                    if not isinstance(content, list):
                        continue
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == tool:
                            yield (d.get("timestamp") or "", d.get("cwd") or "", c.get("input") or {})


def run_hook(cmd, payload):
    try:
        p = subprocess.run(cmd, shell=True, input=payload, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return "error", "timeout"
    out = p.stdout.strip()
    if not out:
        return "silent", ""
    try:
        d = json.loads(out)
    except json.JSONDecodeError:
        return "error", "non-json"
    hso = d.get("hookSpecificOutput", {}) if isinstance(d, dict) else {}
    if hso.get("permissionDecision") == "deny":
        return "deny", hso.get("permissionDecisionReason", "")
    if hso.get("additionalContext"):
        return "warn", hso.get("additionalContext", "")
    return "silent", ""


# Convention: a hook names its rule in parentheses right after its own name, before any
# text that could carry a filename or a path: "Blocked by deny-destructive (git push --force); ..."
RULE_RX = re.compile(r"^[A-Za-z][\w -]{0,60}?\s\(([^()]{1,80})\)")


def rule_name(text):
    m = RULE_RX.match((text or "").strip())
    return m.group(1).strip() if m else "unnamed"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook", required=True)
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--tool", default="Bash")
    ap.add_argument("--threshold", type=float, default=5.0)
    a = ap.parse_args()

    real_root = os.path.realpath(os.path.expanduser("~/.claude/projects"))
    if os.path.realpath(a.transcripts).startswith(real_root):
        sys.exit("refusing to read ~/.claude/projects directly; copy the transcripts first")
    fx = json.load(open(a.fixture))
    born = fx.get("born")
    if not born or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", born):
        sys.exit(f"fixture {os.path.basename(a.fixture)} has no born date (YYYY-MM-DD); add it")

    files = 0
    total = {"before": 0, "after": 0}
    fires = {"before": collections.Counter(), "after": collections.Counter()}
    verdicts = collections.Counter()
    errors = 0
    first = last = None
    for ts, cwd, tool_input in iter_calls(a.transcripts, a.tool):
        if ts == "__file__":
            files += 1
            continue
        day = ts[:10]
        if day:
            first = day if first is None or day < first else first
            last = day if last is None or day > last else last
        side = "after" if day >= born else "before"
        total[side] += 1
        payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": a.tool,
                              "tool_input": tool_input, "cwd": cwd})
        v, text = run_hook(a.hook, payload)
        verdicts[v] += 1
        if v == "error":
            errors += 1
        elif v in ("deny", "warn"):
            fires[side][f"{v}: {rule_name(text)}"] += 1

    n = total["before"] + total["after"]
    print(f"replay-hooks: tool={a.tool} transcripts={files} commands={n} "
          f"range={first or '-'}..{last or '-'} born={born} "
          f"before={total['before']} after={total['after']} errors={errors}")
    print(f"verdicts: " + ", ".join(f"{k}={verdicts[k]}" for k in ("deny", "warn", "silent", "error")))
    rules = sorted(set(fires["before"]) | set(fires["after"]))
    if not rules:
        print("no rule fired")
    print(f"{'rule':52} {'before':>7} {'/100':>6} {'after':>7} {'/100':>6}  flag")
    for r in rules:
        b, af = fires["before"][r], fires["after"][r]
        rb = 100.0 * b / total["before"] if total["before"] else 0.0
        ra = 100.0 * af / total["after"] if total["after"] else 0.0
        overall = 100.0 * (b + af) / n if n else 0.0
        flag = "NOISY" if overall > a.threshold else ""
        print(f"{r[:52]:52} {b:7d} {rb:6.2f} {af:7d} {ra:6.2f}  {flag}")
    print(f"threshold: a rule above {a.threshold:g} fires per 100 commands overall is too noisy to wire as a WARN")


if __name__ == "__main__":
    main()
