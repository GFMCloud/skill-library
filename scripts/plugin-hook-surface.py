#!/usr/bin/env python3
"""Copy a plugin's hook surface into an output dir, for update-installed-plugins.sh to diff.

Usage: plugin-hook-surface.py <plugin dir> <empty out dir>

The surface is everything that decides which hook code runs: every file under hooks/,
the "hooks" value in .claude-plugin/plugin.json (inline object, or a path to a file),
and any existing file a hook definition names as ${CLAUDE_PLUGIN_ROOT}/<path>. File
modes are recorded too. Scripts those files call in turn are not followed. A plugin
with no hooks yields an empty surface. Exits non-zero if the manifest cannot be read.
"""
import json, os, re, shutil, sys

src, out = map(os.path.realpath, sys.argv[1:3])
modes = []


def keep(rel):
    p = os.path.realpath(os.path.join(src, rel))
    if p.startswith(src + os.sep) and os.path.isfile(p):
        r = os.path.relpath(p, src)
        dst = os.path.join(out, "files", r)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(p, dst)
        modes.append("%o %s" % (os.stat(p).st_mode & 0o777, r))


for d, _, fs in os.walk(os.path.join(src, "hooks"), followlinks=True):
    for f in fs:
        keep(os.path.relpath(os.path.join(d, f), src))

text = ""
manifest = os.path.join(src, ".claude-plugin", "plugin.json")
hooks = json.load(open(manifest)).get("hooks") if os.path.isfile(manifest) else None
if hooks is not None:
    text = json.dumps(hooks, sort_keys=True, indent=1)
    open(os.path.join(out, "plugin-hooks.json"), "w").write(text + "\n")
    for p in [hooks] if isinstance(hooks, str) else hooks if isinstance(hooks, list) else []:
        if isinstance(p, str):
            keep(p)

for d, _, fs in os.walk(os.path.join(out, "files")):
    text += "".join(open(os.path.join(d, f), errors="replace").read() for f in fs if f.endswith(".json"))
for ref in re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\s\"'\\)]+)", text):
    keep(ref)

open(os.path.join(out, "modes.txt"), "w").write("".join(x + "\n" for x in sorted(set(modes))))
