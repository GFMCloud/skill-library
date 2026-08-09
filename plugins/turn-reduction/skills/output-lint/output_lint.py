#!/usr/bin/env python3
"""output-lint — check a message or document carrying commands or asks, before it is sent.

Every correction in the audited corpus was a human fixing the agent's *process*, not its
facts. Six of those process defects are mechanically checkable. This checks those six and
names the two that are not, rather than pretending they were checked.

Exit codes:
  0  no errors (warnings may be present; --strict promotes them)
  1  at least one error
  2  the input could not be read

Stdlib only. Runs on Python 3.9+.
"""

import argparse
import re
import sys

FENCE_OPEN = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([A-Za-z0-9_+.-]*)\s*$")
SHELL_LANGS = {"bash", "sh", "zsh", "shell", "shellsession", "console", "ksh"}
PYTHON_LANGS = {"python", "python3", "py"}

# `<br>` in prose is markup, not an unfilled slot.
HTML_TAGS = {
    "br", "b", "i", "u", "em", "strong", "code", "pre", "p", "a", "img", "hr", "div",
    "span", "ul", "ol", "li", "sub", "sup", "kbd", "table", "tr", "td", "th", "details",
    "summary", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6",
}

ANGLE_SLOT = re.compile(r"<([A-Za-z][A-Za-z0-9_ .-]{0,38})>")
CURLY_SLOT = re.compile(r"\{\{[^}]{0,60}\}\}")
YOUR_SLOT = re.compile(r"\bYOUR_[A-Z0-9_]+")
PLACEHOLDER_WORD = re.compile(r"(?i)\bplaceholder\b")

PY_IN_SHELL = [
    re.compile(r"^\s*(?:import|from)\s+[A-Za-z_][\w.]*"),
    re.compile(r"^\s*def\s+[A-Za-z_]\w*\s*\("),
    re.compile(r"^\s*class\s+[A-Za-z_]\w*\s*[(:]"),
    re.compile(r"^\s*print\s*\("),
    re.compile(r"^\s*(?:if|for|while|with|try|else|elif)\b.*:\s*$"),
]
SH_IN_PYTHON = re.compile(
    r"^\s*(?:git|npm|yarn|pnpm|brew|apt|apt-get|cd|ls|mkdir|rm|cp|mv|curl|wget|sudo|chmod|"
    r"docker|kubectl|make|pytest|pip3?|python3?)\s+\S"
)

# Commands whose meaning depends on where they are run from.
CWD_DEPENDENT = re.compile(
    r"^\s*(?:\./|"
    r"(?:npm|yarn|pnpm|make|pytest|tox|cargo|go|bundle|rake|mvn|gradle|terraform|"
    r"docker[- ]compose|poetry|uv|just)\s+\S|"
    r"git\s+(?!-C\b|--git-dir\b|clone\b|config\s+--global\b)\S)"
)
CD_LINE = re.compile(r"^\s*(?:cd|pushd)\s+\S")
DIR_IN_PROSE = re.compile(
    r"(?i)\b(?:from|in|inside|at|under)\b[^.]{0,60}?"
    r"(?:repo(?:sitory)?\s*root|project\s*root|working\s*director|directory|folder|cwd)"
)
PATHISH_CODE = re.compile(r"`[^`]*[~/][^`]*`")

BRACE_EXPANSION = re.compile(r"\{[^{}\s]*,[^{}\s]*\}")
GLOBSTAR = re.compile(r"(?<![\"'\w])\*\*")
GLOBSTAR_ENABLED = re.compile(r"shopt\s+-s\s+globstar")

