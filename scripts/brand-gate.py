#!/usr/bin/env python3
"""brand-gate.py - keep employer terms and AWS account ids out of this public repo.

The library takes in skills de-branded from a private work repository. A branded
string that reaches any branch here is in public history for good, so this gate runs
before the push (a local pre-commit, commit-msg and pre-push hook, see
scripts/install-hooks.sh) and again in CI as a backstop.

What it checks, in whatever text a mode hands it:
  FAIL  a word on the denylist. The list is stored as SHA-256 hashes
        (maintainers/brand-gate/denylist.sha256) so this public file does not itself
        publish the terms it guards. Hashes of short words can be brute-forced; the
        point is not to advertise them, not to keep them secret.
  FAIL  a 12-digit number standing alone: the shape of an AWS account id.
  WARN  a review flag (maintainers/brand-gate/review-flags.txt, plain words): not
        wrong in itself, but read the surrounding text before it ships.

Matching is on words, case-insensitive: a denied "acme" matches "ACME" and
"acme-blue" but not "acmesoft". Each hyphenated word is also tried as its parts and
runs of parts, joined with and without the hyphen, and two adjacent words are tried
joined ("Ac Me" matches "acme").

Modes (exactly one):
  --staged            added lines and new paths in the index (pre-commit)
  --message FILE      a commit message file (commit-msg)
  --range A..B        added lines, paths and commit messages in a revision range
                      (pre-push, CI)
  --text              stdin, e.g. a PR title and body (CI)
  --tree              every tracked file at HEAD (baseline)
  --hash TERM         print the hash line to append for a new term; never commit
                      the term itself
Exit 0 clean (warnings allowed), 1 on any FAIL, 2 on usage error.
"""
import hashlib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DENY = os.path.join(ROOT, "maintainers", "brand-gate", "denylist.sha256")
FLAGS = os.path.join(ROOT, "maintainers", "brand-gate", "review-flags.txt")
# The gate's own data files hold hashes and plain review words, never a denied term.
SELF = {"maintainers/brand-gate/denylist.sha256", "maintainers/brand-gate/review-flags.txt"}

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
WORD = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
# An AWS account id is 12 digits standing alone. Two shapes that look the same are
# skipped: the last group of a UUID (preceded by a hyphen) and a YYYYMMDDhhmm
# timestamp (`touch -t`). A real account id shaped like a timestamp would slip past;
# that trade keeps the gate quiet on fixtures.
ACCOUNT_ID = re.compile(r"(?<![0-9A-Za-z-])\d{12}(?![0-9A-Za-z-])")
TIMESTAMP = re.compile(r"(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])"
                       r"(?:[01]\d|2[0-3])[0-5]\d")


def h(term):
    return hashlib.sha256(term.strip().lower().encode()).hexdigest()


def load_list(path, hashed):
    if not os.path.isfile(path):
        sys.exit(f"brand-gate: missing {os.path.relpath(path, ROOT)}")
    out = set()
    for line in open(path, encoding="utf-8"):
        line = line.split("#", 1)[0].strip().lower()
        if line:
            out.add(line if hashed else line)
    return out


DENIED = load_list(DENY, True)
FLAG_TERMS = load_list(FLAGS, False)


def candidates(text):
    """Every string a denied term could be hidden as, from one line of text."""
    words = WORD.findall(text.lower())
    for i, w in enumerate(words):
        parts = w.split("-")
        for a in range(len(parts)):
            for b in range(a + 1, len(parts) + 1):
                run = parts[a:b]
                yield "-".join(run)
                if len(run) > 1:
                    yield "".join(run)
        if i + 1 < len(words):
            yield words[i].replace("-", "") + words[i + 1].replace("-", "")


def scan(label, text, fails, warns):
    for n, line in enumerate(text.splitlines(), 1):
        where = f"{label}:{n}" if label else f"line {n}"
        hit = next((c for c in candidates(line) if h(c) in DENIED), None)
        if hit:
            # Say where, never which term: the log of a public CI run is public too.
            fails.append(f"{where}: denylisted word")
        if any(not TIMESTAMP.fullmatch(m) for m in ACCOUNT_ID.findall(line)):
            fails.append(f"{where}: 12-digit number (AWS account id shape)")
        low = line.lower()
        for f in FLAG_TERMS:
            if re.search(r"(?<![a-z0-9])" + re.escape(f) + r"(?![a-z0-9])", low):
                warns.append(f"{where}: review flag '{f}'")


def git(*args):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                       errors="replace")
    if r.returncode != 0:
        sys.exit(f"brand-gate: git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def scan_diff(diff, fails, warns):
    """Added lines and new paths of a unified diff (-U0)."""
    path, lineno = None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            p = line[4:]
            path = p[2:] if p.startswith("b/") else None
            if path and path not in SELF:
                scan(f"(path) {path}", path, fails, warns)
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            lineno = int(m.group(1)) if m else 0
        elif line.startswith("+") and path and path not in SELF:
            scan(f"{path}:{lineno}", line[1:], fails, warns)
            lineno += 1
        elif line.startswith("Binary files") and " and b/" in line:
            p = line.split(" and b/", 1)[1].rsplit(" differ", 1)[0]
            if p not in SELF:
                scan(f"(path) {p}", p, fails, warns)


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    mode, rest = argv[1], argv[2:]
    fails, warns = [], []
    if mode == "--hash" and rest:
        print(h(" ".join(rest))); return 0
    elif mode == "--staged":
        scan_diff(git("diff", "--cached", "-U0", "--no-color", "--diff-filter=ACMR"),
                  fails, warns)
    elif mode == "--message" and rest:
        text = "\n".join(l for l in open(rest[0], encoding="utf-8", errors="replace")
                         .read().splitlines() if not l.startswith("#"))
        scan("commit message", text, fails, warns)
    elif mode == "--range" and rest:
        rng = rest[0]
        # A bare commit (a first push with no common base) is checked whole, against
        # the empty tree.
        diff_args = [rng] if ".." in rng else [EMPTY_TREE, rng]
        scan_diff(git("diff", "-U0", "--no-color", "--diff-filter=ACMR", *diff_args),
                  fails, warns)
        for sha in git("rev-list", rng).split():
            scan(f"commit {sha[:8]} message", git("log", "-1", "--format=%B", sha),
                 fails, warns)
    elif mode == "--text":
        scan("text", sys.stdin.read(), fails, warns)
    elif mode == "--tree":
        for p in git("ls-files").splitlines():
            if p in SELF:
                continue
            scan(f"(path) {p}", p, fails, warns)
            fp = os.path.join(ROOT, p)
            try:
                data = open(fp, "rb").read()
            except OSError:
                continue
            if b"\0" in data[:8000]:
                continue  # binary
            scan(p, data.decode("utf-8", "replace"), fails, warns)
    else:
        print(__doc__); return 2
    for w in warns:
        print(f"WARN {w}")
    for f in fails:
        print(f"FAIL {f}")
    print(f"brand-gate {mode}: {len(fails)} failures, {len(warns)} warnings")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
