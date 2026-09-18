#!/usr/bin/env python3
"""check-report.py: validate an evidence report's shape mechanically.

Usage: check-report.py <report.md>

Rules, from the skill body ("The format", "The not-verified list is mandatory"):
  - every block opened by a CLAIM: line has CHECK:, OUTPUT: and VERDICT: lines before
    the next CLAIM: or the NOT VERIFIED heading;
  - VERDICT starts with VERIFIED, UNVERIFIED or FAILED;
  - OUTPUT is non-empty for VERIFIED and FAILED (an UNVERIFIED block may have an empty
    OUTPUT, with the reason on the VERDICT line);
  - a VERIFIED or FAILED block carries an identifier somewhere in its CLAIM or OUTPUT: a
    number, a SHA-like hex run, a timestamp, or a path;
  - a NOT VERIFIED section exists, with at least one entry or the word "none".
Exit 0 and a count when clean; exit 1 with one line per failure otherwise.
Known weakness: the identifier rule is a heuristic (any digit or hex run counts), so a
block that quotes a version number as decoration passes it; the rule catches the block
that cites nothing at all, which is the shipped defect it exists for. It cannot tell
whether a CHECK was run; it can only see that its OUTPUT is empty.
"""
import re, sys

if len(sys.argv) != 2:
    sys.exit(__doc__)
path = sys.argv[1]
try:
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
except OSError as e:
    sys.exit("check-report: cannot read %s: %s" % (path, e))
fails = []
blocks, cur = [], None
nv_index = None
for i, line in enumerate(lines, 1):
    s = line.strip()
    if re.match(r"^#*\s*NOT VERIFIED\b", s):
        nv_index = i
        if cur:
            blocks.append(cur); cur = None
        continue
    m = re.match(r"^(CLAIM|CHECK|OUTPUT|VERDICT):\s*(.*)$", s)
    if not m:
        if cur and cur.get("_last") == "OUTPUT" and s and nv_index is None:
            cur["OUTPUT"] += "\n" + s
        continue
    key, val = m.group(1), m.group(2)
    if key == "CLAIM":
        if cur:
            blocks.append(cur)
        cur = {"line": i, "CLAIM": val, "_last": "CLAIM"}
        continue
    if cur is None:
        fails.append("line %d: %s outside any CLAIM block" % (i, key))
        continue
    cur[key] = val
    cur["_last"] = key
if cur:
    blocks.append(cur)
if not blocks:
    fails.append("no CLAIM block found")
ident = re.compile(r"\d|[0-9a-f]{7,}|/[\w.-]+/")
for b in blocks:
    where = "block at line %d (%s)" % (b["line"], b["CLAIM"][:50])
    for k in ("CHECK", "OUTPUT", "VERDICT"):
        if k not in b:
            fails.append("%s: missing %s" % (where, k))
    v = b.get("VERDICT", "")
    vm = re.match(r"^(VERIFIED|UNVERIFIED|FAILED)\b", v)
    if v and not vm:
        fails.append("%s: VERDICT does not start with VERIFIED, UNVERIFIED or FAILED: %s" % (where, v[:40]))
    token = vm.group(1) if vm else ""
    if token in ("VERIFIED", "FAILED"):
        if not b.get("OUTPUT", "").strip():
            fails.append("%s: OUTPUT is empty on a %s verdict" % (where, token))
        if not ident.search(b.get("CLAIM", "") + " " + b.get("OUTPUT", "")):
            fails.append("%s: no identifier (number, hash, timestamp or path) in CLAIM or OUTPUT" % where)
    if token == "VERIFIED" and not re.search(r"rules out|eliminat|shows|confirm", v, re.I):
        fails.append("%s: VERIFIED verdict does not say what it rules out" % where)
if nv_index is None:
    fails.append("no NOT VERIFIED section")
else:
    tail = [l.strip() for l in lines[nv_index:] if l.strip()]
    if not tail or not (any(l.startswith(("-", "*")) for l in tail) or any(l.lower().startswith("none") for l in tail)):
        fails.append("NOT VERIFIED section has no entry and does not say none")
if fails:
    for f in fails:
        print("check-report: " + f)
    sys.exit(1)
print("check-report: ok: %d block(s), NOT VERIFIED section present" % len(blocks))