ANNOUNCE_FUTURE = re.compile(
    r"(?i)\b(?:i['’]ll|i\s+will|i['’]m\s+going\s+to|i\s+am\s+going\s+to|i['’]m\s+about\s+to|"
    r"let\s+me|next\s+i['’]ll|now\s+i['’]ll)\b[^.\n]{0,70}?"
    r"\b(write|writing|create|creating|commit|committing|push|pushing|update|updating|"
    r"delete|deleting|remove|removing|install|installing|deploy|deploying|add|adding|"
    r"edit|editing|modify|modifying|overwrite|rename|renaming)\b"
)
ANNOUNCE_PRESENT = re.compile(
    r"(?i)^\s*(?:now\s+)?(writing|creating|committing|pushing|installing|deploying|"
    r"updating|deleting|removing|overwriting)\b"
)

COUNTABLE = re.compile(
    r"\b(\d{1,7})\s+(?:\w+\s+){0,2}?"
    r"(turns?|files?|rows?|items?|sessions?|errors?|tests?|commits?|checks?|plugins?|"
    r"instances?|records?|lines?|entries|occurrences|matches|skills?|agents?|components?|"
    r"defects?|findings?|violations?|places?)\b"
)
ENUMERATION_MARK = re.compile(
    r"(?i)(?:wc\s+-l|grep\s+-c|--count|rev-list\s+--count|\|\s*wc\b|ls\s+-1|find\s|"
    r"\benumerat\w+|\bcounted\b|\btallied\b|\blisted\s+below\b|\bas\s+listed\b|"
    r"\beach\s+named\s+below\b|\bnamed\s+below\b|\bper\s+the\s+table\b)"
)

WEAK_HALF = [
    ("Lead with the ask.",
     "If the reader has to act, the action is the first line — not the conclusion of the "
     "analysis. Nothing here checks this."),
    ("One decision per message where possible.",
     "Three consecutive turns in one audited session were a single decision: an over-broad "
     "ask, then \"which question is real?\", then approval of what should have been decided. "
     "Nothing here checks this."),
]


class Finding(object):
    def __init__(self, line, severity, rule, message):
        self.line = line
        self.severity = severity
        self.rule = rule
        self.message = message


class Block(object):
    def __init__(self, lang, start, lines):
        self.lang = lang
        self.start = start          # 1-based line number of the opening fence
        self.lines = lines          # list of (lineno, text)

    @property
    def is_shell(self):
        return self.lang.lower() in SHELL_LANGS

    @property
    def is_python(self):
        return self.lang.lower() in PYTHON_LANGS

    @property
    def is_untagged(self):
        return self.lang == ""


def split_source(text):
    """Return (blocks, prose) where prose is a list of (lineno, text) outside fences."""
    blocks = []
    prose = []
    fence = None
    buf = []
    for i, raw in enumerate(text.splitlines(), start=1):
        if fence is None:
            match = FENCE_OPEN.match(raw)
            if match:
                fence = {"marker": match.group(2)[0] * 3, "lang": match.group(3), "start": i}
                buf = []
                continue
            prose.append((i, raw))
        else:
            stripped = raw.strip()
            if stripped.startswith(fence["marker"]) and set(stripped) <= set(fence["marker"][0]):
                blocks.append(Block(fence["lang"], fence["start"], buf))
                fence = None
                continue
            buf.append((i, raw))
    if fence is not None:
        blocks.append(Block(fence["lang"], fence["start"], buf))
    return blocks, prose


def strip_comment(line):
    return re.sub(r"(?<!\S)#.*$", "", line)


def is_quoted(text, index):
    """Rough but adequate: is position `index` inside a quoted run on this line?"""
    single = text.count("'", 0, index) % 2 == 1
    double = text.count('"', 0, index) % 2 == 1
    return single or double


# --------------------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------------------

