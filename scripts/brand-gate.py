#!/usr/bin/env python3
"""brand-gate.py - keep employer terms and AWS account ids out of this public repo.

The library takes in skills de-branded from a private work repository. A branded
string that reaches any branch here is in public history for good, so this gate runs
before the push (a local pre-commit, commit-msg and pre-push hook, see
scripts/install-hooks.sh) and again in CI as a backstop.

What it checks, in whatever text a mode hands it:
  FAIL  a word on the denylist. The list is stored as SHA-256 hashes
        (maintainers/brand-gate/denylist.sha256) so this public file does not spell out
        the terms it guards. Hashes of short words can be brute-forced; the
        point is not to advertise them, not to keep them secret.
  FAIL  a 12-digit number standing alone, or in the console's NNNN-NNNN-NNNN form: the
        shape of an AWS account id.
  WARN  a denied term buried inside a longer lowercase token ("acmelogo"); read it.
  WARN  every added binary file, by name: its text is scanned (the XML parts of a
        zip or Office file, the printable strings of anything else), but a picture of
        a logo is not text, so a human looks at it.
  WARN  a review flag (maintainers/brand-gate/review-flags.txt, plain words): not
        wrong in itself, but read the surrounding text before it ships.

Matching is on words, case-insensitive, after Unicode NFKC folding: a denied "acme"
matches "ACME", "acme-blue", "acmeBlue" and "AcmeLogo.svg" (case changes split words).
Each hyphenated word is also tried as its parts and runs of parts, joined with and
without the hyphen, and two adjacent words are tried joined ("Ac Me" matches "acme").
An all-lowercase glued token ("acmesoft") is only a WARN, from the substring pass.

The gate's own data files are checked too: every non-comment line of the denylist
must be a 64-hex hash, the list must not be empty (either is exit 2, so a mistake
fails closed), and the comments in both files are scanned like any other text.

Modes (exactly one):
  --staged            added lines and new paths in the index (pre-commit)
  --message FILE      a commit message file (commit-msg)
  --range A..B        added lines, paths and commit messages in a revision range;
                      the diff runs from the merge-base (pre-push, CI)
  --text              stdin, e.g. a PR title and body (CI)
  --tree              every tracked file at HEAD (baseline)
  --hash TERM         print the hash line to append for a new term; never commit
                      the term itself
Exit 0 clean (warnings allowed), 1 on any FAIL, 2 on usage error or a broken list.
"""
import hashlib, io, os, re, subprocess, sys, unicodedata, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DENY = os.path.join(ROOT, "maintainers", "brand-gate", "denylist.sha256")
FLAGS = os.path.join(ROOT, "maintainers", "brand-gate", "review-flags.txt")
# The gate's own data files hold hashes and plain review words, never a denied term.
SELF = {"maintainers/brand-gate/denylist.sha256", "maintainers/brand-gate/review-flags.txt"}

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
WORD = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
CASE_BREAK = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
SUBSTR_MIN = 5    # substring pass: shorter terms would hit ordinary words
SUBSTR_MAX = 64   # tokens longer than this (hashes, base64) are not words
# An AWS account id is 12 digits standing alone, where a hyphen counts as a boundary
# (the CDK bucket cdk-<qualifier>-assets-<id>-<region>), or the console's dashed
# NNNN-NNNN-NNNN form. Two shapes that look the same are skipped: a UUID, removed
# from the line before matching, and a YYYYMMDDhhmm timestamp (`touch -t`). A real
# account id shaped like a timestamp would slip past; that trade keeps the gate quiet
# on fixtures.
UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
ACCOUNT_ID = re.compile(r"(?<![0-9A-Za-z])\d{12}(?![0-9A-Za-z])")
DASHED_ID = re.compile(r"(?<![0-9A-Za-z-])\d{4}-\d{4}-\d{4}(?![0-9A-Za-z-])")
HEX64 = re.compile(r"[0-9a-f]{64}")
MAX_BLOB = 50 * 1024 * 1024
TIMESTAMP = re.compile(r"(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])"
                       r"(?:[01]\d|2[0-3])[0-5]\d")


def h(term):
    return hashlib.sha256(term.strip().lower().encode()).hexdigest()


def fail_closed(msg):
    print(f"brand-gate: {msg}", file=sys.stderr)
    sys.exit(2)


def load_list(path, hashed):
    rel = os.path.relpath(path, ROOT)
    if not os.path.isfile(path):
        fail_closed(f"missing {rel}")
    out = set()
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.split("#", 1)[0].strip().lower()
        if not line:
            continue
        if hashed and not HEX64.fullmatch(line):
            # Most likely the term itself, appended instead of its hash: refuse to run
            # rather than accept a line that can never match.
            fail_closed(f"{rel}:{n} is not a 64-hex SHA-256 line; add terms with --hash")
        out.add(line)
    if hashed and not out:
        fail_closed(f"{rel} has no hashes; an empty denylist would pass everything")
    return out


DENIED = load_list(DENY, True)
FLAG_TERMS = load_list(FLAGS, False)


def fold(text):
    """NFKC-fold, then split case changes, then lowercase: acmeBlue -> acme blue."""
    return CASE_BREAK.sub(" ", unicodedata.normalize("NFKC", text)).lower()


def candidates(text):
    """Every string a denied term could be hidden as, from one line of text."""
    words = WORD.findall(fold(text))
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


