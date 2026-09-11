#!/usr/bin/env python3
"""One poll cycle of change-watch.

Consumes and updates a Seen-index entry v1 file (toolkit interface spec,
section 6). Applies the transition predicate: report iff
current_state != last_state. last_seen advances on every call; last_state
and last_reported advance only on a transition.

Usage:
    watch-step.py <seen-index.yaml> <source> <current-state>

Prints exactly one line:
    REPORT <source> <old> -> <new>     (a transition happened)
    NO-REPORT                          (same state as last time, or first
                                         observation with no prior state)

Exit codes: 0 on success (either outcome), 1 on a usage or file error.

No YAML library dependency: the seen-index file is small and line-shaped
(spec section 6 field list is fixed), so this reads and writes it with a
minimal hand-rolled parser rather than pulling in PyYAML. This is a
narrow, single-purpose format, not general YAML.
"""
import sys
import datetime


FIELDS = ["seen", "source", "last_state", "last_seen", "last_reported"]


def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def load_entry(path):
    """Return a dict with keys from FIELDS, or None values for a missing file."""
    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return {"seen": "v1", "source": None, "last_state": None,
                "last_seen": None, "last_reported": None}

    entry = {}
    for line in lines:
        line = line.rstrip("\n")
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if key in FIELDS:
            entry[key] = value
    for key in FIELDS:
        entry.setdefault(key, None)
    return entry


def write_entry(path, entry):
    last_reported = entry["last_reported"] if entry["last_reported"] is not None else "never"
    with open(path, "w") as f:
        f.write("seen: v1\n")
        f.write(f"source: {entry['source']}\n")
        f.write(f"last_state: {entry['last_state']}\n")
        f.write(f"last_seen: {entry['last_seen']}\n")
        f.write(f"last_reported: {last_reported}\n")


def main(argv):
    if len(argv) != 4:
        sys.stderr.write(
            "usage: watch-step.py <seen-index.yaml> <source> <current-state>\n"
        )
        return 1

    path, source, current_state = argv[1], argv[2], argv[3]
    entry = load_entry(path)

    if entry.get("source") is not None and entry["source"] != source:
        sys.stderr.write(
            f"error: seen-index at {path} is for source '{entry['source']}', "
            f"not '{source}'\n"
        )
        return 1

    old_state = entry.get("last_state")
    timestamp = now_iso()

    # The predicate is a transition (current != last), never mere presence
    # in the index. A first observation (old_state is None) has nothing to
    # transition from, so it is recorded but not reported.
    is_transition = old_state is not None and old_state != current_state

    entry["source"] = source
    entry["last_seen"] = timestamp
    if old_state is None:
        entry["last_state"] = current_state
        # first observation: no prior state, so no report, but seed last_state
    elif is_transition:
        entry["last_state"] = current_state
        entry["last_reported"] = timestamp

    write_entry(path, entry)

    if is_transition:
        print(f"REPORT {source} {old_state} -> {current_state}")
    else:
        print("NO-REPORT")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
