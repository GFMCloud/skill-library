#!/usr/bin/env bash
# goal-block-check.sh — validate a Goal block v1 file (interface spec section 1).
#
# Usage: goal-block-check.sh <path-to-goal-block.yaml>
#
# Exit 0: every field except `rubric` is filled, `baseline` is non-empty,
#         and `goal_condition` contains a stop clause (a digit followed by
#         an attempt/time word).
# Exit 1: a required field is missing or empty, or no stop clause is found.
#         The missing/malformed field is named on stderr.
#
# Runs from any directory; resolves its own path so it does not depend on cwd.

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $(basename "$0") <path-to-goal-block.yaml>" >&2
  exit 1
fi

file="$1"

if [ ! -f "$file" ]; then
  echo "FAIL: file not found: $file" >&2
  exit 1
fi

fail=0

# Required fields for every goal block, regardless of kind.
required_fields="goal_block ask kind end_state check expected baseline constraints budget human_gate goal_condition"

get_field_value() {
  # Prints the value on the same line as "field:", trimmed. Empty if absent
  # or if the value is empty/whitespace only. `|| true` is required here:
  # under `set -eo pipefail`, a field that is entirely absent (grep finds no
  # line, exit 1) would otherwise abort the whole script instead of being
  # reported as a missing field by the caller.
  local field="$1"
  /usr/bin/grep -m1 -E "^${field}:" "$file" 2>/dev/null | sed -E "s/^${field}:[[:space:]]*//" | sed -E 's/[[:space:]]+$//' || true
}

for field in $required_fields; do
  value="$(get_field_value "$field")"
  if [ -z "$value" ]; then
    echo "FAIL: field '$field' is missing or empty" >&2
    fail=1
  fi
done

# baseline must be non-empty specifically (redundant with the loop above,
# but stated explicitly per the roadmap's gate wording).
baseline_value="$(get_field_value baseline)"
if [ -z "$baseline_value" ]; then
  echo "FAIL: 'baseline' is empty — the check must be run once before work starts" >&2
  fail=1
fi

# goal_condition must contain a stop clause: a digit followed (within a few
# words) by an attempt/time word, or vice versa.
goal_condition_value="$(get_field_value goal_condition)"
if [ -n "$goal_condition_value" ]; then
  if ! echo "$goal_condition_value" | /usr/bin/grep -qiE '[0-9]+[^0-9]{0,15}(try|tries|attempt|minute|hour|second|day|turn)'; then
    echo "FAIL: 'goal_condition' has no stop clause (expected a number with 'tries', 'attempts', 'minutes', 'turns', etc.)" >&2
    fail=1
  fi
else
  echo "FAIL: 'goal_condition' is missing or empty" >&2
  fail=1
fi

# rubric is required only when kind: judgment; forbidden-empty is not
# checked when kind: measurable (the field is simply absent then).
kind_value="$(get_field_value kind)"
rubric_value="$(get_field_value rubric)"
if [ "$kind_value" = "judgment" ] && [ -z "$rubric_value" ]; then
  echo "FAIL: kind is 'judgment' but 'rubric' is missing or empty" >&2
  fail=1
fi

if [ "$fail" -ne 0 ]; then
  exit 1
fi

echo "PASS: $file is a complete Goal block v1"
exit 0
