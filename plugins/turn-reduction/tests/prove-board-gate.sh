#!/usr/bin/env bash
# Prove hooks/board_gate.py against fixtures/board-gate/cases.json. Exit 0 only when every
# case gets its expected exit code (2 = the stop is blocked, 0 = it is allowed), and every
# blocked case blocks for the reason its name gives, (a) or (b), and no other.
#
#   bash plugins/turn-reduction/tests/prove-board-gate.sh [hook_path]
#
# Pass a different hook (fixtures/board-gate/stub-never-blocks.py) to prove this prover
# can fail: against a hook that never blocks, every must-block case goes red.
#
# Each case names a throwaway project shape, built fresh under $TMPDIR:
#   full        .claude/board.json with triggers[] + authorization.json
#   notriggers  .claude/board.json without triggers[] + authorization.json
#   noauthz     .claude/board.json only (authorization.json renamed .superseded)
#   superseded  .claude/board.json renamed .superseded + authorization.json
#   none        no .claude/board.json at all
set -u -o pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
HOOK="${1:-$HERE/../hooks/board_gate.py}"
CASES="$HERE/fixtures/board-gate/cases.json"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

python3 - "$CASES" "$TMP" <<'PY'
import json, os, sys
cases, tmp = sys.argv[1], sys.argv[2]
board = {"project": "fixture project", "url": "https://claude.ai/artifact/TestBoard123",
         "collection": "cards", "lanes": [{"id": "now", "name": "This week"}]}
triggers = [{"name": "seed write", "regex": "\\bseed\\.py\\b.*--apply\\b"}]
authz = {"project": "fixture"}
def proj(name, board_obj, board_file, authz_file):
    d = os.path.join(tmp, "proj-" + name)
    os.makedirs(os.path.join(d, ".claude"), exist_ok=True)
    if board_obj is not None:
        json.dump(board_obj, open(os.path.join(d, ".claude", board_file), "w"))
    if authz_file:
        json.dump(authz, open(os.path.join(d, authz_file), "w"))
proj("full", dict(board, triggers=triggers), "board.json", "authorization.json")
proj("notriggers", board, "board.json", "authorization.json")
proj("noauthz", board, "board.json", "authorization.json.superseded")
proj("superseded", board, "board.json.superseded", "authorization.json")
proj("none", None, "", "authorization.json")
for i, case in enumerate(json.load(open(cases))):
    lines = []
    for step in case["transcript"]:
        if "user" in step:
            lines.append({"type": "user", "isSidechain": False, "message": {"role": "user", "content": step["user"]}})
            continue
        if "bash" in step:
            block = {"type": "tool_use", "name": "Bash", "input": {"command": step["bash"]}}
        elif "artifact" in step:
            block = {"type": "tool_use", "name": "ArtifactData", "input": step["artifact"]}
        else:
            block = {"type": "text", "text": step["text"]}
        lines.append({"type": "assistant", "isSidechain": bool(step.get("sidechain")),
                      "message": {"role": "assistant", "content": [block]}})
        if block["type"] == "tool_use":
            lines.append({"type": "user", "isSidechain": bool(step.get("sidechain")),
                          "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t", "content": "ok"}]}})
    t = os.path.join(tmp, "t%d.jsonl" % i)
    with open(t, "w") as fh:
        for l in lines:
            fh.write(json.dumps(l) + "\n")
    inp = {"session_id": "fixture", "hook_event_name": "Stop", "stop_hook_active": False,
           "transcript_path": t, "cwd": "/nowhere"}
    inp.update(case.get("input") or {})
    json.dump(inp, open(os.path.join(tmp, "in%d.json" % i), "w"))
    with open(os.path.join(tmp, "meta%d" % i), "w") as fh:
        fh.write("%s\t%s\t%s\n" % (case["expect"], os.path.join(tmp, "proj-" + case["project"]), case["name"]))
PY
[ $? -eq 0 ] || { echo "BOARD-GATE PROOF: could not build fixtures"; exit 1; }

N=$(ls "$TMP" | /usr/bin/grep -c '^meta')
FAIL=0
i=0
while [ "$i" -lt "$N" ]; do
  IFS=$'\t' read -r EXPECT PROJ NAME < "$TMP/meta$i"
  CLAUDE_PROJECT_DIR="$PROJ" python3 "$HOOK" < "$TMP/in$i.json" > /dev/null 2> "$TMP/err$i.txt"
  GOT=$?
  # a blocked case must block for the reason its name gives, (a) or (b), and only that one
  WHY=""
  if [ "$GOT" = 2 ]; then
    for tag in "(a)" "(b)"; do
      if /usr/bin/grep -qF "board-gate $tag" "$TMP/err$i.txt"; then WHY="$WHY$tag"; fi
    done
  fi
  WANT=""
  if [ "$EXPECT" = 2 ]; then
    case "$NAME" in *"(a)"*) WANT="(a)" ;; *"(b)"*) WANT="(b)" ;; esac
  fi
  if [ "$GOT" = "$EXPECT" ] && [ "$WHY" = "$WANT" ]; then
    echo "PASS  exit $GOT ${WHY:+$WHY }  $NAME"
  elif [ "$GOT" = "$EXPECT" ]; then
    echo "FAIL  exit $GOT but fired '$WHY', expected '$WANT'  $NAME"
    sed 's/^/        | /' "$TMP/err$i.txt"
    FAIL=1
  else
    echo "FAIL  exit $GOT (expected $EXPECT)  $NAME"
    sed 's/^/        | /' "$TMP/err$i.txt"
    FAIL=1
  fi
  i=$((i + 1))
done
if [ "$FAIL" -ne 0 ]; then echo "BOARD-GATE PROOF: FAIL"; exit 1; fi
echo "BOARD-GATE PROOF: PASS ($N cases)"
