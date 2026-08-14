#!/usr/bin/env bash
# validate-skills.sh — reference implementation of docs/validator-spec.md
# Usage: bash scripts/validate-skills.sh [plugins/<name>]
#   STRICT=1        warnings also cause exit 1
#   STALE_MONTHS=6  staleness threshold for W1
# Checks every plugins/*/skills/*/ skill (or just the given plugin's).
set -uo pipefail
# Resolve the repo root from this script's own location, never from the cwd:
# a cwd-derived root inside any other repo found zero skills and exited 0 (A-11).
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 - "${1:-plugins}" <<'PY'
import os, re, sys, datetime

root = sys.argv[1]
STRICT = os.environ.get("STRICT", "0") == "1"
STALE_MONTHS = int(os.environ.get("STALE_MONTHS", "6"))
fails, warns = [], []

def parse_frontmatter(text):
    """Minimal YAML-subset parser: scalars, one nested map level, >-/|/> blocks."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    data, ctx = {}, None  # ctx = name of open nested map
    block_key, block_lines, block_ctx, block_indent = None, [], None, -1
    for line in text[3:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if block_key is not None:
            if indent > block_indent:
                block_lines.append(line.strip())
                continue
            tgt = data[block_ctx] if block_ctx else data
            tgt[block_key] = " ".join(block_lines)
            block_key, block_lines, block_ctx = None, [], None
        m = re.match(r"^(\s*)([\w.-]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(2), m.group(3).strip()
        if indent == 0:
            ctx = None
        if val in (">-", ">", "|", "|-"):
            block_key, block_ctx, block_indent = key, ctx, indent
        elif val == "":
            if indent == 0:
                data[key], ctx = {}, key
            else:
                (data[ctx] if ctx else data)[key] = ""
        else:
            val = val.strip("'\"")
            if indent == 0:
                data[key] = val
            elif ctx:
                data[ctx][key] = val
    if block_key is not None:
        tgt = data[block_ctx] if block_ctx else data
        tgt[block_key] = " ".join(block_lines)
    return data, text[end + 4:]

skill_dirs = sorted(
    os.path.join(p, s)
    for pat in ([root] if root != "plugins" else [root])
    for plug in (sorted(os.listdir(pat)) if os.path.isdir(pat) else [])
    for p in [os.path.join(pat, plug, "skills")] if os.path.isdir(p)
    for s in sorted(os.listdir(p)) if os.path.isdir(os.path.join(p, s))
)
if root != "plugins":  # single-plugin arg: plugins/<name>
    sp = os.path.join(root, "skills")
    skill_dirs = sorted(
        os.path.join(sp, s) for s in (os.listdir(sp) if os.path.isdir(sp) else [])
        if os.path.isdir(os.path.join(sp, s)))

names = {}
for d in skill_dirs:
    rel, dirname = d, os.path.basename(d)
    plugin = d.split(os.sep)[1] if len(d.split(os.sep)) > 1 else "?"
    sk = os.path.join(d, "SKILL.md")
    if not os.path.isfile(sk):
        fails.append(f"F1 {rel}: no SKILL.md"); continue
    text = open(sk, encoding="utf-8", errors="replace").read()
    parsed = parse_frontmatter(text)
    if parsed is None:
        fails.append(f"F2 {rel}: no parseable frontmatter block"); continue
    fm, body = parsed
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    name, desc = str(fm.get("name", "")).strip(), str(fm.get("description", "")).strip()
    if not name:
        fails.append(f"F3 {rel}: missing name")
    if len(desc) < 40:
        fails.append(f"F4 {rel}: description missing or <40 chars ({len(desc)})")
    if name and name != dirname:
        fails.append(f"F5 {rel}: name '{name}' != directory '{dirname}'")
    if name:
        if name in names:
            fails.append(f"F6 {rel}: duplicate name '{name}' (also {names[name]})")
        else:
            names[name] = rel
    nlines = len(body.splitlines())
    if nlines > 500:
        fails.append(f"F7 {rel}: body {nlines} lines (>500)")
    for link in re.findall(r"\]\(([^)#][^)]*)\)", text):
        if re.match(r"^[a-z]+:", link):
            continue
        if not os.path.exists(os.path.join(d, link.split("#")[0])):
            fails.append(f"F8 {rel}: broken link '{link}'")
    mat = str(meta.get("maturity", "")).strip()
    if mat not in ("incubator", "stable", "deprecated"):
        fails.append(f"F9 {rel}: metadata.maturity missing/invalid ('{mat}')")
    if mat == "stable":
        ver, rev = str(meta.get("version", "")), str(meta.get("reviewed", ""))
        if not re.match(r"^\d+\.\d+\.\d+$", ver):
            fails.append(f"F10 {rel}: stable without semver version ('{ver}')")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", rev):
            fails.append(f"F10 {rel}: stable without ISO reviewed date ('{rev}')")
        else:
            age = (datetime.date.today()
                   - datetime.date.fromisoformat(rev)).days
            if age > STALE_MONTHS * 30:
                warns.append(f"W1 {rel}: reviewed {rev} is >{STALE_MONTHS} months old")
    if mat == "deprecated" and not str(meta.get("supersedes", "")).strip():
        fails.append(f"F11 {rel}: deprecated without metadata.supersedes")
    if plugin == "_incubator" and mat == "stable":
        fails.append(f"F12 {rel}: _incubator skill marked stable")
    if str(fm.get("disable-model-invocation", "")).lower() == "true":
        warns.append(f"W2 {rel}: disable-model-invocation set — slash-only intended?")
    for base, _, files in os.walk(d):
        for f in files:
            fp = os.path.join(base, f)
            if os.path.getsize(fp) > 100_000:
                warns.append(f"W3 {rel}: large file {os.path.relpath(fp, d)} "
                             f"({os.path.getsize(fp)//1024} KB)")

# F11 second pass: supersedes must name an existing skill
for d in skill_dirs:
    sk = os.path.join(d, "SKILL.md")
    if not os.path.isfile(sk):
        continue
    parsed = parse_frontmatter(open(sk, encoding="utf-8", errors="replace").read())
    if not parsed:
        continue
    meta = parsed[0].get("metadata") or {}
    sup = str(meta.get("supersedes", "")).strip() if isinstance(meta, dict) else ""
    if sup and sup not in names:
        fails.append(f"F11 {d}: supersedes '{sup}' names no existing skill")

if not skill_dirs:
    fails.append("F0: zero skills found; a green run that checked nothing is a false green")
for f in fails: print(f"FAIL {f}")
for w in warns: print(f"WARN {w}")
print(f"\n{len(skill_dirs)} skills checked: {len(fails)} failures, {len(warns)} warnings")
sys.exit(1 if fails or (STRICT and warns) else 0)
PY
