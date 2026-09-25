#!/usr/bin/env bash
# prove-brand-gate.sh: deliberate-failure proof for scripts/brand-gate.py. FIXTURE data
# only: copies the gate into a temp dir with a denylist holding the hash of one fixture
# word, then asserts which lines it fails and which it lets through. The real denylist
# is never read, so no denied word appears in this file or its output.
# Usage: bash maintainers/scripts/prove-brand-gate.sh   (from any directory)
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mkdir -p "$T/scripts" "$T/maintainers/brand-gate"
cp "$HERE/../../scripts/brand-gate.py" "$T/scripts/"
printf '%s\n' "$(printf '%s' fixturecorp | sha256sum | cut -d' ' -f1)" \
  "$(printf '%s' fixture-voice | sha256sum | cut -d' ' -f1)" \
  > "$T/maintainers/brand-gate/denylist.sha256"
printf 'reviewword\n' > "$T/maintainers/brand-gate/review-flags.txt"
fail=0
check() { # check <expect-exit> <label> <text>
  local rc
  printf '%s\n' "$3" | python3 "$T/scripts/brand-gate.py" --text >/dev/null 2>&1; rc=$?
  if [ "$rc" -eq "$1" ]; then echo "PASS  exit $rc  $2"
  else echo "FAIL  expected exit $1, got $rc  $2"; fail=1; fi
}
check 1 "denied word, other case"            "Built for FixtureCorp"
check 1 "denied word inside a CSS token"     "--fixturecorp-accent: red;"
check 1 "denied word split across two words" "a Fixture Corp deck"
check 1 "denied hyphenated term"             "see fixture-voice first"
check 0 "denied word as part of a longer word" "fixturecorporation"
check 1 "AWS account id in an ARN"           "arn:aws:iam::$(printf %s%s 123456 789012):role/x"
check 0 "UUID last group"                    "550e8400-e29b-41d4-a716-446655440000"
check 0 "touch -t timestamp"                 "touch -t 202609010000 a.txt"
check 0 "review flag only warns"             "one reviewword here"
check 0 "clean text"                         "nothing to see"
if [ "$fail" -eq 0 ]; then echo "prove-brand-gate: all cases PASS"; else echo "prove-brand-gate: FAIL"; exit 1; fi
