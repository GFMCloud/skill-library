"""Fixtures for scripts/ingest.py: a stand-in `claude` on PATH, a throwaway repo and vault (fixture_env.py).
Run with the readwise-links venv: bash fixtures/run-fixtures.sh"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixture_env import ART, PROJECT, build, doc, git, put, run  # noqa: E402

NOTE = """# Opus leads, Sonnet builds: a three-role agent team

## Key points

- The post recommends an Opus lead with Sonnet teammates. [post] "Run an Opus lead that plans and merges"
- A read-only reviewer checks at fixed points. [post] "A read-only Fable reviewer checks the work at three checkpoints"
- Teams are switched on by one setting. [linked page 1] "enabled with a single setting in the project configuration file"

## Rationale and limits

One post and one linked page; no measurements.

## Dropped

- The claim that teams cut token cost by 60 percent.
"""
TITLE = "Opus leads, Sonnet builds: a three-role agent team"
KNOWLEDGE = "Knowledge/Opus leads, Sonnet builds a three-role agent team.md"


def retrieval(note=TITLE, section="post", quote="Run an Opus lead that plans and merges"):
    return "```json\n" + json.dumps([
        {"question": 1, "note": note, "section": section, "quote": quote},
        {"question": 2, "note": None, "section": None, "quote": None},
        {"question": 3, "note": None, "section": None, "quote": None}]) + "\n```\n"


@pytest.fixture
def env(tmp_path):
    e = build(tmp_path)
    stub(e, NOTE, retrieval())
    return e


def stub(e, note, retr):
    put(e["tmp"] / "note.reply", note)
    put(e["tmp"] / "retrieval.reply", retr)
    b = e["bin"]
    put(b / "claude", f"""#!/bin/bash
