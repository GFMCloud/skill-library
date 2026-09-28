#!/usr/bin/env python3
"""board_gate: the work-board Stop hook shipped by the turn-reduction plugin.

It does nothing unless the project has `.claude/board.json` (written by the work-board
skill's `init` or `adopt`). When the board exists it refuses to let a turn end in two
cases:

(a) The session changed state (a git commit, merge or push, a PR merge, a deploy, a
    mutating `aws` call, or a project trigger from board.json `triggers[]`) and there is
    no write to the board after the last such command. Satisfied by an ArtifactData write
    whose url names the board, or an assistant line `BOARD: no card affected: <reason>`.
(b) The turn's last assistant message asks Graham a should-I question in chat and the
    turn wrote no inbox card. Satisfied by an ArtifactData write to the board that puts a
    card in the `inbox` column or writes an `ask`, or an assistant line
    `INBOX: none needed: <reason>`. Intent questions ("What is this change for?") do not
    match the should-I patterns and pass.

Kill switches (PROPOSAL V8): with no `.claude/board.json` both checks are off. With no
`authorization.json` at the project root check (b) is off; (a) still runs. Renaming either
file to `.superseded` is how a project turns them off.

Generalized from SCL `scripts/hooks/board-gate.py`: the SCL-only scripts moved out of the
built-in trigger list and into that project's board.json `triggers[]`.

Exit 2 with the reason on stderr blocks the stop, once: `stop_hook_active` lets the next
stop through. Exit 0 when nothing is owed. Any error fails open (exit 0).

Known weaknesses, stated beside the rule:
- The trigger list is a pattern list, matched at the command position of each shell
  segment. A state change behind an alias, a Makefile target, a shell function or a
  script not named in triggers[] is not seen, nor one inside `$(...)` or backticks within
  double quotes. Project triggers[] regexes are matched against the segment from its
  command position, so they need no anchor, but a loose one can still match an argument.
- The should-I check reads the first and last paragraph of the final message and matches
  a phrase list. An ask phrased another way ("Thoughts?") passes; a rhetorical
  "should I" in prose that ends in a question mark blocks.
- A board write is recognized from the tool input. An ArtifactData write that loads its
  rows from a file (`file_path`) counts as an inbox write only if that file is still
  readable and holds an inbox card.

Proven by plugins/turn-reduction/tests/prove-board-gate.sh against
plugins/turn-reduction/tests/fixtures/board-gate/cases.json.
"""
import json
import os
import re
import sys

WRITE_ACTIONS = {"set", "update", "batch", "delete", "str_replace"}
SHELL_TOOLS = {"Bash", "mcp__terminal__run_in_terminal"}

# A marker must open its own line and carry a real reason (8+ characters, not a <...>
# placeholder), so prose that quotes the marker format never counts.
BOARD_MARKER = re.compile(r"(?m)^[ \t]*BOARD: no card affected:[ \t]*(?!<)(\S.{7,})$")
INBOX_MARKER = re.compile(r"(?m)^[ \t]*INBOX: none needed:[ \t]*(?!<)(\S.{7,})$")

