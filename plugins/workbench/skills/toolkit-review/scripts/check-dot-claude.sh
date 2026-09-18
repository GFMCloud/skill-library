#!/bin/bash
# toolkit-review: the mechanical form of "the run never wrote to ~/.claude".
# Usage: check-dot-claude.sh [root] [marker]      defaults: ~/.claude, $TR_RUN/.marker
# Lists every file under root newer than the marker. Exit 0 unless one of them is on the
# denylist: the parts of ~/.claude that carry the installed setup (hooks, agents, commands,
# settings files, CLAUDE.md, keybindings, skills and plugins outside their synced/
# directories). A denylisted path is printed under VIOLATIONS and the exit is 9, a stop.
# Everything else is Claude Code's own bookkeeping (backups, cache, file-history, projects,
# sessions, synced manifests, the per-process plugin lock markers plugins/**/.in_use/<pid>
# and plugins/.last_inuse_sweep) and is counted by top-level directory so the record shows
# what it was. An allowlist was tried first in the ECC run and stopped the run three times
# on new bookkeeping paths (2026-09-17); the denylist is what survived.
# The arguments exist so the check can be proven against a fake tree. Prove it at the
# start of every run: start an interactive session, run this, expect ok.
root="${1:-$HOME/.claude}"
marker="${2:-${TR_RUN:-.}/.marker}"
echo "marker: $marker"
if [ ! -d "$root" ] || [ ! -f "$marker" ]; then echo "check-dot-claude: need root dir and marker file: $root $marker" >&2; exit 2; fi
all="$(find "$root" -newer "$marker" -type f | sort)"
deny="^$root/(hooks/|agents/|commands/|settings[^/]*\.json$|CLAUDE\.md$|keybindings\.json$|skills/|plugins/)"
bad="$(printf '%s\n' "$all" | /usr/bin/grep -E "$deny" | /usr/bin/grep -v -E "^$root/(skills|plugins)/synced/" | /usr/bin/grep -v -E "^$root/plugins/(.*/)?\.in_use/[^/]+$|^$root/plugins/\.last_inuse_sweep$")"
echo "files newer than marker: $(printf '%s\n' "$all" | /usr/bin/grep -c .)"
printf '%s\n' "$all" | /usr/bin/grep . | sed -E "s#^$root/((plugins|skills)/synced|[^/]+).*#\1#" | sort | uniq -c
if [ -n "$bad" ]; then echo "VIOLATIONS:"; printf '%s\n' "$bad"; exit 9; fi
echo "check-dot-claude: ok"
