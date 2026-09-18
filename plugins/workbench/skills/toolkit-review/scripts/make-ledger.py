#!/usr/bin/env python3
"""toolkit-review: assemble the ledger from the judgments, rubric v2.

Usage: make-ledger.py            (reads $TR_RUN; writes ledger-items/, LEDGER.md, decisions.md,
                                  AMBIGUOUS-CELLS.md)

The slot verdict is computed from the per-item rows, never read from the judge:
  comparison slots (judgments judge-XY, judge-YX, judge-ESC):
    replace    every installed item is SUPERSEDED BY a candidate item (or is the target of
               a candidate SUPERSEDES) or DISCARD, and at least one is superseded
    merge      any candidate item is SUPERSEDES, COMPLEMENT or FRAGMENT, but not replace
    drop-both  every row on both sides is DISCARD
    keep       otherwise
  self-review slots (judge-S1, judge-S2): the verdict is the count of each class.
Judge agreement is per derived verdict and per item (same class word). A candidate item
counts as "named to take" when a judge classed it SUPERSEDES, COMPLEMENT or FRAGMENT.
Cells the assembler could not resolve (a class with an id that is not in items.tsv, a row
for an id no report has, a judge classing one item two ways) are printed in
AMBIGUOUS-CELLS.md and never guessed. decisions.md uses source-intake's contract v1
vocabulary by a fixed mapping (SUPERSEDES to SUPERIOR SUBSTITUTE, SUPERSEDED BY and
REDUNDANT to REDUNDANT, FRAGMENT to INGESTIBLE FRAGMENT, COMPLEMENT and DISCARD unchanged)
so the file a later source-intake run reads keeps its contract.
"""
import csv, glob, json, os, re, sys

run = os.environ.get("TR_RUN")
if not run:
    sys.exit("make-ledger.py: set TR_RUN to the run directory")
