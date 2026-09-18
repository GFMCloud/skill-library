#!/usr/bin/env python3
"""toolkit-review: pattern scorer and discrimination gate for the review fixture (full size).

Usage: score-fixture.py <arm>                 score every run of one arm
       score-fixture.py --gate <min-misses>   the bare arm must miss at least <min-misses>
                                              planted conditions in EVERY run, else exit 1

Reads $TR_RUN/fixtures/review/planted.tsv (id, regex, description) and
fixtures/review/runs/<arm>-<n>.md. A condition counts as found when its regex matches the
report. The gate exists because the ECC fixture (2026-09-17) spent 27 percent of its budget
after a bare arm that already found 8 to 10 of 10 conditions; a fixture whose bare arm
misses nothing cannot show an arm difference and is dropped before the arms run. Known
weakness: a regex can match a report that names the condition only to decline it; spot
check hits by reading the lines, and prefer a blinded restricted scorer for the summary.
"""
import csv, glob, os, re, sys

run = os.environ.get("TR_RUN")
if not run:
    sys.exit("score-fixture.py: set TR_RUN to the run directory")
fx = os.path.join(run, "fixtures", "review")
planted = list(csv.DictReader(open(os.path.join(fx, "planted.tsv"), encoding="utf-8"), delimiter="\t"))
if not planted:
    sys.exit("score-fixture.py: planted.tsv is empty")

def score(arm):
    out = []
    for path in sorted(glob.glob(os.path.join(fx, "runs", arm + "-*.md"))):
        text = open(path, encoding="utf-8", errors="replace").read()
        found = [p["id"] for p in planted if re.search(p["regex"], text, re.I | re.M)]
        out.append((os.path.basename(path), found))
    return out

if len(sys.argv) >= 3 and sys.argv[1] == "--gate":
    need = int(sys.argv[2])
    runs = score("bare")
    if not runs:
        sys.exit("score-fixture.py: no bare runs to gate on")
    ok = True
    for name, found in runs:
        misses = len(planted) - len(found)
        print("%s: found %d of %d, missed %d" % (name, len(found), len(planted), misses))
        if misses < need:
            ok = False
    print("gate: bare arm must miss at least %d in every run: %s" % (need, "PASS" if ok else "FAIL, drop the fixture"))
    sys.exit(0 if ok else 1)
if len(sys.argv) < 2:
    sys.exit(__doc__)
for name, found in score(sys.argv[1]):
    print("%s: %d of %d (%s)" % (name, len(found), len(planted), ", ".join(found)))
