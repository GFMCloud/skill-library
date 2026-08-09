#!/usr/bin/env python3
"""standing-authorization — authorization as a file the agent reads, not a norm it remembers.

The rule "if the executor has a clear recommended action within ceilings, take it and log
it; do not ask" was already written down. It was violated 17 times, five of them in one
session, by sessions that had just written it. Prose did not bind. This is the same rule
as a file plus a check that can call an unnecessary ask a defect.

Subcommands:
  validate FILE            structural check of the authorization file
  list FILE                print the granted and stop lists, for reading at session start
  check FILE --ask TEXT    classify a proposed ask

Exit codes:
  0  fine — file valid, or the ask is legitimate
  1  defect — file invalid, or the ask is for something already granted
  2  the file could not be read

Stdlib only. Runs on Python 3.9+.
"""

import argparse
import json
import re
import sys

CEILING_WORDS = re.compile(r"(?i)\b(ceiling|budget|cap|limit|threshold|quota|max(?:imum)?)\b")


class DuplicateKey(ValueError):
    pass


def _no_duplicate_keys(pairs):
    """A prior project referenced 'the turn ceiling' from four documents and defined it in
    none. A duplicate key here would collapse silently and produce the same phantom."""
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise DuplicateKey("duplicate key %r — one value, in one place, or it is not a "
                               "ceiling" % key)
        seen[key] = value
    return seen


def load(path):
    with open(path, "r") as handle:
        return json.load(handle, object_pairs_hook=_no_duplicate_keys)


# --------------------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------------------

def _match_list(entry, where, errors):
    match = entry.get("match")
    if not isinstance(match, list) or not match:
        errors.append("%s: 'match' must be a non-empty array of keywords or re: patterns"
                      % where)
        return []
    out = []
    for i, item in enumerate(match):
        if not isinstance(item, str) or not item.strip():
            errors.append("%s.match[%d]: must be a non-empty string" % (where, i))
            continue
        if item.startswith("re:"):
            try:
                re.compile(item[3:])
            except re.error as exc:
                errors.append("%s.match[%d]: bad regex — %s" % (where, i, exc))
                continue
        out.append(item)
    return out


def validate(doc):
    errors = []
    warnings = []
    if not isinstance(doc, dict):
        return ["authorization file root must be a JSON object"], []

    if not isinstance(doc.get("project"), str) or not doc["project"].strip():
        errors.append("'project' must be a non-empty string")

    ceilings = doc.get("ceilings", {})
    if not isinstance(ceilings, dict):
        errors.append("'ceilings' must be an object")
        ceilings = {}
    for name, body in ceilings.items():
        where = "ceilings.%s" % name
        if not isinstance(body, dict):
            errors.append("%s: must be an object with 'value' and 'unit'" % where)
            continue
        if "value" not in body:
            errors.append("%s: has no 'value'. A ceiling with no number is a phantom — it "
                          "reads as settled precisely because it is cross-referenced and "
                          "never defined." % where)
        if not isinstance(body.get("unit"), str) or not body["unit"].strip():
            errors.append("%s: 'unit' must be a non-empty string — a bare number is not a "
                          "ceiling" % where)

    granted = doc.get("granted")
    if not isinstance(granted, list) or not granted:
        errors.append("'granted' must be a non-empty array. An empty granted list is the "
                      "state this file exists to leave.")
        granted = []

    stop = doc.get("stop")
    if not isinstance(stop, list) or not stop:
        errors.append("'stop' must be a non-empty array — irreversible actions, spend, "
                      "credentials, production, anything changing intent")
        stop = []

    referenced = set()
    granted_keys = {}
    for i, entry in enumerate(granted):
        where = "granted[%d]" % i
        if not isinstance(entry, dict):
            errors.append("%s: must be an object" % where)
            continue
        action = entry.get("action")
        if not isinstance(action, str) or not action.strip():
            errors.append("%s: 'action' must be a non-empty string" % where)
            action = ""
        else:
            where = "granted %r" % action
        for key in _match_list(entry, where, errors):
            granted_keys.setdefault(key.lower(), []).append(action)
        if not isinstance(entry.get("log_to"), str) or not entry["log_to"].strip():
            errors.append("%s: 'log_to' must name where the action is logged. Granted "
                          "without logged is not granted." % where)
        ceiling = entry.get("ceiling")
        if ceiling is not None:
            names = [ceiling] if isinstance(ceiling, str) else ceiling
            if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
                errors.append("%s: 'ceiling' must name an entry in 'ceilings', or list "
                              "several" % where)
                names = []
            for name in names:
                if name not in ceilings:
                    errors.append("%s: references ceiling %r, which is not defined in "
                                  "'ceilings'. Referenced-and-undefined is the exact shape "
                                  "of the phantom." % (where, name))
                else:
                    referenced.add(name)
        elif action and CEILING_WORDS.search(action):
            errors.append("%s: names a ceiling in prose but binds none — add a 'ceiling' "
                          "key pointing at 'ceilings'" % where)

    stop_keys = {}
    for i, entry in enumerate(stop):
        where = "stop[%d]" % i
        if not isinstance(entry, dict):
            errors.append("%s: must be an object" % where)
            continue
        action = entry.get("action")
        if not isinstance(action, str) or not action.strip():
            errors.append("%s: 'action' must be a non-empty string" % where)
            action = ""
        else:
            where = "stop %r" % action
        for key in _match_list(entry, where, errors):
            stop_keys.setdefault(key.lower(), []).append(action)

    for key in sorted(set(granted_keys) & set(stop_keys)):
        errors.append(
            "keyword %r appears in both granted (%s) and stop (%s). One keyword, one side. "
            "An ambiguous rule is the rule that gets ignored."
            % (key, granted_keys[key][0], stop_keys[key][0]))

    for name in sorted(set(ceilings) - referenced):
        warnings.append("ceilings.%s is defined and never referenced — either bind it to a "
                        "granted action or delete it" % name)

    return errors, warnings


