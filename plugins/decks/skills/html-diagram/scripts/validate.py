#!/usr/bin/env python3
"""
Validate an html-diagram file before handing it over.

Checks the four content slots line up:
  - every edge id referenced by a FLOWS entry exists in the SVG
  - every node data-k referenced by a FLOWS entry exists in the SVG
  - every node has a matching DETAIL entry (and vice-versa)
  - every edge label (data-e) points at a real edge
  - flags edges that no flow ever lights (usually a layout leftover)

Usage:
  python3 validate.py path/to/diagram.html            # cross-ref check only
  python3 validate.py path/to/diagram.html --shots     # also write light/dark/flow PNGs (needs playwright)

Exit code is non-zero if any hard check fails, so it can gate a build.
"""
import re, sys, pathlib

def load(path):
    return pathlib.Path(path).read_text()

def structural_integrity(raw):
    """Catch a truncated or incomplete file - independent of cross-references.
    Truncation usually happens when the whole file is regenerated in one shot and
    the output budget runs out mid-script, so cross-refs can still 'pass'."""
    problems = []
    tail = raw.rstrip()
    if not tail.endswith('</html>'):
        problems.append("file does not end with </html> - likely truncated mid-write")
    if raw.count('<script') != raw.count('</script>'):
        problems.append(f"unbalanced script tags ({raw.count('<script')} open, {raw.count('</script>')} close) - engine block not closed")
    # engine sentinels: these exact strings live at the very end of the frozen engine.
    for sentinel in ["function setFlow(key)", "diagram-theme', dark ? 'dark' : 'light'", "</body>"]:
        if sentinel not in raw:
            problems.append(f"missing engine sentinel: {sentinel!r} - template engine incomplete or edited")
    return problems

def cross_ref(html):
    # ignore commented-out example syntax in the template / leftover comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    edge_ids = set(re.findall(r'class="edge[^"]*"\s+id="([^"]+)"', html))
    # node data-k from SVG only (exclude the JS selector template `${k}`)
    node_ks = set(k for k in re.findall(r'<g class="node[^"]*"\s+data-k="([^"]+)"', html))
    elbl_es = set(re.findall(r'class="elbl"\s+data-e="([^"]+)"', html))

    detail_block = html.split('const DETAIL = {', 1)[1].split('};', 1)[0]
    detail_keys = set(re.findall(r'^\s*"?(\w[\w-]*)"?\s*:\s*{', detail_block, re.M))

    flows_block = html.split('const FLOWS = {', 1)[1].split('\nconst stage', 1)[0]
    flow_edges = set(re.findall(r'"(e-[\w-]+)"', flows_block))
    flow_nodes = set()
    for grp in re.findall(r'nodes:\s*\[([^\]]*)\]', flows_block):
        flow_nodes |= set(re.findall(r'"([\w-]+)"', grp))

    problems, warnings = [], []
    miss_edge = flow_edges - edge_ids
    miss_node = flow_nodes - node_ks
    bad_label = elbl_es - edge_ids
    no_detail = node_ks - detail_keys
    extra_detail = detail_keys - node_ks
    unused_edges = edge_ids - flow_edges

    if miss_edge:    problems.append(f"FLOWS reference edges not in SVG: {sorted(miss_edge)}")
    if miss_node:    problems.append(f"FLOWS reference nodes not in SVG: {sorted(miss_node)}")
    if bad_label:    problems.append(f"Edge labels point at missing edges: {sorted(bad_label)}")
    if no_detail:    problems.append(f"Nodes with no DETAIL entry: {sorted(no_detail)}")
    if extra_detail: warnings.append(f"DETAIL entries with no node (ok if intentional): {sorted(extra_detail)}")
    if unused_edges: warnings.append(f"Edges no flow ever lights (layout leftover?): {sorted(unused_edges)}")

    stats = dict(edges=len(edge_ids), nodes=len(node_ks), labels=len(elbl_es),
                 flows=len(re.findall(r'^\s*"?[\w-]+"?\s*:\s*{', flows_block, re.M)))
    return problems, warnings, stats

def shots(path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  (playwright not installed - skipping screenshots)")
        return
    uri = pathlib.Path(path).resolve().as_uri()
    base = pathlib.Path(path).with_suffix('')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1560, 'height': 900})
        pg.goto(uri); pg.wait_for_timeout(600)
        pg.screenshot(path=f"{base}-light.png")
        # first non-"all" chip, in dark mode
        pg.evaluate("document.documentElement.classList.add('dark')")
        chip = pg.query_selector('.chip[data-flow]:not([data-flow="all"])')
        if chip:
            chip.click(); pg.wait_for_timeout(400)
        pg.screenshot(path=f"{base}-dark-flow.png")
        b.close()
    print(f"  wrote {base}-light.png and {base}-dark-flow.png")

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    path = sys.argv[1]
    html = load(path)

    struct = structural_integrity(html)
    if struct:
        print(f"\n{path}")
        for pr in struct:
            print(f"  FAIL  {pr}")
        print("\n  -> file looks truncated or the engine was altered. Re-build by copying the\n"
              "     template and editing ONLY the content slots - never regenerate the whole file.\n")
        sys.exit(1)

    problems, warnings, stats = cross_ref(html)

    print(f"\n{path}")
    print(f"  {stats['nodes']} nodes · {stats['edges']} edges · {stats['labels']} labels · {stats['flows']} flows\n")
    for w in warnings:
        print(f"  warn  {w}")
    if problems:
        for pr in problems:
            print(f"  FAIL  {pr}")
        print("\n  -> fix the FAILs above before handing over.\n")
    else:
        print("  pass  all cross-references resolve.\n")

    if '--shots' in sys.argv:
        shots(path)

    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
