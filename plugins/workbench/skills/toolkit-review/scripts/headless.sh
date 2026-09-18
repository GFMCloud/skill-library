#!/bin/bash
# toolkit-review: core headless runner. Every model call in a run goes through here.
#
# Usage: headless.sh <profile> <cwd> <model> <prompt-file> <output-file> <label> [extra claude flags...]
#   profile: clean    judge flags: no settings, restricted, no MCP, Read/Glob/Grep only
#            bare     no settings, Read/Glob/Grep only (fixture baseline arm)
#            current  default settings, Read/Glob/Grep only (fixture arms that load the real setup)
#            open     default settings, default tools (negative controls only)
# Env:  TR_RUN              the run directory (required); the budget file is $TR_RUN/budget/usage.tsv
#       HEADLESS_TIMEOUT_S  per-call timeout; default timeout_s from $TR_RUN/run.json, else 1200
#       TR_CLAUDE           the claude binary; default "claude". Proofs point it at a stub.
#
# Writes the reply text to <output-file>, the raw JSON result to <output-file>.json, stderr
# to <output-file>.stderr, and appends one line to the budget file. Exit codes: 0 ok,
# 2 bad arguments, 3 stalled (timeout), 4 rate limited, 5 empty output or model-reported
# error, 6 claude failed. Handles no credential: auth is whatever the CLI already has.
RUN="${TR_RUN:?headless.sh: set TR_RUN to the run directory}"
BUDGET="$RUN/budget/usage.tsv"
CLAUDE="${TR_CLAUDE:-claude}"
default_timeout=1200
if [ -s "$RUN/run.json" ]; then default_timeout=$(jq -r '.timeout_s // 1200' "$RUN/run.json"); fi
TIMEOUT_S="${HEADLESS_TIMEOUT_S:-$default_timeout}"

if [ "$#" -lt 6 ]; then echo "usage: headless.sh <profile> <cwd> <model> <prompt-file> <output-file> <label> [flags...]" >&2; exit 2; fi
profile="$1"; cwd="$2"; model="$3"; prompt_file="$4"; out="$5"; label="$6"; shift 6

if [ ! -d "$cwd" ]; then echo "headless.sh: cwd does not exist: $cwd" >&2; exit 2; fi
if [ ! -s "$prompt_file" ]; then echo "headless.sh: prompt file missing or empty: $prompt_file" >&2; exit 2; fi

case "$profile" in
  clean)   flags=(--setting-sources "" --restricted --strict-mcp-config --permission-prompts none --tools "Read,Glob,Grep") ;;
  bare)    flags=(--setting-sources "" --strict-mcp-config --permission-prompts none --tools "Read,Glob,Grep") ;;
  current) flags=(--permission-prompts none --tools "Read,Glob,Grep") ;;
  open)    flags=(--permission-prompts none) ;;
  *) echo "headless.sh: unknown profile: $profile" >&2; exit 2 ;;
esac

mkdir -p "$(dirname "$out")" "$(dirname "$BUDGET")"
prompt="$(cat "$prompt_file")"
cd "$cwd" || exit 2

timeout "$TIMEOUT_S" "$CLAUDE" -p "$prompt" --model "$model" "${flags[@]}" \
  --no-session-persistence --output-format json "$@" > "$out.json" 2> "$out.stderr"
rc=$?

status=ok
if [ "$rc" -eq 124 ]; then status=stalled; fi
if [ "$rc" -ne 0 ] && [ "$rc" -ne 124 ]; then status=failed; fi
# A reply that merely discusses rate limits is not a 429: the raw JSON is searched only
# when it is unparseable or the CLI itself flagged an error. stderr is always searched.
rl_re='"?(status|code)"?: ?429|rate.?limit|hit your (session|usage) limit'
rl_files=("$out.stderr")
if ! jq -e . "$out.json" > /dev/null 2>&1 || [ "$(jq -r '.is_error // false' "$out.json")" = "true" ]; then rl_files+=("$out.json"); fi
if /usr/bin/grep -q -i -E "$rl_re" "${rl_files[@]}" 2>/dev/null; then status=rate-limited; fi

in_tok=0; out_tok=0
if [ -s "$out.json" ] && jq -e . "$out.json" > /dev/null 2>&1; then
  jq -r '.result // ""' "$out.json" > "$out"
  in_tok=$(jq -r '[.usage.input_tokens, .usage.cache_creation_input_tokens, .usage.cache_read_input_tokens] | map(. // 0) | add' "$out.json")
  out_tok=$(jq -r '.usage.output_tokens // 0' "$out.json")
  if [ "$status" = ok ] && [ "$(jq -r '.is_error // false' "$out.json")" = "true" ]; then status=model-error; fi
else
  : > "$out"
fi
# jq prints a newline for an empty string, so test the content, not the file size.
if [ "$status" = ok ] && [ -z "$(tr -d '[:space:]' < "$out")" ]; then status=empty; fi

printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$label" "$profile" "$model" "$in_tok" "$out_tok" "$status" >> "$BUDGET"

case "$status" in
  ok) exit 0 ;;
  stalled) echo "headless.sh: stalled after ${TIMEOUT_S}s: $label" >&2; exit 3 ;;
  rate-limited) echo "headless.sh: RATE LIMITED, stop the wave: $label" >&2; /usr/bin/grep -i -o -E 'reset[^"]{0,80}' "$out.json" "$out.stderr" 2>/dev/null | head -2 >&2; exit 4 ;;
  empty|model-error) echo "headless.sh: $status: $label" >&2; exit 5 ;;
  *) echo "headless.sh: claude exited $rc: $label" >&2; exit 6 ;;
esac