p=$(cat); echo call >> {e['tmp']}/calls.log
if grep -q "You run a retrieval test" <<< "$p"; then cat {e['tmp']}/retrieval.reply; else cat {e['tmp']}/note.reply; fi
""").chmod(0o755)


def calls(e):
    f = e["tmp"] / "calls.log"
    return len(f.read_text().splitlines()) if f.exists() else 0


def commits(e):
    return int(git(e["vault"], "rev-list", "--count", "HEAD"))


def test_a_new_item_is_written_linked_and_committed(env):
    r = run(env)
    assert r.returncode == 0, r.stdout + r.stderr
    v = env["vault"]
    note = (v / KNOWLEDGE).read_text()
    rec = next((v / "Sources").glob("Saved link 30 *.md"))
    assert f"[[Sources/{rec.stem}|post]]" in note and f"[[Sources/{rec.stem}|linked page 1]]" in note
    assert "Run an Opus lead" not in note and "60 percent" not in note  # quotes removed, dropped point gone
    assert f"source_path: {env['art']}" in note and "draft_blob:" in note and "status: draft" in note
    assert "`linked page 2`" not in rec.read_text()  # not captured, so not citable
    proj = (v / "Projects" / f"{PROJECT}.md").read_text()
    assert f"- [[Knowledge/{Path(KNOWLEDGE).stem}]]" in proj and f"- [[Sources/{rec.stem}]]" in proj
    assert "No note answers yet: When is Opus worth its cost?" in proj
    assert f"- [[Projects/{PROJECT}]]" in (v / "Home.md").read_text()
    rt = (v / "Retrieval test.md").read_text()
    assert f"## {PROJECT} (" in rt and "Pass for recorded content" in rt and rt.count("Gap: no note") == 2
    assert commits(env) == 2 and git(v, "status", "--porcelain") == ""
    assert "60 percent" in (env["logs"] / "dropped.md").read_text()
    assert "retrieval: 3 question(s), 1 pass, 2 gap" in r.stdout


def test_a_second_run_on_the_same_batch_writes_nothing(env):
    assert run(env).returncode == 0
    n_calls, n_commits = calls(env), commits(env)
    r = run(env)
    assert r.returncode == 3 and "skipped #30" in r.stdout and "Nothing to do." in r.stdout
    assert calls(env) == n_calls and commits(env) == n_commits and git(env["vault"], "status", "--porcelain") == ""


def test_a_seeded_matching_note_is_updated_not_duplicated(env):
    v = env["vault"]
    put(v / "Knowledge" / "Old title.md", doc({"type": "knowledge", "project": "agent-practice",
                                               "source_path": str(env["art"])}, "# Old title\n\nOld text.\n"))
    git(v, "add", "-A"); git(v, "commit", "-q", "-m", "seed")
    r = run(env)
    assert r.returncode == 0, r.stdout + r.stderr
    assert sorted(p.name for p in (v / "Knowledge").iterdir()) == ["Old title.md"]
    assert TITLE in (v / "Knowledge" / "Old title.md").read_text() and "updated #30" in r.stdout


def test_a_dirty_vault_stops(env):
    put(env["vault"] / "scratch.md", "x")
    r = run(env)
    assert r.returncode == 2 and "STOP:" in r.stdout and "uncommitted" in r.stdout and calls(env) == 0


def test_an_item_that_is_not_the_committed_copy_on_origin_stops(env):
    p = env["repo"] / "vault-ready" / "30-team-on-x" / "note.md"
    p.write_text(p.read_text() + "\nlocal edit\n")
    r = run(env)
    assert r.returncode == 2 and "not the committed copy on origin/main" in r.stdout and calls(env) == 0


def test_a_missing_project_map_stops(env):
    r = run(env, "--project", "No such project")
    assert r.returncode == 2 and "no project map" in r.stdout


@pytest.mark.parametrize("bad, expect", [
    (NOTE.replace("[linked page 1]", "[linked page 2]"), "cites linked page 2"),
    (NOTE.replace('"Run an Opus lead that plans and merges"', '"Run a Haiku lead that plans and merges"'),
     "quote not found in the cited section"),
    (NOTE.replace("No measurements.", "No <img src=x> measurements.").replace("no measurements", "<script>x</script>"),
     "no HTML outside code"),
    (NOTE.replace(' "Run an Opus lead that plans and merges"', ""), "key point 1: must end with"),
])
def test_a_bad_note_is_refused_and_nothing_is_written(env, bad, expect):
    stub(env, bad, retrieval())
    r = run(env)
    assert r.returncode == 1 and "FAILED #30" in r.stdout, r.stdout
    assert expect in (env["logs"] / "note-30-2.check").read_text()
    assert calls(env) == 2 and commits(env) == 1 and not (env["vault"] / "Knowledge").exists()


@pytest.mark.parametrize("retr, expect", [
    (retrieval(note="Some other note"), "no note in this project is titled as given"),
    (retrieval(section="linked page 2"), "does not cite linked page 2"),
    (retrieval(quote="Run a Haiku lead that plans and merges"), "quote not found"),
])
def test_a_failed_retrieval_test_stops_before_anything_is_written(env, retr, expect):
    stub(env, NOTE, retr)
    r = run(env)
    assert r.returncode == 2 and "STOP: the retrieval test failed" in r.stdout and expect in r.stdout, r.stdout
    assert commits(env) == 1 and git(env["vault"], "status", "--porcelain") == ""


def test_dry_run_plans_without_calling_the_model(env):
    r = run(env, "--dry-run")
    assert r.returncode == 0 and "new #30" in r.stdout and calls(env) == 0 and commits(env) == 1


def test_sections_and_quotes_normalize_whitespace_and_curly_quotes(tmp_path):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    import ingest
    import briefing
    e = build(tmp_path)
    secs = ingest.article_sections(e["art"].read_text(), briefing.split_front)
    assert sorted(secs) == ["linked page 1", "post"] and ART  # page 2 was not captured
    assert ingest.quote_ok("Run an   Opus lead\nthat plans and merges", secs["post"]) is None
    assert ingest.quote_ok("too short quote", secs["post"]) == "quote has 3 words (5-40)"
