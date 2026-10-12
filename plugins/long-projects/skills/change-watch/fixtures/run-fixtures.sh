#!/usr/bin/env bash
# FIXTURE runner: the Verify replay proof for watch-step.py, run against scratch copies of
# seen-index-ok.yaml (never the fixture itself).
# Usage: bash run-fixtures.sh [path/to/watch-step.py]   (default ../scripts/watch-step.py)
# Asserts:
#   undelivered  a REPORT that is never confirmed leaves last_state and last_reported
#                unchanged, so the next cycle in the same state reports it again
#   confirm      --confirm records last_state and last_reported for the delivered report
#   replay       the same state three times after the confirm: three NO-REPORT lines,
#                last_reported unchanged
#   flap         OK, ALARM, OK, ALARM, each report confirmed: three REPORT lines
#   refusals     step and --confirm both exit 1 on a mismatched source, --confirm exits 1
#                on a missing seen-index, and classify-action.py exits 1 on an
#                unclassified action
# Exits 0 only when every assertion holds. Pass the pre-0.19.7 watch-step.py as the
# argument to see the undelivered case fail: it marked the transition reported before
# the report was delivered.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STEP="${1:-$HERE/../scripts/watch-step.py}"
CLASSIFY="$HERE/../scripts/classify-action.py"
SRC="cloudwatch:demo-alarm-fixture"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
fails=0

assert() {  # assert <label> <condition-exit-code>
    if [ "$2" -eq 0 ]; then echo "PASS  $1"; else echo "FAIL  $1"; fails=$((fails + 1)); fi
}
field() { grep "^$2:" "$1" | cut -d' ' -f2-; }

# undelivered: the report from this cycle is never confirmed (delivery failed).
IDX="$TMP/undelivered.yaml"; cp "$HERE/seen-index-ok.yaml" "$IDX"
out="$(python3 "$STEP" "$IDX" "$SRC" ALARM)"
[ "$out" = "REPORT $SRC OK -> ALARM" ]; assert "undelivered: first cycle reports OK -> ALARM" $?
[ "$(field "$IDX" last_state)" = "OK" ]; assert "undelivered: last_state still OK before confirm" $?
[ "$(field "$IDX" last_reported)" = "never" ]; assert "undelivered: last_reported still never before confirm" $?
out="$(python3 "$STEP" "$IDX" "$SRC" ALARM)"
[ "$out" = "REPORT $SRC OK -> ALARM" ]; assert "undelivered: next cycle reports the same transition again" $?

# confirm: the report was delivered.
python3 "$STEP" --confirm "$IDX" "$SRC" ALARM; code=$?
[ "$code" -eq 0 ]; assert "confirm: exit 0 (got $code)" $?
[ "$(field "$IDX" last_state)" = "ALARM" ]; assert "confirm: last_state is ALARM" $?
reported="$(field "$IDX" last_reported)"
[ "$reported" != "never" ]; assert "confirm: last_reported is a timestamp" $?

# replay: same state three times after the confirm.
out="$(for _ in 1 2 3; do python3 "$STEP" "$IDX" "$SRC" ALARM; done)"
[ "$(grep -c '^NO-REPORT$' <<<"$out")" -eq 3 ]; assert "replay: three NO-REPORT lines" $?
[ "$(field "$IDX" last_reported)" = "$reported" ]; assert "replay: last_reported unchanged" $?

# flap: OK, ALARM, OK, ALARM from a fresh copy, confirming each delivered report.
IDX="$TMP/flap.yaml"; cp "$HERE/seen-index-ok.yaml" "$IDX"
reports=0
for state in OK ALARM OK ALARM; do
    out="$(python3 "$STEP" "$IDX" "$SRC" "$state")"
    case "$out" in REPORT*) reports=$((reports + 1)); python3 "$STEP" --confirm "$IDX" "$SRC" "$state";; esac
done
[ "$reports" -eq 3 ]; assert "flap: three REPORT lines, one per transition (got $reports)" $?

# refusals.
IDX="$TMP/refuse.yaml"; cp "$HERE/seen-index-ok.yaml" "$IDX"
python3 "$STEP" "$IDX" cloudwatch:other-fixture ALARM 2>/dev/null; code=$?
[ "$code" -eq 1 ]; assert "refusals: step on a mismatched source exits 1 (got $code)" $?
python3 "$STEP" --confirm "$IDX" cloudwatch:other-fixture ALARM 2>/dev/null; code=$?
[ "$code" -eq 1 ]; assert "refusals: --confirm on a mismatched source exits 1 (got $code)" $?
cmp -s "$IDX" "$HERE/seen-index-ok.yaml"; assert "refusals: the refused calls left the seen-index untouched" $?
python3 "$STEP" --confirm "$TMP/missing.yaml" "$SRC" ALARM 2>/dev/null; code=$?
[ "$code" -eq 1 ]; assert "refusals: --confirm on a missing seen-index exits 1 (got $code)" $?
[ ! -e "$TMP/missing.yaml" ]; assert "refusals: --confirm did not create the missing seen-index" $?
python3 "$CLASSIFY" "$HERE/classify-rules.yaml" page-manager >/dev/null 2>&1; code=$?
[ "$code" -eq 1 ]; assert "refusals: an unclassified action exits 1, never safe (got $code)" $?

echo
if [ "$fails" -eq 0 ]; then echo "ALL PASS"; exit 0; else echo "$fails FAILED"; exit 1; fi
