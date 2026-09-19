#!/usr/bin/env python3
"""
Scan a project folder for secrets before it becomes a git repo.

The whole point of this script is the rule from the repo standard: git history is
forever, so a secret that gets committed stays recoverable even after you delete the
file. The only safe time to catch a secret is BEFORE the first commit. That's here.

It splits findings into two buckets, because they need different handling:

  - WHOLE_FILE: the entire file is a secret container (.env, credentials, *.pem,
    *.tfvars, id_rsa, etc.). Safe to add to .gitignore and move on - the file was
    never meant to be tracked.

  - EMBEDDED: a secret-looking value is sitting INSIDE a file you'd otherwise want
    to keep (an AWS key pasted into app.py, a token in a config you need tracked).
    You can't gitignore the whole file without losing real code, so this is a hard
    stop - a human has to look, pull the secret out, and rotate it.

Usage:
    python scan_secrets.py /path/to/folder
    python scan_secrets.py /path/to/folder --json   # machine-readable output

Exit codes:
    0  clean, or only whole-file secrets found (gitignore-and-continue is safe)
    2  at least one EMBEDDED secret found (caller must hard-stop)
"""

import argparse
import json
import os
import re
import sys

# Files/dirs we never bother scanning - either binary or already-ignored noise.
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "env", "__pycache__",
             ".terraform", "dist", "build", ".cache", ".idea", ".vscode",
             ".pytest_cache", ".mypy_cache"}

# Extensions whose whole existence implies a secret container.
WHOLE_FILE_SECRET_EXT = {".pem", ".key", ".p12", ".pfx", ".tfvars"}

# Exact filenames (or basenames) that are whole-file secret containers.
WHOLE_FILE_SECRET_NAMES = {"credentials", "id_rsa", "id_ed25519", "aws.json",
                           "secrets.json"}

# Anything matching these basename patterns is a whole-file secret container.
WHOLE_FILE_SECRET_PATTERNS = [
    re.compile(r"^\.env(\..+)?$"),      # .env, .env.local, .env.production
    re.compile(r".*\.secret$"),
    re.compile(r".*_secret.*"),
]

# Files we should NOT treat as whole-file secrets even if names look close.
WHOLE_FILE_ALLOW = {".env.example", "example.tfvars", ".env.sample"}

# Patterns for secrets EMBEDDED in otherwise-keepable text files. These are tuned
# to be specific so we don't cry wolf on every "password" string in a comment.
EMBEDDED_PATTERNS = [
    ("AWS access key id", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("AWS secret access key",
     re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*['\"]?[A-Za-z0-9/+=]{40}['\"]?")),
    ("Generic API key assignment",
     re.compile(r"(?i)\b(api[_-]?key|apikey|secret[_-]?key|access[_-]?token|auth[_-]?token)\b\s*[=:]\s*['\"][A-Za-z0-9_\-]{16,}['\"]")),
    ("Bearer token", re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-\.]{20,}")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Password assignment",
     re.compile(r"(?i)\b(password|passwd|pwd)\b\s*[=:]\s*['\"][^'\"]{6,}['\"]")),
    ("DB connection string with creds",
     re.compile(r"(?i)(postgres|postgresql|mysql|mongodb(\+srv)?|redis)://[^:\s]+:[^@\s]+@")),
]

# Placeholder values we should ignore inside embedded matches - these are obviously
# fake and live in .env.example files and docs on purpose.
PLACEHOLDER_HINTS = re.compile(
    r"(?i)(your[_-]?|example|placeholder|changeme|xxx+|<.*>|\bdummy\b|\bfake\b|\btest[_-]?key\b|\.\.\.)"
)

TEXT_EXT_HINT = {".txt", ".md", ".py", ".js", ".ts", ".jsx", ".tsx", ".json",
                 ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".sh",
                 ".env", ".tf", ".html", ".xml", ".properties", ".rb", ".go",
                 ".java", ".php", ".cs", ".sql", ""}


def basename_is_whole_file_secret(name):
    low = name.lower()
    if low in WHOLE_FILE_ALLOW:
        return False
    ext = os.path.splitext(name)[1].lower()
    if ext in WHOLE_FILE_SECRET_EXT:
        return True
    if low in WHOLE_FILE_SECRET_NAMES:
        return True
    for pat in WHOLE_FILE_SECRET_PATTERNS:
        if pat.match(low):
            return True
    return False


def looks_like_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in TEXT_EXT_HINT:
        return True
    # Fall back to a quick binary sniff.
    try:
        with open(path, "rb") as f:
            chunk = f.read(2048)
        if b"\x00" in chunk:
            return False
        return True
    except OSError:
        return False


def scan_embedded(path):
    findings = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for lineno, line in enumerate(f, 1):
                if len(line) > 4000:  # skip minified blobs
                    continue
                for label, pat in EMBEDDED_PATTERNS:
                    m = pat.search(line)
                    if not m:
                        continue
                    snippet = m.group(0)
                    # Ignore obvious placeholders so .env.example etc. stays quiet.
                    if PLACEHOLDER_HINTS.search(line):
                        continue
                    findings.append({
                        "line": lineno,
                        "type": label,
                        "snippet": (snippet[:60] + "...") if len(snippet) > 60 else snippet,
                    })
    except OSError:
        pass
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(args.folder)
    whole_file = []
    embedded = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            if basename_is_whole_file_secret(fn):
                whole_file.append({"file": rel})
                continue
            if looks_like_text(full):
                hits = scan_embedded(full)
                for h in hits:
                    h["file"] = rel
                    embedded.append(h)

    result = {
        "folder": root,
        "whole_file_secrets": whole_file,
        "embedded_secrets": embedded,
        "clean": not whole_file and not embedded,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["clean"]:
            print("CLEAN - no secrets detected.")
        if whole_file:
            print("\nWHOLE-FILE SECRETS (safe to .gitignore and continue):")
            for w in whole_file:
                print(f"  - {w['file']}")
        if embedded:
            print("\nEMBEDDED SECRETS (HARD STOP - human must review + rotate):")
            for e in embedded:
                print(f"  - {e['file']}:{e['line']}  [{e['type']}]  {e['snippet']}")

    # Exit 2 only when there's an embedded secret - that's the case the caller
    # must hard-stop on. Whole-file-only findings are exit 0 (gitignore-and-go).
    sys.exit(2 if embedded else 0)


if __name__ == "__main__":
    main()
