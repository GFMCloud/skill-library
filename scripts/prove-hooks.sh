#!/usr/bin/env bash
# prove-hooks.sh - prove every hook in a Claude Code settings file by deliberate failure.
# Usage: bash scripts/prove-hooks.sh [path/to/settings.json]   (default ~/.claude/settings.json)
#
# For every hook command registered in the settings file, run the command twice with the
# stdin JSON Claude Code would send it: a POSITIVE control (the payload the hook exists to
# refuse; it must answer with a deny or block) and a NEGATIVE control (a payload it must
# let through; it must answer with no decision or an allow). Both verdicts are asserted.
# A hook with no fixture, a hook that cannot run, or a settings file with no hooks block
# is RED, never silent: a guard that cannot fire is a failed guard (global rule "a gate or
# validator is trusted only after being proven by deliberate failure"; hstack review
# 2026-09-03 rows 1, 3, 5).
#
# Fixtures live in scripts/prove-hooks.d/<Event>__<matcher>[__<index>].json, where <index>
# counts hooks with that matcher across every entry (two entries matching Bash are #0 and #1):
#   {"positive": <stdin json> | [<stdin json>, ...], "negative": <stdin json> | [...],
#    "env": {<VAR>: <value>} (optional, exported to the hook for every control),
#    "positive_verdict": "deny" (default) | "warn" (a WARN-only hook answers with
#    additionalContext and no permissionDecision; its positives must warn, never deny),
#    "born": "YYYY-MM-DD" (the date the hook was wired; ignored here, required by
#    scripts/replay-hooks.py, the second proof, which measures noise on real history)}
# Every positive must deny and every negative must allow; the first control that
# disagrees names the hook RED.
# Placeholders inside fixture strings are materialized as temp files before the run:
#   {{TMP_EMDASH}}  a file containing an em dash      {{TMP_PLAIN}}  a plain ASCII file
#   {{TMP_ENDASH}}  a file containing an en dash      {{TMP_LARGE}}  a 300 KB ASCII file
#   {{TMP_SUPERSEDED}}  an em-dash file whose name ends .superseded
# A payload written as {"_raw": "<text>"} is sent to the hook as that text, unparsed: the
# way to give a hook stdin that is not valid JSON.
# Project-directory placeholders (FIXTURE data for the session-memory hooks; every handoff
# and state file in them says FIXTURE, and timestamps are relative to the run):
#   {{PROJ_FRESH}}  newest handoff has a claims block written 1 day ago (plus an older one)
#   {{PROJ_STALE}}  claims written 8 days ago      {{PROJ_NONE}}  no handoff at all
#   {{PROJ_MALFORMED}}  a Typed Claims section with no usable block
#   {{PROJ_NOCLAIMS}}  a handoff with no Typed Claims section
#   {{PROJ_SYMLINK}}  the newest handoff is a symlink to a fresh one outside the project,
#       beside an older real one that is still fresh
#   {{PROJ_SECRET}}  a fresh claims block holding a secret-shaped string
#   {{PROJ_STATE}}  a STATE.md                     {{PROJ_STATE_TAKEN}}  STATE.md plus an
#   existing STATE-precompact-FIXTURESTAMP.md      {{PROJ_STATE_SECRET}}  secret-shaped STATE.md
#   {{PROJ_STATE_SYMLINK}}  STATE.md is a symlink to a file outside the project
# Side effects and text: an optional "expect": {"positive": [...], "negative": [...]} holds
# one object per control, in order, asserted after that control's verdict:
#   "stdout_contains" / "stdout_excludes" / "stderr_contains": [<text>, ...]
#   "dir_unchanged": <dir>   the hook created, changed and removed nothing under it
#   "dir_adds_only": {"dir": <dir>, "patterns": [<fnmatch>, ...]}   nothing changed or
#       removed, and the new files are exactly one per pattern
#   "file_contains": {"dir": <dir>, "pattern": <fnmatch>, "text": [<text>, ...]}
# "positive_verdict": "allow" is for a hook whose work is a side effect, not a decision
# (PreCompact); it is accepted only when every positive control has an "expect" object.
# Add a fixture for every new hook in the same commit that adds the hook.
#
# Registry: every wired hook must also have a row in docs/hooks-registry.md (event, matcher,
# script file name). A wired hook with no row is RED; a row with no wiring is a NOTE.
#
# Detector arm vs exemption arm (hstack row 3, the second step, not yet implemented): a
# dead detector UNDER-blocks (positive control passes through), a dead exemption
# OVER-blocks (negative control is denied). The two controls above catch both; a
# mutation arm that corrupts each hook's pattern and expects the positive control to
# start passing would prove the fixtures themselves. Do that when a second hook exists.
#
# Re-verify against your Claude Code version (hstack row 5): the hstack author reports
# that settings keys such as `fallbackModel` and `workflowSizeGuideline` have silently
# dropped the whole hooks block in some versions. This script verifies hooks by side
# effect (the command ran and answered), never by the presence of a config key. If the
# hooks block is missing, the result is RED with that hint.
#
# Re-run after every Claude Code update: 2.1.260 alone fixed four ways a permission rule
# silently failed to apply (parentheses in paths, an uncompilable pattern, zsh substitution
# auto-approval, trailing text), so a hook or rule that was green last week is unproven today.
#
# Exit 0 only when every hook is GREEN. Output is one line per hook plus a summary.
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SETTINGS="${1:-$HOME/.claude/settings.json}"
exec python3 - "$SETTINGS" <<'PY'
import datetime, fnmatch, hashlib, json, os, re, subprocess, sys, tempfile