cfg = json.load(open(os.path.join(run, "run.json"), encoding="utf-8"))
items = {}
with open(os.path.join(run, "items.tsv"), encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        if row.get("id", "").startswith("item-"):
            items[row["id"]] = row
slot_map = {}
with open(os.path.join(run, "slot-map.tsv"), encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        slot_map[row["slot"]] = row
mapping = {}
mp = os.path.join(run, "private", "map.json")
if os.path.isfile(mp):
    mapping = json.load(open(mp, encoding="utf-8"))
V1 = {"SUPERSEDES": "SUPERIOR SUBSTITUTE", "SUPERSEDED": "REDUNDANT", "REDUNDANT": "REDUNDANT",
      "FRAGMENT": "INGESTIBLE FRAGMENT", "COMPLEMENT": "COMPLEMENT", "DISCARD": "DISCARD"}
ambiguous, ledger_rows, decision_rows = [], [], []

def parse_rows(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"^#{2,4}\s+(.+?)\s*$", text, re.M)]
    start = next((p for p, h in heads if re.match(r"Per-item rows", h, re.I)), None)
    if start is None:
        return {}, text
    end = min([p for p, _ in heads if p > start] + [len(text)])
    out = {}
    for line in text[start:end].splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip().strip("`* ") for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() == "item" or re.fullmatch(r"-+:?", cells[0].replace(" ", "")):
            continue
        item = cells[0]
        if item in out:
            ambiguous.append("%s: %s classed twice (%s / %s)" % (os.path.basename(path), item, out[item][0], cells[1]))
            continue
        out[item] = (cells[1], cells[2:])
    return out, text

def deciding(text):
    m = re.search(r"Deciding criteria[:*\s]*\n?(.+)", text, re.I)
    return m.group(1).strip() if m else ""

os.makedirs(os.path.join(run, "ledger-items"), exist_ok=True)
for slot in sorted(slot_map):
    jfiles = sorted(glob.glob(os.path.join(run, "judgments", slot, "judge-*.md")))
    if not jfiles:
        ledger_rows.append((slot, "none: no judgment", "", slot_map[slot].get("evidence", ""), "", "", "no judgment on disk"))
        continue
    self_mode = all(re.search(r"judge-S\d", j) for j in jfiles)
    sides = {r["side"] for r in items.values() if r["slot"] == slot}
    letter_side = mapping.get(slot, {})
    per_judge = []
    for j in jfiles:
        rows, text = parse_rows(j)
        per_judge.append((os.path.basename(j), rows, deciding(text)))
    all_ids = sorted({i for _, rows, _ in per_judge for i in rows})
    with open(os.path.join(run, "ledger-items", slot + ".tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["id", "side", "source", "type", "path"] + [name for name, _, _ in per_judge])
        for i in all_ids:
            meta = items.get(i)
            if not meta:
                ambiguous.append("%s: judge row for unknown id %s" % (slot, i))
                continue
            w.writerow([i, meta["side"], meta["source"], meta["type"], meta["path"]]
                       + [rows.get(i, ("", []))[0] for _, rows, _ in per_judge])
    if self_mode:
        counts = {}
        for name, rows, _ in per_judge:
            for i, (cls, _) in rows.items():
                counts.setdefault(name, {}).setdefault(cls.split()[0], 0)
                counts[name][cls.split()[0]] += 1
        verdicts = ["; ".join("%s %d" % (k, v) for k, v in sorted(c.items())) for c in counts.values()]
        agree_items = sum(1 for i in all_ids if len({rows.get(i, ("", []))[0].split()[0] if rows.get(i) else "" for _, rows, _ in per_judge}) == 1)
        ledger_rows.append((slot, " / ".join(verdicts), "%d of %d items same class" % (agree_items, len(all_ids)),
                            "self-review, reading only", " / ".join(d for _, _, d in per_judge),
                            "ledger-items/%s.tsv" % slot, ""))
        for i in all_ids:
            meta = items.get(i, {})
            decision_rows.append((slot, i, meta.get("path", ""), " / ".join(rows.get(i, ("", []))[0] for _, rows, _ in per_judge), "self-review"))
        continue
    installed = {i for i, r in items.items() if r["slot"] == slot and r["side"] == "installed"}
    cand = {i for i, r in items.items() if r["slot"] == slot and r["side"] != "installed"}
    derived, named = [], {}
    for name, rows, _ in per_judge:
        classes = {i: c for i, (c, _) in rows.items()}
        for i, c in classes.items():
            m = re.search(r"item-[0-9a-f]{8}", c)
            if m and m.group(0) not in items:
                ambiguous.append("%s %s: %s names unknown id %s" % (slot, name, i, m.group(0)))
        superseded = {i for i in installed if classes.get(i, "").startswith("SUPERSEDED BY")}
        for i in cand:
            m = re.match(r"SUPERSEDES\s+(item-[0-9a-f]{8})", classes.get(i, ""))
            if m and m.group(1) in installed:
                superseded.add(m.group(1))
        discarded = {i for i in installed if classes.get(i, "") == "DISCARD"}
        take = {i for i in cand if re.match(r"(SUPERSEDES|COMPLEMENT|FRAGMENT)", classes.get(i, ""))}
        for i in take:
            named.setdefault(i, []).append(name)
        if all(classes.get(i, "") == "DISCARD" for i in installed | cand) and (installed | cand):
            v = "drop-both"
        elif installed and installed <= (superseded | discarded) and superseded:
            v = "replace"
        elif take:
            v = "merge"
        else:
            v = "keep"
        derived.append(v)
    agree = "%d of %d" % (derived.count(derived[0]), len(derived))
    agree_items = sum(1 for i in all_ids if len({rows.get(i, ("", []))[0].split()[0] if rows.get(i) else "" for _, rows, _ in per_judge}) == 1)
    both = sum(1 for i, js in named.items() if len(js) == len(per_judge))
    risk = "judges agree on the class of %d of %d items; %d candidate items named to take by at least one judge, %d by both" % (agree_items, len(all_ids), len(named), both)
    ledger_rows.append((slot, " / ".join(derived), agree, slot_map[slot].get("evidence", ""),
                        " / ".join(d for _, _, d in per_judge), "ledger-items/%s.tsv" % slot, risk))
    for i in sorted(cand):
        meta = items[i]
        classes = [rows.get(i, ("", []))[0] for _, rows, _ in per_judge]
        v1 = " / ".join(V1.get(c.split()[0], c) if c else "" for c in classes)
        decision_rows.append((slot, i, meta["path"], v1, "; ".join(classes)))

# LEDGER.md
tpl = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", "ledger.md"), encoding="utf-8").read()
srcs = ", ".join("%s at %s" % (s.get("id"), s.get("pin", "?")) for s in cfg.get("sources", [])) or "none (self-review)"
table = "\n".join("| %s | %s | %s | %s | %s | %s | %s |" % r for r in ledger_rows)
out = tpl.replace("[run name]", cfg.get("name", "")).replace("[sources]", srcs).replace("[created]", cfg.get("created", ""))
out = out.replace("[slot rows]", table)
open(os.path.join(run, "LEDGER.md"), "w", encoding="utf-8").write(out)
# decisions.md, contract v1 shape
lines = ["# Decisions: %s" % cfg.get("name", ""), "", "contract: v1", "classes: rubric v2 mapped to v1 (see make-ledger.py)",
         "source: %s" % srcs, "reviewed: %s" % cfg.get("created", ""), "verdict: <ADOPT | HARVEST | WATCH | SKIP, ruled by the owner from the rows>", "",
         "## Rows", "", "| # | Slot | Item | Source path | Class (v1, per judge) | Class (v2, per judge) | Ruling |", "|---|---|---|---|---|---|---|"]
for n, (slot, i, path, v1, v2) in enumerate(decision_rows, 1):
    lines.append("| %d | %s | %s | %s | %s | %s | proposed |" % (n, slot, i, path, v1, v2))
open(os.path.join(run, "decisions.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
open(os.path.join(run, "AMBIGUOUS-CELLS.md"), "w", encoding="utf-8").write(
    "# Ambiguous cells\n\n" + ("\n".join("- " + a for a in ambiguous) if ambiguous else "none") + "\n")
print("LEDGER.md: %d slot rows; decisions.md: %d rows; ambiguous cells: %d" % (len(ledger_rows), len(decision_rows), len(ambiguous)))
