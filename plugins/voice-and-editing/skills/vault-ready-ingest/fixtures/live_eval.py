"""Live eval: the real tool-less model on a throwaway repo and vault. The draft carries one planted key point the
article never makes ("Teams cut token cost by 60 percent"). Pass: the run commits, the planted point is absent from the
knowledge note, and it is listed in dropped.md. Costs two to four Sonnet calls.
Run: READWISE_REPO=~/work/readwise-links ~/work/readwise-links/.venv/bin/python fixtures/live_eval.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixture_env import build, git, run  # noqa: E402

env = build(Path(tempfile.mkdtemp(prefix="vault-ingest-eval-")))
r = run(env)
print(r.stdout, r.stderr, sep="")
notes = list((env["vault"] / "Knowledge").glob("*.md")) if (env["vault"] / "Knowledge").exists() else []
dropped = (env["logs"] / "dropped.md").read_text() if (env["logs"] / "dropped.md").exists() else ""
checks = {
    "run committed (exit 0)": r.returncode == 0,
    "one knowledge note": len(notes) == 1,
    "planted point absent from the note": bool(notes) and "60 percent" not in notes[0].read_text(),
    "planted point listed in dropped.md": "60" in dropped,
    "vault clean after the commit": git(env["vault"], "status", "--porcelain") == "",
}
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'} {name}")
print(f"logs: {env['logs']}")
sys.exit(0 if all(checks.values()) else 1)