# Command text that changes state. Each regex is matched against one shell segment
# rewritten from its command position (after VAR=val, sudo, time, env, nohup, command,
# exec, xargs and its options, and an interpreter such as bash or sh; the string after
# `bash -c` or `sh -lc` and the words after `eval` are read as commands of their own),
# with quoted words that contain spaces replaced by Q and heredoc bodies removed.
# Backtick substitution outside quotes opens a segment of its own. So `grep "sam deploy"
# f`, `cat deploy.sh` and a heredoc line mentioning `git push` are not state changes. Project-specific scripts
# belong in board.json triggers[], not here.
TRIGGERS = [
    ("git commit", re.compile(r"^git\b(\s+-\S+(\s+\S+)?)*\s+commit\b(?!.*--dry-run)")),
    ("git merge", re.compile(r"^git\b(\s+-\S+(\s+\S+)?)*\s+merge\b(?!-)")),  # not merge-base, merge-tree
    ("git push", re.compile(r"^git\b(\s+-\S+(\s+\S+)?)*\s+push\b(?!.*--dry-run)")),
    ("gh pr merge", re.compile(r"^gh\s+pr\s+merge\b")),
    ("gh repo create", re.compile(r"^gh\s+repo\s+create\b")),
    ("deploy script", re.compile(r"^(\S*/)?deploy\.sh\b")),
    ("sam deploy", re.compile(r"^sam\s+deploy\b")),
    ("terraform apply", re.compile(r"^terraform\b.*\s(apply|destroy)\b")),
    ("cdk deploy", re.compile(r"^(npx\s+)?cdk\s+(deploy|destroy)\b")),
]
PREFIXES = {"sudo", "time", "env", "nohup", "command", "exec", "xargs"}
# xargs options that take the next word as their value (BSD and GNU spellings).
XARGS_VALUE_FLAGS = {"-I", "-J", "-L", "-n", "-P", "-s", "-E", "-e", "-d", "-a", "-R", "-S"}
INTERPRETERS = {"bash", "sh", "zsh", "source", "."}
ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
# First word of an aws operation that writes.
MUTATING = {"put", "create", "delete", "update", "execute", "start", "stop", "invoke", "copy",
            "tag", "untag", "attach", "detach", "enable", "disable", "modify", "set", "remove",
            "add", "register", "deregister", "rotate", "restore", "publish", "send", "cancel",
            "terminate", "reboot", "import", "associate", "disassociate", "request", "reset",
            "upload", "deploy", "change", "revoke", "authorize", "replace", "release"}

# A should-I ask: a permission question put to the user. Matched per sentence that ends
# in "?", plus the "let me know if you want me to" form, which has no question mark.
ASK = re.compile(
    r"(?i)\b(should i|shall i|should we|shall we|do you want me to|want me to|"
    r"would you like me to|would you like (?:to|us to)|ok(?:ay)? (?:to|if i)|"
    r"can i go ahead|may i|good to (?:go|proceed|push|merge|commit|deploy)|"
    r"proceed with|ready (?:for me )?to (?:push|merge|deploy|commit))\b")
LET_ME_KNOW = re.compile(r"(?i)\b(let me know|tell me) (if|whether) (you('d)? (want|like) me to|i should|to)\b")


def strip_heredocs(command):
    """Drop heredoc bodies, keeping the line that opens each and its closing delimiter."""
    out, delim = [], None
    for line in command.split("\n"):
        if delim is not None:
            if line.strip() == delim:
                out.append(line)
                delim = None
            continue
        out.append(line)
        m = HEREDOC.search(line)
        if m:
            delim = m.group(2)
    return "\n".join(out)


def lex(command):
    """Split a command into segments of (word, quoted) pairs. Separators outside quotes:
    ; & | && || newline ( ) and backtick. Quotes are removed from the word; `quoted`
    records that any part of the word was quoted."""
    segs, words, cur, quoted, have, q = [], [], [], False, False, None
    i, n = 0, len(command)

    def end_word():
        nonlocal cur, quoted, have
        if have:
            words.append(("".join(cur), quoted))
        cur, quoted, have = [], False, False

    def end_seg():
        nonlocal words
        end_word()
        if words:
            segs.append(words)
        words = []

    while i < n:
        c = command[i]
        if q:
            if c == q:
                q = None
            elif c == "\\" and q == '"' and i + 1 < n:
                i += 1
                cur.append(command[i])
            else:
                cur.append(c)
            i += 1
            continue
        if c in "'\"":
            q, quoted, have = c, True, True
        elif c == "\\" and i + 1 < n:
            i += 1
            if command[i] != "\n":
                cur.append(command[i])
                have = True
        elif c in " \t":
            end_word()
        elif c in ";&|\n()`":
            end_seg()
        else:
            cur.append(c)
            have = True
        i += 1
    end_seg()
    return segs


