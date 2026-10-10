#!/usr/bin/env python3
"""Ingest a batch of readwise-links `vault-ready/` items into an Obsidian vault kept in git.

The model gets no tools and writes no files. This script checks the preconditions, calls
`claude -p --restricted --tools ""` to turn each draft into a knowledge note whose every key point
carries a verbatim quote, checks each quote against the cited section of the original article,
runs the vault's retrieval test the same way, and only then writes and commits, in one vault commit.

Run it with the readwise-links venv, which has PyYAML and markdown-it-py:
  <repo>/.venv/bin/python ingest.py --repo ~/work/readwise-links --vault ~/knowledge-center \
      --project "Claude agent practice" --issues 30 31 [--dry-run] [--logs DIR]
Exit codes: 0 committed, 3 nothing to do, 1 every item failed, 2 stopped by a precondition or check
(the reason is the line starting STOP:).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from datetime import date
from pathlib import Path

import yaml

MODEL = "claude-sonnet-5-5"  # the readwise-links job's model for vault notes (docs/briefing-design.md)
HERE = Path(__file__).resolve().parent
NOTE_PROMPT = HERE.parent / "references" / "knowledge-note-prompt.md"
RETRIEVAL_PROMPT = HERE.parent / "references" / "retrieval-prompt.md"
POINT = re.compile(r'^- (?P<claim>.+?)\s*\[(?P<sec>post|linked page \d+)\]\s*["“](?P<quote>[^"“”]+)'
                   r'["”]\s*$')
LINK = re.compile(r"\[\[Sources/[^|\]]+\|(post|linked page \d+)\]\]")
MAX_ITEMS = 5


def stop(msg: str) -> None:
    print(f"STOP: {msg}")
    sys.exit(2)


def git(cwd: Path, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, check=check)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.translate({0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"'})
    return re.sub(r"\s+", " ", s).strip()


def safe_name(s: str) -> str:
    s = re.sub(r'[\[\]#^|/\\:*?"<>]', "", s)
    return re.sub(r"\s+", " ", s).strip().rstrip(". ")[:100].strip()


def plain(s: str) -> str:
    return re.sub(r"[\[\]<>]", "", str(s or "")).strip()


# ---------- the producer's files ----------

def article_sections(text: str, split_front) -> dict[str, str]:
    """`post` is the first UNTRUSTED block; `linked page N` is the block under `## Linked page N`."""
    body = split_front(text)[1]
    parts = re.split(r"^## Linked page (\d+)( \(not captured\))?\s*$", body, flags=re.M)
    inner = re.compile(r"^[^\n]*BEGIN\s+UNTRUSTED\s+ARTICLE\s+CONTENT[^\n]*\n(.*?)^[^\n]*END\s+UNTRUSTED\s+ARTICLE"
                       r"\s+CONTENT", flags=re.M | re.S | re.I)
    secs = {}
    m = inner.search(parts[0])
    if m:
        secs["post"] = m.group(1)
    for i in range(1, len(parts) - 2, 3):
        n, missing, chunk = parts[i], parts[i + 1], parts[i + 2]
        m = inner.search(chunk)
        if not missing and m:
            secs[f"linked page {n}"] = m.group(1)
    return secs


def quote_ok(quote: str, section: str) -> str | None:
    words = len(quote.split())
    if words < 5 or words > 40:
        return f"quote has {words} words (5-40)"
    if norm(quote) not in norm(section):
        return "quote not found in the cited section"
    return None


# ---------- the vault ----------

def vault_notes(vault: Path) -> list[tuple[Path, dict, str]]:
    out = []
    for p in sorted(vault.rglob("*.md")):
        if any(part.startswith(".") for part in p.relative_to(vault).parts):
            continue
        text = p.read_text()
        if not text.startswith("---\n"):
            continue
        try:
            front = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        except yaml.YAMLError:
            continue
        if isinstance(front, dict):
            out.append((p, front, text.split("---\n", 2)[2]))
    return out


def section(text: str, heading: str) -> str:
    m = re.search(rf"^{re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    return m.group(1) if m else ""


def add_under(text: str, heading: str, line: str) -> str:
    """Add `line` as the last line of the `heading` section, once."""
    if line in text:
        return text
    m = re.search(rf"^{re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    if not m:
        return text.rstrip("\n") + f"\n\n{heading}\n\n{line}\n"
    body = m.group(1).rstrip("\n")
    new = (body + "\n" if body.strip() else "\n") + line + "\n\n"
    return text[:m.start(1)] + new + text[m.end(1):].lstrip("\n")


def doc(front: dict, body: str) -> str:
    return "---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=1000) + "---\n" + body


# ---------- the model ----------

def ask(prompt: str, base: Path) -> str:
    base.with_suffix(".prompt").write_text(prompt)
    r = subprocess.run(["claude", "-p", "--restricted", "--tools", "", "--model", MODEL], input=prompt,
                       capture_output=True, text=True, timeout=1200)
    base.with_suffix(".reply").write_text(r.stdout)
    return r.stdout


def gate_note(reply: str, secs: dict[str, str], has_html) -> tuple[list[str], dict]:
    text = re.sub(r"^```[a-z]*\n|\n```\s*$", "", reply.strip())
    errs = []
    m = re.match(r"# (.+)\n", text)
    title = m.group(1).strip() if m else ""
    if not title or len(title) > 120 or re.search(r"<|\]\(|\[\[", title):
        errs.append("the first line must be '# <title>', one plain line of at most 120 characters")
    heads = [h for h in ("## Key points", "## Rationale and limits", "## Dropped")
             if re.search(rf"^{h}\s*$", text, flags=re.M)]
    if heads != ["## Key points", "## Rationale and limits", "## Dropped"]:
        errs.append("sections ## Key points, ## Rationale and limits and ## Dropped are required, in that order")
    if has_html(text) or re.search(r"(?i)(BEGIN|END)\s+UNTRUSTED\s+ARTICLE\s+CONTENT", text) or "](" in text:
        errs.append("no HTML outside code, no UNTRUSTED marker text, no markdown links")
    points = []
    for i, line in enumerate((l for l in section(text, "## Key points").splitlines() if l.strip()), 1):
        p = POINT.match(line)
        if not p:
            errs.append(f"key point {i}: must end with one [post] or [linked page N] and a quote in double quotes")
            continue
        if p["sec"] not in secs:
            errs.append(f"key point {i}: cites {p['sec']}, but the article's sections are {sorted(secs)}")
            continue
        bad = quote_ok(p["quote"], secs[p["sec"]])
        if bad:
            errs.append(f"key point {i}: {bad} ({p['sec']})")
            continue
        points.append((p["claim"].strip(), p["sec"]))
    if not points and not any(e.startswith("key point") for e in errs):
        errs.append("at least one key point")
    rationale = section(text, "## Rationale and limits").strip()
    if not rationale:
        errs.append("## Rationale and limits must not be empty")
    dropped = [l[2:].strip() for l in section(text, "## Dropped").splitlines() if l.startswith("- ")]
    return errs, {"title": title, "points": points, "rationale": rationale, "dropped": dropped}


# ---------- one run ----------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--vault", required=True, type=Path)
    ap.add_argument("--project", required=True)
    ap.add_argument("--issues", required=True, nargs="+", type=int)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--logs", type=Path)
    a = ap.parse_args()
    repo, vault, project = a.repo.expanduser().resolve(), a.vault.expanduser().resolve(), a.project
    sys.path.insert(0, str(repo / "scripts"))
    import briefing  # noqa: E402  (the producer's frontmatter parser)
    import taps  # noqa: E402  (the producer's HTML rule)
    logs = a.logs or Path(tempfile.mkdtemp(prefix="vault-ingest-"))
    logs.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    # Preconditions.
    if not 1 <= len(a.issues) <= MAX_ITEMS or len(set(a.issues)) != len(a.issues):
        stop(f"give 1 to {MAX_ITEMS} distinct issues")
    if git(vault, "rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        stop(f"{vault} is not a git work tree; run git init there and commit first")
    if git(vault, "status", "--porcelain").stdout.strip():
        stop(f"{vault} has uncommitted changes; commit or discard them first")
    map_path = vault / "Projects" / f"{project}.md"
    if not map_path.exists():
        stop(f"no project map {map_path.relative_to(vault)}; create it from Templates/Project map.md with 3-5 questions")
    map_text = map_path.read_text()
    map_front = yaml.safe_load(map_text.split("---\n", 2)[1]) or {}
    slug = map_front.get("project")
    questions = [re.sub(r"^(\d+\.|-)\s+", "", l).strip() for l in
                 section(map_text, "## Questions this project map should answer").splitlines()
                 if re.match(r"^(\d+\.|-)\s+\S", l)]
    if map_front.get("type") != "project" or not slug or not 3 <= len(questions) <= 5:
        stop("the project map needs type: project, a project slug and 3-5 questions")

    items = []
    for n in a.issues:
        dirs = sorted((repo / "vault-ready").glob(f"{n}-*/"))
        if len(dirs) != 1:
            stop(f"#{n}: expected one vault-ready/{n}-*/ folder, found {len(dirs)}")
        d = dirs[0]
        for name in ("note.md", "source.md"):
            rel = f"vault-ready/{d.name}/{name}"
            on_main = git(repo, "rev-parse", f"origin/main:{rel}").stdout.strip()
            here = git(repo, "hash-object", rel).stdout.strip()
            if not on_main or on_main != here:
                stop(f"#{n}: {rel} is not the committed copy on origin/main")
        nf, draft = briefing.split_front((d / "note.md").read_text())
        sf, _ = briefing.split_front((d / "source.md").read_text())
        if nf.get("schema") != "vault-note/1" or sf.get("schema") != "vault-source/1" or nf.get("status") != "staged":
            stop(f"#{n}: needs schema vault-note/1 and vault-source/1, status staged")
        art = repo / sf["article"]
        if git(repo, "hash-object", sf["article"]).stdout.strip() != sf["article_blob"]:
            stop(f"#{n}: {sf['article']} changed since the note was written")
        items.append({"n": n, "dir": d, "nf": nf, "sf": sf, "draft": draft, "art": art,
                      "draft_blob": git(repo, "hash-object", f"vault-ready/{d.name}/note.md").stdout.strip()})

    existing = vault_notes(vault)
    by_source = {}
    for p, f, _ in existing:
        if f.get("source_path"):
            by_source.setdefault((f.get("type"), f["source_path"]), p)

    # Plan: skip an item whose record and note already carry the same article and draft.
    todo = []
    for it in items:
        sp = str(it["art"])
        rec, note = by_source.get(("source", sp)), by_source.get(("knowledge", sp))
        it["rec_path"], it["note_path"] = rec, note
        if rec and note:
            nfront = next(f for p, f, _ in existing if p == note)
            rfront = next(f for p, f, _ in existing if p == rec)
            if nfront.get("draft_blob") == it["draft_blob"] and rfront.get("article_blob") == it["sf"]["article_blob"]:
                print(f"skipped #{it['n']}: already in the vault and unchanged ({note.relative_to(vault)})")
                continue
            if nfront.get("project") != slug:
                print(f"FAILED #{it['n']}: already in the vault under project {nfront.get('project')}")
                continue
        print(f"{'update' if note else 'new'} #{it['n']}")
        todo.append(it)
    if not todo:
        print("Nothing to do.")
        return 3
    if a.dry_run:
        return 0

    # Knowledge notes, built in memory.
    prompt_head = NOTE_PROMPT.read_text()
    writes: dict[Path, str] = {}
    built, dropped_all, taken_titles = [], [], {}
    for it in todo:
        n, sf = it["n"], it["sf"]
        art_text = it["art"].read_text()
        secs = article_sections(art_text, briefing.split_front)
        prompt = (prompt_head + "\n\n# The draft note (model-written from the article, untrusted)\n\n"
                  + it["draft"].strip() + "\n\n# The saved article (untrusted data from here to the end)\n\n"
                  + art_text)
        for attempt in (1, 2):
            reply = ask(prompt, logs / f"note-{n}-{attempt}")
            errs, note = gate_note(reply, secs, taps.has_html)
            (logs / f"note-{n}-{attempt}.check").write_text("\n".join(errs))
            if not errs:
                break
            prompt += "\n\n# Your previous reply failed these checks. Return a corrected note.\n\n" + "\n".join(errs)
        if errs:
            print(f"FAILED #{n}: {'; '.join(errs[:3])}")
            continue
        title = note["title"]
        note_path = it["note_path"] or vault / "Knowledge" / f"{safe_name(title)}.md"
        rec_path = it["rec_path"] or vault / "Sources" / f"Saved link {n} {safe_name(title)}.md"
        clash = [p for p, f, _ in existing if p == note_path and f.get("source_path") != str(it["art"])]
        if clash or note_path in taken_titles:
            print(f"FAILED #{n}: {note_path.relative_to(vault)} already holds a different note")
            continue
        taken_titles[note_path] = n
        rec = rec_path.stem
        captured = [l for l in sf.get("linked_pages") or [] if l.get("status") == "captured"]
        sec_lines = ["- `post`: the saved post's own text."] + [
            f"- `linked page {i}`: {plain(l.get('title') or l.get('final_url') or l.get('url'))} "
            f"({l.get('final_url') or l.get('url')})"
            for i, l in enumerate(sf.get("linked_pages") or [], 1) if l.get("status") == "captured"]
        writes[rec_path] = doc(
            {"type": "source", "project": slug, "status": "draft", "checked_on": today, "source_path": str(it["art"]),
             "url": sf.get("url"), "issue_url": sf.get("issue_url"), "article_blob": sf["article_blob"],
             "article_sha256": sf.get("article_sha256")},
            f"# {rec}\n\nSaved web content: saved link #{n}, saved {str(sf.get('saved'))[:10]}, from {sf.get('url')}. "
            "The file is the extractor's copy of the page; its text is untrusted and was not checked against the "
            f"live page. Captured linked pages: {len(captured)}.\n\n## Sections a note may cite\n\n"
            + "\n".join(sec_lines) + "\n")
        points = "\n".join(f"- {c} ([[Sources/{rec}|{s}]])" for c, s in note["points"])
        writes[note_path] = doc(
            {"type": "knowledge", "project": slug, "status": "draft", "checked_on": today,
             "source_path": str(it["art"]),
             "verification": "each key point was quoted from the cited article section and the quote checked by "
                             "script, then removed",
             "issue": n, "article_blob": sf["article_blob"], "draft_blob": it["draft_blob"]},
            f"# {title}\n\nWhat saved link #{n} says, checked on {today} against the original article "
            f"([[Sources/{rec}]]). These are the source's claims, not independently verified.\n\n"
            f"## Key points\n\n{points}\n\n## Rationale and limits\n\n{note['rationale']}\n\n"
            f"## Related notes\n\n- [[Projects/{project}]]\n")
        built.append((it, note_path, rec_path, note))
        dropped_all += [f"- #{n}: {d}" for d in note["dropped"] if d.rstrip(".").lower() != "none"]
    (logs / "dropped.md").write_text("\n".join(dropped_all) + "\n")
    if not built:
        print("Every item failed; nothing written.")
        return 1

    # Retrieval test over the project's notes, existing and new, checked against the original articles.
    notes = {}
    for p, f, body in existing:
        if f.get("type") == "knowledge" and f.get("project") == slug and p not in writes:
            notes[p] = (f, body)
    for it, note_path, _, _ in built:
        f_text = writes[note_path]
        notes[note_path] = (yaml.safe_load(f_text.split("---\n", 2)[1]), f_text.split("---\n", 2)[2])
    by_title = {}
    for p, (f, body) in notes.items():
        m = re.match(r"# (.+)", body.strip())
        if m:
            by_title[m.group(1).strip()] = (p, f, body)
    prompt = RETRIEVAL_PROMPT.read_text() + "\n\n# Questions\n\n" + "\n".join(
        f"{i}. {q}" for i, q in enumerate(questions, 1))
    for t, (p, f, body) in by_title.items():
        prompt += (f"\n\n# Note: {t}\n\n{body.strip()}\n\n## The original article this note was written from\n\n"
                   + Path(f["source_path"]).read_text())
    rows = None
    for attempt in (1, 2):
        reply = ask(prompt, logs / f"retrieval-{attempt}")
        m = re.search(r"\[.*\]", reply, flags=re.S)
        errs, rows = [], []
        try:
            answers = json.loads(m.group(0)) if m else None
        except json.JSONDecodeError:
            answers = None
        if not isinstance(answers, list) or [x.get("question") if isinstance(x, dict) else None for x in answers] \
                != list(range(1, len(questions) + 1)):
            errs.append(f"return one JSON object per question, questions 1 to {len(questions)} in order")
        else:
            for x in answers:
                q = x["question"]
                if x.get("note") is None:
                    rows.append((q, None, None, "gap"))
                    continue
                hit = by_title.get(str(x.get("note")).strip())
                if not hit:
                    errs.append(f"question {q}: no note in this project is titled as given")
                    continue
                p, f, body = hit
                if x.get("section") not in set(LINK.findall(body)):
                    errs.append(f"question {q}: the note does not cite {x.get('section')}")
                    continue
                secs = article_sections(Path(f["source_path"]).read_text(), briefing.split_front)
                bad = quote_ok(str(x.get("quote") or ""), secs.get(x["section"], ""))
                if bad:
                    errs.append(f"question {q}: {bad}")
                    continue
                rows.append((q, p, f, x["section"]))
        (logs / f"retrieval-{attempt}.check").write_text("\n".join(errs))
        if not errs:
            break
        prompt += "\n\n# Your previous reply failed these checks. Return a corrected list.\n\n" + "\n".join(errs)
    if errs:
        stop(f"the retrieval test failed, nothing written: {'; '.join(errs[:3])} (logs: {logs})")

    # Project map, Home and the retrieval table; then write and commit.
    for it, note_path, rec_path, _ in built:
        map_text = add_under(map_text, "## Knowledge notes", f"- [[Knowledge/{note_path.stem}]]")
        map_text = add_under(map_text, "## Source records", f"- [[Sources/{rec_path.stem}]]")
    gaps = [questions[q - 1] for q, p, _, _ in rows if p is None]
    for g in gaps:
        map_text = add_under(map_text, "## Known gaps and next check", f"- No note answers yet: {g}")
    writes[map_path] = map_text
    home = vault / "Home.md"
    writes[home] = add_under(home.read_text(), "## Start here", f"- [[Projects/{project}]]")
    rt = vault / "Retrieval test.md"
    head = f"## {project} ({today})"
    rt_text = re.sub(rf"^{re.escape(head)}\s*$\n.*?(?=^## |\Z)", "", rt.read_text(), flags=re.M | re.S)
    table = [head, "", f"Run by vault-ready-ingest after ingesting saved links {', '.join('#' + str(b[0]['n']) for b in built)}. "
             "A tool-less model answered from the project's notes; the script checked each quote against the original "
             "article section the note cites.", "",
             "| Question | Vault answer | Original source and section | Result |", "|---|---|---|---|"]
    for q, p, f, sec in rows:
        if p is None:
            table.append(f"| {questions[q - 1]} | none yet | | Gap: no note answers this yet |")
        else:
            rel = Path(f["source_path"]).relative_to(repo) if Path(f["source_path"]).is_relative_to(repo) \
                else Path(f["source_path"]).name
            table.append(f"| {questions[q - 1]} | [[Knowledge/{p.stem}]] | `{rel}`, {sec} | "
                         "Pass for recorded content; the source's own claims not independently checked |")
    writes[rt] = rt_text.rstrip("\n") + "\n\n" + "\n".join(table) + "\n"
    for p, text in writes.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    git(vault, "add", "-A", check=True)
    nums = " ".join(f"#{b[0]['n']}" for b in built)
    git(vault, "commit", "-q", "-m", f"Ingest saved links {nums} into {project}", check=True)
    sha = git(vault, "rev-parse", "--short", "HEAD").stdout.strip()
    for it, note_path, _, _ in built:
        print(f"{'updated' if it['note_path'] else 'written'} #{it['n']}: {note_path.relative_to(vault)}")
    print(f"dropped: {len(dropped_all)} point(s), listed in {logs / 'dropped.md'}")
    print(f"retrieval: {len(rows)} question(s), {len(rows) - len(gaps)} pass, {len(gaps)} gap")
    print(f"committed {sha} in {vault}. Logs: {logs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
