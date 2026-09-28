#!/usr/bin/env bash
# Prove skills/work-board/scripts/push_check.sh on throwaway clones. Never touches a real
# checkout: every repo is created under a fresh mktemp directory (set TMPDIR to choose
# where) and removed on exit. gh is a stub on PATH that reports $STUB_GH_LOGIN, so no real
# account is read or switched.
#
#   bash plugins/turn-reduction/tests/prove-push-check.sh
#
# Exit 0 only when the green case passes and every must-fail case fails for its reason.
set -u -o pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/../skills/work-board/scripts/push_check.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/bin"
cat > "$TMP/bin/gh" <<'STUB'
#!/usr/bin/env bash
# stub gh: `gh api user --jq .login` prints $STUB_GH_LOGIN, or fails when it is empty
if [ "$1 $2" = "api user" ]; then
  [ -n "${STUB_GH_LOGIN:-}" ] || { echo "not logged in" >&2; exit 1; }
  echo "$STUB_GH_LOGIN"; exit 0
fi
echo "stub gh: unsupported: $*" >&2; exit 1
STUB
chmod +x "$TMP/bin/gh"
export PATH="$TMP/bin:$PATH"
G() { git -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null "$@"; }

# fresh <name> <origin-url>: a bare "remote" with one commit on main, and a clone of it
# whose origin url is then set to <origin-url> (origin/main stays the real remote ref)
fresh() {
  local d="$TMP/$1"
  mkdir -p "$d"
  git init -q --bare -b main "$d/remote.git"
  G clone -q "$d/remote.git" "$d/clone" 2>/dev/null
  echo seed > "$d/clone/README.md"
  G -C "$d/clone" add README.md
  G -C "$d/clone" commit -q -m "seed"
  G -C "$d/clone" push -q origin HEAD:main 2>/dev/null
  G -C "$d/clone" fetch -q origin
  git -C "$d/clone" branch -q --set-upstream-to=origin/main 2>/dev/null
  git -C "$d/clone" remote set-url origin "$2"
  echo "$d/clone"
}
commit() { # commit <repo> <file> <text> -> prints the new SHA
  echo "$3" > "$1/$2"; G -C "$1" add "$2"; G -C "$1" commit -q -m "change $2"; git -C "$1" rev-parse HEAD
}

FAIL=0
run() { # run <expect-exit> <reason-substring> <label> -- args...
  local expect="$1" why="$2" label="$3"; shift 4
  local out rc
  out="$(bash "$CHECK" "$@" 2>&1)"; rc=$?
  if [ "$rc" = "$expect" ] && printf '%s' "$out" | /usr/bin/grep -qF -- "$why"; then
    echo "PASS  exit $rc  $label"
  else
    echo "FAIL  exit $rc (expected $expect with '$why')  $label"; printf '%s\n' "$out" | /usr/bin/sed 's/^/        | /'; FAIL=1
  fi
}

GOOD_URL="https://github.com/GFMCloud/fixture-repo.git"

R=$(fresh green "$GOOD_URL"); A=$(commit "$R" a.txt one); B=$(commit "$R" b.txt two)
STUB_GH_LOGIN=GFMCloud run 0 "PUSH CHECK: PASS" "own commits, GFMCloud account and remote: passes" -- --repo "$R" --branch main --sha "$A" --sha "$B"

R=$(fresh foreign "$GOOD_URL"); A=$(commit "$R" a.txt one); F=$(commit "$R" planted.txt "another session")
STUB_GH_LOGIN=GFMCloud run 1 "not recorded by this session" "planted foreign commit: stops" -- --repo "$R" --branch main --sha "$A"

R=$(fresh remote "https://github.com/gmorris1221/fixture-repo.git"); A=$(commit "$R" a.txt one)
STUB_GH_LOGIN=GFMCloud run 1 "is not under github.com/GFMCloud/" "non-GFMCloud remote: stops" -- --repo "$R" --branch main --sha "$A"

R=$(fresh lookalike "https://github.com/GFMCloudX/fixture-repo.git"); A=$(commit "$R" a.txt one)
STUB_GH_LOGIN=GFMCloud run 1 "is not under github.com/GFMCloud/" "look-alike owner GFMCloudX: stops" -- --repo "$R" --branch main --sha "$A"

R=$(fresh account "$GOOD_URL"); A=$(commit "$R" a.txt one)
STUB_GH_LOGIN=gmorris1221 run 1 "not GFMCloud" "active gh account gmorris1221: stops" -- --repo "$R" --branch main --sha "$A"
STUB_GH_LOGIN= run 1 "not authenticated" "gh not authenticated: stops" -- --repo "$R" --branch main --sha "$A"

R=$(fresh missing "$GOOD_URL"); A=$(commit "$R" a.txt one)
STUB_GH_LOGIN=GFMCloud run 1 "recorded but not outgoing" "recorded SHA not in the outgoing range: stops" -- --repo "$R" --branch main --sha "$A" --sha "$(git -C "$R" rev-parse HEAD~1)"

# A token-shaped string built at run time, so no secret-shaped text lives in this file.
R=$(fresh leak "$GOOD_URL")
TOKEN="ghp_$(LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 36)"
A=$(commit "$R" config.txt "github_token = $TOKEN")
STUB_GH_LOGIN=GFMCloud run 1 "gitleaks found a secret" "secret in an outgoing commit: stops" -- --repo "$R" --branch main --sha "$A"

run 2 "usage" "no SHAs given: usage error" -- --repo "$R" --branch main

if [ "$FAIL" -ne 0 ]; then echo "PUSH-CHECK PROOF: FAIL"; exit 1; fi
echo "PUSH-CHECK PROOF: PASS (9 cases)"
