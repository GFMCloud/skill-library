#!/usr/bin/env python3
"""Copy a plugin's hook surface into an output dir, for update-installed-plugins.sh to diff.

Usage: plugin-hook-surface.py <plugin dir> <empty out dir>

The surface is everything that decides which hook code runs:
  - every file under hooks/;
  - the "hooks" value in .claude-plugin/plugin.json (inline object, or a path to a file);
  - the top-level `hooks:` block of the YAML frontmatter of every .md under skills/ and
    agents/ (the block only, not the whole file, so editing a skill's body or description
    does not count as a hook change);
  - any existing file those definitions name as ${CLAUDE_PLUGIN_ROOT}/<path>, with or
    without braces, bare or inside quotes;
  - file modes of the copied files.
Scripts that those files call in turn are not followed. A plugin with no hooks yields an
empty surface. Fails closed: exits non-zero if the manifest cannot be read, or if anything
in the surface resolves outside the plugin dir (a symlink or ../ reference), because the
copy would then compare equal while the real hook code differs.
"""
import json, os, re, shutil, sys

src, out = map(os.path.realpath, sys.argv[1:3])
modes = []
escaped = []


def inside(p):
    return p == src or p.startswith(src + os.sep)


def keep(rel):
    p = os.path.realpath(os.path.join(src, rel))
    if not inside(p):
        escaped.append(rel)
    elif os.path.isfile(p):
        r = os.path.relpath(p, src)
        dst = os.path.join(out, "files", r)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(p, dst)
        modes.append("%o %s" % (os.stat(p).st_mode & 0o777, r))


def walk(top):
    for d, _, fs in os.walk(os.path.join(src, top), followlinks=True):
        if not inside(os.path.realpath(d)):
            escaped.append(os.path.relpath(d, src))
        for f in fs:
            yield os.path.relpath(os.path.join(d, f), src)


def frontmatter_hooks(path):
    """The top-level `hooks:` block of a file's YAML frontmatter, or ''."""
    lines = open(path, errors="replace").read().split("\n")
    if not lines or lines[0].strip() != "---":
        return ""
    block, on = [], False
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if re.match(r"hooks\s*:", line):
            on = True
        elif on and line.strip() and not re.match(r"[ \t-]", line):
            on = False
        if on:
            block.append(line)
    return "\n".join(block)


for rel in walk("hooks"):
    keep(rel)

text = ""
manifest = os.path.join(src, ".claude-plugin", "plugin.json")
hooks = json.load(open(manifest)).get("hooks") if os.path.isfile(manifest) else None
if hooks is not None:
    text = json.dumps(hooks, sort_keys=True, indent=1)
    open(os.path.join(out, "plugin-hooks.json"), "w").write(text + "\n")
    for p in [hooks] if isinstance(hooks, str) else hooks if isinstance(hooks, list) else []:
        if isinstance(p, str):
            keep(p)

for top in ("skills", "agents"):
    for rel in walk(top):
        if rel.endswith(".md"):
            block = frontmatter_hooks(os.path.join(src, rel))
            if block:
                dst = os.path.join(out, "frontmatter", rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                open(dst, "w").write(block + "\n")
                text += "\n" + block

for d, _, fs in os.walk(os.path.join(out, "files")):
    text += "".join(open(os.path.join(d, f), errors="replace").read() for f in fs if f.endswith(".json"))
for ref in re.findall(r"\$\{?CLAUDE_PLUGIN_ROOT\}?(?:\\?[\"'])?/([^\s\"'\\)]+)", text):
    keep(ref)

if escaped:
    sys.exit("hook surface resolves outside the plugin dir: " + ", ".join(sorted(set(escaped))))
open(os.path.join(out, "modes.txt"), "w").write("".join(x + "\n" for x in sorted(set(modes))))
