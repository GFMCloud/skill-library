#!/usr/bin/env bash
# push_check.sh: the push procedure (PROPOSAL section 4 plus V1) as a check. It never pushes.
#
#   push_check.sh --repo <path> --branch <branch> [--base <ref>] --sha <sha> [--sha <sha> ...]
#
# The base is the ref the outgoing range starts from. It is --base when given (it must
# name a ref under refs/remotes/origin/, such as origin/stack; a SHA, HEAD~N or local
# branch stops, since it could start the range above a foreign commit); otherwise
# origin/<branch> when that ref exists; otherwise (a branch's first push) origin/<default
# branch>, read from `git symbolic-ref refs/remotes/origin/HEAD`, else origin/main. The
# base used, and why, is printed.
#
# Exit 0 only when every check holds; exit 1 on the first mismatch, with the reason:
#   1. the active gh account is GFMCloud            (gh api user --jq .login)
#   2. origin is under github.com/GFMCloud/          (git remote get-url origin)
#   3. gitleaks finds nothing in the commits to push (gitleaks git, <base>..HEAD)
#   4. git log --oneline <base>..HEAD lists exactly the recorded SHAs, no more, no fewer
#      (a planted or foreign commit is a hard stop)
# Exit 2 on bad usage. The push itself is a separate command the session runs after this
# exits 0, never chained to it. The pushes_per_session ceiling lives in authorization.json
# and is the session's to count.
#
# Known weaknesses: the SHA list is what the session says it created; the check proves the
# outgoing range equals that list, not that the session really authored each commit. It
# compares against local origin/* refs, so fetch first if another session may have pushed.
# On a first push the range is measured from the default branch: a new branch stacked on
# another unpushed-to-default branch needs --base naming that branch's remote ref.
set -u

repo="" branch="" base=""
shas=()
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) repo="${2:-}"; shift 2 ;;
    --branch) branch="${2:-}"; shift 2 ;;
    --base) base="${2:-}"; [ -n "$base" ] || { echo "push_check: --base needs a ref" >&2; exit 2; }; shift 2 ;;
    --sha) shas+=("${2:-}"); shift 2 ;;
    -h|--help) sed -n '2,27p' "$0"; exit 0 ;;
    *) echo "push_check: unknown option $1" >&2; exit 2 ;;
  esac
done
[ -n "$repo" ] && [ -n "$branch" ] && [ "${#shas[@]}" -gt 0 ] || {
  echo "push_check: usage: push_check.sh --repo <path> --branch <branch> [--base <ref>] --sha <sha> [--sha ...]" >&2; exit 2; }

stop() { echo "PUSH CHECK: STOP - $*"; exit 1; }
ok() { echo "  ok  $*"; }

# 1. active gh account
command -v gh >/dev/null 2>&1 || stop "gh is not installed, so the active account cannot be checked"
login="$(gh api user --jq .login 2>/dev/null)" || stop "gh api user failed: gh is not authenticated"
[ "$login" = "GFMCloud" ] || stop "active gh account is '$login', not GFMCloud (gh auth switch --user GFMCloud)"
ok "active gh account is GFMCloud"

# 2. origin under github.com/GFMCloud/
origin="$(git -C "$repo" remote get-url origin 2>/dev/null)" || stop "$repo has no origin remote"
case "$origin" in
  https://github.com/GFMCloud/*|git@github.com:GFMCloud/*|ssh://git@github.com/GFMCloud/*) ok "origin $origin" ;;
  *) stop "origin '$origin' is not under github.com/GFMCloud/" ;;
esac

# the base ref the outgoing range starts from
if [ -n "$base" ]; then
  # Only a remote-tracking ref may be the base: a SHA, HEAD~N or a local branch could
  # start the range above a foreign commit and hide it from the check.
  full="$(git -C "$repo" rev-parse --symbolic-full-name "$base" 2>/dev/null)"
  case "$full" in
    refs/remotes/origin/*) why="given with --base, $full" ;;
    *) stop "--base $base is not a ref under refs/remotes/origin/ (resolved to '${full:-no symbolic ref}'); a SHA, HEAD~N or local branch could hide commits from the range" ;;
  esac
elif git -C "$repo" rev-parse --verify -q "origin/$branch" >/dev/null; then
  base="origin/$branch"; why="the branch's remote ref"
else
  base="$(git -C "$repo" symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null)"
  if [ -n "$base" ]; then
    why="no origin/$branch yet (first push); origin's default branch from refs/remotes/origin/HEAD"
  else
    base="origin/main"; why="no origin/$branch yet (first push) and no refs/remotes/origin/HEAD; assumed origin/main"
  fi
fi
git -C "$repo" rev-parse --verify -q "$base^{commit}" >/dev/null || stop "base ref $base ($why) does not resolve in $repo; fetch first or pass --base"
ok "base $base ($why)"

# 3. secret scan of the outgoing commits
command -v gitleaks >/dev/null 2>&1 || stop "gitleaks is not installed; the secret scan is not optional"
if gitleaks git --log-opts="$base..HEAD" --redact --exit-code 1 --no-banner "$repo" >/dev/null 2>&1; then
  ok "gitleaks: clean on $base..HEAD"
else
  stop "gitleaks found a secret (or failed) on $base..HEAD. Re-run for detail: gitleaks git --log-opts=$base..HEAD --redact -v $repo"
fi

# 4. outgoing commits equal the recorded SHAs
outgoing="$(git -C "$repo" log --format=%H "$base..HEAD")" || stop "git log failed"
expected=""
for s in "${shas[@]}"; do
  full="$(git -C "$repo" rev-parse --verify -q "$s^{commit}")" || stop "recorded SHA $s is not a commit in $repo"
  expected="$expected$full"$'\n'
done
got_sorted="$(printf '%s\n' "$outgoing" | /usr/bin/sed '/^$/d' | sort -u)"
want_sorted="$(printf '%s' "$expected" | /usr/bin/sed '/^$/d' | sort -u)"
if [ "$got_sorted" != "$want_sorted" ]; then
  echo "  outgoing (git log --oneline $base..HEAD):"
  git -C "$repo" log --oneline "$base..HEAD" | /usr/bin/sed 's/^/    /'
  extra="$(comm -23 <(printf '%s\n' "$got_sorted") <(printf '%s\n' "$want_sorted") | /usr/bin/sed '/^$/d')"
  missing="$(comm -13 <(printf '%s\n' "$got_sorted") <(printf '%s\n' "$want_sorted") | /usr/bin/sed '/^$/d')"
  [ -n "$extra" ] && echo "  not recorded by this session: $(echo $extra)"
  [ -n "$missing" ] && echo "  recorded but not outgoing: $(echo $missing)"
  stop "the outgoing commits are not exactly this session's recorded SHAs"
fi
ok "outgoing commits equal the ${#shas[@]} recorded SHA(s)"
echo "PUSH CHECK: PASS. Push as a separate command: git -C $repo push origin $branch"
exit 0
