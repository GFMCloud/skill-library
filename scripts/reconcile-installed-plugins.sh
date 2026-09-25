#!/usr/bin/env bash
# reconcile-installed-plugins.sh: read-only report of where each skill-library pack
# stands across the four places a version can live: the install record
# (~/.claude/plugins/installed_plugins.json), the plugin cache on disk, the working
# clone's manifest, and origin/main's manifest. Also reports the clone's git state.
# Added 2026-09-24 (ruled Q-2026-09-24-9): three sessions in one week rebuilt this
# check by hand around update-installed-plugins.sh. Prints, never changes anything.
# Usage: bash scripts/reconcile-installed-plugins.sh [clone dir, default ~/skill-library]
set -uo pipefail
CLONE="${1:-$HOME/skill-library}"
RECORD="$HOME/.claude/plugins/installed_plugins.json"
CACHE="$HOME/.claude/plugins/cache/skill-library"

if [[ ! -f "$RECORD" ]]; then echo "no install record at $RECORD"; exit 2; fi

echo "=== clone: $CLONE"
if git -C "$CLONE" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git -C "$CLONE" fetch -q origin 2>/dev/null || echo "fetch failed (offline?): origin/main may be stale"
  git -C "$CLONE" status -sb | sed -n 1p
  dirty=$(git -C "$CLONE" status --short | wc -l | tr -d ' ')
  echo "dirty files: $dirty"
else
  echo "not a git repo; source and origin columns will be empty"
fi

echo
printf '%-22s %-10s %-10s %-10s %-10s %s\n' pack installed cache source origin note
python3 - "$RECORD" "$CACHE" "$CLONE" <<'PY'
import json, os, subprocess, sys
record, cache, clone = sys.argv[1:4]
plugins = json.load(open(record))["plugins"]

def manifest_version(text):
    try:
        return json.loads(text).get("version") or "-"
    except Exception:
        return "-"

def source_version(pack):
    p = os.path.join(clone, "plugins", pack, ".claude-plugin", "plugin.json")
    return manifest_version(open(p).read()) if os.path.isfile(p) else "-"

def origin_version(pack):
    r = subprocess.run(["git", "-C", clone, "show", f"origin/main:plugins/{pack}/.claude-plugin/plugin.json"],
                       capture_output=True, text=True)
    return manifest_version(r.stdout) if r.returncode == 0 else "-"

def key(v):
    out = []
    for part in str(v).split("."):
        digits = "".join(ch for ch in part if ch.isdigit())
        out.append(int(digits) if digits else -1)
    return tuple(out)

rows = []
for name, entries in sorted(plugins.items()):
    if not name.endswith("@skill-library"):
        continue
    pack = name.split("@")[0]
    inst = entries[0].get("version", "-") if entries else "-"
    path = entries[0].get("installPath", "") if entries else ""
    cache_dir = os.path.join(cache, pack)
    cached = sorted(os.listdir(cache_dir), key=key) if os.path.isdir(cache_dir) else []
    cache_ok = "present" if path and os.path.isdir(path) else "MISSING"
    src, org = source_version(pack), origin_version(pack)
    notes = []
    if cache_ok == "MISSING":
        notes.append("install path missing on disk")
    if org != "-" and inst != "-" and key(inst) < key(org):
        notes.append(f"origin has {org}, installed {inst}: run update-installed-plugins.sh")
    if src != "-" and org != "-" and key(src) > key(org):
        notes.append("clone is ahead of origin (unpushed bump)")
    if src != "-" and org != "-" and key(src) < key(org):
        notes.append("clone is behind origin: pull")
    stale = [v for v in cached if v != inst]
    if len(stale) > 3:
        notes.append(f"{len(stale)} old cache versions")
    rows.append((pack, inst, cache_ok, src, org, "; ".join(notes) or "ok"))
    print(f"{pack:<22} {inst:<10} {cache_ok:<10} {src:<10} {org:<10} {rows[-1][5]}")

# packs cached but no longer installed (retired or renamed)
installed = {n.split("@")[0] for n in plugins if n.endswith("@skill-library")}
if os.path.isdir(cache):
    orphans = sorted(d for d in os.listdir(cache) if os.path.isdir(os.path.join(cache, d)) and d not in installed)
    if orphans:
        print()
        print("cached but not installed (retired or renamed packs): " + ", ".join(orphans))
PY
