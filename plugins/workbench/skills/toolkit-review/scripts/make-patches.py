#!/usr/bin/env python3
"""toolkit-review: one file list per slot of the candidate items named to take.

Usage: make-patches.py            (reads $TR_RUN/ledger-items/*.tsv; writes patches/<slot>/PATCH.md)

A patch is a file list with the judges' classes beside each path, not rewritten content.
Gate B approves intent to rewrite; the rewrite itself is landing work for approved rows
only, and the landing session reads each source file as data and checks it against the
judge's description before rewriting it (position or id mismatches are a stop).
"""
import csv, glob, os, re, sys

run = os.environ.get("TR_RUN")
if not run:
    sys.exit("make-patches.py: set TR_RUN to the run directory")
n = 0
for tsv in sorted(glob.glob(os.path.join(run, "ledger-items", "*.tsv"))):
    slot = os.path.basename(tsv)[:-4]
    rows = list(csv.DictReader(open(tsv, encoding="utf-8"), delimiter="\t"))
    judges = [k for k in (rows[0].keys() if rows else []) if k.startswith("judge-")]
    take = []
    for r in rows:
        if r["side"] == "installed":
            continue
        classes = {j: r.get(j, "") for j in judges}
        named = [j for j, c in classes.items() if re.match(r"(SUPERSEDES|COMPLEMENT|FRAGMENT)", c or "")]
        if named:
            take.append((r, classes, named))
    if not take:
        continue
    d = os.path.join(run, "patches", slot)
    os.makedirs(d, exist_ok=True)
    lines = ["# Patch: %s (file list, not content)" % slot, "",
             "| Item | Source path | " + " | ".join(judges) + " | Named by |", "|---|---|" + "---|" * (len(judges) + 1)]
    for r, classes, named in take:
        lines.append("| %s | %s | %s | %d of %d |" % (r["id"], r["path"], " | ".join(classes[j] for j in judges), len(named), len(judges)))
    open(os.path.join(d, "PATCH.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    n += 1
    print("patches/%s/PATCH.md: %d rows" % (slot, len(take)))
print("patch files: %d" % n)
