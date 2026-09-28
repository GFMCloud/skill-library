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

# First push of a new branch: there is no origin/<branch>, so the base falls back to
# origin's default branch and the range must still be exactly the recorded SHAs.
R=$(fresh newbranch "$GOOD_URL"); git -C "$R" checkout -q -b feature; A=$(commit "$R" a.txt one)
STUB_GH_LOGIN=GFMCloud run 0 "base origin/main (no origin/feature yet" "first push of a new branch, own commit only: passes on origin/main" -- --repo "$R" --branch feature --sha "$A"

R=$(fresh newforeign "$GOOD_URL"); git -C "$R" checkout -q -b feature; A=$(commit "$R" a.txt one); F=$(commit "$R" planted.txt "another session")
STUB_GH_LOGIN=GFMCloud run 1 "not recorded by this session" "first push of a new branch with a foreign commit: stops" -- --repo "$R" --branch feature --sha "$A"

# origin's default branch is read from refs/remotes/origin/HEAD when it is set: here the
# default is trunk, which is one commit ahead of main, so origin/main would list a foreign
# commit and only origin/trunk gives exactly the recorded SHA.
R=$(fresh defaulthead "$GOOD_URL"); git -C "$R" checkout -q -b trunk; T=$(commit "$R" t.txt trunk)
G -C "$R" push -q "$TMP/defaulthead/remote.git" trunk 2>/dev/null; G -C "$R" fetch -q "$TMP/defaulthead/remote.git" '+refs/heads/*:refs/remotes/origin/*'
git -C "$R" symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/trunk
git -C "$R" checkout -q -b feature; A=$(commit "$R" a.txt one)
STUB_GH_LOGIN=GFMCloud run 0 "base origin/trunk (no origin/feature yet (first push); origin's default branch" "first push reads origin's default branch from origin/HEAD: passes on origin/trunk" -- --repo "$R" --branch feature --sha "$A"

# Explicit --base: a new branch stacked on a pushed branch. The default-branch fallback
# counts the stacked-on commit as foreign and stops; --base origin/stack passes.
R=$(fresh stacked "$GOOD_URL"); git -C "$R" checkout -q -b stack; S=$(commit "$R" s.txt stack)
G -C "$R" push -q "$TMP/stacked/remote.git" stack 2>/dev/null; G -C "$R" fetch -q "$TMP/stacked/remote.git" '+refs/heads/*:refs/remotes/origin/*'
git -C "$R" checkout -q -b feature; A=$(commit "$R" a.txt one)
STUB_GH_LOGIN=GFMCloud run 1 "not recorded by this session" "stacked branch without --base: fallback to origin/main stops" -- --repo "$R" --branch feature --sha "$A"
STUB_GH_LOGIN=GFMCloud run 0 "base origin/stack (given with --base, refs/remotes/origin/stack)" "stacked branch with explicit --base origin/stack: passes" -- --repo "$R" --branch feature --base origin/stack --sha "$A"
STUB_GH_LOGIN=GFMCloud run 1 "--base origin/nope is not a ref under refs/remotes/origin/" "explicit --base that does not resolve: stops" -- --repo "$R" --branch feature --base origin/nope --sha "$A"

# --base must be a ref under refs/remotes/origin/. A foreign commit F sits under the
# session's own commit M; any base at or above F would hide it, so each one stops.
R=$(fresh narrowbase "$GOOD_URL"); git -C "$R" checkout -q -b feature; F=$(commit "$R" planted.txt "another session"); M=$(commit "$R" a.txt one)
git -C "$R" branch -q localbase "$F"
STUB_GH_LOGIN=GFMCloud run 1 "is not a ref under refs/remotes/origin/" "--base HEAD~1 above a foreign commit: stops" -- --repo "$R" --branch feature --base HEAD~1 --sha "$M"
STUB_GH_LOGIN=GFMCloud run 1 "is not a ref under refs/remotes/origin/" "--base <sha> of a foreign commit: stops" -- --repo "$R" --branch feature --base "$F" --sha "$M"
STUB_GH_LOGIN=GFMCloud run 1 "is not a ref under refs/remotes/origin/" "--base <local branch> at a foreign commit: stops" -- --repo "$R" --branch feature --base localbase --sha "$M"
STUB_GH_LOGIN=GFMCloud run 1 "not recorded by this session" "same repo with --base origin/main: stops on the foreign commit" -- --repo "$R" --branch feature --base origin/main --sha "$M"

if [ "$FAIL" -ne 0 ]; then echo "PUSH-CHECK PROOF: FAIL"; exit 1; fi
echo "PUSH-CHECK PROOF: PASS (19 cases)"
