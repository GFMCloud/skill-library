#!/usr/bin/env bash
# generate-inventory.sh: write every generated page from its source.
#   docs/inventory.md                 one line per skill, from skill frontmatter
#   plugins/<pack>/README.md          the "What's inside" tables, from the
#                                     plugins/<pack>/reader-table.tsv beside it
#   README.md                         the pack catalog and the counts, from
#                                     .claude-plugin/marketplace.json and the tree
#                                     (the pack map's image line and alt text too; the
#                                     image itself is maintainers/scripts/generate-pack-map.py)
# Only the text between a page's generated markers is written; the rest of the page is
# hand-written. Edit the source and run this, never the rendered block.
# Usage: bash maintainers/scripts/generate-inventory.sh          # regenerate
#        bash maintainers/scripts/generate-inventory.sh --check  # exit 1 if anything is stale
# Parsing and rendering live in scripts/skill_meta.py (shared with the validator).
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
exec python3 - "${1:-write}" <<'PY'
import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "scripts"))
from skill_meta import skill_rows, render_inventory, generated_pages

rows = skill_rows("plugins")
pages, problems = generated_pages("plugins")
pages[os.path.join("docs", "inventory.md")] = render_inventory(rows)
for p in problems:
    print(f"PROBLEM: {p}")
if sys.argv[1] == "--check":
    stale = [path for path, text in sorted(pages.items())
             if not os.path.isfile(path) or open(path, encoding="utf-8").read() != text]
    for path in stale:
        print(f"STALE: {path} does not match its source. "
              "Run: bash maintainers/scripts/generate-inventory.sh")
    if stale or problems:
        sys.exit(1)
    print(f"docs/inventory.md is current ({len(rows)} skills); "
          f"{len(pages) - 1} generated page(s) current")
    sys.exit(0)
if problems:
    sys.exit(1)
for path, text in sorted(pages.items()):
    open(path, "w", encoding="utf-8").write(text)
print(f"wrote docs/inventory.md: {len(rows)} skills; {len(pages) - 1} generated page(s)")
PY
