#!/usr/bin/env python3
"""toolkit-review: compute the mechanical facts the extraction prompt copies.

Usage: make-facts.py            (reads $TR_RUN/slots/<slot>/items.tsv, writes facts/<slot>.json)

Per item: id, side, type, body_lines (lines of the main markdown file after frontmatter),
description_words (frontmatter description), load (always | on-demand, by type),
runtime_deps (interpreters and runtimes named in shebangs or imports of any code file),
enforcement_files (code files, relative to the item directory), file (the item's main
file, relative to the side directory so it names nothing). These are counted, not
estimated, so a judge does not guess context cost from prose. Known weakness: load is by
type (hooks and rule files always, skills and agents on demand); a skill that a CLAUDE.md
loads unconditionally is still recorded on-demand.
"""
import csv, json, os, re, sys

run = os.environ.get("TR_RUN")
if not run:
    sys.exit("make-facts.py: set TR_RUN to the run directory")
CODE = (".py", ".js", ".ts", ".sh", ".mjs", ".cjs", ".rb")
ALWAYS = ("hook", "rule", "settings", "claude-md")
DEP_WORDS = {"node": "node", "python": "python3", "python3": "python3", "bash": "bash", "zsh": "zsh",
             "docker": "docker", "npm": "npm", "npx": "npm", "gh ": "gh", "jq": "jq", "uv ": "uv"}

def frontmatter_and_body(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return "", text
    return m.group(1), m.group(2)

def main_file(d):
    for cand in ("SKILL.md",):
        p = os.path.join(d, cand)
        if os.path.isfile(p):
            return p
    files = sorted(os.path.join(b, f) for b, _, fs in os.walk(d) for f in fs)
    md = [f for f in files if f.endswith(".md")]
    return (md or files or [None])[0]

slots_dir = os.path.join(run, "slots")
os.makedirs(os.path.join(run, "facts"), exist_ok=True)
written = 0
for slot in sorted(os.listdir(slots_dir)):
    tsv = os.path.join(slots_dir, slot, "items.tsv")
    if not os.path.isfile(tsv):
        continue
    items = []
    with open(tsv, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            d = os.path.join(slots_dir, slot, row["side"], row["id"])
            mf = main_file(d)
            body_lines = desc_words = 0
            if mf and mf.endswith(".md"):
                text = open(mf, encoding="utf-8", errors="replace").read()
                fm, body = frontmatter_and_body(text)
                body_lines = len(body.splitlines())
                dm = re.search(r"^description:\s*(>-?\s*)?(.*?)(?=^\w+:|\Z)", fm, re.S | re.M)
                if dm:
                    desc_words = len(dm.group(2).split())
            elif mf:
                body_lines = len(open(mf, encoding="utf-8", errors="replace").read().splitlines())
            enforce, deps = [], set()
            for b, _, fs in os.walk(d):
                for fn in fs:
                    p = os.path.join(b, fn)
                    if fn.endswith(CODE):
                        enforce.append(os.path.relpath(p, d))
                        head = open(p, encoding="utf-8", errors="replace").read(4000)
                        for word, dep in DEP_WORDS.items():
                            if word in head:
                                deps.add(dep)
                        if fn.endswith((".js", ".mjs", ".cjs", ".ts")):
                            deps.add("node")
                        if fn.endswith(".py"):
                            deps.add("python3")
            items.append({
                "id": row["id"], "side": row["side"], "type": row["type"],
                "body_lines": body_lines, "description_words": desc_words,
                "load": "always" if row["type"] in ALWAYS else "on-demand",
                "runtime_deps": sorted(deps), "enforcement_files": sorted(enforce),
                "file": os.path.relpath(mf, os.path.join(slots_dir, slot, row["side"])) if mf else "",
            })
    with open(os.path.join(run, "facts", slot + ".json"), "w", encoding="utf-8") as f:
        json.dump({"slot": slot, "items": items}, f, indent=2)
    written += 1
    print("facts/%s.json: %d items" % (slot, len(items)))
if not written:
    sys.exit("make-facts.py: no slots with items.tsv under %s" % slots_dir)
