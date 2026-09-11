#!/usr/bin/env python3
"""check-pointer.py — validate a rendered Scheduled-task pointer v1 file.

Usage:
    python3 check-pointer.py <pointer.md>

Exit 0 and print "OK" plus a one-line summary when every check passes.
Exit 1 and print one "FAIL <code> <message>" line per violation, then a summary
count, when any check fails. Never raises on a malformed file; a parse failure is
reported as a FAIL line like every other check.

Checks (interface spec section 7, Scheduled-task pointer v1 and Absolute-limits
block v1):
    F1  frontmatter parses and has exactly the keys {name, description}
    F2  body names the harness directory as an absolute path
    F3  body names the phase skill by an absolute path
    F4  body names a mode
    F5  every fixed line of the Absolute-limits block v1 is present verbatim
    F6  the hook-timeout line is present with a filled-in integer
    F7  the consecutive-retry-cap line is present with a filled-in integer

This script only reads the file given on the command line. It never touches
~/.claude/scheduled-tasks/ and never registers anything.
"""
import re
import sys
from pathlib import Path

# The fixed lines of Absolute-limits block v1 (interface spec section 7), excluding
# the two numeric lines, which get their own regex checks so a placeholder or a
# missing value is caught rather than accepted as "present".
FIXED_LIMIT_LINES = [
    "- no git push",
    "- no deletion (rename to .superseded)",
    "- no credentials",
    "- no edits under ~/.claude/plugins/",
    "- no edits to the harness's own CONFIG.md, CLAUDE.md, or prompts/",
    "- no edits in a repo with uncommitted changes this run did not make",
    "- anything the run would have asked becomes a queued Tier 3 item",
]

HOOK_TIMEOUT_RE = re.compile(r"^- hook timeout: (\d+)\s*$", re.M)
RETRY_CAP_RE = re.compile(
    r"^- consecutive-retry cap on a failed or rate-limited step: (\d+)\s*$", re.M
)


def parse_frontmatter(text: str):
    """Return (dict of keys found, remaining body) or (None, text) if no
    frontmatter block is found. Deliberately simple (this pointer's frontmatter
    is two flat scalar keys) rather than a full YAML parse, so a malformed block
    still yields a useful F1 message instead of a traceback."""
    # The frontmatter block must open a line (either the file's first line, the
    # real case, or after a leading FIXTURE-label comment in a fixture file) —
    # re.search with the (?:^|\n) anchor tolerates the latter without accepting
    # '---' appearing mid-paragraph.
    m = re.search(r"(?:^|\n)---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, text
    fm_text, body = m.group(1), m.group(2)
    keys = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        km = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if km:
            keys[km.group(1)] = km.group(2)
    return keys, body


def check(path: Path):
    fails = []
    text = path.read_text(encoding="utf-8")

    keys, body = parse_frontmatter(text)
    if keys is None:
        fails.append("F1 no parseable '---' frontmatter block found")
        keys = {}
        body = text
    else:
        extra = sorted(set(keys) - {"name", "description"})
        missing = sorted({"name", "description"} - set(keys))
        if extra:
            fails.append(f"F1 frontmatter has extra key(s): {extra}")
        if missing:
            fails.append(f"F1 frontmatter missing key(s): {missing}")

    harness_m = re.search(r"^Harness:\s*(\S.*)$", body, re.M)
    if not harness_m:
        fails.append("F2 no 'Harness:' line in the body")
    elif not harness_m.group(1).strip().startswith("/"):
        fails.append(f"F2 harness path is not absolute: '{harness_m.group(1).strip()}'")

    phase_m = re.search(r"^Phase skill:\s*(\S.*)$", body, re.M)
    if not phase_m:
        fails.append("F3 no 'Phase skill:' line in the body")
    elif not phase_m.group(1).strip().startswith("/"):
        fails.append(f"F3 phase skill path is not absolute: '{phase_m.group(1).strip()}'")

    mode_m = re.search(r"^Mode:\s*(\S.*)$", body, re.M)
    if not mode_m:
        fails.append("F4 no 'Mode:' line in the body")

    for line in FIXED_LIMIT_LINES:
        if line not in body:
            fails.append(f"F5 missing Absolute-limits block v1 line: '{line}'")

    if not HOOK_TIMEOUT_RE.search(body):
        fails.append("F6 missing or unfilled 'hook timeout: <seconds>' line")

    if not RETRY_CAP_RE.search(body):
        fails.append(
            "F7 missing or unfilled 'consecutive-retry cap on a failed or "
            "rate-limited step: <n>' line"
        )

    return fails


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"FAIL F0 no such file: {path}")
        print("\n1 failure")
        return 1
    fails = check(path)
    for f in fails:
        print(f"FAIL {f}")
    if fails:
        print(f"\n{len(fails)} failure(s)")
        return 1
    print("OK")
    print("\n0 failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