def command_words(words):
    """Words from the command position on, plus the command string of any `bash -c`
    (also combined flags such as `sh -lc`) or `eval`."""
    k = 0
    while k < len(words):
        w = words[k][0]
        if ASSIGN.match(w) and not words[k][1]:
            k += 1
        elif w in PREFIXES:
            k += 1
            while k < len(words) and words[k][0].startswith("-"):
                if w == "xargs" and words[k][0] in XARGS_VALUE_FLAGS:
                    k += 1
                k += 1
        else:
            break
    rest = words[k:]
    if rest and rest[0][0] == "eval":
        return [], " ".join(w for w, _ in rest[1:])
    if rest and os.path.basename(rest[0][0]) in INTERPRETERS:
        j = 1
        while j < len(rest) and rest[j][0].startswith("-"):
            flag = rest[j][0]
            if not flag.startswith("--") and "c" in flag[1:] and j + 1 < len(rest):
                return [], rest[j + 1][0]
            j += 1
        rest = rest[j:]
    return rest, None


def segments(command):
    """Yield (cleaned command text, words) per shell segment, recursing into bash -c."""
    for words in lex(strip_heredocs(command)):
        rest, inner = command_words(words)
        if inner is not None:
            for item in segments(inner):
                yield item
            continue
        if not rest:
            continue
        text = " ".join("Q" if quoted and re.search(r"\s", w) else w for w, quoted in rest)
        yield text, [w for w, _ in rest]


def aws_writes(toks):
    """True when the segment's command words are an aws CLI call that writes."""
    if not toks or os.path.basename(toks[0]) != "aws":
        return False
    words = []
    skip = False
    for t in toks[1:]:
        if skip:
            skip = False
            continue
        if t.startswith("--"):
            skip = "=" not in t and t not in ("--no-cli-pager", "--debug", "--no-paginate")
            continue
        words.append(t)
    if len(words) < 2 or "--generate-cli-skeleton" in toks:
        return False
    service, op = words[0], words[1]
    if service == "s3":
        if op in ("rm", "mb", "rb"):
            return True
        if op in ("cp", "mv", "sync"):
            paths = [w for w in words[2:] if w.startswith("s3://") or w.startswith(("/", ".", "~")) or ("/" in w and "://" not in w)]
            return bool(paths) and paths[-1].startswith("s3://")
        return False
    if service in ("sso", "sts", "configure"):
        return False
    return op.split("-")[0] in MUTATING


def project_triggers(board):
    out = []
    for i, t in enumerate(board.get("triggers") or []):
        if isinstance(t, str):
            name, rx = "project trigger %d" % i, t
        elif isinstance(t, dict):
            name, rx = t.get("name") or "project trigger %d" % i, t.get("regex") or ""
        else:
            continue
        try:
            out.append((name, re.compile(rx)))
        except re.error:
            continue
    return out


def trigger_hits(command, extra):
    """(trigger name, cleaned segment text) for each segment of the command that changes
    state. tests/replay-board-gate.py prints the segment so a person can judge the hit."""
    found = []
    for text, toks in segments(command):
        for name, rx in TRIGGERS + extra:
            if rx.search(text):
                found.append((name, text))
                break
        else:
            if aws_writes(toks):
                found.append(("aws write", text))
    return found


def triggers_in(command, extra):
    return [name for name, _ in trigger_hits(command, extra)]


def board_id(url):
    m = re.search(r"/artifact/([A-Za-z0-9_-]+)", url or "")
    return m.group(1) if m else ""


def is_board_write(block, bid):
    name = block.get("name") or ""
    inp = block.get("input") or {}
    return (name == "ArtifactData" or name.endswith("__ArtifactData")) and \
        inp.get("action") in WRITE_ACTIONS and bool(bid) and bid in str(inp.get("url") or "")


INBOX_WRITE = re.compile(r'"column"\s*:\s*"inbox"|"ask"\s*:\s*\{')


def is_inbox_write(block):
    inp = block.get("input") or {}
    text = json.dumps(inp)
    paths = [inp.get("file_path")] + [w.get("file_path") for w in inp.get("writes") or [] if isinstance(w, dict)]
    for p in paths:
        if p and os.path.isfile(p):
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    text += fh.read(1_000_000)
            except OSError:
                pass
    return bool(INBOX_WRITE.search(text))


def is_prompt(entry):
    """A user entry that starts a turn: typed text, not a tool result."""
    if entry.get("type") != "user" or entry.get("isSidechain") or entry.get("isMeta"):
        return False
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    if isinstance(content, list):
        return any(isinstance(b, dict) and b.get("type") == "text" for b in content) and \
            not any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content)
    return False