# --------------------------------------------------------------------------------------
# classification
# --------------------------------------------------------------------------------------

def matches(entry, text):
    for item in entry.get("match", []):
        if not isinstance(item, str):
            continue
        if item.startswith("re:"):
            try:
                if re.search(item[3:], text, re.IGNORECASE):
                    return item
            except re.error:
                continue
        elif item.lower() in text:
            return item
    return None


def classify(doc, ask):
    text = " ".join(ask.lower().split())
    for entry in doc.get("stop", []):
        if isinstance(entry, dict):
            hit = matches(entry, text)
            if hit:
                return ("STOP-LISTED", entry, hit)
    for entry in doc.get("granted", []):
        if isinstance(entry, dict):
            hit = matches(entry, text)
            if hit:
                return ("ALREADY-GRANTED", entry, hit)
    return ("NOT-COVERED", None, None)


def ceiling_text(doc, entry):
    ceiling = entry.get("ceiling")
    if not ceiling:
        return "no ceiling bound"
    names = [ceiling] if isinstance(ceiling, str) else ceiling
    parts = []
    for name in names:
        body = doc.get("ceilings", {}).get(name, {})
        parts.append("%s = %s %s" % (name, body.get("value"), body.get("unit")))
    return "; ".join(parts)


# --------------------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------------------

def cmd_validate(doc, path, out):
    errors, warnings = validate(doc)
    for warning in warnings:
        out.write("WARN  %s\n" % warning)
    for error in errors:
        out.write("ERROR %s\n" % error)
    out.write("\nSCOPE OF THIS RESULT\n")
    out.write("-" * 78 + "\n")
    out.write("  Structure only, for %s. It checks that every ceiling resolves to one\n" % path)
    out.write("  stated value in one place, that granted and stop do not overlap, and that\n")
    out.write("  every granted action says where it is logged. It does not judge whether the\n")
    out.write("  granted list is the right list — that is Graham's call and his alone.\n\n")
    if errors:
        out.write("INVALID — %d error(s), %d warning(s)\n" % (len(errors), len(warnings)))
        return 1
    out.write("VALID — 0 errors, %d warning(s)\n" % len(warnings))
    return 0


def cmd_list(doc, out):
    out.write("standing authorization — %s\n" % doc.get("project", "(unnamed project)"))
    out.write("=" * 78 + "\n\n")
    out.write("GRANTED — do these and log them. Asking is the defect.\n")
    out.write("-" * 78 + "\n")
    for entry in doc.get("granted", []):
        out.write("  - %s\n" % entry.get("action"))
        out.write("      ceiling: %s\n" % ceiling_text(doc, entry))
        out.write("      log to:  %s\n" % entry.get("log_to"))
    out.write("\nSTOP — never without a fresh answer, whatever the file says elsewhere.\n")
    out.write("-" * 78 + "\n")
    for entry in doc.get("stop", []):
        out.write("  - %s\n" % entry.get("action"))
    out.write("\nAnything named in neither list is uncovered: ask, and add the answer here.\n")
    return 0


def cmd_check(doc, ask, out):
    verdict, entry, hit = classify(doc, ask)
    out.write("ask:     %s\n" % " ".join(ask.split()))
    out.write("verdict: %s\n" % verdict)
    if verdict == "STOP-LISTED":
        out.write("matched: %r against stop entry %r\n" % (hit, entry.get("action")))
        out.write("\nAsking is correct. This one is on the stop-list and stays there.\n")
        return 0
    if verdict == "ALREADY-GRANTED":
        out.write("matched: %r against granted entry %r\n" % (hit, entry.get("action")))
        out.write("ceiling: %s\n" % ceiling_text(doc, entry))
        out.write("log to:  %s\n" % entry.get("log_to"))
        out.write("\nDEFECT — this is already authorized. Asking for it spends a turn that the\n")
        out.write("file exists to remove. Take the action, stay inside the ceiling above, and\n")
        out.write("log it where the entry says.\n")
        return 1
    out.write("\nNot covered either way. Asking is correct. When the answer comes back, add it\n")
    out.write("to granted or to stop so the same question cannot be asked twice.\n")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="authz.py",
        description="Standing authorization as a file, with a check that can call an "
                    "unnecessary ask a defect.")
    sub = parser.add_subparsers(dest="command")

    p_validate = sub.add_parser("validate", help="structural check of the authorization file")
    p_validate.add_argument("file")

    p_list = sub.add_parser("list", help="print the granted and stop lists")
    p_list.add_argument("file")

    p_check = sub.add_parser("check", help="classify a proposed ask")
    p_check.add_argument("file")
    p_check.add_argument("--ask", required=True, help="the question you are about to send")

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 2

    try:
        doc = load(args.file)
    except (IOError, OSError) as exc:
        sys.stderr.write("cannot read authorization file: %s\n" % exc)
        return 2
    except DuplicateKey as exc:
        sys.stderr.write("authorization file is invalid: %s\n" % exc)
        return 1
    except ValueError as exc:
        sys.stderr.write("authorization file is not valid JSON: %s\n" % exc)
        return 2

    if args.command == "validate":
        return cmd_validate(doc, args.file, sys.stdout)
    if args.command == "list":
        return cmd_list(doc, sys.stdout)
    return cmd_check(doc, args.ask, sys.stdout)


if __name__ == "__main__":
    sys.exit(main())
