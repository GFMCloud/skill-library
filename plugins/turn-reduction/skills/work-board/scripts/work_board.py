#!/usr/bin/env python3
"""work_board.py: the scripted half of the work-board skill.

A board is a private claude.ai artifact (the page from templates/work-board.html, with the
`db` capability, collection `cards`). Bash cannot publish an artifact, so standing one up is
two parts (PROPOSAL V6): this script renders the page, Claude publishes it with the
Artifact tool, then this script writes `.claude/board.json` from the returned URL and
Claude seeds the cards with ArtifactData.

Subcommands:
  render    template + config -> page. Config is --board <board.json>, or --name and
            --lane flags for the first render, before a URL exists.
  init      new project: write .claude/board.json from --url and options, write the
            starter authorization.json, re-render the page. Refuses to overwrite either.
  adopt     existing project: as init, but an existing authorization.json is kept (its
            granted list is the project's own), and --trigger adds project triggers.
  validate  check a board.json against the schema below, and that the generated page on
            disk still matches a fresh render (a mismatch is a hand edit: drift).

board.json schema (version 1):
  schema      1
  project     non-empty string, shown on the page
  url         https://claude.ai/artifact/<id> or https://claude.ai/code/artifact/<uuid>
  collection  non-empty string, default "cards"
  lanes       non-empty list of {id, name, when?}; ids unique, lowercase slug
  page        path of the generated page, relative to the project, default
              .claude/work-board.html
  triggers    optional list of extra state-change regexes for the Stop hook: a string, or
              {name, regex}; each must compile

Exit codes: 0 fine; 1 refused or invalid; 2 bad usage or unreadable input.
Stdlib only. Python 3.9+.
"""
import argparse
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
TEMPLATE = os.path.join(SKILL, "templates", "work-board.html")
AUTHZ_TEMPLATE = os.path.join(SKILL, "templates", "authorization.json")
AUTHZ_PY = os.path.join(os.path.dirname(SKILL), "standing-authorization", "authz.py")
TEMPLATE_LABEL = "turn-reduction/skills/work-board/templates/work-board.html"
DEFAULT_PAGE = ".claude/work-board.html"
URL_RX = re.compile(r"^https://claude\.ai/(artifact/[A-Za-z0-9_-]+|code/artifact/[0-9a-fA-F-]{36})/?$")
SLUG_RX = re.compile(r"^[a-z0-9][a-z0-9-]*$")
KNOWN = {"schema", "project", "url", "collection", "lanes", "page", "triggers"}


def regenerate_cmd():
    return "work_board.py render --board .claude/board.json"


def parse_lane(text):
    parts = text.split(":", 2)
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError("--lane must be ID:NAME or ID:NAME:WHEN, got %r" % text)
    lane = {"id": parts[0], "name": parts[1]}
    if len(parts) == 3 and parts[2]:
        lane["when"] = parts[2]
    return lane


def parse_trigger(text):
    if "=" in text:
        name, rx = text.split("=", 1)
        return {"name": name.strip(), "regex": rx}
    return {"name": "project trigger", "regex": text}


def validate_board(doc):
    errors, warnings = [], []
    if not isinstance(doc, dict):
        return ["board.json root must be an object"], []
    if doc.get("schema") != 1:
        errors.append("'schema' must be 1")
    if not isinstance(doc.get("project"), str) or not doc["project"].strip():
        errors.append("'project' must be a non-empty string")
    if not isinstance(doc.get("url"), str) or not URL_RX.match(doc["url"]):
        errors.append("'url' must be the board artifact's claude.ai URL "
                      "(https://claude.ai/artifact/<id>), got %r" % doc.get("url"))
    if not isinstance(doc.get("collection"), str) or not doc["collection"].strip():
        errors.append("'collection' must be a non-empty string")
    lanes = doc.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        errors.append("'lanes' must be a non-empty list of {id, name, when?}")
        lanes = []
    seen = set()
    for i, lane in enumerate(lanes):
        if not isinstance(lane, dict):
            errors.append("lanes[%d] must be an object" % i)
            continue
        lid = lane.get("id")
        if not isinstance(lid, str) or not SLUG_RX.match(lid):
            errors.append("lanes[%d].id must be a lowercase slug, got %r" % (i, lid))
        elif lid in seen:
            errors.append("lanes[%d].id %r is used twice" % (i, lid))
        seen.add(lid)
        if not isinstance(lane.get("name"), str) or not lane["name"].strip():
            errors.append("lanes[%d].name must be a non-empty string" % i)
        if "when" in lane and not isinstance(lane["when"], str):
            errors.append("lanes[%d].when must be a string" % i)
    page = doc.get("page", DEFAULT_PAGE)
    if not isinstance(page, str) or not page.strip() or os.path.isabs(page) or ".." in page.split("/"):
        errors.append("'page' must be a relative path inside the project, got %r" % page)
    triggers = doc.get("triggers", [])
    if not isinstance(triggers, list):
        errors.append("'triggers' must be a list")
        triggers = []
    for i, t in enumerate(triggers):
        rx = t if isinstance(t, str) else (t.get("regex") if isinstance(t, dict) else None)
        if not isinstance(rx, str) or not rx:
            errors.append("triggers[%d] must be a regex string or {name, regex}" % i)
            continue
        try:
            re.compile(rx)
        except re.error as exc:
            errors.append("triggers[%d] does not compile: %s" % (i, exc))
    for key in sorted(set(doc) - KNOWN):
        warnings.append("unknown key %r is ignored" % key)
    return errors, warnings