def buried(line):
    """True when a denied term sits inside a longer glued lowercase token."""
    for tok in set(WORD.findall(unicodedata.normalize("NFKC", line).lower())):
        tok = tok.replace("-", "")
        if not SUBSTR_MIN < len(tok) <= SUBSTR_MAX:
            continue
        for a in range(len(tok) - SUBSTR_MIN + 1):
            for b in range(a + SUBSTR_MIN, len(tok) + 1):
                if h(tok[a:b]) in DENIED:
                    return True
    return False


def scan(label, text, fails, warns, first=1):
    for n, line in enumerate(text.splitlines(), first):
        where = f"{label}:{n}" if label else f"line {n}"
        # Say where, never which term: the log of a public CI run is public too.
        if any(h(c) in DENIED for c in candidates(line)):
            fails.append(f"{where}: denylisted word")
        elif buried(line):
            warns.append(f"{where}: denylisted word inside a longer token; read it")
        bare = UUID.sub(" ", line)
        if (any(not TIMESTAMP.fullmatch(m) for m in ACCOUNT_ID.findall(bare))
                or DASHED_ID.search(bare)):
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


def git_bytes(*args):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    if r.returncode != 0:
        sys.exit(f"brand-gate: git {' '.join(args)} failed: "
                 f"{r.stderr.decode(errors='replace').strip()}")
    return r.stdout


STRINGS = re.compile(rb"[\x20-\x7e]{4,}")


def scan_blob(label, data, fails, warns, depth=0):
    """A binary file's text: each member of a zip (Office files are zipped XML), or
    the printable strings of anything else. Always WARNs, naming the file."""
    if depth == 0:
        warns.append(f"{label}: binary file; its text was scanned, look at the rest")
    if len(data) > MAX_BLOB:
        fails.append(f"{label}: binary over {MAX_BLOB // 2**20} MB, not scanned")
        return
    if data[:4] == b"PK\x03\x04" and depth < 2:
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for info in z.infolist():
                    scan(f"{label}!{info.filename} (name)", info.filename, fails, warns)
                    part = z.read(info)
                    if b"\0" in part[:8000]:
                        scan_blob(f"{label}!{info.filename}", part, fails, warns, depth + 1)
                    else:
                        text = part.decode("utf-8", "replace")
                        # Tags become spaces so a word split across runs is rejoined
                        # by the adjacent-word pass.
                        scan(f"{label}!{info.filename}",
                             re.sub(r"<[^>]*>", " ", text), fails, warns)
                        scan(f"{label}!{info.filename}", text, fails, warns)
            return
        except (zipfile.BadZipFile, RuntimeError, NotImplementedError):
            fails.append(f"{label}: zip that can't be read (encrypted or damaged)")
            return
    scan(label, "\n".join(m.decode() for m in STRINGS.findall(data)), fails, warns)


def comments_only(text):
    """The gate's own data files: hash and flag lines are data, comments are text."""
    return "\n".join(l.split("#", 1)[1] if "#" in l else "" for l in text.splitlines())


def scan_diff(diff, fails, warns, blob):
    """Added lines and new paths of a unified diff (-U0). `blob(path)` returns the
    new content of a binary file."""
    path, lineno = None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            p = line[4:]
            path = p[2:] if p.startswith("b/") else None
            if path:
                scan(f"(path) {path}", path, fails, warns)
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            lineno = int(m.group(1)) if m else 0
        elif line.startswith("+") and path:
            text = comments_only(line[1:]) if path in SELF else line[1:]
            scan(path, text, fails, warns, lineno)
            lineno += 1
        elif line.startswith("Binary files") and " and b/" in line:
            p = line.split(" and b/", 1)[1].rsplit(" differ", 1)[0]
            scan(f"(path) {p}", p, fails, warns)
            scan_blob(p, blob(p), fails, warns)


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    mode, rest = argv[1], argv[2:]
    fails, warns = [], []
    if mode == "--hash" and rest:
        print(h(" ".join(rest))); return 0
    elif mode == "--staged":
        scan_diff(git("diff", "--cached", "-U0", "--no-color", "--diff-filter=ACMR"),
                  fails, warns, lambda p: git_bytes("show", f":{p}"))
    elif mode == "--message" and rest:
        text = "\n".join(l for l in open(rest[0], encoding="utf-8", errors="replace")
                         .read().splitlines() if not l.startswith("#"))
        scan("commit message", text, fails, warns)
    elif mode == "--range" and rest:
        rng = rest[0]
        # A bare commit (a first push with no common base) is checked whole, against
        # the empty tree. A.. B diffs from their merge-base: what the range adds.
        if ".." in rng:
            a, b = rng.replace("...", "..").split("..", 1)
            diff_args = [f"{a}...{b}"]
        else:
            b, diff_args = rng, [EMPTY_TREE, rng]
        scan_diff(git("diff", "-U0", "--no-color", "--diff-filter=ACMR", *diff_args),
                  fails, warns, lambda p: git_bytes("show", f"{b}:{p}"))
        for sha in git("rev-list", rng).split():
            scan(f"commit {sha[:8]} message", git("log", "-1", "--format=%B", sha),
                 fails, warns)
    elif mode == "--text":
        scan("text", sys.stdin.read(), fails, warns)
    elif mode == "--tree":
        for p in git("ls-files").splitlines():
            scan(f"(path) {p}", p, fails, warns)
            fp = os.path.join(ROOT, p)
            try:
                data = open(fp, "rb").read()
            except OSError:
                continue
            if b"\0" in data[:8000]:
                scan_blob(p, data, fails, warns)
                continue
            text = data.decode("utf-8", "replace")
            scan(p, comments_only(text) if p in SELF else text, fails, warns)
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
