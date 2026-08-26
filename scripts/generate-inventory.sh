#!/usr/bin/env bash
# generate-inventory.sh — write docs/inventory.md from skill frontmatter.
# Usage: bash scripts/generate-inventory.sh          # regenerate docs/inventory.md
#        bash scripts/generate-inventory.sh --check  # exit 1 if the committed file is stale
# Parsing and rendering live in scripts/skill_meta.py (shared with the validator).
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 - "${1:-write}" <<'PY'
import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "scripts"))
from skill_meta import skill_rows, render_inventory

rows = skill_rows("plugins")
text = render_inventory(rows)
path = os.path.join("docs", "inventory.md")
if sys.argv[1] == "--check":
    cur = open(path, encoding="utf-8").read() if os.path.isfile(path) else None
    if cur != text:
        print("STALE: docs/inventory.md does not match the tree. "
              "Run: bash scripts/generate-inventory.sh")
        sys.exit(1)
    print(f"docs/inventory.md is current ({len(rows)} skills)")
    sys.exit(0)
open(path, "w", encoding="utf-8").write(text)
print(f"wrote {path}: {len(rows)} skills")
PY
