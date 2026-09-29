#!/usr/bin/env python3
"""board_gate: the work-board Stop hook shipped by the turn-reduction plugin.

It does nothing unless the project has `.claude/board.json` (written by the work-board
skill's `init` or `adopt`). When the board exists it refuses to let a turn end in four
cases:

(a) The session changed state (a git commit, merge or push, a PR merge, a deploy, a
    mutating `aws` call, or a project trigger from board.json `triggers[]`) and there is
    no write to the board it is owed to after the last such command. A change is owed to
    the nearest `.claude/board.json` at or above the repo the command ran in (`git -C
    <dir>`, else the transcript entry's cwd), so a commit in another repo with its own
    board is logged there; a repo with no board of its own stays owed to the project's
    board. Satisfied by an ArtifactData write whose url names that board, or an assistant
    line `BOARD: no card affected: <reason>`.
(b) The turn's last assistant message asks Graham a should-I question in chat and the
    turn wrote no inbox card. Satisfied by an ArtifactData write to the board that puts a
    card in the `inbox` column or writes an `ask`, or an assistant line
    `INBOX: none needed: <reason>`. Intent questions ("What is this change for?") do not
    match the should-I patterns and pass. The last message is the Stop input's
    `last_assistant_message` when present, since the transcript file can lag it; the
    transcript's final text is the fallback. A trailing paragraph that is only a link
    (`Board: <url>`) is skipped, so the paragraph above it counts as the last.
    (b) also catches an offer to start work when Graham says so ("I'll start it when you
    say go", "which I can start when you want"), with or without a question mark. That
    breaks "continue by default", and an inbox card for some other question does not
    excuse it; only the INBOX marker does.
(c) The session wrote an inbox card to the board and holds no comment watch on the board
    that says `auto-replies armed`, so Graham's Tell Claude would wake a chat Claude, not
    this session. Proven by an ArtifactComments `watch` result: the listing row for the
    board, or a `watch` on it that says a comment reaches this session. A publish result
    alone does not count, and a later "Stopped watching" undoes it. Satisfied by that
    result, or an assistant line `WATCH: not armed: <reason>` anywhere in the session.
(d) An inbox `ask` written this turn has no `command` and its question carries a command
    (a script path or a known CLI, with a flag). Satisfied by rewriting it as a command
    card, or an assistant line `ASK: not a command card: <reason>` in the turn.

Kill switches (PROPOSAL V8): with no `.claude/board.json` every check is off. With no
`authorization.json` at the project root checks (b), (c) and (d) are off; (a) still runs.
Renaming either file to `.superseded` is how a project turns them off.

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
- The board a change is owed to comes from `git -C <dir>` (with `~` expanded) or the
  transcript entry's cwd. `cd <dir> && git commit` and `$HOME/...` paths are charged to
  the entry's cwd board, not `<dir>`'s; sessions here use `git -C`, so this is rare.
- The should-I check reads the first and last paragraph of the final message and matches
  a phrase list. An ask phrased another way ("Thoughts?") passes; a rhetorical
  "should I" in prose that ends in a question mark blocks. The offer check reads the last
  paragraph only and needs a first-person action verb and a gate on Graham in one
  sentence; "I'll leave it for you to run when you want" passes, "I can kick it off
  whenever" does not match either.
- The watch check trusts the text of the watch result: a listing row must read
  "connected, ... auto-replies armed". A row still "connecting", or one the tool words
  another way (after a resume, say), reads as not armed and blocks once; list again, or
  use the WATCH marker. If the tool rewords "auto-replies armed", every board session
  blocks at the first stop after an inbox card, which is loud, not silent.
- The command-in-prose check matches a script path or a known CLI followed by a flag; a
  command with no flag ("gh pr merge 12?") passes, and a policy question that names one
  ("Keep git log --oneline as the range display?") blocks until the ASK marker.
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
WATCH_MARKER = re.compile(r"(?m)^[ \t]*WATCH: not armed:[ \t]*(?!<)(\S.{7,})$")
ASK_MARKER = re.compile(r"(?m)^[ \t]*ASK: not a command card:[ \t]*(?!<)(\S.{7,})$")

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
# An offer to start work once Graham says so: a first-person action and a gate on him, in
# one sentence of the last paragraph (SCL 2026-09-28: "I'll start it when you say go",
# "which I can start when you want"). Continue by default says take the card instead.
OFFER_ACT = re.compile(
    r"(?i)\b(?:i['’]ll|i will|i can|i could|i['’]d|(?:i['’]m )?happy to|ready to)\s+(?:\w+\s+){0,2}?"
    r"(?:start|begin|pick|take|do|run|deploy|merge|push|continue|go|build|kick|move|work|get)\b")
OFFER_GATE = re.compile(
    r"(?i)\b(?:when(?:ever)? you(?:['’]re| are) ready|when(?:ever)? you (?:say (?:go|so|the word)|give the word|want|like|decide)|"
    r"if you(?:['’]d)? (?:want|like)|say the word|(?:on|with) your (?:go|word|say-so|ok|okay)|"
    r"once you (?:say|give|confirm|approve)|(?:awaiting|waiting (?:for|on)) your (?:go|word|say-so|ok|okay))\b")
# A paragraph that is only a link, optionally labelled ("Board: <url>"); skipped at the end.
LINK_ONLY = re.compile(r"^(?:[*_]*[\w ]{1,40}(?:[*_]*:|:[*_]*)\s*)?(?:<?https?://\S+>?|\[[^\]]*\]\(https?://[^)\s]+\))$")
# A command in an ask's question: a script path or a known CLI, then a flag.
CMD_IN_PROSE = re.compile(
    r"(?:[\w./-]+\.(?:py|sh|js|ts|rb)|\b(?:aws|gh|git|sam|terraform|kubectl|npx?|uv|python3?|bash|curl|cdk|docker|gcloud|az|psql)"
    r"\s+[\w.:/-]+)(?:\s+[^\s?]+){0,8}?\s--?[A-Za-z][\w-]*")
WATCH_TOOLS = {"ArtifactComments"}


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


def _hits(command, extra):
    """(trigger name, cleaned segment text, words) for each segment that changes state."""
    for text, toks in segments(command):
        for name, rx in TRIGGERS + extra:
            if rx.search(text):
                yield name, text, toks
                break
        else:
            if aws_writes(toks):
                yield "aws write", text, toks


def trigger_hits(command, extra):
    """(trigger name, cleaned segment text) for each segment of the command that changes
    state. tests/replay-board-gate.py prints the segment so a person can judge the hit."""
    return [(name, text) for name, text, _ in _hits(command, extra)]


def triggers_in(command, extra):
    return [name for name, _ in trigger_hits(command, extra)]


def git_c_dir(toks):
    """The directory a `git -C <dir> ...` segment runs in (repeated -C joined, as git
    does), else None."""
    if not toks or os.path.basename(toks[0]) != "git":
        return None
    path, k = None, 1
    while k < len(toks) and toks[k].startswith("-"):
        if toks[k] == "-C" and k + 1 < len(toks):
            path = os.path.join(path, toks[k + 1]) if path else toks[k + 1]
            k += 1
        elif toks[k] in ("-c", "--git-dir", "--work-tree", "--namespace") and k + 1 < len(toks):
            k += 1
        k += 1
    return path


def trigger_dirs(command, extra):
    """(trigger name, git -C directory or None) for each segment that changes state."""
    return [(name, git_c_dir(toks)) for name, _, toks in _hits(command, extra)]


def board_for(start, fallback):
    """The nearest .claude/board.json at or above start; fallback when there is none, so
    a state change in a repo without a board stays owed to the session project's board."""
    d = os.path.realpath(start)
    while True:
        p = os.path.join(d, ".claude", "board.json")
        if os.path.isfile(p):
            return p
        parent = os.path.dirname(d)
        if parent == d:
            return fallback
        d = parent