settings_path = sys.argv[1]
fixture_dir = os.path.join(os.getcwd(), "scripts", "prove-hooks.d")
results = []

def red(label, why): results.append(("RED", label, why))
def green(label, why): results.append(("GREEN", label, why))

try:
    with open(settings_path) as fh:
        settings = json.load(fh)
except Exception as e:  # unreadable settings is a failed guard, not a skipped one
    red("settings", f"cannot read {settings_path}: {e}")
    settings = {}

hooks = settings.get("hooks") if isinstance(settings, dict) else None
if not hooks:
    red("settings", f"no hooks block in {settings_path} (a key that silently disables hooks? see header)")

# docs/hooks-registry.md: a hook wired in settings with no row there is RED.
registry_path = os.path.join(os.getcwd(), "docs", "hooks-registry.md")
registered = set()  # (event, matcher, script file name)
try:
    with open(registry_path, encoding="utf-8") as fh:
        for line in fh:
            # a matcher such as startup|clear is written startup\|clear in the table
            cells = [c.strip().strip("`").replace("\\|", "|")
                     for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            if len(cells) >= 4 and cells[3] in ("blocks", "warns"):
                registered.add((cells[0], cells[1], cells[2]))
except OSError as e:
    red("registry", f"cannot read docs/hooks-registry.md: {e}")
wired = set()

def script_name(command):
    m = re.search(r"[A-Za-z0-9_.-]+\.(?:py|sh|js)\b", command)
    return m.group(0) if m else command.strip()

tmpdir = tempfile.mkdtemp(prefix="prove-hooks-")
def materialize(name, content):
    p = os.path.join(tmpdir, name)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(content)
    return p
placeholders = {
    "{{TMP_EMDASH}}": materialize("emdash.html", "<p>before — after</p>\n"),
    "{{TMP_PLAIN}}": materialize("plain.html", "<p>before and after</p>\n"),
    "{{TMP_ENDASH}}": materialize("endash.html", "<p>2026\u2013 2027</p>\n"),
    "{{TMP_LARGE}}": materialize("large.txt", ("x" * 99 + "\n") * 3072),
    "{{TMP_SUPERSEDED}}": materialize("old.html.superseded", "<p>before \u2014 after</p>\n"),
}
def project(name, files=None, links=None, old=()):
    d = os.path.join(tmpdir, name)
    os.makedirs(d)
    for rel, content in (files or {}).items():
        with open(os.path.join(d, rel), "w", encoding="utf-8") as fh:
            fh.write(content)
    for rel, target in (links or {}).items():
        os.symlink(target, os.path.join(d, rel))
    for rel in old:  # pushed a year back, so it is never the newest by mtime
        t = datetime.datetime.now().timestamp() - 365 * 86400
        os.utime(os.path.join(d, rel), (t, t))
    return d
def handoff(days_old, extra=""):
    written = (datetime.datetime.now().astimezone() - datetime.timedelta(days=days_old)).isoformat(timespec="seconds")
    return ("# Claude Handoff - FIXTURE\n\nWHAT HAPPENED\n- FIXTURE free text that must never be injected\n\n"
            "## Typed Claims\n\n```yaml\nclaims: v1\nwritten_at: " + written + "\ncheckable:\n"
            "  - type: branch\n    claim: FIXTURE claim, work is on fixture-branch\n"
            "    check: git branch --show-current\n    expected: fixture-branch\n" + extra +
            "```\n\nNOTES FOR NEXT CLAUDE\nFIXTURE notes that must never be injected\n")
secret_shaped = "AK" + "IA" + "FIXTUREFIXTURE00"  # FIXTURE; assembled so the repo holds no secret-shaped literal
state_text = "# STATE (FIXTURE)\nphase: 2\nnext: FIXTURE state line\n"
outside_handoff = materialize("outside-handoff.md", handoff(1))
outside_state = materialize("outside-STATE.md", "# STATE (FIXTURE) outside the project\n")
placeholders.update({
    "{{PROJ_FRESH}}": project("proj-fresh", {"handoff-fixture-new.md": handoff(1),
                                             "handoff-fixture-old.md": handoff(30).replace("fixture-branch", "old-branch")},
                              old=["handoff-fixture-old.md"]),
    "{{PROJ_STALE}}": project("proj-stale", {"handoff-fixture.md": handoff(8)}),
    "{{PROJ_NONE}}": project("proj-none", {"README.md": "FIXTURE project with no handoff\n"}),
    "{{PROJ_MALFORMED}}": project("proj-malformed", {"handoff-fixture.md": "# Claude Handoff - FIXTURE\n\n## Typed Claims\n\nFIXTURE: the block was never written\n"}),
    "{{PROJ_NOCLAIMS}}": project("proj-noclaims", {"handoff-fixture.md": "# Claude Handoff - FIXTURE\n\nFIXTURE free text that must never be injected\n"}),
    "{{PROJ_SYMLINK}}": project("proj-symlink", {"handoff-real.md": handoff(2).replace("fixture-branch", "real-branch")},
                                links={"handoff-link.md": outside_handoff}, old=["handoff-real.md"]),
    "{{PROJ_SECRET}}": project("proj-secret", {"handoff-fixture.md": handoff(1, "  - type: count\n    claim: FIXTURE key is " + secret_shaped + "\n    check: true\n    expected: x\n")}),
    "{{PROJ_STATE}}": project("proj-state", {"STATE.md": state_text}),
    "{{PROJ_STATE_TAKEN}}": project("proj-state-taken", {"STATE.md": state_text,
                                    "STATE-precompact-FIXTURESTAMP.md": "FIXTURE existing snapshot, must survive byte for byte\n"}),
    "{{PROJ_STATE_SECRET}}": project("proj-state-secret", {"STATE.md": state_text + "key: " + secret_shaped + "\n"}),
    "{{PROJ_STATE_SYMLINK}}": project("proj-state-symlink", links={"STATE.md": outside_state}),
})

def snapshot(d):
    snap = {}
    for root, dirs, names in os.walk(d):
        for n in names:
            p = os.path.join(root, n)
            rel = os.path.relpath(p, d)
            snap[rel] = ("link", os.readlink(p)) if os.path.islink(p) else ("file", hashlib.sha256(open(p, "rb").read()).hexdigest())
    return snap

def check_expect(exp, before, stdout, stderr):
    """Failures of one control's "expect" object, as a list of strings."""
    bad = []
    for t in exp.get("stdout_contains", []):
        if t not in stdout: bad.append(f"stdout lacks {t!r}")
    for t in exp.get("stdout_excludes", []):
        if t in stdout: bad.append(f"stdout holds {t!r}")
    for t in exp.get("stderr_contains", []):
        if t not in stderr: bad.append(f"stderr lacks {t!r}")
    for key in ("dir_unchanged", "dir_adds_only"):
        if key not in exp:
            continue
        d = exp[key] if key == "dir_unchanged" else exp[key]["dir"]
        patterns = [] if key == "dir_unchanged" else list(exp[key]["patterns"])
        after = snapshot(d)
        for rel, was in before[d].items():
            if after.get(rel) != was: bad.append(f"{rel} was changed or removed")
        new = sorted(set(after) - set(before[d]))
        unmatched = [n for n in new if not any(fnmatch.fnmatch(n, pt) for pt in patterns)]
        if unmatched: bad.append(f"unexpected new file(s): {unmatched}")
        if len(new) != len(patterns): bad.append(f"{len(new)} new file(s), expected {len(patterns)}")
    if "file_contains" in exp:
        fc = exp["file_contains"]
        hits = [n for n in os.listdir(fc["dir"]) if fnmatch.fnmatch(n, fc["pattern"])]
        body = "".join(open(os.path.join(fc["dir"], n), encoding="utf-8").read() for n in hits)
        for t in fc["text"]:
            if t not in body: bad.append(f"{fc['pattern']} lacks {t!r}")
    return bad

def fill(obj):
    if isinstance(obj, dict) and set(obj) == {"_raw"}:
        return obj["_raw"]  # sent as-is: stdin that is not valid JSON
    s = json.dumps(obj)
    for k, v in placeholders.items():
        s = s.replace(k, v)
    return s

def verdict(stdout):
    """deny | warn | allow | error. A hook allows by staying silent or by saying so; a
    WARN-only hook answers with additionalContext and no permissionDecision."""
    text = stdout.strip()
    if not text:
        return "allow"
    try:
        d = json.loads(text)
    except json.JSONDecodeError:
        return "error"
    hso = d.get("hookSpecificOutput", {}) if isinstance(d, dict) else {}
    if hso.get("permissionDecision") == "deny" or d.get("decision") == "block":
        return "deny"
    if hso.get("permissionDecision") in ("allow", "ask") or d.get("decision") == "approve":
        return "allow"
    if hso.get("additionalContext") and not hso.get("permissionDecision"):
        return "warn"
    return "error"

def run(cmd, payload, env=None):
    try:
        p = subprocess.run(cmd, shell=True, input=payload, capture_output=True, text=True, timeout=30,
                           env={**os.environ, **(env or {})})
    except subprocess.TimeoutExpired:
        return "error", "timeout after 30s", "", ""
    if p.returncode not in (0, 2):  # 2 is Claude Code's blocking exit code
        return "error", f"exit {p.returncode}: {p.stderr.strip()[:200]}", p.stdout, p.stderr
    return verdict(p.stdout), p.stdout.strip()[:200], p.stdout, p.stderr

seen = {}  # (event, matcher) -> running hook index across entries, so two entries with the
           # same matcher never share a fixture
for event, entries in (hooks or {}).items():
    if not isinstance(entries, list):
        continue
    for entry in entries:
        matcher = str(entry.get("matcher", "*"))
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", matcher)
        for hook in entry.get("hooks", []):
            j = seen.get((event, safe), 0)
            seen[(event, safe)] = j + 1
            label = f"{event} matcher={matcher} #{j}"
            if hook.get("type") != "command" or not hook.get("command"):
                red(label, "not a command hook; nothing to prove")
                continue
            key = (event, matcher, script_name(hook["command"]))
            wired.add(key)
            if key not in registered:
                red(f"{label} registry", f"unlisted: {key[2]} is wired in settings but has no row in docs/hooks-registry.md")
            candidates = [f"{event}__{safe}__{j}.json", f"{event}__{safe}.json"]
            fixture = next((os.path.join(fixture_dir, c) for c in candidates
                            if os.path.exists(os.path.join(fixture_dir, c))), None)
            if not fixture:
                red(label, f"unproven: no fixture ({' or '.join(candidates)} in scripts/prove-hooks.d/)")
                continue
            try:
                fx = json.load(open(fixture))
                pos, neg = fx["positive"], fx["negative"]
                pos = pos if isinstance(pos, list) else [pos]
                neg = neg if isinstance(neg, list) else [neg]
                env = {k: json.loads(fill(v)) for k, v in (fx.get("env") or {}).items()}
                want = fx.get("positive_verdict", "deny")  # "warn" for a WARN-only hook
                if want not in ("deny", "warn", "allow"):
                    raise ValueError(f"positive_verdict must be deny, warn or allow, not {want}")
                expect = json.loads(fill(fx.get("expect") or {}))
                pexp = expect.get("positive") or [None] * len(pos)
                nexp = expect.get("negative") or [None] * len(neg)
                if len(pexp) != len(pos) or len(nexp) != len(neg):
                    raise ValueError("expect needs one entry per control, in order")
                if want == "allow" and not all(pexp):
                    raise ValueError("positive_verdict allow proves nothing without an expect object per positive")
            except Exception as e:
                red(label, f"bad fixture {os.path.basename(fixture)}: {e}")
                continue
            why = []
            def dirs_of(exp):
                ds = [exp[k] if k == "dir_unchanged" else exp[k]["dir"] for k in ("dir_unchanged", "dir_adds_only") if k in (exp or {})]
                return {d: snapshot(d) for d in ds}
            for k, payload in enumerate(pos):
                before = dirs_of(pexp[k])
                pv, pout, so, se = run(hook["command"], fill(payload), env)
                if pv != want:
                    why.append(f"positive #{k} was {pv}, expected {want} (dead detector under-blocks): {pout or '<empty>'}")
                why += [f"positive #{k}: {b}" for b in check_expect(pexp[k] or {}, before, so, se)]
            for k, payload in enumerate(neg):
                before = dirs_of(nexp[k])
                nv, nout, so, se = run(hook["command"], fill(payload), env)
                if nv != "allow":
                    why.append(f"negative #{k} was {nv} (dead exemption over-blocks): {nout or '<empty>'}")
                why += [f"negative #{k}: {b}" for b in check_expect(nexp[k] or {}, before, so, se)]
            if not why:
                green(label, f"{len(pos)} positive={want}, {len(neg)} negative=allow (fixture {os.path.basename(fixture)})")
            else:
                red(label, "; ".join(why))

if wired and wired <= registered:
    green("registry", f"all {len(wired)} wired hook(s) are listed in docs/hooks-registry.md")

reds = [r for r in results if r[0] == "RED"]
for status, label, why in results:
    print(f"{status}  {label}  {why}")
for event, matcher, name in sorted(registered - wired):
    print(f"NOTE  registry lists {event} matcher={matcher} {name}, which {settings_path} does not wire")
print(f"\n{len(results)} hook check(s): {len(results) - len(reds)} green, {len(reds)} red")
sys.exit(1 if reds or not results else 0)
PY
