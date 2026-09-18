#!/usr/bin/env bash
# smoke-stop-hook.sh: the Stop hook that keeps a "ready" claim from ending the turn
# while the smoke script is red.
#
# Usage (in ~/.claude/settings.json, Stop event, matcher "*"):
#   bash /abs/path/to/smoke-gate/scripts/smoke-stop-hook.sh /abs/path/to/project/smoke.sh
# Any SMOKE_* overrides the generated script needs (connection addresses) are set in the
# hook command's environment, as the generator's docstring describes.
#
# Behavior, per foundry-core:bounded-loop's stop-hook contract: runs the smoke script,
# and on a non-zero exit re-prints its output to stderr and exits 2, which blocks the
# stop with the script's own SMOKE FAIL lines as the message. On exit 0 it exits 0 and
# prints nothing, so a green run releases the turn silently. Reads the hook's stdin JSON
# for `stop_hook_active`: when Claude Code is already continuing because this hook
# blocked once, the hook prints the failure to stderr and exits 0 instead of 2, so a
# smoke script that stays red cannot hold the session in a loop; the red output is
# still the last thing in the transcript. Fails open with a stderr line when the smoke
# script path is missing, because a hook that cannot run must not silently pass as
# green either: the line names the missing path.
set -u
smoke="${1:-}"
input="$(cat 2>/dev/null || true)"
if [ -z "$smoke" ] || [ ! -f "$smoke" ]; then
  echo "smoke-stop-hook: smoke script missing: '${smoke}'; the gate did not run" >&2
  exit 0
fi
active=false
if printf '%s' "$input" | /usr/bin/grep -q -E '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then active=true; fi
out="$(bash "$smoke" 2>&1)"; code=$?
if [ "$code" -ne 0 ]; then
  printf '%s\n' "$out" >&2
  if [ "$active" = true ]; then
    echo "smoke-stop-hook: smoke is still red after one blocked stop; releasing the turn so the session cannot loop" >&2
    exit 0
  fi
  exit 2
fi
exit 0
