#!/usr/bin/env bash
# verdict-check.sh: validates a Verdict object v1 file (interface spec section 3)
# and, given two, applies the review-pair hold rule.
#
# Usage:
#   verdict-check.sh <verdict-file>                     validate one verdict
#   verdict-check.sh <first-verdict> <second-verdict>    validate both, apply hold rule
#
# Also checks each issue's `evidence`: it must carry an executed check and its output
# ("<command> → <output>") or an explicit "not-checked: <reason>"; a bare quote fails.
#
# Exit codes:
#   0  valid (single file), or valid pair with no hold triggered
#   1  invalid/malformed verdict, missing file, or bad usage
#   2  valid pair that is a repeat fail, HOLD, queue for Graham
#
# Runnable from any directory; takes absolute or relative paths to verdict files.

set -u

get_field() {
  # $1 = file, $2 = top-level field name -> prints the scalar value on that line
  awk -v f="$2" '
    $0 ~ "^" f ":" {
      sub("^" f ":[ ]*", "");
      gsub(/^"|"$/, "");
      print;
      exit
    }
  ' "$1"
}

validate_one() {
  local file="$1"
  local ok=1

  if [ ! -f "$file" ]; then
    echo "FAIL $file: file not found"
    return 1
  fi

  local shape target result severity confidence new_info
  shape=$(get_field "$file" "verdict")
  target=$(get_field "$file" "target")
  result=$(get_field "$file" "result")
  severity=$(get_field "$file" "severity")
  confidence=$(get_field "$file" "confidence")
  new_info=$(get_field "$file" "new_information")

  [ -z "$shape" ]      && { echo "FAIL $file: missing required field 'verdict' (shape/version)"; ok=0; }
  [ -z "$target" ]     && { echo "FAIL $file: missing required field 'target'"; ok=0; }
  [ -z "$result" ]     && { echo "FAIL $file: missing required field 'result'"; ok=0; }
  [ -z "$severity" ]   && { echo "FAIL $file: missing required field 'severity'"; ok=0; }
  [ -z "$confidence" ] && { echo "FAIL $file: missing required field 'confidence'"; ok=0; }
  [ -z "$new_info" ]   && { echo "FAIL $file: missing required field 'new_information'"; ok=0; }

  if [ -n "$result" ] && [ "$result" != "pass" ] && [ "$result" != "fail" ]; then
    echo "FAIL $file: result '$result' not in {pass, fail}"
    ok=0
  fi

  if [ -n "$severity" ]; then
    case "$severity" in
      none|low|medium|high) ;;
      *) echo "FAIL $file: severity '$severity' not in {none, low, medium, high}"; ok=0 ;;
    esac
  fi

  if [ -n "$confidence" ]; then
    if ! awk -v c="$confidence" 'BEGIN { if ((c+0) < 0 || (c+0) > 1) exit 1; else exit 0 }' < /dev/null; then
      echo "FAIL $file: confidence '$confidence' not in 0..1"
      ok=0
    fi
  fi

  if [ -n "$new_info" ] && [ "$new_info" != "true" ] && [ "$new_info" != "false" ]; then
    echo "FAIL $file: new_information '$new_info' not a boolean (true|false)"
    ok=0
  fi

  # issues must be empty iff result is pass
  local issue_count
  issue_count=$(grep -c '^\s*-\s*id:' "$file")
  if [ "$result" = "pass" ] && [ "$issue_count" -ne 0 ]; then
    echo "FAIL $file: result is pass but issues has $issue_count entries (must be empty)"
    ok=0
  fi
  if [ "$result" = "fail" ] && [ "$issue_count" -eq 0 ]; then
    echo "FAIL $file: result is fail but issues is empty (must be non-empty)"
    ok=0
  fi

  # Every issue's evidence names an executed check and its output ("<command> → <output>"),
  # or says outright that nothing was run ("not-checked: <reason>"). A bare quote is an
  # opinion with a citation, not evidence (self-review 2026-09-18, TIGHTEN).
  local bad_evidence
  bad_evidence=$(awk '
    /^[[:space:]]*evidence:/ {
      sub(/^[[:space:]]*evidence:[[:space:]]*/, ""); gsub(/^"|"$/, "");
      if ($0 ~ /(→|->)/ || $0 ~ /^not-checked:[[:space:]]*[^[:space:]]/) next;
      print
    }' "$file")
  if [ -n "$bad_evidence" ]; then
    while IFS= read -r line; do
      echo "FAIL $file: issue evidence names no executed check output (needs '<command> → <output>' or 'not-checked: <reason>'): $line"
    done <<< "$bad_evidence"
    ok=0
  fi

  if [ "$ok" -eq 1 ]; then
    echo "OK $file: valid Verdict object v1 (target=$target result=$result severity=$severity confidence=$confidence new_information=$new_info issues=$issue_count)"
    return 0
  fi
  return 1
}

main() {
  if [ "$#" -eq 1 ]; then
    validate_one "$1"
    exit $?
  fi

  if [ "$#" -eq 2 ]; then
    local r1 r2
    validate_one "$1"; r1=$?
    validate_one "$2"; r2=$?
    if [ "$r1" -ne 0 ] || [ "$r2" -ne 0 ]; then
      echo "FAIL: one or both verdicts invalid, cannot apply the hold rule"
      exit 1
    fi

    local result1 result2 new_info2
    result1=$(get_field "$1" "result")
    result2=$(get_field "$2" "result")
    new_info2=$(get_field "$2" "new_information")

    if [ "$result1" = "fail" ] && [ "$result2" = "fail" ] && [ "$new_info2" = "false" ]; then
      echo "HOLD: second verdict is a fail with new_information: false, repeat fail, hold the target and queue for Graham"
      exit 2
    fi

    echo "OK: pair valid, no repeat-fail hold triggered (result1=$result1 result2=$result2 new_information[2]=$new_info2)"
    exit 0
  fi

  echo "usage: $0 <verdict-file> [<second-verdict-file>]" >&2
  exit 1
}

main "$@"