def page_config(project, collection, lanes):
    return {"project": project, "collection": collection, "lanes": lanes,
            "template": TEMPLATE_LABEL, "regenerate": regenerate_cmd()}


def render_html(cfg):
    with open(TEMPLATE, encoding="utf-8") as fh:
        html = fh.read()
    blob = json.dumps(cfg, indent=2, sort_keys=True).replace("</", "<\\/")
    title = "%s Work Board" % cfg["project"]
    title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for marker in ("__BOARD_CONFIG__", "__PAGE_TITLE__"):
        if html.count(marker) != 1:
            raise SystemExit("template defect: %s appears %d times, expected once" % (marker, html.count(marker)))
    return html.replace("__BOARD_CONFIG__", blob).replace("__PAGE_TITLE__", title)


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_new(path, text):
    """Create-only write: refuses to replace an existing file."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "x", encoding="utf-8") as fh:
        fh.write(text)


def authz_validate(path):
    spec = importlib.util.spec_from_file_location("authz", AUTHZ_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.validate(mod.load(path))


# ------------------------------------------------------------------------------ commands

def cmd_render(args):
    if args.board:
        try:
            board = load_json(args.board)
        except (OSError, ValueError) as exc:
            print("cannot read %s: %s" % (args.board, exc), file=sys.stderr)
            return 2
        errors, _ = validate_board(board)
        if errors:
            for e in errors:
                print("ERROR %s" % e, file=sys.stderr)
            return 1
        cfg = page_config(board["project"], board["collection"], board["lanes"])
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(args.board)))
        out = args.out or os.path.join(project_dir, board.get("page", DEFAULT_PAGE))
    else:
        if not args.name or not args.out:
            print("render needs --board, or --name and --out for a first render", file=sys.stderr)
            return 2
        try:
            lanes = [parse_lane(l) for l in args.lane] or [{"id": "main", "name": "All work"}]
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        cfg = page_config(args.name, args.collection, lanes)
        out = args.out
    html = render_html(cfg)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("rendered %s (%d bytes) for project %r, %d lane(s)" % (out, len(html), cfg["project"], len(cfg["lanes"])))
    print("next: publish it with the Artifact tool and capabilities {\"db\": {}} (first time), or "
          "republish to the board's url (regeneration)")
    return 0


def cmd_setup(args, adopt):
    project_dir = os.path.abspath(args.project_dir)
    if not os.path.isdir(project_dir):
        print("no such project directory: %s" % project_dir, file=sys.stderr)
        return 2
    board_path = os.path.join(project_dir, ".claude", "board.json")
    authz_path = os.path.join(project_dir, "authorization.json")
    if os.path.exists(board_path):
        print("refusing to overwrite %s. This project already has a board; edit board.json "
              "and run render, or rename it .superseded first." % board_path, file=sys.stderr)
        return 1
    if os.path.exists(authz_path) and not adopt:
        print("refusing to overwrite %s. A new project should not have one yet; use adopt "
              "for an existing project, which keeps it." % authz_path, file=sys.stderr)
        return 1
    try:
        lanes = [parse_lane(l) for l in args.lane] or [{"id": "main", "name": "All work"}]
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    name = args.name or os.path.basename(project_dir)
    board = {"schema": 1, "project": name, "url": args.url, "collection": args.collection,
             "lanes": lanes, "page": DEFAULT_PAGE}
    triggers = [parse_trigger(t) for t in (args.trigger or [])]
    if triggers:
        board["triggers"] = triggers
    errors, _ = validate_board(board)
    if errors:
        for e in errors:
            print("ERROR %s" % e, file=sys.stderr)
        print("nothing was written", file=sys.stderr)
        return 1

    # authorization.json first, from the template, validated before anything is written
    wrote_authz = False
    if not os.path.exists(authz_path):
        with open(AUTHZ_TEMPLATE, encoding="utf-8") as fh:
            authz_text = fh.read().replace("__PROJECT__", name.replace('"', "'"))
        tmp = os.path.join(project_dir, ".claude", ".authorization.check.json")
        os.makedirs(os.path.dirname(tmp), exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(authz_text)
        try:
            a_errors, _ = authz_validate(tmp)
        finally:
            os.remove(tmp)
        if a_errors:
            for e in a_errors:
                print("ERROR authorization template: %s" % e, file=sys.stderr)
            return 1
        write_new(authz_path, authz_text)
        wrote_authz = True

    write_new(board_path, json.dumps(board, indent=2) + "\n")
    page_path = os.path.join(project_dir, DEFAULT_PAGE)
    html = render_html(page_config(name, args.collection, lanes))
    previous = None
    if os.path.exists(page_path):
        with open(page_path, encoding="utf-8") as fh:
            previous = fh.read()
    with open(page_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    print("wrote %s" % board_path)
    print(("wrote %s (starter tiers; trim the granted list to this project)" % authz_path) if wrote_authz
          else "kept the existing %s (adopt never replaces a project's own grants)" % authz_path)
    print("rendered %s" % page_path)
    if previous is not None and previous != html:
        print("NOTE the page on disk differed from this render: republish %s to %s" % (page_path, args.url))
    print("next: seed the cards with ArtifactData (url %s, collection %s), then add the board "
          "link to README.md and CLAUDE.md" % (args.url, args.collection))
    return 0


def cmd_validate(args):
    try:
        board = load_json(args.board)
    except (OSError, ValueError) as exc:
        print("cannot read %s: %s" % (args.board, exc), file=sys.stderr)
        return 2
    errors, warnings = validate_board(board)
    if not errors:
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(args.board)))
        page = os.path.join(project_dir, board.get("page", DEFAULT_PAGE))
        if not os.path.exists(page):
            errors.append("generated page %s is missing: run render" % page)
        else:
            with open(page, encoding="utf-8") as fh:
                on_disk = fh.read()
            if on_disk != render_html(page_config(board["project"], board["collection"], board["lanes"])):
                errors.append("generated page %s does not match a fresh render: it was hand-edited "
                              "or the template changed. Run render and republish." % page)
    for w in warnings:
        print("WARN  %s" % w)
    for e in errors:
        print("ERROR %s" % e)
    if errors:
        print("INVALID: %d error(s), %d warning(s)" % (len(errors), len(warnings)))
        return 1
    print("VALID: 0 errors, %d warning(s); %d lane(s), %d project trigger(s)"
          % (len(warnings), len(board["lanes"]), len(board.get("triggers", []))))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="work_board.py", description="Render, stand up and validate a work board.")
    sub = p.add_subparsers(dest="cmd")

    r = sub.add_parser("render", help="template + config -> page")
    r.add_argument("--board", help="the project's .claude/board.json")
    r.add_argument("--name", help="project name, for a first render before board.json exists")
    r.add_argument("--lane", action="append", default=[], help="ID:NAME[:WHEN], repeatable")
    r.add_argument("--collection", default="cards")
    r.add_argument("--out", help="output path (default: board.json's page)")

    for cmd in ("init", "adopt"):
        s = sub.add_parser(cmd, help="write board.json and authorization.json for %s project"
                           % ("a new" if cmd == "init" else "an existing"))
        s.add_argument("--project-dir", required=True)
        s.add_argument("--url", required=True, help="the URL the Artifact tool returned for the page")
        s.add_argument("--name", help="project name (default: the directory name)")
        s.add_argument("--lane", action="append", default=[], help="ID:NAME[:WHEN], repeatable")
        s.add_argument("--collection", default="cards")
        s.add_argument("--trigger", action="append", help="NAME=REGEX, an extra state change for the Stop hook")

    v = sub.add_parser("validate", help="check board.json and the generated page")
    v.add_argument("board")

    args = p.parse_args(argv)
    if args.cmd == "render":
        return cmd_render(args)
    if args.cmd in ("init", "adopt"):
        return cmd_setup(args, adopt=args.cmd == "adopt")
    if args.cmd == "validate":
        return cmd_validate(args)
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
