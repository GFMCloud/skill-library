#!/usr/bin/env python3
"""
check-claims.py - the resume-side gate for the handoff skill's Typed claim v1 block.

Usage:
    python3 check-claims.py <path-to-handoff-markdown-file>

Reads the first ```yaml fenced block whose content starts with "claims: v1" out of the
given markdown file, runs every `checkable[].check` command against the live artifact it
names, compares the fresh output to `expected`, and prints a discrepancy table followed
by the "unverified by design" list. Exits 1 if any checkable claim mismatches, exits 0
if every checkable claim matches (this is a re-check, not a substitute for asking the
one question Resume Mode calls for when a claim is ambiguous - that judgment stays with
the session, not this script).

This implements the read side described in
plugins/workbench/skills/handoff/references/claims.md, steps 2-4. The shape itself
(Typed claim v1) is defined once in the toolkit interface spec, section 4; this script
does not redefine it.
"""
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


def main(argv):
    if len(argv) != 2:
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
    print("RESULT: all checkable claims match.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
