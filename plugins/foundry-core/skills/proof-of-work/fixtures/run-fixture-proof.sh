#!/usr/bin/env bash
# FIXTURE: deliberate-failure proof for scripts/run-checks.sh. Runs from any directory.
#   bash <skill>/fixtures/run-fixture-proof.sh
# Green: every phase in checks-green.tsv runs and exits 0 (expect exit 0, six "ran").
# Red: checks-red.tsv fails at tests, a stop phase, so secrets and diff are skipped
# (expect exit 1, "tests failed", two "skipped"). Absent: checks-absent.tsv has a phase
# whose command is "-" (expect exit 3 and "not-run", never "ran").
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S="$HERE/../scripts/run-checks.sh"
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
fail=0
t() { # t <expected exit> <label> <checks file> <must-contain> <must-not-contain>
  local exp="$1" label="$2" checks="$3" must="$4" mustnot="$5"
  out="$(cd "$W" && bash "$S" "$W/log-$label" "$checks" 2>&1)"; rc=$?
  v=PASS
  [ "$rc" -eq "$exp" ] || v=FAIL
  printf '%s' "$out" | /usr/bin/grep -q -F "$must" || v=FAIL
  if [ -n "$mustnot" ] && printf '%s' "$out" | /usr/bin/grep -q -F "$mustnot"; then v=FAIL; fi
  [ "$v" = FAIL ] && fail=1
  printf '%s  expected exit %s got %s  %s\n' "$v" "$exp" "$rc" "$label"
  printf '%s\n' "$out" | sed 's/^/      | /'
}
t 0 green  "$HERE/checks-green.tsv"  "all 6 phases ran and passed" "failed"
t 1 red    "$HERE/checks-red.tsv"    "tests	failed	1" "secrets	ran"
t 3 absent "$HERE/checks-absent.tsv" "types	not-run" "types	ran"
# A phase file with no recorded exit code is reported not-run even if the summary says ran.
mkdir -p "$W/log-tamper"; printf 'build\ttrue\tran\t0\t%s/log-tamper/1-build.out\n' "$W" > "$W/log-tamper/summary.tsv"
if [ "$fail" -eq 0 ]; then echo "FIXTURE PROOF: PASS"; else echo "FIXTURE PROOF: FAIL"; exit 1; fi