def board_id(url):
    m = re.search(r"/artifact/([A-Za-z0-9_-]+)", str(url or ""))
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


def paragraphs(text):
    """The message's paragraphs, with trailing link-only ones (`Board: <url>`) dropped
    unless nothing else is left."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text or "") if p.strip()]
    while len(paras) > 1 and LINK_ONLY.match(paras[-1]):
        paras.pop()
    return paras


def ask_sentence(text):
    """The should-I sentence in the first or last paragraph of the message, else ""."""
    paras = paragraphs(text)
    for para in dict.fromkeys(paras[:1] + paras[-1:]):
        m = LET_ME_KNOW.search(para)
        if m:
            start = max(para.rfind(".", 0, m.start()), para.rfind("\n", 0, m.start())) + 1
            return para[start:].strip()
        for sentence in re.findall(r"[^.?!\n]*\?", para):
            if ASK.search(sentence):
                return sentence.strip()
    return ""


def asks_should_i(text):
    """True when the first or last paragraph of the message holds a should-I ask."""
    return bool(ask_sentence(text))


def offer_sentence(text):
    """The sentence in the last paragraph that offers to start work once Graham says so,
    else ""."""
    paras = paragraphs(text)
    if not paras:
        return ""
    for sentence in re.split(r"(?<=[.!?])\s+|\n", paras[-1]):
        if OFFER_ACT.search(sentence) and OFFER_GATE.search(sentence):
            return sentence.strip()
    return ""


def asks_in(block):
    """Every `ask` object an ArtifactData write sets, from inline data, batch entries, or
    a data file that is still readable."""
    inp = block.get("input") or {}
    datas = [inp.get("data")] + [w.get("data") for w in inp.get("writes") or [] if isinstance(w, dict)]
    paths = [inp.get("file_path")] + [w.get("file_path") for w in inp.get("writes") or [] if isinstance(w, dict)]
    for p in paths:
        if p and os.path.isfile(p):
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    datas.append(json.loads(fh.read(1_000_000)))
            except (OSError, ValueError):
                pass
    return [d["ask"] for d in datas if isinstance(d, dict) and isinstance(d.get("ask"), dict)]


def prose_command(ask):
    """The question of an ask that carries a command in its prose and no `command`, else ""."""
    if str(ask.get("command") or "").strip():
        return ""
    q = str(ask.get("question") or "")
    return q if CMD_IN_PROSE.search(q) else ""


def result_text(block):
    c = block.get("content")
    if isinstance(c, list):
        return "\n".join(str(x.get("text") or "") for x in c if isinstance(x, dict))
    return str(c or "")


def watch_state(text, bid, armed):
    """This session's armed state for board bid after an ArtifactComments watch result."""
    url = r"https://claude\.ai/artifact/" + re.escape(bid) + r"\b"
    if re.search(r"Stopped watching " + url, text):
        return False
    if re.search(r"(?m)^\s*-\s*" + url + r"\s+(?:—|--|-)\s+connected,[^\n]*\bauto-replies armed\b", text):
        return True
    if re.search(r"^Watching " + url + r"[^\n]*reaches this session \(its status row says auto-replies armed\)", text):
        return True
    if re.search(r"\d+ artifact watch(?:es)? in this session|^No artifact watches in this session", text):
        return False  # a listing without an armed row for the board: not armed now
    return armed


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

    # Boards a state change can be owed to, by board id: the project's, plus the nearest
    # board above a command's repo (`git -C <dir>`, else the entry's cwd) when that repo
    # has its own .claude/board.json.
    boards = {bid: board}
    owed_cache = {}  # board.json path -> board id it resolves to

    def owed_to(start):
        found = board_for(start, board_path)
        if found not in owed_cache:
            owed_cache[found] = bid
            try:
                if os.path.getsize(found) <= 1 << 20:  # a board.json is small; skip anything odd
                    with open(found, encoding="utf-8") as fh:
                        other = json.load(fh)
                    obid = board_id(other.get("url"))
                    if obid:
                        boards.setdefault(obid, other)
                        owed_cache[found] = obid
            except (OSError, ValueError, AttributeError, TypeError):
                pass
        return owed_cache[found]

    pending = []          # (kind, command, board id) since that board's last write or a BOARD marker
    turn_inbox = False    # an inbox write or INBOX marker in the current turn
    turn_marker = False   # an INBOX marker in the current turn (the only excuse for an offer)
    session_inbox = False # an inbox card written to the project board this session
    armed = False         # the last watch result says the project board's auto-replies are armed
    watch_marker = False  # a WATCH marker this session
    watch_ids = set()     # tool_use ids of ArtifactComments watch calls
    prose_asks = []       # questions written this turn with a command in the prose
    ask_marker = False    # an ASK marker in the current turn
    last_text = ""        # the final assistant message's text
    prev_text = False     # the previous assistant entry was text only
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            if is_prompt(entry):
                turn_inbox = turn_marker = ask_marker = False
                prose_asks = []
                last_text = ""
                prev_text = False
                continue
            if entry.get("type") == "user" and not entry.get("isSidechain") and watch_ids:
                content = (entry.get("message") or {}).get("content")
                for block in content if isinstance(content, list) else []:
                    if isinstance(block, dict) and block.get("type") == "tool_result" and \
                            block.get("tool_use_id") in watch_ids:
                        armed = watch_state(result_text(block), bid, armed)
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
                        turn_inbox = turn_marker = True
                    if WATCH_MARKER.search(t):
                        watch_marker = True
                    if ASK_MARKER.search(t):
                        ask_marker = True
                elif block.get("type") == "tool_use":
                    inp = block.get("input") or {}
                    tool = block.get("name") or ""
                    if (tool in WATCH_TOOLS or tool.endswith("__ArtifactComments")) and inp.get("action") == "watch":
                        watch_ids.add(block.get("id"))
                    elif (tool == "ArtifactData" or tool.endswith("__ArtifactData")) and \
                            inp.get("action") in WRITE_ACTIONS:
                        url = str(inp.get("url") or "")
                        pending = [p for p in pending if not (p[2] and p[2] in url)]
                        if is_board_write(block, bid) and is_inbox_write(block):
                            turn_inbox = session_inbox = True
                        if is_board_write(block, bid):
                            prose_asks += [q for q in map(prose_command, asks_in(block)) if q]
                    elif tool in SHELL_TOOLS:
                        cmd = str(inp.get("command") or "")
                        base = entry.get("cwd") or project_dir
                        for kind, cdir in trigger_dirs(cmd, extra):
                            start = os.path.join(base, os.path.expanduser(cdir)) if cdir else base
                            pending.append((kind, cmd, owed_to(start)))
            used_tool = any(isinstance(b, dict) and b.get("type") == "tool_use"
                            for b in (entry.get("message") or {}).get("content") or [])
            if used_tool:
                last_text = ""  # a tool call after the text: that text did not end the turn
                prev_text = False
            elif texts:
                joined = "\n\n".join(texts)
                last_text = (last_text + "\n\n" + joined) if prev_text else joined
                prev_text = True

    # The final message can reach the Stop input before it reaches the transcript file (c11,
    # 2026-09-28: the hook read the transcript 12 ms after the message and missed it), so the
    # input's copy is the final text, and its markers count.
    final = data.get("last_assistant_message")
    if isinstance(final, str) and final.strip():
        last_text = final
        if BOARD_MARKER.search(final):
            pending = []
        if INBOX_MARKER.search(final):
            turn_inbox = turn_marker = True
        if WATCH_MARKER.search(final):
            watch_marker = True
        if ASK_MARKER.search(final):
            ask_marker = True

    url = board.get("url") or "(board.json has no url)"
    lines = []
    if pending:
        lines.append("board-gate (a): this session changed state since its last work-board write:")
        for owed in dict.fromkeys(p[2] for p in pending):
            mine = [p for p in pending if p[2] == owed]
            ob = boards.get(owed) or board
            for kind, cmd, _ in mine[:8]:
                lines.append("  - %s: %s" % (kind, " ".join(cmd.split())[:160]))
            if len(mine) > 8:
                lines.append("  - ... and %d more" % (len(mine) - 8))
            lines.append("Update the affected card(s) with ArtifactData (url %s, collection %s; a "
                         "move to done needs evidence and a green review)."
                         % (ob.get("url") or "(board.json has no url)", ob.get("collection") or "cards"))
        lines.append("If no card is affected, write the line `BOARD: no card affected: <reason>` "
                     "with a real reason.")
    if not ask_check:
        return lines
    offer = offer_sentence(last_text)
    if not turn_inbox and asks_should_i(last_text):
        lines.append("board-gate (b): this turn ends by asking a should-I question in chat. In a "
                     "project with a board, asks go to the inbox: write a card to column `inbox` "
                     "with an `ask` {question, default, why, evidence_link, ask_rev} via ArtifactData "
                     "(url %s), keep working, and close with the inbox count. If no ask is really "
                     "needed (check authorization.json first), write the line "
                     "`INBOX: none needed: <reason>`. Intent questions are exempt." % url)
    elif offer and not turn_marker:
        lines.append("board-gate (b): this turn ends by offering to start work when Graham says "
                     "so: \"%s\". Continue by default: take the next Ready card now, in lane then "
                     "due-date order, skipping blocked_by cards and the run's \"Not this time\" "
                     "list. A push ceiling stops pushes, not work that needs none. If everything "
                     "left really waits on Graham, it is already an inbox card; say so in the line "
                     "`INBOX: none needed: <reason>`." % " ".join(offer.split())[:200])
    if session_inbox and not armed and not watch_marker:
        lines.append("board-gate (c): this session filed an inbox card, but no ArtifactComments "
                     "watch result shows the board (%s) with auto-replies armed, so Graham's Tell "
                     "Claude would wake a chat Claude, not this session. Run ArtifactComments "
                     "`watch` with no URL; if the board's row does not say auto-replies armed, "
                     "republish %s to that URL with the Artifact tool (no re-render) and list "
                     "again. If replies cannot be armed here (stopped by Graham, or a subagent), "
                     "write the line `WATCH: not armed: <reason>`."
                     % (url, board.get("page") or ".claude/work-board.html"))
    if prose_asks and not ask_marker:
        lines.append("board-gate (d): an inbox ask written this turn puts a command in the "
                     "question's prose and has no `ask.command`: \"%s\". A Graham-tier action is a "
                     "command card: the exact command in `ask.command`, what it prints in "
                     "`ask.expect`, ask_rev + 1, and the session never runs it (work-board "
                     "SKILL.md, \"An Accept does not reach the auto-mode classifier\"). If the "
                     "question names a command but asks for no action, write the line "
                     "`ASK: not a command card: <reason>`." % " ".join(prose_asks[0].split())[:200])
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
