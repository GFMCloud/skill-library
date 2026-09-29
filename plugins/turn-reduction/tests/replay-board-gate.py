#!/usr/bin/env python3
"""Replay local Claude Code transcripts through board_gate.py's matching functions.

Opt-in and local only: transcripts live on this machine, so no CI job runs this. The
fixture proof (prove-board-gate.sh) checks the cases someone thought of; this checks the
commands and messages sessions really produced, so a person can judge each hit.

    python3 plugins/turn-reduction/tests/replay-board-gate.py [--n 60] [--projects-dir DIR]

It reads the N most recently modified `<projects-dir>/*/*.jsonl` files (default
~/.claude/projects, main-session transcripts only; sub-agent files in deeper folders are
not read) and, for the main session only (sidechain entries skipped, as the hook does):

  (a) every Bash or terminal command is passed to board_gate.trigger_hits (what
      triggers_in counts) with the built-in trigger list; each trigger that fires is
      printed with the shell segment that fired it, as the hook matched it (from the
      command position, quoted words with spaces shown as Q, heredoc bodies removed).
  (b) the final assistant message of each turn (the text the turn ended on, as the hook
      builds it) is passed to board_gate.ask_sentence, then offer_sentence; each hit is
      printed with the sentence that matched, as a should-I ask or an offer.

A hit is what the hook would count, not a verdict that the hook would block: (a) is
cleared by a later board write and (b) by an inbox card (an offer only by the INBOX
marker), and a transcript from a project without a board never blocks at all. Checks (c)
and (d) read tool results and board writes across a session, so this does not replay them. Transcripts are opened read-only and never written.
Output carries short excerpts (--excerpt characters, default 160, whitespace collapsed),
never whole messages or tool output. Exit 0 after a completed replay, whatever it found;
exit 2 when no transcript was found.
"""
import argparse
import glob
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "..", "hooks", "board_gate.py")


def load_hook(path):
    spec = importlib.util.spec_from_file_location("board_gate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def excerpt(text, width):
    one = " ".join((text or "").split())
    return one if len(one) <= width else one[: width - 3] + "..."


def replay(bg, path, width, hits, counts):
    label = "%s/%s" % (os.path.basename(os.path.dirname(path))[-40:], os.path.basename(path)[:8])
    last_text, prev_text, turn_line = "", False, 0

    def close_turn():
        # A --hook from before 1.3.7 has asks_should_i only, and no offer check.
        if hasattr(bg, "ask_sentence"):
            ask = bg.ask_sentence(last_text) if last_text else ""
        else:
            ask = last_text if last_text and bg.asks_should_i(last_text) else ""
        offer = bg.offer_sentence(last_text) if last_text and not ask and hasattr(bg, "offer_sentence") else ""
        if ask:
            hits.append(("(b)", "should-I ask", label, turn_line, excerpt(ask, width)))
        elif offer:
            hits.append(("(b)", "offer", label, turn_line, excerpt(offer, width)))
        if last_text:
            counts["final messages"] += 1

    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for n, line in enumerate(fh, 1):
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            if not isinstance(entry, dict):
                continue
            if bg.is_prompt(entry):
                close_turn()
                last_text, prev_text = "", False
                continue
            if entry.get("type") != "assistant" or entry.get("isSidechain"):
                continue
            content = (entry.get("message") or {}).get("content") or []
            if not isinstance(content, list):
                continue
            texts, used_tool = [], False
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text":
                    texts.append(block.get("text") or "")
                elif block.get("type") == "tool_use":
                    used_tool = True
                    if (block.get("name") or "") in bg.SHELL_TOOLS:
                        cmd = str((block.get("input") or {}).get("command") or "")
                        counts["commands"] += 1
                        for kind, seg in bg.trigger_hits(cmd, []):
                            hits.append(("(a)", kind, label, n, excerpt(seg, width)))
            if used_tool:
                last_text, prev_text = "", False
            elif texts:
                joined = "\n\n".join(texts)
                last_text = (last_text + "\n\n" + joined) if prev_text else joined
                prev_text, turn_line = True, n
    close_turn()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--n", type=int, default=60, help="how many of the most recent transcripts (default 60)")
    ap.add_argument("--projects-dir", default=os.path.expanduser("~/.claude/projects"))
    ap.add_argument("--excerpt", type=int, default=160, help="excerpt width in characters (default 160)")
    ap.add_argument("--hook", default=HOOK, help="board_gate.py to replay through (default: this pack's)")
    args = ap.parse_args()

    bg = load_hook(args.hook)
    files = [p for p in glob.glob(os.path.join(args.projects_dir, "*", "*.jsonl")) if os.path.isfile(p)]
    files.sort(key=os.path.getmtime, reverse=True)
    files = files[: max(args.n, 0)]
    if not files:
        print("REPLAY: no transcripts under %s" % args.projects_dir)
        return 2

    hits, counts = [], {"commands": 0, "final messages": 0}
    for path in files:
        replay(bg, path, args.excerpt, hits, counts)

    for check, kind, label, line, text in hits:
        print("%s %-14s %s:%d  %s" % (check, kind, label, line, text))
    a = [h for h in hits if h[0] == "(a)"]
    b = [h for h in hits if h[0] == "(b)"]
    by_kind = {}
    for h in a:
        by_kind[h[1]] = by_kind.get(h[1], 0) + 1
    print("-" * 78)
    print("REPLAY: %d transcripts, %d shell commands, %d final messages" %
          (len(files), counts["commands"], counts["final messages"]))
    print("REPLAY: (a) %d hits%s; (b) %d hits" %
          (len(a), (" (" + ", ".join("%s %d" % kv for kv in sorted(by_kind.items())) + ")") if a else "", len(b)))
    print("Each hit is what the hook would count, not a block: judge each one by hand.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
