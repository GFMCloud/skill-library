#!/usr/bin/env python3
"""Classify an action name as safe or approval-only from a rules file.

This is the separate classification step the roadmap and the research record
(arXiv 2605.10223, separation of powers) require: it runs before any
diagnostic or fix-drafting call, and it contains no diagnostic content of its
own. It is a lookup, not a judgment call, and it never defaults to safe.

Rules file format: one "<action> <safe|approval-only>" pair per non-comment,
non-blank line. Example:

    diagnose safe
    draft-fix-on-branch safe
    smoke-gate-staging safe
    deploy-production approval-only
    rotate-credential approval-only

Usage:
    classify-action.py <rules-file> <action-name>

Prints the classification word (safe or approval-only) on a match.
On no match, prints "unclassified" to stderr and exits 1. It never
falls back to "safe" for an action absent from the rules file.
"""
import sys


def load_rules(path):
    rules = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 2:
                continue
            action, classification = parts
            if classification not in ("safe", "approval-only"):
                continue
            rules[action] = classification
    return rules


def main(argv):
    if len(argv) != 3:
        sys.stderr.write("usage: classify-action.py <rules-file> <action-name>\n")
        return 1

    rules_path, action = argv[1], argv[2]
    rules = load_rules(rules_path)

    if action not in rules:
        sys.stderr.write("unclassified\n")
        return 1

    print(rules[action])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
