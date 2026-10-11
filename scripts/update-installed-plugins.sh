#!/bin/zsh
# Refresh this machine's installed skill-library plugins from the marketplace,
# so installed caches track the repo. Intended to run daily via launchd:
#   ~/Library/LaunchAgents/com.gfm.skill-library-plugin-update.plist
# Safe to run manually at any time. Updates apply to newly started sessions.
# A plugin whose hook surface (hook definitions, hooks/ files, files a hook command
# names) differs between the installed and incoming version is REFUSED and its diff
# printed: a hook change is installed only by hand, after reading the diff.
# Test hooks (see scripts/test-update-installed-plugins.sh): PLUGINS_ROOT,
# UPDATER_PATH_PREFIX (dirs put ahead of the fixed PATH), UPDATER_SKIP_RECONCILE.
set -uo pipefail
export PATH="${UPDATER_PATH_PREFIX:+$UPDATER_PATH_PREFIX:}/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
PLUGINS_ROOT="${PLUGINS_ROOT:-$HOME/.claude/plugins}"
CACHE="$PLUGINS_ROOT/cache/skill-library"
CLONE="$PLUGINS_ROOT/marketplaces/skill-library/plugins"
HERE="${0:A:h}"  # resolved here: inside a function zsh sets $0 to the function name
surface() { python3 "$HERE/plugin-hook-surface.py" "$1" "$2"; }

# hooks_ok <plugin@skill-library> <installed version>: return 0 only if the hook
# surface is identical; otherwise print REFUSED (and the diff) and return 1.
hooks_ok() {
  local plugin=$1 ver=$2 name=${1%@*} inst inc incver d
  inst="$CACHE/$name/$ver" inc="$CLONE/$name"
  [[ -d $inst ]] || { echo "REFUSED $plugin: installed copy not found at $inst, cannot compare hooks"; return 1; }
  [[ -d $inc ]] || { echo "REFUSED $plugin: marketplace copy not found at $inc, cannot compare hooks"; return 1; }
  incver=$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$inc/.claude-plugin/plugin.json" 2>/dev/null | head -1)
  d="$work/$name"; mkdir -p "$d/installed" "$d/incoming"
  if ! surface "$inst" "$d/installed" || ! surface "$inc" "$d/incoming"; then
    echo "REFUSED $plugin: could not read hook definitions, not updating"; return 1
  fi
  (cd "$d" && diff -ruN installed incoming) > "$d/diff.txt" 2>&1
  case $? in
    0) return 0 ;;
    1) echo "REFUSED $plugin: hooks changed between $ver and ${incver:-unknown}" ;;
    *) echo "REFUSED $plugin: diff of hook surfaces failed, not updating" ;;
  esac
  cat "$d/diff.txt"
  return 1
}

echo "=== $(date '+%Y-%m-%d %H:%M:%S') skill-library plugin update ==="

if ! claude plugin marketplace update skill-library; then
  echo "marketplace update FAILED (offline or auth issue) — skipping plugin updates"
  exit 1
fi

fail=0
work=$(mktemp -d) || exit 1
trap 'rm -rf "$work"' EXIT
for entry in $(claude plugin list | awk '/@skill-library/ {p=$2} p && /Version:/ {print p ":" $2; p=""}'); do
  plugin=${entry%%:*}
  if hooks_ok "$plugin" "${entry##*:}"; then
    echo "--- updating $plugin"
    claude plugin update "$plugin" || fail=1
  else
    fail=1
  fi
done

echo "=== done (updates apply to newly started sessions)"

# Then say where every pack stands (install record, cache, clone, origin), read-only.
[[ -n "${UPDATER_SKIP_RECONCILE:-}" ]] || bash "$(dirname "$0")/reconcile-installed-plugins.sh" || true
exit $fail
