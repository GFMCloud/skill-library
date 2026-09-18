#!/bin/bash
# toolkit-review: run a wave of headless jobs with a cap on how many are in flight.
# Usage: run-wave.sh <jobs-file> <log-file>
# <jobs-file>: one job per line, "<runner-script> <arg> [<arg>]", runner-script one of
# run-extractor.sh, run-judge.sh, run-reader.sh, run-fixture-arm.sh.
# Keeps at most wave_size (run.json, default 4) headless runs in flight on this machine,
# counting runs started elsewhere too. Stops launching on the first exit 4 (rate limited).
# Appends one line per finished job to <log-file>: end time, job, exit code.
# Exit 0 if every job exited 0, 4 if stopped for a rate limit, 1 otherwise, 2 on a bad job.
#
# The scripts directory is copied into <log-file>.bin/ before the first job starts and
# every job runs from that copy, so an edit to the skill's scripts while a wave is in
# flight cannot reach a running job (a runner edited mid-wave in the ECC run, 2026-09-17).
RUN="${TR_RUN:?run-wave.sh: set TR_RUN to the run directory}"
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WAVE=4
if [ -s "$RUN/run.json" ]; then WAVE=$(jq -r '.wave_size // 4' "$RUN/run.json"); fi
jobs_file="$1"; log="$2"
if [ ! -s "$jobs_file" ] || [ -z "$log" ]; then echo "usage: run-wave.sh <jobs-file> <log-file>" >&2; exit 2; fi
mkdir -p "$(dirname "$log")"
snap="$log.bin"
rm -rf "$snap"; mkdir -p "$snap"
cp "$S"/*.sh "$S"/*.py "$snap"/ 2>/dev/null
# The runners resolve references/ relative to their own directory; give the snapshot one.
ln -s "$(dirname "$S")/references" "$snap/../references" 2>/dev/null || true
stopflag="$log.rate-limited"
rm -f "$stopflag"
# Validate every line before launching anything, so a bad job never waits behind good ones.
while read -r script a b; do
  [ -z "$script" ] && continue
  case "$script" in run-extractor.sh|run-judge.sh|run-reader.sh|run-fixture-arm.sh) ;; *) echo "run-wave.sh: not a runner: $script" >&2; exit 2 ;; esac
done < "$jobs_file"
inflight() { pgrep -f "headless.sh" | wc -l | tr -d ' '; }
run_one() {
  script="$1"; shift
  bash "$snap/$script" "$@" > /dev/null 2>> "$log.stderr"
  rc=$?
  printf '%s\t%s %s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$script" "$*" "$rc" >> "$log"
  if [ "$rc" -eq 4 ]; then : > "$stopflag"; fi
}
while read -r script a b; do
  [ -z "$script" ] && continue
  while [ "$(inflight)" -ge "$WAVE" ] && [ ! -e "$stopflag" ]; do sleep 5; done
  if [ -e "$stopflag" ]; then echo "run-wave.sh: RATE LIMITED, not launching: $script $a $b" >&2; break; fi
  if [ -n "$b" ]; then run_one "$script" "$a" "$b" & else run_one "$script" "$a" & fi
  sleep 3
done < "$jobs_file"
wait
if [ -e "$stopflag" ]; then echo "stopped: rate limited; see $log"; exit 4; fi
bad=$(awk -F'\t' '$3 != 0' "$log" | wc -l | tr -d ' ')
echo "wave finished: $(wc -l < "$log" | tr -d ' ') jobs logged, $bad non-zero"
[ "$bad" -eq 0 ]