def asks_should_i(text):
    """True when the first or last paragraph of the message holds a should-I ask."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text or "") if p.strip()]
    if not paras:
        return False
    for para in {paras[0], paras[-1]}:
        if LET_ME_KNOW.search(para):
            return True
        for sentence in re.findall(r"[^.?!\n]*\?", para):
            if ASK.search(sentence):
                return True
    return False


def evaluate(data, project_dir):
    """Return a list of stderr lines; empty means the stop is allowed."""
    if data.get("stop_hook_active"):
        return []
    board_path = os.path.join(project_dir, ".claude", "board.json")
    if not os.path.isfile(board_path):
        return []
    with open(board_path, encoding="utf-8") as fh:
        board = json.load(fh)
    bid = board_id(board.get("url"))
    ask_check = os.path.isfile(os.path.join(project_dir, "authorization.json"))
    extra = project_triggers(board)
    path = data.get("transcript_path") or ""
    if not path or not os.path.exists(path):
        return []

    pending = []          # state changes since the last board write or BOARD marker
    turn_inbox = False    # an inbox write or INBOX marker in the current turn
    last_text = ""        # the final assistant message's text
    prev_text = False     # the previous assistant entry was text only
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            if is_prompt(entry):
                turn_inbox = False
                last_text = ""
                prev_text = False
                continue
            if entry.get("type") != "assistant" or entry.get("isSidechain"):
                continue
            texts = []
            for block in (entry.get("message") or {}).get("content") or []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text":
                    t = block.get("text") or ""
                    texts.append(t)
                    if BOARD_MARKER.search(t):
                        pending = []
                    if INBOX_MARKER.search(t):
                        turn_inbox = True
                elif block.get("type") == "tool_use":
                    inp = block.get("input") or {}
                    if is_board_write(block, bid):
                        pending = []
                        if is_inbox_write(block):
                            turn_inbox = True
                    elif (block.get("name") or "") in SHELL_TOOLS:
                        cmd = str(inp.get("command") or "")
                        for kind in triggers_in(cmd, extra):
                            pending.append((kind, cmd))
            used_tool = any(isinstance(b, dict) and b.get("type") == "tool_use"
                            for b in (entry.get("message") or {}).get("content") or [])
            if used_tool:
                last_text = ""  # a tool call after the text: that text did not end the turn
                prev_text = False
            elif texts:
                joined = "\n\n".join(texts)
                last_text = (last_text + "\n\n" + joined) if prev_text else joined
                prev_text = True

    url = board.get("url") or "(board.json has no url)"
    coll = board.get("collection") or "cards"
    lines = []
    if pending:
        lines.append("board-gate (a): this session changed state since its last work-board write:")
        for kind, cmd in pending[:8]:
            lines.append("  - %s: %s" % (kind, " ".join(cmd.split())[:160]))
        if len(pending) > 8:
            lines.append("  - ... and %d more" % (len(pending) - 8))
        lines.append("Update the affected card(s) with ArtifactData (url %s, collection %s; a move "
                     "to done needs evidence and a green review), or, if no card is affected, write "
                     "the line `BOARD: no card affected: <reason>` with a real reason." % (url, coll))
    if ask_check and not turn_inbox and asks_should_i(last_text):
        lines.append("board-gate (b): this turn ends by asking a should-I question in chat. In a "
                     "project with a board, asks go to the inbox: write a card to column `inbox` "
                     "with an `ask` {question, default, why, evidence_link, ask_rev} via ArtifactData "
                     "(url %s), keep working, and close with the inbox count. If no ask is really "
                     "needed (check authorization.json first), write the line "
                     "`INBOX: none needed: <reason>`. Intent questions are exempt." % url)
    return lines


def main():
    try:
        data = json.load(sys.stdin)
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
        lines = evaluate(data, project_dir)
        if not lines:
            return 0
        print("\n".join(lines), file=sys.stderr)
        return 2
    except Exception:
        return 0  # fail open


if __name__ == "__main__":
    sys.exit(main())
