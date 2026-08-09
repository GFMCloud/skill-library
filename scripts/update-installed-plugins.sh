#!/bin/zsh
# Refresh this machine's installed skill-library plugins from the marketplace,
# so installed caches track the repo. Intended to run daily via launchd:
#   ~/Library/LaunchAgents/com.gfm.skill-library-plugin-update.plist
# Safe to run manually at any time. Updates apply to newly started sessions.
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') skill-library plugin update ==="

if ! claude plugin marketplace update skill-library; then
  echo "marketplace update FAILED (offline or auth issue) — skipping plugin updates"
  exit 1
fi

fail=0
for plugin in $(claude plugin list | awk '/@skill-library/ {print $2}'); do
  echo "--- updating $plugin"
  claude plugin update "$plugin" || fail=1
done

echo "=== done (updates apply to newly started sessions)"
exit $fail
