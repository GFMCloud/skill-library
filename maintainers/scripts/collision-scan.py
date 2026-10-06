#!/usr/bin/env python3
"""collision-scan.py: description collision scan over the installed skills.

Reads docs/inventory.md (one row per skill), builds a TF-IDF vector over each skill's name
plus description, and prints every pair whose cosine similarity is at or above the
threshold (default 0.35). Two skills that print here would compete for the same prompts.
Stdlib only. Usage, from the library root:

    python3 maintainers/scripts/collision-scan.py [--threshold 0.35] [--inventory docs/inventory.md]
    python3 maintainers/scripts/collision-scan.py --self-test

--self-test proves the scan on fixtures (FIXTURE text, not real skills): two near-identical
descriptions must score at or above the threshold and two unrelated ones below it; exit 1
otherwise. Idea from the placebo review (2026-09-28, pin da03cc2, static/collisions.py);
written fresh here so nothing is installed.
"""
import math, re, sys, argparse, collections

STOP = set("a an the and or of to for in on with by from as is are be this that it its into "
           "use when use whenever not no any all one two three your you we they what which who".split())

def tokens(text):
    return [w for w in re.findall(r"[a-z][a-z0-9_-]+", text.lower()) if w not in STOP and len(w) > 2]

def vectors(docs):
    tfs = [collections.Counter(tokens(d)) for d in docs]
    df = collections.Counter()
    for tf in tfs:
        df.update(tf.keys())
    n = len(docs)
    out = []
    for tf in tfs:
        total = sum(tf.values()) or 1
        v = {w: (c / total) * math.log((1 + n) / (1 + df[w])) for w, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        out.append({w: x / norm for w, x in v.items()})
    return out

def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(w, 0.0) for w, x in a.items())

def read_inventory(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        if not line.startswith("| ") or line.startswith("| name") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5:
            rows.append((cells[0], cells[1], cells[0] + " " + cells[4]))
    return rows

def scan(rows, threshold):
    vecs = vectors([r[2] for r in rows])
    pairs = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            s = cosine(vecs[i], vecs[j])
            if s >= threshold:
                pairs.append((s, rows[i], rows[j]))
    return sorted(pairs, reverse=True)

def self_test(threshold):
    rows = [
        ("fixture-a", "p", "fixture-a Review an incoming GitHub repo or article against what is installed and turn the verdict into applied changes"),
        ("fixture-b", "p", "fixture-b Review an incoming GitHub repository or article against the installed set and turn the verdict into applied changes"),
        ("fixture-c", "p", "fixture-c Convert slide deck exports into native editable PowerPoint files with placeholder boxes for charts"),
        ("fixture-d", "p", "fixture-d Migrate a static site from GitHub Pages onto Cloudflare Pages with a custom domain on external DNS"),
    ]
    pairs = scan(rows, threshold)
    names = {(p[1][0], p[2][0]) for p in pairs}
    ok_pos = ("fixture-a", "fixture-b") in names
    ok_neg = all(("fixture-a" in n and "fixture-b" in n) for n in names)
    for s, a, b in pairs:
        print(f"FIXTURE pair {a[0]} ~ {b[0]} cosine {s:.3f}")
    print("SELF-TEST", "PASS" if (ok_pos and ok_neg) else "FAIL",
          f"(positive pair found: {ok_pos}; no unrelated pair above {threshold}: {ok_neg})")
    return 0 if (ok_pos and ok_neg) else 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.35)
    ap.add_argument("--inventory", default="docs/inventory.md")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test(a.threshold))
    rows = read_inventory(a.inventory)
    if not rows:
        print("collision-scan: zero skills read from", a.inventory, "(a scan of nothing is not a pass)"); sys.exit(2)
    pairs = scan(rows, a.threshold)
    for s, x, y in pairs:
        print(f"{s:.3f}  {x[1]}:{x[0]}  ~  {y[1]}:{y[0]}")
    print(f"{len(rows)} skills scanned, {len(pairs)} pair(s) at or above {a.threshold}")

if __name__ == "__main__":
    main()
