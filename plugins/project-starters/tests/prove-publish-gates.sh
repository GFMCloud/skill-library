#!/usr/bin/env bash
# Prove the two publish gates in skills/new-project/scripts/scaffold.sh:
#   - publish refuses while .claude/board.json (the work board) is missing
#   - publish refuses unless the active gh account is GFMCloud, before gh repo create
# and that a dry run shows both checks. Every project is scaffolded under a fresh mktemp
# directory (set TMPDIR to choose where) and removed on exit. gh is a stub on PATH: it
# reports $STUB_GH_LOGIN and logs any other call, so nothing reaches GitHub, and a
# `repo create` in the log is itself a failure.
#
#   bash plugins/project-starters/tests/prove-publish-gates.sh [scaffold.sh]
set -u -o pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SCAFFOLD="${1:-$HERE/../skills/new-project/scripts/scaffold.sh}"   # pass another scaffold.sh to prove this prover can fail
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/bin"
cat > "$TMP/bin/gh" <<'STUB'
#!/usr/bin/env bash
echo "$*" >> "$STUB_GH_LOG"
case "$1 $2" in
  "auth status") exit 0 ;;
  "api user") [ -n "${STUB_GH_LOGIN:-}" ] && { echo "$STUB_GH_LOGIN"; exit 0; }; exit 1 ;;
esac
exit 0
STUB
chmod +x "$TMP/bin/gh"
export PATH="$TMP/bin:$PATH" STUB_GH_LOG="$TMP/gh.log"
: > "$STUB_GH_LOG"

# project <name> <with-board: 0|1>: scaffold, fill the doc stubs, optionally add a board
project() {
  bash "$SCAFFOLD" init --name "$1" --type python --dir "$TMP/projects" --desc "fixture" >/dev/null 2>&1 || { echo "init failed for $1"; exit 1; }
  local root="$TMP/projects/$1"
  for d in README.md CLAUDE.md SPEC.md KICKOFF.md; do
    /usr/bin/sed -i.bak '/<!-- SCAFFOLD-TODO -->/d' "$root/$d" && rm "$root/$d.bak"
  done
  if [ "$2" = 1 ]; then
    mkdir -p "$root/.claude"
    printf '{"schema": 1, "project": "%s", "url": "https://claude.ai/artifact/FixtureBoard1", "collection": "cards", "lanes": [{"id": "main", "name": "All work"}], "page": ".claude/work-board.html"}\n' "$1" > "$root/.claude/board.json"
  fi
  echo "$root"
}

FAIL=0
run() { # run <expect-exit> <label> <login> <path> [publish args...]; then `has` / `lacks` on $OUT
  local expect="$1" label="$2" login="$3" path="$4"; shift 4
  : > "$STUB_GH_LOG"
  OUT="$(STUB_GH_LOGIN="$login" bash "$SCAFFOLD" publish --path "$path" "$@" 2>&1)"; local rc=$?
  if [ "$rc" = "$expect" ]; then echo "PASS  exit $rc  $label"; else echo "FAIL  exit $rc (expected $expect)  $label"; printf '%s\n' "$OUT" | /usr/bin/sed 's/^/        | /'; FAIL=1; fi
}
has() { if printf '%s' "$OUT" | /usr/bin/grep -qF -- "$1"; then echo "PASS    output has: $1"; else echo "FAIL    output lacks: $1"; FAIL=1; fi; }
never_created() { if /usr/bin/grep -q 'repo create' "$STUB_GH_LOG"; then echo "FAIL    gh repo create was called"; FAIL=1; else echo "PASS    gh repo create was never called"; fi; }
no_commit() { if git -C "$1" rev-parse -q --verify HEAD >/dev/null 2>&1; then echo "FAIL    a commit was made"; FAIL=1; else echo "PASS    no commit was made"; fi; }

P=$(project no-board 0)
run 1 "no board.json, dry run: refuses" GFMCloud "$P" --dry-run
has "no work board"
run 1 "no board.json, real publish: refuses before anything is created" GFMCloud "$P"
has "no work board"; never_created; no_commit "$P"

P=$(project wrong-account 1)
run 1 "gh account gmorris1221, dry run: refuses" gmorris1221 "$P" --dry-run
has "active gh account is 'gmorris1221', not GFMCloud"
run 1 "gh account gmorris1221, real publish: refuses before gh repo create" gmorris1221 "$P"
has "not GFMCloud"; never_created; no_commit "$P"

P=$(project good 1)
run 0 "board present and GFMCloud, dry run: passes and shows both gates" GFMCloud "$P" --dry-run
has "work board: .claude/board.json present"
has "gh account: GFMCloud"
has "[dry-run] gh repo create good --private"
never_created; no_commit "$P"

if [ "$FAIL" -ne 0 ]; then echo "PUBLISH-GATES PROOF: FAIL"; exit 1; fi
echo "PUBLISH-GATES PROOF: PASS"