def check_placeholders(blocks, prose, findings):
    """A shipped YOUR_LEAGUE_ID produced a 400 that tested nothing."""
    def scan(lineno, text, severity, where):
        for match in YOUR_SLOT.finditer(text):
            findings.append(Finding(lineno, severity, "placeholder",
                                    "unsubstituted %s in %s" % (match.group(0), where)))
        for match in CURLY_SLOT.finditer(text):
            findings.append(Finding(lineno, severity, "placeholder",
                                    "unsubstituted %s in %s" % (match.group(0), where)))
        if PLACEHOLDER_WORD.search(text):
            findings.append(Finding(lineno, severity, "placeholder",
                                    "the word PLACEHOLDER survived into %s" % where))
        for match in ANGLE_SLOT.finditer(text):
            inner = match.group(1)
            if inner.lower() in HTML_TAGS or inner.lower().rstrip("/") in HTML_TAGS:
                continue
            findings.append(Finding(lineno, severity, "placeholder",
                                    "unsubstituted <%s> in %s" % (inner, where)))

    for block in blocks:
        for lineno, text in block.lines:
            scan(lineno, text, "ERROR", "a command block")

    for lineno, text in prose:
        for span in re.finditer(r"`([^`]+)`", text):
            scan(lineno, span.group(1), "ERROR", "an inline command")
        # In prose a slot is a strong signal but not a shipped command, so it warns.
        without_code = re.sub(r"`[^`]*`", "", text)
        scan(lineno, without_code, "WARN", "prose")


def check_interpreter(blocks, findings):
    """Python was once presented as a shell command."""
    for block in blocks:
        body = [(n, strip_comment(t)) for n, t in block.lines]
        if block.is_shell:
            for lineno, text in body:
                if not text.strip():
                    continue
                for pattern in PY_IN_SHELL:
                    if pattern.match(text):
                        findings.append(Finding(
                            lineno, "ERROR", "interpreter",
                            "block is tagged %r but this line is Python — it will not run as "
                            "written" % block.lang))
                        break
        elif block.is_python:
            for lineno, text in body:
                if SH_IN_PYTHON.match(text):
                    findings.append(Finding(
                        lineno, "WARN", "interpreter",
                        "block is tagged %r but this line is a shell command" % block.lang))
        elif block.is_untagged and any(
                CWD_DEPENDENT.match(strip_comment(t)) for _, t in block.lines):
            findings.append(Finding(
                block.start, "WARN", "interpreter",
                "command block states no interpreter — tag the fence bash, sh, or python"))


def check_working_directory(blocks, prose, findings):
    prose_by_line = dict(prose)
    for block in blocks:
        if not (block.is_shell or block.is_untagged):
            continue
        offenders = [(n, t) for n, t in block.lines if CWD_DEPENDENT.match(strip_comment(t))]
        if not offenders:
            continue
        if any(CD_LINE.match(strip_comment(t)) for _, t in block.lines):
            continue
        # A directory named in the two non-blank prose lines above the fence also states it.
        stated = False
        checked = 0
        for lineno in range(block.start - 1, 0, -1):
            text = prose_by_line.get(lineno)
            if text is None:
                break
            if not text.strip():
                continue
            if DIR_IN_PROSE.search(text) or PATHISH_CODE.search(text):
                stated = True
                break
            checked += 1
            if checked >= 2:
                break
        if not stated:
            lineno, text = offenders[0]
            findings.append(Finding(
                lineno, "ERROR", "cwd",
                "`%s` depends on the working directory and none is stated — add a `cd` line "
                "or name the directory just above the block" % text.strip()))


def check_globs(blocks, findings):
    for block in blocks:
        if not block.is_shell:
            continue
        enabled = any(GLOBSTAR_ENABLED.search(t) for _, t in block.lines)
        posix_sh = block.lang.lower() in ("sh", "ksh")
        for lineno, raw in block.lines:
            text = strip_comment(raw)
            if not enabled:
                for match in GLOBSTAR.finditer(text):
                    if is_quoted(text, match.start()):
                        continue      # quoted: the tool expands it, not the shell
                    findings.append(Finding(
                        lineno, "ERROR", "glob",
                        "unquoted ** is not recursive without `shopt -s globstar` — it "
                        "expands as a single *"))
                    break
            if posix_sh:
                for match in BRACE_EXPANSION.finditer(text):
                    if is_quoted(text, match.start()):
                        continue
                    findings.append(Finding(
                        lineno, "ERROR", "glob",
                        "brace expansion %s is not POSIX sh — this block is tagged %r"
                        % (match.group(0), block.lang)))
                    break


