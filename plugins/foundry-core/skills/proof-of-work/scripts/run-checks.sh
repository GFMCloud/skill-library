#!/usr/bin/env bash
# run-checks.sh: run the code check sequence and record what actually ran.
#
# Usage: run-checks.sh <log-dir> [checks-file]
#   <log-dir>      created if missing; one <n>-<phase>.out per phase, plus summary.tsv
#   [checks-file]  tab-separated lines "<phase>\t<command>", run in file order. When
#                  omitted, the sequence in references/code-checklist.md is derived from
#                  the current directory (package.json scripts, tsconfig, pyproject or
#                  *.py, an available secret scanner, git).
#
# Every phase is run with `bash -c` and its stdout and stderr go to the phase's file,
# never through a pipe, so the exit code recorded is the tool's own. A phase is marked
# `ran` only when its exit code was captured; a phase whose tool is absent is `not-run`,
# and a phase skipped because an earlier stop phase failed is `skipped`. The summary is
# read back from the per-phase files, so nothing is reported that did not run.
# Exit 1 if any phase failed, 3 if any phase could not run, 0 otherwise. `not-run` and
# `skipped` phases belong in the report's NOT VERIFIED list, never in a pass.
#
# Stop phases (from the checklist): build and tests. A failure there ends the sequence.
set -u
log="${1:-}"; checks="${2:-}"
if [ -z "$log" ]; then echo "usage: run-checks.sh <log-dir> [checks-file]" >&2; exit 2; fi
mkdir -p "$log"
: > "$log/summary.tsv"

has_npm_script() { [ -f package.json ] && python3 -c "import json,sys; sys.exit(0 if '$1' in json.load(open('package.json')).get('scripts',{}) else 1)" 2>/dev/null; }
derive() {
  # phase<TAB>command<TAB>stop(yes|no); a command of "-" means the tool is absent
  local build="-" types="-" lint="-" tests="-" secrets="-" diff="git diff --stat"
  if [ -f package.json ]; then
    has_npm_script build && build="npm run build"
    [ -f tsconfig.json ] && types="npx --no-install tsc --noEmit"
    has_npm_script lint && lint="npm run lint"
    has_npm_script test && tests="npm test -- --coverage"
  elif [ -f pyproject.toml ] || [ -f setup.py ] || ls ./*.py > /dev/null 2>&1; then
    build="python3 -m compileall -q ."
    command -v pyright > /dev/null 2>&1 && types="pyright ."
    command -v ruff > /dev/null 2>&1 && lint="ruff check ."
    if python3 -c "import pytest" 2>/dev/null; then tests="python3 -m pytest -q"; else tests="python3 -m unittest discover"; fi
  fi
  local scanner
  scanner="$(find "${HOME}/skill-library/plugins" -name scan_secrets.py 2>/dev/null | sort | head -1)"
  if [ -n "$scanner" ]; then secrets="python3 $scanner ."; else secrets="/usr/bin/grep -rn -E '(AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)' --exclude-dir=.git --exclude-dir=node_modules . ; test \$? -eq 1"; fi
  git rev-parse > /dev/null 2>&1 || diff="-"
  printf 'build\t%s\tyes\ntypes\t%s\tno\nlint\t%s\tno\ntests\t%s\tyes\nsecrets\t%s\tyes\ndiff\t%s\tno\n' "$build" "$types" "$lint" "$tests" "$secrets" "$diff"
}

if [ -n "$checks" ]; then
  if [ ! -s "$checks" ]; then echo "run-checks.sh: checks file missing or empty: $checks" >&2; exit 2; fi
  plan="$(awk -F'\t' 'NF >= 2 { stop = ($1 == "build" || $1 == "tests" || $1 == "secrets") ? "yes" : "no"; if (NF >= 3) stop = $3; printf "%s\t%s\t%s\n", $1, $2, stop }' "$checks")"
else
  plan="$(derive)"
fi

n=0; stopped=0; failed=0; notrun=0
while IFS="$(printf '\t')" read -r phase cmd stop; do
  [ -z "$phase" ] && continue
  n=$((n + 1))
  out="$log/$n-$phase.out"
  if [ "$stopped" -eq 1 ]; then
    printf '%s\t%s\tskipped\t-\t%s\n' "$phase" "$cmd" "$out" >> "$log/summary.tsv"; : > "$out"; continue
  fi
  if [ "$cmd" = "-" ]; then
    printf '%s\t-\tnot-run\t-\t%s\n' "$phase" "$out" >> "$log/summary.tsv"; : > "$out"; notrun=$((notrun + 1)); continue
  fi
  bash -c "$cmd" > "$out" 2>&1
  rc=$?
  echo "$rc" > "$out.exit"
  status=ran; [ "$rc" -ne 0 ] && { status=failed; failed=$((failed + 1)); }
  printf '%s\t%s\t%s\t%s\t%s\n' "$phase" "$cmd" "$status" "$rc" "$out" >> "$log/summary.tsv"
  if [ "$rc" -ne 0 ] && [ "$stop" = "yes" ]; then stopped=1; fi
done <<< "$plan"

# The table is read back from the files, so a phase with no recorded exit code cannot show as ran.
echo "phase	status	exit	command"
while IFS="$(printf '\t')" read -r phase cmd status rc out; do
  if [ "$status" = ran ] || [ "$status" = failed ]; then
    if [ ! -s "$out.exit" ]; then status="not-run"; rc="-"; fi
  fi
  printf '%s\t%s\t%s\t%s\n' "$phase" "$status" "$rc" "$cmd"
done < "$log/summary.tsv"
echo "logs: $log"
if [ "$failed" -gt 0 ]; then echo "run-checks: $failed phase(s) failed; stopped after the first stop-phase failure"; exit 1; fi
if [ "$notrun" -gt 0 ]; then echo "run-checks: $notrun phase(s) could not run; list them as not verified"; exit 3; fi
echo "run-checks: all $n phases ran and passed"
