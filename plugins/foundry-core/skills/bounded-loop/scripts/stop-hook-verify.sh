#!/usr/bin/env bash
# stop-hook-verify.sh: the script-based Stop hook for bounded-loop.
#
# Reads the Stop hook's JSON on stdin (session_id, cwd, hook_event_name, ...;
# see references/stop-hook-contract.md for the quoted doc lines), then:
#   - runs --check in --repo
#   - exit 0 while the check passes, or once the run has escalated (release
#     the turn; nothing left to gate)
#   - exit 2 with the check's verbatim output on stderr while the check fails
#     and budget remains (this is the doc-verified way a Stop hook's stderr
#     becomes Claude's blocking message, i.e. what keeps the retry loop going)
#   - on budget exhaustion, or a guarded-file change, or two consecutive
#     identical attempts: write Escalation report v1 to --escalation-out and
#     exit 0 (release the turn so the report can be presented)
#
# Usage (see SKILL.md "Inputs" for how each flag maps to the goal block):
#   stop-hook-verify.sh --check "<command>" [--budget N] [--repo PATH]
#     [--state PATH] [--guard PATH ...] [--escalation-out PATH] [--goal TEXT]
#
# Runnable from any directory: paths are resolved absolute or relative to
# --repo, never to the caller's cwd.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Collect args into a form the python heredoc can read without re-parsing
# bash's quoting rules. GUARD_PATHS is repeatable.
CHECK=""
BUDGET="3"
REPO=""
STATE=""
ESCALATION_OUT=""
GOAL_TEXT="not provided"
GUARD_PATHS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) CHECK="$2"; shift 2 ;;
    --budget) BUDGET="$2"; shift 2 ;;
    --repo) REPO="$2"; shift 2 ;;
    --state) STATE="$2"; shift 2 ;;
    --guard) GUARD_PATHS+=("$2"); shift 2 ;;
    --escalation-out) ESCALATION_OUT="$2"; shift 2 ;;
    --goal) GOAL_TEXT="$2"; shift 2 ;;
    -h|--help)
      grep '^#' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    *) echo "stop-hook-verify.sh: unknown argument '$1'" >&2; exit 64 ;;
  esac
done

# Stdin carries the hook's JSON (session_id, cwd, hook_event_name, ...). Read
# it once, best-effort: a fixture invoking this directly may pass a minimal
# {"cwd": "..."} or nothing at all (stdin closed), both must work.
HOOK_STDIN=""
if [ ! -t 0 ]; then
  HOOK_STDIN="$(cat)"
fi

if [ -z "$CHECK" ]; then
  echo "stop-hook-verify.sh: --check is required" >&2
  exit 64
fi

export CHECK BUDGET REPO STATE ESCALATION_OUT GOAL_TEXT HOOK_STDIN
if [ "${#GUARD_PATHS[@]}" -gt 0 ]; then
  python3 "$SCRIPT_DIR/_verify_impl.py" "${GUARD_PATHS[@]}"
else
  python3 "$SCRIPT_DIR/_verify_impl.py"
fi
