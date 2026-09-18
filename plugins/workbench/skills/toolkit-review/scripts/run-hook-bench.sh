#!/bin/bash
# toolkit-review: feed synthetic events to hook scripts in throwaway containers (full size only).
# Usage: run-hook-bench.sh <side>      side: installed | <source id>
# One container per script per event: no network, read-only mounts, no host environment,
# HOME and the candidate's data-home variable inside the container. No install step, ever.
# These are synthetic events fed to scripts, not hooks firing inside a Claude session, and
# every container starts fresh, so a hook with first-use state shows only its first use
# (the stateful bench is not built; see references/limits.md).
#
# Inputs under $TR_RUN/bench/: events/*.json; hooks-<side>.tsv with one line per hook,
# <name>\t<interpreter>\t<path under /code>[\t<extra args>]; code/<side>/ mounted at /code.
# run.json: .bench.images.<side> (an official image), .bench.data_home_var (optional).
# A candidate side refuses to run unless $TR_RUN/gate-a/rulings.md contains
# "auth_candidate_hook_bench: yes".
RUN="${TR_RUN:?run-hook-bench.sh: set TR_RUN to the run directory}"
TIMEOUT_S=60
side="$1"
if [ -z "$side" ]; then echo "usage: run-hook-bench.sh installed|<source id>" >&2; exit 2; fi
if [ "$side" != "installed" ]; then
  if ! /usr/bin/grep -q '^auth_candidate_hook_bench: yes$' "$RUN/gate-a/rulings.md" 2>/dev/null; then
    echo "run-hook-bench.sh: REFUSED. Gate A has not authorized running candidate hook scripts (no 'auth_candidate_hook_bench: yes' line in $RUN/gate-a/rulings.md)." >&2
    exit 7
  fi
fi
image=$(jq -r --arg s "$side" '.bench.images[$s] // empty' "$RUN/run.json" 2>/dev/null)
datavar=$(jq -r '.bench.data_home_var // "TOOLKIT_REVIEW_DATA_HOME"' "$RUN/run.json" 2>/dev/null)
code="$RUN/bench/code/$side"
list="$RUN/bench/hooks-$side.tsv"
if [ -z "$image" ] || [ ! -s "$list" ] || [ ! -d "$RUN/bench/events" ] || [ ! -d "$code" ]; then
  echo "run-hook-bench.sh: need run.json .bench.images.$side, $list, $RUN/bench/events and $code" >&2; exit 2
fi
out="$RUN/bench/results/$side"
mkdir -p "$out"
fail=0
while IFS="$(printf '\t')" read -r name interp path args; do
  [ -z "$name" ] && continue
  for ev in "$RUN"/bench/events/*.json; do
    evname="$(basename "$ev" .json)"
    res="$out/${name}__${evname}.txt"
    timeout "$TIMEOUT_S" docker run --rm -i --network none --read-only --tmpfs /tmp --tmpfs /home/bench \
      -v "$code":/code:ro -e HOME=/home/bench -e "$datavar=/home/bench/data" -e CLAUDE_PLUGIN_ROOT=/code \
      -w /tmp "$image" "$interp" "/code/$path" $args < "$ev" > "$res.stdout" 2> "$res.stderr"
    rc=$?
    { echo "hook: $name"; echo "event: $evname"; echo "exit_code: $rc"; echo "--- stdout"; cat "$res.stdout"; echo "--- stderr"; cat "$res.stderr"; } > "$res"
    rm -f "$res.stdout" "$res.stderr"
    if [ "$rc" -eq 124 ] || [ "$rc" -eq 125 ]; then fail=1; fi
  done
done < "$list"
echo "results in $out: $(find "$out" -name '*.txt' | wc -l | tr -d ' ') files"
exit $fail
