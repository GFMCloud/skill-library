#!/bin/bash
# toolkit-review: structure check for one judgment, rubric v2.
# Usage: check-judgment.sh <judgment.md> [compare|self]     default: compare
# Exit 0 only if the judgment has the required sections in order, every per-item row
# carries a valid class with the id its class requires, no two items supersede each other,
# no item names itself, and exactly one "Deciding criteria" line exists. A judgment that
# fails is re-dispatched, never repaired. Known weakness: structure only. It cannot tell a
# thoughtful steelman from a token one, and it does not know whether a named id exists;
# make-ledger.py checks ids against items.tsv.
f="$1"; mode="${2:-compare}"
if [ ! -s "$f" ]; then echo "check-judgment: missing or empty: $f"; exit 1; fi
python3 - "$f" "$mode" <<'PY'
import re, sys
path, mode = sys.argv[1], sys.argv[2]
text = open(path, encoding="utf-8", errors="replace").read()
fails = []
heads = [(m.start(), m.group(1).strip()) for m in re.finditer(r"^#{2,4}\s+(.+?)\s*$", text, re.M)]
def pos(pattern):
    for p, h in heads:
        if re.match(pattern, h, re.I):
            return p
    return None
if mode == "compare":
    steel = [p for p, h in heads if re.match(r"Steelman\s+\S", h, re.I)]
    if len(steel) < 2:
        fails.append("need two Steelman sections, found %d" % len(steel))
    order = [("Scores", pos(r"Scores")), ("Per-item rows", pos(r"Per-item rows")),
             ("Deciding criteria", pos(r"Deciding criteria")), ("What I could not assess", pos(r"What I could not assess"))]
    classes = re.compile(r"^(SUPERSEDES\s+(item-[0-9a-f]{8})|SUPERSEDED BY\s+(item-[0-9a-f]{8})|COMPLEMENT|FRAGMENT\s*->\s*(item-[0-9a-f]{8})|REDUNDANT\s+(item-[0-9a-f]{8})|DISCARD)\s*$")
    bare = re.compile(r"^(SUPERSEDES|SUPERSEDED BY|FRAGMENT|REDUNDANT)\b")
    ncols = 3
else:
    steel = [p for p, h in heads if re.match(r"Steelman", h, re.I)]
    if len(steel) < 1:
        fails.append("need a Steelman section")
    order = [("Scores", pos(r"Scores")), ("Per-item rows", pos(r"Per-item rows")),
             ("Deciding criteria", pos(r"Deciding criteria")), ("What I could not assess", pos(r"What I could not assess"))]
    classes = re.compile(r"^(KEEP|TIGHTEN\s+\S.*|SPLIT|RETIRE)\s*$")
    bare = re.compile(r"^TIGHTEN\s*$")
    ncols = 4
for name, p in order:
    if p is None:
        fails.append("missing section: " + name)
present = [p for _, p in order if p is not None]
if present != sorted(present):
    fails.append("sections out of order (Scores, Per-item rows, Deciding criteria, What I could not assess)")
if steel and present and max(steel) > present[0]:
    fails.append("a steelman comes after the score table")
# Rows: the table under Per-item rows, up to the next heading.
rows_start = pos(r"Per-item rows")
rows = []
if rows_start is not None:
    nxt = min([p for p, _ in heads if p > rows_start] + [len(text)])
    block = text[rows_start:nxt]
    for line in block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or re.fullmatch(r"-+:?", cells[0].replace(" ", "")) or cells[0].lower() == "item":
            continue
        rows.append(cells)
    if not rows:
        fails.append("Per-item rows has no table rows")
supers = {}
for cells in rows:
    if len(cells) < ncols:
        fails.append("row has %d cells, need %d: %s" % (len(cells), ncols, " | ".join(cells)[:80]))
        continue
    item, cls = cells[0].strip("`* "), cells[1].strip("`* ")
    if not re.fullmatch(r"item-[0-9a-f]{8}", item):
        fails.append("row item is not an id: " + item)
    m = classes.match(cls)
    if not m:
        if bare.match(cls):
            fails.append("class needs an id or a section, none given: %s (%s)" % (cls, item))
        else:
            fails.append("invalid class: %s (%s)" % (cls, item))
        continue
    if mode == "compare":
        target = m.group(2) or m.group(3) or m.group(4) or m.group(5)
        if target and target == item:
            fails.append("item names itself: %s %s" % (item, cls))
        if m.group(2):
            supers[item] = m.group(2)
for a, b in supers.items():
    if supers.get(b) == a:
        fails.append("mutual SUPERSEDES: %s and %s" % (a, b))
        break
ndec = len(re.findall(r"Deciding criteria", text, re.I))
if ndec != 1 and not (ndec == 2 and pos(r"Deciding criteria") is not None):
    fails.append("need exactly one Deciding criteria line, found %d" % ndec)
if fails:
    for x in fails:
        print("check-judgment: " + x)
    sys.exit(1)
print("check-judgment: ok: " + path)
PY
