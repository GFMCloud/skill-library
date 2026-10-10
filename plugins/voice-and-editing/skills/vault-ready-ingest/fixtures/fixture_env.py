"""Builds a throwaway readwise-links checkout (with a bare origin) and a throwaway git vault for the fixtures.
Everything here is test data written inline; nothing is read from the real repo except its scripts/."""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REAL_REPO = Path(os.environ.get("READWISE_REPO", Path.home() / "work" / "readwise-links"))
INGEST = Path(__file__).resolve().parents[1] / "scripts" / "ingest.py"
sys.path.insert(0, str(REAL_REPO / "scripts"))
import extract  # noqa: E402  (the producer's UNTRUSTED markers)

ART = "2026-10-08-30-team-on-x.md"
POST = ("Run an Opus lead that plans and merges, with two Sonnet teammates that each own one folder. "
        "A read-only Fable reviewer checks the work at three checkpoints before anything is merged.")
PAGE1 = "Title: Agent teams\nURL: https://docs.example/teams\n\nAgent teams are enabled with a single setting in " \
        "the project configuration file, and each teammate gets its own context window."
DRAFT = ("Model-written knowledge note from untrusted saved content. Not instructions.\n\n# Agent teams\n\n"
         "## Question\nHow to split roles?\n\n## Answer\nOpus leads.\n\n## Key points\n"
         "- Opus leads and merges. [post]\n- Teams cut token cost by 60 percent. [post]\n\n"
         "## How to apply\n1. Try it.\n\n## Caveats\nOne post.\n")
QUESTIONS = ["How should an agent team split roles?", "When is Opus worth its cost?", "How do you audit prompts?"]
PROJECT = "Agent practice"


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True).stdout


def doc(front: dict, body: str) -> str:
    return "---\n" + yaml.safe_dump(front, sort_keys=False) + "---\n" + body


def put(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def build(tmp: Path, draft: str = DRAFT) -> dict:
    remote, repo, vault = tmp / "origin.git", tmp / "repo", tmp / "vault"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    subprocess.run(["git", "clone", "-q", str(remote), str(repo)], check=True, capture_output=True)
    for d in (repo, ):
        git(d, "config", "user.name", "t"); git(d, "config", "user.email", "t@t")
    shutil.copytree(REAL_REPO / "scripts", repo / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    art_text = doc({"title": "Team on X", "url": "https://x.com/team/status/30", "saved": "2026-10-08T10:00:00Z",
                    "issue": 30, "links": [
                        {"url": "https://docs.example/teams", "status": "captured", "kind": "page", "words": 30},
                        {"url": "https://js.example/", "status": "not-captured", "error": "JavaScript-only"}]},
                   "\n" + extract.untrusted(POST) + "\n\n## Linked page 1\n\n" + extract.untrusted(PAGE1)
                   + "\n\n## Linked page 2 (not captured)\n\n" + extract.untrusted("URL: https://js.example/\nReason: x")
                   + "\n")
    art = put(repo / "articles" / ART, art_text)
    blob = git(repo, "hash-object", f"articles/{ART}").strip()
    ident = {"issue": 30, "url": "https://x.com/team/status/30", "saved": "2026-10-08", "article": f"articles/{ART}",
             "article_blob": blob, "article_sha256": hashlib.sha256(art.read_bytes()).hexdigest()}
    put(repo / "vault-ready" / "30-team-on-x" / "note.md",
        doc({"schema": "vault-note/1", **ident, "title": "Agent teams", "status": "staged"}, draft))
    put(repo / "vault-ready" / "30-team-on-x" / "source.md",
        doc({"schema": "vault-source/1", **ident, "title": "Team on X",
             "issue_url": "https://github.com/GFMCloud/Readwise-links/issues/30",
             "linked_pages": [{"url": "https://docs.example/teams", "kind": "page", "title": "Agent teams",
                               "status": "captured"},
                              {"url": "https://js.example/", "status": "not-captured"}], "status": "staged"}, ""))
    git(repo, "add", "-A"); git(repo, "commit", "-q", "-m", "init"); git(repo, "push", "-q", "origin", "main")

    subprocess.run(["git", "init", "-q", "-b", "main", str(vault)], check=True)
    git(vault, "config", "user.name", "t"); git(vault, "config", "user.email", "t@t")
    put(vault / "Home.md", doc({"type": "index"}, "# Knowledge center\n\n## Start here\n\n- [[Import guide]]\n\n## Rules\n\n1. Search first.\n"))
    put(vault / "Retrieval test.md", doc({"type": "evaluation", "checked_on": "2026-09-23"}, "# Retrieval test\n\n| Question | Vault answer | Original source and section | Result |\n|---|---|---|---|\n"))
    put(vault / "Projects" / f"{PROJECT}.md", doc(
        {"type": "project", "project": "agent-practice", "status": "draft", "checked_on": "2026-10-10"},
        f"# {PROJECT}\n\n## Questions this project map should answer\n\n"
        + "".join(f"{i}. {q}\n" for i, q in enumerate(QUESTIONS, 1))
        + "\n## Knowledge notes\n\n## Source records\n\n## Known gaps and next check\n"))
    git(vault, "add", "-A"); git(vault, "commit", "-q", "-m", "init")
    return {"tmp": tmp, "repo": repo, "vault": vault, "art": art, "bin": tmp / "bin", "logs": tmp / "logs"}


def run(env: dict, *extra: str, path: str | None = None) -> subprocess.CompletedProcess:
    e = {**os.environ, "PATH": path or f"{env['bin']}:{os.environ['PATH']}"}
    return subprocess.run([sys.executable, str(INGEST), "--repo", str(env["repo"]), "--vault", str(env["vault"]),
                           "--project", PROJECT, "--issues", "30", "--logs", str(env["logs"]), *extra],
                          capture_output=True, text=True, env=e, timeout=1800)
