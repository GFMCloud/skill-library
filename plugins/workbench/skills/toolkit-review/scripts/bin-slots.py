#!/usr/bin/env python3
"""toolkit-review: bin items into slot directories and assign the X/Y letters.

Usage: bin-slots.py            (reads $TR_RUN/items.tsv and $TR_RUN/slot-map.tsv)

items.tsv columns: id, side, source, slot, type, path. An id written as "-" is computed
here as item-<first 8 hex of sha256(path)>, which is stable and names nothing. Each item
is copied (never symlinked, so a reader cannot follow a path back) into
slots/<slot>/<side>/<id>/. Per slot: items.tsv (with ids filled), purpose.txt from the
slot map. Slots with two or more sides get a SystemRandom X/Y assignment in
private/map.json; the assignment is not printed. Slots with one side get no entry and are
extracted as R (self-review). Exit 2 on a missing path or an unknown slot.
"""
import csv, hashlib, json, os, random, shutil, sys

run = os.environ.get("TR_RUN")
if not run:
    sys.exit("bin-slots.py: set TR_RUN to the run directory")
slot_map = {}
with open(os.path.join(run, "slot-map.tsv"), encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        slot_map[row["slot"]] = row
rows = []
with open(os.path.join(run, "items.tsv"), encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        if not row.get("path"):
            continue
        path = os.path.expanduser(row["path"])
        if not os.path.exists(path):
            sys.exit("bin-slots.py: missing path: %s" % path)
        if row["slot"] not in slot_map:
            sys.exit("bin-slots.py: unknown slot %s (not in slot-map.tsv)" % row["slot"])
        if row["id"] in ("", "-"):
            row["id"] = "item-" + hashlib.sha256(os.path.abspath(path).encode()).hexdigest()[:8]
        row["path"] = os.path.abspath(path)
        rows.append(row)
if not rows:
    sys.exit("bin-slots.py: items.tsv has no rows")
slots_dir = os.path.join(run, "slots")
per_slot = {}
for row in rows:
    dest = os.path.join(slots_dir, row["slot"], row["side"], row["id"])
    if os.path.exists(dest):
        shutil.rmtree(dest)
    if os.path.isdir(row["path"]):
        shutil.copytree(row["path"], dest, symlinks=False)
    else:
        os.makedirs(dest, exist_ok=True)
        shutil.copy2(row["path"], os.path.join(dest, os.path.basename(row["path"])))
    per_slot.setdefault(row["slot"], []).append(row)
cols = ["id", "side", "source", "slot", "type", "path"]
mapping = {}
rnd = random.SystemRandom()
for slot, srows in per_slot.items():
    d = os.path.join(slots_dir, slot)
    with open(os.path.join(d, "items.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in srows:
            w.writerow(r)
    with open(os.path.join(d, "purpose.txt"), "w", encoding="utf-8") as f:
        f.write(slot_map[slot].get("purpose", "").strip() + "\n")
    sides = sorted({r["side"] for r in srows})
    if len(sides) == 2:
        letters = ["X", "Y"]
        rnd.shuffle(letters)
        mapping[slot] = {letters[0]: sides[0], letters[1]: sides[1]}
    elif len(sides) > 2:
        sys.exit("bin-slots.py: slot %s has %d sides; many-repos runs bin one candidate side per slot" % (slot, len(sides)))
# Write the full items.tsv back with ids filled, so later steps use the same ids.
with open(os.path.join(run, "items.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow(r)
os.makedirs(os.path.join(run, "private"), exist_ok=True)
with open(os.path.join(run, "private", "map.json"), "w", encoding="utf-8") as f:
    json.dump(mapping, f, indent=2)
nsym = sum(1 for base, dirs, files in os.walk(slots_dir) for n in dirs + files if os.path.islink(os.path.join(base, n)))
print("slots: %d; items placed: %d; two-sided slots mapped: %d; symlinks under slots/: %d"
      % (len(per_slot), len(rows), len(mapping), nsym))
