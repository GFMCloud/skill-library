#!/usr/bin/env python3
"""check-poison-coverage.py - report which assertion categories have a poison entry.

Usage: check-poison-coverage.py <manifest.yaml>

Per the harness interface spec section 5: "a category with no poison entry is not
proven and the gate reports it as unproven, never as passed." This script is the one
place that reports UNPROVEN; nothing downstream is allowed to read a missing poison
entry as a pass.

Prints one PROVEN/UNPROVEN line per assertion category present in the manifest.
Exit code:
    0  every assertion category has a poison entry (fully proven, pending the actual
       poison run and the live run)
    3  at least one assertion category has no poison entry (unproven) - distinct from
       the smoke script's own 0/1 pass/fail exit codes, so a caller cannot mistake
       "never tested" for "passed"
"""
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("check-poison-coverage.py: PyYAML is required (pip install pyyaml)\n")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("usage: check-poison-coverage.py <manifest.yaml>\n")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        m = yaml.safe_load(f)
    if not isinstance(m, dict) or m.get("smoke") != "v1":
        sys.stderr.write("check-poison-coverage.py: manifest does not declare 'smoke: v1'\n")
        sys.exit(1)

    assertions = m.get("assertions", {}) or {}
    poison = m.get("poison", {}) or {}

    unproven = []
    for category in assertions:
        if category in poison and poison[category] not in (None, ""):
            print(f"PROVEN   {category}: poison entry present")
        else:
            print(f"UNPROVEN {category}: no poison entry - never report this category as passed")
            unproven.append(category)

    if unproven:
        print(f"RESULT: {len(unproven)} unproven categor{'y' if len(unproven) == 1 else 'ies'}: {', '.join(unproven)}")
        sys.exit(3)
    print("RESULT: every assertion category has a poison entry")
    sys.exit(0)


if __name__ == "__main__":
    main()
