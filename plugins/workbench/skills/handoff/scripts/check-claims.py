#!/usr/bin/env python3
"""
check-claims.py - the resume-side gate for the handoff skill's Typed claim v1 block.

Usage:
    python3 check-claims.py <path-to-handoff-markdown-file> [--project <repo dir>]

Reads the first ```yaml fenced block whose content starts with "claims: v1" out of the
given markdown file, runs every `checkable[].check` command against the live artifact it
names, compares the fresh output to `expected`, and prints a staleness section, then a
discrepancy table, then the "unverified by design" list. The staleness section lists
files in the project's git repo (--project, default the current directory) whose mtime
is after the block's `written_at`; it warns and never changes the exit code, because a
project that moved on is a fact for the status, not a failed claim. It sees files that
exist now: a deletion or a commit that left mtimes alone does not show.
Exits 1 if any checkable claim mismatches, exits 0
if every checkable claim matches (this is a re-check, not a substitute for asking the
one question Resume Mode calls for when a claim is ambiguous - that judgment stays with
the session, not this script).

This implements the read side described in
plugins/workbench/skills/handoff/references/claims.md, steps 2-4. The shape itself
(Typed claim v1) is defined once in the toolkit interface spec, section 4; this script
does not redefine it.
"""
import datetime
import os
import re
import subprocess
import sys

FENCE_RE = re.compile(r"```yaml\s*\n(claims: v1\n.*?)```", re.DOTALL)


def extract_claims_yaml(text: str) -> str:
    match = FENCE_RE.search(text)
    if not match:
        raise ValueError("no fenced ```yaml claims: v1 block found in the handoff file")
    return match.group(1)


def run_check(command: str) -> str:
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def written_timestamp(doc, handoff_path):
    """(epoch seconds, label) for when the handoff was written: the block's written_at,
    else the handoff file's mtime (weaker: claiming a handoff appends a line to it)."""
    written_at = doc.get("written_at")
    if isinstance(written_at, str):
        try:
            written_at = datetime.datetime.fromisoformat(written_at)
        except ValueError:
            written_at = None
    if isinstance(written_at, datetime.datetime):
        return written_at.timestamp(), f"written_at {written_at.isoformat()}"
    mtime = os.path.getmtime(handoff_path)
    stamp = datetime.datetime.fromtimestamp(mtime).isoformat(timespec="seconds")
    return mtime, f"the handoff file's mtime {stamp}; the block has no usable written_at"


def files_changed_since(project, since, handoff_path):
    """Tracked and untracked-unignored files under the git repo at `project` whose mtime
    is after `since`, newest first, or None when `project` is not inside a git repo."""
    listing = subprocess.run(
        ["git", "-C", project, "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
    )
    if listing.returncode != 0:
        return None
    handoff_real = os.path.realpath(handoff_path)
    changed = []
    for rel in sorted(set(filter(None, listing.stdout.split("\0")))):
        full = os.path.join(project, rel)
        if os.path.realpath(full) == handoff_real or not os.path.isfile(full):
            continue
        mtime = os.path.getmtime(full)
        if mtime > since:
            changed.append((mtime, rel))
    return sorted(changed, reverse=True)


def print_staleness(project, doc, handoff_path):
    since, label = written_timestamp(doc, handoff_path)
    changed = files_changed_since(project, since, handoff_path)
    print("Staleness")
    print("=========")
    if changed is None:
        print(f"not checked: {project} is not inside a git repo. Pass --project <repo dir>.")
    elif not changed:
        print(f"fresh: no file in {project} changed after {label}.")
    else:
        print(f"STALE: {len(changed)} file(s) in {project} changed after {label}. Newest first:")
        for mtime, rel in changed[:10]:
            stamp = datetime.datetime.fromtimestamp(mtime).isoformat(timespec="seconds")
            print(f"  {stamp}  {rel}")
        if len(changed) > 10:
            print(f"  ... and {len(changed) - 10} more")
        print("A match below proves only the claimed value; it does not cover these changes.")
    print()
    return bool(changed)


def main(argv):
    if len(argv) == 4 and argv[2] == "--project":
        project = argv[3]
    elif len(argv) == 2:
        project = os.getcwd()
    else:
        print(__doc__)
        return 2

    path = argv[1]
    with open(path, "r") as f:
        text = f.read()

    try:
        import yaml
    except ImportError:
        print("PyYAML is required: pip install pyyaml", file=sys.stderr)
        return 2

    try:
        claims_yaml = extract_claims_yaml(text)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    doc = yaml.safe_load(claims_yaml)
    if doc.get("claims") != "v1":
        print(f"ERROR: expected claims: v1, got claims: {doc.get('claims')!r}", file=sys.stderr)
        return 2

    checkable = doc.get("checkable", [])
    not_checkable = doc.get("not_checkable", [])

    rows = []
    any_mismatch = False
    for entry in checkable:
        claim = entry["claim"]
        command = entry["check"]
        expected = str(entry["expected"]).strip()
        actual = run_check(command)
        status = "match" if actual == expected else "mismatch"
        if status == "mismatch":
            any_mismatch = True
        rows.append((claim, command, actual, status))

    stale = print_staleness(project, doc, path)

    print("Discrepancy table")
    print("=================")
    for claim, command, actual, status in rows:
        print(f"claim:   {claim}")
        print(f"command: {command}")
        print(f"actual:  {actual}")
        print(f"status:  {status}")
        print("-----------------")

    print()
    print("Unverified by design")
    print("=====================")
    if not not_checkable:
        print("(none listed)")
    else:
        for entry in not_checkable:
            print(f"[{entry.get('kind')}] {entry.get('text')}")

    print()
    if any_mismatch:
        print("RESULT: mismatch - stop and ask before acting on this handoff.")
        return 1
    if stale:
        print("RESULT: all checkable claims match, but the project changed after the handoff "
              "was written - say so in the status.")
        return 0
    print("RESULT: all checkable claims match.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
