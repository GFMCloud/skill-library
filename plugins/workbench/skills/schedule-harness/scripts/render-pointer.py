#!/usr/bin/env python3
"""render-pointer.py: render a Scheduled-task pointer v1 file from a small
YAML or JSON input.

Usage:
    python3 render-pointer.py <input.yaml|input.json> [-o <output.md>]

Input fields (all required):
    name              - short identifier, becomes the pointer's frontmatter `name`
    description       - one line, becomes the pointer's frontmatter `description`
    harness_path      - absolute path to the phased harness this task runs
    phase_skill_path  - absolute path to the harness's /phase SKILL.md
    mode              - "continuous" or a named phase (e.g. "grade", "3")
    hook_timeout      - seconds, filled into the Absolute-limits block v1
    retry_cap         - consecutive-retry cap, filled into the same block

Reads the template at ../templates/pointer.md (relative to this script, so it
runs correctly regardless of the caller's cwd), extracts the fenced example body,
substitutes every {{placeholder}}, and writes the rendered pointer to stdout or
the path given with -o.

This script only renders. It never writes into ~/.claude/scheduled-tasks/ and
never registers a task; registration is Graham's action in the desktop app, or
the mcp__scheduled-tasks__create_scheduled_task tool, with his approval.
"""
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR.parent / "templates" / "pointer.md"

REQUIRED_FIELDS = [
    "name", "description", "harness_path", "phase_skill_path",
    "mode", "hook_timeout", "retry_cap",
]


def load_input(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # local import: only needed for the YAML path
    except ImportError:
        print("error: PyYAML not installed and input is not .json", file=sys.stderr)
        sys.exit(2)
    return yaml.safe_load(text)


def extract_fenced_block(template_text: str) -> str:
    m = re.search(r"```markdown\n(.*?)\n```", template_text, re.S)
    if not m:
        print(f"error: no ```markdown fenced block found in {TEMPLATE_PATH}",
              file=sys.stderr)
        sys.exit(2)
    return m.group(1)


def render(data: dict) -> str:
    missing = [f for f in REQUIRED_FIELDS if f not in data or data[f] in (None, "")]
    if missing:
        print(f"error: missing required field(s): {', '.join(missing)}",
              file=sys.stderr)
        sys.exit(2)
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    block = extract_fenced_block(template_text)
    for key in REQUIRED_FIELDS:
        block = block.replace("{{" + key + "}}", str(data[key]))
    leftover = re.findall(r"\{\{[a-zA-Z_]+\}\}", block)
    if leftover:
        print(f"error: unresolved placeholder(s) after substitution: {leftover}",
              file=sys.stderr)
        sys.exit(2)
    return block


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    out_path = None
    if "-o" in args:
        i = args.index("-o")
        out_path = Path(args[i + 1])
        del args[i:i + 2]
    if not args:
        print("error: no input file given", file=sys.stderr)
        return 2
    input_path = Path(args[0])
    data = load_input(input_path)
    rendered = render(data)
    if out_path:
        out_path.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