def check_announced_writes(prose, findings):
    """Proof-of-work was violated one message after being written down."""
    for lineno, text in prose:
        if ANNOUNCE_FUTURE.search(text) or ANNOUNCE_PRESENT.search(text):
            findings.append(Finding(
                lineno, "ERROR", "announced-write",
                "a write is announced before it is made — make it, then report it with its "
                "result"))


def check_counts(prose, findings):
    """Recall said 128; enumeration said 148."""
    window = {lineno: text for lineno, text in prose}
    for lineno, text in prose:
        if text.lstrip().startswith("|"):
            continue          # a table is its own enumeration
        for match in COUNTABLE.finditer(text):
            number = int(match.group(1))
            if number <= 1:
                continue
            context = " ".join(
                window.get(n, "") for n in range(lineno - 2, lineno + 3)
            )
            if ENUMERATION_MARK.search(context):
                continue
            findings.append(Finding(
                lineno, "ERROR", "uncited-count",
                "\"%s\" is a bare count — attach the enumeration that produced it (the "
                "command, or the list itself)" % match.group(0)))


# --------------------------------------------------------------------------------------

def lint(text):
    blocks, prose = split_source(text)
    findings = []
    check_placeholders(blocks, prose, findings)
    check_interpreter(blocks, findings)
    check_working_directory(blocks, prose, findings)
    check_globs(blocks, findings)
    check_announced_writes(prose, findings)
    check_counts(prose, findings)
    findings.sort(key=lambda f: (f.line, f.rule))
    return findings, blocks


def report(path, findings, blocks, stream, strict):
    errors = [f for f in findings if f.severity == "ERROR"]
    warns = [f for f in findings if f.severity == "WARN"]

    for finding in findings:
        stream.write("%s:%d: %s [%s] %s\n"
                     % (path, finding.line, finding.severity, finding.rule, finding.message))
    if findings:
        stream.write("\n")

    stream.write("SCOPE OF THIS RESULT\n")
    stream.write("-" * 78 + "\n")
    stream.write("  Checked: %d fenced block(s) and the prose around them, in this input only.\n"
                 % len(blocks))
    stream.write("  Six mechanical rules ran: placeholder, interpreter, cwd, glob,\n")
    stream.write("  announced-write, uncited-count. A clean result means those six found\n")
    stream.write("  nothing here. It is not a statement about the message being good, and it\n")
    stream.write("  does not carry to any other message.\n\n")

    stream.write("NOT CHECKED — read these yourself before sending\n")
    stream.write("-" * 78 + "\n")
    for title, detail in WEAK_HALF:
        stream.write("  - %s\n    %s\n" % (title, detail))
    stream.write("\n")

    if errors:
        stream.write("FAIL — %d error(s), %d warning(s)\n" % (len(errors), len(warns)))
        return 1
    if warns and strict:
        stream.write("FAIL (--strict) — 0 errors, %d warning(s)\n" % len(warns))
        return 1
    stream.write("PASS — 0 errors, %d warning(s)\n" % len(warns))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="output_lint.py",
        description="Check a message or document carrying commands or asks, before it is sent.",
    )
    parser.add_argument("path", nargs="?", default="-",
                        help="file to check, or - for stdin (default: stdin)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)

    if args.path == "-":
        text = sys.stdin.read()
        label = "<stdin>"
    else:
        try:
            with open(args.path, "r") as handle:
                text = handle.read()
        except (IOError, OSError) as exc:
            sys.stderr.write("cannot read input: %s\n" % exc)
            return 2
        label = args.path

    findings, blocks = lint(text)
    return report(label, findings, blocks, sys.stdout, args.strict)


if __name__ == "__main__":
    sys.exit(main())
