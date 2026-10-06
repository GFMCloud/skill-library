#!/usr/bin/env python3
"""
check-claims.py - the resume-side gate for the handoff skill's Typed claim v1 block.

Usage:
    python3 check-claims.py <path-to-handoff-markdown-file> [--project <project dir>]

Reads the first ```yaml fenced block whose content starts with "claims: v1" out of the
given markdown file, runs every `checkable[].check` command against the live artifact it
names, compares the fresh output to `expected`, and prints a staleness section, then a
discrepancy table, then the "unverified by design" list. The staleness section lists
files under the project (--project, default the current directory) whose mtime is after
the block's `written_at`: the git listing inside a repo, a plain directory walk outside
one (labelled "not a git repo, mtime walk"); it warns and never changes the exit code,
because a project that moved on is a fact for the status, not a failed claim. It sees
files that exist now: a deletion or a commit that left mtimes alone does not show.
Every check is printed before any runs, and a write-shaped check (rm, mv, cp, chmod,
sudo, a redirect into a file, a pipe into a shell, git push and its cousins) is refused
with status "refused" and never run. Exits 1 if any check is refused or any checkable
claim mismatches, exits 0 if every checkable claim matches (this is a re-check, not a substitute for asking the
one question Resume Mode calls for when a claim is ambiguous - that judgment stays with
the session, not this script).

This implements the read side described in
plugins/long-projects/skills/handoff/references/claims.md, steps 2-4. The shape itself
(Typed claim v1) is defined once in the toolkit interface spec, section 4; this script
does not redefine it.
"""
import datetime
import os
import re
import subprocess
import sys

FENCE_RE = re.compile(r"```yaml\s*\n(claims: v1\n.*?)```", re.DOTALL)

# Write-shaped check commands are refused, never run (added 2026-09-24, ruled
# Q-2026-09-24-7): a handoff file is data, and its checks are supposed to read the
# live artifact, not change it. Documented in references/claims.md; proven by the
# fourth fixture in fixtures/run-fixtures.sh. Known weakness: a pattern list, so a
# write hidden behind an alias, a here-doc, or a program's own write flag passes, and
# a `>` inside a quoted argument (`grep '=>' f`) is refused as if it were a redirect.
WRITE_SHAPES = [
    re.compile(r"(?<![\w-])(rm|mv|cp|chmod|chown|sudo|tee|truncate|dd|mkfs|ln)\b"),
    # git: the verb must be the subcommand itself (after -C <dir> or --flags), so
    # `git log --grep merge` and `git stash list` stay read-only.
    # `merge(?!-)`: `git merge-base --is-ancestor` is read-only and was refused by the
    # plain `merge\b` form in two sessions (2026-09-27 and 09-28); a word boundary sits
    # between "merge" and "-".
    re.compile(r"\bgit\b(?:\s+-C\s+\S+|\s+--?[\w-]+(?:=\S+)?)*\s+(push|reset|checkout|rebase|"
               r"merge(?!-)|commit|clean|stash\s+(?:push|pop|drop|apply|clear)|branch\s+-[dD]\b|"
               r"worktree\s+(?:remove|prune)|tag\s+-[dfa]\b)\b"),
    re.compile(r"\|\s*(sh|bash|zsh|python3?|perl|ruby|node)\b"),
    re.compile(r"(?<![<>0-9])>{1,2}\s*(?!/dev/null)[^\s|&;]"),   # redirect into a file
]


def write_shaped(command: str):
    """The first write-shaped fragment in `command`, or None when it looks read-only."""
    for pattern in WRITE_SHAPES:
        m = pattern.search(command)
        if m:
            return m.group(0)
    return None


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
    else the handoff file's mtime (weaker; since 0.6.4 a claim is a sidecar file, so the
    handoff's own mtime is no longer disturbed by claiming it)."""
    written_at = doc.get("written_at")
    if isinstance(written_at, str):
        # YAML hands a datetime for `2026-09-11T00:00:00-05:00` and for a trailing `Z`,
        # but a plain string for an offset written without a colon (`-0500`, what
        # `date +%z` prints), and a quoted value stays a string in every form. This Mac's
        # /usr/bin/python3 is 3.9, whose fromisoformat rejects `-0500` and `Z`, so until
        # 0.6.5 such a handoff silently fell back to the file's mtime. Normalize.
        text = written_at.strip()
        text = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", text)
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            written_at = datetime.datetime.fromisoformat(text)
        except ValueError:
            written_at = None
    if isinstance(written_at, datetime.datetime):
        return written_at.timestamp(), f"written_at {written_at.isoformat()}"
    mtime = os.path.getmtime(handoff_path)
    stamp = datetime.datetime.fromtimestamp(mtime).isoformat(timespec="seconds")
    return mtime, f"the handoff file's mtime {stamp}; the block has no usable written_at"


WALK_SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".claude"}


def files_changed_since(project, since, handoff_path):
    """Files under `project` whose mtime is after `since`, newest first, as
    (changed, source). Inside a git repo the listing is tracked plus untracked-unignored
    files (`git ls-files`); outside one it is a plain directory walk that skips
    `.git`, `node_modules`, `__pycache__`, virtualenvs and `.claude`, so a research or
    rollout folder that is not a repo still gets a staleness result (three sessions on
    2026-09-27 and 09-28 checked mtimes by hand because this returned None)."""
    listing = subprocess.run(
        ["git", "-C", project, "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
    )
    if listing.returncode == 0:
        rels = sorted(set(filter(None, listing.stdout.split("\0"))))
        source = "git listing"
    else:
        rels = []
        for root, dirs, files in os.walk(project):
            dirs[:] = sorted(d for d in dirs if d not in WALK_SKIP_DIRS)
            for name in files:
                rels.append(os.path.relpath(os.path.join(root, name), project))
        rels.sort()
        source = "not a git repo, mtime walk"
    handoff_real = os.path.realpath(handoff_path)
    changed = []
    for rel in rels:
        full = os.path.join(project, rel)
        if os.path.realpath(full) == handoff_real or not os.path.isfile(full):
            continue
        mtime = os.path.getmtime(full)
        if mtime > since:
            changed.append((mtime, rel))
    return sorted(changed, reverse=True), source


def print_staleness(project, doc, handoff_path):
    since, label = written_timestamp(doc, handoff_path)
    changed, source = files_changed_since(project, since, handoff_path)
    print("Staleness")
    print("=========")
    if not changed:
        print(f"fresh: no file in {project} changed after {label} ({source}).")
    else:
        print(f"STALE: {len(changed)} file(s) in {project} changed after {label} ({source}). Newest first:")
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

    # Print every check before running any: these are shell commands read from a file.
    print("Checks to run")
    print("=============")
    for entry in checkable:
        print(f"  {entry['check']}")
    print()

    rows = []
    any_mismatch = False
    any_refused = False
    for entry in checkable:
        claim = entry["claim"]
        command = entry["check"]
        expected = str(entry["expected"]).strip()
        shape = write_shaped(command)
        if shape:
            any_refused = True
            rows.append((claim, command, f"(not run: write-shaped, '{shape}')", "refused"))
            continue
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
    if any_refused:
        print("RESULT: refused - a check is write-shaped and was not run; show the row and "
              "ask before acting on this handoff.")
        return 1
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
